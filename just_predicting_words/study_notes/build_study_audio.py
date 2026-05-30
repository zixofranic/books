"""
Assemble study_notes/*.md into TWO plain-text audio source parts.

Why two parts: render_sections.py's parse_sections collapses any stem with
more than 15 trailing-ellipsis markers into a single section (a guard
against glossary-shaped inputs that would produce 40+ tiny sections).
A single section render of all 24 chapters timed out. Splitting into two
parts keeps each stem at ~12 markers — comfortably under the cap, so each
chapter renders as its own section with per-section retry on failure.

Section marker convention (per render_sections.py):
    - Lines ending in '...' are structural markers.
    - A line matching ^Chapter [Word]\\.\\.\\.$ is the chapter LABEL.
    - We avoid that pattern by emitting just the chapter TITLE on the
      marker line ("Just Predicting Words..." not "Chapter One...").
      That way all markers are section breaks, none get consumed as
      "chapter label + title" pairs.

Output:
    audio_src/study_v1_part1_raw.txt   (chapters 1-12, ~100 min)
    audio_src/study_v1_part2_raw.txt   (chapters 13-21 + appendices, ~100 min)

Usage:
    python build_study_audio.py
"""
import re
import sys
from pathlib import Path

BOOK_DIR = Path(__file__).parent
OUT_DIR = BOOK_DIR / "audio_src"

CHAPTER_FILES = sorted(BOOK_DIR.glob("ch*.md"))
APPENDIX_FILES = sorted(BOOK_DIR.glob("app*.md"))

# Split point: chapters 1-12 vs chapters 13-21 + appendices A/B/C
PART1_FILES = CHAPTER_FILES[:12]                       # ch01..ch12
PART2_FILES = CHAPTER_FILES[12:] + APPENDIX_FILES      # ch13..ch21 + appA..C

PARTS = [
    ("study_v1_part1_raw.txt", "Just Predicting Words. Study Notes. Part one.", PART1_FILES),
    ("study_v1_part2_raw.txt", "Just Predicting Words. Study Notes. Part two.", PART2_FILES),
]


def strip_markdown(body_text: str) -> str:
    """Convert the chapter body (after the metadata block) into prose."""
    out_lines = []
    for raw in body_text.split("\n"):
        s = raw.rstrip()

        # Skip H1 (the chapter title — we emit it separately as the marker).
        if s.startswith("# "):
            continue

        # Skip metadata key/value lines we still see post-divider.
        if s.startswith("**Version:**") or s.startswith("**Source:**"):
            continue
        if s.startswith("**Last updated:**") or s.startswith("**Subtitle"):
            continue

        # H2 section header -> "Section. <name>." as PROSE (no '...', so
        # it's not a marker — just a spoken cue).
        if s.startswith("## "):
            name = s[3:].strip()
            name = re.sub(r"\*\*", "", name)
            out_lines.append("")
            out_lines.append(f"Section. {name}.")
            out_lines.append("")
            continue

        # H3 subsection — brief spoken cue, also not a marker.
        if s.startswith("### "):
            name = s[4:].strip()
            name = re.sub(r"\*\*", "", name)
            out_lines.append("")
            out_lines.append(f"{name}.")
            out_lines.append("")
            continue

        # Bullet -> prose sentence.
        stripped = s.lstrip()
        if stripped.startswith(("- ", "* ")):
            content = stripped[2:].strip()
            content = re.sub(r"\*\*(.+?)\*\*", r"\1", content)
            content = re.sub(r"\*(.+?)\*", r"\1", content)
            content = re.sub(r"`([^`]+)`", r"\1", content)
            if content and content[-1] not in ".!?":
                content += "."
            out_lines.append(content)
            continue

        # Remaining inline markdown.
        s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
        s = re.sub(r"\*(.+?)\*", r"\1", s)
        s = re.sub(r"`([^`]+)`", r"\1", s)
        out_lines.append(s)

    return "\n".join(out_lines)


def extract_marker(text: str) -> str:
    """Read the H1 line and emit a section-marker line.

    We deliberately drop the 'Chapter N' prefix and emit only the title
    + trailing '...' so the line is recognized as a marker but NOT as a
    CHAPTER_LABEL (which would consume it + the next marker as a
    label/title pair, breaking our 12-section structure).
    """
    first_line = text.split("\n", 1)[0]

    m = re.match(r"#\s*Chapter\s+\d+\s*—\s*(.+)", first_line)
    if m:
        return f"{m.group(1).strip()}..."

    m = re.match(r"#\s*Appendix\s+(\w+)\s*—\s*(.+)", first_line)
    if m:
        return f"Appendix {m.group(1)}. {m.group(2).strip()}..."

    return first_line.lstrip("#").strip() + "..."


def split_metadata(text: str) -> str:
    """Drop everything up to and including the first '---' divider."""
    parts = text.split("\n---\n", 1)
    return parts[1] if len(parts) == 2 else text


def assemble_part(preamble: str, files: list) -> str:
    pieces = [preamble, ""]
    for f in files:
        text = f.read_text(encoding="utf-8")
        marker = extract_marker(text)
        body = strip_markdown(split_metadata(text))
        body = re.sub(r"\n{3,}", "\n\n", body).strip()
        pieces.append("")
        pieces.append("")
        pieces.append(marker)
        pieces.append("")
        pieces.append(body)
    pieces.append("")
    return re.sub(r"\n{3,}", "\n\n", "\n".join(pieces))


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    total_words = 0
    for out_name, preamble, files in PARTS:
        if not files:
            print(f"  !! {out_name}: no source files found", file=sys.stderr)
            continue
        out_path = OUT_DIR / out_name
        text = assemble_part(preamble, files)
        out_path.write_text(text, encoding="utf-8")

        # Marker count diagnostic — must stay <= 15.
        marker_count = sum(1 for line in text.split("\n") if line.strip().endswith("..."))
        words = len(text.split())
        total_words += words
        minutes = words / 140
        print(f"  {out_name}")
        print(f"    files:   {len(files)}")
        print(f"    markers: {marker_count}  (cap: 15)")
        print(f"    words:   {words:,}")
        print(f"    audio:   ~{minutes:.0f} min")

    print(f"\n  TOTAL: {total_words:,} words -> ~{total_words/140/60:.1f} h audio")


if __name__ == "__main__":
    main()
