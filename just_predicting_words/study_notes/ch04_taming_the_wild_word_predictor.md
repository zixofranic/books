# Chapter 4 — Taming the Wild Word Predictor

**Version:** v1 · **Last updated:** 2026-05-30 · **Source:** *Just Predicting Words*, Ch4

---

## The problem after pre-training

A model fresh out of pre-training is a raw next-token predictor. It does not know what a conversation is. It does not know what a "user" is. It does not know it is supposed to be helpful, honest, or harmless. Given the right prompt it will produce racist text, instructions for harm, conspiracy theories, sexually explicit content, or any other pattern present in the training data, because the training data contained all of those patterns.

Turning that raw model into something safe and useful for ordinary users is the work of the alignment phase. Three techniques do most of the work: instruction tuning, reinforcement learning from human feedback, and Constitutional AI.

## Instruction tuning

The first step is to show the model examples of being helpful. Human contractors write thousands of example exchanges — a request and an ideal response. The model is fine-tuned on these examples. After this fine-tuning, the model has a sense that when it sees a question-shaped input it should produce an answer-shaped output. It now behaves like an assistant rather than a generic text continuation engine.

Instruction tuning alone is enough to produce a basically functional chatbot. It is not enough to produce a safe or carefully-behaved one.

## Reinforcement Learning from Human Feedback (RLHF)

RLHF is the technique that shaped raw word predictors into the polished assistants we use today. The training method:

1. The model produces several different responses to the same prompt.
2. Human raters rank the responses from best to worst.
3. The model is updated to make highly-ranked responses more likely and low-ranked responses less likely.
4. Repeat across millions of prompts.

Over millions of these comparisons, the model learns to produce the kind of response humans prefer. This is where it picks up tone, friendliness, format conventions, the habit of declining to help with abusive requests, and many other behaviors.

RLHF has a known side effect: sycophancy. Humans, on average, prefer responses that agree with them, that compliment them, and that don't push back too hard. The model picks up a subtle bias toward telling you what you want to hear. We come back to this failure mode in chapter twelve.

## Constitutional AI

Constitutional AI is Anthropic's variant on the same idea. Instead of relying entirely on direct human feedback for every behavior, Anthropic gives the model a written set of principles — its "constitution." The model is then trained to critique and revise its own outputs against the principles, with humans involved in the loop more sparingly.

The advantages, as Anthropic argues them: explicit principles can be audited, debated, and changed; the model can be trained on a much larger scale because humans don't have to grade every output; and the principles can address subtle behaviors (such as how to handle dual-use information requests) that are hard to capture in single-example comparisons.

Other major labs use a mix of RLHF and constitutional-style techniques. The boundary has blurred over time.

## The "helpful, honest, harmless" frame

The explicit alignment goal at most major labs is for the assistant to be helpful, honest, and harmless. The triad is often abbreviated HHH. The three are in real tension: a fully harmless model would refuse most requests; a fully helpful model would explain how to do dangerous things; an honest model has to admit when it doesn't know something, which is sometimes unhelpful. Labs spend most of their alignment effort negotiating these trade-offs.

## The system prompt

Once the model is deployed as a product, every conversation starts with a hidden block of text called the system prompt, prepended to the conversation before the model sees it. The system prompt is where the company tells the model what kind of assistant to be — tone, topics to avoid, format of responses, legal disclaimers, the model's persona, the rules for handling sensitive topics. For a consumer chatbot like ChatGPT or Claude, the system prompt is typically several thousand words.

The system prompt is the fastest-moving part of the defense system around a model. It can be changed without retraining, so labs can respond to new failure modes within hours. It is also one of the most fragile parts: clever users can sometimes get the model to ignore its system prompt through carefully designed inputs, an attack family known as prompt injection.

## What you actually talk to

When you use a frontier AI product, you are talking to a model that has been pre-trained on the internet, instruction-tuned on examples, refined through RLHF or Constitutional AI, given a system prompt by the company, and wrapped in additional safety classifiers that watch the conversation. The assistant you experience is the cumulative product of all of those layers. We come back to the defensive stack in chapter sixteen.
