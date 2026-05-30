# To Fix — Just Predicting Words

## DONE — rendered + live in the current m4b (2026-05-28)

All known text-detectable TTS errors are fixed, re-rendered, and in
`audio_v2/just_predicting_words.m4b` (29 markers, 8.92h, cover embedded):

- **Dedication** — "Dedication" was said twice → now once (L-025)
- **Author's Note** — opened with "...Final Locked Version" cruft → now "A Note on How This Book Was Made" (L-025)
- **About the Author** — opened with "Author Bio Final Locked Version" → now "About the Author" (L-025)
- **Ch 1** — "What'S Coming" stray capital S → "What's Coming" (L-024)
- **Ch 5** — "Openai" → "Open AI" (L-026)
- **Ch 10** — "Wraps Openai" → "Wraps Open AI" (L-026)
- **Ch 12** — fake court cases "v." → "versus" (6 names) (L-027)
- **Ch 19** — "Complement Vs Substitute" → "Complement versus Substitute" (L-027)
- **Appendix A** (glossary) — "Chatgpt" → "Chat GPT" (L-026)
- **Appendix B** (timeline) — "Chatgpt" → "Chat GPT" (L-026)
- **Chapter markers** renamed to "Chapter N: Title"

## 2026-05-29 — fact corrections synced to raw; PENDING GPU re-render

Triple-check found the print (InDesign) had the fact corrections but the
**raw source did not** — audio had drifted behind print. Now fixed:

- 11 corrections (CORRECTIONS.md Part 1) applied to `source/raw/`:
  ch1 + ch2 (fastest-growing "in history" hedge), ch2 (Amazon $25B),
  ch5 ×3 (Musk lawsuit resolved, not ongoing), ch6 (seven not twelve
  researchers; Pentagon dispute reason; 80× growth), ch8 (Scale AI
  $14.3B), ch12 (Schwartz "early 2023").
- `_tts.txt` + `_clean.txt` regenerated for those 6 chapters (0 flags).
- `prep` re-hashed; **11 stale sections** flagged, pending GPU render:
  - ch1: intro
  - ch2: the_night_the_world_noticed, the_explosion
  - ch5: intro, the_founding_idea, the_present_tension
  - ch6: the_claude_code_moment, the_valuation_race
  - ch8: the_superintelligence_labs_pivot
  - ch12: intro
- Verified by grep: every OLD phrase absent from `_tts`, every NEW phrase
  present. Print + audio text now match.
- Appendix B: NO audio change needed (raw already line-breaks timeline
  entries; Llama 4 sentence already correct in raw). The colon fix was
  print-only.

**Still to do (GPU + ear):** render the 6 stems → rebuild m4b →
re-embed cover (commands below). ch5/ch6 grew, so manifest durations
change and ALL downstream chapter markers shift — `build_m4b.py` reads
the regenerated `_manifest.json`, so rebuild after rendering, don't reuse
old offsets. joe-cto go/no-go: **listen to the re-rendered ch5 + ch6
sections** before calling it done.

**Guardrail (joe-cto):** a correction is not "done" until BOTH surfaces
pass the same grep — export the InDesign story text to a throwaway .txt
and grep it with the same script that greps `_clean.txt`. Every REPLACE
present + every OLD string absent, on both. This is what would have caught
the print/raw drift.

### Print-side proofread (InDesign, applied by author 2026-05-29)
- ch6 stray subtitle (duplicate Google bridge line) — deleted
- 3 section headings styled as body text (ch10 xAI; ch15 risks 1 & 4) — restored
- ch2 Firth quote backwards opening curly quote — fixed
- 3 double-spaces (ch5 ×2, ch6 ×1) — collapsed
- Appendix B timeline — colon after each entry title (print-only)

## Open — awaiting author listen-through
- [ ] Author listen-through of the rebuilt m4b — verify the spots above, and
      flag any **mispronounced names** or other spoken errors NOT detectable by
      grep (note chapter + word). Those need a pronunciation override + another
      batched re-render.
- [ ] (Optional, low priority) ch21 label "Chapter Twenty-One" lacks the
      trailing "..." title-pause cue — `CHAPTER_LABEL` regex in
      `tts_normalize.py` / `render_sections.py` doesn't match hyphenated
      ordinals. Fix = allow `-[A-Z][a-z]+`. Cosmetic; intro still reads.

## Re-render reference (for the next batch, if more issues surface)
```
# render only changed stems (NEVER bare `render` — picks up non-narrated design docs, L-020)
python C:/AI/books/render_sections.py render just_predicting_words <stem>
python build_m4b.py
# re-embed cover (cover_std.jpg already in audio_v2/)
ffmpeg -y -i audio_v2/just_predicting_words.m4b -i audio_v2/cover_std.jpg \
  -map 0:a -map 1:0 -c:a copy -c:v copy -disposition:v:0 attached_pic \
  -map_chapters 0 audio_v2/_f.m4b && mv -f audio_v2/_f.m4b audio_v2/just_predicting_words.m4b
```
GPU note: a CUDA "unknown error" can wedge ComfyUI and starve VRAM, which
makes Chatterbox OOM (500 on /tts). If renders fail with OOM, check
`nvidia-smi` + restart the stack (`START_ALL.bat`).
