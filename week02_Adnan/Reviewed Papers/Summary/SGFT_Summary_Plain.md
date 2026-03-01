# 🗺️ Solution Guidance Fine-Tuning (SGFT) — Plain Language Summary
### *What if instead of teaching the AI to solve problems, you just teach it to make a plan first?*
> Bi et al., Beijing Jiaotong University · arXiv December 2024

---

## 💡 The Big Idea — In One Sentence

> **Instead of teaching a small AI to calculate answers step by step, teach it to write a problem-solving plan first — then let it (or any other AI) follow that plan to get the right answer. Uses only 3% of the training data.**

---

## 🤔 What Problem Does This Solve?

The standard way to make a small AI better at reasoning is called **Chain-of-Thought (CoT)** — basically teaching it to "show its working" like a student would. But this has a hidden flaw:

| 😬 The Problem with CoT | ✅ What SGFT Does Instead |
|------------------------|--------------------------|
| The AI tries to *think* and *calculate* at the same time in every step | Splits the job: **plan first**, **calculate second** |
| One calculation error corrupts all the steps that follow | A planning error doesn't directly cause calculation errors |
| Needs ~30,000 examples to train well | Needs only **~1,000–3,000 examples** (3% as much) |
| Over-trained models start inventing unnecessary reasoning chains | The planner stays focused on structure, not numbers |

> 💬 Think of it like building with IKEA furniture. CoT gives you complicated multi-step instructions mixed with measurements. SGFT gives you just the assembly diagram — the steps without the numbers — and lets you figure out the measurements yourself.

---

## ⚙️ How It Works — No Jargon

The system uses **two small AIs working as a team**:

```
  📋 AI #1 — The Planner (trained with SGFT)
       Reads the question.
       Does NOT calculate anything.
       Just writes a clear step-by-step plan:
       "Step 1: Find total X. Step 2: Divide by Y. Step 3: Add Z."

        ↓  Passes the plan to →

  🧮 AI #2 — The Solver (no special training needed)
       Gets the original question + the plan.
       Follows the plan to calculate the actual answer.
       Gets it right far more often because the logic is already laid out.
```

> 🎯 The key insight: *planning what to do* and *doing the calculations* are two different skills. Separating them makes both easier.

---

## 🔧 Exact Methodology — Step by Step (Simply Put)

**① Ask GPT-4o to solve 7 sample questions and observe the pattern**
They gave GPT-4o a handful of maths questions and studied how it approached them — not the answers, but the *structure* of its reasoning. They identified a common pattern: identify what's needed → solve intermediate steps → combine → verify.

**② Use GPT-4o to generate ~3,000 "plans" (called Solution Guidances)**
For each training question, GPT-4o produces a plan of 2–6 steps with *no numbers or calculations* — just the logical roadmap. These become the training data.

> 💬 **What is a Solution Guidance?** It looks like: *"Step 1: Calculate total slices needed. Step 2: Divide by slices per pizza. Step 3: Sum both types."* — no actual numbers, just the strategy.

**③ Clean the data — remove anything with actual calculations**
Any training example where GPT-4o accidentally included numbers or computations was removed. The goal is pure planning data only.

**④ Fine-tune a small AI (the Planner) on this planning data only**
Using a lightweight training method (LISA — faster than standard fine-tuning), the small AI learns to produce plans. It's specifically instructed: *"Do not solve it, just output the steps."*

**⑤ At test time: Planner generates a plan → Solver reads plan + question → gives answer**
The Solver can be *any* small AI — even one from a different model family. No extra training needed for the Solver. The plan just goes in as extra context.

**⑥ Optionally: mix and match different Planners and Solvers**
One of the most useful findings is that the best Planner and best Solver don't have to be the same model. A ChatGLM Planner feeding a Qwen Solver outperformed both models working alone.

---

## 📊 Results — How Much Did It Improve?

> Scores = % of questions answered correctly (higher = better)
> Tested on maths word problems and commonsense reasoning

### 🏆 SGFT vs. Standard CoT Fine-Tuning (ChatGLM3-6B)

| Method | Training Data Needed | GSM8K Score | Improvement |
|--------|:-------------------:|:-----------:|:-----------:|
| Original model (no training) | — | 27.4% | baseline |
| CoT fine-tuning | **30,000 examples** | 34.4% | +7.0% |
| **SGFT (ours)** | **3,000 examples** | **43.7%** | **+16.3%** ✅ |

> 🎉 Better result with **10× less data**

