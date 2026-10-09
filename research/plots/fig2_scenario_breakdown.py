#!/usr/bin/env python3
"""
Figure 2: Per-Scenario MSMI/100 Breakdown (Confirmation, 40 clusters).

Grouped bar chart comparing simple_fifo against greedy across six scenario
families evaluated on confirmation seeds 3001-3040.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Output configuration
OUTPUT_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = OUTPUT_DIR / "fig2_scenario_breakdown.png"


# Confirmation stage evaluation data (seeds 3001-3040, 40 clusters per scenario)
SCENARIOS = [
    "Development",
    "Sparse",
    "Cold Start",
    "Delayed",
    "Shift",
    "Drift",
]
GREEDY_SCORES = [0.463, 0.100, 0.438, 0.400, 0.375, 0.463]
SIMPLE_FIFO_SCORES = [0.362, 0.087, 0.475, 0.400, 0.312, 0.350]
DIFFERENCES = ["-0.100", "-0.013", "+0.037", "0.000", "-0.062", "-0.113"]
OVERALL_GREEDY_MEAN = 0.373


def plot_scenario_breakdown(save_path: Path = OUTPUT_FILE) -> None:
    """Generate and save publication-quality Figure 2."""
    sns.set_theme(style="whitegrid")

    fig, ax = plt.subplots(figsize=(10, 5))

    x = np.arange(len(SCENARIOS))
    bar_width = 0.35

    # Grouped bars
    rects_greedy = ax.bar(
        x - bar_width / 2,
        GREEDY_SCORES,
        bar_width,
        label="greedy",
        color="#2196F3",
        edgecolor="none",
        alpha=0.95,
        zorder=3,
    )
    rects_fifo = ax.bar(
        x + bar_width / 2,
        SIMPLE_FIFO_SCORES,
        bar_width,
        label="simple_fifo",
        color="#FF9800",
        edgecolor="none",
        alpha=0.95,
        zorder=3,
    )

    # Horizontal dashed line at overall greedy mean
    ax.axhline(
        y=OVERALL_GREEDY_MEAN,
        color="#455a64",
        linestyle="--",
        linewidth=1.4,
        label=f"Overall greedy mean ({OVERALL_GREEDY_MEAN:.3f})",
        zorder=2,
    )

    # Difference annotation above each scenario pair
    for i in range(len(SCENARIOS)):
        max_height = max(GREEDY_SCORES[i], SIMPLE_FIFO_SCORES[i])
        diff_text = f"Δ = {DIFFERENCES[i]}"
        ax.annotate(
            diff_text,
            xy=(x[i], max_height),
            xytext=(0, 6),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9.5,
            fontweight="bold",
            color="#263238",
            zorder=4,
        )

    # Axis styling and labeling
    ax.set_xticks(x)
    ax.set_xticklabels(SCENARIOS, fontsize=10.5)
    ax.set_xlabel("Scenario", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_ylabel("MSMI per 100 arrived", fontsize=11, fontweight="bold", labelpad=8)
    ax.set_title(
        "Per-Scenario MSMI/100 (Confirmation, 40 clusters)",
        fontsize=13,
        fontweight="bold",
        pad=14,
    )
    ax.set_ylim(0, 0.64)
    ax.set_xlim(-0.6, len(SCENARIOS) - 0.4)

    # Legend configuration
    ax.legend(
        loc="upper center",
        ncol=3,
        frameon=True,
        facecolor="white",
        edgecolor="#cccccc",
        framealpha=0.95,
        fontsize=10,
    )

    plt.tight_layout()

    save_path = Path(save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"Saved scenario breakdown plot to: {save_path}")


if __name__ == "__main__":
    plot_scenario_breakdown()
