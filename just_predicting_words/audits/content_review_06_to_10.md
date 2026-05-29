# Content Review: Chapters 06-10

Book: *Just Predicting Words: How ChatGPT, Claude, and Modern AI Actually Work* by Ziad El Feghali
Voice: Chatterbox `burton`, ~120 wpm
Reviewer pass: prose audit + factual sanity for May 2026

---

## BLOCKERS

- Ch6, opening block (lines 1-7) — A "NOTE ON CONFLICT OF INTEREST" appears BEFORE the chapter heading and is phrased as a meta-note to the reader (not the chapter body). This is a cleaning artifact / front-matter bleed. Then lines 15-17 repeat the same disclosure inside the chapter ("A note before we begin." then "A small disclosure before this chapter starts.") — two near-identical disclosure openings back-to-back. Recommend: delete the lines 1-7 pre-chapter note entirely, and collapse the two opening disclosure lines into one ("A small disclosure before we begin.").
- Ch6, line 33 — "His sister, Daniela Amodei, who had been OpenAI's Vice President of Operations." is a sentence fragment (no main verb). Reads fine in print but breaks mid-listen. Recommend: merge into prior sentence or rephrase as "His sister Daniela Amodei, OpenAI's Vice President of Operations, joined him."
- Ch7, line 17 — "Demis Hassabis ... won a Nobel Prize in 2024 for his work using AI to predict protein structures." Factually shaky as written: Hassabis shared the 2024 Nobel in Chemistry with John Jumper (and David Baker took the other half). Calling it "his work" without naming Jumper risks a fact-check ding. Recommend: "...shared a Nobel Prize in 2024 with John Jumper for AlphaFold..."
- Ch8, line 69 — "By November 2025, he had left Meta to found his own startup, Advanced Machine Intelligence Labs..." Conflicts with line 113 in the same chapter which calls it "AMI Labs" and refers to "his successor at AMI Labs" (LeCun is the founder, not someone with a successor at his own new lab). The "successor" framing is wrong. Recommend: rewrite line 113 to "expressed mostly by the now-departed LeCun, who is now at AMI Labs" or similar.
- Ch10, lines 47-49 — The xAI -> SpaceX acquisition / "SpaceXAI" rename is presented as fact. This is a bold, recent, easily-fact-checked claim. Confirm with Ziad that this reflects actual reporting as of May 2026, not a speculative scenario. If speculative, soften with "Reports in early 2026 suggested..."

---

## 06_chapter_06_clean.txt

