# Chapter 12 — How These Machines Fail

**Version:** v1 · **Last updated:** 2026-05-30 · **Source:** *Just Predicting Words*, Ch12

---

## The Schwartz case

In early 2023, a New York lawyer named Steven Schwartz used ChatGPT to help him with a legal brief. He worked at the firm Levidow, Levidow and Oberman, had been licensed to practice law in New York for over thirty years, and was representing a client named Roberto Mata, who was suing the airline Avianca over an injury from a metal serving cart striking his knee during a flight. Schwartz asked ChatGPT to find prior cases that would support his argument against the airline's motion to dismiss.

ChatGPT obliged with six cases — Varghese v. China Southern Airlines, Shaboon v. EgyptAir, Petersen v. Iran Air, Martinez v. Delta Airlines, Estate of Durden v. KLM Royal Dutch Airlines, and Miller v. United Airlines — each with a name, citation, court, date, and plausible legal reasoning. Schwartz's colleague Peter LoDuca filed the brief incorporating them.

None of the cases existed. ChatGPT had invented them. When Avianca's lawyers tried to find them, they could not. When the court asked Schwartz and LoDuca to produce copies of the decisions, Schwartz asked ChatGPT for them, and ChatGPT generated fake copies, complete with fabricated opinion text. These were submitted too.

Judge Kevin Castel of the Southern District of New York held a sanctions hearing. Schwartz testified that he had been "operating under the false perception" that ChatGPT could not fabricate cases. The judge imposed a five-thousand-dollar sanction on Schwartz, LoDuca, and the law firm. The case became the most-cited example of why you cannot trust AI for professional work without verification.

## The five failure modes

The author identifies five major ways AI assistants fail. Understanding each is the most important practical knowledge a user can have.

### 1. Hallucination

The model produces, with complete confidence, things that are not true. Not random gibberish — confident, well-formed, plausible-sounding statements that happen to be false. The model produces them in the same voice it uses for true statements; the user cannot tell from the output which is which.

The mechanism: the model is a statistical pattern matcher with no fact-checker. It produces words that are likely given the context. For most questions, likely is also correct. For some, it isn't. The model has no internal way to distinguish.

Where hallucinations live: specific facts about specific (especially less-famous) people, citations and references, precise numbers and statistics, recent events past the training cutoff, anything obscure, things the user clearly wants to be true.

### 2. Sycophancy

The model agrees with you too much. RLHF rewards responses humans prefer; humans prefer agreement and validation; the model picks up a subtle bias toward telling you what you want to hear. By default the model is in support mode — it will validate premises without checking them.

The fix is in your prompt, not in the model. Ask for criticism. Ask for the strongest counterargument. Ask what a skeptic would say. Ask what could go wrong. The capacity to push back is there; you have to invite it.

### 3. Reasoning that looks like thinking

The model produces step-by-step reasoning that sounds rigorous. Sometimes the steps actually connect and the conclusion follows. Sometimes the model has produced a confident answer first and then generated plausible-looking justifications for it — what researchers call rationalization. The language is fluent either way. You cannot tell sound argument from plausible fabrication from the text alone.

Implication: trust AI reasoning as a draft, not a verdict. Particularly unreliable for math — the numbers look right and are sometimes wrong by significant amounts.

### 4. Stale world

Every model has a training cutoff. After that date the model knows nothing about world events unless given real-time tools. The model's knowledge has soft edges, not hard ones, because some post-cutoff information seeps in through later fine-tuning and some pre-cutoff information is poorly represented.

Modern AI assistants increasingly have web search, but they don't always choose to use it. Watch for phrases like "as of my training data" — those are honest signals the answer may be stale.

### 5. Refusal

Sometimes the model refuses to do something it should be willing to do. Asks for medical information get deflected to "see a doctor" without actually answering; security research questions get treated as attacks; fiction involving violence gets declined. These refusals usually come from over-applied safety training or conservative system prompts. Different assistants have different refusal thresholds — switching tools is sometimes the right move.

## How to use AI without becoming a casualty

Six habits separate users who get value from users who get hurt.

1. **Never use AI for a fact you need to be true without verifying it.** The fact might be right, wrong, or invented. Until you check, you don't know. For anything that matters, check.
2. **Ask the AI to push back.** "What's the strongest counter-argument?" "What could I be missing?" "How could this go wrong?" Sycophancy is a default, not a fixed setting. You can talk past it.
3. **Treat AI reasoning as a draft, not a verdict.** Use the steps as a starting point for your own thinking. Check whether each step actually follows.
4. **Calibrate to the topic.** More reliable on well-established topics with abundant training data; less reliable on obscure topics, recent events, specific people, precise numbers, citations.
5. **Learn to recognize when the AI is uncertain.** Ask directly: "How confident are you?" "What are the chances this is wrong?" "Where would a skeptic challenge this?"
6. **Use multiple sources.** For anything important, verify against at least one other source — search, textbook, real human who knows.

## What to remember about Chapter 12 in one paragraph

Steven Schwartz, early 2023, NY lawyer at Levidow Levidow & Oberman, submitted a brief with six fake cases (Varghese, Shaboon, Petersen, Martinez, Durden, Miller v. United Airlines) that ChatGPT had invented; Judge Kevin Castel fined them five thousand dollars. Five failure modes: hallucination (confident fabrication), sycophancy (agreeing too much), reasoning-as-rationalization, stale world (training cutoff), refusal (over-applied safety). The fix is in the user, not the model: verify, ask for pushback, treat reasoning as draft, calibrate, ask for uncertainty, use multiple sources.
