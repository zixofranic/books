"""
render_sections.py — per-section audiobook renderer for any book on
Chatterbox. Splits each chapter's _tts.txt into sections (by trailing-
ellipsis heading cues), renders each as a separate WAV, then concats the
sections into the final chapter WAV/MP3. Reduces per-mistake iteration
cost from ~25 min (whole chapter) to ~5 min (one section).

Book-agnostic. Each book provides:
  - source/<stem>_tts.txt files (from tts_normalize.py)
  - shared voices module at ../voices.py

Output layout (under <book>/audio_v2/, overridable via BOOKS_AUDIO_DIR):
  <stem>.mp3                       final chapter (concat of sections)
  <stem>.wav
  sections/<stem>/
    _manifest.json                 per-chapter section manifest
    NN_<slug>.wav                  per-section audio
  listening/<stem>.md              timestamps companion (mm:ss + section title)

Usage:
  python render_sections.py prep <book_dir>
        Analyze _tts.txt files, write section manifests. Detects stale
        sections via SHA hash of section text — if you edit a section's
        text, the manifest marks it for re-render on next `render`.

  python render_sections.py render <book_dir> [<chapter_stem>]
        Render all pending sections. With <chapter_stem>, just that chapter.
        Auto-assembles chapters once all their sections are rendered.

  python render_sections.py section <book_dir> <chapter_stem> <slug>
        Re-render one specific section (e.g. after editing its text).
        Auto-assembles the chapter when all sections are rendered.

  python render_sections.py assemble <book_dir> [<chapter_stem>]
        Concat sections into final chapter WAV+MP3. Writes listening
        companion file.

  python render_sections.py status <book_dir>
        Show status grid: per chapter, which sections are rendered,
        whether assembled, total duration.

  python render_sections.py all <book_dir>
        prep + render + assemble. Recommended top-level command.

<book_dir> can be a relative book slug (e.g. "just_predicting_words") or
an absolute path. Relative slugs resolve against this script's directory.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

THIS_DIR = Path(__file__).parent
sys.path.insert(0, str(THIS_DIR))
import voices  # noqa: E402

CHATTERBOX_URL = "http://localhost:8004"
DEFAULT_VOICE = "burton"

# Pattern: a section heading is a line that ends in "..." (the inline pause
# cue we add to chapter labels, chapter titles, and ALL-CAPS section breaks
# during tts_normalize). The standalone "..." pause-line form is NOT used
# (it caused CB to vocalize a phantom letter — see C:/AI/books/CLAUDE.md
# "Pause cues" section) so we don't need to disambiguate.
ELLIPSIS_TRAILING = re.compile(r"\.\.\.$")
CHAPTER_LABEL_PATTERN = re.compile(r"^Chapter\s+[A-Z][a-z]+\.\.\.$")

STOP_WORDS = {"the", "a", "an", "of"}  # used only to shorten over-long slugs


# =============================================================================
# Section parsing
# =============================================================================

def slugify(title: str) -> str:
    """Title → filename-safe snake_case. Trims to 40 chars, drops stop
    words if needed to stay under the limit."""
    s = title.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    if len(s) > 40:
        parts = [p for p in s.split("_") if p not in STOP_WORDS]
        s = "_".join(parts)[:40].rstrip("_")
    return s or "section"


def parse_sections(tts_text: str) -> list:
    """Split a _tts.txt into ordered sections.

    Returns list of {"slug", "title", "text"} dicts. First section is
    always "intro" for chapter files (chapter label + title + body
    through the first section heading). For files without a chapter
    structure (front matter, short closing, glossaries), returns a
    single "body" section.

    Detection: lines ending with "..." are structural markers (from
    `tts_normalize.py`'s trailing-ellipsis pause cue). First marker
    matching CHAPTER_LABEL_PATTERN ("Chapter Seven...") is the chapter
    label; the marker immediately after is the chapter title; subsequent
    markers are section breaks.
    """
    lines = tts_text.split("\n")
    marker_idxs = []
    for i, line in enumerate(lines):
        s = line.strip()
        if s == "...":
            continue  # defensive: shouldn't appear, standalone pause is banned
        if ELLIPSIS_TRAILING.search(s):
            marker_idxs.append(i)

    # Single-section cases: too few markers (no structure) or too many
    # (glossary-shaped — would produce 40+ tiny sections, defeating the
    # iteration-cost benefit).
    if len(marker_idxs) <= 1 or len(marker_idxs) > 15:
        return [{
            "slug": "body",
            "title": _first_meaningful_line(lines) or "Body",
            "text": tts_text.strip(),
        }]

    first_text = lines[marker_idxs[0]].strip()
    has_chapter_label = bool(CHAPTER_LABEL_PATTERN.match(first_text))

    if has_chapter_label and len(marker_idxs) >= 3:
        section_marker_idxs = marker_idxs[2:]
        chapter_title = lines[marker_idxs[1]].strip().rstrip(".")
        intro_title = chapter_title or "Intro"
    elif has_chapter_label:
        # Chapter label + title but no body sections — render as one piece
        return [{
            "slug": "intro",
            "title": lines[marker_idxs[1]].strip().rstrip(".") if len(marker_idxs) > 1 else "Intro",
            "text": tts_text.strip(),
        }]
    else:
        # No chapter label — every marker is a section break
        section_marker_idxs = marker_idxs
        intro_title = "Intro"

    sections = []
    intro_end = section_marker_idxs[0]
    sections.append({
        "slug": "intro",
        "title": intro_title,
        "text": "\n".join(lines[:intro_end]).strip(),
    })
    for i, marker_idx in enumerate(section_marker_idxs):
        next_idx = section_marker_idxs[i + 1] if i + 1 < len(section_marker_idxs) else len(lines)
        title_line = lines[marker_idx].strip().rstrip(".")
        sections.append({
            "slug": slugify(title_line),
            "title": title_line,
            "text": "\n".join(lines[marker_idx:next_idx]).strip(),
        })
    return sections


def _first_meaningful_line(lines):
    for line in lines:
        s = line.strip()
        if s and s != "...":
            return s.rstrip(".")
    return None


# =============================================================================
# Render helpers (CB synth + atempo + silence_cap + mp3)
# =============================================================================
# Duplicated from <book>/batch_render.py. If a third book starts using CB,
# extract into a shared cb_render_lib.py. Two copies isn't worth the
# abstraction overhead.

def add_pause_hints(text: str) -> str:
    text = text.replace(" — ", "... ").replace("—", "... ")
    text = text.replace(". ", ".  ")
    text = text.replace(", ", ",  ")
    return text


def chatterbox_clone(text: str, ref_filename: str, out_path: Path) -> float:
    import requests
    payload = {
        "text": text, "voice_mode": "clone",
        "reference_audio_filename": ref_filename,
        "output_format": "wav", "split_text": True, "chunk_size": 240,
        "temperature": 0.75, "exaggeration": 0.5, "cfg_weight": 0.5,
        "speed_factor": 1.0, "seed": 4242, "language": "en",
    }
    t0 = time.time()
    resp = requests.post(f"{CHATTERBOX_URL}/tts", json=payload, timeout=3600)
    elapsed = time.time() - t0
    resp.raise_for_status()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(resp.content)
    return elapsed


def atempo(in_path: Path, out_path: Path, factor: float) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(in_path), "-filter:a", f"atempo={factor}", str(out_path)],
        check=True, capture_output=True,
    )


def silence_cap(in_path: Path, out_path: Path, stop_silence: float,
                stop_duration: float = 1.5) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(in_path), "-af",
         f"silenceremove=stop_periods=-1:stop_duration={stop_duration}:"
         f"stop_silence={stop_silence}:stop_threshold=-40dB",
         str(out_path)],
        check=True, capture_output=True,
    )


def to_mp3(in_path: Path, out_path: Path) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(in_path),
         "-c:a", "libmp3lame", "-b:a", "128k", "-ac", "1", str(out_path)],
        check=True, capture_output=True,
    )


def probe_duration(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        check=True, capture_output=True, text=True,
    )
    return float(r.stdout.strip())


# =============================================================================
# Manifest
# =============================================================================

def section_hash(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]


def audio_dir(book_dir: Path) -> Path:
    override = os.environ.get("BOOKS_AUDIO_DIR")
    return book_dir / override if override else book_dir / "audio_v2"


def section_dir(book_dir: Path, chapter_stem: str) -> Path:
    return audio_dir(book_dir) / "sections" / chapter_stem


def manifest_path(book_dir: Path, chapter_stem: str) -> Path:
    return section_dir(book_dir, chapter_stem) / "_manifest.json"


def load_manifest(book_dir: Path, chapter_stem: str) -> dict:
    mp = manifest_path(book_dir, chapter_stem)
    if mp.exists():
        return json.loads(mp.read_text(encoding="utf-8"))
    return {
        "chapter": chapter_stem,
        "voice": DEFAULT_VOICE,
        "sections": [],
        "chapter_assembled": False,
        "chapter_duration_sec": None,
    }


def save_manifest(book_dir: Path, chapter_stem: str, m: dict) -> None:
    mp = manifest_path(book_dir, chapter_stem)
    mp.parent.mkdir(parents=True, exist_ok=True)
    mp.write_text(json.dumps(m, indent=2), encoding="utf-8")


def recompute_start_times(m: dict) -> None:
    """Fill in start_in_chapter for each section based on cumulative
    duration of rendered prior sections."""
    cum = 0.0
    for s in m["sections"]:
        if s.get("rendered") and s.get("duration_sec") is not None:
            s["start_in_chapter"] = round(cum, 1)
            cum += s["duration_sec"]
        else:
            s["start_in_chapter"] = None


# =============================================================================
# File discovery
# =============================================================================

def find_tts_files(book_dir: Path) -> list:
    return sorted((book_dir / "source").glob("*_tts.txt"))


def chapter_stem_from_tts(tts_path: Path) -> str:
    stem = tts_path.stem
    return stem[:-len("_tts")] if stem.endswith("_tts") else stem


def resolve_book_dir(arg: str) -> Path:
    """Accept absolute path or relative book slug."""
    p = Path(arg)
    if p.is_absolute() and p.exists():
        return p
    candidate = THIS_DIR / arg
    if candidate.exists():
        return candidate
    return p.resolve()


# =============================================================================
# Prep — build section manifests, detect stale text via hash
# =============================================================================

def prep(book_dir: Path) -> None:
    tts_files = find_tts_files(book_dir)
    print(f"=== prep: {len(tts_files)} _tts.txt files in {book_dir.name} ===")
    for tts_path in tts_files:
        stem = chapter_stem_from_tts(tts_path)
        text = tts_path.read_text(encoding="utf-8")
        sections = parse_sections(text)
        m = load_manifest(book_dir, stem)
        existing_by_slug = {s["slug"]: s for s in m["sections"]}
        new_sections = []
        stale_slugs = []
        for idx, sec in enumerate(sections, start=1):
            h = section_hash(sec["text"])
            existing = existing_by_slug.get(sec["slug"])
            if existing and existing.get("text_hash") == h:
                existing["idx"] = idx
                existing["title"] = sec["title"]
                existing["char_count"] = len(sec["text"])
                new_sections.append(existing)
            else:
                new_sections.append({
                    "idx": idx,
                    "slug": sec["slug"],
                    "title": sec["title"],
                    "text_hash": h,
                    "char_count": len(sec["text"]),
                    "rendered": False,
                    "rendered_at": None,
                    "synth_sec": None,
                    "duration_sec": None,
                    "start_in_chapter": None,
                })
                if existing:
                    stale_slugs.append(sec["slug"])
        m["sections"] = new_sections
        recompute_start_times(m)
        if any(not s["rendered"] for s in m["sections"]):
            m["chapter_assembled"] = False
        save_manifest(book_dir, stem, m)
        n_total = len(m["sections"])
        n_done = sum(1 for s in m["sections"] if s["rendered"])
        stale_note = f"  STALE: {','.join(stale_slugs)}" if stale_slugs else ""
        print(f"  {stem:<32} {n_done}/{n_total} sections rendered{stale_note}")


# =============================================================================
# Render a section
# =============================================================================

def render_section(book_dir: Path, chapter_stem: str, section_idx: int,
                   voice_name: str = None) -> None:
    m = load_manifest(book_dir, chapter_stem)
    if not m["sections"]:
        raise RuntimeError(f"no manifest for {chapter_stem}; run prep first")
    voice = voices.get(voice_name or m.get("voice", DEFAULT_VOICE))
    sec = next((s for s in m["sections"] if s["idx"] == section_idx), None)
    if sec is None:
        raise RuntimeError(f"section idx {section_idx} not found in {chapter_stem}")

    # Re-read source in case it changed since last prep
    tts_path = book_dir / "source" / f"{chapter_stem}_tts.txt"
    parsed = parse_sections(tts_path.read_text(encoding="utf-8"))
    match = next((s for s in parsed if s["slug"] == sec["slug"]), None)
    if not match:
        raise RuntimeError(f"section {sec['slug']!r} no longer in source; re-run prep")
    text = match["text"]
    sec["text_hash"] = section_hash(text)
    sec["char_count"] = len(text)

    sec_dir = section_dir(book_dir, chapter_stem)
    raw_dir = sec_dir / "_raw_pre_atempo"
    silcap_dir = sec_dir / "_raw_pre_silcap"
    filename = f"{sec['idx']:02d}_{sec['slug']}.wav"
    raw = raw_dir / filename
    stretched = silcap_dir / filename if voice.silence_cap else sec_dir / filename
    final_wav = sec_dir / filename

    print(f"  [render] {chapter_stem}/{filename}  ({len(text)} chars)")
    hinted = add_pause_hints(text)
    t0 = time.time()
    synth = chatterbox_clone(hinted, voice.ref_filename, raw)
    atempo(raw, stretched, voice.atempo)
    if voice.silence_cap:
        silence_cap(stretched, final_wav, voice.stop_silence, voice.stop_duration)
    duration = probe_duration(final_wav)

    sec["rendered"] = True
    sec["rendered_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    sec["synth_sec"] = round(synth, 1)
    sec["duration_sec"] = round(duration, 1)
    recompute_start_times(m)
    m["chapter_assembled"] = False
    save_manifest(book_dir, chapter_stem, m)
    print(f"    -> {duration:.1f}s ({duration/60:.1f} min) in {time.time()-t0:.0f}s")


def render_pending(book_dir: Path, only_stem: str = None) -> None:
    for tts_path in find_tts_files(book_dir):
        stem = chapter_stem_from_tts(tts_path)
        if only_stem and stem != only_stem:
            continue
        m = load_manifest(book_dir, stem)
        if not m["sections"]:
            continue
        for sec in m["sections"]:
            if sec["rendered"]:
                continue
            try:
                render_section(book_dir, stem, sec["idx"])
            except Exception as e:
                print(f"  !! FAILED {stem}/{sec['slug']}: {e}")


# =============================================================================
# Assemble — ffmpeg concat sections into final chapter
# =============================================================================

def assemble_chapter(book_dir: Path, chapter_stem: str) -> None:
    m = load_manifest(book_dir, chapter_stem)
    if not m["sections"]:
        print(f"  [skip] {chapter_stem}: no manifest")
        return
    missing = [s["slug"] for s in m["sections"] if not s["rendered"]]
    if missing:
        print(f"  [skip assemble] {chapter_stem}: {len(missing)} section(s) not rendered ({', '.join(missing[:3])}...)")
        return

    sec_dir = section_dir(book_dir, chapter_stem)
    concat_list = sec_dir / "_concat.txt"
    # ffmpeg concat demuxer resolves paths in the list RELATIVE TO THE LIST
    # FILE's directory, not cwd. So write just basenames here — the WAVs sit
    # next to the _concat.txt file.
    with open(concat_list, "w", encoding="utf-8") as f:
        for sec in m["sections"]:
            filename = f"{sec['idx']:02d}_{sec['slug']}.wav"
            f.write(f"file '{filename}'\n")

    final_wav = audio_dir(book_dir) / f"{chapter_stem}.wav"
    final_mp3 = audio_dir(book_dir) / f"{chapter_stem}.mp3"
    final_wav.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
         "-i", str(concat_list), "-c", "copy", str(final_wav)],
        check=True, capture_output=True,
    )
    to_mp3(final_wav, final_mp3)
    duration = probe_duration(final_wav)
    m["chapter_assembled"] = True
    m["chapter_duration_sec"] = round(duration, 1)
    m["assembled_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    recompute_start_times(m)
    save_manifest(book_dir, chapter_stem, m)
    write_listening_md(book_dir, chapter_stem)
    print(f"  [assembled] {chapter_stem} -> {duration/60:.1f} min, "
          f"{final_mp3.stat().st_size/1024/1024:.1f} MB mp3")


# =============================================================================
# Listening companion file
# =============================================================================

def fmt_mmss(seconds) -> str:
    if seconds is None:
        seconds = 0
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"


def write_listening_md(book_dir: Path, chapter_stem: str) -> None:
    m = load_manifest(book_dir, chapter_stem)
    if not m["sections"]:
        return
    listening_dir = audio_dir(book_dir) / "listening"
    listening_dir.mkdir(parents=True, exist_ok=True)
    out = listening_dir / f"{chapter_stem}.md"

    chapter_title = m["sections"][0]["title"] if m["sections"] else chapter_stem
    lines = [f"# {chapter_stem} — {chapter_title}"]
    if m.get("chapter_duration_sec"):
        lines.append(f"Total: {fmt_mmss(m['chapter_duration_sec'])}")
    lines.append("")
    lines.append("| Time  | Section                          | File |")
    lines.append("|-------|----------------------------------|------|")
    for sec in m["sections"]:
        start = sec.get("start_in_chapter") or 0.0
        fname = f"{sec['idx']:02d}_{sec['slug']}.wav"
        lines.append(f"| {fmt_mmss(start)} | {sec['title']:<32} | `sections/{chapter_stem}/{fname}` |")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


# =============================================================================
# Status
# =============================================================================

def status(book_dir: Path) -> None:
    print(f"=== status: {book_dir.name} ===")
    print(f"{'chapter':<32} done/tot  grid                       asm  duration")
    print("-" * 90)
    for tts_path in find_tts_files(book_dir):
        stem = chapter_stem_from_tts(tts_path)
        m = load_manifest(book_dir, stem)
        if not m["sections"]:
            print(f"{stem:<32} (run prep)")
            continue
        n_total = len(m["sections"])
        n_done = sum(1 for s in m["sections"] if s["rendered"])
        grid = "".join("X" if s["rendered"] else "." for s in m["sections"])
        asm = "X" if m["chapter_assembled"] else " "
        dur = fmt_mmss(m.get("chapter_duration_sec")) if m.get("chapter_duration_sec") else "—"
        print(f"{stem:<32} {n_done}/{n_total:<5} {grid:<25}  {asm}    {dur}")


# =============================================================================
# CLI
# =============================================================================

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    cmd = sys.argv[1]

    if cmd in ("help", "-h", "--help"):
        print(__doc__)
        return

    if len(sys.argv) < 3:
        print(f"usage: python render_sections.py {cmd} <book_dir>")
        return
    book_dir = resolve_book_dir(sys.argv[2])
    if not book_dir.exists():
        print(f"book directory not found: {book_dir}")
        return

    if cmd == "status":
        status(book_dir)
        return

    if cmd == "prep":
        prep(book_dir)
        return

    if cmd == "render":
        only = sys.argv[3] if len(sys.argv) >= 4 else None
        render_pending(book_dir, only_stem=only)
        # Auto-assemble any chapter whose sections are all rendered
        for tts_path in find_tts_files(book_dir):
            stem = chapter_stem_from_tts(tts_path)
            if only and stem != only:
                continue
            m = load_manifest(book_dir, stem)
            if m["sections"] and all(s["rendered"] for s in m["sections"]) and not m["chapter_assembled"]:
                assemble_chapter(book_dir, stem)
        return

    if cmd == "section":
        if len(sys.argv) < 5:
            print("usage: python render_sections.py section <book_dir> <chapter_stem> <slug>")
            return
        stem = sys.argv[3]
        slug = sys.argv[4]
        m = load_manifest(book_dir, stem)
        match = next((s for s in m["sections"] if s["slug"] == slug), None)
        if not match:
            print(f"section {slug!r} not found in {stem}; available: "
                  f"{[s['slug'] for s in m['sections']]}")
            return
        render_section(book_dir, stem, match["idx"])
        m = load_manifest(book_dir, stem)
        if all(s["rendered"] for s in m["sections"]):
            assemble_chapter(book_dir, stem)
        return

    if cmd == "assemble":
        if len(sys.argv) >= 4:
            assemble_chapter(book_dir, sys.argv[3])
        else:
            for tts_path in find_tts_files(book_dir):
                assemble_chapter(book_dir, chapter_stem_from_tts(tts_path))
        return

    if cmd == "all":
        prep(book_dir)
        render_pending(book_dir)
        for tts_path in find_tts_files(book_dir):
            stem = chapter_stem_from_tts(tts_path)
            m = load_manifest(book_dir, stem)
            if m["sections"] and all(s["rendered"] for s in m["sections"]) and not m["chapter_assembled"]:
                assemble_chapter(book_dir, stem)
        status(book_dir)
        return

    print(f"unknown command: {cmd}")
    print(__doc__)


if __name__ == "__main__":
    main()
