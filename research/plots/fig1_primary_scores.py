#!/usr/bin/env python3
"""
fig1_primary_scores.py

Generates publication-quality primary MSMI/100 score visualizations:
1. Confirmatory comparison: Horizontal bar chart comparing simple_fifo vs greedy
   on the 40 confirmation seed clusters (seeds 3001-3040), saved to
   fig1_primary_comparison.png.
2. Stage-by-stage comparison: Grouped bar chart comparing primary scores
   across all methods across Development (seeds 1001-1008), Selection (seeds 2001-2012),
   and Confirmation (seeds 3001-3040), saved to fig1_all_stages_grouped.png.
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Directory for saved figures
PLOTS_DIR = Path("/Volumes/1700 APFS/PERSONAL_PROGRAMMING_PROJECTS/romio-juliet/The-Sequential-Matching-Problem/research/plots")

# -----------------------------------------------------------------------------
# Self-contained Data Definitions
# -----------------------------------------------------------------------------

# Confirmation stage (seeds 3001-3040, n=40 clusters)
CONFIRMATION_SCORES = {
    "greedy": 0.373,
    "simple_fifo": 0.331,
}

CONFIRMATION_STATS = {
    "difference": -0.042,
    "p_value": 0.096,
    "ci95_difference": (-0.091, 0.008),
    "ci_half_width": (0.008 - (-0.091)) / 2.0,  # 0.0495
}

# Development stage (seeds 1001-1008)
DEVELOPMENT_SCORES = {
    "no_learning_fifo": 0.510,
    "terminal_soft": 0.510,
    "independent_fifo": 0.469,
    "simple_fifo": 0.469,
    "terminal_fifo": 0.458,
    "greedy": 0.417,
}

# Selection stage (seeds 2001-2012)
SELECTION_SCORES = {
    "no_learning_fifo": 0.347,
    "terminal_fifo": 0.340,
    "independent_fifo": 0.333,
    "greedy": 0.312,
    "simple_fifo": 0.312,
    "terminal_soft": 0.278,
}


def plot_confirmatory_comparison(output_path: Path = None) -> Path:
    """
    Generate clean horizontal bar chart for the confirmatory stage results.
    - Compares simple_fifo vs greedy on 40 seed clusters
    - Dashed vertical reference at greedy's score (0.373)
    - Error bars derived from paired difference 95% CI
    - Explicit annotations for difference (-0.042), p-value (0.096), and 95% CI [-0.091, +0.008]
    """
    if output_path is None:
        output_path = PLOTS_DIR / "fig1_primary_comparison.png"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(8, 3))

    # Display order: greedy on top (y=1), simple_fifo below (y=0)
    methods = ["simple_fifo", "greedy"]
    scores = [CONFIRMATION_SCORES[m] for m in methods]
    colors = ["#FF9800", "#2196F3"]  # simple_fifo: orange, greedy: blue
    error_hw = CONFIRMATION_STATS["ci_half_width"]

    y_pos = np.arange(len(methods))

    # Horizontal bar plot
    ax.barh(
        y_pos,
        scores,
        xerr=[error_hw, error_hw],
        capsize=5,
        height=0.40,
        color=colors,
        edgecolor="#222222",
        linewidth=0.8,
        error_kw=dict(ecolor="#333333", lw=1.4, capthick=1.4, zorder=3),
        zorder=2,
    )

    # Dashed vertical line at greedy's score
    greedy_score = CONFIRMATION_SCORES["greedy"]
    ax.axvline(
        x=greedy_score,
        color="#1976D2",
        linestyle="--",
        linewidth=1.5,
        alpha=0.9,
        label=f"Greedy score ({greedy_score:.3f})",
        zorder=1,
    )

    # Value annotations inside each bar
    for score, y in zip(scores, y_pos):
        ax.text(
            score / 2.0,
            y,
            f"{score:.3f}",
            va="center",
            ha="center",
            fontsize=11.5,
            fontweight="bold",
            color="white",
            zorder=4,
        )

    # Y-axis ticks and labels
    ax.set_yticks(y_pos)
    ax.set_yticklabels(methods, fontweight="bold", fontsize=11.5)
    ax.set_ylim(-0.55, 1.55)

    # X-axis formatting
    ax.set_xlim(0.0, 0.58)
    ax.set_xlabel("Primary Score (MSMI / 100)", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_title("Confirmatory Primary Score (40 seed clusters)", fontsize=13, fontweight="bold", pad=12)

    # Legend for the dashed reference line at upper right
    ax.legend(
        loc="upper right",
        frameon=True,
        facecolor="#fcfcfc",
        edgecolor="#b0bec5",
        fontsize=9.5,
    )

    # Statistical comparison annotation box placed neatly at lower right
    annotation_text = (
        r"$\bf{Confirmatory\ Contrast}$" + "\n"
        f"Difference: {CONFIRMATION_STATS['difference']:.3f}  (p = {CONFIRMATION_STATS['p_value']:.3f})\n"
        f"95% CI on diff: [{CONFIRMATION_STATS['ci95_difference'][0]:+.3f}, {CONFIRMATION_STATS['ci95_difference'][1]:+.3f}]"
    )

    ax.text(
        0.98,
        0.28,
        annotation_text,
        transform=ax.transAxes,
        fontsize=9.5,
        verticalalignment="center",
        horizontalalignment="right",
        bbox=dict(
            boxstyle="round,pad=0.55",
            facecolor="#fcfcfc",
            edgecolor="#b0bec5",
            linewidth=1.0,
            alpha=0.95,
        ),
        zorder=5,
    )

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    return output_path


def plot_all_stages_grouped(output_path: Path = None) -> Path:
    """
    Generate grouped bar chart comparing primary MSMI/100 scores across ALL methods
    and stages (Development, Selection, Confirmation).
    """
    if output_path is None:
        output_path = PLOTS_DIR / "fig1_all_stages_grouped.png"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    records = []
    for method, score in DEVELOPMENT_SCORES.items():
        records.append({"stage": "Development (seeds 1001-1008)", "method": method, "score": score})
    for method, score in SELECTION_SCORES.items():
        records.append({"stage": "Selection (seeds 2001-2012)", "method": method, "score": score})
    for method, score in CONFIRMATION_SCORES.items():
        records.append({"stage": "Confirmation (seeds 3001-3040)", "method": method, "score": score})

    df = pd.DataFrame(records)

    methods_order = [
        "greedy",
        "simple_fifo",
        "independent_fifo",
        "terminal_fifo",
        "terminal_soft",
        "no_learning_fifo",
    ]

    palette = {
        "Development (seeds 1001-1008)": "#56B4E9",  # Sky Blue
        "Selection (seeds 2001-2012)": "#E69F00",    # Orange
        "Confirmation (seeds 3001-3040)": "#009E73", # Bluish Green
    }

    sns.set_theme(style="whitegrid", font_scale=1.05)
    fig, ax = plt.subplots(figsize=(10, 5.5))

    sns.barplot(
        data=df,
        x="score",
        y="method",
        hue="stage",
        order=methods_order,
        palette=palette,
        ax=ax,
        edgecolor="#333333",
        linewidth=0.8,
    )

    ax.set_title("Primary MSMI / 100 Scores Across Research Stages", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Primary Score (MSMI / 100)", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_ylabel("Method", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_xlim(0, 0.60)
    ax.legend(title="Stage", loc="lower right", frameon=True, facecolor="white", edgecolor="#cccccc")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    return output_path


def main() -> None:
    p1 = plot_confirmatory_comparison()
    print(f"Confirmatory comparison plot saved to: {p1}")

    p2 = plot_all_stages_grouped()
    print(f"All stages grouped plot saved to: {p2}")


if __name__ == "__main__":
    main()
