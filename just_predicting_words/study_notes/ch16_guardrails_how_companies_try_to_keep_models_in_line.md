# Chapter 16 — Guardrails, How Companies Try to Keep Models in Line

**Version:** v1 · **Last updated:** 2026-05-30 · **Source:** *Just Predicting Words*, Ch16

---

## The defensive stack

Every AI company knows their untamed models would do things users do not want. This chapter describes the layered defenses they use to manage that, and where the stack holds versus where it leaks. Seven layers, in roughly the order they kick in.

## Layer 1: Training the model to be helpful

Where the work starts, covered in chapter four. The raw post-pretraining model is a wild word predictor — does not know it's in a conversation, does not know what a user is. Instruction tuning shows it examples of helpful responses. RLHF shapes its preferences. Constitutional AI gives it written principles. By the time the model reaches you, it has been shaped, layer on layer, into something that defaults to helpful, honest, harmless. The explicit goal at most major labs is the H-H-H triad.

This first layer does most of the work. The vast majority of user interactions — billions per day — run fine with no further intervention.

## Layer 2: The system prompt

Every conversation begins with a hidden block of text prepended before the model sees the user's input. The system prompt tells the model what kind of assistant to be — tone, topics to avoid, format of responses, the model's persona, the rules for sensitive topics. For consumer chatbots, the system prompt typically runs several thousand words. For enterprise deployments, it can be further customized ("never discuss specific account balances," "include the regulatory disclaimer," etc.).

The system prompt is the fastest-moving part of the defense — it can be changed without retraining, so labs can respond to new failure modes within hours. It is also one of the most fragile parts. Users have learned they can sometimes coax models into ignoring system prompts through clever phrasing — a family of attacks called prompt injection. The 2026 generation of attacks is sophisticated: hidden instructions buried in documents the model reads, encoded text the model interprets but humans cannot easily see, multi-step conversations that gradually erode adherence.

## Layer 3: Input and output classifiers

A second set of models watches the conversation in real time, separate from the main model, looking for content to block or modify.

- **Input classifiers** examine what the user typed before it reaches the main model. If the input matches patterns associated with abuse, manipulation, or harmful intent, the system can refuse to process it.
- **Output classifiers** examine what the model is about to produce before it reaches the user. If the response contains certain patterns, it gets modified or replaced.

The user usually does not see these classifiers — only the refusal triggered by them.

The trouble: the classifiers are themselves AI models, susceptible to the same kinds of confusion that affect the main model. In October 2025, researchers at a security firm called HiddenLayer demonstrated that OpenAI's Guardrails framework could be bypassed using straightforward techniques. The reason was structural — the classifier judging the content was itself a language model, vulnerable to the same manipulation.

Classifiers help. They do not solve the problem. They are filters, not walls.

## Layer 4: Red teaming

Before a model is released, the company tries to break it on purpose. Red teamers (the term comes from military exercises) are paid to find every way the model can be made to misbehave. They try every prompt injection technique. They probe every edge case. They roleplay every adversarial scenario.

When red teamers find a problem, the company patches it through additional training, new classifier rules, or system-prompt changes. Then the red teamers try again. Major labs run substantial internal red teams, hire external researchers, and invite the broader security community via bug bounty programs.

The structural problem: red teamers try to find every problem. Attackers in the real world only need to find one. The asymmetry favors attackers.

A 2026 industry survey on jailbreak defenses put the situation bluntly. Advanced attacks routinely achieve ninety to ninety-nine percent success rates on open-weight models and eighty to ninety-four percent on proprietary ones. Defenses raise the cost of unsophisticated attacks. They do not hold against motivated adversaries.

## Layer 5: Refusal training

Modern models are trained to refuse certain requests. The categories vary by company but generally include: direct help with violence against specific people; creating bioweapons or chemical weapons; sexual content involving minors; specific instructions for self-harm or suicide; detailed instructions for major cyberattacks; producing content designed to manipulate elections through impersonation; helping stalk or harass specific individuals.

These refusals generally work. The major models reliably decline these categories. When they fail to decline, the failure usually involves a sophisticated attempt to disguise the request, and even those usually fail.

