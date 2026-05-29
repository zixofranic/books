# Content Review — Chapter 21, Appendices A/B/C, Author's Note

Scope: final-pass content review of the five cleaned files listed below, evaluated for narration on Chatterbox burton voice. May 2026.

## BLOCKERS

- `22_appendix_A_clean.txt` line 13 `AGI (ARTIFICIAL general intelligence).` — sentence-casing artifact: only the first word of the parenthetical was capitalized, leaving "ARTIFICIAL" shouting. CB will read this as caps-emphasis on one word only. Same defect at line 90 `GPT (GENERATIVE pre-trained transformer).` and line 154 `Rag (RETRIEVAL-AUGMENTED generation).` and line 166 `Reinforcement learning from human feedback (RLHF).`. Fix: drop the all-caps from the first parenthetical word in each — `AGI (artificial general intelligence).`, `GPT (generative pre-trained transformer).`, `RAG (retrieval-augmented generation).` (and capitalize the term itself: `RAG` not `Rag`), `Reinforcement learning from human feedback (RLHF).` is fine but the headword line above it should match the casing convention used by neighboring entries.
- `23_appendix_B_clean.txt` lines 99-105 — chronology is out of order: "2025 - Anthropic Catches Up" (full year) is placed BEFORE "2025, April - Llama 4 Disaster" and "2025, November - LeCun Leaves Meta". Reorder so April → May → November → year-spanning entry, or move the year-spanning summary entry to the end of the 2025 block.

---

## 21_chapter_21_clean.txt

- Line 99 `Appendices follow: glossary, model timeline, further reading.` — the appendix B file is titled "a timeline at a glance," not "model timeline." Minor mismatch. Fix: `Appendices follow: glossary, timeline, further reading.`
- Line 41 `the more speculative ones, may or may not arrive on the timelines their advocates predict.` — sentence reads as referring to risks from "chapter fifteen" but the antecedent is far back; reads cleanly aloud. No fix required, just flag.
- Pronunciation watchpoints: "AGI" (ay-jee-eye, CB usually fine), "AI-fluent" / "AI-illiterate" (hyphenation may cause CB to stutter — listen on first render).
- No other findings.

---

## 22_appendix_A_clean.txt

