"""
log_lesson.py — interactive lesson logger for audiobook production.

Adds a structured entry to <book>/lessons.md with auto-assigned ID,
auto-detected book (from cwd), and auto-stamped date. Optionally promotes
the same entry to C:/AI/books/LESSONS_INDEX.md when the rule is universal.
Regenerates the index table at the top of each affected file on every run.

Usage:
  cd C:/AI/books/<book>
  python C:/AI/books/log_lesson.py

  (Walks you through: title, symptom, diagnosis, fix, rule, related ids,
  CLAUDE.md ref, promote? — then appends to lessons.md and optionally
  to LESSONS_INDEX.md. Multi-line answers: end with a single line
  containing only the word `END` on its own.)

The schema (mirrors LESSONS_INDEX.md):

  ### L-NNN: Short title
  - **Date**: YYYY-MM-DD
  - **Book**: book-slug
  - **Status**: active | superseded-by:L-XXX | observation
  - **Symptom**: ...
  - **Diagnosis**: ...
  - **Fix**: ...
  - **Rule**: ...
  - **Related**: L-XXX, L-YYY
  - **CLAUDE.md ref**: section name
"""
import re
import sys
from datetime import date
from pathlib import Path

THIS_DIR = Path(__file__).parent  # C:/AI/books
INDEX_PATH = THIS_DIR / "LESSONS_INDEX.md"

LESSONS_HEADER_TEMPLATE = """# Lessons — {book_name} (production journal)

The discovery log for this book's audiobook production. Same schema and IDs
as the cross-book `C:/AI/books/LESSONS_INDEX.md`.

See `C:/AI/books/CLAUDE.md` -> "Logging discoveries" for the system overview.

"""


def detect_book_dir(cwd: Path) -> Path | None:
    """Walk up from cwd until we find a directory whose parent is THIS_DIR."""
    p = cwd.resolve()
    while p != p.parent:
        if p.parent == THIS_DIR and p.is_dir():
            return p
        p = p.parent
    return None


def next_id(*md_paths: Path) -> int:
    """Highest L-NNN id found across the given files, +1. Returns 1 if none."""
    max_id = 0
    for path in md_paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for m in re.finditer(r"L-(\d{3,})", text):
            max_id = max(max_id, int(m.group(1)))
    return max_id + 1


def ask(prompt: str, default: str = "", multiline: bool = False) -> str:
    if multiline:
        print(f"{prompt} (multi-line; end with a line containing only END):")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        return "\n".join(lines).strip()
    suffix = f" [{default}]" if default else ""
    val = input(f"{prompt}{suffix}: ").strip()
    return val or default


def ask_yes_no(prompt: str, default: bool = False) -> bool:
    d = "Y/n" if default else "y/N"
    val = input(f"{prompt} [{d}]: ").strip().lower()
    if not val:
        return default
    return val in ("y", "yes")


def format_entry(lesson_id: int, book: str, title: str, symptom: str,
                 diagnosis: str, fix: str, rule: str, related: str,
                 claude_ref: str, status: str) -> str:
    lines = [
        f"### L-{lesson_id:03d}: {title}",
        f"- **Date**: {date.today().isoformat()}",
        f"- **Book**: {book}",
        f"- **Status**: {status}",
        f"- **Symptom**: {symptom or '_(none)_'}",
        f"- **Diagnosis**: {diagnosis or '_(none)_'}",
        f"- **Fix**: {fix or '_(none)_'}",
        f"- **Rule**: {rule or '_(none)_'}",
    ]
    if related:
        lines.append(f"- **Related**: {related}")
    if claude_ref:
        lines.append(f"- **CLAUDE.md ref**: {claude_ref}")
    return "\n".join(lines) + "\n"


# ---- Index table regeneration ----------------------------------------------

ENTRY_HEADER_RE = re.compile(r"^### (L-\d{3,}): (.+)$", re.MULTILINE)
ENTRY_FIELD_RE = re.compile(r"^- \*\*([A-Za-z .]+)\*\*: (.+)$", re.MULTILINE)


def parse_entries(text: str) -> list[dict]:
    """Extract every L-NNN entry's metadata from a lessons file."""
    entries = []
    matches = list(ENTRY_HEADER_RE.finditer(text))
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end]
        fields = {}
        for fm in ENTRY_FIELD_RE.finditer(body):
            fields[fm.group(1).strip()] = fm.group(2).strip()
        entries.append({
            "id": m.group(1),
            "title": m.group(2).strip(),
            "date": fields.get("Date", ""),
            "book": fields.get("Book", ""),
            "status": fields.get("Status", ""),
        })
    return entries


INDEX_BLOCK_START = "## Index\n"
INDEX_BLOCK_END = "\n---\n"


