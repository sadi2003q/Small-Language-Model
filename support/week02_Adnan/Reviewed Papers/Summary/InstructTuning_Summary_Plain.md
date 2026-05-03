# 🔎 Do Instruction-Tuned Models Always Perform Better? — Plain Language Summary
### *The surprising truth: the "upgraded" AI isn't always the smarter one*
> Munjal et al., M42, Abu Dhabi · arXiv January 2026

---

## 💡 The Big Idea — In One Sentence

> **Instruction-tuned models — the polished, "ready-to-use" versions of AI — are not always smarter than their raw base counterparts. Under the right conditions, the unfinished base model wins.**

---

## 🤔 What Problem Does This Solve?

There are two versions of almost every AI model:

| 🧱 Base Model | ✨ Instruction-Tuned Model |
|--------------|--------------------------|
| The raw, unpolished version — trained on huge amounts of text but not specifically told how to respond | The finished product — extra-trained to follow instructions, be helpful, format answers nicely |
| Usually ignored in comparisons | Almost always assumed to be better |

The field has largely *assumed* that the instruction-tuned version is always superior. This paper tests that assumption rigorously — and finds it's often **wrong**.

> 💬 Think of it like a raw cooking ingredient vs. a pre-seasoned ready meal. The ready meal is convenient and usually tasty — but sometimes the raw ingredient, prepared the right way, is actually better.

---

## ⚙️ How It Works — No Jargon

The researchers ran a large controlled experiment:

```
  📋 Step 1 — Pick 16 AI models across 5 major families
       (Llama, Qwen, DeepSeek, Kimi, SmolLM — sizes from tiny to massive)
       For each model, they tested BOTH versions:
       the base model AND the instruction-tuned version

        ↓

  🧪 Step 2 — Test them on 4 different types of problems
       Standard maths  →  GSM8K (grade school maths)
       Hard maths      →  Math-500 (university-level)
       Tricky maths    →  Math-Perturb (same problems, disguised differently)
       Medical maths   →  MedCalc (clinical calculations, totally new domain)

        ↓

  🔁 Step 3 — Try each question 20 times per model
       This gives a fair picture of what the model is capable of
       at its best, not just on one lucky attempt

        ↓

  📊 Step 4 — Compare the scores across all conditions
       Zero-shot (no examples given) vs. few-shot (some examples given)
       Standard evaluation vs. stricter evaluation
```

---

## 🔧 Exact Methodology — Step by Step (Simply Put)

**① Two different answer strategies were used fairly**
Base models used a technique called *CoT decoding* — which explores multiple possible answer paths before committing. Instruction-tuned models used standard repeated sampling. Both generated 20 attempts per question.

**② Four benchmarks were deliberately chosen to stress-test the assumption**
Standard tests (GSM8K, Math-500) show how models perform in ideal conditions. The tricky tests (Math-Perturb, MedCalc) reveal whether the improvement is real reasoning or just pattern memorisation.

> 💬 **What is Math-Perturb?** The same maths questions from Math-500, but reworded to break any memorised shortcuts. If a model truly *understands* maths, it should still do well. If it was just memorising answer patterns, its score collapses.

**③ Two different scoring methods were compared**
They discovered that even the scoring tools disagree with each other — one tool might say the model got a question right while another says it got it wrong. This exposed a hidden reliability problem in how AI benchmarks are measured.

**④ Zero-shot vs. few-shot settings were tested separately**
*Zero-shot* = no examples given, just the question. *Few-shot* = a few example questions and answers given first to warm up the model. This revealed that instruction-tuned models are heavily dependent on being given examples, while base models are more self-sufficient.

---

## 📊 Results — What They Actually Found

### 🏆 Finding 1: Base Models Win on Zero-Shot Maths

> Zero-shot = no example questions given first

| Model | Instruction-Tuned Score | Base Model Score | Base Advantage |
|-------|:-----------------------:|:----------------:|:--------------:|
| Llama3-70B | 58.1% | **90.8%** | 🟢 **+32.7%** |
| Kimi-K2 | 67.6% | **98.9%** | 🟢 **+31.3%** |
| DeepSeek-V3.1 | 69.9% | **96.6%** | 🟢 **+26.7%** |
| Qwen3-14B | 67.0% | **97.7%** | 🟢 **+30.7%** |

> 🎯 The instruction-tuned model drops by up to **33 percentage points** when no example answers are provided first. The base model doesn't need the examples — it already knows how to reason.

---

### 🏥 Finding 2: Base Models Win on Medical Calculations (New Domain)

When tested on medical maths — a domain neither model was specifically trained on:

