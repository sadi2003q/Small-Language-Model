# 📊 Performance Results & Conclusion — Phi-4 Eval

> Benchmarking **microsoft/Phi-4-mini-instruct** across 6 prompting strategies on SVAMP and WinoGrande (100 samples each).
> 

<page url="[🧠 Phi-4 Mini — SLD-VM Evaluation Report](https://www.notion.so/Phi-4-Mini-SLD-VM-Evaluation-Report-3164982ee17981019500cc8aae1e0cab?pvs=21)">

---

## 🎯 Full Results Table

All scores are **accuracy (%)** on 100 samples. Strategies are ordered by pipeline phase.

| # | Strategy | SVAMP | WinoGrande | Δ SVAMP vs Best Baseline | Δ Wino vs Best Baseline |
| --- | --- | --- | --- | --- | --- |
| 1 | Zero-Shot | 89.0% | 69.0% | −1.0% | −3.0% |
| 2 | Few-Shot ⭐ | **90.0%** | 67.0% | — | −5.0% |
| 3 | Chain-of-Thought ⭐ | **90.0%** | **72.0%** | — | — |
| 4 | Structured CoT | 85.0% | 69.0% | −5.0% | −3.0% |
| 5 | Self-Consistency (5×) | 88.0% | 70.0% | −2.0% | −2.0% |
| 6 | SC + VCE | **90.0%** | 70.0% | — | −2.0% |

> ⭐ **Best per dataset.** — SVAMP best: Few-Shot & CoT & SC+VCE (90%). WinoGrande best: Chain-of-Thought (72%).
> 

---

## 📊 SVAMP — Performance by Strategy

```
Strategy              Accuracy   ▁▁▁▁▁▁▁▁▁▁ Visual
───────────────────────────────────────────────────────────
Few-Shot              90.0%      ██████████████████  90%
Chain-of-Thought      90.0%      ██████████████████  90%
SC + VCE              90.0%      ██████████████████  90%
Zero-Shot             89.0%      █████████████████   89%
Self-Consistency      88.0%      ████████████████    88%
Structured CoT        85.0%      ███████████████     85%
```

---

## 📊 WinoGrande — Performance by Strategy

```
Strategy              Accuracy   ▁▁▁▁▁▁▁▁▁▁ Visual
────────────────────────────────────────────────────────────────
Chain-of-Thought      72.0%      ██████████████████████  72% 🏆
Self-Consistency      70.0%      █████████████████████   70%
SC + VCE              70.0%      █████████████████████   70%
Zero-Shot             69.0%      ████████████████████    69%
Structured CoT        69.0%      ████████████████████    69%
Few-Shot              67.0%      ███████████████████     67%
Random Baseline       50.0%      ███████████████         50%
```

---

## 🏆 Strategy Rankings (Sorted by Performance)

### SVAMP — Ranked

| Rank | Strategy | Accuracy |
| --- | --- | --- |
| 🥇 1st | Few-Shot | 90.0% |
| 🥇 1st | Chain-of-Thought | 90.0% |
| 🥇 1st | SC + VCE | 90.0% |
| 🥈 4th | Zero-Shot | 89.0% |
| 🥉 5th | Self-Consistency | 88.0% |
| 6th | Structured CoT | 85.0% |

### WinoGrande — Ranked

| Rank | Strategy | Accuracy |
| --- | --- | --- |
| 🥇 1st | Chain-of-Thought | 72.0% |
| 🥈 2nd | Self-Consistency | 70.0% |
| 🥈 2nd | SC + VCE | 70.0% |
| 🥉 4th | Zero-Shot | 69.0% |
| 🥉 4th | Structured CoT | 69.0% |
| 6th | Few-Shot | 67.0% |

---

## 🔍 Failure Analysis Highlights

From examining errors in the zero-shot baseline:

| Dataset | Common Failure Pattern | Example |
| --- | --- | --- |
| SVAMP | Model applies real-world common sense to refuse impossible arithmetic | “Bobby can’t eat 34 candies if he only has 20” — model refuses instead of computing |
| SVAMP | Over-counting when problem involves subtraction from a larger pool | Predicts 0 instead of remainder |
| WinoGrande | Pronoun resolution fails when both entities are syntactically similar | Picks wrong antecedent when context requires world knowledge |
| WinoGrande | Few-shot examples hurt by biasing toward a particular answer pattern | Few-shot ↓ vs Zero-shot / CoT ↑ |

> **Key insight:** The model applies overly literal real-world reasoning to SVAMP problems, treating impossible scenarios as invalid rather than solving arithmetically as intended.
> 

---

## ✅ Final Conclusion

- 💡 Expand Full Conclusion
    
    **SVAMP:** Phi-4-mini-instruct is already a strong mathematical reasoner out-of-the-box. Simple zero-shot prompting achieves 89% — already above the expected 55–70% range. Few-Shot and CoT tie at 90%, effectively the ceiling on this dataset size. Structured CoT unexpectedly *hurt* performance (85%), likely because rigid formatting prevents the model from leveraging its natural reasoning style. Self-Consistency and SC+VCE recover to 90% but add significant compute cost for zero net gain.
    
    **WinoGrande:** The task is harder for this model class. CoT is the clear winner at 72%, giving the model space to reason through coreference explicitly. Few-Shot *hurts* performance (67%), suggesting that commonsense examples bias the model toward specific patterns that don’t generalise. Advanced techniques like Self-Consistency only marginally improve over zero-shot (70% vs 69%), and VCE overrides provided no benefit (0 corrections).
    

### 📌 Key Takeaways

| Finding | Detail |
| --- | --- |
| 🟢 Phi-4-mini is exceptionally strong at math | 89–90% SVAMP accuracy beats expected benchmarks by ~20pp |
| 🟡 Commonsense reasoning has a ceiling around 70–72% | WinoGrande remains challenging; CoT is the only reliable boost |
| 🔴 Complex pipelines add cost, not accuracy | SC (5×) takes 5× compute but delivers no improvement on either dataset |
| 🔵 Structured CoT can hurt | Forcing rigid step formats degrades SVAMP by 5pp |
| 🟠 Few-Shot is task-dependent | Best for SVAMP, worst for WinoGrande — choose per task |
| ⭐ Best overall strategy: CoT | Ties for best on SVAMP, wins on WinoGrande — and is fast |

> **Recommendation:** For Phi-4-mini, use simple Chain-of-Thought prompting. It achieves peak performance on both tasks with minimal compute overhead, and avoids the pitfalls of over-engineered pipelines.
>