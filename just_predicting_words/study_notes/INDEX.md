# Study Notes — Just Predicting Words

A chapter-by-chapter, audio-narratable knowledge extract of the book, designed for replay and memorization. No Q/A, no sleep-loop repetition — comprehensive declarative prose, organized by section within each chapter.

---

## Version log

| Version | Date | Status | What changed |
|---------|------|--------|--------------|
| **v1** | 2026-05-30 | **active** | Initial extraction from the May 2026 book text + applied corrections (Musk-lawsuit dismissed, seven not twelve Anthropic researchers, $14.3B Scale AI, fastest-growing-"in-history" hedge, Amazon $25B, Pentagon dispute, Schwartz "early 2023"). |
| v2 | — | planned | Triggered by: a new frontier model release (Llama 5, GPT-6, DeepSeek V5, etc.), a major leadership change (CEO, founder), a regulatory milestone (EU AI Act full enforcement, US federal AI law), a major event (lawsuit, acquisition, IPO). |
| v3 | — | planned | Next major refresh. |

## File map

24 files. ~28,000 words total → ~3 hours of audio at Burton's narration pace.

### Part 1 — How the technology works
- `ch01_just_predicting_words.md` — The ChatGPT launch, the next-word-prediction trick, book preview.
- `ch02_short_history_of_machines_that_read.md` — Distributional semantics, word2vec, Transformer paper, the GPT line, the post-ChatGPT scramble.
- `ch03_inside_the_machine.md` — Tokens, embeddings, attention, the Transformer architecture, parameters, context windows.
- `ch04_taming_the_wild_word_predictor.md` — Instruction tuning, RLHF, Constitutional AI, system prompts, the helpful-honest-harmless triad.

### Part 2 — The companies
- `ch05_openai_the_company_that_started_the_wave.md` — OpenAI founding, Musk lawsuit (dismissed May 2026), board crisis, Microsoft partnership, IPO horizon.
- `ch06_anthropic_the_company_that_broke_off_over_safety.md` — Founded by seven, Claude Code revenue jump, Pentagon dispute, $40B Google / $25B Amazon, ~$900B valuation.
- `ch07_google_the_giant_that_almost_lost_the_future.md` — Brain + DeepMind merged, Hassabis Nobel 2024, Bard-to-Gemini, distribution as advantage.
- `ch08_meta_the_open_bet_that_changed_everything.md` — Open-weight Llama era, Llama 4 disaster, Superintelligence Labs (Scale AI / Alexandr Wang), LeCun departure, Muse Spark pivot to closed weights.
- `ch09_the_other_half_of_the_map.md` — China: DeepSeek moment, Qwen, Kimi, GLM, ByteDance, Tencent; efficiency-from-constraints; Huawei Ascend; censorship reality.
- `ch10_everyone_else.md` — Microsoft (wraps OpenAI, MAI hedge), xAI/SpaceX, Mistral (Europe), Perplexity, Amazon (Bedrock), Apple (late and privacy-focused), Cohere, Hugging Face, others.

### Part 3 — Capabilities and limits
- `ch11_what_these_machines_are_genuinely_good_at.md` — Seven uses: writing you steer, translation, document analysis, code (with the McKinsey/DX/METR numbers), thinking partner, teaching, structured extraction.
- `ch12_how_these_machines_fail.md` — The Schwartz case in full, the five failure modes (hallucination, sycophancy, rationalization, stale world, refusal), six habits for using AI without becoming a casualty.
- `ch13_the_limits_of_language.md` — Four structural limits no engineering will fix: qualia, tacit knowledge, the cultural unsaid, embodied experience.

### Part 4 — Risks and rules
- `ch14_the_risks_that_are_real.md` — Synthetic media, bias at scale, job displacement, privacy erosion — with the WEF/Bengio/Challenger/Goldman/Lisa Simon numbers.
- `ch15_the_risks_that_are_mostly_hype.md` — The author's opinion chapter: consciousness/Terminator, total job destruction, brain-rot, permanent power concentration.
- `ch16_guardrails_how_companies_try_to_keep_models_in_line.md` — The seven defensive layers and where they fail (HiddenLayer, Princeton 100-example degradation, 80–99% jailbreak rates).
- `ch17_regulation_what_governments_are_doing.md` — EU AI Act, US patchwork, China's framework, UK/Japan/Canada/Korea/Vietnam; the four questions regulators are wrestling with.

### Part 5 — Practice
- `ch18_how_to_use_them_well.md` — Seven rules, plus the practical habits of high-quality users.
- `ch19_how_to_handle_ai_at_work.md` — Six framings (tasks not jobs, complement vs substitute, judgment, relationships, early-career problem, official vs real policy) plus scenarios.
- `ch20_how_to_talk_to_your_kids_about_them.md` — Seven principles (age, foundational skills, questioning, AI is not a friend, education changing, talk about the future honestly, mental health signals).

### Part 6 — Forecast
- `ch21_where_this_is_all_going.md` — Three trajectories, what's confident, four determining questions, what to do given uncertainty.

### Appendices
- `appA_glossary_distilled.md` — The terms in compact form.
- `appB_timeline_distilled.md` — The dates in compact form.
- `appC_further_reading_distilled.md` — Books, essays, sources organized by topic.

## How versioning works

Each chapter file carries a version block at the top: `**Version:** v1 · **Last updated:** YYYY-MM-DD`. When the field changes:

- **Small update** (a number, a date, a name): edit the line in place, bump the version block at the top to `v2 (YYYY-MM-DD)` and add a one-line CHANGELOG entry at the bottom describing what changed.
- **Larger update** (whole new event, dropped passage, restructured section): replace the affected section, bump the version, append a CHANGELOG.
- **New chapter** (an event significant enough to need its own narrative — a major lab spin-off, a new region entering the frontier): create a new file (e.g. `ch22_*.md`) with its own version block.
- **MASTER LOG:** update the version log table in this INDEX.md so the diff between v1 and v2 is one row.

## How the audio gets made

The render pipeline mirrors the book's:

1. **Assemble.** Run `build_study_audio.py` (next to this INDEX). It reads each chapter file in order, strips the markdown shell, converts section headers and bullet lists into prose, and writes a single plain-text file to `audio_src/study_v1_raw.txt`.
2. **Normalize.** Run the same `tts_normalize.py` driver that powers the book on the assembled raw file. Produces `audio_src/study_v1_tts.txt` — numbers spelled out, brand names re-cased, etc.
3. **Render.** Send the `_tts.txt` to Chatterbox via the existing pipeline (either as a single-stem render, or split into per-chapter stems with section markers for m4b navigation — depends on how you want to listen).
4. **Package.** Either a single long .mp3/.m4a for replay, or an .m4b with chapter markers for jump-by-topic navigation.

For v2/v3 audio: only the chapters that changed need re-rendering; the rest of the audio is reused.
