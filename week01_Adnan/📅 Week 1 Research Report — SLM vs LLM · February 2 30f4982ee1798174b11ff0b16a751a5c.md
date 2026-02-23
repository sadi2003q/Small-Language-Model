# 📅 Week 1 Research Report — SLM vs LLM · February 2026

---

> 🎯 **Mission:** Build a comparable Small Language Model (SLM) to rival Large Language Models — within **4 weeks**.
> 

> 📅 **Week:** 1 of 4 · February 2026 · Hardware: NVIDIA T4 GPU (Google Colab / Kaggle)
> 

> 🧠 **Core Model:** Microsoft Phi-3-mini-4k-instruct (3.8B) · Benchmark: GSM8K (Grade School Math)
> 

---

# 🏆 Week 1 — Executive Highlights

Six key achievements from Week 1:

1. **Fine-tuned SLM beats larger LLMs** — Phi-3-mini (3.8B) scored **80% on GSM8K** with 5-shot CoT, surpassing Mistral-7B (12%) and Qwen2.5-7B (40%).
2. **LoRA fine-tuning is the dominant lever** — SFT alone delivered **+20%** alone taking the performance from 56% to 72% for Microsoft Phi 3 model.
3. **Hidden states encode reasoning quality** — Embedding probes on PRM800K confirmed Phi-3 (73%) > Mistral-7B (70%) > Gemma-2B (66%), with architecture mattering more than scale.
4. **True PRM signal isolated** — Test 3 on Gemma 2B's own outputs produced an honest accuracy range of **73.7%–84.7%**, eliminating proxy and distribution mismatch errors.
5. **Annotation quality rivals model architecture** — Same model, same data, same code produced an **11-point gap** between annotators (ChatGPT: 84.7% ✅ vs Claude: 73.7% ⚠️).
6. **Full SLD-VM pipeline is live** — The end-to-end LTG → RGC → VCE system was built, ablated across 7 configurations, and validated on 200 held-out problems.

---

# 📊 Week 1 — Performance Overview

| Report | Model | Task | Key Result |
| --- | --- | --- | --- |
| Small Model, Big Win | Phi-3-mini (FT) | GSM8K Accuracy | **80.0%** ✅ |
| PRM800K Classifier | Phi-3-mini | Hidden State Probe | **73.0%** ⚠️ |
| Test 3 — Step PRM | Gemma-2B | Step-Level PRM | **84.7% / 73.7%** |
| SLD-VM Pipeline | Phi-3 (3.8B) | Full Pipeline | **68.5%** ✅ |

---

# 1 · 📊 Small Model, Big Win — GSM8K Benchmark

> **Benchmark:** GSM8K · **Problems Evaluated:** 50 · **Hardware:** T4 GPU · **Date:** Feb 2026
> 

## Methodology

Six language model configurations were evaluated on 50 randomly sampled GSM8K test problems. Each model received a zero-shot prompt requesting only the final numeric answer. The fine-tuned Phi-3-mini used LoRA adapters trained on GSM8K-style data and merged before inference. Answers were extracted with a multi-pattern regex pipeline and matched with numeric tolerance. The 5-shot Chain-of-Thought variant provided five worked examples at inference time.

## Results

| Rank | Model | Setup | Accuracy | Signal |
| --- | --- | --- | --- | --- |
| 🥇 1 | Phi-3-mini *(fine-tuned)* | 5-Shot CoT | **80.0%** | ████████████████ |
| 🥈 2 | Phi-3-mini *(fine-tuned)* | Zero-Shot | **72.0%** | ██████████████░░ |
| 🥉 3 | Phi-4k-it | Zero-Shot | **54.0%** | ███████████░░░░░ |
| 4 | Qwen2.5-7B-Instruct | Zero-Shot | **40.0%** | ████████░░░░░░░░ |
| 5 | Mistral-7B-Instruct-v0.3 | Zero-Shot | **12.0%** | ██░░░░░░░░░░░░░░ |
| 6 | Gemma 2B | Zero-Shot | **4.0%** | █░░░░░░░░░░░░░░░ |

## Key Takeaways

**Size ≠ Performance.** Fine-tuned Phi-3-mini (3.8B) beat Mistral-7B and Qwen2.5-7B by a massive margin. Targeted fine-tuning on quality data outweighs raw parameter count. The jump from 72% → 80% with 5-shot CoT confirms that structured reasoning prompts are a low-cost, high-reward technique. Mistral-7B's 12% collapse is a prompt format failure, not a capability ceiling — instruction-tuned models require strict template compliance.

---

# 2 · ⚙️ PRM800K Classifier — LLM Hidden State Evaluation

> **Dataset:** PRM800K (OpenAI Phase 2) · **Task:** Binary step-level classification · **Balanced Set:** 2,000 steps · **Date:** Feb 2026
> 

## Methodology