def render_index_table(entries: list[dict], include_book_col: bool) -> str:
    if include_book_col:
        header = "| ID | Title | Status | Date | Book |\n|----|-------|--------|------|------|\n"
        rows = [
            f"| {e['id']} | {e['title']} | {e['status']} | {e['date']} | {e['book']} |"
            for e in entries
        ]
    else:
        header = "| ID | Title | Status | Date |\n|----|-------|--------|------|\n"
        rows = [
            f"| {e['id']} | {e['title']} | {e['status']} | {e['date']} |"
            for e in entries
        ]
    return header + "\n".join(rows) + "\n"


def regenerate_index_block(path: Path, include_book_col: bool) -> None:
    """Find `## Index` block in the file and rewrite the table inside it
    from the file's current entries."""
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    entries = parse_entries(text)
    if not entries:
        return
    table = render_index_table(entries, include_book_col)

    # Find existing index block ("## Index\n...\n---\n") and replace its table portion
    if INDEX_BLOCK_START in text:
        # Split at the index block
        before, rest = text.split(INDEX_BLOCK_START, 1)
        # Find the next "---" delimiter
        if "\n---\n" in rest:
            _, after = rest.split("\n---\n", 1)
        else:
            after = ""
        new_text = before + INDEX_BLOCK_START + "\n" + table + "\n---\n" + after
        path.write_text(new_text, encoding="utf-8")


# ---- File initialization ---------------------------------------------------

def ensure_book_lessons_file(path: Path, book_name: str) -> None:
    if path.exists():
        return
    header = LESSONS_HEADER_TEMPLATE.format(book_name=book_name)
    header += "---\n\n## Index\n\n_(populated automatically as lessons are added)_\n\n---\n\n## Lessons\n"
    path.write_text(header, encoding="utf-8")


def append_lesson(path: Path, entry: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write("\n\n" + entry)


# ---- Promotion suggestion --------------------------------------------------

def suggest_promote(symptom: str, diagnosis: str, fix: str, rule: str) -> bool:
    """Heuristic: lesson is likely universal if it mentions CB-pipeline
    components (Chatterbox, ffmpeg, silence_cap, _tts.txt, atempo, etc.)."""
    haystack = f"{symptom} {diagnosis} {fix} {rule}".lower()
    cb_signals = [
        "chatterbox", "ffmpeg", "silence_cap", "atempo", "_tts.txt",
        "tts_normalize", "render_sections", "m4b", "cb voice", "burton",
        "voice clone", "section heading", "metadata_line", "_clean.txt",
    ]
    return any(sig in haystack for sig in cb_signals)


# ---- Main ------------------------------------------------------------------

def main():
    cwd = Path.cwd()
    book_dir = detect_book_dir(cwd)
    if not book_dir:
        print(f"Not inside a book directory under {THIS_DIR}.")
        print("cd into one first (e.g. C:\\AI\\books\\just_predicting_words).")
        sys.exit(1)

    book_lessons = book_dir / "lessons.md"
    ensure_book_lessons_file(book_lessons, book_dir.name)

    print(f"=== Log a lesson for: {book_dir.name} ===\n")

    lesson_id = next_id(book_lessons, INDEX_PATH)
    print(f"Next ID: L-{lesson_id:03d}\n")

    title = ask("Short title (one line, sentence case)")
    if not title:
        print("Title required — aborting.")
        sys.exit(1)

    print()
    symptom = ask("Symptom (what was heard/seen)", multiline=True)
    diagnosis = ask("Diagnosis (what was actually happening — root cause)", multiline=True)
    fix = ask("Fix (specific action taken)", multiline=True)
    rule = ask("Rule (general principle distilled)", multiline=True)

    related = ask("\nRelated lesson IDs (comma-separated, e.g. 'L-003, L-007')", "")
    claude_ref = ask("CLAUDE.md section name (if rule lives there)", "")
    status = ask("Status", default="active")

    # Promotion suggestion
    suggested = suggest_promote(symptom, diagnosis, fix, rule)
    if suggested:
        print("\nThis lesson mentions CB-pipeline components — likely universal.")
    promote = ask_yes_no("Promote to LESSONS_INDEX.md (universal rule)?", default=suggested)

    entry = format_entry(lesson_id, book_dir.name, title, symptom,
                         diagnosis, fix, rule, related, claude_ref, status)

    append_lesson(book_lessons, entry)
    regenerate_index_block(book_lessons, include_book_col=False)
    print(f"\n[+] L-{lesson_id:03d} written to {book_lessons}")

    if promote:
        append_lesson(INDEX_PATH, entry)
        regenerate_index_block(INDEX_PATH, include_book_col=True)
        print(f"[+] L-{lesson_id:03d} promoted to {INDEX_PATH}")

    print(f"\nDone. Index tables regenerated.")
    if claude_ref:
        print(f"Remember to update CLAUDE.md \"{claude_ref}\" if the rule there needs to reflect this lesson.")


if __name__ == "__main__":
    main()
