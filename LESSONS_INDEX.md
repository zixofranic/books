# Lessons Index — Audiobook Production on Chatterbox

Cross-book learning log for the local Chatterbox audiobook pipeline.
Each lesson is a node with a stable ID, edges to related lessons,
and a back-reference to the CLAUDE.md rule it became (if any).

This file aggregates lessons that proved **universal** across books on this
pipeline. Per-book learning journals live in `<book>/lessons.md` and may
include book-specific observations that don't generalize.

See `C:\AI\books\CLAUDE.md` → "Logging discoveries" for the system overview
and `C:\AI\books\log_lesson.py` for the interactive logger.

---

## Schema

Each lesson is one markdown section. Fields:

```
### L-NNN: Short title (sentence case, one line)
- **Date**: YYYY-MM-DD
- **Book**: book-slug (where it was discovered)
- **Status**: active | superseded-by:L-XXX | observation
- **Symptom**: What was heard/seen that didn't match expectation
- **Diagnosis**: What was actually happening (root cause, not just description)
- **Fix**: Specific action taken — code change, setting tune, text edit
- **Rule**: General principle distilled (the part that becomes a rule)
- **Related**: L-XXX, L-YYY (linked lessons — the edge list)
- **CLAUDE.md ref**: Section name where the rule lives (if promoted to ruleset)
```

`L-NNN` IDs are stable forever — once assigned, never reused.
`superseded-by` is used when a later lesson invalidates this one
(keep the entry, just change status).

---

## Index

| ID | Title | Status | Date | Book |
|----|-------|--------|------|------|
| L-001 | Years read inconsistently as digit strings | active | 2026-05-22 | just_predicting_words |
| L-002 | CamelCase brand names mispronounced as run-together gibberish | active | 2026-05-23 | just_predicting_words |
| L-003 | Dot-spelled acronyms cause letter stutter on burton voice | active | 2026-05-24 | just_predicting_words |
| L-004 | Number-suffixed model names need word-form numbers | active | 2026-05-23 | just_predicting_words |
| L-005 | ALL-CAPS section headings detected reliably from raw, not _clean.txt | active | 2026-05-23 | just_predicting_words |
| L-006 | Standalone "..." pause lines produce phantom letter sounds | active | 2026-05-23 | just_predicting_words |
| L-007 | Italic epigraphs read as extra title sentences in audio | active | 2026-05-23 | just_predicting_words |
| L-008 | METADATA_LINE prefix-only patterns false-match body sentences | active | 2026-05-23 | just_predicting_words |
| L-009 | silence_cap stop_duration=1.5s too loose for dramatic short sentences | active | 2026-05-25 | just_predicting_words |
| L-010 | Author's dramatic short sentences are intentional prose, fix at audio level | active | 2026-05-25 | just_predicting_words |
| L-011 | Embedded ALL-CAPS brand mentions need Title-casing mid-sentence | active | 2026-05-23 | just_predicting_words |
| L-012 | Glossary cross-references in ALL-CAPS need Title-casing too | active | 2026-05-23 | just_predicting_words |
| L-013 | Section heading detection needs lowercase tolerance for CamelCase brand prefixes | active | 2026-05-23 | just_predicting_words |
| L-014 | Section-by-section rendering gives 5-min iteration vs 25-min per chapter | active | 2026-05-25 | just_predicting_words |
| L-015 | M4B cover embed — strip alpha + explicitly map chapters | active | 2026-05-26 | just_predicting_words |
| L-016 | "Chapter" vs "navigation marker" — be precise about which count is meant | active | 2026-05-26 | just_predicting_words |
| L-017 | Three-layer lessons system: rules / index / per-book journal | active | 2026-05-26 | just_predicting_words |
| L-018 | ffmpeg concat demuxer resolves paths relative to the list file, not cwd | active | 2026-05-26 | just_predicting_words |
| L-019 | Windows cp1252 console crashes on Unicode arrows in Python print() | active | 2026-05-26 | just_predicting_words |
| L-020 | Narrated-files allowlist required, not *.txt glob | active | 2026-05-26 | just_predicting_words |
| L-021 | `render_sections.py all` defers assembly until ALL sections render — manually assemble mid-batch for progressive listening | active | 2026-05-26 | just_predicting_words |
| L-022 | Validate the full TTS recipe on one chapter before committing full-book GPU time | active | 2026-05-26 | just_predicting_words |
| L-023 | CB synthesis is opaque mid-render — log silence is normal, not stuck | active | 2026-05-26 | just_predicting_words |
| L-024 | Possessive 'S in ALL-CAPS headings title-cased into a standalone capital letter | active | 2026-05-28 | just_predicting_words |
| L-025 | ALL-CAPS banner between dividers is a file/editorial label, not always the spoken heading | active | 2026-05-28 | just_predicting_words |
| L-026 | Brands in ALL-CAPS headings get capitalized to gibberish ("OPENAI" -> "Openai") | active | 2026-05-28 | just_predicting_words |
| L-027 | Legal "v." citation read as "via"/"vee" instead of "versus" | active | 2026-05-28 | just_predicting_words |