- Lines 1-7 — Pre-chapter "NOTE ON CONFLICT OF INTEREST" block appears before the chapter heading; reads like a stray author-to-editor note that escaped cleaning. See BLOCKERS.
- Lines 15-17 — Two redundant disclosure openings ("A note before we begin." then "A small disclosure before this chapter starts.") — merge into one.
- Line 33 — "His sister, Daniela Amodei, who had been OpenAI's Vice President of Operations." — fragment, no verb. See BLOCKERS.
- Line 67 — "the UN Declaration of Human Rights" — actual title is "Universal Declaration of Human Rights." Recommend correction.
- Line 71 — "Claude 3. Claude 3.5. Claude 3.7." — skips Claude 4 / 4.5 / 4.6 / 4.7 which would be the actual 2025 lineup as of May 2026. Either expand the list or rephrase as "a series of increasingly capable models through Claude 3.5, 3.7, and successors" so it doesn't read as a complete enumeration.
- Line 83 — "from a few hundred million to thirty billion dollars. Eighty times the company's own internal forecasts." — second sentence is a fragment. Acceptable as stylistic punch but flag for narrator pacing.
- Line 85 — "a chatbot that you copy and pasted answers from" — tense slip; should be "copy and paste" (parallel with "read your files, ran your tests"). Actually the surrounding verbs are past tense, so "copied and pasted" is correct. Recommend: "copied and pasted."
- Line 97 — "approximately nine hundred billion dollars" / "slightly more than OpenAI" — fact-check: confirm OpenAI's May 2026 valuation is below $900B; recent reporting has put OpenAI at $500B+ with talks of higher.
- Line 103 — "Elon Musk's SpaceX for additional capacity" — surprising claim (SpaceX as compute provider). Confirm sourcing.
- Line 107 — "March 2026, the United States Pentagon designated Anthropic a supply chain risk and blacklisted the company from working with the military." Major and recent claim — confirm sourcing. Reads as a significant reversal worth more than one paragraph.
- Line 111 — "What ANTHROPIC actually believes." — heading capitalization inconsistent with sibling headings ("THE FOUNDING", "THE PRODUCTS"). Note that CB normalizes case so non-blocking, but visually inconsistent.
- Pronunciation watchpoints: Amodei (AM-uh-day vs ah-MOH-day-ee — confirm Ziad's preference); Anthropic (AN-throh-pik); Daniela; Dario; Jared Kaplan; "anthropos"; RLHF (probably read as letters); claude.ai (clawd-dot-A-I).
- Bridge line at end (line 139): "What comes next: Google DeepMind and the giant that almost lost the future." — present and good.

---

## 07_chapter_07_clean.txt

- Line 17 — Nobel Prize attribution incomplete. See BLOCKERS.
- Line 27 — "about six hundred and fifty million dollars" for DeepMind acquisition — widely reported figure was ~$500M-$650M depending on source; $650M is on the high end but defensible. Acceptable.
- Line 29 — "Mark Zuckerberg, at Facebook, had also tried to acquire DeepMind." — fine, but worth confirming "Facebook" vs "Meta" framing for a 2014 event (Facebook is correct for the era).
- Line 41 — "Concerns about brand safety. Concerns about... Concerns about... And honest concerns..." — four sentence fragments in a row. Stylistic but heavy on the ear. Consider folding into one sentence with semicolons or commas. Note: per CLAUDE.md, semicolons don't trigger CB pauses, so prefer commas with "and."
- Line 45 — "wiped one hundred billion dollars off Alphabet's stock value in a single day" — widely reported as ~$100B; acceptable. The Bard/Gemini rename happened in Feb 2024, so "rebranded it to 'Gemini' a year later" is correct (Bard launched March 2023, Gemini brand Feb 2024 — close to a year).
- Line 59 — "Gemini 2.5 shipped in March 2025" / "In November 2025, they launched Gemini 3" — confirm both dates. Gemini 2.5 was actually released in March 2025 (correct). Gemini 3 in November 2025 — confirm with Ziad; Google's roadmap had this slot but the exact month deserves a check.
- Line 63 — "over seven hundred and fifty million monthly active users" / "more than ten billion tokens per minute" / "nearly one hundred and fourteen billion dollars" — all big numbers, all worth a fact-check pass.
- Line 67 — "between one hundred and seventy-five and one hundred and eighty-five billion dollars" — heavy on the ear ("one hundred and..." three times in one sentence). Acceptable but pacing-heavy. Consider "between roughly $175 and $185 billion" — though numerals would be expanded by CB anyway. Leave as-is unless re-read confirms it drags.
- Line 75 — "Isomorphic Labs, which is Hassabis's drug discovery spinoff" — Isomorphic was launched in 2021, not strictly a "spinoff" of DeepMind in the classic sense (it's a sister Alphabet company). Minor framing nit.
- Line 87 — "diminishing returns from pure scaling" / "one or two more breakthroughs" — Hassabis-style quote. Confirm it's accurate to public statements.
- Line 89 — "Veo and Genie" — both real Google products. Pronunciation watchpoint: Veo (VAY-oh), Genie (JEE-nee).
- Line 93 — "no plans" — quoted phrase but no quotation marks; intentional per Ziad's narration style. OK.
- Pronunciation watchpoints: Hassabis (huh-SAH-bis); Demis (DEM-is); AlphaGo (AL-fuh-go), AlphaZero, AlphaFold; shogi (SHOH-ghee); TPU (read as letters); Mountain View; Veo; Genie; Isomorphic.
- Bridge line at end (line 115): "What comes next: Meta and the open-weight bet that changed everything." — present and good.

---

## 08_chapter_08_clean.txt

- Line 17 — "By making the models freely available, Meta would commoditize the layer..." — clean, but worth noting "commoditize" is sometimes a CB watchpoint (kuh-MAH-dih-tize).
- Line 19 — "Llama series, released in versions 1 through 3" — fine. Pronunciation note: "Llama" is LAH-muh per Meta, not YAH-muh (Spanish) and not LAM-uh.
- Line 41 — "In February 2023, Meta released a model called Llama. Initially it was research-only..." Then "in July 2023, they officially released Llama 2 with a permissive license, free for commercial use except by the largest companies. In April 2024, Llama 3." — last bit is a fragment ("In April 2024, Llama 3."). Acceptable as stylistic punch but flag.
- Line 53 — Heading "The llama 4 disaster." — lowercase "llama" inside running heading; brand convention is "Llama". Cosmetic only.
- Line 63 — "In an interview with the Financial Times, LeCun said the team had 'fudged a little bit'" — quote attribution. Confirm this is a real quote from LeCun in FT. If accurate, fine. If paraphrased, soften.
- Line 67 — "Mark Zuckerberg, according to reports from people inside the company, lost confidence in the team that had produced Llama 4." — uses anonymous-source framing without naming the outlet. Consider citing the publication for credibility.
- Line 69 — "Advanced Machine Intelligence Labs" — verify the actual name of LeCun's startup. Reporting as of late 2025/early 2026 has used variants. Worth a check.
- Line 75 — "He spent fourteen and a half billion dollars to acquire forty-nine percent of Scale AI" — widely reported figure. Acceptable.
- Line 77 — "The aging Turing Award winner Yann LeCun, on paper at least, reported to a twenty-eight-year-old executive." — "aging" feels editorial and slightly unkind for a chapter that aims for fairness. LeCun is in his 60s, not "aging" in the geriatric sense. Recommend: "The 65-year-old Turing Award winner..." or just "Turing Award winner Yann LeCun..."
- Line 81 — "Muse Spark" — confirm this is the actual name of Meta's post-Llama 4 model. If invented for the book, flag. (As of public reporting through 2026, no such model has been confirmed under that name.)
- Line 83-89 — Whole "Muse Spark was not open-weight" passage hinges on the model being real. See above.
- Line 95 — "between one hundred and fifteen and one hundred and thirty-five billion dollars" — pacing-heavy phrasing again. Acceptable.
- Line 113 — "his successor at AMI Labs" — wrong; LeCun founded AMI. See BLOCKERS.
- Line 119 — "you interact with Meta's AI hundreds of times a day" — strong claim, but fine for the audience.
- Pronunciation watchpoints: Llama (LAH-muh); LeCun (luh-KUHN); Zuckerberg; Yann (YAHN); Alexandr Wang (al-ex-AHN-der WAHNG — Russian-style first name); Threads; FAIR (read as a word, "fair", or as letters?); Mistral; Qwen (CHWEN or KWEN); DeepSeek; Veo; Muse Spark.
- Bridge line at end (line 131): "What comes next: the Chinese frontier and the AI race the West almost missed." — present and good.

---

## 09_chapter_09_clean.txt

- Line 11 — "A small American technology stock called Nvidia" — sarcastic / ironic phrasing (Nvidia is one of the largest companies on Earth). Intentional and works on the page but may sound flat read straight. Consider tonal cue or mark for narrator emphasis.
- Line 15 — "trained for about six million dollars" — DeepSeek's $6M figure was for the final training run only and is widely contested. Recommend: "...for a final training run reportedly costing about six million dollars..." to head off "actually it was way more" criticism.
- Line 21 — "I have not lived there. My information comes from public sources..." — humility frame, good.
- Line 29 — "since October 2022, the United States has been actively trying to slow Chinese AI development." — first export controls were October 2022, correct. Good.
- Line 43 — "Their V4 model, released in April 2026, comes in two versions, including a 1.6 trillion parameter variant" — confirm DeepSeek V4 details with Ziad. As of public knowledge, DeepSeek's most recent named release was V3.1 / V3.2 territory; "V4" with 1.6T params is a forward claim worth verification.
- Line 47 — "Their Kimi K2.6 model, released in April 2026" — same flag. Kimi K2 was real (mid-2025), K2.6 in April 2026 is a specific recent claim. Verify.
- Line 49 — "China's first publicly listed AI company" (Zhipu) — Zhipu's IPO was approved/in-progress in 2025. Confirm "first publicly listed" framing is accurate.
- Line 55 — "over one hundred and forty million dollars in cash bonuses through their AI chatbot during the 2026 Lunar New Year" — Tencent's red-envelope-via-Yuanbao campaign is reportable. Confirm dollar figure.
- Line 57 — "MiniMax, 01.AI, StepFun" — pronunciation: "01.AI" should be "Zero-One AI" or "oh-one dot AI"; flag for substitution because CB will likely read "01" as "one".
- Line 63 — "Multi-Head Latent Attention" — capitalized term, fine.
- Line 69 — "DeepSeek V4 Flash, released in April 2026, costs twenty-eight cents per million output tokens" — same V4 verification flag.
- Line 71 — "Huawei Ascend chips" — pronunciation: Huawei (HWAH-way commonly, or hoo-AH-way); Ascend (uh-SEND).
- Line 77 — "the 1989 events at Tiananmen Square" — Tiananmen pronunciation: tee-EN-an-men or tyen-AHN-men. Worth flagging for narrator.
- Line 99 — "instruments of national strategy" — used twice in adjacent paragraphs (re: Chinese AI then American AI). Intentional symmetry. OK.
- Line 107 — "DeepSeek usage in Africa is, by some estimates, two to four times higher than in other regions" — soft claim, "by some estimates" is good hedge. OK.
- Line 111 — "OpenAI, Anthropic, Google, Meta, and the Chinese frontier" then mentions "xAI, Mistral, Cohere, Inflection. They matter too." — fine teaser for chapter 10.
- Line 113 — "The Transformer architecture. The next-word predictor. Scaled up. Trained on enormous data. Aligned through some combination of human feedback and explicit principles. Deployed as products with system prompts and safety classifiers." — six fragments in a row. Heavy stylistic choice, may sound staccato over CB pacing. Consider folding the last 3-4 into one sentence.
- Pronunciation watchpoints (HEAVY on this chapter): DeepSeek (DEEP-seek); Qwen (likely CHWEN per Alibaba's own pronunciation guidance, not KWEN); Alibaba (ah-lee-BAH-bah); Moonshot AI; Kimi (KEE-mee); Tsinghua (CHING-hwah, NOT TSING-hua); Zhipu (JEE-poo or JR-poo); ByteDance (BITE-dance); Doubao (DOH-bow); Baidu (BYE-doo); ERNIE (read as a word, "Ernie"); Tencent (TEN-cent); WeChat; MiniMax; 01.AI (substitute "Zero-One AI"); StepFun; Yann LeCun; Demis Hassabis; Huawei (HWAH-way); Ascend; Tiananmen; Hassabis; High-Flyer; AlphaFold; Nvidia (en-VID-ee-uh); HIPAA (HIP-uh); GDPR (read as letters).
- Bridge line at end (line 121): "What comes next: what AI is genuinely good at, with examples." — but this duplicates the Chapter 10 bridge. Chapter 9 should bridge into Chapter 10 ("Everyone Else"), not jump to Part Four. RECOMMEND FIX: rewrite to something like "What comes next: the other half of the industry — Microsoft, xAI, Mistral, Apple, and the wrapper companies you already use." This is a real continuity issue because Ch10 also ends with the Part Four bridge.

---

## 10_chapter_10_clean.txt

- Lines 47-49 — SpaceX acquires xAI / "SpaceXAI" rename. See BLOCKERS.
- Line 23 — "the AI thing in Windows" / "the AI thing in Word" / "the AI thing in GitHub" — colloquial parallel structure. Good.
- Line 33 — "Microsoft has invested over thirteen billion dollars in OpenAI" — figure is widely reported as $13B+. Acceptable.
- Line 35 — "Mustafa Suleyman (the cofounder of Google DeepMind and later founder of Inflection)" — Suleyman cofounded DeepMind (correct), then Inflection (correct). Good. Note: parenthetical might read awkwardly; consider em-dash equivalent or comma since CB ignores parens-as-pause anyway. Actually CB will just read the inner text continuously, which is fine.
- Line 35 — "MAI" — pronunciation: read as letters "M-A-I" or as "may"? Microsoft uses "MAI" pronounced as letters. Flag for narrator.
- Line 41 — "He recruited eleven researchers from Google, DeepMind, OpenAI, and Microsoft." — minor: Google and DeepMind are the same company (since 2014/2023 merger). Recommend: "from Google DeepMind, OpenAI, and Microsoft" or "from Google, OpenAI, and Microsoft."
- Line 43 — "modeled, by Musk's own description, on the irreverent voice of Douglas Adams's 'The Hitchhiker's Guide to the Galaxy.'" — punctuation: Adams's vs Adams' (style choice, fine). Title in quotes — CB will read the quote marks as nothing, fine.
- Line 45 — "By 2024, Musk had built a supercomputer called Colossus in Memphis, Tennessee, with two hundred thousand GPUs." — Colossus came online late 2024 with ~100K GPUs initially, expanded to 200K+ in 2025. The "By 2024" timing slightly compresses the actual rollout. Minor.
- Line 47 — "In March 2025, Musk announced that xAI was acquiring X... for thirty-three billion dollars in stock." — actual deal was announced March 2025, valued xAI at $80B and X at $33B. The way this is written reads cleanly as "$33B in stock" which matches the X valuation. Acceptable.
- Line 51 — "civilize space and free humanity from various restrictions" — vague phrasing. "Various restrictions" is hand-wavy. Consider sharper or cut.
- Line 63 — "annual recurring revenue grew from twenty million dollars in early 2025 to four hundred million dollars in early 2026" — Mistral revenue figures, verify.
- Line 63 — "raised eight hundred and thirty million dollars" — verify; Mistral raised ~€600M Series B in 2024 ($640M-ish), then larger rounds. $830M is plausible for a 2025/2026 round but verify.
- Line 63 — "Voxtral, a voice generation system" — Voxtral is real (Mistral's speech model, 2025). Good.
- Line 65 — "discussions with xAI about possible collaboration" — vague and forward-looking. Consider sourcing or hedge harder.
- Line 73 — "Sometimes OpenAI. Sometimes Anthropic. Sometimes Mistral." — fragment trio. Stylistic, OK.
- Line 77 — "Cursor, the AI coding tool. Granola, the AI meeting notes app. Lindy, the AI workflow builder." — pronunciation watchpoints; all three are real companies. Granola (gruh-NOH-luh); Lindy (LIN-dee).
- Line 89 — "AI21 Labs, Cohere, Stability, Mistral" — AI21 pronunciation: "A-I twenty-one." Flag for substitution.
- Line 91 — "Amazon's biggest single AI bet has been on Anthropic. They have committed up to twenty-five billion dollars" — matches Ch6 figure. Consistent.
- Line 101 — "In June 2024, they announced 'Apple Intelligence,'" — correct (WWDC 2024).
- Line 103 — "They have licensed external models, including Gemini from Google" — confirm; Apple+Google Gemini integration was reported as in talks/negotiation; whether it actually shipped by May 2026 deserves verification.
- Line 113 — "Aidan Gomez, one of the eight authors of the original Transformer paper at Google" — correct.
- Line 115 — "In March 2024, Microsoft executed an unusual deal in which they hired most of Inflection's team and licensed the technology" — correct (March 2024 Inflection-Microsoft deal).
- Line 117 — "Their Watson product, which won Jeopardy in 2011" — correct year.
- Line 119 — "Hugging Face is technically not an AI lab. It is the platform where open-weight models live." — fair characterization. Pronunciation: Hugging Face read straight, fine.
- Line 121 — "Stability AI, who built Stable Diffusion. Black Forest Labs, who built Flux. Runway, who is leading on AI video. Suno, on AI music. ElevenLabs, on voice." — "who" should be "which" for companies (grammar nit; spoken English is forgiving here). OK to leave.
- Line 141 — "Welcome, properly this time, to Part Four." — references Ch9's "Welcome to Part Four" line. Self-aware joke. Works if Ch9 keeps that phrasing; otherwise cut. See Ch9 bridge issue above.
- Pronunciation watchpoints: xAI (read as "X-A-I" letters? or "X-A-I" as one word? confirm); Grok (rhymes with "rock"); Colossus (kuh-LOS-us); Mistral (mis-TRAHL or MIS-trul — French pronunciation typically mis-TRAHL); Le Chat (luh SHAH); Voxtral (VOX-trahl); Mustafa Suleyman (moo-STAH-fah SOO-lay-man); Aidan Gomez (AY-den GOH-mez); Mustafa; Inflection's "Pi" (read as the letter, "pie"); Granola; Lindy; Hugging Face; Cohere (koh-HEER); Suno (SOO-noh); ElevenLabs; AI21 ("A-I twenty-one"); MAI (letters); Bedrock; Titan; Nova; Alexa; Siri; WWDC.
- Bridge line at end (line 143): "What comes next: what AI is genuinely good at, with examples." — present and good. (Note: same line as Ch9's bridge — see Ch9 finding.)

---

## Cross-chapter notes

- **Number-spelling consistency**: Across all five chapters, numbers are spelled out ("nine hundred billion dollars", "one hundred and fourteen billion dollars"). Consistent. CB handles this fine but compound multi-clause numbers ("between one hundred and seventy-five and one hundred and eighty-five billion dollars") get pacing-heavy. Consider abbreviating where prose gets unwieldy.
- **Fragment style**: Ziad uses sentence fragments as stylistic punches throughout ("Real story. Real complications. Honest assessment."). Works on the page; lands as staccato over CB. Not an error, just a pacing thing for narrator delivery — Burton handles it OK at his measured cadence but flag for awareness.
- **Chapter-end bridge duplication**: Ch9 and Ch10 both end with "What comes next: what AI is genuinely good at, with examples." Ch9 should bridge into Ch10, not skip ahead. See Ch9 finding.
- **Fact-check pass needed**: Chapters 6-10 are heavy on company-specific recent facts (valuations, product launch dates, leadership moves, M&A). Many of these are plausible but specific enough to need verification before publication. Highest-risk items flagged inline; suggest a dedicated fact-check pass against May 2026 reporting before final render.
- **Pronunciation lexicon**: Chinese names in Ch9 are the densest pronunciation risk in the book so far. Recommend building a per-book pronunciation substitution dict (in `generate.py` text preprocessing) for: Tsinghua, Qwen, Zhipu, Doubao, Tiananmen, Huawei, 01.AI, and the Amodei surname.
