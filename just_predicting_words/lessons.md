# Lessons — Just Predicting Words (production journal)

The discovery log for this book's audiobook production. Same schema and IDs
as the cross-book `C:/AI/books/LESSONS_INDEX.md`. Where the index is brief
and rule-focused, this file preserves the full diagnostic narrative for
future reference (and as a cautionary tale for the next book on the same
pipeline).

See `C:/AI/books/CLAUDE.md` → "Logging discoveries" for the system overview.

---

## Index

| ID | Title | Status | Date |
|----|-------|--------|------|
| L-001 | Years read inconsistently as digit strings | active | 2026-05-22 |
| L-002 | CamelCase brand names mispronounced as run-together gibberish | active | 2026-05-23 |
| L-003 | Dot-spelled acronyms cause letter stutter on burton voice | active | 2026-05-24 |
| L-004 | Number-suffixed model names need word-form numbers | active | 2026-05-23 |
| L-005 | ALL-CAPS section headings detected reliably from raw, not _clean.txt | active | 2026-05-23 |
| L-006 | Standalone "..." pause lines produce phantom letter sounds | active | 2026-05-23 |
| L-007 | Italic epigraphs read as extra title sentences in audio | active | 2026-05-23 |
| L-008 | METADATA_LINE prefix-only patterns false-match body sentences | active | 2026-05-23 |
| L-009 | silence_cap stop_duration=1.5s too loose for dramatic short sentences | active | 2026-05-25 |
| L-010 | Author's dramatic short sentences are intentional prose, fix at audio level | active | 2026-05-25 |
| L-011 | Embedded ALL-CAPS brand mentions need Title-casing mid-sentence | active | 2026-05-23 |
| L-012 | Glossary cross-references in ALL-CAPS need Title-casing too | active | 2026-05-23 |
| L-013 | Section heading detection needs lowercase tolerance for CamelCase brand prefixes | active | 2026-05-23 |
| L-014 | Section-by-section rendering gives 5-min iteration vs 25-min per chapter | active | 2026-05-25 |
| L-015 | M4B cover embed — strip alpha + explicitly map chapters | active | 2026-05-26 |
| L-016 | "Chapter" vs "navigation marker" — be precise about which count is meant | active | 2026-05-26 |
| L-017 | Three-layer lessons system: rules / index / per-book journal | active | 2026-05-26 |
| L-018 | ffmpeg concat demuxer resolves paths relative to the list file, not cwd | active | 2026-05-26 |
| L-019 | Windows cp1252 console crashes on Unicode arrows in Python print() | active | 2026-05-26 |
| L-020 | Narrated-files allowlist required, not *.txt glob | active | 2026-05-26 |
| L-021 | `render_sections.py all` defers assembly until ALL sections render — manually assemble mid-batch for progressive listening | active | 2026-05-26 |
| L-022 | Validate the full TTS recipe on one chapter before committing full-book GPU time | active | 2026-05-26 |
| L-023 | CB synthesis is opaque mid-render — log silence is normal, not stuck | active | 2026-05-26 |
| L-024 | Possessive 'S in ALL-CAPS headings title-cased into a standalone capital letter | active | 2026-05-28 |
| L-025 | ALL-CAPS banner between dividers is a file/editorial label, not always the spoken heading | active | 2026-05-28 |
| L-026 | Brands in ALL-CAPS headings get capitalized to gibberish ("OPENAI" -> "Openai") | active | 2026-05-28 |
| L-027 | Legal "v." citation read as "via"/"vee" instead of "versus" | active | 2026-05-28 |

---

## Lessons

### L-001: Years read inconsistently as digit strings
- **Date**: 2026-05-22
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: Listener flagged ch 7 first. CB read "2025" as "two zero twenty five" mid-paragraph, while reading the same `2025` correctly elsewhere in the same chapter. Author said: "this does not progress, there is a fucking letter E by itself" — well, that was a different bug (L-006), but the year bug was real too: "the chatterbox are ok, but there are some stupid mistakes, really stupid, like in chapter 7 or 8 chatterbox read teh date 2-0-25 two zero twenty five, while it was doing great before."
- **Diagnosis**: CB's chunker splits at ~240 chars. Internal year-to-speech heuristic flips based on chunk position + the model's state at chunk-boundary entry. Same seed, same reference voice, same source file — different chunks pick different readings.
- **Fix**: `tts_normalize.py` `fix_years()` substitutes digit-form years with their spoken form deterministically: 2000-2009 → "two thousand X", 2010-2099 → "twenty XX", 1900-1999 → "nineteen XX". Decade plurals also handled (`fix_decade_plurals`): `2010s` → "twenty tens", `1990s` → "nineteen nineties". Runs as one of the pattern subs after structural parsing.
- **Rule**: Always pre-substitute years with their spoken form in the `_tts.txt`. Don't trust CB to read year-shaped digits consistently.
- **Related**: L-004
- **CLAUDE.md ref**: "Pattern substitutions to apply in `_tts.txt`" → item 6