---

## Lessons

### L-001: Years read inconsistently as digit strings
- **Date**: 2026-05-22
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: Listener heard "two zero two five" instead of "twenty twenty-five" at one chunk boundary, while the same `2025` was read correctly elsewhere in the same chapter.
- **Diagnosis**: Chatterbox's internal number-to-speech heuristic flips based on chunk position + seed. Not deterministic across chunk boundaries within a file. Year-shaped numbers especially affected.
- **Fix**: `tts_normalize.py` substitutes digit-form years with their spoken form (`2025` → "twenty twenty-five", `2008` → "two thousand eight", `1998` → "nineteen ninety-eight") + decade plurals (`2010s` → "twenty tens"). Done before CB ever sees the text.
- **Rule**: Always pre-substitute years with their spoken form in the `_tts.txt`. Don't trust CB to read year-shaped digits consistently.
- **Related**: L-004 (model versions — sibling number-handling issue)
- **CLAUDE.md ref**: "Pattern substitutions to apply in `_tts.txt`" → item 6


### L-002: CamelCase brand names mispronounced as run-together gibberish
- **Date**: 2026-05-23
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: `OpenAI`, `ChatGPT`, `DeepMind` etc. came out as garbled syllable mashups in CB's voice.
- **Diagnosis**: CB doesn't split CamelCase tokens internally. It tries to read them as single words and produces nonsense phonemes.
- **Fix**: `BRAND_FIXES` dict in `tts_normalize.py` maps each CamelCase brand to a space-separated form: `OpenAI` → "Open AI", `ChatGPT` → "Chat GPT", `DeepMind` → "Deep Mind", `AlphaFold` → "Alpha Fold", etc. ~18 brands enumerated.
- **Rule**: Pre-split every CamelCase brand in `_tts.txt`. Maintain an explicit dict — don't try to auto-detect via regex (false positives on legitimate proper names like `iPhone`).
- **Related**: L-011 (embedded ALL-CAPS brand mentions), L-013 (CamelCase in section headings)
- **CLAUDE.md ref**: "Pattern substitutions to apply in `_tts.txt`" → item 3


### L-003: Dot-spelled acronyms cause letter stutter on burton voice
- **Date**: 2026-05-24
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: Listener heard "consumer A I I assistants" — an extra "I" inserted after `A.I.` Same artifact on other dot-spelled acronyms.
- **Diagnosis**: We had tried writing acronyms as `A.I.`, `G.P.T.` with periods to force CB to pause between letters. With burton's voice/seed, the trailing period at the end of the dot-spelled acronym caused CB to repeat the final letter at the next chunk boundary. The "test one chapter first" warning in the original normalizer README was correct.
- **Fix**: Reverted `SPELL_OUT` dict to identity mappings (`"AI": "AI"`, `"GPT": "GPT"`). Acronyms stay bare in `_tts.txt`. CB reads them adequately when not dot-spelled — same behavior as v1 audio which didn't have this problem. Period substitutions in BRAND_FIXES (`OpenAI` → "Open A.I.") also reverted to bare ("Open AI"). For an acronym that mispronounces specifically, override with phonetic spelling ("AGI" → "ay gee eye") — not periods.
- **Rule**: Never dot-spell acronyms in `_tts.txt`. Bare form is CB-safe; phonetic form is the escape hatch when needed.
- **Related**: L-006 (sibling CB-audio gotcha, similar empirical-validation lesson)
- **CLAUDE.md ref**: "Pattern substitutions to apply in `_tts.txt`" → item 4


### L-004: Number-suffixed model names need word-form numbers
- **Date**: 2026-05-23
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: `GPT-4` read as "G P T dash four" with weird pacing; `Gemini 2.5` mangled.
- **Diagnosis**: CB sees the hyphen + digit and can't decide whether the digit is a numeral or a label. Same chunk-boundary inconsistency as years.
- **Fix**: `fix_model_versions()` substitutes: `GPT-4` → "GPT four", `Gemini 2.5` → "Gemini two point five", `K2.6` → "K two point six", `AI21` → "AI twenty-one", `WMT24` → "W M T twenty twenty-four". Must run BEFORE acronym handling, or `GPT-4` becomes `G.P.T.-4` and the regex misses it.
- **Rule**: Pre-substitute all `Brand-N` or `Brand N.M` patterns into spoken form. Run before acronym handling.
- **Related**: L-001 (years), L-003 (acronyms)
- **CLAUDE.md ref**: "Pattern substitutions to apply in `_tts.txt`" → item 1