### 📊 Works Across All Models and Tasks

| Model Pair (Planner → Solver) | GSM8K | Commonsense |
|-------------------------------|:-----:|:-----------:|
| ChatGLM → ChatGLM | 43.7% | 69.8% |
| Qwen → ChatGLM | **48.3%** | **75.7%** |
| ChatGLM → Llama | 39.6% | 68.2% |
| Llama → Llama | 28.6% | 62.1% |

> 📌 Mixing models often beats using the same model for both jobs. The best combo (Qwen as Planner, ChatGLM as Solver) hit **48.3%** on maths — far above any single model.

### 📉 Data Efficiency — The Most Remarkable Finding

```
CoT fine-tuning:   needs ~30,000 examples to reach ~34%
SGFT:              needs ~3,000  examples to reach ~44%

SGFT with 1,000 examples STILL beats CoT with 30,000 examples 🟢
```

---

## 🔬 The Most Interesting Discovery

When they tested four combinations of trained/untrained models, the winner was surprising:

```
Option A: Untrained Planner + Untrained Solver         → ~30%  (baseline)
Option B: Untrained Planner + CoT-trained Solver       → ~26%  ❌ (worse!)
Option C: SG-trained Planner + Untrained Solver        → ~44%  ✅ (best!)
Option D: SG-trained Planner + CoT-trained Solver      → ~39%  (good but not best)
```

> 💬 The CoT-trained Solver actually *hurt* performance when used as the answering model. The over-trained solver became too rigid — it needed a clean, untrained model to freely follow the plan. This echoes Paper 4's finding: heavy fine-tuning can sometimes make things worse.

---

## 🆚 How Does This Compare to the Other Papers?

| Feature | ISC (P2) | ReflectEvo (P1) | SCORE (P3) | SGFT (This Paper) |
|---------|:--------:|:---------------:|:----------:|:-----------------:|
| Core idea | Self-check & fix | Deep reflection | Critique & correct | Plan first, then solve |
| Training data needed | ~15k | ~460k | ~14–25k | **~3k** ✅ |
| Uses two separate models? | ❌ No | ❌ No | ⚠️ For verifier | **✅ Yes — by design** |
| Fixes errors after the fact? | ✅ Yes | ✅ Yes | ✅ Yes | ❌ Prevents them upfront |
| Works on a single consumer GPU? | ✅ | ❌ | ❌ | **✅ Yes** |
| Max improvement seen | +5.6% | +33% | +14.6% | **+16.3% on 3% data** |

> 💬 SGFT is the most **resource-efficient** of the five approaches. The others fix mistakes after they happen; SGFT tries to prevent mistakes from happening in the first place.

---

## 🚀 Feasibility for Your Project
### *Building a small AI that performs like a large one*

| Your Goal | What SGFT Proves |
|-----------|-----------------|
| Improve small model reasoning without huge data | ✅ 3,000 examples is enough — very accessible |
| Run on limited hardware | ✅ Single consumer GPU confirmed |
| Not rely on GPT-4 for everything | ⚠️ GPT-4o used once to generate plans — but only needed at setup, not at runtime |
| Mix and match models flexibly | ✅ Any model can be the Solver with no extra training |
| Generalise to new topics | ✅ Trained only on maths, tested on commonsense — still improved |

### 🛠️ What to Take From This Paper for Your Project

```
1. Consider separating planning from solving  →  two small models in a team
                                                   can beat one larger model alone

2. Start with just 1,000–3,000 examples  →  this is very realistic for a
                                              student or small research project

3. Don't over-train your solver model  →  a clean, untuned solver following
                                           a good plan outperforms a heavily
                                           fine-tuned one (see Option C vs D)

4. Use GPT-4 only once — for data generation  →  you don't need ongoing
                                                   API costs after setup

5. Combine with self-correction (Papers 1–3)  →  Plan first (SGFT) →
                                                    Answer → Self-check (ISC/SCORE)
                                                    for a powerful two-stage pipeline
```

> 💬 **Bottom line for your project:** SGFT is the most practically achievable approach of the five papers. It works on one GPU, needs minimal data, and doesn't require the AI to be good at self-reflection (which Papers 1–3 all demand). If you're resource-constrained, this is your starting point. If you have more compute, combine it with self-correction for extra gains.

---

*Based on: "Enhancing the Reasoning Capabilities of Small Language Models via Solution Guidance Fine-Tuning" — arXiv:2412.09906 (December 2024)*
