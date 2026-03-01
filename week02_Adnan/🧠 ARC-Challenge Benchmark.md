# 🧠 ARC-Challenge Benchmark — Full Strategy Report

> **In plain English:** We tested 7 different ways of asking an AI science questions to find out which approach gives the most correct answers — from simply asking directly, all the way to a complex multi-step reasoning pipeline.
> 

---

## 🎯 What We Did

Using **200 hard science multiple-choice questions**, we ran Microsoft’s Phi-4-mini AI through 7 prompting strategies — each adding more structure and complexity. The goal was to see whether the extra effort translates into better answers.

---

## 🤖 Models & Setup

|  | Details |
| --- | --- |
| **Main AI** | Microsoft Phi-4-mini-instruct |
| **Verifier AI** | Qwen2.5-72B-Instruct (used to double-check reasoning steps) |
| **Hardware** | Tesla P100 GPU · 16 GB VRAM |
| **Dataset** | ARC-Challenge — 200 hard science questions (4 answer choices each) |
| **Random guess score** | 25% (1-in-4 chance) |

---

## 📊 Results — All 7 Strategies Ranked

| Rank | Strategy | Score | Time for 200 Qs |
| --- | --- | --- | --- |
| 🥇 1st | Zero-Shot *(just ask directly)* | **82.5%** | ~1.5 min |
| 🥇 1st | Self-Consistency *(5 votes, majority wins)* | **82.5%** | ~49 min |
| 3rd | Chain-of-Thought *(think out loud)* | 82.0% | ~20 min |
| 3rd | Structured CoT *(forced elimination format)* | 82.0% | ~18 min |
| 5th | SLD-VM — No Verifier | 81.5% | ~64 min |
| 6th | SLD-VM — With AI Verifier | 81.0% | ~147 min |
| 7th | Few-Shot *(show 3 examples first)* | 79.0% | ~1.5 min |

---

## 📉 Performance Chart

```
Score out of 200 questions
────────────────────────────────────────────
Zero-Shot          82.5%  █████████████████████████████████ 🏆
Self-Consistency   82.5%  █████████████████████████████████ 🏆
Chain-of-Thought   82.0%  ████████████████████████████████▊
Structured CoT     82.0%  ████████████████████████████████▊
SLD-VM (no AI)     81.5%  ████████████████████████████████▎
SLD-VM (+ AI)      81.0%  ████████████████████████████████
  Few-Shot         79.0%  ███████████████████████████████▊
```

---

## ⏱️ Accuracy vs Time — The Efficiency Gap

```
Time cost to run 200 questions
────────────────────────────────────────────
Zero-Shot         ~1.5 min   ■  Score: 82.5% ★ Best value
Few-Shot          ~1.5 min   ■  Score: 79.0%
Structured CoT    ~18 min    ■■■■■■  Score: 82.0%
Chain-of-Thought  ~20 min    ■■■■■■■  Score: 82.0%
Self-Consistency  ~49 min    ■■■■■■■■■■■■■■■  Score: 82.5%
SLD-VM (no AI)    ~64 min    ■■■■■■■■■■■■■■■■■■■  Score: 81.5%
SLD-VM (+ AI)     ~147 min   ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■  Score: 81.0%
```

> The SLD-VM pipeline with AI verification used **702 API calls** to the large Qwen model yet scored *lower* than asking the AI directly in under 2 minutes.
> 

---

## ⚔️ Pipeline vs Simple Methods — Head-to-Head

| Compared against | SLD-VM wins | SLD-VM loses | Both right |
| --- | --- | --- | --- |
| Zero-Shot | 12 | 15 | 150 |
| Few-Shot | 19 | 15 | 143 |
| Chain-of-Thought | 22 | 24 | 140 |
| Self-Consistency | 15 | 18 | 147 |

> The pipeline never beats any individual strategy overall, but does *uniquely* solve questions the others miss — suggesting the architecture has selective value, not broad value.
> 

---

## ✅ Final Conclusion

**The simplest method tied for best.** Zero-Shot — just asking the AI the question directly — matched or beat every more complex strategy at 82.5%, completing 200 questions in under 2 minutes.

| Finding | Takeaway |
| --- | --- |
| 🟢 Zero-Shot = best value | 82.5% accuracy in ~1.5 min |
| 🟡 Adding AI verification hurts slightly | −0.5% and 100× more time |
| 🔴 Few-Shot is the worst strategy | Showing examples biases the model |
| 🔵 Complexity ≠ accuracy | 147 min pipeline ≤ 1.5 min direct ask |
| ⭐ Architecture has niche value | Pipeline uniquely solves some Qs others miss |

**Recommendation:** Use Zero-Shot for speed and accuracy. Consider the full pipeline only when individual question precision matters more than overall efficiency — and only after fixing the over-eager verification logic that currently prunes correct reasoning steps.