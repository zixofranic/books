# Chapter 2 — A Short History of Machines That Read

**Version:** v1 · **Last updated:** 2026-05-30 · **Source:** *Just Predicting Words*, Ch2

---

## Distributional semantics

The intellectual ancestor of modern language AI is an idea from 1950s linguistics: words get their meaning from the company they keep. The slogan version was coined by the British linguist John Rupert Firth: "You shall know a word by the company it keeps." For decades this was just an observation. It became useful only when somebody figured out how to compute with it.

## word2vec, 2013

The breakthrough came in 2013. A researcher at Google named Tomas Mikolov, with colleagues, built a tool called word2vec. It read enormous amounts of text and learned, for every word, a list of about three hundred numbers — a vector — that captured the word's "company" in the corpus. Words that appeared in similar contexts ended up with similar vectors.

The striking demonstration was that the vectors did arithmetic. You could take the vector for "king," subtract "man," add "woman," and get something extremely close to "queen." You could take Paris minus France plus Germany and get Berlin. The system had learned the concept of gender, and the concept of "capital of," without ever being told these things existed. It had extracted meaning from raw text, at scale, for the first time in any machine.

The limit of word2vec was that it knew about words but not sentences. It could tell you that "dog" and "puppy" were similar. It could not tell you what "the dog chased its tail" meant, or how meaning depended on word order.

## The Transformer, 2017

The architecture that made sentences tractable was published in June 2017 in a paper called "Attention Is All You Need." It came out of Google. There were eight authors. The architecture they introduced — the Transformer — is the basis for essentially every modern large language model. ChatGPT, Claude, Gemini, Llama, DeepSeek, Qwen — all Transformers.

Within the next eight years, all eight of those Google researchers had left Google. They founded or led other AI organizations. Aidan Gomez went on to co-found Cohere. Others ended up at OpenAI, Anthropic, and various startups. Google had invented the architecture that now powers most of the modern AI industry and then watched a generation of competitors build on it.

## The GPT line, 2018–2020

OpenAI built on the Transformer. The pattern was to take the architecture and scale it up — more parameters, more data, more compute. The GPT name stands for Generative Pre-trained Transformer.

- GPT-1, released 2018, had one hundred and seventeen million parameters. It was a research curiosity.
- GPT-2, released 2019, had one and a half billion parameters. OpenAI initially withheld it, calling it "too dangerous to release." They eventually released it in November 2019.
- GPT-3, released 2020, had one hundred and seventy-five billion parameters. It was the first model that startled even its creators with what it could do, and it was available only through an API.

The jump from GPT-2 to GPT-3 was about a hundred times more parameters. The capability jump was larger still.

## The ChatGPT moment, November 2022

On November 30, 2022, OpenAI launched ChatGPT — a chat interface to a fine-tuned version of GPT-3.5. The launch was framed as a low-key research preview. It went viral within hours.

One million users in five days. One hundred million users in two months. At the time, the fastest-growing consumer product in history.

## The scramble that followed, late 2022 through 2023

The ChatGPT launch triggered a frantic reordering of the industry.

Google declared an internal "code red." It treated ChatGPT as an existential threat to search.

Anthropic, founded by ex-OpenAI researchers, released the first version of its Claude assistant in March 2023.

Meta released the first version of Llama, becoming the first major company to release a frontier-class model with open weights (anyone could download and run it).

Microsoft, which had already invested in OpenAI starting in 2019, deepened the relationship dramatically. The total Microsoft investment in OpenAI eventually exceeded thirteen billion dollars.

Amazon made a comparable bet on Anthropic, eventually committing up to twenty-five billion dollars.

By the end of 2023, the modern AI industry — its big players, its commercial structure, its competitive shape — was largely set. Most of what has happened since has been the elaboration of that structure.
