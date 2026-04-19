from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


NOTEBOOK_MODEL_PATTERNS = {
    "guide_base": re.compile(r"[\"']guide_base[\"']\s*:\s*[\"']([^\"']+)[\"']"),
    "response_model": re.compile(r"[\"']response_model[\"']\s*:\s*[\"']([^\"']+)[\"']"),
    "solver_model": re.compile(r"[\"']solver_model[\"']\s*:\s*[\"']([^\"']+)[\"']"),
    "model_name": re.compile(r"[\"']model_name[\"']\s*:\s*[\"']([^\"']+)[\"']"),
}


def normalize_text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip().lower()


def normalize_answer(value: Any) -> str:
    text = str(value or "").strip().upper()
    text = text.replace("OPTION ", "")
    text = re.sub(r"[^A-Z0-9.\-]", "", text)
    return text


def to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    text = str(value or "").strip().lower()
    return text in {"1", "true", "yes", "y", "t"}


def to_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def count_steps(plan: str) -> int:
    if not plan:
        return 0
    return len(re.findall(r"\bstep\s*\d+\b", plan, flags=re.IGNORECASE))


def parse_notebook_models(root: Path) -> tuple[list[dict[str, str]], list[tuple[str, str]]]:
    rows: list[dict[str, str]] = []
    parse_errors: list[tuple[str, str]] = []

    for nb in sorted(root.glob("week*_Adnan/**/*.ipynb")):
        rel = str(nb.relative_to(root)).replace("\\", "/")
        try:
            data = json.loads(nb.read_text(encoding="utf-8", errors="ignore"))
        except Exception as exc:
            parse_errors.append((rel, str(exc)))
            continue

        cell_texts: list[str] = []
        for cell in data.get("cells", []):
            source = cell.get("source", "")
            if isinstance(source, list):
                source = "".join(source)
            if not isinstance(source, str):
                source = str(source)
            cell_texts.append(source)
        full = "\n".join(cell_texts)

        vals = {
            key: sorted(set(match.group(1).strip() for match in pattern.finditer(full)))
            for key, pattern in NOTEBOOK_MODEL_PATTERNS.items()
        }
        if not any(vals.values()):
            continue

        rows.append(
            {
                "notebook": rel,
                "guide_base": vals["guide_base"][0] if vals["guide_base"] else "",
                "response_model": vals["response_model"][0] if vals["response_model"] else "",
                "solver_model": vals["solver_model"][0] if vals["solver_model"] else "",
                "model_name": vals["model_name"][0] if vals["model_name"] else "",
            }
        )

    return rows, parse_errors


def infer_mode(record: dict[str, Any], file_path: Path) -> str:
    mode = str(record.get("mode", "")).strip().lower()
    strategy = str(record.get("strategy", "")).strip().lower()
    p = str(file_path).lower()

    if mode in {"guided", "baseline", "cot", "ceiling_3b"}:
        return mode

    if not mode:
        if "guided" in p and "baseline" not in p:
            return "guided"
        if "base_line" in p or "baseline" in p or "cot" in p:
            return "baseline"
        if "guided_line" in p:
            return "guided"
        if strategy == "coin_flip" and "base_line" in p:
            return "baseline"

    return mode or "unknown"


def infer_benchmark(file_path: Path) -> str:
    name = file_path.name.upper()
    match = re.search(r"RESULTS_([A-Z0-9_]+?)_(QWEN|LLAMA)", name)
    if match:
        return match.group(1)

    parts = [p.upper() for p in file_path.parts]
    for key in ["ARC", "ASDIV", "COMMONSENSE", "COMMONSENSEQA", "PIQA", "RACE", "SVAMP", "GSM8K"]:
        if any(key in part for part in parts):
            return key
    return "UNKNOWN"


