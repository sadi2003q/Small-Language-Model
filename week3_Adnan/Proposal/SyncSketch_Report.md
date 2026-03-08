# SyncSketch: Persistent Symbolic Memory for Notation-Consistent SLM-Driven Scientific Visualization
**Research Proposal & 6-Month Roadmap**
*PaperBanana (Google, Jan 2026)*

---

## 1. The Problem

PaperBanana automates scientific diagram generation using Small Language Models (SLMs). While promising, it suffers a critical flaw: **symbolic inconsistency**.

When a researcher writes a paper with a defined notation — say, the attention weight matrix is labeled *W_attn* — PaperBanana's SLM often generates a diagram that labels the same component *W_a*, *W*, or something entirely different. This is not a minor visual bug. In academic science, **a wrong symbol = wrong meaning**.

### Why SLMs Make This Worse

This problem is especially severe with SLMs (vs. large models like GPT-4) for three reasons:

- **Short effective context window** — the notation was defined on page 2; the diagram is generated from page 8. The SLM has already "forgotten" it.
- **Limited abstraction capacity** — SLMs struggle to maintain long-range symbolic mappings across a full paper.
- **No dedicated memory** — the drawing agent has no structured external reference to fall back on; it guesses from local context, causing inconsistency across multiple diagrams in the same paper.

This is not a prompting issue. It is a **structural architectural gap**.

---

## 2. How It Affects Research

| Impact Area | Effect |
|---|---|
| **Scientific Accuracy** | Diagrams misrepresent the paper's actual methodology |
| **Peer Review** | Reviewers catch notation mismatches — paper gets rejected |
| **Reproducibility** | Other researchers misread the architecture from the figure |
| **Trust in Automation** | Researchers abandon the tool after first mismatch |

The downstream effect is serious: a tool meant to save time ends up creating **error-prone diagrams that require manual correction anyway** — defeating its own purpose.

---

## 3. Proposed Solution: Notation-Synced Multi-Agent Framework with Persistent Symbolic Memory

Instead of relying on a single SLM to both *understand the paper* and *draw the diagram*, we split the responsibility into two specialized agents — connected through a **shared external JSON memory file** that acts as the system's persistent symbolic brain.

---

### The Core Idea: External JSON Memory

The system maintains a structured JSON memory file per paper session:

```json
{
  "paper_id": "attention_is_all_you_need",
  "notation_memory": {
    "attention_weight": "W_attn",
    "query_matrix": "W^Q",
    "key_matrix": "W^K",
    "hidden_state": "h_t",
    "loss_function": "L_ce"
  },
  "flagged_ambiguous": ["W", "h"],
  "last_updated_page": 6,
  "figures_generated": ["fig1_encoder", "fig2_decoder"]
}
```

This file is **read, queried, and written back to** by both agents — persisting across the entire paper session. It is not a prompt. It is structured memory that survives across multiple diagram generation calls.

---

### Agent 1 — The Notation Auditor
- Reads the full paper (PDF/LaTeX source)
- Extracts every defined symbol, variable, and label
- Writes results into the **JSON memory file** as the ground truth Notation Dictionary
- Flags ambiguous or overloaded symbols for human review
- Updates memory if the user manually corrects a symbol

### Agent 2 — The Drawing Agent
- Before generating any diagram, **reads the JSON memory file**
- Cannot output a label not present in `notation_memory`
- After generating, writes the figure ID into `figures_generated` so all future diagrams stay consistent with previous ones
- If a symbol is in `flagged_ambiguous`, it pauses and asks the user to clarify

### Why This Architecture Is Novel

| Standard SLM Approach | SyncSketch Approach |
|---|---|
| Notation lives only in the prompt | Notation lives in **persistent external memory** |
| Each diagram call starts from zero | Each call **reads warm memory** — no re-extraction |
| 1 diagram can be consistent | **All diagrams across a paper are consistent** |
| Memory lost between sessions | JSON file can be **saved, versioned, and reused** |

The Auditor offloads the long-range memory problem entirely. The Drawing Agent operates in a constrained, grounded symbol space — it no longer needs to remember anything; it just looks up.

This also means if a researcher generates 5 diagrams from the same paper over 3 days, **the notation stays identical across all of them** — something no current SLM-based tool can guarantee.

---

## 4. Tools & Tech Stack

| Component | Tool / Library |
|---|---|
| **PDF Parsing** | PyMuPDF or pdfplumber |
| **LaTeX Symbol Extraction** | Custom regex + SymPy for math parsing |
| **SLM Framework** | Hugging Face Transformers (local inference) |
| **Agent Orchestration** | LangGraph or Microsoft AutoGen |
| **Persistent Memory** | JSON file (per-paper session) + Python `json` module |
| **Memory Schema Validation** | Pydantic (ensures JSON structure integrity) |
| **Diagram Output** | TikZ (via LaTeX) or SVG |
| **Evaluation** | Custom symbol-match scoring script (precision/recall on notation) |
| **Experiment Tracking** | Weights & Biases (wandb) |

---

## 5. Models to Use

| Role | Recommended Model | Why |
|---|---|---|
| **Notation Auditor** | Phi-3 Mini / Qwen2.5-3B | Strong at extraction tasks, low compute |
| **Drawing Agent** | Phi-3.5 / Mistral-7B (quantized) | Better code generation for TikZ/SVG |
| **Baseline Comparison** | PaperBanana's original SLM | To prove your method fixes the gap |

> **Note:** Keep both agents under 7B parameters. This keeps it clearly in SLM territory, which strengthens your paper's contribution claim.

---

## 6. 6-Month Roadmap

```
Month 1 — Problem Validation
  ├── Collect 30–50 real academic papers with complex notation
  ├── Run PaperBanana on them
  └── Measure baseline symbol mismatch rate (your motivation data)

Month 2 — Build the Notation Auditor + JSON Memory Schema
  ├── PDF/LaTeX parser → symbol extractor
  ├── Design and validate JSON memory schema (using Pydantic)
  ├── Build write/read/update logic for the memory file
  └── Test extraction accuracy on collected papers

Month 3 — Build the Drawing Agent + Full Integration
  ├── Prompt-engineer Drawing Agent to read from JSON memory
  ├── Implement ambiguity-pause logic (flagged symbols)
  ├── Connect both agents via LangGraph
  └── Generate multi-diagram sequences end-to-end from one paper

Month 4 — Evaluation
  ├── Compare: PaperBanana vs. SyncSketch (single diagram)
  ├── Compare: PaperBanana vs. SyncSketch (multi-diagram, same paper)
  ├── Measure: symbol precision, recall, cross-figure consistency score
  └── Run on held-out test set of papers

Month 5 — Writing
  ├── Write paper: Introduction, Related Work, Method, Results
  ├── Key contribution framing: persistent external symbolic memory
  └── Target venue: EMNLP, ACL Findings, or arXiv first

Month 6 — Buffer + Submission
  ├── Revisions, figures, proofreading
  └── Submit
```

---

## 7. Expected Contribution

> *"We propose SyncSketch — a two-agent SLM framework with persistent external JSON symbolic memory, where a dedicated Notation Auditor builds and maintains a structured notation dictionary that grounds a Drawing Agent across all diagram generation calls. Our approach reduces notation mismatch by X% over the PaperBanana baseline and, uniquely, enforces cross-figure symbolic consistency for multi-diagram paper sessions."*

**Two measurable claims:**
1. Lower symbol mismatch rate on single diagrams
2. Consistent notation across multiple diagrams from the same paper — a problem no prior work addresses

---
*Report prepared March 2026*
