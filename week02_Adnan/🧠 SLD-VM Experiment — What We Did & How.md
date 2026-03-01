# 🧠 SLD-VM Experiment — What We Did & How

> **Plain-English Summary:** We tested whether adding a sophisticated multi-step reasoning pipeline to an AI model would make it smarter than simply asking it questions directly.
> 

---

## 🎯 What We Did

We built a complex AI reasoning system called **SLD-VM** *(Structured Latent Deliberation with Verifiable Memory)* and tested it against two challenging tasks — competition-level maths and science questions. The core question: *does adding more structure and verification actually help?*

---

## 🤖 The AI Models Used

| Role | Model | What it does |
| --- | --- | --- |
| **Main brain** | Microsoft Phi-4-mini | Reads questions, reasons through steps, gives answers |
| **Fact-checker** | Qwen2.5-72B | A much larger model used to verify the smaller model's reasoning |

---

## 📚 What We Tested It On

| Dataset | What it is | Difficulty | Random guess score |
| --- | --- | --- | --- |
| **MATH** | Competition-level algebra & number theory | ⭐⭐⭐⭐⭐ Very Hard | N/A |
| **ARC-Challenge** | Hard science multiple-choice questions | ⭐⭐⭐⭐ Hard | 25% (4 options) |

100 questions were used for each dataset.

---

## 🔧 How the Pipeline Works

Think of SLD-VM as an AI with a strict internal checklist:

| Step | Plain English |
| --- | --- |
| 1 · Memory lookup | Checks if it has seen a similar problem before |
| 2 · Break it down | Splits the problem into small numbered steps |
| 3 · Build a reasoning map | Connects steps into a logical chain |
| 4 · Triple-check each step | Rules engine → small model → large model verify every step |
| 5 · Backtrack if wrong | If a step fails, tries a different approach |
| 6 · Write the final answer | Synthesises only from verified steps |
| 7 · Save what worked | Stores successful patterns in memory for next time |

**What it was compared against:**

- **Zero-Shot** — Just ask the model the question directly, no extras
- **Chain-of-Thought (CoT)** — Ask the model to think step-by-step in plain text

---

## ⏱️ Time & Resources

```jsx
Time per 100 questions (lower is better)

MATH
Zero-shot   ~25 min | ████████████
CoT         ~18 min | █████████
SLD-VM      ~62 min | ███████████████████████████████

ARC
Zero-shot    ~1 min | █
CoT          ~9 min | █████
SLD-VM      ~46 min | ███████████████████████
```

> The full pipeline used **472 API calls** to the large verifier model and took up to **60× longer** than a direct question.
> 

## **📊 SLD-VM Results — Did It Work?**

> **Short answer:** No. The complex pipeline did not outperform simply asking the AI to think step-by-step. For maths it was dramatically worse. For science it was nearly identical.
> 

---

---

## 📊 Performance Visualised

```
MATH                   Accuracy
─────────────────────────────────────────
Chain-of-Thought   66% ██████████████████████████ 🏆
Zero-Shot          61% ████████████████████████
SLD-VM Pipeline    32% █████████████ 🚨

SCIENCE (ARC) Accuracy
─────────────────────────────────────────
Chain-of-Thought   83% █████████████████████████████████ 🏆
SLD-VM Pipeline    82% ████████████████████████████████
Zero-Shot          80% ███████████████████████████████
Random Guess       25% █████████
```

---

## ⚔️ Head-to-Head: Pipeline vs. Chain-of-Thought

| Outcome | MATH | Science (ARC) |
| --- | --- | --- |
| 🟢 Pipeline wins, CoT was wrong | 4 questions | 14 questions |
| 🔴 CoT wins, pipeline was wrong | **38 questions** | 15 questions |
| ✅ Both correct | 28 questions | 68 questions |
| ❌ Both wrong | 30 questions | 3 questions |

---

## 🔍 Why Did the Pipeline Fail at Maths?

The verification system was **too strict**. When the model attempted non-standard arithmetic (like borrowing in base-7 subtraction), the rules engine wrongly flagged correct steps as errors and deleted them. Across 100 maths questions, **215 valid reasoning nodes were pruned** — the pipeline was erasing its own correct work before it could finish.

---

## ✅ Final Verdict

|  | MATH | Science (ARC) |
| --- | --- | --- |
| **Winner** | Chain-of-Thought | Chain-of-Thought |
| **Pipeline gap** | 🚨 −34% — major regression | ⚠️ −1% — negligible |
| **Worth the extra cost?** | No | No |

**The bottom line:** For this model and these tasks, asking the AI to simply *think out loud* is faster, cheaper, and more accurate than a complex multi-step verification pipeline. The pipeline did show selective promise — it solved 14 science questions CoT missed — but its verification rules need serious recalibration before the architecture can be useful.