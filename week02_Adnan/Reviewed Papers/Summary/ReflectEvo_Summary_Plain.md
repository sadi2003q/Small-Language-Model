# 🧠 ReflectEvo — Plain Language Summary
### *Can a small AI learn to think twice and get smarter?*
> Research by BIGAI & Peking University · May 2025

---

## 💡 The Big Idea — In One Sentence

> **A small, cheap AI model can become just as smart as a model 8× its size — simply by learning to review its own mistakes.**

---

## 🤔 What Problem Does This Solve?

Imagine two types of students:

| 🐢 Small Model (before this research) | 🚀 Small Model (after ReflectEvo) |
|---------------------------------------|-----------------------------------|
| Answers a question, gets it wrong, moves on | Answers a question, **notices the mistake**, figures out *why*, tries again |
| Needs a much bigger (expensive) AI to improve | **Teaches itself** using its own errors |
| Costs a lot to scale up | Stays small and affordable |

Until now, researchers assumed you needed a **very large AI** to do this kind of self-checking. This paper proves that wrong.

---

## ⚙️ How It Works — No Jargon

Think of it like a student doing homework with a self-grading system:

```
  📝 Step 1 — Answer the question
       The AI reads a question and gives its best answer.

        ↓  Wrong answer?

  🔍 Step 2 — Look in the mirror (Self-Reflection)
       The AI asks itself:
       "Where exactly did I go wrong?"
       "Why did I make that mistake?"
       "What should I do differently?"

        ↓

  ✏️  Step 3 — Try again (Self-Correction)
       Armed with that reflection, the AI writes a new, better answer.

        ↓

  🔁 Step 4 — Learn from this for next time (Self-Training)
       The good reflections are saved and used to train the AI
       so it gets better at reflecting over time.
```

This loop repeats across **460,000 practice examples** covering maths, logic, coding, reading comprehension, and more.

---

## 🔧 Exact Methodology — Step by Step (Simply Put)

**① Collect 460,000 questions from 17 public datasets across 10 subjects**
They pulled together questions from maths, logic, coding, commonsense reasoning and more — all with known correct answers. No expensive human annotation needed.

**② Build a pool of 32 different "reflection instructions"**
Instead of one fixed prompt like *"reflect on your answer"*, they created 32 different ways to ask the AI to reflect — varying the tone, focus, and depth. This variety stops the AI from memorising one reflection style and forces it to genuinely think.

**③ Let the AI answer each question and check if it got it right**
A simple automatic checker compares the AI's answer to the known correct answer and returns just one signal: *"correct"* or *"incorrect"*. No human needed for this step.

**④ For wrong answers — ask the same AI to reflect on its mistake**
Using one of the 32 instructions, the AI is asked: *"Where did you go wrong? Why? What should you do differently?"* It then writes a reflection and tries the question again. This is repeated with different instructions to generate multiple reflections per question.

**⑤ Sort the reflections into three groups for training**
- **D⁺** (Positive only): Reflections where the AI successfully corrected itself — high quality, used for standard training
- **D±** (Positive + Negative pairs): Pairs of a good correction and a bad one side by side — used to teach the AI to *prefer* good reflections
- **Dpref** (GPT-4o ranked): GPT-4o reads two competing reflections and picks the better one — the highest quality signal, used for preference training

**⑥ Train using four different methods (Settings 1–4)**
- **Setting 1** — One-stage: train reflection and correction together in a single step
- **Setting 2** — Two-stage: train reflection first, then correction separately
- **Setting 3** — DPO on D± : teach the AI to prefer correct reflections over incorrect ones
- **Setting 4** — DPO on Dpref: same but using GPT-4o's quality rankings as the signal

> 💬 **What is DPO?** Direct Preference Optimisation — instead of just training on correct examples, it explicitly teaches the model *"this reflection is better than that one"*, like giving it a ranking test rather than just a pass/fail test.

**⑦ At test time — the trained AI reflects once and corrects automatically**
Given a new question, the AI answers it, checks itself, reflects if wrong, and corrects — all in two turns. More turns can be added for further improvement (up to 6 turns tested in this paper).

---

## 📊 Results — How Much Did It Actually Improve?

### 🏆 The Headline Numbers

> Think of these scores like **exam results out of 100**

| Model | First Attempt Score | After Reflecting | Improvement |
|-------|:-------------------:|:----------------:|:-----------:|
| Small AI (8B) — no training | 38 / 100 | 52 / 100 | +14 pts |
| **Small AI (8B) — with ReflectEvo** | 38 / 100 | **71 / 100** | **+33 pts** ✅ |
| Big AI (70B) — 8× larger & costlier | 48 / 100 | 64 / 100 | +19 pts |

> 🎉 The **small trained model scores 71** while the **big expensive model only scores 64**

---

### 📈 The More It Thinks, The Better It Gets

Each "turn" = one extra round of reflection and retry:

```
Round 1 ──► Round 2 ──► Round 3 ──► Round 4 ──► Round 5 ──► Round 6
  38%          63%          70%          76%          79%         80%+
                                                              🏁 keeps climbing
```

> Like a student who keeps re-reading an exam question — each pass catches something new.

---

### 🗂️ It Works Across Many Subjects

| Subject | First Try | After Reflecting | Boost |
|---------|:---------:|:----------------:|:-----:|
| Common sense reasoning | 40% | 99% | 🟢 +59% |
| Social reasoning | 34% | 70% | 🟢 +36% |
| Reading comprehension | 35% | 58% | 🟢 +23% |
| Logic | 31% | 49% | 🟡 +18% |
| Maths | 14% | 24% | 🔴 modest |
| Coding | 28% | 30% | 🔴 modest |

> Reflection helps most with **reasoning and understanding**. Maths and coding need more specialised practice.

---

### 🐛 What Kind of Mistakes Does Reflection Catch?

| Mistake Type | How Often |
|-------------|:---------:|
| Wrong reasoning / flawed logic | **55%** of errors |
| Misread the question or instructions | **36%** of errors |
| Wrong calculation | 7% of errors |
| Wrong facts | 1% of errors |

> Most mistakes aren't about *not knowing facts* — they're about *thinking sloppily*. Reflection directly fixes that.

---

## 🚀 What This Means for Your Project
### *Building a small AI that performs like a large one*

ReflectEvo is essentially a **blueprint for your idea**. Here's how it lines up:

| Your Goal | What ReflectEvo Proves |
|-----------|----------------------|
| Make a small model compete with big ones | ✅ Done — 8B beats 70B on reasoning |
| Avoid paying for massive compute | ✅ Runs on just 2 GPUs |
| Not rely on expensive proprietary AI (like GPT-4) for training | ✅ Model trains itself — GPT-4 only optional for a boost |
| Use openly available data | ✅ All 17 training datasets are public |
| Apply to multiple problem types | ✅ Tested across 10 different subjects |

### 🛠️ Simplest Path to Get Started

```
1. Pick a small open model  →  Llama-3-8B or Mistral-7B (free, open-source)

2. Pick one subject to focus on  →  e.g., logic or reading comprehension
                                     (these get the biggest gains)

3. Let the model answer questions and flag its own wrong answers

4. Train it on its own reflections  →  the "thinking twice" habit gets built in

5. Test if it now beats a bigger model  →  based on this paper, it likely will
```

> 💬 **Bottom line:** This paper is strong evidence that your project idea is not just feasible — it has already been proven to work. The key ingredient isn't a bigger model, it's *teaching the model to pause and think critically about its own answers.*

---

*Based on: ReflectEvo — arXiv:2505.16475 (May 2025)*
