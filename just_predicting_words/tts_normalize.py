"""
TTS Normalizer for Chatterbox — Just Predicting Words

Reads `source/raw/*.txt`, applies three rounds of normalization, writes
`source/<stem>_tts.txt` ready for `batch_render.py`.

Round 1 — Pattern substitution (automatic):
  - Years (incl. decade plurals: 2010s -> "twenty tens")
  - Number-suffixed model names (GPT-4 -> "G.P.T. four", Gemini 2.5 -> "Gemini two point five")
  - CamelCase brand names (ChatGPT -> "Chat G.P.T.", DeepMind -> "Deep Mind")
  - Standalone acronyms (AI -> "A.I.", GPT -> "G.P.T.")
  - Embedded ALL-CAPS brand mentions (GOOGLE inside a sentence -> Google)

Round 2 — Edge-case sweep:
  - Surface any remaining 3+ char ALL-CAPS tokens not in any dict (likely
    new acronyms / brand caps that need a dict entry)
  - Surface CamelCase tokens not yet substituted
  - Surface alphanumeric tokens that look like model versions

Round 3 — Structural pauses:
  - Chapter label / title / teaser get trailing "..." + standalone "..."
    pause lines so CB doesn't blur them into the body prose
  - Section headings (ALL-CAPS lines in raw) get the same treatment
  - One blank-line + "..." buffer separates body sections from headings

Usage:
  python tts_normalize.py                 # all *.txt in source/raw/
  python tts_normalize.py 07_chapter_07   # one file (no .txt)
"""
import re
import sys
from pathlib import Path

BOOK_DIR = Path(__file__).parent
RAW_DIR = BOOK_DIR / "source" / "raw"
OUT_DIR = BOOK_DIR / "source"

# =============================================================================
# Round 1 — Pattern substitution dictionaries
# =============================================================================

# CamelCase brands: detected as full tokens, replaced with spaced phonetic form.
# Order matters in fix_brands — longer tokens replaced first.
BRAND_FIXES = {
    "OpenAI": "Open AI",
    "openAI": "Open AI",
    "ChatGPT": "Chat GPT",
    "DeepMind": "Deep Mind",
    "DeepSeek": "Deep Seek",
    "AlphaFold": "Alpha Fold",
    "AlphaGo": "Alpha Go",
    "AlphaZero": "Alpha Zero",
    "ByteDance": "Byte Dance",
    "MiniMax": "Mini Max",
    "StepFun": "Step Fun",
    "WeChat": "Wee Chat",
    "ElevenLabs": "Eleven Labs",
    "GitHub": "Git Hub",
    "PowerPoint": "Power Point",
    "SpaceXAI": "Space X AI",
    "SpaceX": "Space X",
    "xAI": "X AI",
    "LeCun": "Le Cun",
    "WhatsApp": "Whats App",
    "TikTok": "Tik Tok",
    "iPhone": "iPhone",
    "iPhones": "iPhones",
    "YouTube": "YouTube",
    "EgyptAir": "Egypt Air",
    "HiddenLayer": "Hidden Layer",
    "JetBrains": "Jet Brains",
    "LoDuca": "Lo Duca",
    "McKinsey": "McKinsey",  # CB reads correctly
    "McCarthy": "McCarthy",  # CB reads correctly
}

# Acronym registry. Originally the values were dot-spelled (`A.I.`, `G.P.T.`)
# to make CB pause between letters. With this CB voice/seed (burton) the
# trailing period at the end of a dot-spelled acronym caused an audible
# letter stutter — listener heard "consumer A.I. assistants" as
# "consumer A I I assistants" (extra trailing I). On 2026-05-24 the values
# were reverted to identity-mappings: the acronyms stay bare in the output
# and CB handles them the way it did in v1 (which the listener did NOT
# complain about for pronunciation). The dict is retained because:
#   (a) Round 2 flag detection uses it to know which all-caps tokens are
#       expected vs. need attention.
#   (b) `title_case_heading` uses it to keep acronyms in their original
#       form inside section headings (so "AGENTIC AI" Title-cases to
#       "Agentic AI" not "Agentic Ai").
# If any specific acronym mispronounces, override its value here with
# phonetic spelling (e.g. "AGI": "ay gee eye"). Don't reach for the
# `X.Y.Z.` periods form — it produces the stutter artifact.
SPELL_OUT = {
    "AGI": "AGI", "AI": "AI", "AIs": "AIs",
    "API": "API", "APIs": "APIs",
    "GPT": "GPT", "GPTs": "GPTs",
    "LLM": "LLM", "LLMs": "LLMs",
    "CEO": "CEO", "CEOs": "CEOs",
    "SEC": "SEC",
    "IPO": "IPO", "IPOs": "IPOs",
    "DNA": "DNA", "RNA": "RNA", "GDPR": "GDPR",
    "RLHF": "RLHF", "RLAIF": "RLAIF", "RLEF": "RLEF",
    "DPO": "DPO",
    "TPU": "TPU", "TPUs": "TPUs",
    "IBM": "IBM", "AWS": "AWS",
    "GLM": "GLM", "FAQ": "FAQ", "MAI": "MAI",
    "DOI": "DOI", "KLM": "KLM", "PII": "PII",
    "OECD": "OECD", "MIT": "MIT", "METR": "METR",
    "AMI": "AMI",
    "HIPAA": "HIPAA", "NASA": "NASA", "NATO": "NATO", "FAIR": "FAIR",
}

