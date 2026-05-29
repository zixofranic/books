# Corrections worklist — Just Predicting Words

**DRAFT — pending author approval of wording.**

This is the single source of correction wording. The SAME text goes into:
1. `source/raw/<chapter>.txt` (→ regenerates `_clean.txt` for the text record + `_tts.txt` for audio → re-render), and
2. the **InDesign document, by hand** (surgical find/replace — no re-import, design work is preserved).

Use the **FIND** string to locate the passage in InDesign; replace with **REPLACE**. Identical wording in both places = print and audio stay in sync. After applying, run the verification grep (bottom).

Legend: 🔴 hard error (must fix) · 🟠 wording/precision · ✎ copyedit defect.

---

## 🔴 1 — Ch 5 — Musk lawsuit is OVER, not ongoing (FC-005)
Three spots. The trial ended **May 18, 2026**: jury rejected all Musk's claims (sued too late), judge dismissed, Musk appealing.

**1a — ch5 (≈L19)**
- FIND: `in a structure so unusual that it generated lawsuits that are still in court as I write this.`
- REPLACE: `in a structure so unusual that it generated lawsuits — the most prominent of which, brought by Elon Musk, went all the way to a jury trial in 2026.`

**1b — ch5 (≈L39)**
- FIND: `Eight years later, the two men would be on opposite sides of a federal lawsuit in Oakland, California, that is unfolding as I write this.`
- REPLACE: `Eight years later, the two men ended up on opposite sides of a federal lawsuit in Oakland, California. In May 2026, a jury rejected Musk's claims, finding he had waited too long to sue, and the judge dismissed the case. Musk has said he will appeal.`

**1c — ch5 (≈L101)**
- FIND: `There is the lawsuit from Elon Musk, which is in trial as I write this. Musk argues that OpenAI's transition from non-profit to for-profit was a betrayal of the original founding mission. He is asking the court to undo the for-profit conversion. He is seeking, in damages, up to one hundred and fifty billion dollars. The case is being heard by a jury in Oakland.`
- REPLACE: `There is the lawsuit from Elon Musk. Musk argued that OpenAI's transition from non-profit to for-profit was a betrayal of the original founding mission. He asked the court to undo the for-profit conversion, and sought up to one hundred and fifty billion dollars in damages. In May 2026, after an eleven-day trial in Oakland, a jury found that he had filed too late, and the judge dismissed the case. Musk's lawyers have said they will appeal.`
- Source: NPR/NBC/CNN, 2026-05-18.

---

## 🔴 2 — Ch 6 — "twelve researchers" → "seven" (FC-026)
**ch6 (≈L99)**
- FIND: `founded by twelve researchers became a nine-hundred-billion-dollar company`
- REPLACE: `founded by seven researchers became a nine-hundred-billion-dollar company`
- Source: Wikipedia/Britannica (Anthropic = 7 co-founders).

---

## 🔴 3 — Ch 6 — Pentagon reason is wrong (FC-031)
**ch6 (≈L97)** — the cause was a contract/usage-terms dispute, not "funding sources and corporate connections."
- FIND: `The reasoning, which has not been fully public, appears to involve concerns about the company's funding sources and corporate connections. Over a hundred enterprise customers reportedly raised concerns. Anthropic has been navigating this issue while continuing its broader growth.`
- REPLACE: `The dispute arose after contract negotiations broke down. The Pentagon wanted unrestricted use of Claude for all lawful military purposes; Anthropic refused to permit uses like fully autonomous weapons and domestic mass surveillance. When the company missed the government's deadline, the administration moved to bar federal agencies from using its technology. Anthropic has been challenging the designation in court while continuing its broader growth.`
- Source: CNBC/CNN/TechCrunch, March 2026.

---

## ✎ 4 — Appendix B — broken Llama 4 sentence (FC-056)
**Appendix B (timeline, "2025, April - Llama 4 Disaster")**
- FIND: `Meta releases Llama 4. The release is later found to have used results. Internal consequences are severe.`
- REPLACE: `Meta releases Llama 4. The launch is later found to have used manipulated benchmark results — different model versions were submitted to leaderboards than were released publicly. Internal consequences are severe.`

---

## 🟠 5 — Ch 8 — Scale AI figure $14.5B → $14.3B (FC-037)
**ch8 (≈L75)**
- FIND: `He spent fourteen and a half billion dollars to acquire forty-nine percent of Scale AI`
- REPLACE: `He spent about fourteen point three billion dollars to acquire forty-nine percent of Scale AI`

## 🟠 6 — Ch 6 — "80× forecasts" → growth (FC-028)
**ch6 (≈L73)**
- FIND: `Eighty times the company's own internal forecasts.`
- REPLACE: `Eighty times what it had been a year earlier.`

## 🟠 7 — "fastest-growing in human history" → hedge (FC-012) — TWO spots
**ch1 (≈L9)**
- FIND: `It became the fastest-growing consumer product in human history, faster than Facebook,`
- REPLACE: `It became, at the time, the fastest-growing consumer product in history, faster than Facebook,`

**ch2 (≈L133)**
- FIND: `A hundred million in two months. The fastest-growing consumer product in human history.`
- REPLACE: `A hundred million in two months. At the time, the fastest-growing consumer product in history.`
- (Note: Meta's Threads surpassed it for raw signup speed in July 2023.)

## 🟠 8 — Ch 2 — Amazon "similar money" → reconcile with ch6's $25B (FC-020)
**ch2 (≈L153)**
- FIND: `Amazon poured similar money into Anthropic.`
- REPLACE: `Amazon made a comparable bet on Anthropic, eventually committing up to twenty-five billion dollars.`

## 🟠 9 — Ch 12 — Schwartz date precision (FC-047) — optional
**ch12 (≈L9)**
- FIND: `In May 2023, a New York lawyer named Steven Schwartz`
- REPLACE: `In early 2023, a New York lawyer named Steven Schwartz`

---

## HELD — do NOT apply until author decides (open ⚠, FC-046/051/038/053/042)
The ch11 developer-productivity + translation stats, ch16 guardrail specifics, ch8 Meta capex/layoffs, ch17 OECD/Stanford figures, ch9 minor China stats. Verify against sources first; then add here.

---

## Verification (after applying)
**Audio/text record (automated):** grep each REPLACE string in the regenerated `_clean.txt` and `_tts.txt`; grep that each old string ("twelve", "still in court", "$14.5B"/"fourteen and a half", "internal forecasts") is ABSENT. (In `_tts.txt`, numbers are normalized — assert the spoken form.)
**Print (manual):** after the InDesign surgical edits, export the story text (or a proof PDF) and run the same grep so the printed book is confirmed to match.