### L-005: ALL-CAPS section headings detected reliably from raw, not _clean.txt
- **Date**: 2026-05-23
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: `THE STUMBLE` (2-word ALL-CAPS) stayed all-caps in `_clean.txt`, while `THE COMPANY BEFORE THE STUMBLE` (5-word) was sentence-cased to `"The company before the stumble."`. Inconsistent.
- **Diagnosis**: `clean_chapter.py` only sentence-cases ALL-CAPS lines with 3+ words. The 2-word rule was intentional (to skip false positives like "THE END") but it also skipped legitimate 2-word headings.
- **Fix**: `tts_normalize.py` works from `source/raw/*.txt`, NOT from `_clean.txt`. In raw, all section headings are reliably ALL-CAPS between `· · ·` dividers — no inconsistency to inherit. Title-case via regex on alphabetic tokens (`re.sub(r"[A-Za-z]+", repl, s)`) so punctuation like `(ARTIFICIAL` doesn't break naïve splits.
- **Rule**: For TTS normalization, read RAW chapter sources directly. Don't inherit clean_chapter.py's heuristic decisions about headings.
- **Related**: L-013 (heading detection edge case)
- **CLAUDE.md ref**: "Section heading detection"


### L-006: Standalone "..." pause lines produce phantom letter sounds
- **Date**: 2026-05-23
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: Listener heard a stray "E" letter between the chapter title and the body of chapter 7. Same artifact appeared everywhere a `...` line stood alone between blanks.
- **Diagnosis**: CB vocalizes a standalone `...` line as a letter sound (not as silence). The CLAUDE.md note that "CB honors ellipses for pause cues" turned out to apply to INLINE ellipses only. We had been adding standalone `...` lines to extend pauses between title/subtitle/section heading and body.
- **Fix**: Removed all standalone `...` lines from `tts_normalize.py`'s output. Kept ONLY inline trailing `...` on title/subtitle/heading lines. Blank lines do the rest of the pause work.
- **Rule**: Inline trailing `...` is CB-safe. Standalone `...` lines are NOT. Validate empirically on the chosen voice before assuming any pause-cue idea works.
- **Related**: L-003 (sibling CB-audio gotcha)
- **CLAUDE.md ref**: "Pause cues — INLINE trailing only, never standalone"


### L-007: Italic epigraphs read as extra title sentences in audio
- **Date**: 2026-05-23
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: The italic chapter epigraph (`*They built the architecture that powers every AI assistant in the world. Then they sat on it.*`) read as a third title sentence in the audio. In print it's a visual flourish; in audio it sounds like an extra title beat that doesn't belong.
- **Diagnosis**: Wholly-italic lines (lines where all non-whitespace content is wrapped in `*...*`) are deliberately decorative — chapter teasers in print, "what comes next" callouts at chapter end. Audio doesn't have a typographic register to mark them as different.
- **Fix**: `WHOLLY_ITALIC_LINE` regex in `tts_normalize.py` detects single-line italic blocks (`^\*[^*]+\*$` after `collapse_italics`) and drops them entirely. Mid-sentence emphasis (`This was *not* enough`) is unaffected — keeps the word, just strips the asterisks.
- **Rule**: Drop wholly-italic lines from audio. Keep mid-sentence italics with asterisks stripped.
- **Related**: L-008 (similar "drop entirely" decision for metadata)
- **CLAUDE.md ref**: "Italic epigraphs / teasers"


### L-008: METADATA_LINE prefix-only patterns false-match body sentences
- **Date**: 2026-05-23
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: A body sentence — "Within the next eight years, all eight of those researchers had left Google" — was missing from BOTH `_clean.txt` and `_tts.txt` for ch 7. Audio had a noticeable gap in the narrative.
- **Diagnosis**: `METADATA_LINE` regex in `clean_chapter.py` listed `"Within the"` as a metadata-block prefix (presumably for book-design-doc metadata like *"Within the company's voice..."*). It false-matched the body sentence and triggered the metadata-block skip behavior, dropping the line.
- **Fix**: Removed `"Within the"` from METADATA_LINE in `tts_normalize.py`. Audited remaining prefix-only patterns in the regex and confirmed no other body sentences across the book false-match.
- **Rule**: Avoid prefix-only patterns in METADATA_LINE. Prefer patterns with explicit colons (`Working draft:`, `Voice:`) or ALL-CAPS line patterns (`TITLE PAGE`) that can't accidentally match prose.
- **Related**: L-005 (also about avoiding inherited cleaner heuristics)
- **CLAUDE.md ref**: "Metadata-regex gotcha"


### L-009: silence_cap stop_duration=1.5s too loose for dramatic short sentences
- **Date**: 2026-05-25
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: Listener heard a too-long pause before the word "badly" in `Google was losing. Badly.`
- **Diagnosis**: The existing `silence_cap` config used `stop_duration=1.5` (only trim silences LONGER than 1.5 seconds) and `stop_silence=0.7` (trim to 0.7s). CB at the period boundary was inserting ~1.3s of silence — slipping under the 1.5s threshold, never trimmed. Heard as "long pause."
- **Fix**: Added `stop_duration` field to `Voice` class in `voices.py`. Burton config tightened to `stop_duration=0.9, stop_silence=0.5` — any pause over 0.9s gets trimmed to 0.5s. Re-processed existing `_raw_pre_silcap/*.wav` files (ffmpeg only, no CB re-synth) — chapter shrunk ~18s and the dramatic short sentences now land as beats instead of dead air.
- **Rule**: Silence-cap is a per-voice setting. Tune `stop_duration` to be SHORTER than the typical chunk-boundary silence CB inserts on punctuation-heavy prose. Test on a chapter with many short emphatic sentences before committing to settings.
- **Related**: L-010 (sibling realization — fix at audio not text level)
- **CLAUDE.md ref**: voices.py burton config + recipe section


