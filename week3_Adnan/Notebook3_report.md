# SCORE Data Generation Report

## Overview
This report summarizes the results of the SCORE data generation process.  
The objective of this evaluation was to identify valid *(wrong solution → correct solution)* pairs while filtering out already-correct answers and invalid generations.

---

## Dataset Processing Summary

| Metric | Value |
|------|------:|
| **Total questions processed** | 200 |
| **All-correct (skipped)** | 160 |
| **Questions with wrong solutions** | 40 |
| **Total wrong solutions generated** | 74 |
| **Valid pairs saved** | 24 |
| **Survival rate** | **32.4%** |
| **Paper baseline survival rate** | ~25% |

**Observation:**  
The achieved survival rate of **32.4%** exceeds the reported paper baseline, indicating improved filtering or generation quality.

---

## Failure Analysis

The following table shows a breakdown of failure causes encountered during validation:

| Failure Type | Count |
|-------------|------:|
| `wrong_ans_6` | 4 |
| `no_answer` | 3 |
| `wrong_ans_400` | 2 |
| `wrong_ans_650` | 2 |
| `wrong_ans_200` | 2 |
| `wrong_ans_252` | 2 |
| `wrong_ans_0` | 2 |
| `wrong_ans_31` | 1 |
| `wrong_ans_57` | 1 |
| `wrong_ans_60` | 1 |
| `wrong_ans_54` | 1 |
| `crit_missing_correction` | 1 |
| `wrong_ans_62` | 1 |
| `wrong_ans_83` | 1 |
| `wrong_ans_3` | 1 |
| `wrong_ans_250` | 1 |
| `wrong_ans_22` | 1 |
| `wrong_ans_17` | 1 |
| `wrong_ans_12` | 1 |
| `wrong_ans_14` | 1 |
| `wrong_ans_1` | 1 |
| `wrong_ans_8060` | 1 |
| `wrong_ans_450` | 1 |
| `wrong_ans_55` | 1 |
| `wrong_ans_2046` | 1 |
| `wrong_ans_360000` | 1 |
| `wrong_ans_112` | 1 |
| `wrong_ans_531000` | 1 |

**Key Insights:**
- Most failures are due to **incorrect numeric answers**, often with large or outlier values.
- A small number of cases failed due to **missing answers** or **missing correction steps**, indicating potential generation or parsing issues.

---

## Final Verdict
- Gemma 3 Model is too Good For GSM8k Dataset


### Suggestion:
- Skip Step 3 and 4 and Directly move to step 5