"""
Build a single M4B audiobook from the rendered chapter MP3s.

Concats all 29 narrated MP3s in narrative order, re-encodes as AAC 64k
mono (audiobook standard), embeds ffmpeg chapter markers using each
chapter's `_manifest.json` duration. Output ends up at
`audio_v2/just_predicting_words.m4b`.

Players that read M4B chapter metadata (Apple Books, Smart Audiobook
Player on Android, Bound, Plexamp, etc.) will show all 29 chapter
titles and let the listener jump between them + remember position.

Run from `just_predicting_words/`:
  python build_m4b.py
"""
import json
import subprocess
import sys
from pathlib import Path

BOOK_DIR = Path(__file__).parent
AUDIO_DIR = BOOK_DIR / "audio_v2"

# Narrative order — matches batch_render.RENDER_ORDER
ORDER = [
    "00_opening_credits", "00_dedication", "00_author_note_FINAL",
    "01_chapter_01", "02_chapter_02", "03_chapter_03", "04_chapter_04",
    "05_chapter_05", "06_chapter_06", "07_chapter_07", "08_chapter_08",
    "09_chapter_09", "10_chapter_10", "11_chapter_11", "12_chapter_12",
    "13_chapter_13", "14_chapter_14", "15_chapter_15", "16_chapter_16",
    "17_chapter_17", "18_chapter_18", "19_chapter_19", "20_chapter_20",
    "21_chapter_21", "22_appendix_A", "23_appendix_B", "24_appendix_C",
    "00_author_bio_FINAL", "99_closing",
]

# Human-readable titles shown in audiobook players
TITLES = {
    "00_opening_credits": "Opening Credits",
    "00_dedication": "Dedication",
    "00_author_note_FINAL": "Author's Note",
    "01_chapter_01": "Chapter 1: Just Predicting Words",
    "02_chapter_02": "Chapter 2: A Short History of Machines That Read",
    "03_chapter_03": "Chapter 3: Inside the Machine",
    "04_chapter_04": "Chapter 4: Taming the Wild Word Predictor",
    "05_chapter_05": "Chapter 5: Open AI, the Company That Started the Wave",
    "06_chapter_06": "Chapter 6: Anthropic, the Company That Broke Off Over Safety",
    "07_chapter_07": "Chapter 7: Google, the Giant That Almost Lost the Future",
    "08_chapter_08": "Chapter 8: Meta, the Open Bet That Changed Everything",
    "09_chapter_09": "Chapter 9: The Other Half of the Map",
    "10_chapter_10": "Chapter 10: Everyone Else",
    "11_chapter_11": "Chapter 11: What These Machines Are Genuinely Good At",
    "12_chapter_12": "Chapter 12: How These Machines Fail",
    "13_chapter_13": "Chapter 13: The Limits of Language",
    "14_chapter_14": "Chapter 14: The Risks That Are Real",
    "15_chapter_15": "Chapter 15: The Risks That Are Mostly Hype",
    "16_chapter_16": "Chapter 16: Guardrails, How Companies Try to Keep Models in Line",
    "17_chapter_17": "Chapter 17: Regulation, What Governments Are Doing",
    "18_chapter_18": "Chapter 18: How to Use Them Well",
    "19_chapter_19": "Chapter 19: How to Handle AI at Work",
    "20_chapter_20": "Chapter 20: How to Talk to Your Kids About Them",
    "21_chapter_21": "Chapter 21: Where This Is All Going",
    "22_appendix_A": "Appendix A: Glossary",
    "23_appendix_B": "Appendix B",
    "24_appendix_C": "Appendix C",
    "00_author_bio_FINAL": "About the Author",
    "99_closing": "Closing",
}


def probe_duration(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        check=True, capture_output=True, text=True,
    )
    return float(r.stdout.strip())


def collect_chapters():
    chapters = []
    cumulative_ms = 0
    for stem in ORDER:
        mp3 = AUDIO_DIR / f"{stem}.mp3"
        if not mp3.exists():
            print(f"  WARNING: missing {mp3.name} — skipping")
            continue
        manifest_path = AUDIO_DIR / "sections" / stem / "_manifest.json"
        dur_sec = None
        if manifest_path.exists():
            m = json.loads(manifest_path.read_text(encoding="utf-8"))
            dur_sec = m.get("chapter_duration_sec")
        if dur_sec is None:
            dur_sec = probe_duration(mp3)
        dur_ms = int(round(dur_sec * 1000))
        chapters.append({
            "stem": stem,
            "title": TITLES.get(stem, stem),
            "start_ms": cumulative_ms,
            "end_ms": cumulative_ms + dur_ms,
            "duration_sec": dur_sec,
        })
        cumulative_ms += dur_ms
    return chapters, cumulative_ms


def write_concat_list(chapters, path: Path):
    with open(path, "w", encoding="utf-8") as f:
        for ch in chapters:
            f.write(f"file '{ch['stem']}.mp3'\n")


def write_metadata(chapters, path: Path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(";FFMETADATA1\n")
        f.write("title=Just Predicting Words\n")
        f.write("artist=Ziad El Feghali\n")
        f.write("album=Just Predicting Words\n")
        f.write("album_artist=Ziad El Feghali\n")
        f.write("composer=Ziad El Feghali\n")
        f.write("genre=Non-Fiction\n")
        f.write("date=2026\n")
        f.write("comment=An accessible guide to large language models for non-technical readers.\n")
        f.write("\n")
        for ch in chapters:
            f.write("[CHAPTER]\n")
            f.write("TIMEBASE=1/1000\n")
            f.write(f"START={ch['start_ms']}\n")
            f.write(f"END={ch['end_ms']}\n")
            f.write(f"title={ch['title']}\n")
            f.write("\n")


def main():
    print("=== M4B build ===")
    chapters, total_ms = collect_chapters()
    print(f"chapters: {len(chapters)}")
    print(f"total duration: {total_ms/1000/60:.1f} min ({total_ms/1000/3600:.2f} hours)")

    concat_list = AUDIO_DIR / "_m4b_concat.txt"
    metadata_file = AUDIO_DIR / "_m4b_metadata.txt"
    combined = AUDIO_DIR / "_m4b_combined.mp3"
    output = AUDIO_DIR / "just_predicting_words.m4b"

    write_concat_list(chapters, concat_list)
    write_metadata(chapters, metadata_file)

    print("\n[1/2] concat 29 MP3s -> single MP3 (copy, no re-encode)")
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
         "-i", str(concat_list), "-c", "copy", str(combined)],
        check=True, capture_output=True,
    )
    print(f"  combined mp3: {combined.stat().st_size/1024/1024:.1f} MB")

    print("\n[2/2] encode AAC 64k mono + embed chapter metadata -> M4B")
    subprocess.run(
        ["ffmpeg", "-y",
         "-i", str(combined),
         "-i", str(metadata_file),
         "-map", "0:a",
         "-map_metadata", "1",
         "-c:a", "aac", "-b:a", "64k", "-ac", "1",
         "-f", "mp4",
         str(output)],
        check=True, capture_output=True,
    )

    combined.unlink(missing_ok=True)

    size_mb = output.stat().st_size / 1024 / 1024
    print("\n=== Done ===")
    print(f"M4B:        {output}")
    print(f"Size:       {size_mb:.1f} MB")
    print(f"Duration:   {total_ms/1000/3600:.2f} hours")
    print(f"Chapters:   {len(chapters)}")


if __name__ == "__main__":
    main()
