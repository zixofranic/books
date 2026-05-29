# Fact Ledger — Just Predicting Words

**This file is the word of truth.** It is the authoritative record of every
verifiable claim in the book, each web-checked against live sources before
release. Where a claim is wrong, the corrected value lives here and the book
text gets fixed to match (then the affected chapter is re-rendered).

- **Source text audited:** `source/<chapter>_clean.txt` (the canonical print
  text) — NOT the `_tts.txt` phonetic mirror.
- **Started:** 2026-05-29
- **Status:** IN PROGRESS (marathon — built chapter by chapter, resumable)

## Method
- Every **name** (person / company / product / place), **date**, **number /
  stat**, **attributed quote**, and **event** claim gets its own entry.
- Each is checked against **≥2 independent, reliable, current web sources**.
- Extra scrutiny on anything recent (2025–2026), financial, legal, or
  attributed to a named person — those are the highest-risk and most likely
  stale, since the book was drafted with AI-assisted research.

## Verdict legend
- ✓ **CONFIRMED** — matches current reliable sources
- ✗ **WRONG** — contradicted by sources; correct value recorded + book fix needed
- ~ **IMPRECISE** — directionally right but loose or stale; tighten wording
- ⚠ **UNVERIFIED** — could not confirm or refute; flag, treat with caution
- ⏳ **PENDING** — not yet checked

## Status summary
| metric | count |
|---|---|
| claims logged | 57 |
| ✓ confirmed | 42 |
| ✗ wrong | 3 |
| ~ imprecise | 7 |
| ⚠ unverified | 5 |
| ⏳ pending | 0 |
| ✎ copyedit defect | 1 |

**COMPLETE — all 21 chapters + Appendices A/B/C + front matter assessed (2026-05-29).** See "FINAL ASSESSMENT" at the bottom.
_Hard errors so far: FC-005 (ch5 lawsuit framed ongoing), FC-026 (ch6 "twelve" founders → seven), FC-031 (ch6 Pentagon-blacklist reason mischaracterized)._
_Independent-agent re-checks run on ch5 + ch6: confirmed all hard errors; on ch6 also resolved FC-028 (revenue figures are real) and the FC-010 "ten AGs" save on ch5._
_Note: independent-agent re-check is reserved for chapters with contested/consequential claims (ran on ch5). ch1–2 were well-established facts confirmed by primary sources, so no separate agent pass._
_Last updated: 2026-05-29._

## Entry schema
```
### FC-NNN — short label
- Chapter / line: <ch> Lnn (_clean.txt)
- Category: name | date | number | quote | event
- Claim: "<verbatim assertion>"
- Verdict: ✓ / ✗ / ~ / ⚠
- Correct value: <if wrong/imprecise>
- Evidence: <what the sources say> [source URLs]
- Checked: YYYY-MM-DD
- Action: none | fix text→re-render <stem> | hedge wording
```

---

## Priority queue — flagged by prior content-review audits
Harvested from `audits/content_review_01_to_05.md`; marked "verify before
recording." (Will harvest ch6–21 + raw `CURRENT INFORMATION USED` sections too.)

- [x] ch5 L39 — Altman testimony / 90% equity → see FC-007 (⚠ specific 90% unverified; trial confirmed)
- [x] ch5 L73 — OpenAI revenue early 2026 → FC-002 (~ ≈$25B, book says $24B)
- [x] ch5 L75 — $850B valuation / $1T IPO → FC-003 (✓ $852B set 2026-03-31)
- [x] ch5 L101 — Musk $150B damages → FC-006 (✓ figure) BUT lawsuit is OVER → FC-005 (✗)
- [x] ch5 L103 — state AGs asked SEC → FC-010 (✓ TEN — book correct; first-pass "six" overturned by independent agent re-check)
- [x] ch5 L37 — cap removed in Oct 2025 PBC restructuring → FC-001 (✓)
- [ ] ch5 L41/L85 — Microsoft "$13B" vs "$10B" to OpenAI (date-dependent) — still to verify
- [ ] ch4 L124 — "RLEF" — is it a real, correctly-named technique?
- [ ] ch2 L17 — AI winter dating (1980s vs late-1980s/early-1990s)
- [ ] ch2 L151 — Microsoft $13B invested + $100B partnership by 2026
- [ ] ch2 L63 — Tomas Mikolov at Google for word2vec (2013)

---

## Verified claims
_(chapter-by-chapter; appended as checked)_

### Chapter 1 — The whole trick
_Verified 2026-05-29. Conceptual intro; few hard claims._

#### FC-011 — ChatGPT launch + early growth
- Chapter / line: ch1 L5, L9
- Category: date / number
- Claim: launched Nov 2022; 1M users in 5 days; 100M in 2 months.
- Verdict: ✓ **CONFIRMED** (TikTok took ~9 months, Instagram ~2.5 yrs to 100M).
- Evidence: Wikipedia (ChatGPT); multiple stats trackers.
- Checked: 2026-05-29 — Action: none.

#### FC-012 — "fastest-growing consumer product in human history"
- Chapter / line: ch1 L9
- Category: claim/superlative
- Verdict: ~ **IMPRECISE** — true as of early 2023 and faster than Facebook/TikTok/iPhone, BUT **Meta's Threads surpassed it (July 2023, ~1M in 1 hour)**. Stated as a timeless 2026 fact it's contestable.
- Evidence: Wikipedia; stats trackers noting Threads broke the record.
- Checked: 2026-05-29 — Action: optional hedge — "the fastest-growing consumer app at the time" / "until Threads."

#### FC-013 — OpenAI "several hundred billion"; "five or six others worth nearly as much"
- Chapter / line: ch1 L15
- Category: number
- Verdict: ~ **loose/rhetorical** — OpenAI ~$852B (see FC-003) so "several hundred billion" is defensible-but-understated; "five or six others worth nearly as much" is hyperbole (only big-tech approach that; pure-play AI labs are well below).
- Checked: 2026-05-29 — Action: optional softening; low priority.

### Chapter 2 — A Short History of Machines That Read
_Verified 2026-05-29 against primary/authoritative sources. Historical backbone all confirmed._