# Embedded ALL-CAPS brand names — when a brand appears in ALL-CAPS inside a
# normal sentence, replace with its normal mixed-case form. Used by
# `fix_embedded_brand_caps`. Distinct from section headings, which get
# Title-cased structurally by the parser.
BRAND_CAPS = {
    "GOOGLE": "Google",
    "FACEBOOK": "Facebook",
    "AMAZON": "Amazon",
    "MICROSOFT": "Microsoft",
    "APPLE": "Apple",
    "META": "Meta",
    "NETFLIX": "Netflix",
    "TESLA": "Tesla",
    "NVIDIA": "Nvidia",
    "ANTHROPIC": "Anthropic",
    "OPENAI": "Open AI",
    "CHATGPT": "Chat GPT",
    "DEEPMIND": "Deep Mind",
    "ERNIE": "Ernie",
}

# Comprehensive ALL-CAPS brand map. A brand that appears ALL-CAPS inside a
# section heading (e.g. "...THAT WRAPS OPENAI") would otherwise be capitalized
# to "Openai" by title_case_heading and never repaired, because the CamelCase
# brand list (BRAND_FIXES) only matches mixed-case tokens. This merges the
# upper-cased CamelCase brands with the explicit ALL-CAPS list so headings
# convert correctly (e.g. OPENAI -> "Open AI", CHATGPT -> "Chat GPT"). Used by
# both title_case_heading (keep-set) and fix_embedded_brand_caps. (L-024/L-025)
BRAND_CAPS_ALL = {k.upper(): v for k, v in BRAND_FIXES.items()}
BRAND_CAPS_ALL.update(BRAND_CAPS)  # explicit ALL-CAPS entries win on overlap


# =============================================================================
# Round 1 — Year handling
# =============================================================================

