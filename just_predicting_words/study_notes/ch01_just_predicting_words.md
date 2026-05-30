# Chapter 1 — Just Predicting Words

**Version:** v1 · **Last updated:** 2026-05-30 · **Source:** *Just Predicting Words*, Ch1
**Subtitle in print:** *The whole trick is small. The world it built is not.*

---

## The launch

ChatGPT launched on November 30, 2022. The company behind it was OpenAI, a San Francisco AI lab. The product was a simple chat interface sitting on top of a fine-tuned version of an existing language model called GPT-3.5. It was not announced as a major release. Internally, it was described as a low-key research preview.

Within five days, ChatGPT had one million users. Within two months, it had a hundred million. At the time, it was the fastest-growing consumer product in history — faster than Facebook, faster than TikTok, faster than the iPhone. Within a few weeks of launch, it had quietly entered the daily routines of writers, programmers, teachers, lawyers, doctors, and ordinary users who had never tried any AI tool before in their lives.

## The mechanism

The technology underneath ChatGPT, despite the apparent intelligence of its outputs, is doing one specific thing: predicting the next word in a sequence. Given everything written so far, the model assigns a probability to every possible next word, picks one, and continues. Then it does the same thing again with the new word included in the context. It produces text one token at a time, left to right, by repeatedly answering the question: what word comes next.

This is the central claim of the book and the source of its title. Modern AI assistants are next-word predictors. The trick is small. What emerges from it is not.

## Why this matters as framing

Most discussion of AI either over-mystifies the technology (treating it as a conscious mind) or dismisses it (calling it autocomplete). The next-word-prediction framing is meant to do neither. It is meant to be honest about the mechanism — really, the model is just predicting words — while leaving room for the fact that doing this at sufficient scale, on sufficient data, with the right architecture, produces capabilities that look qualitatively new.

The author's stance: AI assistants are genuinely useful, genuinely limited, and the user who understands how they actually work makes better decisions than the user who treats them as magic or as a toy.

## What the book covers (preview)

The book is structured in roughly six parts:

- Part 1 (Chapters 1–4): how the technology actually works — tokens, embeddings, the Transformer architecture, attention, training, and the alignment techniques that shape raw word predictors into helpful assistants.
- Part 2 (Chapters 5–10): the companies — OpenAI, Anthropic, Google, Meta, the Chinese labs (DeepSeek, Qwen, Kimi, others), and the rest of the ecosystem (Microsoft, xAI, Mistral, Perplexity, Amazon, Apple).
- Part 3 (Chapters 11–13): what AI is genuinely good at, how it fails, and the structural limits of language as a medium.
- Part 4 (Chapters 14–17): real risks, hyped risks, the guardrails companies use, and the regulatory landscape (EU AI Act, US patchwork, China's state framework).
- Part 5 (Chapters 18–20): how to use AI well, how to handle it at work, how to talk to your kids about it.
- Part 6 (Chapter 21): where this is going, and what to do given the uncertainty.

The book was written through May 2026 and reflects the state of the field at that moment.