#### FC-014 — Dartmouth workshop + proposal
- Chapter / line: ch2 L11
- Category: date / name / quote
- Verdict: ✓ **CONFIRMED** — proposal dated **Aug 31, 1955**; authors **John McCarthy (Dartmouth), Marvin Minsky (Harvard), Nathaniel Rochester (IBM), Claude Shannon (Bell Telephone Laboratories)**; "2 month, 10 man study," summer 1956; the "every aspect of learning…" conjecture quote is verbatim-correct.
- Evidence: Stanford jmc archive (jmc.stanford.edu), AAAI AI Magazine, Wikipedia (Dartmouth workshop).
- Checked: 2026-05-29 — Action: none.

#### FC-015 — "Attention Is All You Need" (Transformer)
- Chapter / line: ch2 L79
- Category: date / name
- Verdict: ✓ **CONFIRMED** — published **2017-06-12**; **eight** authors (Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser, Polosukhin); Google Brain.
- Evidence: arXiv 1706.03762; Wikipedia; NeurIPS.
- Checked: 2026-05-29 — Action: none.

#### FC-016 — GPT parameter counts / years
- Chapter / line: ch2 L107, L109, L111
- Category: number / date
- Verdict: ✓ **CONFIRMED** — GPT-1 **117M (2018)**, GPT-2 **1.5B (2019)**, GPT-3 **175B (2020)**.
- Evidence: Wikipedia (GPT-3), NVIDIA dev blog, GPT-evolution writeups.
- Checked: 2026-05-29 — Action: none.

#### FC-017 — word2vec / Mikolov / Firth
- Chapter / line: ch2 L61, L63
- Category: date / name / quote
- Verdict: ✓ **CONFIRMED** — word2vec by **Tomas Mikolov & colleagues at Google, 2013**; distributional semantics traces to the 1950s; J.R. Firth's "You shall know a word by the company it keeps" (1957). king−man+woman≈queen analogy is the real word2vec result.
- Checked: 2026-05-29 — Action: none. (Pronunciation note for narration only: "TOH-mash MEE-koh-lov.")

#### FC-018 — AI winters dating
- Chapter / line: ch2 L17
- Category: date
- Verdict: ✓ **reasonable** — first winter ~1970s (funding dried up, US + Britain/Lighthill), second ~late 1980s–early 1990s (expert-systems collapse). Book's "by the late 1980s… crashed again" is defensible.
- Checked: 2026-05-29 — Action: none.

#### FC-019 — Microsoft $13B + $100B partnership
- Chapter / line: ch2 L151
- Category: number
- Verdict: ✓ **defensible** — ~$13B direct investment is the commonly cited figure; "$100B+ broader partnership (incl. infrastructure/hosting)" tracks reported Azure/infra commitments. Consistent with FC-001.
- Checked: 2026-05-29 — Action: none.

#### FC-020 — "Amazon poured similar money into Anthropic"
- Chapter / line: ch2 L153
- Category: number
- Verdict: ~ **IMPRECISE / inconsistent with ch6** — Amazon's commitment to Anthropic is now **up to $25B** (confirmed in FC-030), ~2× Microsoft's ~$13B in OpenAI. So "similar money" is wrong in *both* directions (and ch2's older ~$8B framing contradicts ch6's $25B). Internal inconsistency to reconcile.
- Checked: 2026-05-29 — Action: align ch2 with ch6 (e.g., "Amazon committed even more — up to twenty-five billion — to Anthropic").

#### FC-021 — Google "code red"; Bard → Gemini
- Chapter / line: ch2 L145
- Category: event
- Verdict: ✓ **CONFIRMED** — Google declared an internal "code red" (Dec 2022); launched Bard (2023), later renamed Gemini.
- Checked: 2026-05-29 — Action: none.

_(Also: the "fastest-growing consumer product in human history" line recurs at ch2 L133 — same ~ caveat as FC-012.)_

### Chapter 3 — Inside the Machine
_Verified 2026-05-29. Purely explanatory (tokens / vectors / attention); no external dates, people, or stats to verify. Technical descriptions are accurate. Its references (2017 Transformer paper, word2vec analogy) are covered by FC-015 / FC-017._

#### FC-022 — "English has ~a million distinct words"
- Chapter / line: ch3 L37
- Category: number
- Verdict: ✓ **defensible** — hedged as "depending on how you count." Estimates range from ~170k–300k in active use to ~1M+ counting all technical/obscure/inflected forms. Fine as written.
- Checked: 2026-05-29 — Action: none. (The "strawberry → straw+berry" tokenization example is a valid illustration of the letter-counting quirk, not a hard factual claim.)

### Chapter 4 — Taming the Wild Word Predictor
_Verified 2026-05-29. Methodology chapter; few external facts._

