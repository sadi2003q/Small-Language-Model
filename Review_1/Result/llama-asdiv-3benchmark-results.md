# Llama+ASDiv Guide — 3-Benchmark Evaluation Results

Companion to the earlier **Qwen+ASDiv retrain — 6-benchmark results** report. This
covers the **Llama** side of the same #26/#27 fine-tune-threshold-reconciliation
work — the guide fine-tuned on the corrected ASDiv corpus, cross-architecture
replication for the benchmarks completed so far.

## Results (Llama+ASDiv-FT guide)

| Dataset | N | Base | Guided | Δ | B | C | Self-consistent? |
|---|---|---|---|---|---|---|---|
| CommonsenseQA | 900 | 47.9 | 58.0 | +10.1pp | 194 | 103 | ✅ |
| RACE-High | 500 | 43.0 | 47.4 | +4.4pp | 93 | 71 | ✅ |
| PIQA | 900 | 59.9 | 56.0 | −3.9pp | 234 | 269 | ✅ |

All three self-reconcile — (B−C)/N matches accuracy delta exactly.

## Comparison to Qwen+ASDiv-FT (same 3 benchmarks, from the completed 6-benchmark run)

| Dataset | Qwen+ASDiv-FT Δ | Llama+ASDiv-FT Δ |
|---|---|---|
| CommonsenseQA | +3.4pp | +10.1pp |
| RACE-High | +1.6pp | +4.4pp |
| PIQA | +19.2pp | −3.9pp |

## Interpretation

- **CommonsenseQA and RACE-High replicate directionally across architectures** —
  both positive, Llama actually showing a larger lift on both. Strengthens the
  case that ASDiv-FT guidance transfers cross-architecture for these two tasks.
- **PIQA diverges sharply** — Qwen shows a strong positive gain (+19.2pp) while
  Llama shows a small negative (−3.9pp). This is consistent with the paper's
  already-established **bias-substitution failure mode**: PIQA is the one
  benchmark where guide quality and solver-specific positional bias interact
  unpredictably, and this pattern already appears elsewhere in the paper (Table
  12's Qwen +24.2pp vs. Llama −5.4pp reversal under GSM8K-FT). This is *not* a
  new anomaly — it's the same known failure mode recurring under a different
  fine-tuning source.

## Status — what's still missing

Only 3 of 6 benchmarks are done for Llama+ASDiv-FT. **SVAMP, ASDiv, and
ARC-Challenge still need to be run** for this guide to complete the full
cross-architecture picture (matching what's already done for Qwen+ASDiv-FT).

## Changes required to the manuscript

- Table 13 (secondary Llama replication) should incorporate these corrected
  ASDiv-FT numbers once the corpus-size fix (#7) and remaining 3 benchmarks are
  folded in.
- The PIQA divergence is worth a one-line cross-reference to the existing
  bias-substitution discussion (Analysis section) rather than treated as a new,
  separate finding.
