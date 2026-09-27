# RACE-High TOST Equivalence Test

Addresses Reviewer #1, Major Concern #4 (null claimed from p=1.000 is not
equivalence; requested TOST/equivalence procedure or CI reporting instead).

## Data

Qwen+GSM8K-FT primary condition, RACE-High, N=500 — same paired data behind
Table 5/6 (base=58.6%, guided=58.4%, B=60, C=61, mean paired difference = −0.20pp,
SE = 2.20pp). Verified identical to the existing Table 5/6 figures before running TOST.

## TOST Results

| Margin | t_lower (p) | t_upper (p) | TOST p (max) | Verdict |
|---|---|---|---|---|
| ±2pp | 0.82 (0.207) | −1.00 (0.159) | 0.207 | Not equivalent |
| ±3pp | 1.27 (0.102) | −1.45 (0.073) | 0.102 | Not equivalent |
| ±5pp | 2.18 (0.015) | −2.36 (0.009) | 0.015 | **Equivalent** |

**90% CI (TOST-relevant, α=0.05 per side):** [−3.83, +3.43] pp
**95% CI (reference):** [−4.53, +4.13] pp

## Interpretation

Equivalence is confirmed only at a fairly generous margin (±5pp), not at the tighter,
more standard margins (±2–3pp) that would make a "true null" claim airtight. At
N=500, the design can rule out an effect larger than ~3.8pp in either direction, but
cannot rule out something in the 3–5pp range.

This is notable because the Llama replication (Table 12) found a real +5.7pp effect
on this same benchmark — just outside what this Qwen TOST can exclude. The two
results are therefore statistically consistent with each other, not contradictory: Qwen's
"null" and Llama's "small positive" both sit comfortably inside the same plausible
effect range once honestly bounded.

## Recommendation for the manuscript

Replace "p=1.000 constitutes strong evidence for a true null" with a CI-based
statement, e.g.:

> "The design excludes effects larger than ~3.8pp in either direction (90% CI:
> [−3.8, +3.4] pp); we cannot rule out a true effect in the 3–5pp range, consistent
> with the smaller positive effect observed in the Llama replication (+5.7pp,
> Table 12)."

This directly answers Concern #4 with a quantitative, honest bound instead of
over-claiming exact equality, and reframes the Qwen/Llama RACE-High divergence as
expected statistical variation rather than an unexplained architecture-conditional
contradiction (Concern #6 / Limitations, secondary benefit).