### L-010: Author's dramatic short sentences are intentional prose, fix at audio level
- **Date**: 2026-05-25
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: Audit of all chapters surfaced 100+ instances of short emphatic sentences (`People cried. People laughed. People got angry.`, `Contracts. Emails. Reports.`, etc.) similar in shape to the `losing. Badly.` case that triggered investigation.
- **Diagnosis**: This is the author's deliberate rhetorical style, not a bug. Mass-replacing periods with commas would rewrite the book's voice.
- **Fix**: Did NOT touch the text. Instead tightened `silence_cap` settings (L-009) to handle the CB over-pause behavior at the audio level. Text stays as the author wrote it; audio handles the timing.
- **Rule**: When a CB rendering artifact correlates with a stylistic pattern that's intentional in the source, fix at the audio post-processing level (silence_cap, atempo) not the text level. Only edit text when CB's reading is wrong (mispronunciation, missed sentence). Don't edit text for prosody.
- **Related**: L-009 (the actual fix this rule enables)
- **CLAUDE.md ref**: "Render granularity" + voices.py burton notes


### L-011: Embedded ALL-CAPS brand mentions need Title-casing mid-sentence
- **Date**: 2026-05-23
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: A section heading `WHAT GOOGLE BELIEVES` got sentence-cased by `clean_chapter.py` to `What GOOGLE believes.` — the brand stayed all-caps mid-sentence. CB would have read it as "What G-O-O-G-L-E believes."
- **Diagnosis**: `clean_chapter.py`'s sentence-case logic processed the whole line but kept already-ALL-CAPS tokens uppercase, intending to preserve acronyms. Brand names in caps got swept along.
- **Fix**: `BRAND_CAPS` dict in `tts_normalize.py` maps known ALL-CAPS brand forms to their mixed-case spelling (`GOOGLE` → "Google", `META` → "Meta", `OPENAI` → "Open AI", etc.). Applied via `fix_embedded_brand_caps`.
- **Rule**: When a known brand appears in ALL-CAPS inside a normal sentence, re-case it to its standard mixed-case form. Acronyms (in SPELL_OUT) are excluded — they stay as they are.
- **Related**: L-002 (CamelCase brand handling)
- **CLAUDE.md ref**: "Pattern substitutions to apply in `_tts.txt`" → item 2


### L-012: Glossary cross-references in ALL-CAPS need Title-casing too
- **Date**: 2026-05-23
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: In appendix A (glossary), entries referenced other terms like "See EMBEDDING. A list of numbers that..." — `EMBEDDING` stayed all-caps inside body prose.
- **Diagnosis**: Same root cause as L-011 but in a different context — cross-reference convention in glossaries. Not a brand, but a known term being pointed at.
- **Fix**: `fix_embedded_all_caps()` Title-cases any 4+ char ALL-CAPS word remaining in body text that isn't already in SPELL_OUT or BRAND_CAPS. Conservative threshold (4+ chars) avoids touching real acronyms like USA, NATO, etc.
- **Rule**: After dict-based brand and acronym substitution, sweep remaining embedded ALL-CAPS tokens (4+ chars, not in any dict) and Title-case them. Catches glossary refs and any missed proper nouns.
- **Related**: L-011 (sibling Title-casing rule for brands)
- **CLAUDE.md ref**: "Pattern substitutions to apply in `_tts.txt`" → item 5


### L-013: Section heading detection needs lowercase tolerance for CamelCase brand prefixes
- **Date**: 2026-05-23
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: Section heading `xAI, THE LAB THAT BECAME A SPACE COMPANY` wasn't detected as a heading. Result: it stayed uppercase in the body, and the "long heading" rendered poorly.
- **Diagnosis**: Strict `^[A-Z]` heading regex failed because the line started with lowercase `x` (the `xAI` brand). The single CamelCase brand prefix disqualified an otherwise-all-caps line.
- **Fix**: `is_section_heading()` uses a percentage rule: ≥80% of letters uppercase + line ≤20 words + ≥3 letters. Allows CamelCase brand prefixes inside otherwise-all-caps headings.
- **Rule**: Don't use strict `^[A-Z]` for heading detection. Use a percentage-of-uppercase rule that tolerates CamelCase brand tokens at any position in the heading.
- **Related**: L-005 (also about heading detection)
- **CLAUDE.md ref**: "Section heading detection"


