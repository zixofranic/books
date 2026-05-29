# Books

Long-form audiobook narration for Ziad's books. Sits separately from the
short-form content channels (`wisdom`, `gibran`, `na`, `aa`) because books
need different economics, different cadence, and a per-book structure rather
than a per-channel pipeline.

## On a new session — read these first

This file is auto-loaded by Claude Code in this directory. Two more files
that are NOT auto-loaded but YOU SHOULD READ before making any change to
the pipeline or starting a new book:

1. **`C:\AI\books\LESSONS_INDEX.md`** — every production discovery from
   prior books on this pipeline, with stable IDs (L-NNN) and back-refs
   to the rules in this CLAUDE.md. Search it for any symptom that
   resembles what you're hearing before debugging from scratch — most
   pipeline issues are already documented there.
2. **`C:\AI\books\<active-book>\lessons.md`** — if you're working on a
   specific book, its per-book journal has the full diagnostic narrative
   that the cross-book index summarizes.

Treat unknown CB rendering artifacts as candidate new lessons. Log them
via `python C:\AI\books\log_lesson.py` from the book directory once
diagnosed. See the "Logging discoveries" section below for the system.

## Where this runs (recording infrastructure)

**All recording happens locally on Ziad's workstation.** Zero cloud calls,
zero per-character billing. The audio you hear in `audio_v2/` was rendered
on the same Windows machine that hosts the short-form content pipeline at
`C:\AI\system\`. Specifics:

| Component | Where | Notes |
|---|---|---|
| Chatterbox TTS server | `C:\AI\system\Chatterbox-TTS-Server\`, port `8004` | The actual voice cloner. GPU-bound (shares GPU with ComfyUI). Brought up by `C:\AI\system\START_ALL.bat`. |
| Voice reference WAVs | `C:\AI\system\voice\recordings\` | Each `Voice` in `voices.py` points at a basename here. Must be <30s per CB constraint. |
| Conda env | `chatterbox` (Python 3.11, PyTorch 2.11+cu128) | Per `C:\AI\system\CLAUDE.md`. |
| ffmpeg + ffprobe | On PATH | Used for atempo, silence_cap, MP3 conversion, M4B concat + mux. WinGet-installed Gyan build. |
| GPU time per chapter | ~3-5 min per section (~20-25 min per chapter, ~9 hours for a full 9-hour book) | Same GPU does both inference and post-processing. |
| Storage | Local SSD only | No object storage, no cloud blob, no streaming. Outputs live in `<book>/audio_v2/`. |
| Cost per render | $0 | Compare: a full 9-hour JPW on ElevenLabs would cost ~$99-$198 (we calculated this; see [[ElevenLabs cost math]] in conversation history). |

### Why local Chatterbox instead of cloud (ElevenLabs)

Three reasons, in priority order:

1. **Iteration cost.** ElevenLabs Creator plan = 100K credits/month
   ($22/mo). A single full-book render burns ~400K characters = 4 months of
   the plan budget. Iteration on a 9-hour audiobook (which is what JPW
   turned out to need — 17 lessons of discoveries) would have cost
   $300-600+. Local CB iterations are free past the one-time GPU
   investment.
2. **Quality is "good enough" + steerable.** Burton voice on CB is
   ~85-90% of a well-tuned ElevenLabs voice on the same content. The
   gap closes further with the normalization recipe + silence_cap
   tuning + section-by-section iteration documented elsewhere in this
   file. For the listenability target ("smart friend over coffee"
   register), it's there.
3. **Sovereignty.** Source text never leaves the workstation. The book
   exists as a local file, gets read by a local model, rendered by
   local ffmpeg, packaged into a local M4B. No vendor lock-in, no
   API outage to recover from, no terms-of-service surprises.

### The production tricks (what makes the recipe work)

These are codified in the codebase but worth naming explicitly here so
they're not buried in script comments:

- **`seed=4242`** across every CB call in the project — deterministic
  output. Same text + same seed + same ref = same audio every time.
  Makes re-renders byte-identical when the text is byte-identical.
- **`split_text=True, chunk_size=240`** in the CB request — lets CB
  handle paragraph-level chunking internally. Going lower (e.g. 100)
  produced more chunk-boundary artifacts; higher (e.g. 500) ran into CB
  memory issues on long inputs.
- **`temperature=0.75, exaggeration=0.5, cfg_weight=0.5`** — tuned by
  ear on the burton voice. Higher temperature → more variation but
  also more mispronunciation; lower → flatter delivery.
- **`speed_factor=1.0`** in the CB request — DON'T change. CB pitch-
  shifts when you change this. Use ffmpeg `atempo` post-process instead
  (no pitch shift).
- **`atempo=0.89`** for burton — CB renders ~12% hot, atempo undoes it.
  The actual ratio varies by voice; ear-tuned per `Voice` entry in
  `voices.py`.
- **`silence_cap` (per voice)** — caps the long chunk-boundary silences
  CB hallucinates on short isolated sentences. Burton at `stop_duration=0.9,
  stop_silence=0.5` after the L-009 tuning. See voices.py for the why.
- **Pause-hint pre-processing** in `batch_render.add_pause_hints` /
  `render_sections.add_pause_hints`: ` — ` → `... `, `. ` → `.  `,
  `, ` → `,  `. These exploit CB's whitespace-honoring pause behavior
  to land natural commas and periods. Em-dashes get converted to
  ellipses because CB ignores em-dashes.
- **Render order matters in `tts_normalize.py`** (per L-001/L-002/L-004
  and the CLAUDE.md "Pattern substitutions" section). Get the order
  wrong and earlier subs mask later patterns.

### Setting up on a new machine

If this pipeline ever needs to move to a different workstation:

1. Install Python 3.11, PyTorch with CUDA matching the GPU.
2. Install Chatterbox-TTS-Server, configure `reference_audio_path` to
   point at the voice recordings folder.
3. Install ffmpeg + ffprobe (Gyan build on Windows, system package on
   Linux).
4. Copy `C:\AI\books\` to the new machine. The pipeline scripts are
   pure Python + ffmpeg shellouts — no other native deps.
5. Copy voice reference WAVs to the new machine's recordings folder.
6. Smoke test: `cd <book> && python -c "import requests; print(requests.get('http://localhost:8004/').status_code)"` should return 200.
7. Run one section render: `python C:/AI/books/render_sections.py prep <book>` then `python C:/AI/books/render_sections.py render <book> 07_chapter_07` and listen.

The pipeline is intentionally portable — no Windows-specific code paths
in the scripts themselves, only in the documented paths (which a Linux
move would update to `~/AI/books/`-style).

---

## Why this exists separately

The short-form content pipeline in `C:\AI\system\` is built around a
queue-driven orchestrator. Books don't fit that model:

- **Length.** A chapter is 2,000-3,000 words = 15-25 minutes of audio. Way past
  any short/midform format the orchestrator handles.
- **Cost.** ElevenLabs Creator plan is 100K credits / month. One full chapter
  burns ~3,000-5,000 credits. A whole book would torch the monthly cap before
  the short-form channels even ran.
- **Iteration.** Books get re-recorded as drafts evolve. You don't queue a
  book the way you queue a daily short — you render specific excerpts on
  demand, audition takes, and re-render.

So books use **Chatterbox locally** (free, unlimited, runs on the same GPU
that ComfyUI uses) instead of ElevenLabs. Trade-off: CB is roughly 80-90%
the quality of a well-tuned EL voice, but it's free and you can iterate.

## Per-book structure

```
C:\AI\books\
├── CLAUDE.md              ← this file
└── <book-slug>\
    ├── source\            ← raw chapter text files
    │   └── chapter_NN_vX.Y.txt
    ├── audio\             ← rendered output
    │   ├── chapter_NN_*.wav        (final, post-atempo)
    │   └── _raw_pre_atempo\        (raw CB output, kept for re-tuning)
    └── generate.py        ← per-book renderer (excerpt + settings)
