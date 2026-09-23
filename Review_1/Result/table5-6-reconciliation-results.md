# Table 5/6 Reconciliation — Rerun Results (SVAMP, ASDiv, CommonsenseQA, PIQA)

Addresses Reviewer #1, Major Concerns #1 and #2 (McNemar B/C arithmetic inconsistency;
contradictory sample sizes across Tables 4/5/6).

## Results

| Dataset | N | Base | Guided | Δ (guided−base) | B | C | (B−C)/N | Self-consistent? |
|---|---|---|---|---|---|---|---|---|
| SVAMP | 300 | 38.7 | 59.0 | +20.3pp | 88 | 27 | +20.3pp | ✅ |
| ASDiv | 300 | 54.7 | 68.3 | +13.7pp | 73 | 32 | +13.7pp | ✅ |
| CommonsenseQA | 900 | 70.6 | 76.1 | +5.6pp | 133 | 83 | +5.6pp | ✅ |
| PIQA | 900 | 56.9 | 74.8 | +17.9pp | 312 | 151 | +17.9pp | ✅ |

All four rows now satisfy the paired-design identity (B−C)/N = Δ exactly, at the N
stated in the paper's Table 4 (SVAMP/ASDiv N=300, CommonsenseQA/PIQA N=900).

ARC-Challenge is not rerun here — `ARC_900_three_angle/results.jsonl` (existing repo
data) already reconciles exactly (N=900, B=140, C=65, base=71.7%), with a correction
needed only to Table 5's guided figure (77.0 → 80.0).

## Changes required to the manuscript

- **Table 4:** confirm N=300/300/900/900 for SVAMP/ASDiv/CommonsenseQA/PIQA (resolves
  the N=500-vs-900 PIQA footnote contradiction).
- **Table 5:** replace all four accuracy pairs with the values above. **PIQA changes
  most substantially** — guided accuracy drops from the originally reported 78.4% to
  74.8%, and Δ drops from +24.2pp to +17.9pp. This is the paper's headline result and
  the number itself moves, not just its stated N.
- **Table 6:** replace B, C for all four datasets with the values above; recompute OR,
  Cohen's g, and p from these B/C.
- **Downstream:** McNemar's test (#31), multiple-comparison correction (#5, once all
  final results are in), and any narrative referencing the old PIQA +24.2pp figure
  (abstract, Author Summary, cover letter, Finding 1) need updating to reflect +17.9pp.

## Reviewer concerns this closes

- **#1 (B/C arithmetic inconsistency):** resolved for these 4 datasets — identity now
  holds exactly.
- **#2 (contradictory N across tables):** resolved — real data now exists at the
  stated N for all four, no more mismatch between Table 4's footnote and Table 5.

## Still open

- ARC-Challenge Table 5 typo fix (77.0→80.0) — text-only, not covered by this rerun.
- #3 (multi-seed stability), #4 (RACE-High TOST), #5 (multiple-comparison correction,
  pending final numbers), #6 (richness-ordering re-check with corrected Table 16),
  #7/#8 (already addressed separately via SPGFT filter rerun + Qwen+ASDiv retrain).