### L-002: CamelCase brand names mispronounced as run-together gibberish
- **Date**: 2026-05-23
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: `OpenAI`, `ChatGPT`, `DeepMind`, `AlphaFold` all came out as syllable mush. Hardest hit: chapter 7 which mentions these brands dozens of times.
- **Diagnosis**: CB has no internal CamelCase splitter. It treats the whole token as one word and produces phonemes that match nothing.
- **Fix**: `BRAND_FIXES` dict in `tts_normalize.py` enumerates ~25 brand → spaced-form mappings: `OpenAI` → "Open AI", `ChatGPT` → "Chat GPT", `DeepMind` → "Deep Mind", `AlphaFold` → "Alpha Fold", `AlphaGo`, `AlphaZero`, `ByteDance`, `MiniMax`, `WeChat`, `ElevenLabs`, `GitHub`, `PowerPoint`, `SpaceX`, `WhatsApp`, `TikTok`, `EgyptAir`, `HiddenLayer`, `JetBrains`, `LoDuca`, `McKinsey`, `McCarthy`, etc. Applied via `fix_brands()` which sorts dict keys by length descending so longer matches go first (`SpaceXAI` before `SpaceX`).
- **Rule**: Pre-split every CamelCase brand in `_tts.txt`. Maintain explicit dict — don't try to auto-detect via regex (false positives on legitimate proper names like `iPhone`).
- **Related**: L-011, L-013
- **CLAUDE.md ref**: "Pattern substitutions to apply in `_tts.txt`" → item 3


### L-003: Dot-spelled acronyms cause letter stutter on burton voice
- **Date**: 2026-05-24
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: Author's quote: "there is an error where it says google stumbeled on AI I (another I) assistant". CB rendered "consumer AI assistants" as "consumer A I I assistants" — extra trailing "I" inserted between the acronym and the next word.
- **Diagnosis**: We had used dot-spelling (`AI` → "A.I.", `GPT` → "G.P.T.") on the theory that periods would force CB to pause between letters. With burton's voice/seed, the trailing period at the end of `A.I.` caused CB to repeat the final letter at the next chunk boundary. The original normalizer README we inherited had warned about this exact possibility ("test one chapter first"); we didn't.
- **Fix**: Reverted `SPELL_OUT` dict to identity mappings — every acronym maps to itself in bare form (`"AI": "AI"`, `"GPT": "GPT"`). All BRAND_FIXES that contained `A.I.` or `G.P.T.` (e.g. `"OpenAI": "Open A.I."`) also reverted to bare form (`"OpenAI": "Open AI"`). For acronyms where bare form mispronounces specifically, override with phonetic spelling (`"AGI": "ay gee eye"`) — never with periods. SPELL_OUT dict still useful for tracking which all-caps tokens are expected vs. need attention in Round 2 flag detection.
- **Rule**: Never dot-spell acronyms in `_tts.txt`. Bare form is CB-safe; phonetic form is the escape hatch when needed.
- **Related**: L-006
- **CLAUDE.md ref**: "Pattern substitutions to apply in `_tts.txt`" → item 4


### L-004: Number-suffixed model names need word-form numbers
- **Date**: 2026-05-23
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: `GPT-4`, `Gemini 2.5`, `K2.6` (Moonshot Kimi), `V3` (DeepSeek), `AI21` (the company), `WMT24` (competition) all came out with mangled hyphens/numbers.
- **Diagnosis**: CB chunker can't decide if a digit attached to letters is a numeral or a label. Same chunk-boundary inconsistency as years (L-001).
- **Fix**: `fix_model_versions()` runs BEFORE acronym substitution. Patterns: `GPT-N(.M)?` → "GPT N(.M)" spoken; `Gemini N(.M)?` → "Gemini N(.M)"; `Llama N(.M)?`, `Claude N(.M)?`; single-letter+digit names `K2`, `V3`, `T5` → "K two", "V three", "T five"; `AI21` → "AI twenty-one"; `WMT24` → "W M T twenty twenty-four". Order matters: must run before `fix_acronyms` or `GPT-4` becomes `G.P.T.-4` (back when dot-spelling was used) and the regex would miss it.
- **Rule**: Pre-substitute all `Brand-N` or `Brand N.M` patterns into spoken form. Run before acronym handling.
- **Related**: L-001
- **CLAUDE.md ref**: "Pattern substitutions to apply in `_tts.txt`" → item 1


