"""
Auto-cleaner for chapter source files in the Just-Predicting-Words book.

Reads `source/raw/<file>.txt`, applies the standard cleaning recipe documented
in `C:\\AI\\books\\CLAUDE.md` (audit pre-flight), and writes
`source/<file>_clean.txt` ready for `generate.py`.

Approach: aggressively drop KNOWN cruft (dividers, metadata, section markers,
audio notes, footer blocks) and keep everything else. This handles the
slightly-different formats used across chapters, appendices, author note,
and other front matter without a fragile state machine.

Cleaning rules applied:
  1. Drop ASCII divider lines (>=5 of `=` or `-`).
  2. Drop known metadata lines (Working draft, Voice:, Opener illustration:,
     Concept:, Caption:, Status:, Key change..., Position in book:,
     Word count:, Best for: ...).
  3. Drop section marker lines (TITLE PAGE, CHAPTER OPENING, FINAL TEXT,
     METHODOLOGY, FORMAT:, VERSION 1/2/3 ...:, lines that exist purely to
     introduce a section).
  4. Drop everything from end markers (END CHAPTER, END BIO, END APPENDIX,
     END FRONT MATTER, END STRUCTURE, END AUDIT, END BIO DRAFTS, END FACT-CHECK,
     END SUMMARY, END STYLE, lone END, CHANGES FROM, WHAT CHANGED FROM,
     CHAPTER COMPLETED, CLAIMS THAT REMAIN, FACT-CHECK SUMMARY,
     SUMMARY OF ERRORS, WHAT'S NEXT, STYLE CONFORMANCE).
  5. Drop multi-line `[AUDIO NOTE ...]` blocks (open `[` ... close `]`).
  6. Drop `· · ·` paragraph dividers.
  7. Strip `*foo*` italic markers (asterisks removed, text kept).
  8. Sentence-case ALL-CAPS heading lines (3+ words), colon → period.
  9. Collapse 3+ blank lines to 1.

Use:
  python clean_chapter.py                 # all *.txt in source/raw/
  python clean_chapter.py 03_chapter_03   # one file (no .txt extension)
"""
import re
import sys
from pathlib import Path

BOOK_DIR = Path(__file__).parent
RAW_DIR = BOOK_DIR / "source" / "raw"
CLEAN_DIR = BOOK_DIR / "source"

# Chapter header: `CHAPTER 2: TITLE` — drop because the title page that
# follows produces the canonical spoken title. Appendix headers
# (`APPENDIX A: GLOSSARY`) are kept because there is no title page in
# appendices.
CHAPTER_HEADER = re.compile(r"^\s*CHAPTER\s+\d+\s*:", re.IGNORECASE)
DIVIDER = re.compile(r"^\s*[=\-_]{5,}\s*$")
DOTS_DIVIDER = re.compile(r"^\s*[·•]\s*[·•]\s*[·•›]\s*$")
ITALIC = re.compile(r"\*([^*]+)\*")
AUDIO_NOTE_INLINE = re.compile(r"\[AUDIO NOTE[^\]]*\]")
AUDIO_NOTE_OPEN = re.compile(r"\[AUDIO NOTE")

# Lines that are pure metadata about the document, not narration content.
METADATA_LINE = re.compile(
    r"^\s*("
    r"Working draft|Voice:|Key change|Opener illustration|Concept:|Caption:|"
    r"Status:|Position(?:\s+in\s+book)?:|Word count:|Best for:|Methodology:|"
    r"Format:|Corrections from|Source:|Approximately|Within the|"
    r"Verified with|All chapters in|All chapters end|All real people|"
    r"Per Ziad's instruction|"
    r"NOTE ON CONFLICT OF INTEREST|"
    r"Selected[:.]|Layout tool[:.]|Selected.+Version"
    r")",
    re.IGNORECASE,
)

# Document-header lines: ALL-CAPS that include words like FINAL/VERSION/DRAFT.
# These are document-title metadata (e.g. "AUTHOR'S NOTE ON AI USE - FINAL
# LOCKED VERSION", "AUTHOR BIO - FINAL LOCKED VERSION"), not narration.
DOC_HEADER = re.compile(
    r"^\s*[A-Z][A-Z0-9 \-,'’]{5,}(FINAL|VERSION|DRAFT|LOCKED)[A-Z0-9 \-,'’]*\s*$",
    re.IGNORECASE,
)

# Section marker lines that should be dropped (they label what follows but
# aren't narration).
SECTION_MARKER = re.compile(
    r"^\s*("
    r"TITLE PAGE|CHAPTER OPENING|FINAL TEXT|TABLE OF CONTENTS|"
    r"VERSION \d+[: ]|FACT-CHECK SUMMARY|FACT-CHECK|SUMMARY|"
    r"FRONT MATTER|STYLE CONFORMANCE|STRUCTURE|"
    r"COMPLETE FRONT MATTER SEQUENCE|FINAL BOOK STRUCTURE|"
    r"PAGE \d+|CROSS-REFERENCE AUDIT|JUST PREDICTING WORDS\s*$"
    r")",
    re.IGNORECASE,
)

# End markers — everything from here to EOF gets dropped.
END_MARKER = re.compile(
    r"^\s*("
    r"END CHAPTER|END BIO|END APPENDIX|END FRONT MATTER|END STRUCTURE|"
    r"END AUDIT|END BIO DRAFTS|END FACT-CHECK|END SUMMARY|END STYLE|"
    r"END$|END\s+\w+$|"
    r"WHAT CHANGED FROM|WHAT'S NEXT|CHANGES FROM|CHAPTER COMPLETED|"
    r"CLAIMS THAT REMAIN|SUMMARY OF ERRORS|FACT-CHECK SUMMARY"
    r")",
    re.IGNORECASE,
)