The trouble: refusal training is often over-applied. Legitimate uses get caught alongside actual abuse. Medical professionals asking about drug interactions get treated like patients seeking self-harm. Security researchers asking about vulnerabilities get treated like attackers. Writers helping with morally complex fiction get treated as malicious.

For users: refusals are not always the model's deep conviction. They are sometimes the company's risk management bumping up against your request. Rephrasing usually works; trying a different assistant sometimes works better.

## Layer 6: Monitoring and iteration

Once a model is deployed, the company watches what it is doing. Every major lab runs telemetry on the platform — not the contents of every conversation, but enough to understand patterns. Which categories of queries are growing. Which kinds of refusals are happening. Which novel attack patterns are emerging.

When something new shows up, the company responds. New attack patterns get added to training. New abuse categories get added to classifiers. New refusal patterns get tuned. The model in production today is meaningfully different from the model six months ago, even if the weights have not changed.

The privacy cost is the trade-off (chapter fourteen risk four). The monitoring requires data. Data is sensitive. Different companies strike different balances.

## Layer 7: Third-party infrastructure

Beyond what the labs do, an entire industry has emerged adding more safety layers on top. Companies deploying AI in regulated industries add their own guardrail systems. Specialized vendors sell input/output filters for sensitive data, prompt injection, jailbreak attempts, and content violating industry rules. AWS has Bedrock Guardrails. Azure has Content Safety. Smaller vendors fill gaps in healthcare, finance, education.

In enterprise contexts, this is often where the most aggressive safety work happens. A bank using AI for customer service wraps the lab's model in PII detection, domain-specific filters, legal compliance checks, audit logging, and human review for high-stakes outputs. The lab's model is the engine; the enterprise's safety stack is the brake system.

For consumer users, the third-party layer is mostly invisible.

## Where the whole system fails

Four failure modes:

1. **Sophisticated adversaries.** Motivated, time-rich attackers chaining multiple techniques across long conversations will usually succeed. Princeton researchers showed in 2026 that safety alignment can be degraded with as few as one hundred fine-tuning examples on otherwise benign data. The safety is not a separate module — it is distributed across parameters and can be eroded.
2. **Open-weight models.** Once weights are public, anyone can download and run them without the safety infrastructure. Safety becomes a property of how you deploy the model, not of the model itself.
3. **Indirect injection.** A model that reads documents on your behalf can be manipulated by content inside those documents — hidden instructions in white-on-white text in an email, prompt injections in a shared document. As AI gets more agentic across more data sources, this attack surface grows.
4. **Alignment of the company itself.** The system is only as good as the values of the people designing it. If a company relaxes constraints to compete, the system relaxes. If a company decides certain categories are inconvenient, those categories shift.

## The author's takeaway

Two things: the safety system is doing a lot of work — most users, most of the time, are better protected than they realize. And the safety system is not a wall — it is overlapping filters, each imperfect, that together raise the cost of misuse without making it impossible.

The author's analogy: cars have brakes, traffic laws, license requirements, vehicle inspections, and law enforcement. People still die on the roads. The expectation that AI safety should be perfect in a way no other technology has ever achieved is unrealistic. The expectation that AI safety should be serious, well-funded, transparent, and continuously improving is reasonable, and most major labs in 2026 are meeting that second standard with varying degrees of success.

## What to remember about Chapter 16 in one paragraph

Seven layers of AI safety: training (instruction tuning, RLHF, Constitutional AI for HHH); system prompt (fast to change, fragile to prompt injection); input/output classifiers (HiddenLayer bypassed OpenAI Guardrails October 2025); red teaming (defenders find every flaw, attackers need find only one — eighty to ninety-nine percent jailbreak success rates); refusal training (works on the big categories, over-applies to legitimate uses); monitoring (continuous, with privacy cost); third-party guardrails (AWS Bedrock Guardrails, Azure Content Safety, enterprise stacks). Failures: sophisticated adversaries; open-weight models lack the stack; indirect injection via documents the model reads; the company's own alignment can drift. Princeton 2026: safety alignment can be degraded with one hundred fine-tuning examples. Filters, not walls.
