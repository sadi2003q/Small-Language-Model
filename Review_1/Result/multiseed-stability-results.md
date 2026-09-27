# Multi-Seed Stability — Actual Results (Concern #3)

Addresses Reviewer #1, Major Concern #3 (±1.5pp/SD<1.0pp claim contradicted by
Table 19's ±4pp note and Limitations' "3-6pp" Llama+ASDiv drift statement).

## Verified setup

Llama+ASDiv-FT and Llama+SVAMP-FT guides, evaluated on SVAMP, seeds {0, 1}, adapter
path confirmed correct at runtime (not a fallback/placeholder adapter).

## Results

| Condition | Seed | Base | Guided | Δ |
|---|---|---|---|---|
| Llama+ASDiv-FT | 0 | 34.7 | 50.3 | +15.7pp |
| Llama+ASDiv-FT | 1 | 37.0 | 45.0 | +8.0pp |
| Llama+ASDiv-FT | 42 (paper, Table 13) | 26.0 | 43.3 | +17.3pp |
| Llama+SVAMP-FT | 0 | 39.3 | 48.7 | +9.3pp |
| Llama+SVAMP-FT | 1 | 38.7 | 48.0 | +9.3pp |
| Llama+SVAMP-FT | 42 (paper, Table 14) | 24.7 | 42.0 | +17.3pp |

**Baseline spread across seeds {0, 1, 42}:**
- Llama+ASDiv-FT: 26.0 to 37.0 (**11.0pp range**)
- Llama+SVAMP-FT: 24.7 to 39.3 (**14.6pp range**)

This is a genuine result, not a data artifact — far exceeds the paper's stated
"±1.5pp, SD<1.0pp" bound for these two conditions.

## What this means

The ±1.5pp/SD<1.0pp claim **cannot be maintained as currently written** for
Llama+ASDiv-FT and Llama+SVAMP-FT on SVAMP. The guided accuracy is comparatively
more stable (Δ ranges 8.0–17.3pp) than the baseline, which drives most of the
swing — i.e., the *baseline* is what's seed-sensitive, not necessarily the guided
condition's relative benefit.

## Recommended LaTeX edits

1. **Multi-Seed Validation section:** replace the blanket claim
   > "Accuracy values remain within ±1.5 pp of the Seed 42 values in Table 5 for
   > all five confirmed datasets. Standard deviations are consistently below
   > 1.0 pp."

   with a scoped, honest version, e.g.:
   > "Accuracy was validated across seeds {0, 1, 42}. For the primary Qwen
   > configuration (Table 5), values remained within ±1.5pp with SD < 1.0pp.
   > For the Llama cross-architecture replication (Tables 13–14), baseline
   > accuracy showed larger seed-dependent variation — up to ~15pp on SVAMP for
   > the ASDiv-FT and SVAMP-FT conditions — while guided accuracy gains remained
   > directionally consistent (Δ = +8.0 to +17.3pp). Per-seed values are reported
   > in Table [X]."

2. **Add a new per-seed table** (use the Results table above) rather than
   asserting a single bound — this is what the reviewer explicitly requested
   ("tabulated rather than asserted").

3. **Limitations section:** the existing "3–6pp... reflecting seed-dependent
   question sampling" sentence is now *understated* — update to reflect the
   actual observed range (up to ~15pp) and cite the new per-seed table instead
   of a vague qualitative note.

4. **Table 19 caption:** the "±4pp seed variance" note can now point to the new
   per-seed table for a quantitative source instead of an unsupported aside.

## Still not covered

- Only SVAMP was checked for these two conditions. ASDiv (as a benchmark, not
  fine-tune source) and other benchmarks under Llama+ASDiv-FT/SVAMP-FT have not
  been multi-seed tested — the softened claim above should be scoped to SVAMP
  only unless further seeds are run on other benchmarks.
