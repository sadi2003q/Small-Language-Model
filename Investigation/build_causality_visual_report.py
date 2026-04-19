from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def load_csvs(audit_dir: Path) -> dict[str, pd.DataFrame]:
    files = {
        "model_combo_inventory": "model_combo_inventory.csv",
        "jsonl_mode_summary": "jsonl_mode_summary.csv",
        "paired_outcomes": "paired_outcomes.csv",
        "paired_outcome_summary": "paired_outcome_summary.csv",
        "guided_regression_cases": "guided_regression_cases.csv",
        "cause_distribution": "cause_distribution.csv",
        "json_parse_errors": "json_parse_errors.csv",
    }
    data = {}
    for key, filename in files.items():
        data[key] = pd.read_csv(audit_dir / filename)
    return data


def cast_columns(data: dict[str, pd.DataFrame]) -> None:
    paired = data["paired_outcomes"]
    reg = data["guided_regression_cases"]

    bool_cols_paired = [
        "guided_correct",
        "baseline_correct",
        "refiner_used",
        "refiner_correct",
        "plan_present",
        "correct_vote_present",
    ]
    for col in bool_cols_paired:
        if col in paired.columns:
            paired[col] = paired[col].astype(str).str.lower().isin(["true", "1", "yes", "y", "t"])

    bool_cols_reg = [
        "refiner_used",
        "refiner_correct",
        "plan_present",
        "correct_vote_present",
    ]
    for col in bool_cols_reg:
        if col in reg.columns:
            reg[col] = reg[col].astype(str).str.lower().isin(["true", "1", "yes", "y", "t"])

    numeric_cols_paired = [
        "guided_confidence",
        "baseline_confidence",
        "vote_consistency",
        "wasted_votes",
        "step_count",
    ]
    for col in numeric_cols_paired:
        if col in paired.columns:
            paired[col] = pd.to_numeric(paired[col], errors="coerce")

    numeric_cols_reg = [
        "guided_confidence",
        "baseline_confidence",
        "vote_consistency",
        "step_count",
    ]
    for col in numeric_cols_reg:
        if col in reg.columns:
            reg[col] = pd.to_numeric(reg[col], errors="coerce")

    mode_summary = data["jsonl_mode_summary"]
    numeric_mode_cols = [
        "total_records",
        "bad_lines",
        "guided_records",
        "baseline_records",
        "cot_records",
        "ceiling_records",
        "unknown_records",
    ]
    for col in numeric_mode_cols:
        if col in mode_summary.columns:
            mode_summary[col] = pd.to_numeric(mode_summary[col], errors="coerce")

    outcome_summary = data["paired_outcome_summary"]
    if "count" in outcome_summary.columns:
        outcome_summary["count"] = pd.to_numeric(outcome_summary["count"], errors="coerce")

    cause = data["cause_distribution"]
    if "count" in cause.columns:
        cause["count"] = pd.to_numeric(cause["count"], errors="coerce")


def kpi_metrics(data: dict[str, pd.DataFrame]) -> dict[str, float | int]:
    paired = data["paired_outcomes"]
    reg = data["guided_regression_cases"]

    total_pairs = len(paired)
    guided_acc = float(paired["guided_correct"].mean()) if total_pairs else 0.0
    baseline_acc = float(paired["baseline_correct"].mean()) if total_pairs else 0.0
    accuracy_delta = guided_acc - baseline_acc

    outcomes = paired["outcome"].value_counts(dropna=False)
    guided_only_wrong = int(outcomes.get("guided_only_wrong", 0))
    baseline_only_wrong = int(outcomes.get("baseline_only_wrong", 0))
    both_wrong = int(outcomes.get("both_wrong", 0))
    both_correct = int(outcomes.get("both_correct", 0))

    cause_counts = reg["root_cause"].value_counts(dropna=False)
    top_cause = str(cause_counts.index[0]) if len(cause_counts) else "n/a"
    top_cause_count = int(cause_counts.iloc[0]) if len(cause_counts) else 0

    return {
        "total_pairs": total_pairs,
        "guided_acc": guided_acc,
        "baseline_acc": baseline_acc,
        "accuracy_delta": accuracy_delta,
        "guided_only_wrong": guided_only_wrong,
        "baseline_only_wrong": baseline_only_wrong,
        "both_wrong": both_wrong,
        "both_correct": both_correct,
        "top_cause": top_cause,
        "top_cause_count": top_cause_count,
    }


