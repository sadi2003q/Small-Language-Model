# Qwen+ASDiv Guide Retrain — 6-Benchmark Re-Evaluation Results

Addresses Reviewer #1, Major Concern #7 (SPGFT filter threshold reconciliation) and
contributes to Concerns #6 (monotonic richness ordering) and #8 (corpus-size confound).

## Background

Re-running the SPGFT filter with the corrected, single word-limit threshold changed
the Qwen+ASDiv accepted corpus materially: **1540 → 1870 plans (+21.4%)** — the only
one of six model×dataset conditions to shift beyond noise level. This required
retraining the Qwen+ASDiv guide (previously missing/outdated) and re-evaluating it
across all six benchmarks.

## Results (new Qwen+ASDiv-FT guide, corrected 1870-plan corpus)

| Dataset | N | Base | Guided | Δ | B | C | (B−C)/N | Self-consistent? |
|---|---|---|---|---|---|---|---|---|
| SVAMP | 300 | 39.3 | 53.3 | +14.0pp | 81 | 39 | +14.0pp | ✅ |
| ASDiv | 300 | 54.7 | 63.7 | +9.0pp | 62 | 35 | +9.0pp | ✅ |
| ARC-Challenge | 900 | 71.8 | 81.0 | +9.2pp | 134 | 51 | +9.2pp | ✅ |
| CommonsenseQA | 900 | 71.1 | 74.6 | +3.4pp | 120 | 89 | +3.4pp | ✅ |
| RACE-High | 500 | 58.0 | 59.6 | +1.6pp | 67 | 59 | +1.6pp | ✅ |
| PIQA | 900 | 56.8 | 76.0 | +19.2pp | 304 | 131 | +19.2pp | ✅ |

All six rows satisfy (B−C)/N = Δ exactly — clean, internally consistent data across
the full benchmark suite.

## Comparison to original Table 13 (old 1540-plan guide)

| Dataset | Old guided (Δ) | New guided (Δ) | Change |
|---|---|---|---|
| SVAMP | 49.3 (+9.0) | 53.3 (+14.0) | +4.0pp |
| ASDiv | 57.3 (+3.6) | 63.7 (+9.0) | +6.4pp |
| ARC-Challenge | 74.7 (+3.0) | 81.0 (+9.2) | +6.3pp |
| CommonsenseQA | 74.0 (+3.3) | 74.6 (+3.4) | +0.6pp |
| RACE-High | 59.0 (+1.3) | 59.6 (+1.6) | +0.6pp |
| PIQA | 72.9 (+16.6) | 76.0 (+19.2) | +3.1pp |

The retrained guide improves on every benchmark — expected, given the larger
corrected training corpus.

## What this means for the paper's claims

- **Concern #7 resolved:** filter threshold reconciled; Table 2/3's Qwen+ASDiv
  acceptance stats and this guide's downstream results are now generated from a
  single, consistent threshold.
- **Concern #6 (richness ordering):** the ASDiv-FT guide is now meaningfully
  stronger, narrowing its gap to GSM8K-FT. Table 16 needs its ASDiv-FT column
  replaced with these numbers, and the GSM8K > SVAMP > ASDiv ordering re-checked
  per benchmark — expected to hold, but by a smaller margin than before, which is a
  more defensible version of the claim.
- **Concern #8 (corpus-size confound):** ASDiv's corpus (1870) is now closer in size
  to GSM8K's (2818) than before (1540). If GSM8K-FT still outperforms ASDiv-FT after
  this size gap narrowed, that strengthens (not weakens) the case that richness,
  not just corpus size, drives the effect. This observational improvement does not
  replace the still-outstanding matched-size control experiment (#10–#12).

## Still required

- Domain proximity paradox re-check: verify the ASDiv guide's own performance on the
  ASDiv test set specifically (63.7% guided here vs. the in-domain comparison in the
  paper's paradox argument) against the GSM8K-FT guide's ASDiv performance.
- Corpus-size-matched control (#10–#12) — not addressed by this experiment, still
  needed to fully isolate richness from training-set size.
- Table 16 and any narrative text citing the old Qwen+ASDiv-FT numbers need updating
  throughout the manuscript.