### L-005: ALL-CAPS section headings detected reliably from raw, not _clean.txt
- **Date**: 2026-05-23
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: In `_clean.txt`, section headings were inconsistent: `THE STUMBLE` (2 words) stayed ALL-CAPS; `THE COMPANY BEFORE THE STUMBLE` (5 words) was sentence-cased to `"The company before the stumble."`. Plus embedded "GOOGLE" inside `What GOOGLE believes` got missed.
- **Diagnosis**: `clean_chapter.py:211` only sentence-cases ALL-CAPS headings with `len(stripped.split()) >= 3`. The 2-word floor was intentional to avoid false positives but caught legitimate 2-word headings. Inconsistency cascaded everywhere.
- **Fix**: `tts_normalize.py` reads from `source/raw/*.txt` directly, NOT from `_clean.txt`. In raw, all section headings are reliably ALL-CAPS between `· · ·` dividers. Title-case via `re.sub(r"[A-Za-z]+", repl, line)` over alphabetic tokens — handles punctuation tokens like `(ARTIFICIAL` correctly. Keep tokens already in SPELL_OUT or BRAND_CAPS in their original form.
- **Rule**: For TTS normalization, read RAW chapter sources directly. Don't inherit clean_chapter.py's heuristic decisions about headings.
- **Related**: L-013
- **CLAUDE.md ref**: "Section heading detection"


### L-006: Standalone "..." pause lines produce phantom letter sounds
- **Date**: 2026-05-23
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: Author's exact words: "the chapter 7 started, google the giant that almost lost teh future, E (just and E letter)... investigate, it was never there at alll.. it was introduced in the new fixes. so far 2 errors int eh first 5 seconds, this does not progress, there is a fucking letter E by itself". A stray "E" appeared between the chapter title and the body, on multiple chapters tested.
- **Diagnosis**: I had added standalone `...` lines on their own line between blank lines, intended as longer pause cues. The books CLAUDE.md said "CB honors ellipses for pause cues" — but that turned out to apply to INLINE ellipses (trailing `...` on the end of a sentence), not standalone-line ellipses. CB sees a standalone `...` line and vocalizes it as a letter sound (heard as "E" with the burton voice). Empirically the artifact was reproducible on every chapter with the standalone-line pattern.
- **Fix**: Removed all standalone `...` lines from `tts_normalize.py`'s structural pass. Kept only inline trailing `...` on title/subtitle/heading lines. Blank lines + the trailing inline ellipsis carry the pause cue. Also dropped the dead `teaser_seen` state from the parser since italic teasers are now dropped entirely (L-007), so there's no teaser slot to handle.
- **Rule**: Inline trailing `...` is CB-safe. Standalone `...` lines are NOT. The CLAUDE.md note "CB honors ellipses for pause cues" should be read as "INLINE ellipses." Validate every pause-cue idea empirically on the target voice before applying it book-wide.
- **Related**: L-003
- **CLAUDE.md ref**: "Pause cues — INLINE trailing only, never standalone"


### L-007: Italic epigraphs read as extra title sentences in audio
- **Date**: 2026-05-23
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: Author flagged the chapter 7 epigraph: "another sentence at the title that should not be there." The italic line `*They built the architecture that powers every AI assistant in the world. Then they sat on it.*` was being read as a third title sentence right under the chapter title — sounded like clunky extra title material, not the elegant epigraph it is in print.
- **Diagnosis**: Wholly-italic lines are typographic flourishes — chapter teasers at the opening, "What comes next: ..." callouts at the end. Print uses italic visual register to mark them as different from body. Audio has no such register; they read identically to body prose. Listener-side ambiguity follows.
- **Fix**: `WHOLLY_ITALIC_LINE = re.compile(r"^\*[^*]+\*$")` matches lines where all non-whitespace content is wrapped in a single `*...*` pair (after `collapse_italics` collapses multi-line italics to a single line first). Detected in `parse_and_structure` and dropped entirely. Mid-sentence emphasis (`This was *not* enough`) is unaffected — `re.sub(r"\*([^*]+)\*", r"\1", s)` strips the asterisks but keeps the word.
- **Rule**: Drop wholly-italic lines from audio. Keep mid-sentence italics with asterisks stripped.
- **Related**: L-008
- **CLAUDE.md ref**: "Italic epigraphs / teasers"