### L-014: Section-by-section rendering gives 5-min iteration vs 25-min per chapter
- **Date**: 2026-05-25
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: Each ear-detected issue during listening required a full ~25 min chapter re-render to validate the fix. With 28 chapters and 2-3 iterations each, the iteration cost was crippling.
- **Diagnosis**: CB renders chapter-as-one-chunk had no way to fix just one bad moment without redoing the whole thing.
- **Fix**: Built `render_sections.py` — splits each `_tts.txt` on ALL-CAPS section heading lines (the trailing `...` markers from `tts_normalize.py`'s structural pass), renders each section as a separate WAV (~3-5 min each), concatenates via ffmpeg into the final chapter MP3. Per-chapter `sections/<chapter>/_manifest.json` tracks SHA hashes per section — edit a section's text and only THAT section gets re-rendered on the next run. Each chapter also gets a `listening/<chapter>.md` companion file with timestamp → section navigation.
- **Rule**: For any audiobook over ~3 chapters or any expected iteration cycle, render section-by-section. Concat to chapter MP3 at the end. Per-section manifests + SHA hashing make stale-section detection automatic.
- **Related**: L-009, L-010 (most fixes during JPW listening would have been prohibitive without this)
- **CLAUDE.md ref**: "Render granularity: section-by-section"


### L-015: M4B cover embed — strip alpha + explicitly map chapters
- **Date**: 2026-05-26
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: First attempt to embed the cover JPG into the M4B failed with `Tag text incompatible with output codec id '98314'` from ffmpeg. The naive `ffmpeg -i input.m4b -i cover.jpg -map 0 -map 1 -c copy -disposition:v:0 attached_pic out.m4b` command from the CLAUDE.md cover-art note didn't work.
- **Diagnosis**: Two distinct issues. (a) The cover JPG had alpha channel (`yuva444p` pixel format) — the MP4/ipod muxer doesn't accept that. (b) `-map 0` includes the binary chapter-text stream that the M4B uses to store chapter markers — the ipod muxer rejects it as an incompatible text codec.
- **Fix**: Two-step process. Step 1: `ffmpeg -y -i cover_with_alpha.jpg -pix_fmt yuvj420p -q:v 2 cover_std.jpg` strips alpha to standard JPEG pixel format. Step 2: `ffmpeg -y -i input.m4b -i cover_std.jpg -map 0:a -map 1:0 -c:a copy -c:v copy -disposition:v:0 attached_pic -map_chapters 0 output.m4b` maps only the audio stream from input (drops the binary chapter stream), maps the cover image, copies both (no re-encode), explicitly re-embeds chapters via `-map_chapters 0`. Final M4B has audio + chapter metadata + cover, all preserved.
- **Rule**: When embedding cover art into an existing M4B, never use `-map 0` blanket — explicitly select `-map 0:a` and re-embed chapters via `-map_chapters 0`. Always normalize the cover to RGB pixel format first (`-pix_fmt yuvj420p`).
- **Related**: none
- **CLAUDE.md ref**: "Cover art" section under "Build M4B"


### L-016: "Chapter" vs "navigation marker" — be precise about which count is meant
- **Date**: 2026-05-26
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: I referred to "29 chapter markers" in the M4B when the book has only 21 chapters. Author flagged the imprecision.
- **Diagnosis**: The M4B's navigation markers include not just chapters but also front matter (opening credits, dedication, author's note), appendices (A, B, C), about-the-author, and closing. 29 markers = 3 + 21 + 3 + 1 + 1. Calling all of them "chapters" is wrong.
- **Fix**: Use "navigation markers" or "track markers" for the M4B navigation points. Reserve "chapters" for the actual book chapters (21 in JPW). Updated CLAUDE.md Status section to make the distinction explicit.
- **Rule**: A book has chapters. An M4B has navigation markers — usually MORE than chapters because front matter, appendices, etc. each get their own marker. Always be explicit about which count you mean in any author-facing communication.
- **Related**: none
- **CLAUDE.md ref**: "Status: just_predicting_words"


### L-017: Three-layer lessons system: rules / index / per-book journal
- **Date**: 2026-05-26
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: Repeated TTS-pipeline discoveries during ch 7 iteration (year mispronunciation, stutter, missing sentences, silence_cap tuning). No structured place to capture them — risk of next book repeating the same diagnostic cycle.
- **Diagnosis**: No persistent learning loop existed across books. CLAUDE.md held current rules; Claude memory held cross-conversation context; nothing aggregated the journey from 'surprise' to 'diagnosis' to 'rule.' Each new book would have re-discovered the same gotchas.
- **Fix**: Built three coordinated layers: (1) CLAUDE.md = current ruleset (universal); (2) C:/AI/books/LESSONS_INDEX.md = promoted lessons that proved universal (graph of nodes with stable L-NNN IDs and Related: edges); (3) <book>/lessons.md = per-book production journal with the full diagnostic narrative. Plus log_lesson.py — interactive logger that auto-detects book from cwd, auto-assigns next L-NNN id, auto-stamps date, regenerates index tables on each run, and suggests promotion via a keyword heuristic when the lesson mentions CB-pipeline components.
- **Rule**: When working on the next book, search LESSONS_INDEX.md FIRST for any symptom that resembles what you are hearing. Most pipeline issues are already documented. New surprises get logged via log_lesson.py from the book dir.
- **CLAUDE.md ref**: Logging discoveries — the lessons system


