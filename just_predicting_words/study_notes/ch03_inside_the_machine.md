# Chapter 3 — Inside the Machine

**Version:** v1 · **Last updated:** 2026-05-30 · **Source:** *Just Predicting Words*, Ch3

---

## Tokens

Modern language models don't read characters and they don't quite read words. They read tokens. A token is usually a piece of a word — typically four characters or so, sometimes a whole short word, sometimes a single character for rare cases. "Cat" might be one token. "Unbelievable" might be three. Names, punctuation, and unusual character sequences each become their own tokens.

The model produces text the same way it reads it: one token at a time. The "next-word prediction" framing from chapter one is more precisely "next-token prediction." For practical purposes the distinction usually doesn't matter, but it matters for understanding context limits and pricing — most AI APIs charge per token, not per word.

## Embeddings and vector space

Each token gets converted into a vector — a list of several hundred to several thousand numbers. The vector is the model's internal representation of that token's meaning, learned during training from the patterns of how the token co-occurs with others.

This is the same idea as word2vec from chapter two, but scaled up. The vector space has the property that semantically similar tokens end up close to each other. Words about cooking cluster together. Words about sports cluster together. Mathematical relationships between vectors capture conceptual relationships — gender, capital-of, plural-of, comparative-of, and many others the model discovers without supervision.

The vectors are dense (every dimension carries some signal, none are zero by default), high-dimensional (hundreds to thousands of dimensions, far more than humans can visualize), and the dimensions don't correspond to human-interpretable categories — they emerge from the training process.

## Attention

The Transformer's core mechanism is called attention. When the model is producing the next token, it doesn't treat all the previous tokens equally. For each token it's about to generate, it computes how much "attention" to pay to every previous token in the context, and weights its prediction accordingly.

This solves the problem word2vec couldn't solve: word order matters, and context further back can be relevant. When the model sees "the dog chased its tail," attention lets it know that "its" refers to "dog," not to something earlier or later in the sentence. When the model is summarizing a long document, attention lets it pull together information from anywhere in the document, not just nearby words.

The full name of the 2017 paper that introduced the Transformer was "Attention Is All You Need" — meaning that attention alone, without the other complicated architectural pieces researchers had been trying, was enough.

## The Transformer architecture

A Transformer is a stack of layers, each layer made of attention plus some standard neural-network components. Information flows up the stack: lower layers learn local patterns (which word follows which), middle layers learn syntactic and structural patterns (how sentences are organized), upper layers learn abstract semantic patterns (what the passage is about, how to respond to it).

A modern frontier model has dozens to over a hundred such layers. Each layer transforms the representations slightly. By the top of the stack, the representations are rich enough to support the model's predictions.

## Pre-training

A frontier model is trained on enormous amounts of text. The training objective is simple: given a sequence of tokens, predict the next one. Do this billions of times across trillions of tokens of text. The text comes from essentially the entire public internet, plus licensed datasets, books, code repositories, and other sources.

This phase is called pre-training. It's the most expensive part of building a modern AI model — it requires months of compute on thousands to tens of thousands of GPUs and costs hundreds of millions of dollars for the largest models. The model that comes out of pre-training is a raw next-token predictor. It is not yet a chatbot, doesn't know what a user is, and doesn't know it's supposed to be helpful. That shaping happens in the next phase, which chapter four covers.

## Parameters

A model's parameters are the actual numerical values inside the neural network. Pre-training sets these values. Roughly speaking, more parameters means more capacity to learn complex patterns, though the relationship is not strictly linear.

The headline numbers across the GPT line: GPT-1 had 117 million, GPT-2 had 1.5 billion, GPT-3 had 175 billion. The largest open-weight frontier models in 2026 (such as DeepSeek V4's 1.6 trillion-parameter variant) have crossed the trillion mark. The largest closed-weight frontier models are believed to be comparable or larger but their exact sizes are not disclosed.

When AI labs talk about model size, they almost always mean parameter count.

## Context window

The amount of text the model can consider at once is called the context window, measured in tokens. The first GPT models had context windows of a few thousand tokens. By 2026, frontier models often have context windows of one to two million tokens — enough to fit entire books, large codebases, or long meeting transcripts in a single conversation. Context windows have grown much faster than parameter counts in recent years and are now one of the most important practical differences between competing models.
