"""
Batch renderer for the just-predicting-words audiobook.

Renders cleaned chapter files to WAV + MP3 in groups of 5 (configurable).
Resumable: skips files that already have a `.mp3` in `audio/`.

Usage:
  python batch_render.py 1            # render group 1 only
  python batch_render.py 1 2 3        # render groups 1, 2, and 3
  python batch_render.py all          # render everything not yet done
  python batch_render.py status       # print render status without rendering
  python batch_render.py list         # print the render order

After each file: synth via burton voice → atempo 0.89 → silence_cap 0.7 →
mp3 conversion at 128kbps mono. Logs duration + silence count per file
to `audio/_manifest.json`.
"""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import voices  # noqa: E402

BOOK_DIR = Path(__file__).parent
SOURCE_DIR = BOOK_DIR / "source"
# Output dir overridable via env var so we can render alternate cuts
# (e.g. BOOKS_AUDIO_DIR=audio_v2 for the TTS-normalized re-record) without
# overwriting the original audio.
_AUDIO_OVERRIDE = os.environ.get("BOOKS_AUDIO_DIR")
AUDIO_DIR = BOOK_DIR / _AUDIO_OVERRIDE if _AUDIO_OVERRIDE else BOOK_DIR / "audio"
RAW_PRE_ATEMPO = AUDIO_DIR / "_raw_pre_atempo"
RAW_PRE_SILCAP = AUDIO_DIR / "_raw_pre_silcap"
MANIFEST = AUDIO_DIR / "_manifest.json"

CHATTERBOX_URL = "http://localhost:8004"
DEFAULT_VOICE = "burton"
GROUP_SIZE = 5

# Render order — explicit so audiobook flows naturally regardless of
# alphabetic file naming. Names match the *_clean.txt files in source/.
# Ch 7 is intentionally first when starting a fresh render batch so the
# user gets fastest validation (it was the chapter where the original CB
# render botched "2025" as "two zero two five"). Once ch 7 lands and
# sounds right, the rest renders in narrative order.
RENDER_ORDER = [
    "07_chapter_07_clean",
    "00_opening_credits_clean",
    "00_dedication_clean",
    "00_author_note_FINAL_clean",
    "01_chapter_01_clean", "02_chapter_02_clean", "03_chapter_03_clean",
    "04_chapter_04_clean", "05_chapter_05_clean", "06_chapter_06_clean",
    "08_chapter_08_clean", "09_chapter_09_clean",
    "10_chapter_10_clean", "11_chapter_11_clean", "12_chapter_12_clean",
    "13_chapter_13_clean", "14_chapter_14_clean", "15_chapter_15_clean",
    "16_chapter_16_clean", "17_chapter_17_clean", "18_chapter_18_clean",
    "19_chapter_19_clean", "20_chapter_20_clean", "21_chapter_21_clean",
    "22_appendix_A_clean", "23_appendix_B_clean", "24_appendix_C_clean",
    "00_author_bio_FINAL_clean",
    "99_closing_clean",
]


def out_stem(clean_stem: str) -> str:
    """Strip the trailing `_clean` so audio file naming tracks the chapter."""
    return clean_stem[:-len("_clean")] if clean_stem.endswith("_clean") else clean_stem


def add_pause_hints(text: str) -> str:
    text = text.replace(" — ", "... ").replace("—", "... ")
    text = text.replace(". ", ".  ")
    text = text.replace(", ", ",  ")
    return text


def chatterbox_clone(text: str, ref_filename: str, out_path: Path) -> float:
    import requests
    payload = {
        "text": text,
        "voice_mode": "clone",
        "reference_audio_filename": ref_filename,
        "output_format": "wav",
        "split_text": True,
        "chunk_size": 240,
        "temperature": 0.75,
        "exaggeration": 0.5,
        "cfg_weight": 0.5,
        "speed_factor": 1.0,
        "seed": 4242,
        "language": "en",
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
        ["ffmpeg", "-y", "-i", str(in_path), "-filter:a", f"atempo={factor}",
         str(out_path)],
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
         "-c:a", "libmp3lame", "-b:a", "128k", "-ac", "1",
         str(out_path)],
        check=True, capture_output=True,
    )


def probe_duration(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        check=True, capture_output=True, text=True,
    )
    return float(r.stdout.strip())


def count_silences(path: Path, min_seconds: float) -> int:
    r = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(path), "-af",
         f"silencedetect=noise=-40dB:d={min_seconds}", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    return len(re.findall(r"silence_duration:", r.stderr))


def load_manifest() -> dict:
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {"voice": DEFAULT_VOICE, "files": {}}


def save_manifest(m: dict) -> None:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(m, indent=2), encoding="utf-8")