### L-018: ffmpeg concat demuxer resolves paths relative to the list file, not cwd
- **Date**: 2026-05-26
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: ffmpeg concat failed with cryptic 'No such file or directory' even though every WAV listed in the concat.txt existed and the command was run from C:/AI/books/. Error showed a duplicated path: just_predicting_words/audio_v2/sections/07_chapter_07/just_predicting_words/audio_v2/sections/07_chapter_07/01_intro.wav.
- **Diagnosis**: The ffmpeg concat demuxer (-f concat) resolves each 'file ...' entry in the list relative to the LIST FILE'S directory, not cwd or absolute. Writing relative paths from cwd in the concat list double-prefixes the path.
- **Fix**: render_sections.assemble_chapter() writes ONLY the basename in the concat list (e.g. file '01_intro.wav') since the WAVs sit in the same directory as the _concat.txt. ffmpeg resolves correctly. Caveat: this means concat.txt has to live next to the source WAVs — moving it breaks the relative resolution.
- **Rule**: When writing an ffmpeg concat list, write basenames if the WAVs are in the same directory as the list file. Otherwise use absolute paths. Never write 'cwd-relative' paths in a concat list — ffmpeg ignores cwd for this format.
- **Related**: L-014
- **CLAUDE.md ref**: Build M4B (pipeline step 1 — concat) / Render granularity