def infer_combo(file_path: Path) -> str:
    name = file_path.name.upper()
    if "LLAMA3.2-1B" in name:
        return "meta-llama/Llama-3.2-3B-Instruct -> meta-llama/Llama-3.2-1B-Instruct"
    if "QWEN2.5-1.5B" in name:
        return "Qwen/Qwen2.5-3B-Instruct -> Qwen/Qwen2.5-1.5B-Instruct"
    if "QWEN2.5-3B" in name:
        return "Qwen/Qwen2.5-3B-Instruct (solo)"
    return "unknown"


def pair_key(record: dict[str, Any], benchmark: str) -> str:
    if record.get("idx") is not None:
        return f"{benchmark}|idx:{record.get('idx')}|gt:{normalize_answer(record.get('gt_answer', ''))}"
    q = normalize_text(record.get("question", ""))
    gt = normalize_answer(record.get("gt_answer", ""))
    return f"{benchmark}|q:{q}|gt:{gt}"


def classify_guided_regression(case: dict[str, Any]) -> str:
    if case["refiner_used"] and not case["refiner_correct"]:
        return "aggregation_or_refiner_bottleneck"
    if case["correct_vote_present"] and not case["guided_correct"]:
        return "aggregation_or_refiner_bottleneck"
    if case["plan_present"] and case["step_count"] < 2:
        return "step_quality_issue"
    if case["plan_present"] and case["guided_confidence"] >= 0.6 and case["vote_consistency"] >= 0.6:
        return "guide_plan_bias"
    if case["guided_confidence"] < 0.4 or case["vote_consistency"] < 0.4:
        return "solver_instability_or_sampling"
    return "mixed_uncertain"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        import csv

        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def collect_eval_jsonl_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(root.glob("week*_Adnan/**/*.jsonl")):
        lower_name = path.name.lower()
        if "sg_raw" in lower_name or "sg_valid" in lower_name:
            continue
        if "_dup" in lower_name:
            continue
        files.append(path)
    return files