| Model | Instruction-Tuned | Base Model | Base Advantage |
|-------|:-----------------:|:----------:|:--------------:|
| Llama3-3B | 28.9% | **62.1%** | 🟢 **+33.1%** |
| SmolLM-3B | 39.3% | **61.9%** | 🟢 **+22.6%** |
| Llama3-70B | 44.9% | **51.7%** | 🟢 **+6.8%** |
| Kimi-K2 | 70.1% | **76.2%** | 🟢 **+6.1%** |

> 📌 The instruction tuning that made the model "better" at familiar tasks actually *hurt it* on new ones.

---

### 💥 Finding 3: Hard Disguised Questions Expose Memorisation

When maths problems were reworded to break memorised templates:

```
Model           Math-500 (normal)   Math-Perturb (disguised)   Drop
─────────────────────────────────────────────────────────────────────
LLaMA3-70B          59.8%               22.2%                 -37.6% 😨
Qwen3-14B           78.0%               39.8%                 -38.2% 😨
Kimi-K2             94.2%               76.3%                 -17.9% 😬
DeepSeek-V3.1       95.2%               77.8%                 -17.4% 😬
```

> 🎯 A drop this large suggests the high scores on normal benchmarks partly reflect **memorising question templates**, not genuine understanding.

---

### 📏 Finding 4: Even the Scoring Tools Can't Agree

A surprising bonus discovery — the tools used to *measure* AI performance are unreliable:

| Model | Score by Tool A | Score by Tool B | Disagreement |
|-------|:--------------:|:--------------:|:------------:|
| Qwen3-14B (base) | 88.8% | 85.2% | 3.6% gap |
| Qwen3-14B (instruct) | 78.0% | 84.4% | **6.4% gap** |
| Kimi-K2 (instruct) | 94.2% | 88.6% | 5.6% gap |

> In the worst case, the *direction* of who wins flips entirely depending on which tool you use. Published leaderboard scores may be less trustworthy than they appear.

---

## 🔁 When Does Instruction Tuning Actually Help?

It's not all bad news for instruction tuning — it genuinely helps in specific situations:

| Situation | Does Instruction Tuning Help? |
|-----------|:-----------------------------:|
| Small models (under 7B) | ✅ Yes — big gains |
| When given example questions first (few-shot) | ✅ Yes — closes the gap |
| Standard benchmarks it may have seen during training | ✅ Often yes |
| Large models (70B+) on zero-shot tasks | ❌ No — base often wins |
| Brand new domains (medicine, law, etc.) | ❌ No — base often wins |
| Disguised versions of familiar problems | ❌ No — base is more robust |

---

## 🆚 How Does This Paper Relate to the Other Three?

The previous papers all assumed instruction-tuned models as the starting point. This paper questions that foundation:

| Papers 1–3 (ReflectEvo, ISC, SCORE) | **This Paper** |
|--------------------------------------|----------------|
| Focused on making instruction-tuned SLMs better at self-correction | Asks: *should you even start with an instruction-tuned model?* |
| Assumed instruction tuning is the baseline | Shows the baseline itself may be artificially inflated |
| Tested on standard benchmarks | Tests on standard **and** domain-shifted benchmarks |
| Key message: small models can self-correct | **Key message: base models may already be more capable than assumed** |

> 💬 This paper is an important **reality check** for anyone building on top of instruction-tuned models.

---

## 🚀 Feasibility & Implications for Your Project
### *Building a small AI that performs like a large one*

This paper changes some assumptions you might have had:

| Assumption Before This Paper | What This Paper Suggests Instead |
|------------------------------|----------------------------------|
| Start with an instruction-tuned model | Consider testing the **base model first** — it may already be strong |
| Instruction tuning = better reasoning | Instruction tuning = better at following a specific format, not always better at thinking |
| High benchmark scores = capable model | High benchmark scores may reflect **memorisation** — test on new domains too |
| Small tuned models lag behind large ones | Small **base** models can close the gap more than expected |

### 🛠️ What to Take From This Paper for Your Project

```
1. Don't skip the base model  →  always benchmark base vs. instruct;
                                   you may be surprised which wins

2. Test outside your training domain  →  if your project targets a specific
                                          field, test there — not just on GSM8K

3. Use zero-shot testing too  →  few-shot can flatter instruction-tuned models;
                                   zero-shot reveals true reasoning capability

4. Be sceptical of benchmark scores  →  the scoring tools disagree;
                                          use multiple evaluators if possible

5. For self-correction (Papers 1–3)  →  consider training self-correction
                                          on top of a base model, not just instruct
```

> 💬 **Bottom line for your project:** The previous three papers showed *how* to make small models self-correct. This paper is a warning about *what* you measure and *what* you start with. A base model with smart sampling and self-correction training may outperform a heavily instruction-tuned model that looks impressive on standard tests — but crumbles on anything unfamiliar.

---

*Based on: "Do Instruction-Tuned Models Always Perform Better Than Base Models?" — arXiv:2601.13244 (January 2026)*