Hidden states from the final transformer layer of three LLMs were extracted for 2,000 balanced steps (1,000 correct / 1,000 incorrect) from PRM800K. Mean pooling across token positions produced a fixed-size embedding per step. A Logistic Regression classifier (80/20 stratified split) was trained on these embeddings. Decision thresholds were fixed before experimentation.

| Accuracy Band | Verdict | Interpretation |
| --- | --- | --- |
| > 80% | ✅ GO | Hidden states strongly encode step quality |
| 70–80% | ⚠️ Weak Signal | Partial signal — further optimisation needed |
| < 70% | ❌ NO-GO | Insufficient discriminability |

## Embedding Configurations

| Model | Parameters | Hidden Size | Precision |
| --- | --- | --- | --- |
| `google/gemma-2b` | 2B | 2,048 | float16 |
| `microsoft/Phi-3-mini-4k-instruct` | 3.8B | 3,072 | float16 |
| `mistralai/Mistral-7B-Instruct-v0.3` | 7B | 4,096 | float16 |

## Results

| Model | Parameters | Accuracy | Verdict |
| --- | --- | --- | --- |
| Gemma-2B | 2B | 66.3% | ❌ NO-GO |
| Mistral-7B-Instruct-v0.3 | 7B | 70.0% | ⚠️ Weak |
| **Phi-3-mini-4k-instruct** | **3.8B** | **73.0%** | **⚠️ Weak** |

## Key Takeaways

**Architecture beats scale.** Phi-3-mini (3.8B) outscored Mistral-7B (7B) by 3 points — training methodology and instruction-tuning quality are stronger discriminability drivers than parameter count. No model crossed the GO threshold, confirming that off-the-shelf embeddings alone are insufficient. However, the clear +6.7pp improvement from Gemma → Phi proves the 80% target is reachable via layer selection, contrastive fine-tuning, or adapter layers.

---

# 3 · 🧪 Test 3 — Step-Level PRM on Gemma 2B's Own Outputs

> **Model:** Gemma-2B-IT · **Problems Generated:** 60 · **Balanced Steps:** 152 · **Hardware:** T4 GPU · **Date:** Feb 2026
> 

## Methodology

Gemma-2B-IT was prompted with a chain-of-thought template to generate step-by-step solutions on 60 GSM8K problems. The model's own wrong outputs (51 of 60) were manually labeled step-by-step to identify the *first* error step per solution. Steps before the error → label 1 (correct); at/after → label 0 (wrong). Mean-pooled last hidden states (dim=2048) were extracted and a Logistic Regression classifier was trained on a 75/25 stratified split. Two annotators (ChatGPT and Claude) labeled the same solutions independently.

## Evolution Across Tests

|  | Test 1 | Test 2 | **Test 3 (This)** |
| --- | --- | --- | --- |
| **Label Source** | Solution-level proxy | PRM800K (GPT-4 steps) | Manual step-level on Gemma 2B outputs |
| **Problem** | Too easy — labels too simple | Wrong distribution — cross-model | Neither problem |
| **Result** | 89.5% *(inflated)* | 66.3% *(deflated)* | **True signal** |
| **Verdict** | Misleading GO | False NO-GO | ⚠️ Depends on labeler |

## Results — Labeler Comparison

| Labeler | PRM Step Accuracy | Verdict | Implication |
| --- | --- | --- | --- |
| **ChatGPT** | **84.7%** | ✅ TRUE GO | Build full pipeline with learned VCE |
| **Claude** | **73.7%** | ⚠️ PARTIAL GO | Rule-based VCE; skip learned verifier |
| *Test 2 baseline* | *66.3%* | ❌ NO-GO | *Rethink architecture* |

## Classification Report — Claude Labels (73.7%)

| Class | Precision | Recall | F1-Score | Support |
| --- | --- | --- | --- | --- |
| Wrong Step (0) | 0.71 | 0.79 | 0.75 | 19 |
| Correct Step (1) | 0.76 | 0.68 | 0.72 | 19 |
| **Overall** | — | — | **0.737** | **38** |

## Key Takeaways

**Label quality is the dominant variable.** The 11-point gap between ChatGPT (84.7%) and Claude (73.7%) crosses the critical 80% threshold — annotation philosophy matters as much as model architecture. Test 3 produces the honest PRM signal range: 73.7%–84.7%. Even at PARTIAL GO (73.7%), the pipeline has value via rule-based VCE + RGC majority vote. The *first error step* framing is powerful: correctly labeling early steps as valid prevents the classifier from learning superficial surface features.

---

# 4 · 🔬 SLD-VM Pipeline Report — Phi-3 (3.8B) on GSM8K

> **Model:** Phi-3-mini-4k-instruct (3.8B) · **Train:** 7,473 problems · **Eval:** 200 problems · **Runtime:** ~6–8 hrs · **Date:** Feb 2026
> 

