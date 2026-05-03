# GuidedVote: Verbal Reasoning Richness Governs SLM-to-SLM Guided Reasoning

## 📌 Overview

This repository contains the implementation of **GuidedVote**, a two-stage inference framework for improving reasoning performance in Small Language Models (SLMs).

Instead of scaling model size or relying on large proprietary models, GuidedVote introduces a **guide–solver architecture**, where a fine-tuned guide model generates structured reasoning plans that help a frozen solver model produce more accurate answers.

---

## 🧠 Key Idea

Our research shows that:

* **Verbal reasoning richness** is more important than domain similarity
* A guide trained on rich, multi-step reasoning data generalizes better across tasks
* Small models can collaborate effectively without requiring large-model supervision

This leads to the **Domain Proximity Paradox**, where out-of-domain training can outperform in-domain training.

---

## ⚙️ Method: GUIDEDVOTE Pipeline

### Stage 1 — Plan Generation

A fine-tuned guide model generates a structured reasoning plan:

* Step-by-step decomposition (2–5 steps)
* No direct calculations
* Focus on reasoning structure

### Stage 2 — Guided Voting

* The solver receives: *(question + reasoning plan)*
* Generates multiple answers (K = 5)
* Final output = **majority vote**

---

## 📊 Results

* Up to **+24.2 percentage points improvement**
* Average gain: **+13.5 points**
* **30–47% lower compute cost** than large-model baselines
* Improved calibration and reduced bias

---

## 🧪 Datasets Used

We evaluate our method on six benchmark datasets:

* **SVAMP** (Arithmetic reasoning)
* **ASDiv** (Arithmetic reasoning)
* **PIQA** (Physical commonsense)
* **CommonsenseQA** (Commonsense reasoning)
* **ARC-Challenge** (Science questions)
* **RACE-High** (Reading comprehension)

---

## 💻 Environment

Experiments were conducted using:

* GPU: **NVIDIA T4**
* Platforms:

  * Kaggle Notebooks
  * Google Colab

---

## 🚀 How to Run

### 1. Install Dependencies

```bash
pip install torch transformers datasets peft
```

### 2. Run Notebooks

Each notebook corresponds to a dataset/experiment.

Example:

```bash
notebook-10-arc-challenge-three-angles.ipynb
```

### Typical Workflow:

1. Load dataset
2. Generate reasoning plans using guide model
3. Run guided inference with solver
4. Evaluate results

---

## 🔬 Key Components

### Guide Model

* ~3B parameter model
* Fine-tuned using LoRA
* Trained with **Structured Plan Generation Fine-Tuning (SPGFT)**

### Solver Model

* 1–1.5B parameter model
* Frozen (no fine-tuning)
* Uses majority voting

---

## 📉 Contributions

* Proposes the **Verbal Richness Hypothesis (VRH)**
* Identifies the **Domain Proximity Paradox**
* Introduces **SPGFT** for structured reasoning training
* Defines two failure modes:

  * Bias-substitution
  * Confident misdirection
* Provides a **four-tier task taxonomy** for deployment

---


---

## 👨‍💻 Authors

* Md. Adnan Abdullah Sadi
* Makki Ammer Sakib
* Nahian Syed Ahanaf

---