- Line 1 `Appendix a. glossary of terms.` — sentence-cased "Appendix a." reads as "appendix ay" which is correct, but inconsistent with chapter style elsewhere (`Chapter Twenty-One`). Consider `Appendix A. Glossary of terms.` for narration consistency. Low priority.
- Line 13 `AGI (ARTIFICIAL general intelligence).` — see BLOCKERS.
- Line 90 `GPT (GENERATIVE pre-trained transformer).` — see BLOCKERS.
- Line 113 `Large language model (LLM).` — entry headword is sentence-cased while every other headword is ALL CAPS (e.g. `ATTENTION`, `BIAS`, `CHATGPT`). Inconsistent. Fix: `LLM (large language model).` to match neighbors, or accept the inconsistency as intentional.
- Line 154 `Rag (RETRIEVAL-AUGMENTED generation).` — "Rag" as a headword will be read as the English word "rag." Should be `RAG`. See BLOCKERS.
- Line 166 `Reinforcement learning from human feedback (RLHF).` — same headword-casing inconsistency as LLM entry. Fix: `RLHF (reinforcement learning from human feedback).`
- Line 122 `Meta pivoted away from open weights with Muse Spark.` — factually consistent with the timeline (March 2026). Good.
- Line 133 `Contrast with closed-weight models like GPT-4 or Claude` — by May 2026, GPT-4 is dated as the canonical closed example. GPT-5 is referenced on line 92. Consider `GPT-5 or Claude` for currency.
- Pronunciation watchpoints: "Llama" (CB tends to say "lama" not "lah-mah" — consistent with brand), "DeepSeek" (not in glossary but appears in timeline), "RLHF" (CB will spell it; verify), "RAG" (verify CB doesn't read as "rag").

---

## 23_appendix_B_clean.txt

- Line 1 `Appendix b. a timeline at a glance.` — same casing inconsistency note as appendix A.
- Lines 99-105 — see BLOCKERS for chronology reorder.
- Line 12 `John McCarthy with Marvin Minsky, Nathaniel Rochester, and Claude Shannon.` — CB will say "Claude Shannon" cleanly but readers expecting the chatbot may misparse. No fix needed, audio is unambiguous.
- Line 22 `Tomas Mikolov` — Czech name, CB will likely read as "TOH-mas mee-KOH-lov" which is acceptable. Watchpoint.
- Line 50 `1 million users in 5 days. 100 million in 2 months.` — numerals; CB usually reads "one million" and "one hundred million" correctly. Watchpoint.
- Line 75 `2024, March - Mustafa Suleyman to Microsoft` — Suleyman is pronounced "SOO-lay-mahn." CB watchpoint. Also: this event is dated March 2024, but the Inflection deal was March 2024 — verify against timeline of book.
- Line 84 `Hassabis and John Jumper share the Nobel Prize in Chemistry for AlphaFold's work on protein folding.` — factually correct (October 2024). Good.
- Line 92 `Nvidia loses $500B in market cap in a single day.` — CB will read "$500B" as "five hundred B" or "five hundred billion dollars" depending on tokenization. Recommend: spell out as `$500 billion`.
- Line 96 `it generates over $1B in annualized revenue.` — same. Recommend: `$1 billion`.
- Line 100 `from a few hundred million to tens of billions over the year.` — fine as prose.
- Line 108 `Yann LeCun departs Meta to found AMI Labs` — Yann LeCun is pronounced "yahn luh-KUN." CB watchpoint. AMI Labs — verify CB reads as "A-M-I" not "ah-mee."
- Line 119 `Yoshua Bengio` — "yo-SHOO-ah BEN-jee-oh." CB watchpoint.
- Line 124 `valued at $1.25 trillion.` — CB will read as "one point two five trillion dollars" — fine.
- Line 136 `DeepSeek releases V4 trained largely on Huawei Ascend chips` — "Huawei" is pronounced "HWAH-way" but CB often says "HOO-ah-way." Watchpoint.
- Line 141 `folded entirely into SpaceX's SpaceXAI division.` — "SpaceXAI" is novel coinage; CB will likely read letter-by-letter as "space-ex-A-I" which is intended. Watchpoint.
- Line 9 `1956 - Dartmouth Workshop`, line 14 `1970s - First AI Winter`, line 21 `2013 - word2vec` — the en/em-dash separator between date and title may be read as "dash" by CB depending on character. Verify it's a hyphen-minus (`-`), not `—`. Quick scan suggests they're hyphens; should be safe.
- Line 23 `word2vec` — CB watchpoint, will likely say "word two vec." Acceptable.
- Section headers `PRE-HISTORY`, `The GPT years.`, `The CHATGPT moment.`, `The frontier years.`, `The deepseek moment and beyond.`, `The present moment (2026).` — mixed casing across section labels (some all-caps `PRE-HISTORY`, `CHATGPT`; some sentence-case). Per cleaner instructions this is intentional, no fix.
- Line 147 `2026, August (scheduled) - EU AI Act High-Risk Provisions` — "(scheduled)" reads cleanly. Good.

---

## 24_appendix_C_clean.txt

- Line 1 `Appendix c. further reading.` — same casing note.
- Line 11 `"Attention Is All You Need" (Vaswani et al, 2017)` — "Vaswani et al" — CB will read "et al" as "et al" letter-by-letter or as "et all." Recommend writing `Vaswani and colleagues` for narration clarity.
- Line 16 `"The Illustrated Transformer" (Jay Alammar)` — "Alammar" pronounced "al-AM-mar." Watchpoint.
- Line 21 `"Co-Intelligence: Living and Working with AI" by Ethan Mollick` — Mollick is "MOL-ick." Watchpoint.
- Line 29 `"Empire of AI" by Karen Hao (2025)` — "Hao" pronounced "how." CB watchpoint.
- Line 34 `"The Maniac" by Benjamin Labatut (2023)` — "Labatut" pronounced "lah-bah-TOOT." CB watchpoint. Also "John von Neumann" line 36 — CB usually reads as "von NOY-mahn"; verify.
- Line 39 `"Genius Makers" by Cade Metz (2021)` — fine.
- Line 46 `"The Alignment Problem" by Brian Christian (2020)` — fine.
- Line 52 `"Weapons of Math Destruction" by Cathy O'Neil (2016)` — "O'Neil" with apostrophe — CB usually handles cleanly.
- Line 57 `"Atlas of AI" by Kate Crawford (2021)` — fine.
- Line 64 `"The 2026 International AI Safety Report" (Yoshua Bengio, chair)` — Bengio watchpoint (see appendix B).
- Line 69 `"AI Snake Oil" by Arvind Narayanan and Sayash Kapoor (2024)` — "Arvind Narayanan" (ar-VIND nah-RAH-yah-nahn) and "Sayash Kapoor" (sa-YASH ka-POOR) — both CB watchpoints.
- Line 81 `"Machines of Loving Grace" (Dario Amodei, 2024)` — "Amodei" pronounced "ah-mo-DAY." CB watchpoint, often mispronounced as "ah-MOH-day-ee."
- Line 87 `"Situational Awareness" (Leopold Aschenbrenner, 2024)` — "Aschenbrenner" pronounced "ASH-en-BREN-er." CB watchpoint.
- Line 92 `"AI 2027" (Daniel Kokotajlo et al)` — "Kokotajlo" pronounced "ko-ko-TIE-lo." Strong CB watchpoint. Also `et al` again — recommend `and colleagues`.
- Line 98 `"The Coming Wave" by Mustafa Suleyman (2023)` — Suleyman watchpoint (see appendix B).
- Line 103 `"Filterworld" by Kyle Chayka (2024)` — "Chayka" pronounced "CHAI-kah." CB watchpoint.
- Line 109 `"Determined" by Robert Sapolsky (2023)` — "Sapolsky" pronounced "sa-POL-skee." CB watchpoint.
- Line 116 `The Marginalian, by Maria Popova` — "Popova" pronounced "po-POH-vah." CB watchpoint.
- Line 120-121 `One Useful Thing (Ethan Mollick) and Import AI (Jack Clark)` — fine.
- Line 130 `the AI Safety arxiv` — "arxiv" pronounced "AR-kive" (not "arks-iv"). Strong CB watchpoint; CB will almost certainly read as "arks-iv." Consider rewriting as `the AI Safety section of arxiv` or `the arxiv AI safety listings` — either way the pronunciation is at risk. Worth a manual phonetic substitution: `archive` won't work (different word); consider just accepting CB's likely reading or pre-substituting `arxiv` → `ar-kive` in a narration-only variant.
- Line 11, 16, 21, 29, 34, etc. — every entry uses straight quotes `"..."`. CB ignores quotation marks correctly; no issue.

---

## 00_author_note_FINAL_clean.txt

- Line 1 `Author's note on AI use - final locked version.` — this is metadata, NOT prose. Will be read aloud by CB. Strip before render or replace with the title `A Note on How This Book Was Made` from line 3. This is a cleaning artifact.
- Line 3 `A Note on How This Book Was Made` — works as spoken intro title. Good.
- Line 27 `Welcome.` — strong closing word; works as a transition into the book. Good.
- Lines 4-27 indented with two leading spaces (consistent with chapter 21 line 4-5). CB ignores leading whitespace. No issue.
- Standalone-as-spoken-intro check: yes, the note works standalone. It does what an audiobook author's note needs to do — sets expectations, takes responsibility, ends with a warm transition. No structural changes needed.
- Pronunciation watchpoints: none — vocabulary is plain English throughout.
- Line 1 IS a blocker for narration if not stripped — it will read "Author's note on AI use, dash, final locked version" before the actual title. Strongly recommend deleting line 1 entirely before render.

---

## Summary

- Two real BLOCKERS: the appendix A casing artifacts on AGI/GPT/RAG entries, and the appendix B chronology being out of order in the 2025 block. Both are quick fixes.
- Author's note line 1 is a third near-blocker — leftover metadata that will be spoken aloud unless stripped.
- Appendix C has a long pronunciation watchpoint list (author names) but no factual or structural problems.
- Chapter 21 is clean prose-wise; only the closing pointer line has a minor mismatch with the actual appendix titles.
- Currency check (May 2026): all dated claims align with the timeline. Glossary's "GPT-4 or Claude" example is the only thing reading slightly dated against GPT-5 being mentioned elsewhere in the same file.