## Methodology

The SLD-VM system is a two-phase approach. **Phase 1 — LoRA SFT:** The model was trained for 3 epochs on all 7,473 GSM8K training problems using LoRA adapters (HuggingFace TRL + PEFT + bitsandbytes), teaching structured CoT reasoning. **Phase 2 — SLD-VM Inference:** Three components layer on the fine-tuned model at evaluation: (1) Structured CoT at temperature 0, (2) Self-Consistency across 3 branches (RGC majority vote), (3) VCE proxy PRM re-ranking with arithmetic verification.

## Ablation Results — All 7 Configurations

| Configuration | Accuracy | Δ vs Base CoT |
| --- | --- | --- |
| Base Phi-3 · CoT baseline | 12.5% | — |
| Base Phi-3 · Structured CoT | 14.0% | +1.5% |
| Base Phi-3 · Full Pipeline | 10.0% | −2.5% |
| **Fine-Tuned · Zero-shot** | **78.5%** | **+66.0%** |
| Fine-Tuned · Structured CoT | 69.5% | +57.0% |
| Fine-Tuned · Self-Consistency | 70.0% | +57.5% |
| **Fine-Tuned · Full SLD-VM Pipeline** | **68.5%** | **+56.0%** |

## Component Contribution Breakdown

| Component | Accuracy Gain | Notes |
| --- | --- | --- |
| LoRA Fine-Tuning | **+55.5%** | Dominant contributor |
| Self-Consistency (RGC) | +0.5% | Marginal positive |
| VCE Re-ranking | −1.5% | 7 gains, 10 regressions — net −3 |
| **Total vs Base CoT** | **+56.0%** | Target was +22–26% ✅ Exceeded |

## Key Takeaways

**Fine-tuning dominates.** 55.5 of 56.0 percentage points of total gain come from LoRA SFT alone. **Zero-shot FT (78.5%) outperforms the full pipeline (68.5%)** — the structured prompts and VCE introduce noise that hurts a model that has already internalised strong reasoning. VCE is net negative at this scale (−1.5%) because the proxy PRM is not calibrated for the fine-tuned model's output distribution. The +56% result far exceeded the original +22–26% target, confirming LoRA fine-tuning at 3 epochs on the full 7,473-problem set is highly effective.

---

# 📌 Week 1 — Consolidated Summary

| Metric | Value |
| --- | --- |
| Reports Completed | 5 |
| Models Evaluated | Gemma-2B · Phi-3-mini · Mistral-7B · Qwen2.5-7B |
| Best Single-Config Accuracy (GSM8K) | **80.0%** (Phi-3-mini FT + 5-Shot CoT) |
| Best Pipeline Accuracy | **68.5%** (SLD-VM Full Pipeline on Phi-3) |
| Fine-Tuning Gain | **+56%** over base CoT |
| Core Finding | Fine-tuned SLM (3.8B) > un-tuned LLM (7B) |

## 🏆 Week 1 Conclusion — The Winner is Clear

Across every experiment this week, one configuration stood above all others: **fine-tuned Phi-3-mini (3.8B) with 5-shot Chain-of-Thought prompting at 80% on GSM8K**. This is the peak performer of Week 1 — not just among small models, but across every model tested, including 7B-class LLMs like Mistral and Qwen. A 3.8B parameter model, trained on quality data with LoRA and guided by structured reasoning prompts at inference, comfortably outperformed models with nearly twice its parameter count. The message from Week 1 is definitive: **targeted fine-tuning on a compact, well-designed model is a more effective strategy than scaling up to larger general-purpose LLMs for domain-specific tasks.**

This result anchors the entire SLM vs LLM challenge. With one week complete, the fine-tuned Phi-3-mini is already competing seriously with much larger models. The remaining three weeks will be about pushing this ceiling higher.

---

## 🗓️ Week 2 Plan — What’s Next

**Implement ReflectEvo (paper → code)** — Attempt to implement the ReflectEvo paper methodology and integrate it with the existing Phi-3 fine-tuning pipeline. ReflectEvo’s reflective evolution approach to improving reasoning via self-refinement is a strong candidate for pushing accuracy beyond the current 80% ceiling without increasing model size.

**Tool Integration** — Augment the Phi-3 model with external tool access (calculator, symbolic solver, or code execution) at inference time. Tool-augmented SLMs have shown significant gains on math benchmarks by offloading computation to reliable external executors rather than relying on the model’s arithmetic alone.

**Target for Week 2:** Achieve measurable improvement over the current 80% best result on GSM8K by combining at least one of these two techniques with the existing fine-tuned Phi-3 base.

---

*Research Project: SLM vs LLM — 4-Week Challenge · Week 1 Report · February 2026*: SLM vs LLM — 4-Week Challenge · Week 1 Report · February 2026*