```

One book per subdirectory. The slug is whatever describes the book; first
example is `ai_history\` (working title for Ziad's "A Short History of
Machines That Read" book).

## The render recipe

Lifted from `system\scripts\run_chatterbox_gibran_slow.py`, which is the
empirically-tuned long-form CB recipe.

1. **Text preprocessing — pause hints.** CB ignores em-dashes and semicolons
   for pause cues, but honors extra whitespace and ellipses. So:
   - `" — "` and `"—"` → `"... "`
   - `". "` → `".  "`  (double-space after period)
   - `", "` → `",  "`  (double-space after comma)

2. **Chatterbox /tts call** at `http://localhost:8004/tts`, voice_mode=`clone`:
   ```python
   {
     "voice_mode": "clone",
     "reference_audio_filename": <voice.ref_filename>,
     "output_format": "wav",
     "split_text": True, "chunk_size": 240,
     "temperature": 0.75,
     "exaggeration": 0.5,
     "cfg_weight": 0.5,
     "speed_factor": 1.0,    # leave native — CB pitch-shifts if you change this
     "seed": 4242,
     "language": "en"
   }
   ```
   Reference WAVs live in `C:\AI\system\voice\recordings\` and are referenced
   by basename only (CB resolves via its `reference_audio_path` config).

3. **Post-process — ffmpeg atempo.** CB runs about 20% faster than EL out of
   the box. Time-stretch (no pitch shift) via:
   ```
   ffmpeg -i raw.wav -filter:a atempo=<voice.atempo> final.wav
   ```
   Suggested atempo by content register:
   - `0.85` — contemplative / philosophy / Gibran-style
   - `0.88` — "smart friend over coffee" / general non-fiction (default for `burton` and `don`)
   - `0.92` — punchy / energetic / journalism

4. **Optional silence-cap pass** — only for voices flagged `silence_cap=True`
   in `voices.py`. See "Hallucinated dead air" below for the recipe and why.

## Voices — friendly names

The canonical registry lives in `C:\AI\books\voices.py`. Per-book scripts
import it and pick a voice by friendly name:

```python
import voices
v = voices.get("burton")   # or "don"
```

| Friendly name | Reference file (in `C:\AI\system\voice\recordings\`) | Use for |
|---|---|---|
| `burton` | `wisdom_burton_long_ref.wav` | **Default for non-fiction.** Measured authority, smart-friend register. |
| `don` | `na_old_timer_5min_cbref.wav` | More energetic and weathered than Burton. NA/AA old-timer cadence. **Requires `silence_cap=True`** — see "Hallucinated dead air" below. |

Other reference files in the recordings dir that haven't been wrapped as a
named voice yet: `gibran_long_ref.wav`, `joe_voice_reference.wav`,
`ziad_ref_30sec.wav`. Wrap them in `voices.py` when you decide to use one
in a book.

CB reference clips must be **under 30 seconds** per `system\CLAUDE.md`. The
`*_cbref.wav` files in `recordings\` are pre-trimmed to 28s for that reason.

## Hallucinated dead air (gotcha)

CB occasionally generates a long silence (10-40s) at chunk boundaries when
it sees a short isolated line surrounded by paragraph breaks (e.g. a
standalone `Two months.` between two `\n\n`). Behavior is reference-voice +
seed deterministic — Burton handled it cleanly, `don` produced a 38s gap on
the same input.

Fix is post-render, no re-synth needed:

```
ffmpeg -i raw.wav -af "silenceremove=stop_periods=-1:stop_duration=1.5:\
stop_silence=1.0:stop_threshold=-40dB" out.wav
```

Plain English: anywhere there's >1.5s of silence, trim it down to ~1s.
Preserves natural breath pauses, kills hallucinated dead air. Side benefit:
the surviving 1-2s pause around dramatic short lines lands as a natural beat.

Voices known to need this are flagged with `silence_cap=True` in `voices.py`
and the per-book renderer applies it automatically.

## Why Wisdom voice on Chatterbox (not ElevenLabs)

Memory rule: **"Don't stack Wisdom's slow_factor on CB channels."** That rule
is about the short-form orchestrator (which has Wisdom hardcoded to EL with
its own `atempo=0.88` post-process). It does NOT apply to books — books are
their own pipeline, atempo is tuned from scratch per book, and Burton on CB
is a deliberate choice for cost/iteration reasons.

## Pre-flight: audit before rendering

**Always read the chapter source and audit it before calling Chatterbox.**
Source files mix prose with markdown italics (`*foo*`), audio production
notes (`[AUDIO NOTE, ...]`), ascii dividers (`====`, `· · ·`), and metadata
(WORD COUNT, REAL-WORLD ANALOGIES, AUDIO PRODUCTION NOTES, "END CHAPTER N").
CB will read every one of those literally — asterisks become "asterisk",
dividers stutter, notes get spoken aloud.

The pattern (per `feedback_books_vo_audit.md` in memory):

1. **Strip non-prose blocks** — header metadata, dividers, audio notes,
   end-of-chapter footer.
2. **Strip in-line markup** — asterisk italics, brackets.
3. **Decide on subsection headings** — read as sentences (sentence-cased)
   or skip entirely. Apply consistently across the book.
4. **Flag pronunciation watchpoints** — acronyms (GPT-3), foreign names
   (Tomas Mikolov), brand names CB may mispronounce (Llama, word2vec).
   Don't always need a fix; listing them is the audit value.
4a. **Substitute initials with full names.** Scan the source for the
    regex `[A-Z]\. [A-Z]` — that's the "initial + period + space +
    capital" pattern (e.g. `J. R. Firth`, `J. F. Kennedy`, `H. G. Wells`).
    The pause-hint preprocessing turns `". "` into `".  "` which forces
    a long pause between every initial — CB mangles the resulting read.
    Look up the full name (`John Rupert Firth`, `John Fitzgerald Kennedy`)
    and substitute. If unknown, at minimum strip the periods so CB just
    spells the letters cleanly: `J R Firth`.
5. **Flag dead-air risk lines** — short isolated lines like `Two months.`
   that trigger CB silence-hallucination on certain refs. `silence_cap=True`
   handles them but the audit should call them out.
6. **Write the cleaned text to a sibling file** — `<chapter>_clean.txt` next
   to the source. Renderer reads from clean, never from raw.
7. **Save an audit report** — `audit_<chapter>.md` next to the source so
   decisions are inspectable later.

Example for chapter 2: `source/chapter_02_v0.1.txt` →
`source/chapter_02_clean.txt` + `audit_chapter_02.md`.

## Long-form normalization (the `_tts.txt` pipeline)

For multi-chapter audiobooks (anything 30+ minutes), the `_clean.txt` audit
pattern above is necessary but not sufficient. Chatterbox makes specific,
predictable mistakes on years, brand names, acronyms, model versions, and
section transitions — mistakes that bake into the audio and only get caught
during listen-through.

**Reference implementation: `just_predicting_words/tts_normalize.py`.** It
produces a `_tts.txt` sibling next to each `_clean.txt`. `batch_render.py`
prefers `_tts.txt` when present, falls back to `_clean.txt`.

Two files exist for a reason: `_clean.txt` is human-readable (the eventual
print/ebook source); `_tts.txt` is a phonetic mirror with normalized acronyms,
spelled-out years, etc. fed only to CB. Never treat `_tts.txt` as canonical text.

### Pattern substitutions to apply in `_tts.txt`

Structural pass first (heading detection, drop italic epigraphs, drop metadata
blocks), THEN pattern subs in this order so longer/more-specific replacements
happen first:

1. **Number-suffixed model names**: `GPT-4` → "GPT four", `Gemini 2.5` → "Gemini
   two point five", `K2.6` → "K two point six". MUST run before acronym
   substitution.
2. **Embedded ALL-CAPS brand mentions**: `What GOOGLE believes` → `What Google
   believes`. Maintain a brand-caps dict for proper-noun caps (GOOGLE, META,
   FACEBOOK, etc.) so they get re-cased mid-sentence.
3. **CamelCase brands** to spaced form: `OpenAI` → "Open AI", `ChatGPT` →
   "Chat GPT", `DeepMind` → "Deep Mind". CB mispronounces concatenated CamelCase.
4. **Standalone acronyms — LEAVE BARE, do NOT dot-spell.** We originally tried
   `A.I.` with periods to force CB to pause between letters; with the `burton`
   voice/seed this produced an audible letter-stutter ("consumer A.I.
   assistants" → "consumer A I I assistants"). Identity-map the dict (`"AI":
   "AI"`) and let CB read bare acronyms. If a specific acronym mispronounces,
   override with phonetic spelling (`"AGI": "ay gee eye"`) — never periods.
5. **Embedded all-caps cross-references** (4+ char): `See EMBEDDING` →
   `See Embedding`. Skip anything already in the acronym or brand-caps dicts.
6. **Years and decade plurals**: `2025` → "twenty twenty-five", `2010s` →
   "twenty tens", `1998` → "nineteen ninety-eight", `2008` → "two thousand
   eight". Without this CB inconsistently reads `2025` as "two zero two five"
   at some chunk boundaries (the failure that drove this whole effort).
7. **Punctuation collisions**: `A.I..` (acronym period + sentence period) →
   `A.I.`. Squeeze double spaces.
8. **Legal "versus"**: case citations use `v.` / `vs.` / `Vs` for *versus*
   (e.g. `Varghese v. China Southern Airlines`, `Complement Vs Substitute`).
   CB reads the bare token as "via"/"vee" — expand to "versus". Match only the
   `v.` / `vs.` / `vs` forms; **leave a bare single `V`/`v` alone** so model
   names like `Deep Seek V four` (V4) aren't corrupted (L-027).

### Section heading detection

Source convention: ALL-CAPS standalone lines between `· · ·` dividers mark
section breaks. The pre-flight `clean_chapter.py` only sentence-cases headings
with 3+ words — leaving 2-word headings like `THE STUMBLE` un-touched, and
embedded brand caps like `What GOOGLE believes` un-fixed.

Work from the **raw** source, not from `_clean.txt`, so heading detection is
reliable. Use a percentage rule (80%+ uppercase letters + ≤20 words per line)
rather than a strict `^[A-Z]` regex — that strict version misses CamelCase-
prefixed headings like `xAI, THE LAB THAT BECAME A SPACE COMPANY`.

For Title-casing a heading, iterate via `re.sub(r"[A-Za-z]+(?:'[A-Za-z]+)?", repl, line)`
so punctuation tokens like `(ARTIFICIAL` don't break naïve `.split()` transforms.
Keep tokens already in your acronym dict in their original form (so
`AGENTIC AI` Title-cases to `Agentic AI`, not `Agentic Ai`).

**Brands in ALL-CAPS headings must be preserved, not capitalized (L-026).**
A brand like `OPENAI`/`CHATGPT` inside a heading gets capitalized to
`Openai`/`Chatgpt` by the title-caser and is then never repaired — because the
later brand pass (`fix_brands`) only matches *mixed-case* CamelCase tokens, and
`fix_embedded_brand_caps` historically only knew the explicit ALL-CAPS list.
Fix: build a combined ALL-CAPS brand map (`BRAND_CAPS_ALL` = uppercased
`BRAND_FIXES` keys + `BRAND_CAPS`), add its keys to `title_case_heading`'s
keep-set (so the brand survives title-casing in its ALL-CAPS form), and have
`fix_embedded_brand_caps` iterate that combined map (so `OPENAI` → "Open AI",
`CHATGPT` → "Chat GPT" everywhere, including headings).

**Possessive `'S` must stay attached to its word (L-024).** The naïve
`re.sub(r"[A-Za-z]+", repl, line)` splits `AUTHOR'S` into `AUTHOR` + `S`,
leaving a standalone capital `S` that CB reads as a spelled letter (`AUTHOR'S
NOTE` → `Author'S Note` → "Author … S Note"). Include the apostrophe tail in
the token regex (`[A-Za-z]+(?:'[A-Za-z]+)?`) so `str.capitalize()` yields
`Author's` / `What's`. A lone capital letter anywhere in `_tts.txt` is a
CB letter-spell trap.

**The ALL-CAPS banner between `====` dividers is a file/editorial label, not
always the spoken heading (L-025).** For chapters the banner equals the title —
narrate it. For front-matter/wrapper files (dedication, author's note, about
the author) it's a descriptor that may (a) duplicate the body's first line —
`DEDICATION` heading + "Dedication." body = the word read twice — or
(b) carry version cruft (`AUTHOR'S NOTE ON AI USE - FINAL LOCKED VERSION`) that
should never be spoken and buries the real title. For non-chapter files,
source the spoken title from an explicit map (the `build_m4b.py` `TITLES`
dict), strip `FINAL`/`LOCKED`/`VERSION` editorial suffixes, and dedup the
emitted heading against the first body line.

### Pause cues — INLINE trailing only, never standalone

CB honors **inline** trailing ellipsis as a "longer pause" cue:
`The Stumble...\n\nbody text` reads with a clear beat before the body.

**Do NOT use standalone `...` lines on their own line.** Empirically validated
on the `burton` voice (2026-05-23): a standalone `...` line causes CB to
vocalize a phantom letter sound (heard as a stray "E" between the chapter title
and the body). The "CB honors ellipses for pause cues" rule applies to INLINE
ellipses only — isolated-line ellipses break it.

For longer pauses use blank lines (CB-safe whitespace) and trailing inline
`...` on the line preceding the pause.

### Italic epigraphs / teasers

Drop wholly-italic lines entirely from `_tts.txt`. A "wholly-italic line" is
one where all the non-whitespace content is wrapped in a single `*…*` pair —
typically chapter-opening teasers (`*They built the architecture…*`) and
end-of-chapter "What comes next:" lines.

In print these are italic flourishes. In audio they sound like extra title
sentences that don't belong. Mid-sentence emphasis (`This was *not* enough`)
is unaffected — keep the word, strip the asterisks.

### Metadata-regex gotcha

Avoid prefix-only patterns in `METADATA_LINE` that could match body sentences.
`Within the` was once in the JPW metadata regex — it false-matched the body
sentence *"Within the next eight years, all eight of those researchers had
left Google"* and dropped it from both `_clean.txt` AND `_tts.txt`. Prefer
patterns with explicit colons (`Working draft:`, `Voice:`) or ALL-CAPS line
patterns (`TITLE PAGE`, `CHAPTER OPENING`) that can't accidentally match body.

Audit existing patterns by grepping each raw chapter for sentences that start
with each pattern — if any body sentences match, the pattern is too greedy.

### Render granularity: section-by-section (preferred for iteration)

A 25-minute full-chapter render means each ear-detected mistake costs 25 min
of GPU time to redo. Split each chapter on its section headings and render
each section as a separate WAV (~5 min each). When a section sounds bad, fix
just that section's source text and re-render only that section. The final
chapter WAV is an ffmpeg concat of the section WAVs.

Layout:
```
audio_v2/
├── 07_chapter_07.mp3            ← final, concat of sections
├── 07_chapter_07.wav            ← final
└── sections/
    └── 07_chapter_07/
        ├── 01_intro.wav
        ├── 02_<section_slug>.wav
        └── …
```

One-time risk: voice consistency across separate CB calls. With
`voice_mode=clone` + same `seed` + same reference WAV, CB should be
deterministic across calls. A/B section-rendered vs whole-chapter rendered
output once to confirm before adopting.

### Test protocol — never commit GPU time blindly

For any new book, before kicking off the full batch:
1. Render ONE chapter (or one section) from `_tts.txt`.
2. Listen through it end-to-end.
3. Verify: acronyms, years, brand names, section transitions, the chapter
   intro block.
4. THEN run the full batch.

Burton-voice gotchas that take real ears to catch:
- Phantom letter sounds from standalone `...` pause lines.
- Letter-stutter from dot-spelled acronyms (`A.I.` → "A I I").
- Hallucinated dead air at chunk boundaries (use `silence_cap` for the
  voice — see "Hallucinated dead air" above).
- Inconsistent year readings within the same source file.

The ear test is cheap (one chapter ≈ 25 min GPU). Skipping it costs 10+ hours
when a recipe-wide artifact turns out to be in every chapter.

## Adding a new book

1. `mkdir C:\AI\books\<slug>\source` and drop the chapter text in.
2. Copy `ai_history\generate.py` as a template. The renderer reads from a
   cleaned source file (default `chapter_02_clean.txt`); add the same
   default for your chapter file naming.
3. Run the pre-flight audit (above). Produce `<chapter>_clean.txt` and
   `audit_<chapter>.md`.
4. Pick a voice from `voices.py` — `burton`, `don`, or add a new one.
5. `python generate.py [voice_name] [chapter_clean.txt]` from the book's
   directory. Final WAV lands in `audio/`, raw kept in
   `audio/_raw_pre_atempo/` so you can re-tune atempo without re-synth.

Chatterbox must be running on port 8004. `system\START_ALL.bat` brings it up
along with the rest of the stack.

## Adding a new voice

1. Open `C:\AI\books\voices.py`.
2. Append a new `Voice(...)` constant — pick a friendly name, point at the
   reference WAV in `C:\AI\system\voice\recordings\`, set `atempo` and
   `silence_cap` defaults.
3. Add it to the `VOICES` dict at the bottom.
4. Run a sample render against an existing book to audition it. If you hear
   long dead-air gaps at chunk boundaries, flip `silence_cap=True`.

## Output formats

Default is WAV (CB native, lossless, large). For sharing or streaming, run a
secondary ffmpeg pass to MP3 / M4B as needed — kept out of the main render
path because audiobook output formats vary by destination (Spotify, Audible,
podcast feed, etc.).

## Build M4B (single-file audiobook with chapter markers)

Once a book's chapters are all rendered + assembled (via `render_sections.py`
or `batch_render.py`), the per-book `build_m4b.py` packages everything as a
single `.m4b` audiobook file with embedded chapter markers.

Reference implementation: `just_predicting_words/build_m4b.py`.

Pipeline:
1. ffmpeg `-f concat` joins all 29 chapter MP3s in narrative order (copy,
   no re-encode → ~30 sec)
2. ffmpeg re-encodes the combined stream to AAC 64k mono in an MP4 container
   (audiobook standard; ~5-8 min for a 9-hour book)
3. Chapter markers embedded via `ffmetadata` file with one `[CHAPTER]` block
   per chapter, using timestamps computed from each chapter's
   `_manifest.json` `chapter_duration_sec`
4. Output: `audio_v2/<book>.m4b`, ~250 MB for a 9-hour book at 64k AAC

To add a new book's M4B builder: copy `just_predicting_words/build_m4b.py`,
update the `ORDER` list (matches `batch_render.RENDER_ORDER` minus the
`_clean` suffix) and the `TITLES` dict (human-readable chapter labels for
the player UI).

### Cover art

M4B can embed a JPG cover that audiobook players display on the lock screen
+ library. Specs:

- **Dimensions: 2400×2400 px** (square, 1:1). Works on all major audiobook
  platforms. Apple Books minimum is 1400×1400; Audible-style production
  uses 2400×2400 or 3000×3000.
- **Format**: JPG (preferred for size) or PNG. RGB color space, not CMYK.
- **File size**: under 500 KB ideal, under 2 MB max.
- **DPI**: 72 minimum (most renderers ignore DPI for screen display
  anyway — pixel dimensions are what matter).

To embed into an existing M4B without re-encoding the audio. Two-step
because (a) JPGs with alpha channel (`yuva444p`) break the MP4 muxer, and
(b) `-map 0` includes the binary chapter-text stream that the `ipod`
output codec rejects. Explicit mapping fixes both:

```
# 1. strip alpha + normalize to standard JPEG pixel format
ffmpeg -y -i cover_with_alpha.jpg -pix_fmt yuvj420p -q:v 2 cover_std.jpg

# 2. embed cover into M4B, preserving audio + chapters
ffmpeg -y -i input.m4b -i cover_std.jpg \
       -map 0:a -map 1:0 \
       -c:a copy -c:v copy \
       -disposition:v:0 attached_pic \
       -map_chapters 0 \
       output.m4b
```

`-map 0:a` keeps just the audio stream (drops the binary chapter stream
that confused the muxer). `-map_chapters 0` explicitly re-embeds chapter
markers from the source as MP4 metadata. `-disposition:v:0 attached_pic`
tags the image as cover art so players show it on the lock screen / in
the library, not as a video track.

If no cover is supplied, `build_m4b.py` produces a valid M4B anyway —
the player just shows a generic audiobook icon.

## Logging discoveries — the lessons system

Audiobook production is empirical. Every book surfaces surprises (CB
mispronunciation, chunk-boundary artifacts, silence-cap settings, prose
patterns that interact weirdly with TTS, etc.). We capture them with a
three-layer system so the NEXT book doesn't repeat the discovery cycle.

### The three layers

| Layer | File | Purpose | Lifetime |
|---|---|---|---|
| **Rules** | `C:/AI/books/CLAUDE.md` (this file) | How to do the work, current state | Mutable, in-place |
| **Cross-book lessons** | `C:/AI/books/LESSONS_INDEX.md` | Promoted lessons that proved universal | Append-only with status flags |
| **Per-book journal** | `C:/AI/books/<book>/lessons.md` | Production discoveries from one book, with full diagnostic narrative | Append-only, frozen on ship |

Flow: surprise → write a lesson in the per-book journal → if it generalizes,
promote to LESSONS_INDEX → if it becomes a hard rule, bake into CLAUDE.md.

### Schema (one lesson = one node)

Every lesson is a stable-ID markdown section. Mandatory fields:

```
### L-NNN: Short title
- **Date**: YYYY-MM-DD
- **Book**: book-slug (where it was discovered)
- **Status**: active | superseded-by:L-XXX | observation
- **Symptom**: What was heard/seen
- **Diagnosis**: What was actually happening (root cause, not surface)
- **Fix**: Specific action taken
- **Rule**: General principle distilled
- **Related**: L-XXX, L-YYY (linked lessons)
- **CLAUDE.md ref**: section name (if rule lives there)
```

`L-NNN` IDs are stable forever — once assigned, never reused. `Related:`
forms the edge list of a node graph; cross-links are the navigation.
`Status: superseded-by:L-XXX` retires a lesson without deleting its
history.

### Using the logger

```
cd C:/AI/books/<book>
python C:/AI/books/log_lesson.py
```

Walks you through the schema interactively. Auto-detects the book from
cwd, auto-assigns the next L-NNN id (max across both files +1), auto-
stamps the date. For multi-line fields (symptom, diagnosis, fix, rule)
end with a single line containing only `END`.

The logger also auto-regenerates the index table at the top of each
affected file every time it runs — keeps the index honest without
manual maintenance.

### When to write a lesson

- Any time you fix a surprise during listen-through that took >5 min
  to diagnose.
- Any time you discover a setting or pattern that breaks in a way the
  current CLAUDE.md doesn't predict.
- Any time the author flags an issue you'd want a future reader of
  this codebase to anticipate.

Don't write a lesson for trivial code changes or obvious bug fixes —
the bar is "would a future me (or a future Claude) save time knowing
this?"

### Promotion criteria

A book-level lesson promotes to LESSONS_INDEX.md when ANY of:

- It's about a CB-pipeline component, not a book-specific quirk
  (`tts_normalize.py`, `render_sections.py`, `silence_cap`, `_tts.txt`,
  ffmpeg, voice settings, M4B build, etc.)
- The rule would apply to any future book on this pipeline.
- It was confirmed in 2+ books.

The logger suggests "promote?" automatically when it detects pipeline
keywords in your symptom/diagnosis/fix/rule fields. You can always
override.

### Reading the lessons

Open `LESSONS_INDEX.md` to scan the cross-book learning. Each entry's
`CLAUDE.md ref` field links back to the rule it became — so you can go
from "what surprised someone before" to "what the binding rule says
now" in one click.

For the diagnostic backstory ("why this rule exists, what symptom drove
it, what we tried and discarded"), open the per-book `lessons.md` —
that's where the narrative lives.

---

## Status: just_predicting_words

First book to take the full pipeline end-to-end (as of 2026-05-26):

- **Book is 21 chapters.** "Narrated files" and "M4B navigation markers"
  are larger numbers because they include wrappers — be precise about which
  count you mean in any conversation.
- **29 narrated files** = 3 front matter (opening credits, dedication,
  author's note) + 21 chapters + 3 appendices + 1 about-the-author + 1 closing
- Rendered via `render_sections.py` (section-by-section, ~3-5 min per
  section, 5-min iteration cycle for ear-detected fixes)
- 8h 55m total audio, 253 MB M4B
- **29 navigation markers** in the M4B (one per narrated file — lets the
  listener jump to any wrapper section as well as any chapter)
- 3000×3000 cover embedded via the two-step ffmpeg recipe above
- Lessons baked into this CLAUDE.md from the build:
  - The "Within the" metadata-regex false-match bug (drop body sentences
    that start with a prefix-only metadata token)
  - Standalone `...` pause lines produce phantom letter sounds on CB
  - Dot-spelled acronyms (`A.I.`, `G.P.T.`) produce letter stutter with
    the burton voice — reverted to bare
  - Italic epigraphs / "What comes next" lines should be dropped from audio
  - `silence_cap` `stop_duration=1.5` was too loose for prose with many
    short emphatic sentences — tightened to 0.9s threshold + 0.5s trim
  - Author's dramatic short sentences (`People cried. People laughed.`)
    are intentional rhetoric, NOT a bug to mass-fix in text — handle at
    the audio level via silence_cap settings

## Not yet (notes for later)

- ~~No chapter-spanning chunker yet.~~ Resolved: section renderer +
  `batch_render.py` both work end-to-end.
- ~~No M4B publisher.~~ Resolved: `build_m4b.py` per book.
- No cover-art renderer yet — book covers are produced by hand (or
  separately) and embedded post-hoc via the ffmpeg one-liner above.
- No private podcast feed publisher yet. Path forward: Vercel-hosted
  static RSS XML + per-chapter MP3s on Vercel Blob. See
  `feedback_cb_normalization_patterns.md` in memory for the design
  sketch.
- No subtitle / transcript export. CB doesn't return word timings; would
  need a Whisper pass over the rendered WAV if needed for SRT/VTT.
- No multi-voice / character-voice support. Single narrator per book.