### L-008: METADATA_LINE prefix-only patterns false-match body sentences
- **Date**: 2026-05-23
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: Author noticed during ch 7 listen-test: "at the beginning of the chapter, there is a sentence missing, that start within the next eight years." Confirmed — the body sentence "Within the next eight years, all eight of those researchers had left Google" was missing from BOTH `_clean.txt` AND `_tts.txt`. This sentence is the punch-line of the chapter opening — losing it gutted the rhetoric.
- **Diagnosis**: `METADATA_LINE` regex inherited from `clean_chapter.py` listed `"Within the"` as one of the metadata-block markers. Designed to match book-design-doc metadata like "Within the company's voice..." or similar — but as a prefix-only pattern, it false-matched any body sentence starting with those two words. Triggered the metadata-block skip behavior (drop the line + drop following non-blank continuation lines until next blank). Affected v1 audio too — author had been listening to v1 with this sentence missing the whole time without noticing until the v2 listen-test made him pay closer attention.
- **Fix**: Removed `"Within the"` from METADATA_LINE in `tts_normalize.py` (left commented in the code with the date and reason). Audit-grepped all narrated raw files for body sentences starting with the remaining prefix-only patterns (`Approximately`, `Verified with`, `All chapters`, `Per Ziad`) — no other false matches book-wide.
- **Rule**: Avoid prefix-only patterns in METADATA_LINE. Prefer patterns with explicit colons (`Working draft:`, `Voice:`) or ALL-CAPS line patterns (`TITLE PAGE`, `CHAPTER OPENING`) that can't accidentally match body. When adding a new metadata pattern, grep all raw files first to check for false matches.
- **Related**: L-005
- **CLAUDE.md ref**: "Metadata-regex gotcha"


### L-009: silence_cap stop_duration=1.5s too loose for dramatic short sentences
- **Date**: 2026-05-25
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: Author flagged: "in section 3 of the chapter 7 there is a long pause before the last word badly" — referring to the sentence "And by that measure, Google was losing. Badly." CB rendered a noticeable dead-air gap between "losing." and "Badly."
- **Diagnosis**: `voices.py` Burton config had `silence_cap=True` with `stop_silence=0.7` (trim to 0.7s) and `stop_duration=1.5` (only trim silences longer than 1.5s, hardcoded in `silence_cap()` ffmpeg call). CB at the "losing. Badly." period boundary inserts ~1.3s of silence — slipping under the 1.5s threshold, never trimmed. Heard as "long pause." The threshold was too loose for prose with many short emphatic sentences.
- **Fix**: Added `stop_duration: float = 1.5` field to `Voice` dataclass. Updated `silence_cap()` in both `render_sections.py` and `batch_render.py` to accept and apply `voice.stop_duration`. Burton config tightened to `stop_duration=0.9, stop_silence=0.5` — pauses over 0.9s get trimmed to 0.5s. Re-processed existing ch 7 `_raw_pre_silcap/*.wav` files (ffmpeg only, no CB re-synth) — total chapter shrunk from 20:44 to 20:24, about 18 seconds of dead air removed across 7 sections, and the dramatic short sentences now land as beats instead of pauses.
- **Rule**: `silence_cap` is per-voice. Tune `stop_duration` to be SHORTER than the typical chunk-boundary silence CB inserts on punctuation-heavy prose. Test on a chapter with many short emphatic sentences before committing settings to the whole book.
- **Related**: L-010
- **CLAUDE.md ref**: voices.py burton config + "Pre-flight" section


### L-010: Author's dramatic short sentences are intentional prose, fix at audio level
- **Date**: 2026-05-25
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: Once we identified the "losing. Badly." over-pause issue (L-009), the question became whether to fix it at the text level (change to "losing, badly.") or at the audio level (tighten silence_cap). Audit revealed 100+ similar patterns across the book: "People cried. People laughed. People got angry." (ch 1), "Contracts. Emails. Reports. Code. Proposals." (ch 1), "Elon Musk. Sam Altman. Reid Hoffman." (ch 5), "Two months. Ten people." (ch 2), etc.
- **Diagnosis**: This is the author's deliberate rhetorical style. The short emphatic single-word and two-word sentences are intentional beats — exactly the rhythm device that made the book worth audiobook-ing in the first place. Replacing periods with commas across the board would rewrite the book's voice.
- **Fix**: Did NOT touch the text. Tightened `silence_cap` settings (L-009) to handle CB's over-pause behavior at the audio level. Text stays as the author wrote it; audio post-processing trims the bloated CB-inserted silence. Confirmed in re-render of ch 7 — the "losing, badly" line plus all other short-emphatic-sentence patterns in the chapter now sound like prose beats, not dead air, with the author's voice intact.
- **Rule**: When a CB rendering artifact correlates with a stylistic pattern that's intentional in the source, fix at the audio post-processing level (silence_cap, atempo) not the text level. Only edit text when CB's reading is wrong (mispronunciation, missed sentence). Don't edit text for prosody.
- **Related**: L-009
- **CLAUDE.md ref**: "Render granularity" + voices.py notes