def render_one(clean_stem: str, voice_name: str, manifest: dict) -> None:
    voice = voices.get(voice_name)
    # Prefer _tts.txt (phonetically normalized for CB) over _clean.txt. The
    # _tts.txt files are produced by tts_normalize.py and fix years, brands,
    # acronyms, and structural pause cues for section headings.
    tts_stem = clean_stem.replace("_clean", "_tts") if clean_stem.endswith("_clean") else clean_stem
    tts_src = SOURCE_DIR / f"{tts_stem}.txt"
    clean_src = SOURCE_DIR / f"{clean_stem}.txt"
    src = tts_src if tts_src.exists() else clean_src
    if not src.exists():
        print(f"  SKIP missing source: {clean_src.name}")
        return
    if src is tts_src:
        print(f"  using TTS-normalized source: {src.name}")
    stem = out_stem(clean_stem)
    raw = RAW_PRE_ATEMPO / f"{stem}.wav"
    if voice.silence_cap:
        stretched = RAW_PRE_SILCAP / f"{stem}.wav"
    else:
        stretched = AUDIO_DIR / f"{stem}.wav"
    final_wav = AUDIO_DIR / f"{stem}.wav"
    final_mp3 = AUDIO_DIR / f"{stem}.mp3"

    if final_mp3.exists():
        print(f"  [skip] {stem}.mp3 already exists")
        return

    text = src.read_text(encoding="utf-8")
    word_count = len(text.split())
    char_count = len(text)
    print(f"  [render] {stem}  ({word_count} words, ~{char_count // 240 + 1} chunks)")

    text_hinted = add_pause_hints(text)
    t0 = time.time()
    synth = chatterbox_clone(text_hinted, voice.ref_filename, raw)
    atempo(raw, stretched, voice.atempo)
    if voice.silence_cap:
        silence_cap(stretched, final_wav, voice.stop_silence, voice.stop_duration)
    to_mp3(final_wav, final_mp3)
    total = time.time() - t0

    duration = probe_duration(final_wav)
    silences_long = count_silences(final_wav, 2.0)
    mp3_kb = final_mp3.stat().st_size / 1024

    manifest["files"][stem] = {
        "words": word_count,
        "synth_sec": round(synth, 1),
        "total_sec": round(total, 1),
        "duration_sec": round(duration, 1),
        "duration_mmss": f"{int(duration // 60)}m {int(duration % 60):02d}s",
        "silences_over_2s": silences_long,
        "mp3_kb": round(mp3_kb, 0),
    }
    save_manifest(manifest)
    print(f"    -> {duration/60:.1f} min,  {silences_long} silences>2s,  "
          f"{mp3_kb/1024:.1f} MB mp3,  total {total/60:.1f} min")


def groups() -> list[list[str]]:
    out = []
    for i in range(0, len(RENDER_ORDER), GROUP_SIZE):
        out.append(RENDER_ORDER[i:i + GROUP_SIZE])
    return out


def status() -> None:
    m = load_manifest()
    print(f"=== status (voice={m.get('voice', DEFAULT_VOICE)}) ===")
    for i, group in enumerate(groups(), 1):
        print(f"\n  group {i}:")
        for stem in group:
            out = out_stem(stem)
            mp3 = AUDIO_DIR / f"{out}.mp3"
            done = "X" if mp3.exists() else " "
            info = m.get("files", {}).get(out)
            extra = f"  {info['duration_mmss']}, {info['mp3_kb']/1024:.1f} MB" if info else ""
            print(f"    [{done}] {out}{extra}")


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        return

    if sys.argv[1] == "status":
        status()
        return
    if sys.argv[1] == "list":
        for i, group in enumerate(groups(), 1):
            print(f"group {i}:")
            for stem in group:
                print(f"  {stem}")
        return

    if sys.argv[1] == "all":
        targets = RENDER_ORDER
    else:
        try:
            group_indices = [int(a) for a in sys.argv[1:]]
        except ValueError:
            print(f"bad arg(s); want group numbers or 'all' or 'status'")
            return
        all_groups = groups()
        targets = []
        for gi in group_indices:
            if 1 <= gi <= len(all_groups):
                targets.extend(all_groups[gi - 1])
            else:
                print(f"  group {gi} out of range (1..{len(all_groups)})")

    voice_name = DEFAULT_VOICE
    manifest = load_manifest()
    manifest["voice"] = voice_name
    print(f"=== batch render: voice={voice_name}, {len(targets)} file(s) ===")
    for stem in targets:
        try:
            render_one(stem, voice_name, manifest)
        except Exception as e:
            print(f"  !! FAILED {stem}: {e}")
            manifest["files"][out_stem(stem)] = {"error": str(e)}
            save_manifest(manifest)
    print("=== done ===")
    status()


if __name__ == "__main__":
    main()