def style_plotly(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.92)",
        font=dict(family="'IBM Plex Sans', 'Segoe UI', sans-serif", color="#123"),
        margin=dict(l=40, r=20, t=46, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    return fig


def build_figures(data: dict[str, pd.DataFrame]) -> list[tuple[str, str, go.Figure, str]]:
    paired = data["paired_outcomes"].copy()
    outcome_summary = data["paired_outcome_summary"].copy()
    cause = data["cause_distribution"].copy()
    reg = data["guided_regression_cases"].copy()

    outcome_order = ["both_correct", "baseline_only_wrong", "guided_only_wrong", "both_wrong"]
    outcome_colors = {
        "both_correct": "#1d4ed8",
        "baseline_only_wrong": "#2563eb",
        "guided_only_wrong": "#dc2626",
        "both_wrong": "#475569",
    }

    outcome_summary["outcome"] = pd.Categorical(outcome_summary["outcome"], categories=outcome_order, ordered=True)
    outcome_summary = outcome_summary.sort_values(["combo", "outcome"])

    fig1 = px.bar(
        outcome_summary,
        x="count",
        y="combo",
        color="outcome",
        orientation="h",
        barmode="stack",
        color_discrete_map=outcome_colors,
        title="Paired Outcomes by Model Combo",
    )
    fig1.update_layout(xaxis_title="Question Count", yaxis_title="Model Combo")
    fig1 = style_plotly(fig1)

    acc = paired.groupby("combo", as_index=False).agg(
        guided_accuracy=("guided_correct", "mean"),
        baseline_accuracy=("baseline_correct", "mean"),
    )
    acc_long = acc.melt(
        id_vars=["combo"],
        value_vars=["guided_accuracy", "baseline_accuracy"],
        var_name="system",
        value_name="accuracy",
    )
    acc_long["system"] = acc_long["system"].map(
        {"guided_accuracy": "Guided", "baseline_accuracy": "Baseline"}
    )
    fig2 = px.bar(
        acc_long,
        x="combo",
        y="accuracy",
        color="system",
        barmode="group",
        color_discrete_map={"Guided": "#2563eb", "Baseline": "#dc2626"},
        text=acc_long["accuracy"].map(lambda v: f"{v:.3f}"),
        title="Accuracy Comparison by Combo",
    )
    fig2.update_layout(yaxis_title="Accuracy", xaxis_title="Model Combo")
    fig2.update_traces(textposition="outside")
    fig2 = style_plotly(fig2)

    fig3 = px.bar(
        cause,
        x="benchmark",
        y="count",
        color="root_cause",
        facet_col="combo",
        barmode="stack",
        color_discrete_map={
            "solver_instability_or_sampling": "#f97316",
            "aggregation_or_refiner_bottleneck": "#7c3aed",
            "step_quality_issue": "#e11d48",
            "mixed_uncertain": "#334155",
            "guide_plan_bias": "#0ea5e9",
        },
        title="Guided Regression Root Causes by Benchmark and Combo",
    )
    fig3.update_layout(yaxis_title="Case Count", xaxis_title="Benchmark")
    fig3 = style_plotly(fig3)

    hotspot = reg.groupby(["benchmark", "combo"], as_index=False).size().rename(columns={"size": "count"})
    heat = hotspot.pivot(index="benchmark", columns="combo", values="count").fillna(0)
    fig4 = go.Figure(
        data=go.Heatmap(
            z=heat.values,
            x=list(heat.columns),
            y=list(heat.index),
            colorscale=[
                [0.0, "#e2e8f0"],
                [0.2, "#bfdbfe"],
                [0.5, "#60a5fa"],
                [0.8, "#fca5a5"],
                [1.0, "#dc2626"],
            ],
            colorbar=dict(title="Guided-only-wrong"),
            hovertemplate="Combo=%{x}<br>Benchmark=%{y}<br>Cases=%{z}<extra></extra>",
        )
    )
    fig4.update_layout(title="Hotspot Heatmap: Guided-only-wrong Cases")
    fig4 = style_plotly(fig4)

    sankey_df = reg.groupby(["combo", "root_cause"], as_index=False).size().rename(columns={"size": "count"})
    combos = sankey_df["combo"].drop_duplicates().tolist()
    causes = sankey_df["root_cause"].drop_duplicates().tolist()
    labels = combos + causes
    node_index = {label: idx for idx, label in enumerate(labels)}

    sources = [node_index[c] for c in sankey_df["combo"]]
    targets = [node_index[c] for c in sankey_df["root_cause"]]
    values = sankey_df["count"].tolist()

    fig5 = go.Figure(
        data=[
            go.Sankey(
                arrangement="snap",
                node=dict(
                    pad=18,
                    thickness=20,
                    line=dict(color="#cbd5e1", width=1),
                    label=labels,
                    color=["#2563eb" for _ in combos] + ["#dc2626", "#f97316", "#7c3aed", "#0ea5e9", "#334155"][
                        : len(causes)
                    ],
                ),
                link=dict(source=sources, target=targets, value=values, color="rgba(59,130,246,0.35)"),
            )
        ]
    )
    fig5.update_layout(title="Flow Diagram: Combo -> Root Cause")
    fig5 = style_plotly(fig5)

    scatter_df = reg.dropna(subset=["guided_confidence", "vote_consistency"]).copy()
    if len(scatter_df) > 2500:
        scatter_df = scatter_df.sample(2500, random_state=42)
    fig6 = px.scatter(
        scatter_df,
        x="guided_confidence",
        y="vote_consistency",
        color="root_cause",
        symbol="combo",
        hover_data=["benchmark", "idx", "gt_answer", "guided_final_answer", "baseline_final_answer"],
        title="Confidence vs Vote Consistency in Guided Regression Cases",
        color_discrete_map={
            "solver_instability_or_sampling": "#f97316",
            "aggregation_or_refiner_bottleneck": "#7c3aed",
            "step_quality_issue": "#e11d48",
            "mixed_uncertain": "#334155",
            "guide_plan_bias": "#0ea5e9",
        },
    )
    fig6.update_layout(xaxis_title="Guided Confidence", yaxis_title="Vote Consistency")
    fig6 = style_plotly(fig6)

    return [
        (
            "chart-outcomes",
            "Outcome Distribution",
            fig1,
            "Stacked view of both-correct, guided-only-wrong, baseline-only-wrong, and both-wrong outcomes.",
        ),
        (
            "chart-accuracy",
            "Guided vs Baseline Accuracy",
            fig2,
            "Direct accuracy comparison per model combo.",
        ),
        (
            "chart-root-causes",
            "Root Cause by Benchmark",
            fig3,
            "How failure causes distribute across benchmarks and model families.",
        ),
        (
            "chart-heatmap",
            "Guided Regression Hotspots",
            fig4,
            "Heatmap highlighting where guided pipeline most often underperformed baseline.",
        ),
        (
            "chart-sankey",
            "Causality Flow Diagram",
            fig5,
            "Diagram connecting model combos to root-cause categories.",
        ),
        (
            "chart-scatter",
            "Failure Behavior Scatter",
            fig6,
            "Confidence-consistency patterns in guided-only-wrong cases.",
        ),
    ]


def table_html(df: pd.DataFrame, table_id: str) -> str:
    return df.to_html(index=False, table_id=table_id, classes=["data-table"], border=0, escape=True)


def card_for_csv(title: str, filename: str, df: pd.DataFrame, note: str, table_id: str) -> str:
    rows = len(df)
    cols = len(df.columns)
    return f"""
    <section class=\"table-card\">
      <div class=\"table-head\">
        <div>
          <h3>{title}</h3>
          <p class=\"muted\">{note}</p>
          <p class=\"meta\">Rows: {rows:,} | Columns: {cols}</p>
        </div>
        <div class=\"table-actions\">
          <a class=\"btn\" href=\"{filename}\" download>Download CSV</a>
        </div>
      </div>
      <div class=\"table-tools\">
        <input type=\"text\" placeholder=\"Search this table...\" oninput=\"filterTable('{table_id}', this.value)\" />
      </div>
      <div class=\"table-wrap\">{table_html(df, table_id)}</div>
    </section>
    """


def build_html(audit_dir: Path, data: dict[str, pd.DataFrame]) -> str:
    kpis = kpi_metrics(data)
    figs = build_figures(data)

    chart_blocks = []
    for idx, (chart_id, title, fig, note) in enumerate(figs):
        include_js = "inline" if idx == 0 else False
        chart_html = fig.to_html(full_html=False, include_plotlyjs=include_js, config={"displaylogo": False})
        chart_blocks.append(
            f"""
            <article id=\"{chart_id}\" class=\"viz-card\">
              <h3>{title}</h3>
              <p class=\"muted\">{note}</p>
              <div class=\"viz\">{chart_html}</div>
            </article>
            """
        )

    csv_cards = []
    csv_cards.append(
        card_for_csv(
            "Model Combo Inventory",
            "model_combo_inventory.csv",
            data["model_combo_inventory"],
            "Model families and combo configuration inventory extracted from notebooks.",
            "table-model-inventory",
        )
    )
    csv_cards.append(
        card_for_csv(
            "Paired Outcome Summary",
            "paired_outcome_summary.csv",
            data["paired_outcome_summary"],
            "Aggregated outcome buckets per combo and benchmark.",
            "table-outcome-summary",
        )
    )
    csv_cards.append(
        card_for_csv(
            "Cause Distribution",
            "cause_distribution.csv",
            data["cause_distribution"],
            "Guided-only-wrong root-cause frequencies by combo and benchmark.",
            "table-cause-distribution",
        )
    )
    csv_cards.append(
        card_for_csv(
            "Guided Regression Cases",
            "guided_regression_cases.csv",
            data["guided_regression_cases"],
            "Case-level forensic rows for guided-only-wrong samples.",
            "table-guided-regressions",
        )
    )
    csv_cards.append(
        card_for_csv(
            "Paired Outcomes (All Questions)",
            "paired_outcomes.csv",
            data["paired_outcomes"],
            "Full paired guided-vs-baseline dataset used for all aggregate metrics.",
            "table-paired-outcomes",
        )
    )
    csv_cards.append(
        card_for_csv(
            "JSONL Mode Summary",
            "jsonl_mode_summary.csv",
            data["jsonl_mode_summary"],
            "Input data health summary per source result file.",
            "table-mode-summary",
        )
    )
    csv_cards.append(
        card_for_csv(
            "JSON Parse Errors",
            "json_parse_errors.csv",
            data["json_parse_errors"],
            "Malformed lines detected during audit ingestion.",
            "table-parse-errors",
        )
    )

    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    return f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>Causality Audit | Research Dashboard</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

    :root {{
      --bg: #f5f9ff;
      --ink: #0f172a;
      --muted: #425466;
      --card: rgba(255,255,255,0.88);
      --line: #d9e2ef;
      --blue: #2563eb;
      --red: #dc2626;
      --teal: #0ea5a5;
      --violet: #7c3aed;
      --amber: #f59e0b;
      --shadow: 0 14px 40px rgba(15, 23, 42, 0.12);
    }}

    * {{ box-sizing: border-box; }}

    body {{
      margin: 0;
      font-family: 'IBM Plex Sans', 'Segoe UI', sans-serif;
      color: var(--ink);
      background:
        radial-gradient(1200px 600px at -10% -10%, rgba(37,99,235,0.22), transparent 60%),
        radial-gradient(1000px 560px at 110% 10%, rgba(220,38,38,0.14), transparent 65%),
        linear-gradient(180deg, #f8fbff 0%, #eef5ff 46%, #f7f9ff 100%);
      min-height: 100vh;
    }}

    .page {{
      max-width: 1640px;
      margin: 0 auto;
      padding: 28px 24px 56px;
    }}

    .hero {{
      border: 1px solid rgba(37,99,235,0.22);
      background: linear-gradient(135deg, rgba(255,255,255,0.88), rgba(232,242,255,0.92));
      border-radius: 24px;
      padding: 28px;
      box-shadow: var(--shadow);
      backdrop-filter: blur(6px);
      position: relative;
      overflow: hidden;
    }}

    .hero::after {{
      content: '';
      position: absolute;
      right: -120px;
      top: -120px;
      width: 320px;
      height: 320px;
      background: radial-gradient(circle, rgba(220,38,38,0.18), rgba(220,38,38,0));
      pointer-events: none;
    }}

    .eyebrow {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: #1d4ed8;
      font-weight: 700;
      padding: 8px 12px;
      border-radius: 999px;
      border: 1px solid rgba(37,99,235,0.25);
      background: rgba(37,99,235,0.08);
      margin-bottom: 14px;
    }}

    h1, h2, h3 {{
      font-family: 'Space Grotesk', 'Segoe UI', sans-serif;
      margin: 0;
      line-height: 1.18;
    }}

    .hero h1 {{
      font-size: clamp(1.8rem, 2.4vw, 3.05rem);
      margin-bottom: 10px;
      max-width: 980px;
    }}

    .subtitle {{
      font-size: 1rem;
      color: var(--muted);
      max-width: 980px;
      margin-bottom: 18px;
    }}

    .hero-meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      font-size: 0.92rem;
      color: #1f3b64;
    }}

    .pill {{
      padding: 8px 12px;
      border-radius: 999px;
      border: 1px solid rgba(30,64,175,0.2);
      background: rgba(37,99,235,0.08);
      font-weight: 600;
    }}

    .kpi-grid {{
      margin-top: 20px;
      display: grid;
      grid-template-columns: repeat(5, minmax(150px, 1fr));
      gap: 12px;
    }}

    .kpi {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 16px;
      padding: 14px;
      box-shadow: 0 6px 22px rgba(15,23,42,0.08);
    }}

    .kpi .label {{
      font-size: 0.78rem;
      color: #4a5d7a;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      margin-bottom: 8px;
    }}

    .kpi .value {{
      font-size: 1.4rem;
      font-family: 'Space Grotesk', sans-serif;
      font-weight: 700;
      color: #0b1f45;
    }}

    .kpi .sub {{
      margin-top: 6px;
      font-size: 0.82rem;
      color: #5e728f;
    }}

    .kpi.blue {{ border-top: 4px solid var(--blue); }}
    .kpi.red {{ border-top: 4px solid var(--red); }}
    .kpi.violet {{ border-top: 4px solid var(--violet); }}
    .kpi.teal {{ border-top: 4px solid var(--teal); }}
    .kpi.amber {{ border-top: 4px solid var(--amber); }}

    .section {{
      margin-top: 28px;
      border: 1px solid var(--line);
      border-radius: 20px;
      background: var(--card);
      box-shadow: 0 10px 28px rgba(15,23,42,0.08);
      padding: 20px;
    }}

    .section h2 {{
      font-size: 1.45rem;
      margin-bottom: 6px;
    }}

    .muted {{
      color: var(--muted);
      margin: 0;
      font-size: 0.95rem;
    }}

    .process {{
      display: grid;
      grid-template-columns: repeat(6, minmax(120px, 1fr));
      gap: 12px;
      margin-top: 16px;
    }}

    .step {{
      position: relative;
      background: linear-gradient(165deg, #f8fbff, #e6efff);
      border: 1px solid #cddaf0;
      border-radius: 14px;
      padding: 12px;
      min-height: 120px;
    }}

    .step b {{
      display: block;
      font-family: 'Space Grotesk', sans-serif;
      margin-bottom: 6px;
      color: #143a7d;
      font-size: 0.95rem;
    }}

    .step p {{
      margin: 0;
      font-size: 0.82rem;
      color: #334155;
      line-height: 1.34;
    }}

    .step::after {{
      content: '→';
      position: absolute;
      right: -11px;
      top: 42%;
      color: #3867b4;
      font-size: 1.08rem;
      font-weight: 700;
    }}

    .step:last-child::after {{ content: ''; }}

    .viz-grid {{
      margin-top: 14px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
      align-items: stretch;
    }}

    .viz-card {{
      background: #fbfdff;
      border: 1px solid #d9e4f7;
      border-radius: 14px;
      padding: 12px;
      min-height: 420px;
    }}

    .viz-card h3 {{
      font-size: 1.02rem;
      margin-bottom: 4px;
    }}

    .viz {{
      margin-top: 8px;
    }}

    .table-stack {{
      display: grid;
      gap: 14px;
      margin-top: 14px;
    }}

    .table-card {{
      background: #fbfdff;
      border: 1px solid #d8e3f4;
      border-radius: 14px;
      padding: 14px;
    }}

    .table-head {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 12px;
      margin-bottom: 10px;
    }}

    .table-head h3 {{
      font-size: 1.02rem;
      margin-bottom: 4px;
    }}

    .meta {{
      font-size: 0.82rem;
      color: #556b8a;
      margin-top: 5px;
      margin-bottom: 0;
    }}

    .btn {{
      display: inline-block;
      padding: 8px 12px;
      border-radius: 10px;
      background: linear-gradient(135deg, #1d4ed8, #2563eb);
      color: #fff;
      font-size: 0.83rem;
      font-weight: 600;
      text-decoration: none;
      border: 1px solid rgba(29,78,216,0.5);
    }}

    .table-tools input {{
      width: 100%;
      border: 1px solid #cad6ea;
      border-radius: 10px;
      padding: 9px 11px;
      font-size: 0.9rem;
      background: #fff;
      margin-bottom: 10px;
    }}

    .table-wrap {{
      border: 1px solid #d7e2f3;
      border-radius: 10px;
      overflow: auto;
      max-height: 480px;
      background: #fff;
    }}

    table.data-table {{
      border-collapse: collapse;
      width: 100%;
      font-size: 0.78rem;
      min-width: 940px;
    }}

    table.data-table th,
    table.data-table td {{
      border-bottom: 1px solid #ecf1f8;
      padding: 7px 8px;
      text-align: left;
      vertical-align: top;
    }}

    table.data-table th {{
      position: sticky;
      top: 0;
      z-index: 1;
      background: #eff5ff;
      font-family: 'Space Grotesk', sans-serif;
      font-weight: 600;
      color: #143a7d;
    }}

    footer {{
      margin-top: 24px;
      text-align: center;
      color: #5a6f8f;
      font-size: 0.82rem;
      padding-bottom: 10px;
    }}

    @media (max-width: 1280px) {{
      .kpi-grid {{ grid-template-columns: repeat(3, minmax(150px, 1fr)); }}
      .process {{ grid-template-columns: repeat(3, minmax(160px, 1fr)); }}
      .step::after {{ content: ''; }}
      .viz-grid {{ grid-template-columns: 1fr; }}
    }}

    @media (max-width: 760px) {{
      .page {{ padding: 14px; }}
      .hero {{ padding: 18px; }}
      .kpi-grid {{ grid-template-columns: repeat(2, minmax(130px, 1fr)); }}
      .process {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <main class=\"page\">
    <section class=\"hero\">
      <div class=\"eyebrow\">Causality Audit Dashboard</div>
      <h1>Guided vs Baseline Failure Causality Report</h1>
      <p class=\"subtitle\">Premium visual research dashboard generated from all audit CSV artifacts. This view is optimized for 16:9 laptops, with noob-friendly explanations, full raw tables, and expert-level diagnostic charts.</p>
      <div class=\"hero-meta\">
        <span class=\"pill\">Generated: {generated_at}</span>
        <span class=\"pill\">Scope: week*_Adnan eval JSONL + notebook configs</span>
        <span class=\"pill\">Source folder: FT_result/causality_audit</span>
      </div>

      <div class=\"kpi-grid\">
        <article class=\"kpi blue\">
          <div class=\"label\">Paired Questions</div>
          <div class=\"value\">{kpis['total_pairs']:,}</div>
          <div class=\"sub\">Guided vs baseline aligned comparisons</div>
        </article>
        <article class=\"kpi blue\">
          <div class=\"label\">Guided Accuracy</div>
          <div class=\"value\">{kpis['guided_acc']:.4f}</div>
          <div class=\"sub\">Blue = guided pipeline</div>
        </article>
        <article class=\"kpi red\">
          <div class=\"label\">Baseline Accuracy</div>
          <div class=\"value\">{kpis['baseline_acc']:.4f}</div>
          <div class=\"sub\">Red = baseline system</div>
        </article>
        <article class=\"kpi teal\">
          <div class=\"label\">Accuracy Delta</div>
          <div class=\"value\">{kpis['accuracy_delta']:+.4f}</div>
          <div class=\"sub\">Guided - baseline</div>
        </article>
        <article class=\"kpi amber\">
          <div class=\"label\">Top Root Cause</div>
          <div class=\"value\">{str(kpis['top_cause']).replace('_', ' ')}</div>
          <div class=\"sub\">{kpis['top_cause_count']:,} guided-only-wrong cases</div>
        </article>
      </div>
    </section>

    <section class=\"section\">
      <h2>Investigation Process Diagram</h2>
      <p class=\"muted\">This is the exact workflow used to produce the causality findings and all CSV evidence tables.</p>
      <div class=\"process\">
        <article class=\"step\"><b>1) Notebook Parsing</b><p>Extracted guide/solver model identities from notebook configs to map experimental combos.</p></article>
        <article class=\"step\"><b>2) JSONL Ingestion</b><p>Loaded evaluation JSONL records, excluded training and duplicate artifacts, and tracked parse errors.</p></article>
        <article class=\"step\"><b>3) Mode Inference</b><p>Normalized records into guided/baseline/cot/ceiling modes for clean comparability.</p></article>
        <article class=\"step\"><b>4) Pair Alignment</b><p>Matched guided and baseline rows by benchmark + question key / idx for fair per-question comparison.</p></article>
        <article class=\"step\"><b>5) Causal Scoring</b><p>Assigned guided-only-wrong cases to root-cause buckets using vote/refiner/step-quality signals.</p></article>
        <article class=\"step\"><b>6) Export + Visualize</b><p>Produced CSV evidence files and this interactive report for researcher and teammate handoff.</p></article>
      </div>
    </section>

    <section class=\"section\">
      <h2>Graphs and Diagrams</h2>
      <p class=\"muted\">Use these visuals first; they tell the complete story before diving into raw tables.</p>
      <div class=\"viz-grid\">{''.join(chart_blocks)}</div>
    </section>

    <section class=\"section\">
      <h2>All CSV Tables</h2>
      <p class=\"muted\">Every CSV from the audit is shown below with search and direct download.</p>
      <div class=\"table-stack\">{''.join(csv_cards)}</div>
    </section>

    <footer>
      Research Dashboard | Built from FT_result/causality_audit CSV outputs
    </footer>
  </main>

  <script>
    function filterTable(tableId, query) {{
      const table = document.getElementById(tableId);
      if (!table) return;
      const rows = table.tBodies[0].rows;
      const q = (query || '').toLowerCase().trim();
      for (let i = 0; i < rows.length; i++) {{
        const txt = rows[i].innerText.toLowerCase();
        rows[i].style.display = txt.includes(q) ? '' : 'none';
      }}
    }}
  </script>
</body>
</html>
"""


def main() -> None:
    script_path = Path(__file__).resolve()
    ft_dir = script_path.parent
    audit_dir = ft_dir / "causality_audit"

    data = load_csvs(audit_dir)
    cast_columns(data)

    html = build_html(audit_dir, data)
    out_file = audit_dir / "causality_research_dashboard.html"
    out_file.write_text(html, encoding="utf-8")

    print(f"Report generated: {out_file}")


if __name__ == "__main__":
    main()