### L-011: Embedded ALL-CAPS brand mentions need Title-casing mid-sentence
- **Date**: 2026-05-23
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: After `clean_chapter.py` ran, the section heading `WHAT GOOGLE BELIEVES` became `What GOOGLE believes.` — sentence-cased except "GOOGLE" stayed ALL-CAPS. CB would have read it as "What G-O-O-G-L-E believes."
- **Diagnosis**: `clean_chapter.py`'s sentence-case logic preserved already-ALL-CAPS tokens by default (intent: protect acronyms like "AI"). Brand names in caps got swept along with the preservation rule even though they should be re-cased to their normal form.
- **Fix**: `BRAND_CAPS` dict in `tts_normalize.py` enumerates ALL-CAPS brand forms → mixed-case mappings: `GOOGLE` → "Google", `FACEBOOK` → "Facebook", `AMAZON` → "Amazon", `MICROSOFT` → "Microsoft", `APPLE` → "Apple", `META` → "Meta", `NETFLIX`, `TESLA`, `NVIDIA`, `ANTHROPIC`, `OPENAI` → "Open AI", `CHATGPT` → "Chat GPT", `DEEPMIND` → "Deep Mind", `ERNIE` → "Ernie" (Baidu's model). Applied via `fix_embedded_brand_caps()`.
- **Rule**: When a known brand appears in ALL-CAPS inside a normal sentence, re-case to its standard mixed-case form. Acronyms (in SPELL_OUT) are excluded — they stay as written.
- **Related**: L-002
- **CLAUDE.md ref**: "Pattern substitutions to apply in `_tts.txt`" → item 2


### L-012: Glossary cross-references in ALL-CAPS need Title-casing too
- **Date**: 2026-05-23
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: In appendix A (the glossary), entries cross-reference other terms in ALL-CAPS: "See EMBEDDING. A list of numbers that represents the meaning of a word." `EMBEDDING` stayed in caps inside the body prose, would have been spelled out letter-by-letter by CB.
- **Diagnosis**: Same root cause as L-011 (Title-casing embedded all-caps), different surface — these aren't brands but glossary cross-references. Standalone `EMBEDDING` on its own line (the glossary entry header) WAS detected as a section heading and Title-cased correctly. The body mid-sentence reference wasn't.
- **Fix**: `fix_embedded_all_caps()` runs after BRAND_CAPS and SPELL_OUT substitution. Title-cases any 4+ char ALL-CAPS word remaining in body text that isn't already in either dict. Threshold of 4+ chars avoids touching short real acronyms.
- **Rule**: After dict-based brand and acronym substitution, sweep remaining embedded ALL-CAPS tokens (4+ chars, not in any dict) and Title-case them. Catches glossary refs and any missed proper nouns without false-positiving on USA/NATO/etc.
- **Related**: L-011
- **CLAUDE.md ref**: "Pattern substitutions to apply in `_tts.txt`" → item 5


### L-013: Section heading detection needs lowercase tolerance for CamelCase brand prefixes
- **Date**: 2026-05-23
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: In ch 10, the section heading `xAI, THE LAB THAT BECAME A SPACE COMPANY` wasn't detected as a section heading. Result: it rendered as in-line body prose, the section didn't get its trailing-ellipsis pause cue, and listeners would hear a long sentence with no section transition.
- **Diagnosis**: `is_section_heading()` used a strict `^[A-Z]` regex requiring the line start with an uppercase letter. The CamelCase brand `xAI` starts with lowercase `x`, disqualifying the entire otherwise-all-caps heading.
- **Fix**: Replaced strict regex with a percentage rule. Line is a section heading if: ≥80% of letters uppercase AND ≤20 words AND ≥3 letters total AND contains at least one run of 2+ uppercase letters (rules out single CamelCase words like `iPhone` alone). The 80% threshold tolerates 1-2 CamelCase brand tokens (xAI, iPhone, openAI) anywhere in the line.
- **Rule**: Don't use strict `^[A-Z]` for heading detection. Use a percentage-of-uppercase rule that tolerates CamelCase brand tokens at any position in the heading.
- **Related**: L-005
- **CLAUDE.md ref**: "Section heading detection"


### L-014: Section-by-section rendering gives 5-min iteration vs 25-min per chapter
- **Date**: 2026-05-25
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: During the ch 7 listen-and-iterate cycle, each text fix (years substitution, then italic teaser drop, then "Within the" bug fix, then "AI" period removal, then silence_cap tighten) required a full 23-25 min CB chapter re-render to validate. With 28 chapters and 2-3 expected iterations each, total iteration cost was 10-20 hours of GPU time — and would have been worse if each chapter had different per-chapter issues.
- **Diagnosis**: A whole-chapter CB call has no granularity. Fixing one bad moment means redoing the whole 23 minutes. The iteration cost scales linearly with chapter length, not with the size of the fix.
- **Fix**: Built `C:/AI/books/render_sections.py`. Splits each `_tts.txt` on the trailing-ellipsis heading markers from `tts_normalize.py`'s structural pass (chapter label + chapter title + each ALL-CAPS section heading = section boundary). Renders each section as a separate WAV (~3-5 min). Concatenates via ffmpeg concat demuxer into the chapter MP3. Per-chapter `sections/<chapter>/_manifest.json` tracks SHA-1 hash of each section's text — edit a section in `_tts.txt`, run `python render_sections.py section <book> <chapter> <slug>` and only that section re-renders, then the chapter re-assembles. Each chapter also gets `audio_v2/listening/<chapter>.md` with timestamp → section name navigation, so listener can identify which section a flagged moment lives in.
- **Rule**: For any audiobook over ~3 chapters or any expected iteration cycle, render section-by-section. Concat to chapter MP3 at the end. Per-section manifests + SHA hashing make stale-section detection automatic.
- **Related**: L-009, L-010
- **CLAUDE.md ref**: "Render granularity: section-by-section"


### L-015: M4B cover embed — strip alpha + explicitly map chapters
- **Date**: 2026-05-26
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: First attempt to embed the author-provided cover JPG (3000×3000) into the M4B failed with ffmpeg error `Tag text incompatible with output codec id '98314'`. The cover-art recipe I'd written into CLAUDE.md earlier — `ffmpeg -i input.m4b -i cover.jpg -map 0 -map 1 -c copy -disposition:v:0 attached_pic out.m4b` — didn't work.
- **Diagnosis**: Two distinct issues stacked. (a) The cover JPG had alpha channel — `ffprobe` showed pixel format `yuva444p`. The MP4/ipod muxer doesn't accept alpha-bearing input streams. (b) `-map 0` includes ALL streams from the input M4B, including the binary chapter-text stream that stores chapter markers. The ipod output muxer doesn't recognize that text stream codec and rejects the output.
- **Fix**: Two-step process. Step 1: `ffmpeg -y -i cover_with_alpha.jpg -pix_fmt yuvj420p -q:v 2 cover_std.jpg` — strips alpha to standard JPEG pixel format. Step 2: `ffmpeg -y -i input.m4b -i cover_std.jpg -map 0:a -map 1:0 -c:a copy -c:v copy -disposition:v:0 attached_pic -map_chapters 0 output.m4b` — maps only the audio stream from the input M4B (drops the binary chapter stream), maps the cover image, copies both streams (no re-encode), tags the cover with `attached_pic` disposition (so players show it as cover art, not as a video track), and explicitly re-embeds chapter markers via `-map_chapters 0`. Verified: output M4B has audio + 29 chapter markers + mjpeg cover at 3000×3000 with `DISPOSITION:attached_pic=1`.
- **Rule**: When embedding cover art into an existing M4B, never use `-map 0` blanket — explicitly select `-map 0:a` and re-embed chapters via `-map_chapters 0`. Always normalize the cover to RGB pixel format first (`-pix_fmt yuvj420p`).
- **Related**: none
- **CLAUDE.md ref**: "Cover art" section under "Build M4B"


### L-016: "Chapter" vs "navigation marker" — be precise about which count is meant
- **Date**: 2026-05-26
- **Book**: just_predicting_words
- **Status**: active
- **Symptom**: I described the M4B as having "29 chapter markers." Author flagged: "the book is 21 chapters dude."
- **Diagnosis**: The M4B's 29 navigation markers include not just chapters but also front matter (opening credits, dedication, author's note), appendices (A glossary, B, C), about-the-author, and closing. `3 + 21 + 3 + 1 + 1 = 29` markers ≠ 29 chapters. Calling all of them "chapters" conflates production-pipeline file count with the book's narrative chapter count.
- **Fix**: In CLAUDE.md and ongoing communication, use "navigation markers" or "track markers" for M4B jump points. Reserve "chapters" for actual book chapters (21 in JPW). Updated Status section in CLAUDE.md to make the distinction explicit with the `3 + 21 + 3 + 1 + 1` breakdown.
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
- **Status**: active — FIXED & verified 2026-05-28; `00_author_note_FINAL` + `01_chapter_01` re-rendered and m4b rebuilt (Author's Note track 82.3s→76.8s).
- **Symptom**: Author listen-test of the finished m4b: the "Author's Note" track opens "Author ... [~3 second gap] ... S Note on AI Use, Final Locked Version" — a dead pause after "Author", then the rest of the label runs together. Author's words: "in author notes, it is said Author... 3s notes and than he runs with the other words."
- **Diagnosis**: `tts_normalize.py` `title_case_heading()` title-cases a heading line via `re.sub(r"[A-Za-z]+", repl, s)`. The apostrophe is not in the `[A-Za-z]` class, so a possessive like `AUTHOR'S` is split into TWO separate tokens: `AUTHOR` and `S`. `AUTHOR` → "Author"; the lone `S` is length 1, so it fails the `if len(word) >= 2` capitalize guard and is returned UNCHANGED — staying a capital "S". Result in `_tts.txt`: `Author'S Note On AI Use - Final Locked Version...`. CB reads a standalone capital letter after an apostrophe as a spelled-out letter and inserts a chunk-boundary pause around it. Same trap fires in `01_chapter_01_tts.txt:143` — the section heading `WHAT'S COMING` became `What'S Coming...`.
- **Fix (recommended, NOT yet applied)**: Make the title-case regex treat the possessive tail as part of the same token, then let `str.capitalize()` lowercase it: change `re.sub(r"[A-Za-z]+", repl, s)` to `re.sub(r"[A-Za-z]+(?:'[A-Za-z]+)?", repl, s)`. Python's `"AUTHOR'S".capitalize()` → `"Author's"` and `"WHAT'S".capitalize()` → `"What's"`, which is exactly right. After the code fix, re-normalize, re-render the `00_author_note_FINAL` and `01_chapter_01` sections (CB re-synth — text changed), and rebuild the m4b.
- **Rule**: Heading title-casing must treat possessive `'S`/`'s` as part of the word, never as a standalone token. A lone capital letter anywhere in `_tts.txt` is a CB letter-spell trap (same failure family as dot-spelled acronyms, L-003). When title-casing by alphabetic-token regex, include the apostrophe tail: `[A-Za-z]+(?:'[A-Za-z]+)?`.
- **Related**: L-005, L-013 (heading detection / title-casing), L-003 (standalone-letter CB artifact)
- **CLAUDE.md ref**: "Section heading detection"


### L-025: ALL-CAPS banner between dividers is a file/editorial label, not always the spoken heading
- **Date**: 2026-05-28
- **Book**: just_predicting_words
- **Status**: active — FIXED & verified 2026-05-28; `00_dedication` / `00_author_note_FINAL` / `00_author_bio_FINAL` re-rendered and m4b rebuilt (Dedication 13.8s→11.8s, About-the-Author 51.5s→46.5s).
- **Symptom**: Author listen-test of the finished m4b: the Dedication track says the word "Dedication" twice in a row ("we have audio issue in the dedication, the word is said twice"). Separately, the Author's Note and About-the-Author tracks open by narrating editorial cruft — "...On AI Use, Final Locked Version" and "Author Bio, Final Locked Version" — instead of their real titles.
- **Diagnosis**: Raw source files wrap an ALL-CAPS banner between `====` dividers as the file's editorial label: `DEDICATION`, `AUTHOR'S NOTE ON AI USE - FINAL LOCKED VERSION`, `AUTHOR BIO - FINAL LOCKED VERSION`. `is_section_heading()` matches that banner and `parse_and_structure()` emits it as the spoken section heading (with a trailing `...`). For body chapters this is CORRECT — the banner equals the chapter title. For front-matter/wrapper files it is WRONG on two counts: (a) `DEDICATION` Title-cases to "Dedication" and is emitted as the heading, but the file's FINAL TEXT body ALSO starts with the literal line "Dedication." — so the word is narrated twice (no dedup exists between the emitted heading and the first body line); (b) the `... - FINAL LOCKED VERSION` banners are file-management cruft that should never be spoken, and they bury the real titles, which live in the body ("A Note on How This Book Was Made", "About the Author"). The editorial suffix is never stripped. Blast radius in JPW: `00_dedication` (double word), `00_author_note_FINAL` (cruft heading + L-024 possessive), `00_author_bio_FINAL` (cruft heading). Clean banners like `OPENING CREDITS` / `CLOSING CREDITS` read fine, so a blanket "drop all banners" would be wrong.
- **Fix (recommended, NOT yet applied)**: Two parts. (1) For non-chapter/wrapper files, prefer an EXPLICIT spoken title rather than the raw banner — `build_m4b.py` already maintains a `TITLES` dict (e.g. `00_author_note_FINAL` → "Author's Note", `00_author_bio_FINAL` → "About the Author", `00_dedication` → "Dedication"); reuse it as the heading source for front matter. Failing that, strip editorial suffixes (`- FINAL LOCKED VERSION`, `- FINAL`, `LOCKED`, `VERSION`, descriptor tails like `ON AI USE`) from banner headings. (2) Add a heading↔first-body dedup: if the emitted heading text equals the next non-blank body line case-insensitively (Dedication... / Dedication.), drop one. Re-render `00_dedication`, `00_author_note_FINAL`, `00_author_bio_FINAL`, rebuild the m4b.
- **Rule**: The ALL-CAPS banner between `====` dividers is the file's editorial label. For chapters it equals the title (narrate it). For front-matter/wrapper files it is a descriptor that may duplicate the body or carry version cruft — never narrate it blindly. Prefer an explicit per-file spoken title (the `build_m4b.py` `TITLES` dict is the source of truth), strip "FINAL / LOCKED / VERSION" editorial suffixes, and dedup the heading against the first body line.
- **Related**: L-008 (dropping non-prose / metadata false-match), L-020 (front-matter files need explicit handling, not globbing), L-016 (wrapper tracks are not chapters)
- **CLAUDE.md ref**: "Section heading detection"


### L-026: Brands in ALL-CAPS headings get capitalized to gibberish ("OPENAI" -> "Openai")
- **Date**: 2026-05-28
- **Book**: just_predicting_words
- **Status**: active — FIXED & shipped 2026-05-28; ch5 / ch10 / appendix A / appendix B re-rendered and m4b rebuilt (after a GPU detour — ComfyUI's wedged CUDA context had starved VRAM; resolved by a stack restart).
- **Symptom**: Author listen-test of the m4b: section/chapter titles mispronounced brands. "Microsoft, The Company That Wraps Openai" (ch10) read "oh-pe-nai" instead of "Open A-I"; the glossary (appendix A) and timeline (appendix B) read "Chatgpt" instead of "Chat GPT". Author: "several errors in the titles of chapters, similar to the author's notes."
- **Diagnosis**: `title_case_heading()` capitalizes every ALL-CAPS token not in its keep-set (SPELL_OUT acronyms + "I"). A brand like `OPENAI`/`CHATGPT` in an ALL-CAPS source heading becomes "Openai"/"Chatgpt" via `str.capitalize()`. No later pass repairs it: `fix_brands` only matches mixed-case CamelCase keys (`OpenAI`), and although `fix_embedded_brand_caps`'s `BRAND_CAPS` dict *did* contain `OPENAI`/`CHATGPT`, the token had already been mangled to mixed-case "Openai" by title_case_heading (Round 3) BEFORE the Round 1 brand subs ran — so the `\bOPENAI\b` regex no longer matched. Same root family as L-024.
- **Fix**: Built `BRAND_CAPS_ALL = {k.upper(): v for k,v in BRAND_FIXES.items()}` merged with `BRAND_CAPS` (explicit entries win on overlap). (1) Added its keys to `title_case_heading`'s keep-set so a brand SURVIVES title-casing in its ALL-CAPS form. (2) `fix_embedded_brand_caps` now iterates `BRAND_CAPS_ALL` so the preserved ALL-CAPS brand converts (`OPENAI` → "Open AI", `CHATGPT` → "Chat GPT") everywhere, headings included. Text verified: ch5/ch10 now read "Open AI", appendix A/B read "Chat GPT". Re-render of those sections + m4b rebuild batched in TO_FIX.md.
- **Rule**: Heading title-casing must PRESERVE known brands (never `capitalize()` them); a downstream brand pass converts them. Maintain ONE combined ALL-CAPS brand map shared by both the heading keep-set and the embedded-brand-caps sub. A brand mangled to mixed-case ("Openai") is invisible to every later brand regex.
- **Related**: L-002 (CamelCase brands), L-011 (embedded ALL-CAPS brands), L-024 (sibling title_case_heading bug)
- **CLAUDE.md ref**: "Section heading detection"


### L-027: Legal "v." citation read as "via"/"vee" instead of "versus"
- **Date**: 2026-05-28
- **Book**: just_predicting_words
- **Status**: active — FIXED & shipped 2026-05-28; ch12 / ch19 re-rendered and m4b rebuilt.
- **Symptom**: Author: "in chapter 10 or 11 [actually ch12], where we are talking X v Y for the court cases, the v sometimes is sounding like a via." The fake-case names in the hallucination story — "Varghese v. China Southern Airlines", "Shaboon v. Egypt Air", etc. — plus the ch19 heading "Complement Vs Substitute" had the abbreviation read literally instead of as "versus".
- **Diagnosis**: CB reads the bare legal abbreviation `v.` / `Vs` as the letter / "via", not the word "versus". No normalization existed for it.
- **Fix**: `fix_legal_versus()` substitutes space-bounded `v.` / `vs.` / `vs` → "versus". Critically it does NOT touch a bare single `V`/`v`, because that would corrupt single-letter model names like "Deep Seek V four" (V4) and "V three" (V3) which legitimately contain a standalone capital V. Wired into `normalize()` after `fix_years`, before `fix_punctuation_collisions` (so the removed period doesn't trip the pause-hint pass).
- **Rule**: Expand legal "versus" abbreviations (`v.` / `vs.` / `vs`) to the spoken word — but never a bare single-letter `V`/`v`, which collides with single-letter model versions (DeepSeek V3/V4, L-004). Match the period form or the two-letter "vs" form only.
- **Related**: L-004 (single-letter model names like K2/V3 — what this must NOT break)
- **CLAUDE.md ref**: "Pattern substitutions to apply in `_tts.txt`" → item 8
