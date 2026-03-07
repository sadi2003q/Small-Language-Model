# Research Proposal: PlanCollab
## Role-Specialized Small Language Model Collaboration for Long-Horizon Constrained Planning

---

## 1. The Problem

Large Language Models (LLMs) like GPT-4 and Claude are powerful planners — but they are expensive, closed-source, and require internet access. The natural question is: **can Small Language Models (SLMs) replace them for planning tasks?**

The DeepPlanning benchmark (January 2026) answers that honestly: **No — not yet.** Their paper introduces a rigorous benchmark for long-horizon planning with local constraint reasoning and reveals three critical failure modes in current AI agents:

- **Tool Call Omission** — Agents forget to call required tools as plans grow longer
- **Implicit Constraint Blindness** — Agents miss constraints that are not explicitly stated (e.g., budget limits implied by context)
- **No Backtracking** — When a plan step fails, agents cannot recover; they have no mechanism to revise

These failures were documented for frontier LLMs. For SLMs (7B–14B parameters), **the performance is even worse** — and no study has proposed a fix specifically for SLMs on this benchmark. That is the exact gap this research fills.

---

## 2. What I Am Trying to Solve

This research asks one central question:

> *Can a pipeline of small, specialized SLMs collectively solve long-horizon planning tasks that a single large LLM struggles with?*

Specifically, the goal is to address all three DeepPlanning failure modes **without fine-tuning** and **without using frontier LLMs** — using only open-source SLMs (7B or smaller) accessible via free API tiers.

The hypothesis is: **role separation + constraint memory = better planning.** A single SLM tries to do everything at once and fails. Four SLMs, each doing one job, can outperform it.

---

## 3. How I Am Solving It — The PlanCollab Pipeline

The proposed system assigns four distinct roles to lightweight SLMs:

```
User Query
    │
    ▼
┌─────────────────┐
│  Planner SLM    │  ← Generates the initial step-by-step plan
│  (Qwen2.5-7B)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Critic SLM     │  ← Challenges the plan: "Is this step feasible?"
│  (Mistral-7B)   │
└────────┬────────┘
         │
         ▼
┌──────────────────────┐
│  Constraint Checker  │  ← Verifies ALL constraints (explicit + implicit)
│  (Phi-3-mini)        │     using a JSON Constraint Memory Log
└────────┬─────────────┘
         │  (if violation detected)
         ▼
┌─────────────────┐
│  Replanner SLM  │  ← Receives violation log → fixes the plan
│  (Qwen2.5-7B)   │
└────────┬────────┘
         │
         ▼
    Final Plan ✅
```

### The Key Mechanism: Constraint Violation Tracker (CVT)

A lightweight JSON memory object that logs every constraint violation across planning steps and passes it back to the Replanner. This is the core technical contribution — a simple but explicit mechanism that prevents the same constraint from being violated twice.

```json
{
  "violated_constraints": [
    { "step": 3, "type": "implicit", "description": "Exceeded budget limit", "fix_required": true }
  ]
}
```

No fine-tuning. No GPU required. Runs entirely on **Groq free tier API**.

---

## 4. How My Work Is Different From Others

| Prior Work | What They Did | What's Missing |
|---|---|---|
| DeepPlanning (2026) | Benchmarked frontier LLMs on long-horizon planning | No SLM evaluation, no fix proposed |
| SLM-MATRIX (2025) | Multi-agent SLM collaboration for reasoning | Not tested on planning; no constraint tracking |
| SYMPHONY (NAACL 2025) | Heterogeneous multi-agent collaboration | Uses large models only; no backtracking mechanism |
| SLM-Bench (EMNLP 2025) | Benchmarked 15 SLMs on 9 NLP tasks | Zero planning tasks included |

**My contribution is the intersection nobody has done:**
- SLMs (not LLMs) + Role specialization + Constraint memory + DeepPlanning benchmark

This is novel not because the components are new, but because **combining them to fix explicit, documented failures in a brand-new benchmark** has not been done.

---

## 5. Target Publication

**Primary Target:** EMNLP 2026 Workshop *(Deadline: ~June 2026)*

**Why EMNLP workshop:**
- Workshop papers require a solid method + experiments, not a full ablation study
- EMNLP actively publishes SLM and multi-agent NLP work
- 6-month timeline is realistic for this scope
- Workshop acceptance strengthens the CV for future submissions

**Backup Target:** IEEE Access Journal *(Rolling submission, ~3 month review)*

**Realistic acceptance probability:** 70–75% if experiments show even modest improvement over single-SLM baseline.

---

## 6. How to Proceed — 6-Month Plan

### Month 1 — Setup & Baseline (March 2026)
- [ ] Read DeepPlanning paper fully; note exact metrics and failure examples
- [ ] Download DeepPlanning dataset from HuggingFace
- [ ] Set up Groq API (free) with Qwen2.5-7B and Mistral-7B
- [ ] Run single-SLM baseline on DeepPlanning tasks → record scores

### Month 2 — Build the Pipeline (April 2026)
- [ ] Implement the 4-agent PlanCollab pipeline (~200 lines Python)
- [ ] Build the Constraint Violation Tracker (JSON memory log)
- [ ] Run PlanCollab on same DeepPlanning tasks → compare scores

### Month 3 — Experiments & Analysis (May 2026)
- [ ] Ablation study: pipeline with/without CVT; pipeline with 2 vs 4 agents
- [ ] Error analysis: which constraint types still fail and why
- [ ] Optional: add multilingual test (Bangla or Arabic) for extra novelty

### Month 4 — Writing (June 2026)
- [ ] Write paper (8 pages ACL format)
- [ ] Sections: Abstract → Introduction → Related Work → Method → Experiments → Analysis → Conclusion
- [ ] Get feedback from peers or supervisor

### Month 5–6 — Submission & Revision
- [ ] Submit to EMNLP 2026 workshop
- [ ] If rejected: revise and submit to IEEE Access
- [ ] Begin planning follow-up paper with LoRA fine-tuning

---

## 7. Tools & Resources Required

| Resource | Cost |
|---|---|
| Groq API (Qwen2.5-7B, Mistral-7B) | Free |
| Google Colab Pro | Paid |
| DeepPlanning Dataset | Free (HuggingFace) |
| Phi-3-mini via HuggingFace API | Free |

**Total estimated cost: < $10/month**

---

*Proposal prepared: March 2026*