### L-019: Windows cp1252 console crashes on Unicode arrows in Python print()
- **Date**: 2026-05-26
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: render_sections.assemble_chapter() printed a [assembled] line using a → arrow character. Background batch crashed with UnicodeEncodeError: 'charmap' codec can't encode character '\u2192' — but ONLY after all 7 sections of ch 7 rendered successfully + the concat + the manifest write all completed. Logs were silent until the very last print statement hit.
- **Diagnosis**: Windows console default codepage is cp1252 (NOT UTF-8). Python print() encodes stdout using that codepage when stdout is a console or being captured (e.g. by `| tee` redirect). Unicode arrows (→, ←, ↔), em-dashes (—), and other non-cp1252 characters crash print() at runtime. The crash happens at the FINAL log line, not earlier, because the earlier lines all used ASCII.
- **Fix**: Replaced → with -> in the assembled-log line. Going forward, stdout-bound print() statements in pipeline scripts use ASCII only. The docstring + markdown files can still use unicode (they're written via file I/O with explicit encoding='utf-8').
- **Rule**: Python scripts running on Windows must use ASCII-only characters in print() / log messages. Unicode is fine for file content (with encoding='utf-8'), never for stdout. Arrows: -> and <-. Em-dash: -- or just plain hyphen. Specifically dangerous: → ← — – ✓ ✗ • · (any non-cp1252 char).
- **CLAUDE.md ref**: Where this runs (recording infrastructure)


### L-020: Narrated-files allowlist required, not *.txt glob
- **Date**: 2026-05-26
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: Ran tts_normalize.py on source/raw/*.txt to normalize everything. Then ran render_sections.py prep / render. Result: the section renderer picked up book-design docs that weren't supposed to be narrated — 00_artistic_direction.txt, 00_book_structure.txt, 00_cross_reference_audit.txt, 00_illustration_strategy.txt, 00_visual_language_locked.txt, 00_front_matter_complete.txt, 00_author_bio.txt (draft, not FINAL) — and rendered them. Wasted ~30 GPU min + audio files that needed manual cleanup.
- **Diagnosis**: render_sections.find_tts_files() uses sorted((book_dir / 'source').glob('*_tts.txt')). It accepts every _tts.txt in source/ regardless of whether it's part of the narrated audiobook. The narrative order is encoded in batch_render.py RENDER_ORDER but not enforced as a filter — anything with a _tts.txt becomes a render target.
- **Fix**: Documented as a gotcha. Long-term fix: have render_sections.py consult the book's RENDER_ORDER (or an explicit allowlist file) instead of globbing. Short-term workaround: don't tts_normalize *.txt indiscriminately — pass an explicit list of narrated files, OR clean up the non-narrated _tts.txt files before running the section pipeline.
- **Rule**: Define the narrated-files set explicitly per book (e.g. RENDER_ORDER list). Don't rely on file-system globbing to decide what gets rendered. The cost of a stray _tts.txt is wasted GPU + cleanup.
- **Related**: L-014
- **CLAUDE.md ref**: Adding a new book


### L-021: `render_sections.py all` defers assembly until ALL sections render — manually assemble mid-batch for progressive listening
- **Date**: 2026-05-26
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: Kicked off `render_sections.py all` to render the full book (~9 hours of GPU time). After ~4.6 hours, 13 chapters were fully rendered as sections — but NO chapter MP3s existed in audio_v2/ root yet. Couldn't listen to any chapter while the batch was still running on later chapters.
- **Diagnosis**: The `all` command has two phases: prep + render_pending + (global) assemble loop. The assemble loop only runs after ALL sections across ALL chapters complete. So chapter 1's sections finishing at hour 1 don't trigger ch 1 assembly — ch 1 stays un-assembled until hour 9 when the last section completes.
- **Fix**: Manually ran a side-script that iterated all chapters, found ones with all sections rendered + chapter_assembled=False, and called assemble_chapter() on them. This is safe to run in parallel with the batch as long as it only touches finished chapters (the batch is still on a later chapter — no race condition on the manifest of an already-done chapter). Result: 13 chapters became listenable mid-batch.
- **Rule**: When watching a long batch render, run the mid-batch assembly side-script to make completed chapters listenable as they finish. Long-term fix: change `render_pending` to auto-call `assemble_chapter` immediately after a chapter's last section completes, not at end-of-batch.
- **Related**: L-014
- **CLAUDE.md ref**: Render granularity: section-by-section


### L-022: Validate the full TTS recipe on one chapter before committing full-book GPU time
- **Date**: 2026-05-26
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: First full-book render attempt baked in three subtle bugs (L-006 phantom letters, L-003 dot-spelled stutter, L-008 missing sentence). Caught only when the user listened to ch 7. If the batch had completed, all 28 narrated files would have had the same issues — ~9 hours of wasted GPU + redo cost.
- **Diagnosis**: Recipe-wide artifacts (anything in tts_normalize.py, voices.py, or the render pipeline that applies uniformly to all chapters) are catastrophic if undetected — they hit every chapter identically. Listening to ch 1 in full is the cheap insurance that catches them before they multiply 21x.
- **Fix**: Established a discipline (now in CLAUDE.md): render ONE chapter first (~25 min GPU), listen end-to-end, validate years / acronyms / brand names / section transitions / pause cues. Only then kick off the full batch. The 25-min upfront cost saves hours of redo time.
- **Rule**: Always test the full TTS recipe on one chapter (preferably one rich in the patterns the recipe handles — for JPW that was ch 7 with its years, acronyms, brands, and section headings) before kicking off the full-book batch. Listen to all of it, not just the first 30 seconds. Recipe-wide bugs are silent in scans and catastrophic in production.
- **Related**: L-014, L-006, L-003, L-008
- **CLAUDE.md ref**: Test protocol — never commit GPU time blindly


### L-023: CB synthesis is opaque mid-render — log silence is normal, not stuck
- **Date**: 2026-05-26
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: Kicked off a chapter render. After 5-10 minutes, the render log file was still 0 bytes and CB endpoint timeouts. Worried the process was hung. Checked process state — Python alive with ~0 CPU; CB endpoint busy. Was this normal or stuck?
- **Diagnosis**: Chatterbox returns the full WAV in a single HTTP response at the END of synthesis. There's no streaming, no progress callback, no log output during the 5-25 min synth window. Python sits idle on requests.post() until the response lands. The wrapper script doesn't write anything to stdout until AFTER the synth + atempo + silence_cap + mp3 conversion chain completes. So 'no log output for 20 minutes' is exactly what a healthy CB render looks like.
- **Fix**: Documented the expected timing as a check rather than a fix. Health-check during a long render: (1) python process alive (Get-Process or ps), (2) CB endpoint responds 'busy' (HTTP timeout to localhost:8004/ is correct — it's locked on the inference call), (3) GPU utilization high (nvidia-smi). If all three: render is fine, just wait.
- **Rule**: CB inference is a long blocking HTTP call (5-25 min per section/chapter). No stdout output, no log writes, no progress indicators during synth. Empty log + CB endpoint timeout + alive python process = healthy render in progress. Don't kill it during this window unless ALL THREE signals fail.
- **CLAUDE.md ref**: Where this runs (recording infrastructure)


### L-024: Possessive 'S in ALL-CAPS headings title-cased into a standalone capital letter
- **Date**: 2026-05-28
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: An ALL-CAPS heading containing a possessive (e.g. `AUTHOR'S NOTE`, `WHAT'S COMING`) renders in audio as the word, then a chunk-boundary pause, then a spelled-out capital letter "S", then the rest run together. Heard on the JPW m4b as "Author ... [3s] ... S Note on AI use, final locked version."
- **Diagnosis**: `title_case_heading()` title-cases via `re.sub(r"[A-Za-z]+", repl, s)`. The apostrophe is outside `[A-Za-z]`, so `AUTHOR'S` splits into two tokens — `AUTHOR` and `S`. `AUTHOR` → "Author"; the lone single-char `S` fails the `len(word) >= 2` capitalize guard and is returned unchanged as a capital "S" → `Author'S`. CB reads a standalone capital letter as a spelled letter (same artifact family as dot-spelled acronyms, L-003).
- **Fix**: Change the title-case word regex to keep the possessive tail together: `re.sub(r"[A-Za-z]+(?:'[A-Za-z]+)?", repl, s)`. `str.capitalize()` then does the right thing — `"AUTHOR'S".capitalize()` → `"Author's"`, `"WHAT'S".capitalize()` → `"What's"`. Re-render the affected sections (text changed → CB re-synth) and rebuild the m4b.
- **Rule**: Heading title-casing must treat possessive `'S`/`'s` as part of the word, never as a standalone token. A lone capital letter anywhere in `_tts.txt` is a CB letter-spell trap. When title-casing by alphabetic-token regex, include the apostrophe tail.
- **Related**: L-005, L-013 (heading detection / title-casing), L-003 (standalone-letter CB artifact)
- **CLAUDE.md ref**: "Section heading detection"


### L-025: ALL-CAPS banner between dividers is a file/editorial label, not always the spoken heading
- **Date**: 2026-05-28
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: Front-matter/wrapper tracks misbehave at the top: the Dedication track says "Dedication" twice; the Author's Note and About-the-Author tracks open by narrating editorial cruft ("...On AI Use, Final Locked Version", "Author Bio, Final Locked Version") instead of their real titles.
- **Diagnosis**: Raw files wrap an ALL-CAPS banner between `====` dividers as the file's editorial label (`DEDICATION`, `AUTHOR'S NOTE ON AI USE - FINAL LOCKED VERSION`, `AUTHOR BIO - FINAL LOCKED VERSION`). `is_section_heading()` matches it and `parse_and_structure()` emits it as the spoken heading. For chapters the banner equals the title (correct). For front matter it isn't: (a) the banner can duplicate the body's first line (DEDICATION heading + "Dedication." body → read twice — no heading↔body dedup exists); (b) the banner carries version/editorial cruft that should never be spoken and buries the real title, which lives in the body.
- **Fix**: For non-chapter/wrapper files, source the spoken heading from an explicit per-file title map (the M4B builder's `TITLES` dict) rather than the raw banner; OR strip editorial suffixes (`- FINAL LOCKED VERSION`, `- FINAL`, `LOCKED`, `VERSION`, descriptor tails) from banner headings. Additionally, dedup: if the emitted heading equals the next non-blank body line case-insensitively, drop one. Note clean banners (`OPENING CREDITS`, `CLOSING CREDITS`) read fine, so a blanket "drop all banners" is wrong.
- **Rule**: The ALL-CAPS banner between `====` dividers is the file's editorial label. For chapters it equals the title (narrate it). For front-matter/wrappers it's a descriptor that may duplicate the body or carry version cruft — never narrate it blindly. Prefer an explicit per-file spoken title, strip FINAL/LOCKED/VERSION suffixes, and dedup heading vs. first body line.
- **Related**: L-008 (dropping non-prose), L-020 (front-matter needs explicit handling), L-016 (wrappers are not chapters)
- **CLAUDE.md ref**: "Section heading detection"


### L-026: Brands in ALL-CAPS headings get capitalized to gibberish ("OPENAI" -> "Openai")
- **Date**: 2026-05-28
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: A brand inside an ALL-CAPS section/chapter heading is mispronounced — "...THAT WRAPS OPENAI" reads "oh-pe-nai" instead of "Open A-I"; "CHATGPT" reads "Chatgpt". Heard across multiple chapter/appendix titles.
- **Diagnosis**: `title_case_heading()` runs `str.capitalize()` on every ALL-CAPS token not in its keep-set (acronyms only). A brand like `OPENAI`/`CHATGPT` becomes "Openai"/"Chatgpt" during the structural pass — BEFORE the brand-substitution passes run. By then the token is mixed-case, so `fix_embedded_brand_caps` (which matches `\bOPENAI\b`) no longer fires and `fix_brands` (which matches CamelCase `OpenAI`) never matches either. The brand is stranded in an unpronounceable form.
- **Fix**: Build one combined ALL-CAPS brand map `BRAND_CAPS_ALL` = uppercased `BRAND_FIXES` keys merged with `BRAND_CAPS`. Add its keys to `title_case_heading`'s keep-set (brand survives title-casing as ALL-CAPS), and have `fix_embedded_brand_caps` iterate the combined map (so the preserved `OPENAI` → "Open AI", `CHATGPT` → "Chat GPT" everywhere). 
- **Rule**: Heading title-casing must PRESERVE known brands rather than capitalize them; a downstream brand pass converts them. Keep one combined ALL-CAPS brand map shared by the heading keep-set and the embedded-brand-caps sub. A brand mangled to mixed-case is invisible to every later brand regex.
- **Related**: L-002 (CamelCase brands), L-011 (embedded ALL-CAPS brands), L-024 (sibling title_case_heading bug)
- **CLAUDE.md ref**: "Section heading detection"


### L-027: Legal "v." citation read as "via"/"vee" instead of "versus"
- **Date**: 2026-05-28
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: In court-case citations ("Varghese v. China Southern Airlines") and a "Complement Vs Substitute" heading, CB reads the legal abbreviation `v.`/`Vs` as the letter or "via" rather than "versus".
- **Diagnosis**: No normalization existed for the legal versus abbreviation; CB doesn't expand it.
- **Fix**: `fix_legal_versus()` substitutes space-bounded `v.` / `vs.` / `vs` → "versus". It deliberately does NOT touch a bare single `V`/`v` so single-letter model versions ("Deep Seek V four" = V4, "V three" = V3) aren't corrupted.
- **Rule**: Expand legal versus abbreviations (`v.`/`vs.`/`vs`) to the spoken word — but never a bare single-letter `V`/`v`, which collides with single-letter model versions (L-004). Match the period form or the two-letter "vs" form only.
- **Related**: L-004 (single-letter model names like K2/V3 — what this must NOT break)
- **CLAUDE.md ref**: "Pattern substitutions to apply in `_tts.txt`" → item 8
