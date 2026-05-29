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