NUM_WORDS = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four",
             "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine"}
ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
TEENS = {10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen",
         15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen"}

DECADE_NAMES = {
    ("19", "5"): "nineteen fifties",
    ("19", "6"): "nineteen sixties",
    ("19", "7"): "nineteen seventies",
    ("19", "8"): "nineteen eighties",
    ("19", "9"): "nineteen nineties",
    ("20", "0"): "two thousands",
    ("20", "1"): "twenty tens",
    ("20", "2"): "twenty twenties",
    ("20", "3"): "twenty thirties",
}


def two_digit(n):
    if n == 0:
        return ""
    if n < 10:
        return ONES[n]
    if n < 20:
        return TEENS[n]
    t, o = n // 10, n % 10
    return TENS[t] + ("-" + ONES[o] if o else "")


def year_to_words(y):
    y = int(y)
    rem = y % 100
    if 2000 <= y <= 2009:
        return "two thousand" if rem == 0 else "two thousand " + ONES[rem]
    if 2010 <= y <= 2099:
        return "twenty " + two_digit(rem)
    if 1900 <= y <= 1999:
        if rem == 0:
            return "nineteen hundred"
        if rem < 10:
            return "nineteen oh " + ONES[rem]
        return "nineteen " + two_digit(rem)
    return str(y)


def fix_decade_plurals(text):
    """`2010s` -> `twenty tens`, `1990s` -> `nineteen nineties`."""
    def repl(m):
        century, decade = m.group(1), m.group(2)
        return DECADE_NAMES.get((century, decade), m.group(0))
    return re.sub(r"\b(19|20)(\d)0s\b", repl, text)


def fix_years(text):
    text = fix_decade_plurals(text)
    text = re.sub(r"\b(?:19|20)\d{2}\b",
                  lambda m: year_to_words(m.group(0)), text)
    return text


def number_to_words(s):
    parts = s.split(".")
    return " point ".join(" ".join(NUM_WORDS.get(c, c) for c in p) for p in parts)


def fix_model_versions(text):
    """GPT-4 -> 'G.P.T. four', Gemini 2.5 -> 'Gemini two point five', etc.

    Must run BEFORE fix_acronyms so GPT-4 doesn't become G.P.T.-4 first.
    """
    text = re.sub(r"\bGPT-(\d+(?:\.\d+)?)\b",
                  lambda m: f"GPT {number_to_words(m.group(1))}", text)
    text = re.sub(r"\bGemini (\d+(?:\.\d+)?)\b",
                  lambda m: f"Gemini {number_to_words(m.group(1))}", text)
    text = re.sub(r"\bLlama (\d+(?:\.\d+)?)\b",
                  lambda m: f"Llama {number_to_words(m.group(1))}", text)
    text = re.sub(r"\bClaude (\d+(?:\.\d+)?)\b",
                  lambda m: f"Claude {number_to_words(m.group(1))}", text)
    # Single-letter + digit model names: K2, K2.6, V3, V4, T5
    text = re.sub(r"\b([KVT])(\d+(?:\.\d+)?)\b",
                  lambda m: f"{m.group(1)} {number_to_words(m.group(2))}", text)
    # AI21 -> "AI twenty-one" (AI21 Labs is the company)
    text = re.sub(r"\bAI21\b", "AI twenty-one", text)
    # WMT24 / WMT25 -> "W M T twenty twenty-four" etc.
    text = re.sub(r"\bWMT(\d{2})\b",
                  lambda m: f"W M T twenty {two_digit(int(m.group(1)))}", text)
    return text


def fix_brands(text):
    for term in sorted(BRAND_FIXES.keys(), key=len, reverse=True):
        text = re.sub(r"\b" + re.escape(term) + r"\b", BRAND_FIXES[term], text)
    return text


def fix_acronyms(text):
    for term in sorted(SPELL_OUT.keys(), key=len, reverse=True):
        text = re.sub(r"\b" + re.escape(term) + r"\b", SPELL_OUT[term], text)
    return text


def fix_embedded_brand_caps(text):
    """Replace known ALL-CAPS brand mentions with mixed case (GOOGLE -> Google,
    OPENAI -> Open AI). Covers brands surfaced ALL-CAPS in section headings."""
    for term in sorted(BRAND_CAPS_ALL.keys(), key=len, reverse=True):
        text = re.sub(r"\b" + re.escape(term) + r"\b", BRAND_CAPS_ALL[term], text)
    return text


def fix_legal_versus(text):
    """Legal case citations use 'v.'/'vs.' for 'versus' (e.g. 'Varghese v.
    China Southern Airlines', 'Complement Vs Substitute'). CB reads the bare
    token as "via"/"vee" — expand it to the spoken word. Only the 'v.'/'vs.'/
    'vs' forms are matched; a bare single 'V'/'v' is left alone so model names
    like 'Deep Seek V four' (V4) aren't corrupted."""
    text = re.sub(r"(?<=\s)vs?\.(?=\s)", "versus", text)      # v. / vs.
    text = re.sub(r"(?<=\s)[Vv]s(?=\s)", "versus", text)       # Vs / vs (no period)
    return text


def fix_punctuation_collisions(text):
    """`A.I..` -> `A.I.` (acronym-period + sentence-period), squeeze double spaces."""
    text = re.sub(r"([A-Z]\.)\.(?=\s|$)", r"\1", text)
    text = re.sub(r"  +", " ", text)
    return text


# =============================================================================
# Round 3 — Structural pause insertion
# =============================================================================

# CB vocalizes a STANDALONE "..." line as a stray phantom letter sound
# (heard as "E" in the ch 7 test). Inline trailing ellipsis works fine as a
# pause cue, but a "..." line on its own causes the artifact. So pause cues
# are now trailing-only on heading lines; line separation uses blank lines
# (CB-safe whitespace).
TITLE_SUFFIX = "..."

DIVIDER = re.compile(r"^\s*[=\-_]{5,}\s*$")
DOTS_DIVIDER = re.compile(r"^\s*[·•]\s*[·•]\s*[·•›]?\s*$")
AUDIO_NOTE_OPEN = re.compile(r"\[AUDIO NOTE", re.IGNORECASE)
AUDIO_NOTE_INLINE = re.compile(r"\[AUDIO NOTE[^\]]*\]")
CHAPTER_HEADER = re.compile(r"^\s*CHAPTER\s+\d+\s*:", re.IGNORECASE)
APPENDIX_HEADER = re.compile(r"^\s*APPENDIX\s+[A-Z]\s*:", re.IGNORECASE)

METADATA_LINE = re.compile(
    r"^\s*("
    r"Working draft|Voice:|Key change|Opener illustration|Concept:|Caption:|"
    r"Status:|Position(?:\s+in\s+book)?:|Word count:|Best for:|Methodology:|"
    r"Format:|Corrections from|Source:|"
    # "Within the" was previously here as a metadata marker but it false-matched
    # the body sentence "Within the next eight years..." in ch 7, dropping it
    # from both v1 and v2 audio. Removed 2026-05-23.
    r"Verified with|All chapters in|All chapters end|All real people|"
    r"Per Ziad's instruction|NOTE ON CONFLICT OF INTEREST|"
    r"Selected[:.]|Layout tool[:.]|Selected.+Version|"
    r"VERSION \d+|TITLE PAGE|CHAPTER OPENING|FINAL TEXT|"
    r"WORD COUNT|KEY DECISIONS|CURRENT INFORMATION USED|AUDIO PRODUCTION NOTES"
    r")",
    re.IGNORECASE,
)

# Wholly-italic line — a line where ALL of the non-whitespace content is
# wrapped in a single *...* pair. These are chapter epigraphs (opening
# teaser) and end-of-chapter "What comes next:" teasers. In print they're
# visual italic flourishes; in audio they just sound like an extra title
# sentence that doesn't belong. Dropped entirely.
# Distinct from mid-sentence emphasis (`This was *not* enough`) which has
# non-italic text outside the asterisks and is kept (asterisks stripped).
WHOLLY_ITALIC_LINE = re.compile(r"^\*[^*]+\*$")

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

CHAPTER_LABEL = re.compile(r"^Chapter\s+[A-Z][a-z]+$")
APPENDIX_LABEL = re.compile(r"^Appendix\s+[A-Z]\b", re.IGNORECASE)

# The ALL-CAPS banner between ==== dividers is the file's editorial label. For
# body chapters it equals the title (narrate it). For front-matter/wrapper
# files it carries version cruft ("... - FINAL LOCKED VERSION") that must never
# be spoken — the real title lives in the FINAL TEXT body. Drop such banners
# from the spoken heading (L-025).
EDITORIAL_BANNER = re.compile(r"LOCKED VERSION|FINAL VERSION", re.IGNORECASE)


def is_section_heading(line):
    """Section heading detection — tolerant of CamelCase brand prefixes
    (xAI, iPhone) appearing within an otherwise all-caps line.

    Heuristic: short-ish line (<=12 words), >=2 letters, 80%+ of letters
    uppercase, doesn't end with normal body-prose punctuation pattern.
    """
    s = line.strip()
    if not s or len(s) < 3:
        return False
    if len(s.split()) > 20:
        return False
    letters = [c for c in s if c.isalpha()]
    if len(letters) < 3:
        return False
    upper_count = sum(1 for c in letters if c.isupper())
    if upper_count / len(letters) < 0.80:
        return False
    # Must contain at least one uppercase run of 2+ (rules out lines that are
    # just one CamelCase word like "iPhone")
    if not re.search(r"[A-Z]{2,}", s):
        return False
    return True


def is_chapter_label(line):
    return bool(CHAPTER_LABEL.match(line.strip()))


def title_case_heading(s):
    """Title-case a heading. Tokens already in SPELL_OUT stay as-is so
    fix_acronyms can convert them later. CamelCase brand tokens (xAI,
    iPhone) stay as-is so fix_brands can convert them. Pure-uppercase
    words get capitalized."""
    keep = set(SPELL_OUT.keys()) | set(BRAND_CAPS_ALL.keys()) | {"I"}
    def repl(m):
        word = m.group(0)
        if word in keep:
            return word
        # Mixed-case tokens (xAI, iPhone, McCarthy) — leave alone
        if not word.isupper():
            return word
        # Pure uppercase, 2+ letters → Title-case
        if len(word) >= 2:
            return word.capitalize()
        return word
    # The apostrophe tail must stay attached to its word: a bare `[A-Za-z]+`
    # splits a possessive like AUTHOR'S into AUTHOR + S, leaving a standalone
    # capital "S" that CB reads as a spelled letter (L-024). str.capitalize()
    # on "AUTHOR'S" / "WHAT'S" yields "Author's" / "What's".
    return re.sub(r"[A-Za-z]+(?:'[A-Za-z]+)?", repl, s)


def fix_embedded_all_caps(text):
    """Title-case any 4+ char ALL-CAPS word remaining in body text that
    isn't in any known dict. Catches glossary cross-references like
    'See EMBEDDING' and any embedded all-caps proper nouns missed by
    the section-heading detector or BRAND_CAPS dict. 2-3 char ALL-CAPS
    tokens are almost always acronyms (handled by SPELL_OUT) so they're
    excluded here."""
    def repl(m):
        word = m.group(0)
        if word in SPELL_OUT or word in BRAND_CAPS:
            return word
        return word.title()
    return re.sub(r"\b[A-Z]{4,}[a-z]?\b", repl, text)


def collapse_italics(raw):
    """Collapse multi-line *italic* blocks to a single line, asterisks preserved."""
    return re.sub(r"\*([^*]+?)\*",
                  lambda m: "*" + re.sub(r"\s+", " ", m.group(1).strip()) + "*",
                  raw, flags=re.DOTALL)


def strip_audio_notes(lines):
    """Drop [AUDIO NOTE ...] blocks (single- and multi-line)."""
    out, in_block = [], False
    for line in lines:
        if in_block:
            if "]" in line:
                in_block = False
            continue
        if AUDIO_NOTE_OPEN.search(line) and "]" not in line:
            in_block = True
            continue
        line = AUDIO_NOTE_INLINE.sub("", line)
        out.append(line)
    return out


def truncate_at_end_marker(lines):
    """Drop everything from first END marker to EOF."""
    out = []
    for line in lines:
        if END_MARKER.match(line.strip()):
            break
        out.append(line)
    return out


def dedup_heading_body(lines):
    """Drop a heading line (trailing '...') that merely repeats the next
    body line — e.g. a `DEDICATION` banner heading ("Dedication...")
    immediately followed by the body line "Dedication." would otherwise be
    read twice (L-025). Match is on alphanumerics only, case-insensitive."""
    def norm(x):
        return re.sub(r"[^a-z0-9]+", "", x.lower())
    out, i, n = [], 0, len(lines)
    while i < n:
        line = lines[i]
        if line.rstrip().endswith(TITLE_SUFFIX):
            j = i + 1
            while j < n and not lines[j].strip():
                j += 1
            if j < n and norm(line.rstrip()[:-len(TITLE_SUFFIX)]) == norm(lines[j]):
                i = j  # skip the redundant heading + intervening blanks
                continue
        out.append(line)
        i += 1
    return out


def parse_and_structure(raw):
    """Strip cruft, classify lines, emit structurally-paused text.

    State machine:
      - Skip metadata blocks (continuation until blank).
      - Skip dividers + audio notes.
      - First chapter-label line gets paused.
      - Next non-blank line is chapter title -> paused.
      - Next non-blank line is teaser/subtitle -> double-paused before body.
      - In body, ALL-CAPS lines are section headings -> paused.
    """
    raw = collapse_italics(raw)
    lines = raw.splitlines()
    lines = strip_audio_notes(lines)
    lines = truncate_at_end_marker(lines)

    out = []
    in_meta = False
    chapter_label_seen = False
    chapter_title_seen = False

    for line in lines:
        s = line.strip()

        if not s:
            in_meta = False
            out.append("")
            continue

        if in_meta:
            continue

        if DIVIDER.match(s) or DOTS_DIVIDER.match(s):
            continue
        if CHAPTER_HEADER.match(s) or APPENDIX_HEADER.match(s):
            continue
        if METADATA_LINE.match(s):
            in_meta = True
            continue

        # Drop wholly-italic lines (epigraphs, "what comes next" teasers)
        if WHOLLY_ITALIC_LINE.match(s):
            continue

        # Strip in-line italics (mid-sentence emphasis) — asterisks removed,
        # text kept
        s = re.sub(r"\*([^*]+)\*", r"\1", s)

        # Chapter label — trailing ellipsis gives the "longer pause" inline cue
        # without introducing a standalone-line artifact
        if not chapter_label_seen and is_chapter_label(s):
            out.append(s.rstrip(".") + TITLE_SUFFIX)
            out.append("")
            chapter_label_seen = True
            continue

        # Chapter title
        if chapter_label_seen and not chapter_title_seen:
            out.append(s.rstrip(".") + TITLE_SUFFIX)
            out.append("")
            chapter_title_seen = True
            continue

        # (Previously a "teaser_seen" state appended TITLE_SUFFIX to the
        # italic epigraph line. Now that wholly-italic lines are dropped
        # entirely as epigraphs/teasers, there's no teaser slot — the body
        # starts immediately after the chapter title. Removed 2026-05-23.)

        # Body — check section heading. Trailing ellipsis + blank line
        # for separation; no standalone pause line.
        if is_section_heading(s):
            # Editorial-label banners (e.g. "... - FINAL LOCKED VERSION") are
            # file descriptors, not real section titles — the body carries the
            # human title. Drop them entirely. (L-025)
            if EDITORIAL_BANNER.search(s):
                continue
            cased = title_case_heading(s)
            out.append(cased.rstrip(".") + TITLE_SUFFIX)
            out.append("")
            continue

        out.append(s)

    # Collapse 3+ consecutive blank lines down to 1; preserve PAUSE_LINE rhythm
    final, blank = [], 0
    for line in out:
        if line.strip() == "":
            blank += 1
            if blank <= 1:
                final.append("")
        else:
            blank = 0
            final.append(line)

    while final and not final[0].strip():
        final.pop(0)
    while final and not final[-1].strip():
        final.pop()

    final = dedup_heading_body(final)

    return "\n".join(final) + "\n"


# =============================================================================
# Round 2 — Flag report
# =============================================================================

def round2_flags(text):
    """Return list of (kind, token) for human review."""
    flags = []
    # Remaining ALL-CAPS tokens 3+ chars not handled by any dict
    for m in re.finditer(r"\b[A-Z]{3,}\b", text):
        tok = m.group(0)
        if tok not in SPELL_OUT and tok not in BRAND_CAPS:
            flags.append(("all-caps", tok))
    # CamelCase tokens not in brand dict
    for m in re.finditer(r"\b[A-Z][a-z]+[A-Z][a-zA-Z]+\b", text):
        tok = m.group(0)
        if tok not in BRAND_FIXES:
            flags.append(("camelcase", tok))
    # Alphanumeric model-version-shaped tokens still present
    for m in re.finditer(r"\b[A-Z][a-zA-Z]*-?\d+(?:\.\d+)?\b", text):
        flags.append(("alphanum", m.group(0)))
    # Decade plurals still digit form
    for m in re.finditer(r"\b(19|20)\d0s\b", text):
        flags.append(("decade-digit", m.group(0)))
    return flags


# =============================================================================
# Main
# =============================================================================

def normalize(raw):
    """Full pipeline: structure (Round 3) then patterns (Round 1)."""
    text = parse_and_structure(raw)
    # Pattern subs run in this order so longer/more specific replacements happen first
    text = fix_model_versions(text)
    text = fix_embedded_brand_caps(text)
    text = fix_brands(text)
    text = fix_acronyms(text)
    text = fix_embedded_all_caps(text)
    text = fix_years(text)
    text = fix_legal_versus(text)
    text = fix_punctuation_collisions(text)
    return text


def process_one(raw_path):
    raw = raw_path.read_text(encoding="utf-8")
    normalized = normalize(raw)
    out_path = OUT_DIR / f"{raw_path.stem}_tts.txt"
    out_path.write_text(normalized, encoding="utf-8")
    flags = round2_flags(normalized)
    return out_path, flags


def main():
    if len(sys.argv) > 1:
        targets = [RAW_DIR / f"{name}.txt" for name in sys.argv[1:]]
    else:
        targets = sorted(RAW_DIR.glob("*.txt"))

    print(f"=== normalizing {len(targets)} file(s) ===")
    all_flags = []
    for t in targets:
        if not t.exists():
            print(f"  MISSING: {t}")
            continue
        out_path, flags = process_one(t)
        word_count = len(out_path.read_text(encoding="utf-8").split())
        print(f"  {t.name:40s} -> {out_path.name:50s} ({word_count} words, {len(flags)} flags)")
        if flags:
            all_flags.append((t.name, flags))

    if all_flags:
        print("\n=== Round 2 — tokens to review ===")
        for fname, flags in all_flags:
            seen = {}
            for kind, token in flags:
                seen[(kind, token)] = seen.get((kind, token), 0) + 1
            print(f"\n  {fname}:")
            for (kind, token), count in sorted(seen.items()):
                print(f"    [{kind:14s}] {token!r}  (x{count})")


if __name__ == "__main__":
    main()