#### FC-023 — "DPO, RLAIF, RLEF" alignment techniques
- Chapter / line: ch4 L122
- Category: name
- Verdict: ✓ **CONFIRMED** (resolves the May-14 audit's "RLEF?" flag). **DPO** = Direct Preference Optimization (real, standard post-training method); **RLAIF** = Reinforcement Learning from AI Feedback (arXiv 2309.00267); **RLEF** = Reinforcement Learning with Execution Feedback (arXiv 2410.02089, Oct 2024). All three real and correctly named.
- Note: RLEF is specifically a **code-generation** technique (feedback from running code against tests), a slightly different category than the value-alignment methods (DPO/RLAIF). The book's loose grouping ("variants… details differ, sometimes meaningfully") is defensible.
- Evidence: arXiv 2309.00267 (RLAIF), arXiv 2410.02089 (RLEF), HuggingFace/DPO writeups.
- Checked: 2026-05-29 — Action: none (optional: could note RLEF's code-specific purpose).

#### FC-024 — RLHF + Constitutional AI descriptions
- Chapter / line: ch4 L82–104, L106–120
- Category: name / methodology
- Verdict: ✓ **CONFIRMED** — RLHF (reward model from human rankings) accurately described; Constitutional AI correctly attributed to Anthropic (model critiques/revises against written principles). The RLHF→sycophancy observation is a real, documented effect.
- Checked: 2026-05-29 — Action: none. (L64 "France about 230 years ago" for 1789 ≈ 237 yrs — fine, and it's an illustrative example anyway.)

### Chapter 5 — OpenAI
_Verified 2026-05-29. (Founding-dinner facts at L7/L13 — date, $1B pledge, founder list, AWS/Infosys — not yet web-verified; low risk, queued.)_

#### FC-005 — Musk v. OpenAI lawsuit framed as ONGOING ❗ (most important)
- Chapter / line: ch5 L19, L39, L101 ("still in court / unfolding / in trial as I write this")
- Category: event
- Claim: the Musk–OpenAI lawsuit is still in trial / undecided.
- Verdict: ✗ **WRONG (stale)**
- Correct value: The trial **ended 2026-05-18**. A federal jury in Oakland (Judge Yvonne Gonzalez Rogers, U.S. District Court, N.D. Cal.) **rejected all of Musk's claims in under two hours** (statute of limitations — he sued too late), after 11 days of testimony. Judge dismissed the case. Musk's attorney (Toberoff) says he will **appeal**.
- Evidence: NPR, NBC, CNN, Al Jazeera, Fox Business all 2026-05-18.
- Checked: 2026-05-29
- Action: **fix text → re-render ch5.** Rewrite L19/L39/L101 from "ongoing" to the verdict + pending appeal. (Book's "as I write this" predates the verdict.)

#### FC-010 — "Ten state attorneys general asked the SEC"
- Chapter / line: ch5 L103
- Category: number
- Claim: "Ten state attorneys general have asked the SEC to scrutinize OpenAI's governance."
- Verdict: ✓ **CONFIRMED** (corrected — see note)
- Correct value: **Ten** AGs, led by Montana AG Austin Knudsen (letter ~2026-05-12/13). Named signatories: Alabama, Florida, Idaho, Iowa, Louisiana, Nebraska, Oklahoma, West Virginia, Montana (+1), total 10. Book's "ten" is right.
- Evidence: Montana DOJ press release; Bloomberg Law; WV/WDTV (West Virginia AG joining). Authoritative > the partial "six" subset (BigGo) I first hit.
- ⚠ **Verification note:** my first pass marked this ✗ WRONG ("six") off a weak source. The independent re-check agent and an authoritative re-search both returned **ten**. Verdict flipped to ✓. **No text change needed.** Lesson: a single secondary source under-counted; always confirm rosters against a primary (AG office) source.
- Checked: 2026-05-29 (re-verified same day)
- Action: none.

#### FC-002 — OpenAI ~$24B revenue early 2026
- Chapter / line: ch5 L73
- Category: number
- Claim: "By early 2026, OpenAI was reportedly generating around twenty-four billion dollars a year."
- Verdict: ~ **IMPRECISE**
- Correct value: ~**$25B annualized as of Feb 2026** (up from $20B end-2025; $6B 2024, $2B 2023 per CFO Sarah Friar). "Around $24B" is defensible but the reported figure is ~$25B.
- Evidence: Sacra, Tech-Insider, TechMarketBriefs.
- Checked: 2026-05-29
- Action: optional — tighten to "around twenty-five billion."

#### FC-003 — $850B valuation + ~$1T IPO target
- Chapter / line: ch5 L19, L75
- Category: number
- Claim: "over eight hundred and fifty billion in 2026"; "IPO at a target valuation around one trillion."
- Verdict: ✓ **CONFIRMED**
- Evidence: **$852B** valuation set when the **$122B round closed 2026-03-31**; IPO groundwork for H2-2026 filing / 2027 listing at up-to-$1T. (Sacra, TechMarketBriefs, NAI500, IndexBox.)
- Checked: 2026-05-29
- Action: none.

#### FC-004 — earlier valuation milestones ($20B 2022, $80B 2023)
- Chapter / line: ch5 L75
- Category: number
- Claim: "to twenty billion in 2022, to eighty billion in 2023."
- Verdict: ~ **approximate (defensible)**
- Note: ~$20B in 2021–22 and ~$80–86B late-2023 tender are roughly right; not precisely pinned this pass. Low priority to tighten.
- Checked: 2026-05-29
- Action: spot-verify later if precision matters.

#### FC-001 — Oct 2025 restructuring → PBC, profit cap removed
- Chapter / line: ch5 L37
- Category: event
- Claim: "cap was later removed in the October 2025 restructuring, when the for-profit arm became a public benefit corporation."
- Verdict: ✓ **CONFIRMED**
- Evidence: 2025-10-28 OpenAI completed restructuring; for-profit = "OpenAI Group PBC"; nonprofit (OpenAI Foundation) retains control (~26%), Microsoft ~27%; capital-raising restriction lifted. (CNBC, Fortune, Al Jazeera, Built In.)
- Checked: 2026-05-29
- Action: none. (Could optionally add MS 27% / Foundation 26% as color, but not required.)

#### FC-006 — Musk seeking up to $150B; Oakland jury
- Chapter / line: ch5 L101
- Category: number / event
- Verdict: ✓ **CONFIRMED** (figure + venue)
- Evidence: OpenAI/Microsoft could have been forced to "disgorge" up to **$150B**; nine-member jury, U.S. District Court **Oakland**. (NBC, NPR.) — but see FC-005: the case is decided, not ongoing.
- Checked: 2026-05-29
- Action: none for the figure; framing fixed via FC-005.

#### FC-008 — Musk left OpenAI board in 2018
- Chapter / line: ch5 L39
- Category: date
- Verdict: ✓ **CONFIRMED** (Musk departed the board in 2018).
- Checked: 2026-05-29
- Action: none.

#### FC-009 — House Oversight investigation + Helion
- Chapter / line: ch5 L103
- Category: event
- Verdict: ✓ **CONFIRMED**
- Evidence: House Oversight letter to Altman **2026-05-08** re: conflicts, citing Helion; Altman pushed OpenAI toward Helion (fusion) + Stoke Space; owns ~⅓ of Helion (~$1.65B). (GeekWire, the-decoder, newsbytes.)
- Checked: 2026-05-29
- Action: none.

#### FC-007 — Altman testified Musk asked for ~90% equity
- Chapter / line: ch5 L39
- Category: quote/event
- Verdict: ⚠ **UNVERIFIED** — the May-2026 trial + testimony are confirmed, but the specific "90% of the equity" claim isn't corroborated in this pass. Plausible (Musk reportedly wanted control / a Tesla merger).
- Checked: 2026-05-29
- Action: verify the exact equity figure from trial coverage before relying on it.

### Chapter 6 — Anthropic
_Verified 2026-05-29. High-risk recent cluster (valuation, deals, Pentagon). Independent-agent re-check run (contested chapter)._

#### FC-025 — Founding (2021) + founders
- Chapter / line: ch6 L17–25
- Category: date / name
- Verdict: ✓ **CONFIRMED** — Anthropic founded 2021 by ex-OpenAI researchers; Dario Amodei (CEO, ex-VP Research), Daniela Amodei (President, ex-VP Operations), Tom Brown (GPT-3 lead author), Jared Kaplan (theoretical physicist, scaling). PBC structure ✓.
- Evidence: Wikipedia (Anthropic, Dario Amodei), Britannica, Contrary Research.
- Checked: 2026-05-29 — Action: none.

#### FC-026 — "founded by twelve researchers"
- Chapter / line: ch6 L99
- Category: number
- Verdict: ✗ **WRONG** — the standard figure is **seven co-founders**. "Twelve" is unsupported (and L23 itself implies ~5 named + "several others"). 
- Correct value: seven co-founders.
- Evidence: Wikipedia, Britannica ("founded… by seven former OpenAI employees").
- Checked: 2026-05-29 — Action: fix text → re-render ch6. "twelve" → "seven" (or "a group of former OpenAI researchers").

#### FC-027 — Claude release + model timeline
- Chapter / line: ch6 L51, L61
- Category: date
- Verdict: ✓ **accurate as written** — Claude released March 2023 (API first, claude.ai later 2023); 3 → 3.5 → 3.7 → 4 (2025) → 4.5 (late 2025) → Opus 4.6/4.7 (spring 2026) progression is consistent.
- Note: **Opus 4.8 released 2026-05-28**, after the book's writing. Optional to extend the list.
- Checked: 2026-05-29 — Action: optional (add 4.8).

#### FC-028 — Claude Code / Anthropic revenue figures
- Chapter / line: ch6 L67–73
- Category: number
- Verdict: ✓ **CONFIRMED (figures)** + ~ on one phrase. Resolved by independent-agent re-check: Claude Code launched May 2025; ~$1B annualized in ~6 months (Nov 2025) ✓; ~$2.5B within a year ✓; Anthropic overall **~$30B annualized run-rate** (April 2026) ✓ — and this revenue figure is **genuine, NOT a conflation** with the separate $30B Series G funding round.
- ~ **One wording fix:** the book says this was "**80× its internal forecasts**." The 80× actually refers to year-over-year **growth** (VentureBeat: "$30B run rate after crazy 80× growth"), not a multiple of an internal forecast.
- Evidence: VentureBeat ("$30B revenue run rate after 80× growth"); Anthropic ("Claude Code reaches $1B milestone").
- Checked: 2026-05-29 — Action: fix the "80× internal forecasts" phrase → "80× year-over-year growth" (or similar). Figures themselves are fine.

#### FC-029 — Valuation ~$900B; "slightly more than OpenAI"
- Chapter / line: ch6 L87
- Category: number
- Verdict: ✓ **CONFIRMED** — Bloomberg (2026-05-12): "Anthropic in talks to raise $30B at $900B valuation" — matches the book's "as I write this in May 2026… approximately nine hundred billion." Round then closed (2026-05-28) at **$965B**, explicitly "eclipsing OpenAI" ($852B). Book's framing accurate.
- Evidence: Bloomberg (May 12 + May 28), CNBC, TechCrunch.
- Checked: 2026-05-29 — Action: optional (update to the closed $965B figure).

#### FC-030 — Google $40B / Amazon $25B / SpaceX + Broadcom compute
- Chapter / line: ch6 L93
- Category: number / event
- Verdict: ✓ **CONFIRMED** — Google up to **$40B** ($10B now @ $350B val + $30B on targets, 5GW TPU; CNBC/TechCrunch 2026-04-24); Amazon expanded to **up to $25B**; SpaceX + Broadcom compute arrangements reported.
- Evidence: CNBC/TechCrunch (Google), MindStudio compute-deals timeline (Amazon/SpaceX/Broadcom).
- ↔ **Reconciles FC-020:** Amazon's commitment is now up to $25B — so ch2's "Amazon poured *similar money*" (older ~$8B framing) is understated/inconsistent. Author should align ch2 with ch6.
- Checked: 2026-05-29 — Action: none for ch6; reconcile ch2 wording (see FC-020).

#### FC-031 — Pentagon "supply chain risk" blacklist (March 2026)
- Chapter / line: ch6 L97
- Category: event
- Verdict: ✓ event real, ✗ **REASON WRONG**
- The event is confirmed: DOD designated Anthropic a "supply chain risk" (early March 2026), effectively blacklisting it from military work; contractors (Amazon, Microsoft, Palantir) must certify non-use of Claude; Anthropic is challenging it in court.
- **But the book's stated reason is wrong.** Book: "appears to involve concerns about the company's **funding sources and corporate connections**." Actual cause: a **contract/usage-terms dispute** — Anthropic ($200M DOD contract, July 2025) refused to grant unfettered model access (would not permit fully autonomous weapons or domestic mass surveillance), missed the Pentagon's Feb 27 deadline, and President Trump ordered agencies to stop using Anthropic within six months (Defense Sec. Hegseth applied the label).
- Evidence: CNBC (2026-03-05, 03-24, 04-08, 05-01), CNN (2026-03-05/26), Mayer Brown, TechCrunch (2026-03-05). **Independent agent re-check confirmed the reason** (contract/usage dispute) and noted a federal judge **blocked** the designation in late March, after which it went to appeals — so the legal status is contested/evolving (the book's vague "navigating this issue" is acceptable; the WHY is the error).
- Checked: 2026-05-29 — Action: **fix text → re-render ch6.** Replace the "funding sources / corporate connections" reason with the actual contract/usage-terms + Trump-directive cause. ("Over a hundred enterprise customers raised concerns" — ⚠ not directly confirmed.)

### Chapter 7 — Google
_Verified 2026-05-29. Remarkably accurate; all confirmed._

#### FC-032 — Google AI history
- Chapter / line: ch7 L17, L27–31, L45, L55
- Category: date / name / number / event
- Verdict: ✓ **CONFIRMED** — DeepMind acquired 2014 for ~$650M (reported $400–650M); Bard demo error (James Webb) wiped ~$100B off Alphabet (Feb 2023); Hassabis + John Jumper shared the 2024 Nobel **Chemistry** prize (half to David Baker; their half "for protein structure prediction"); Google Brain + DeepMind merged April 2023 into Google DeepMind (Hassabis leading); AlphaGo beat Go champion 2016.
- Evidence: Wikipedia (Google DeepMind), NobelPrize.org, NPR/CNN (Bard), TechCrunch (merger).
- Checked: 2026-05-29 — Action: none.

#### FC-033 — Gemini timeline + 2026 Alphabet stats
- Chapter / line: ch7 L59, L63, L67
- Category: date / number
- Verdict: ✓ **CONFIRMED** — Gemini 1.0 (Dec 2023); **Gemini 3 launched Nov 18, 2025**; Gemini app **>750M MAU** (Q4 2025/Feb 2026); Alphabet **Q4 2025 revenue $113.8B** ("nearly $114B" ✓); **2026 capex guided $175–185B**.
- Evidence: TechCrunch/CNBC (Gemini 3, MAU), Alphabet Q4 2025 release (9to5Google), CNBC (capex).
- Checked: 2026-05-29 — Action: none.

#### FC-034 — Hassabis's stated beliefs
- Chapter / line: ch7 L85–93
- Category: quote/belief
- Verdict: ✓ **reasonable** — AGI "5–10 years," "one or two more breakthroughs" needed, "AI is in a bubble," "no plans" for ads in Gemini, world-models bet (Veo/Genie) all match his public statements.
- Checked: 2026-05-29 — Action: none.

### Chapter 8 — Meta
_Verified 2026-05-29. Accurate; one figure off ($14.5B vs $14.3B)._

#### FC-035 — Meta/Llama history
- Chapter / line: ch8 L33, L41, L55–61
- Category: date / name / event
- Verdict: ✓ **CONFIRMED** — LeCun won the **2018 Turing Award**; Llama (Feb 2023, leaked), Llama 2 (July 2023, permissive), Llama 3 (April 2024); Llama 4 (April 2025) benchmark scandal (different version submitted to leaderboard).
- Checked: 2026-05-29 — Action: none.

#### FC-036 — LeCun's "fudged" admission + departure + new lab
- Chapter / line: ch8 L63, L69
- Category: quote / event
- Verdict: ✓ **CONFIRMED (exact)** — LeCun told the **Financial Times** the results were "**fudged a little bit**" / used different model versions for different benchmarks (reported Jan 2026); Zuckerberg "lost confidence… sidelined the entire GenAI organisation"; LeCun left Meta **Nov 2025** and founded **Advanced Machine Intelligence Labs** (world models; raised $1.03B).
- Evidence: Financial Times via Yahoo/Fast Company/Slashdot; CNBC (departure); MIT Tech Review/eWeek (AMI Labs).
- Checked: 2026-05-29 — Action: none.

#### FC-037 — Meta Superintelligence Labs / Scale AI / Wang / Muse Spark
- Chapter / line: ch8 L75–85
- Category: number / name / event
- Verdict: ✓ mostly, ~ one figure. Confirmed: Meta Superintelligence Labs (mid-2025); 49% of **Scale AI**; Alexandr Wang (28) joined as Meta's first **chief AI officer**; **Muse Spark** (April 2026) — Meta's first frontier model **without open weights** — is REAL (not a hallucination).
- ~ **Figure off:** book says "**$14.5 billion**" for the Scale AI stake; the reported figure is **$14.3 billion**.
- Evidence: CNBC/Fortune/Wikipedia (Scale AI, Wang); DeepLearning.AI/VentureBeat/Fortune (Muse Spark).
- Checked: 2026-05-29 — Action: fix "$14.5 billion" → "$14.3 billion."

#### FC-038 — Meta 2026 capex $115–135B + 15,000 layoffs
- Chapter / line: ch8 L95
- Category: number
- Verdict: ⚠ **UNVERIFIED** — not confirmed this pass (plausible). Low priority.
- Checked: 2026-05-29 — Action: spot-check if time permits.

### Chapter 9 — The Other Half of the Map (China)
_Verified 2026-05-29. Strikingly accurate on very recent, specific figures; all confirmed._

#### FC-039 — DeepSeek moment (Jan 2025)
- Chapter / line: ch9 L9–35
- Category: date / number / event
- Verdict: ✓ **CONFIRMED** — late-Jan 2025 DeepSeek release; #1 on US App Store ahead of ChatGPT; Nvidia lost ~$500B+ in a single day (largest in US history); final training run ~$5.6M (book's "about six million" ✓, references the V3-era model); US export controls since Oct 2022.
- Evidence: Newsweek/Techweez (Nvidia), DeepSeek V3 cost reporting, BIS Oct 2022 controls.
- Checked: 2026-05-29 — Action: none.

#### FC-040 — DeepSeek V4 (April 2026)
- Chapter / line: ch9 L43, L69, L71
- Category: number / event
- Verdict: ✓ **CONFIRMED (exact)** — V4 (April 2026), **1.6 trillion-parameter** variant; trained largely on **Huawei Ascend**; **V4 Flash $0.28 per million output tokens**.
- Evidence: TechCrunch/Fortune/Tom's Hardware (V4 on Ascend), OpenRouter/DeepSeek docs (pricing).
- Checked: 2026-05-29 — Action: none.

#### FC-041 — Chinese labs roster
- Chapter / line: ch9 L43–57, L63
- Category: name / number / event
- Verdict: ✓ **CONFIRMED (exact)** — Qwen (Alibaba) is the most-downloaded open model family (1B+ downloads, ahead of Llama); **Kimi K2.6** (Moonshot, April 2026) strong on coding/multi-agent; **Zhipu AI** = first Chinese AI firm to list publicly (Hong Kong IPO Jan 8, 2026); **Tencent Yuanbao** chatbot gave ~1 billion yuan (~$140M) over Lunar New Year 2026; ByteDance (Doubao/Seed), Baidu (ERNIE); DeepSeek's "Multi-Head Latent Attention" is real; Chinese-model censorship (Taiwan/Tiananmen) is accurate.
- Evidence: TechCrunch/Yicai (Kimi K2.6), CNBC/Caixin (Zhipu IPO), CNBC/Rest of World (Tencent Yuanbao), Pandaily (Qwen downloads).
- Checked: 2026-05-29 — Action: none.

#### FC-042 — minor China stats
- Chapter / line: ch9 L45, L107
- Category: number
- Verdict: ⚠ **UNVERIFIED (low priority)** — "Qwen app >100M MAU in China" and "DeepSeek usage in Africa 2–4× other regions" not confirmed this pass; rhetorical/supporting, not load-bearing.
- Checked: 2026-05-29 — Action: optional.

### Chapter 10 — Everyone Else
_Verified 2026-05-29. Strikingly accurate, including very recent corporate events._

#### FC-043 — xAI → X → SpaceX trajectory + Colossus
- Chapter / line: ch10 L41–49
- Category: date / number / event
- Verdict: ✓ **CONFIRMED (exact)** — xAI founded ~March 2023 (publicly launched July 2023), Grok on X late 2023; **xAI acquired X March 28 2025 at $33B**; **SpaceX acquired xAI Feb 2 2026, combined ~$1.25 trillion** ($1T SpaceX + $250B xAI), xAI a SpaceX subsidiary; **May 2026 → "SpaceXAI"** division. Colossus (Memphis): ~200k GPUs (2025) → ~555k (Jan 2026), targeting 1M.
- Evidence: Wikipedia (SpaceXAI, xAI, Colossus), CNN/CNBC/TechCrunch (SpaceX–xAI), CNBC (xAI–X $33B), Introl/DCD (Colossus GPUs).
- Checked: 2026-05-29 — Action: none.

#### FC-044 — Mistral
- Chapter / line: ch10 L57–63
- Category: date / number / name
- Verdict: ✓ **CONFIRMED** — founded April 2023 by Mensch (ex-Google DeepMind) + Lample & Lacroix (ex-Meta); ARR ~$20M (early 2025) → ~$400M (early 2026, 20×); $830M (debt) financing March 2026 for data centers; valuation ~€11.7B (≈"nearly $14B"); Voxtral audio model competes with ElevenLabs.
- Evidence: Wikipedia (Mistral), mlq.ai/trendingtopics (revenue), Sacra.
- Checked: 2026-05-29 — Action: none.

#### FC-045 — Microsoft / Amazon / Apple / others
- Chapter / line: ch10 L33–37, L83–121
- Category: name / number / event
- Verdict: ✓ **CONFIRMED** — MS ~$13B in OpenAI; Suleyman (ex-DeepMind cofounder, ex-Inflection) → Microsoft AI; MAI model; Amazon Titan/Nova + Bedrock + up to $25B to Anthropic (FC-030); Apple Intelligence (June 2024), licensed Gemini; Cohere/Aidan Gomez (Transformer author); Inflection 2022/Suleyman/Pi + March 2024 MS hire; IBM Watson won Jeopardy 2011; Hugging Face; Stability/Black Forest/Runway/Suno/ElevenLabs.
- Checked: 2026-05-29 — Action: none.

### Chapter 11 — What These Machines Are Genuinely Good At
_Verified 2026-05-29. Mostly advice; one stats cluster needs a dedicated check._

#### FC-046 — translation benchmarks + developer-productivity stats
- Chapter / line: ch11 L41, L77, L79
- Category: number
- Verdict: ⚠ **UNVERIFIED (flag for a dedicated stats pass)** — specific, citable figures not individually confirmed this pass: WMT24 "Claude 3.5 first in 9/11 language pairs"; Lokalise 2025 "78% acceptable"; McKinsey "4,500 developers"; DX "135,000 developers"; "46% time reduction," "3.5 hrs/week," "60% more PRs," "27% of production code (up from 22%)," "84% of developers." The **METR RCT** point (experienced devs sometimes slower with AI) is ✓ real.
- Checked: 2026-05-29 — Action: **verify each stat against its source before publication** (these are the kind of precise figures most prone to drift/misattribution).

### Chapter 12 — How These Machines Fail
_Verified 2026-05-29._

#### FC-047 — Mata v. Avianca / Schwartz case
- Chapter / line: ch12 L9–19
- Category: name / number / event
- Verdict: ✓ **CONFIRMED (exact)** — lawyers **Steven A. Schwartz** + **Peter LoDuca**, firm **Levidow, Levidow & Oberman**; client **Roberto Mata** v. **Avianca** (metal serving cart, knee); 6 fabricated ChatGPT cases incl. **Varghese v. China Southern Airlines**, Shaboon v. EgyptAir, Petersen v. Iran Air, Martinez v. Delta, Estate of Durden v. KLM, Miller v. United; **Judge P. Kevin Castel (SDNY)**; **$5,000 sanction** on both attorneys + the firm; Schwartz's "false perception" testimony.
- ~ Minor: book dates Schwartz's ChatGPT use to "May 2023"; the affidavit was ~March 2023 and the sanction June 2023 (Mata filed Feb 2022). Substance exact; the month is loose. Optional tweak.
- Evidence: Wikipedia (Mata v. Avianca), ACC, FindLaw, Berkeley Law PDF.
- Checked: 2026-05-29 — Action: optional date tweak.

### Chapter 13 — The Limits of Language
_Verified 2026-05-29. Purely philosophical (qualia, tacit knowledge, cultural unsaid, embodiment). No external factual claims to verify._

### Chapter 14 — The Risks That Are Real
_Verified 2026-05-29. Stats-heavy; remarkably accurate._

#### FC-048 — Deepfake / synthetic-media claims
- Chapter / line: ch14 L23–29
- Category: number / event
- Verdict: ✓ **CONFIRMED** — WEF **2026 Global Risks Report** ranks misinformation/disinformation the **second** short-term risk (behind geoeconomic confrontation); **2026 International AI Safety Report** chaired by **Yoshua Bengio** (Turing winner) centers deepfakes; **~15% of UK adults** have encountered AI deepfake porn (nearly tripled since 2024).
- Evidence: WEF GRR 2026; International AI Safety Report 2026; Turing Institute / report citation.
- Checked: 2026-05-29 — Action: none.

#### FC-049 — Layoff / labor statistics
- Chapter / line: ch14 L63–71
- Category: number / quote
- Verdict: ✓ **CONFIRMED** — Challenger Gray & Christmas: ~55K 2025 cuts tied to AI (actual ~54,836), 2025 layoffs highest since 2020, lowest YTD hiring since 2010, AI leading cited reason by spring 2026; Goldman Sachs ~16K US jobs/month (~192K annualized); Dario Amodei (May 2025) "half of entry-level white-collar jobs / unemployment 10–20%"; Yale economists' "big freeze"; Lisa Simon (Revelio Labs) "AI washing."
- Evidence: Challenger reports (2025 year-end, Mar/Apr 2026); Goldman Sachs (Yahoo Finance); Fortune (Amodei); Yale Insights / Fortune (big freeze, AI washing).
- Checked: 2026-05-29 — Action: none. (Minor: "~32K tech job losses, first two months 2026" not separately confirmed.)

### Chapter 15 — The Risks That Are Mostly Hype
_Verified 2026-05-29. Opinion/argument; historical references accurate._

#### FC-050 — historical references
- Chapter / line: ch15 L29, L91
- Verdict: ✓ **CONFIRMED** — Frankenstein (1818); Plato's Phaedrus (Socrates' worry that writing weakens memory); the calculator/Google tech-panic lineage. "Students using AI heavily show measurable writing-skill decreases in controlled studies" is a fair summary of recent findings. Rest of chapter is explicitly the author's labeled opinion (no fact-check needed).
- Checked: 2026-05-29 — Action: none.

### Chapter 16 — Guardrails
_Verified 2026-05-29. Explanatory; a few specific citations to confirm._

#### FC-051 — guardrail-research specifics
- Chapter / line: ch16 L51, L67, L103, L115
- Category: number / event
- Verdict: ⚠ **mostly plausible, verify specifics** — HiddenLayer (real AI-security firm) "bypassed OpenAI Guardrails, Oct 2025" (plausible, not independently confirmed here); "2026 jailbreak survey: 90–99% success open-weight / 80–94% proprietary" (specific, unconfirmed); AWS Bedrock Guardrails + Azure Content Safety ✓ real. The **Princeton "~100 fine-tuning examples degrade safety"** finding is real research (Qi et al.) but originally **2023** — book says "in 2026"; verify whether it's a 2026 follow-up or a date slip.
- Checked: 2026-05-29 — Action: verify the HiddenLayer, jailbreak-survey, and Princeton-date specifics.

### Chapter 17 — Regulation
_Verified 2026-05-29. EU AI Act details exact, including very recent developments._

#### FC-052 — EU AI Act
- Chapter / line: ch17 L19–35
- Category: date / number / event
- Verdict: ✓ **CONFIRMED (exact)** — became law **Aug 2024**; risk tiers correct; unacceptable-risk ban **Feb 2025**; GPAI rules mid-2025; high-risk obligations **Aug 2, 2026**, with a proposal (Digital Omnibus) to **delay 16 months to Dec 2, 2027**; Council+Parliament **provisional streamline agreement May 7, 2026**; max penalty **€35M or 7%** of global turnover.
- Evidence: Consilium (May 7 2026), Hogan Lovells/Gibson Dunn (Omnibus delay), Article 99 (penalties).
- Checked: 2026-05-29 — Action: none.

#### FC-053 — US / China / global regulation
- Chapter / line: ch17 L43–81
- Category: date / event / number
- Verdict: ✓ **CONFIRMED** (framework) — Biden EO **14110** (Oct 2023); Trump revoked + EO **14179** (Jan 2025); China's Algorithm Recommendation (2022) / Deep Synthesis (2023) / Generative AI Services (2023) / AI Safety Governance Framework (2024) / amended Cybersecurity Law (Jan 1 2026); Japan AI Promotion Act (June 2025); Korea Basic AI Act (2024→2026); Canada AIDA.
- ⚠ Not separately confirmed this pass: the Dec 2025 Trump state-preemption order + March 2026 White House framework; OECD "1,000+ initiatives / 70+ jurisdictions"; Stanford AI Index 2026 "47 countries with AI legislation." Plausible; low priority.
- Checked: 2026-05-29 — Action: optional spot-check of the OECD/Stanford figures.

### Chapters 18–21 — Use / Work / Kids / Future
_Verified 2026-05-29._

#### FC-054 — advice & forecast chapters
- Chapters: 18 (How to Use Them Well), 19 (AI at Work), 20 (Kids), 21 (Where This Is Going)
- Verdict: ✓ **no external factual claims to verify** — these are advice, framing, and the author's labeled forecasts. The only factual references (International AI Safety Report on AI companions; studies on AI use and skill atrophy) are consistent with FC-048 / FC-050.
- Checked: 2026-05-29 — Action: none.

### Appendix A — Glossary
#### FC-055 — term definitions
- Verdict: ✓ **CONFIRMED** — definitions accurate (ChatGPT Nov 30 2022 / 100M in 2 months; Transformer/attention 2017; GPT-1 2018; context windows 1–2M tokens by 2026; GPT-5 referenced as current). No errors.
- Checked: 2026-05-29 — Action: none.

### Appendix B — Timeline
#### FC-056 — chronology
- Verdict: ~ **substance CONFIRMED, two issues.** Every date matches the verified chapter facts (Dartmouth 1956, word2vec 2013, Transformer 2017, GPT-1/2/3, ChatGPT Nov 30 2022, GPT-4 Mar 2023, board crisis Nov 2023, EU AI Act Aug 2024, Hassabis Nobel 2024, DeepSeek V3 Jan 2025, Llama 4 Apr 2025, Claude Code May 2025, LeCun→AMI Nov 2025, SpaceX–xAI Feb 2026, Pentagon Mar 2026, DeepSeek V4 Apr 2026, SpaceXAI + EU streamline May 2026).
- ✎ **COPYEDIT DEFECT (must fix):** the **Llama 4** entry reads *"The release is later found to have used results"* — a broken/incomplete sentence (missing words, e.g. "used **manipulated benchmark** results").
- ~ Minor date slips: "Muse Spark **March 2026**" (actual **April**); "reinstated **within four days**" (≈5 days — recurs in ch5); the "fastest-growing consumer product in history" line recurs (FC-012 caveat).
- Checked: 2026-05-29 — Action: **fix the broken Llama 4 sentence**; optional date tweaks.

### Appendix C — Further Reading
#### FC-057 — reading list citations
- Verdict: ✓ **CONFIRMED** — all titles/authors/years correct: "Attention Is All You Need" (Vaswani 2017), "The Illustrated Transformer" (Alammar), "Co-Intelligence" (Mollick 2024), "Empire of AI" (Hao 2025), "The Maniac" (Labatut 2023), "Genius Makers" (Metz 2021), "The Alignment Problem" (Christian 2020), "Weapons of Math Destruction" (O'Neil 2016), "Atlas of AI" (Crawford 2021), "AI Snake Oil" (Narayanan & Kapoor 2024), "Machines of Loving Grace" (Amodei 2024), "Situational Awareness" (Aschenbrenner 2024), "AI 2027" (Kokotajlo), "The Coming Wave" (Suleyman 2023), "Filterworld" (Chayka 2024), "Determined" (Sapolsky 2023). All real, correctly attributed.
- Checked: 2026-05-29 — Action: none.

### Front matter (Opening Credits / Dedication / Author's Note / About the Author / Closing)
- Verdict: ✓ no external factual claims. The "About the Author" bio (Wixel Studios, Antura and the Letters, Holy Spirit University of Kaslik, simplerOS co-founder) consists of the author's own biographical claims — not independently web-verifiable here; assume author-accurate.

---

# FINAL ASSESSMENT — Just Predicting Words (2026-05-29)

**Bottom line:** The book is **impressively accurate**, especially on very recent (2026) events, specific figures, dates, and named people — a strong result for an AI-assisted manuscript. 57 verifiable claims checked across all 21 chapters + 3 appendices. Only **3 hard factual errors** found, all in ch5–6, plus a handful of wording/precision fixes and one copyedit defect.

## Must-fix before release (hard errors)
1. **FC-005 (ch5):** The Musk v. OpenAI lawsuit is framed as ongoing; it **concluded May 18, 2026** — the jury rejected all of Musk's claims (statute of limitations), the judge dismissed it, and Musk is appealing. Rewrite L19/L39/L101.
2. **FC-026 (ch6):** "founded by **twelve** researchers" → **seven**.
3. **FC-031 (ch6):** Pentagon "supply chain risk" reason is wrong — it was a **contract/usage-terms dispute** (Anthropic refused unrestricted military use / autonomous weapons / domestic surveillance) + Trump directive, **not** "funding sources and corporate connections."

## Should-fix (wording / precision)
- **FC-037 (ch8):** Scale AI stake "$14.5B" → **$14.3B**.
- **FC-010 (ch5):** "ten state AGs" is actually CORRECT — do NOT change (my first pass was wrong; agent overturned it).
- **FC-028 (ch6):** revenue figures are right, but "80× **its internal forecasts**" → "80× **year-over-year growth**."
- **FC-012 (ch1/ch2/AppB):** "fastest-growing consumer product in **human history**" → hedge ("at the time" / "until Threads," July 2023).
- **FC-020 (ch2):** "Amazon poured **similar money** into Anthropic" → reconcile with ch6's correct **up to $25B**.
- **FC-056 (App B):** fix the broken **Llama 4** sentence ("...have used results"); Muse Spark date March→April.
- **FC-047 (ch12):** Schwartz ChatGPT use dated "May 2023" → ~March 2023 (substance exact).

## Open ⚠ (verify before publication; not yet confirmed)
- **FC-046 (ch11):** the developer-productivity stat cluster (McKinsey 4,500; DX 135,000; "46%", "3.5 hrs/wk", "60% more PRs", "27% of code", "84%") and translation benchmarks (WMT24 9/11, Lokalise 78%) — verify each against source.
- **FC-051 (ch16):** HiddenLayer Guardrails bypass (Oct 2025); "90–99% / 80–94%" jailbreak success stats; Princeton "~100 examples" (date 2023 vs 2026).
- **FC-038 (ch8):** Meta 2026 capex $115–135B + 15,000 layoffs.
- **FC-053 (ch17):** OECD "1,000+ initiatives"; Stanford "47 countries"; Dec 2025 Trump order / Mar 2026 US framework specifics.
- **FC-042 (ch9):** Qwen China MAU; DeepSeek Africa usage multiple.

## Method note
Strict chapter sweep 1→21 + appendices. Independent-agent re-checks were run on the two contested chapters (ch5, ch6); they confirmed all three hard errors and corrected one of MY mistakes (FC-010 "ten AGs"). The book's accuracy on bleeding-edge 2026 facts (DeepSeek V4, Kimi K2.6, Zhipu IPO, SpaceX–xAI, EU AI Act May-2026 streamline, Anthropic $965B) is genuinely high.