def analyze(root: Path, out_dir: Path) -> None:
    notebook_rows, notebook_parse_errors = parse_notebook_models(root)

    guide_solver_pairs = Counter()
    single_model_configs = Counter()
    for row in notebook_rows:
        guide = row["guide_base"]
        solver = row["response_model"] or row["solver_model"]
        if guide and solver:
            guide_solver_pairs[(guide, solver)] += 1
        elif row["model_name"]:
            single_model_configs[row["model_name"]] += 1

    eval_files = collect_eval_jsonl_files(root)

    file_mode_rows: list[dict[str, Any]] = []
    paired_case_rows: list[dict[str, Any]] = []
    guided_regression_rows: list[dict[str, Any]] = []
    parse_error_rows: list[dict[str, Any]] = []

    for path in eval_files:
        rel = str(path.relative_to(root)).replace("\\", "/")
        benchmark = infer_benchmark(path)
        combo = infer_combo(path)

        per_mode: dict[str, list[dict[str, Any]]] = defaultdict(list)
        total_records = 0
        bad_lines = 0

        with path.open("r", encoding="utf-8", errors="ignore") as handle:
            for line_no, line in enumerate(handle, 1):
                raw = line.strip()
                if not raw:
                    continue
                try:
                    record = json.loads(raw)
                except Exception as exc:
                    bad_lines += 1
                    parse_error_rows.append(
                        {
                            "file": rel,
                            "line": line_no,
                            "error": str(exc),
                        }
                    )
                    continue

                total_records += 1
                mode = infer_mode(record, path)
                per_mode[mode].append(record)

        mode_counts = {mode: len(rows) for mode, rows in sorted(per_mode.items())}
        file_mode_rows.append(
            {
                "file": rel,
                "combo": combo,
                "benchmark": benchmark,
                "total_records": total_records,
                "bad_lines": bad_lines,
                "guided_records": mode_counts.get("guided", 0),
                "baseline_records": mode_counts.get("baseline", 0),
                "cot_records": mode_counts.get("cot", 0),
                "ceiling_records": mode_counts.get("ceiling_3b", 0),
                "unknown_records": mode_counts.get("unknown", 0),
            }
        )

        guided_rows = per_mode.get("guided", [])
        baseline_rows = per_mode.get("baseline", [])
        if not guided_rows or not baseline_rows:
            continue

        guided_map: dict[str, list[dict[str, Any]]] = defaultdict(list)
        baseline_map: dict[str, list[dict[str, Any]]] = defaultdict(list)

        for record in guided_rows:
            guided_map[pair_key(record, benchmark)].append(record)
        for record in baseline_rows:
            baseline_map[pair_key(record, benchmark)].append(record)

        shared_keys = sorted(set(guided_map).intersection(baseline_map))

        for key in shared_keys:
            g_list = guided_map[key]
            b_list = baseline_map[key]
            for idx in range(min(len(g_list), len(b_list))):
                guided = g_list[idx]
                baseline = b_list[idx]

                guided_correct = to_bool(guided.get("correct"))
                baseline_correct = to_bool(baseline.get("correct"))

                if guided_correct and baseline_correct:
                    outcome = "both_correct"
                elif (not guided_correct) and baseline_correct:
                    outcome = "guided_only_wrong"
                elif guided_correct and (not baseline_correct):
                    outcome = "baseline_only_wrong"
                else:
                    outcome = "both_wrong"

                plan = str(guided.get("plan", "") or "")
                plan_present = bool(plan.strip())
                step_count = count_steps(plan)

                vote_counts = guided.get("vote_counts", {})
                if not isinstance(vote_counts, dict):
                    vote_counts = {}

                gt_answer = normalize_answer(guided.get("gt_answer", ""))
                normalized_vote_counts = {
                    normalize_answer(answer): to_float(count)
                    for answer, count in vote_counts.items()
                }
                correct_vote_present = normalized_vote_counts.get(gt_answer, 0.0) > 0.0

                row = {
                    "file": rel,
                    "combo": combo,
                    "benchmark": benchmark,
                    "pair_key": key,
                    "idx": guided.get("idx", ""),
                    "outcome": outcome,
                    "question": str(guided.get("question", "")),
                    "question_preview": str(guided.get("question", ""))[:220].replace("\n", " "),
                    "gt_answer": guided.get("gt_answer", ""),
                    "guided_final_answer": guided.get("final_answer", ""),
                    "baseline_final_answer": baseline.get("final_answer", ""),
                    "guided_correct": guided_correct,
                    "baseline_correct": baseline_correct,
                    "guided_confidence": to_float(guided.get("confidence", 0.0)),
                    "baseline_confidence": to_float(baseline.get("confidence", 0.0)),
                    "vote_consistency": to_float(guided.get("vote_consistency", 0.0)),
                    "wasted_votes": to_float(guided.get("wasted_votes", 0.0)),
                    "refiner_used": to_bool(guided.get("refiner_used")),
                    "refiner_correct": to_bool(guided.get("refiner_correct")),
                    "plan_present": plan_present,
                    "step_count": step_count,
                    "correct_vote_present": correct_vote_present,
                    "guided_strategy": guided.get("strategy", ""),
                    "baseline_strategy": baseline.get("strategy", ""),
                    "guided_vote_counts": json.dumps(vote_counts, ensure_ascii=False),
                    "baseline_vote_counts": json.dumps(baseline.get("vote_counts", {}), ensure_ascii=False),
                    "guided_plan": plan,
                }
                paired_case_rows.append(row)

                if outcome == "guided_only_wrong":
                    cause = classify_guided_regression(row)
                    reg_row = dict(row)
                    reg_row["root_cause"] = cause
                    guided_regression_rows.append(reg_row)

    paired_outcome_summary = []
    outcome_counter = Counter((row["combo"], row["benchmark"], row["outcome"]) for row in paired_case_rows)
    for (combo, benchmark, outcome), count in sorted(outcome_counter.items()):
        paired_outcome_summary.append(
            {
                "combo": combo,
                "benchmark": benchmark,
                "outcome": outcome,
                "count": count,
            }
        )

    cause_distribution = []
    cause_counter = Counter((row["combo"], row["benchmark"], row["root_cause"]) for row in guided_regression_rows)
    for (combo, benchmark, cause), count in sorted(cause_counter.items()):
        cause_distribution.append(
            {
                "combo": combo,
                "benchmark": benchmark,
                "root_cause": cause,
                "count": count,
            }
        )

    guided_regression_rows.sort(
        key=lambda row: (
            -row["guided_confidence"],
            -row["vote_consistency"],
            -row["baseline_confidence"],
        )
    )

    model_inventory_rows = []
    for row in notebook_rows:
        model_inventory_rows.append(
            {
                "type": "notebook_config",
                "item": row["notebook"],
                "guide_base": row["guide_base"],
                "response_model": row["response_model"],
                "solver_model": row["solver_model"],
                "model_name": row["model_name"],
                "count": 1,
            }
        )
    for (guide, solver), count in sorted(guide_solver_pairs.items(), key=lambda item: (-item[1], item[0])):
        model_inventory_rows.append(
            {
                "type": "guide_solver_pair",
                "item": f"{guide} -> {solver}",
                "guide_base": guide,
                "response_model": solver,
                "solver_model": "",
                "model_name": "",
                "count": count,
            }
        )
    for model_name, count in sorted(single_model_configs.items(), key=lambda item: (-item[1], item[0])):
        model_inventory_rows.append(
            {
                "type": "single_model_config",
                "item": model_name,
                "guide_base": "",
                "response_model": "",
                "solver_model": "",
                "model_name": model_name,
                "count": count,
            }
        )

    write_csv(
        out_dir / "model_combo_inventory.csv",
        model_inventory_rows,
        ["type", "item", "guide_base", "response_model", "solver_model", "model_name", "count"],
    )
    write_csv(
        out_dir / "jsonl_mode_summary.csv",
        file_mode_rows,
        [
            "file",
            "combo",
            "benchmark",
            "total_records",
            "bad_lines",
            "guided_records",
            "baseline_records",
            "cot_records",
            "ceiling_records",
            "unknown_records",
        ],
    )
    write_csv(
        out_dir / "paired_outcomes.csv",
        paired_case_rows,
        [
            "file",
            "combo",
            "benchmark",
            "pair_key",
            "idx",
            "outcome",
            "question_preview",
            "gt_answer",
            "guided_final_answer",
            "baseline_final_answer",
            "guided_correct",
            "baseline_correct",
            "guided_confidence",
            "baseline_confidence",
            "vote_consistency",
            "wasted_votes",
            "refiner_used",
            "refiner_correct",
            "plan_present",
            "step_count",
            "correct_vote_present",
            "guided_strategy",
            "baseline_strategy",
        ],
    )
    write_csv(
        out_dir / "paired_outcome_summary.csv",
        paired_outcome_summary,
        ["combo", "benchmark", "outcome", "count"],
    )
    write_csv(
        out_dir / "guided_regression_cases.csv",
        guided_regression_rows,
        [
            "file",
            "combo",
            "benchmark",
            "idx",
            "question_preview",
            "gt_answer",
            "guided_final_answer",
            "baseline_final_answer",
            "guided_confidence",
            "baseline_confidence",
            "vote_consistency",
            "refiner_used",
            "refiner_correct",
            "plan_present",
            "step_count",
            "correct_vote_present",
            "root_cause",
            "guided_vote_counts",
            "baseline_vote_counts",
        ],
    )
    write_csv(
        out_dir / "cause_distribution.csv",
        cause_distribution,
        ["combo", "benchmark", "root_cause", "count"],
    )
    write_csv(
        out_dir / "json_parse_errors.csv",
        parse_error_rows,
        ["file", "line", "error"],
    )

    total_pairs = len(paired_case_rows)
    guided_correct_total = sum(1 for row in paired_case_rows if row["guided_correct"])
    baseline_correct_total = sum(1 for row in paired_case_rows if row["baseline_correct"])

    guided_acc = (guided_correct_total / total_pairs) if total_pairs else 0.0
    baseline_acc = (baseline_correct_total / total_pairs) if total_pairs else 0.0

    root_cause_counter = Counter(row["root_cause"] for row in guided_regression_rows)
    top_regressions = guided_regression_rows[:25]

    lines = [
        "# Deep Causality Audit",
        "",
        "## Scope",
        "- Source notebooks: week*_Adnan/**/*.ipynb",
        "- Source eval records: week*_Adnan/**/*.jsonl (excluding sg_raw/sg_valid and *_dup* files)",
        "",
        "## Model Combo Inventory",
        f"- Notebook files with parseable model signals: {len(notebook_rows)}",
        f"- Notebook parse errors: {len(notebook_parse_errors)}",
        f"- Unique guide-solver pairs: {len(guide_solver_pairs)}",
    ]

    for (guide, solver), count in sorted(guide_solver_pairs.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"  - {guide} -> {solver} (seen in {count} notebook configs)")

    lines.append(f"- Unique single-model configs: {len(single_model_configs)}")
    for model_name, count in sorted(single_model_configs.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"  - {model_name} (seen in {count} notebook configs)")

    lines.extend(
        [
            "",
            "## Paired Guided vs Baseline Outcomes",
            f"- Paired question count: {total_pairs}",
            f"- Guided accuracy on paired set: {guided_acc:.4f}",
            f"- Baseline accuracy on paired set: {baseline_acc:.4f}",
            f"- Guided-only-wrong cases: {sum(1 for row in paired_case_rows if row['outcome'] == 'guided_only_wrong')}",
            f"- Baseline-only-wrong cases: {sum(1 for row in paired_case_rows if row['outcome'] == 'baseline_only_wrong')}",
            f"- Both-wrong cases: {sum(1 for row in paired_case_rows if row['outcome'] == 'both_wrong')}",
            "",
            "## Guided Regression Root Causes",
        ]
    )

    for cause, count in root_cause_counter.most_common():
        lines.append(f"- {cause}: {count}")

    lines.extend(
        [
            "",
            "## Top Guided Regression Exemplars",
            "(sorted by guided confidence and vote consistency)",
        ]
    )

    for row in top_regressions:
        lines.append(
            "- "
            f"[{row['combo']} | {row['benchmark']} | idx={row.get('idx', '')}] "
            f"gt={row['gt_answer']} guided={row['guided_final_answer']} baseline={row['baseline_final_answer']} "
            f"conf_g={row['guided_confidence']:.2f} cons={row['vote_consistency']:.2f} cause={row['root_cause']} "
            f"question={row['question_preview']}"
        )

    lines.extend(
        [
            "",
            "## Output Files",
            "- model_combo_inventory.csv",
            "- jsonl_mode_summary.csv",
            "- paired_outcomes.csv",
            "- paired_outcome_summary.csv",
            "- guided_regression_cases.csv",
            "- cause_distribution.csv",
            "- json_parse_errors.csv",
        ]
    )

    report_path = out_dir / "deep_causality_report.md"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote audit outputs to: {out_dir}")
    print(f"Paired questions: {total_pairs}")
    print(f"Guided accuracy: {guided_acc:.4f}")
    print(f"Baseline accuracy: {baseline_acc:.4f}")
    print("Root causes:")
    for cause, count in root_cause_counter.most_common():
        print(f"  {cause}: {count}")


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[1]
    output_dir = repo_root / "FT_result" / "causality_audit"
    analyze(repo_root, output_dir)
