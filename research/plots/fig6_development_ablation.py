#!/usr/bin/env python3
"""
fig6_development_ablation.py

Cleveland dot plot showing development-stage component ablation results
across seeds 101-105.
"""

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd
import seaborn as sns


def plot_development_ablation() -> None:
    # Component ablation data (seeds 101-105, MSMI/100 mean)
    data = [
        ("batch7", 0.417),
        ("batch3", 0.383),
        ("greedy", 0.367),
        ("zero", 0.367),
        ("static", 0.350),
        ("batch5", 0.350),
        ("fifo", 0.317),
        ("no_learning", 0.317),
        ("full", 0.300),
        ("greedy_engine", 0.300),
        ("no_dfm", 0.300),
        ("hard15", 0.283),
        ("product", 0.267),
        ("random", 0.267),
        ("hungarian", 0.250),
        ("unilateral", 0.250),
        ("no_asks", 0.183),
        ("soft_only", 0.167),
        ("no_active_asks", 0.167),
    ]

    greedy_threshold = 0.367

    # Sort ascending so highest score appears at top (highest y-index)
    df = pd.DataFrame(data, columns=["component", "score"])
    df = df.sort_values(by="score", ascending=True).reset_index(drop=True)

    # Colorblind-friendly green and red palettes
    color_ge = "#2e7d32"  # >= greedy
    color_lt = "#c62828"  # < greedy
    colors = [color_ge if s >= greedy_threshold else color_lt for s in df["score"]]

    # Seaborn whitegrid style
    sns.set_theme(style="whitegrid")

    fig, ax = plt.subplots(figsize=(8, 8))

    # Vertical reference line at greedy baseline
    ax.axvline(
        x=greedy_threshold,
        color="#455a64",
        linestyle="--",
        linewidth=1.5,
        zorder=2,
        label=f"Greedy baseline ({greedy_threshold:.3f})",
    )

    # Cleveland dot plot points
    ax.scatter(
        df["score"],
        range(len(df)),
        c=colors,
        s=85,
        edgecolor="black",
        linewidth=0.8,
        zorder=3,
    )

    # Legend elements
    legend_elements = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            label=f"≥ Greedy ({greedy_threshold:.3f})",
            markerfacecolor=color_ge,
            markeredgecolor="black",
            markersize=9,
        ),
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            label=f"< Greedy ({greedy_threshold:.3f})",
            markerfacecolor=color_lt,
            markeredgecolor="black",
            markersize=9,
        ),
        Line2D(
            [0],
            [0],
            color="#455a64",
            linestyle="--",
            linewidth=1.5,
            label=f"Greedy baseline ({greedy_threshold:.3f})",
        ),
    ]
    ax.legend(
        handles=legend_elements,
        loc="lower right",
        frameon=True,
        facecolor="white",
        edgecolor="#cccccc",
        framealpha=0.95,
        fontsize=10.5,
    )

    # Axis configuration
    ax.set_yticks(range(len(df)))
    ax.set_yticklabels(df["component"], fontsize=10)
    ax.set_xlim(0.14, 0.44)
    ax.set_xlabel("Mean Score (MSMI / 100)", fontsize=12, labelpad=8)
    ax.set_ylabel("Component", fontsize=12, labelpad=8)
    ax.set_title("Component Ablation (Seeds 101-105)", fontsize=14, fontweight="bold", pad=12)

    plt.tight_layout()

    out_dir = Path("/Volumes/1700 APFS/PERSONAL_PROGRAMMING_PROJECTS/romio-juliet/The-Sequential-Matching-Problem/research/plots")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "fig6_ablation_dotplot.png"

    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"Saved ablation dot plot to: {out_path}")


if __name__ == "__main__":
    plot_development_ablation()