ALL_CAPS_HEADING = re.compile(
    r"^([A-Z][A-Z0-9 ,'?!&():\-\.]{2,})\s*$"
)

KEEP_UPPER = {
    "AI", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
    "EU", "USA", "UK", "UAE", "RLHF", "GPT", "API", "MIT", "LLM",
    "RAG", "DPO", "RLAIF", "CSAM", "SaaS", "GDPR", "OECD", "AWS", "B2B",
    "FAQ", "TV", "PR", "CEO", "CTO", "PhD", "OPENAI", "DEEPMIND",
    "TIKTOK", "META", "GOOGLE", "MICROSOFT", "FACEBOOK", "AMAZON",
    "ANTHROPIC", "MISTRAL", "CHATGPT", "AGI",
    # NOTE: "US" intentionally NOT in this set. Heading like "TURNS AGAINST US"
    # should sentence-case the trailing "us" as the pronoun, not the country.
    # When you genuinely mean the country in a heading, write "USA" or "U.S.".
}


def sentence_case(text: str) -> str:
    """Convert ALL-CAPS heading text to sentence case, preserving brand/acronym tokens."""
    words = text.split()
    out = []
    for i, w in enumerate(words):
        # Match: optional leading (, then alphanum token, then trailing punctuation
        m = re.match(r"^(\(?)([A-Z0-9'\-/]+)([.,;:!?\)]*)\s*$", w)
        if not m:
            out.append(w)
            continue
        prefix, token, trail = m.group(1), m.group(2), m.group(3)
        if token in KEEP_UPPER:
            out.append(prefix + token + trail)
        elif i == 0:
            out.append(prefix + token.capitalize() + trail)
        else:
            out.append(prefix + token.lower() + trail)
    result = " ".join(out)
    # Convert internal colons to periods for clean stops
    result = result.replace(":", ".")
    if not result.endswith("."):
        result += "."
    return result


def clean_text(raw: str) -> str:
    # Pre-pass 1: collapse multi-line *italics* to single-line by removing
    # newlines INSIDE asterisk pairs. Lazy match across newlines.
    raw = re.sub(r"\*([^*]+?)\*",
                 lambda m: "*" + re.sub(r"\s+", " ", m.group(1).strip()) + "*",
                 raw, flags=re.DOTALL)

    lines = raw.splitlines()

    # Pre-pass 2: drop multi-line [AUDIO NOTE ...] blocks
    cleaned_lines = []
    in_audio_note = False
    for line in lines:
        if in_audio_note:
            if "]" in line:
                in_audio_note = False
            continue
        if AUDIO_NOTE_OPEN.search(line) and "]" not in line:
            in_audio_note = True
            continue
        line = AUDIO_NOTE_INLINE.sub("", line)
        cleaned_lines.append(line)
    lines = cleaned_lines

    # Pre-pass 3: drop everything from first END_MARKER to EOF
    truncated = []
    for line in lines:
        if END_MARKER.match(line.strip()):
            break
        truncated.append(line)
    lines = truncated

    # Main pass: drop dividers / dots / metadata blocks / section markers,
    # strip italics, sentence-case ALL-CAPS headings.
    # Metadata block: line starts with metadata pattern → drop that line AND
    # subsequent non-blank continuation lines until next blank line.
    output = []
    in_metadata_block = False
    for line in lines:
        stripped = line.strip()

        if not stripped:
            in_metadata_block = False
            output.append("")
            continue

        if in_metadata_block:
            continue  # continuation of a metadata block

        if DIVIDER.match(stripped):
            continue
        if DOTS_DIVIDER.match(stripped):
            continue
        if CHAPTER_HEADER.match(stripped):
            continue
        if DOC_HEADER.match(stripped):
            continue
        if METADATA_LINE.match(stripped):
            in_metadata_block = True
            continue
        if SECTION_MARKER.match(stripped):
            continue

        # Strip italic asterisks (now single-line after pre-pass 1)
        line = ITALIC.sub(r"\1", line)

        # Sentence-case ALL-CAPS heading lines (>=3 words)
        if ALL_CAPS_HEADING.match(stripped) and len(stripped.split()) >= 3:
            line = sentence_case(stripped)

        output.append(line.rstrip())

    # Collapse runs of blank lines to single blank
    collapsed = []
    blank = 0
    for line in output:
        if not line.strip():
            blank += 1
            if blank <= 1:
                collapsed.append("")
        else:
            blank = 0
            collapsed.append(line)

    # Trim leading/trailing blanks
    while collapsed and not collapsed[0].strip():
        collapsed.pop(0)
    while collapsed and not collapsed[-1].strip():
        collapsed.pop()

    return "\n".join(collapsed) + "\n"


def clean_one(raw_path: Path) -> Path:
    raw_text = raw_path.read_text(encoding="utf-8")
    cleaned = clean_text(raw_text)
    out_path = CLEAN_DIR / f"{raw_path.stem}_clean.txt"
    out_path.write_text(cleaned, encoding="utf-8")
    word_count = len(cleaned.split())
    print(f"  {raw_path.name:40s} -> {out_path.name:48s} ({word_count} words)")
    return out_path


def main() -> None:
    if len(sys.argv) > 1:
        targets = [RAW_DIR / f"{name}.txt" for name in sys.argv[1:]]
    else:
        targets = sorted(RAW_DIR.glob("*.txt"))
    print(f"=== cleaning {len(targets)} file(s) ===")
    for t in targets:
        if not t.exists():
            print(f"  MISSING: {t}")
            continue
        clean_one(t)
    print(f"=== done. clean files in {CLEAN_DIR}\\ ===")


if __name__ == "__main__":
    main()
