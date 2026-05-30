# Appendix A — Glossary

**Version:** v1 · **Last updated:** 2026-05-30 · **Source:** *Just Predicting Words*, Appendix A

A reference for terms used throughout the book. Plain-language definitions.

---

**Agentic AI.** AI that can plan, take actions, and execute multi-step tasks autonomously rather than just answering questions. The 2025–2026 frontier has shifted from chatbots to agents. Claude Code, ChatGPT operators, and several Chinese systems are early examples.

**AGI (Artificial General Intelligence).** The hypothetical capability of AI to perform any cognitive task a human can, across all domains. Different researchers define the threshold differently. Some think AGI is imminent. Some think it is decades away. Some think the concept is poorly defined.

**Alignment.** The technical problem of getting AI systems to do what their designers intend, especially as systems become more capable. Major labs invest in alignment research because they believe current techniques may not be sufficient for more powerful systems.

**Attention.** The mechanism inside a Transformer that lets the model weigh which parts of the input matter most for understanding any given word. Introduced in the 2017 paper "Attention Is All You Need." The core trick of modern language models.

**Bias.** The pattern by which AI systems can produce outputs that systematically disadvantage certain groups, usually because the training data reflected historical inequities. Real and documented, though one labs work continuously to mitigate.

**ChatGPT.** The consumer chatbot from OpenAI, launched November 30, 2022. The product that brought AI assistants into mainstream awareness. Reached 100 million users in two months.

**Claude.** The consumer chatbot from Anthropic. Launched in 2023. Known for being relatively careful, willing to push back on the user, and trained using Constitutional AI principles.

**Constitutional AI.** A technique developed by Anthropic for aligning AI systems by giving them a written set of principles to follow. The model critiques and revises its own outputs against the principles.

**Context window.** The amount of text a model can consider at once. The first GPT models had context windows of a few thousand tokens. By 2026, frontier models often have context windows of one to two million tokens — enough to process entire books.

**Deepfake.** AI-generated audio, video, or images designed to look or sound like a real person. The technology crossed a quality threshold in 2025–2026 that makes it accessible to anyone with a smartphone.

**Embedding.** A representation of a word or piece of text as a list of numbers (a vector) that captures its meaning. Words similar in meaning have embeddings close to each other. The basis of how modern AI represents language.

**Fine-tuning.** Additional training applied to a pre-trained model to specialize it for a particular task or to adjust its behavior. The first training is on broad text; fine-tuning shapes the model toward specific uses.

**Foundation model.** A large AI model trained on broad data that can be adapted to many specific applications. GPT, Claude, Gemini, and Llama are all foundation models. The term emphasizes that the model is the foundation on which many specific products are built.

**Generative AI.** AI systems that produce content (text, images, audio, video, code) rather than just classifying or analyzing existing content. The current AI boom is centered on generative AI.

**GPT (Generative Pre-trained Transformer).** The family of language models from OpenAI, beginning with GPT-1 in 2018 and continuing through GPT-5 and beyond.

**Hallucination.** The phenomenon where AI confidently produces information that is not true. Names of cases that do not exist. Statistics that are made up. Citations that lead nowhere.

**Interpretability.** The research effort to understand what is happening inside an AI model. The model's behavior emerges from billions of parameters; interpretability research tries to make these internal workings legible to humans, which is essential for verifying safety.

**Jailbreak.** A technique for bypassing the safety constraints of an AI model. By 2026, sophisticated jailbreaks achieve high success rates against most frontier models.

**Large Language Model (LLM).** A type of AI model trained on large amounts of text, designed to predict the next word in a sequence. ChatGPT, Claude, Gemini, and most modern AI assistants are large language models.

**Llama.** Meta's family of open-weight language models, released from 2023 through 2025. Versions 1 through 3 made Meta the leader of the open-weight ecosystem. The Llama 4 launch in 2025 was a setback, and Meta pivoted away from open weights with Muse Spark.

**Multimodal.** A model that can work with multiple types of input or output: text, images, audio, video. Most frontier models in 2026 are multimodal.

**Open weight.** A model whose weights are publicly available. Anyone can download and run an open-weight model on their own hardware. Contrast with closed-weight models like GPT-5 or Claude.

**Parameters.** The internal numerical values inside a neural network that get adjusted during training. Modern frontier models have hundreds of billions to trillions of parameters. More parameters generally means more capacity to learn complex patterns.

**Prompt.** The text you give an AI model as input. The skill of writing prompts well is sometimes called prompt engineering, though the term has become less prominent as models have gotten better at understanding casual requests.

**Prompt injection.** An attack technique where an attacker embeds instructions inside content the AI model reads, attempting to override the model's intended behavior. As AI gets more agentic, this becomes a more serious security concern.

**RAG (Retrieval-Augmented Generation).** A technique where an AI model is given access to a specific collection of documents and instructed to base its answers on that collection. Often used to give AI assistants access to specific company knowledge.

**Red teaming.** The practice of having researchers actively try to break an AI model's safety measures. Discovered problems get patched. A standard part of how frontier AI systems are developed.

**RLHF (Reinforcement Learning from Human Feedback).** The training technique that shaped raw word predictors into helpful assistants. Human raters evaluate model outputs; ratings train the model to produce outputs humans prefer.

**System prompt.** A hidden block of instructions prepended to every conversation with an AI assistant. Shapes behavior, tone, and constraints. Most users never see it. Most differences between AI products are in the system prompt rather than the underlying model.

**Token.** A piece of a word that an AI model treats as a single unit. "Cat" might be one token. "Unbelievable" might be three tokens. The model reads and writes in tokens, not characters or words.

**Training data.** The text and other content used to teach a model what patterns to recognize and produce. Frontier models are trained on truly enormous amounts of data, often essentially the entire public internet plus licensed datasets.

**Transformer.** The neural network architecture introduced in the 2017 paper "Attention Is All You Need." The basis for virtually all modern AI assistants.

**Vector.** A list of numbers representing the meaning of a word or piece of text in a high-dimensional space. See Embedding.

**Weights.** The actual numerical values inside a trained AI model. The weights determine what the model does. An open-weight model shares its weights publicly. A closed-weight model keeps them proprietary.

**World model.** A type of AI that learns to predict and simulate physical reality rather than just generating text. A frontier research area in 2026, with significant investment from Google DeepMind, Meta, and others. Believed by some researchers to be necessary for true general intelligence.
