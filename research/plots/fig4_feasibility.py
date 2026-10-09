#!/usr/bin/env python3
"""
Figure 4: Feasibility Graph Density Across Public Pools and Scenario Families.

Publication-quality two-panel figure:
- Subplot 1: Feasibility graph density across 10 public pools (visible vs. active edges).
- Subplot 2: Generated-world feasibility by scenario family across clarification stages.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# Output paths
OUTPUT_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = OUTPUT_DIR / "fig4_feasibility.png"


# Subplot 1 Data: Public Pools Feasibility Density
PUBLIC_POOLS = [
    "public_01",
    "public_02",
    "public_03",
    "public_04",
    "public_05",
    "public_06",
    "public_07",
    "public_08",
    "public_09",
    "public_10",
]
VISIBLE_FEASIBLE = [98, 84, 79, 85, 142, 117, 112, 106, 75, 89]
ACTIVE_FEASIBLE = [15, 12, 23, 20, 31, 13, 21, 15, 22, 15]
MAX_DEGREE = [13, 12, 9, 12, 17, 15, 11, 15, 8, 7]


# Subplot 2 Data: Scenario Family Feasibility (Mean Edges)
SCENARIO_FAMILIES = [
    "Development",
    "Sparse",
    "Cold start",
    "Delayed",
    "Shift",
    "Drift",
]
BEFORE_CLARIFICATION = [17.8, 2.0, 8.6, 17.8, 17.8, 17.8]
AFTER_NON_DECLINED = [59.6, 8.2, 49.8, 59.6, 59.6, 59.6]
ALL_ARRIVAL_TRUTH = [265.0, 45.6, 272.8, 265.0, 265.0, 265.0]


def plot_feasibility(save_path: Path = OUTPUT_FILE) -> None:
    """Generate and save publication-quality Figure 4."""
    # Seaborn theme and colorblind palette
    sns.set_theme(style="whitegrid")
    palette = sns.color_palette("colorblind")
    c_visible = palette[0]  # #0173b2 (blue)
    c_active = palette[1]   # #de8f05 (orange)
    c_truth = palette[2]    # #029e73 (green)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # -------------------------------------------------------------
    # Subplot 1: Feasibility graph density across public pools
    # -------------------------------------------------------------
    ax1 = axes[0]
    n_pools = len(PUBLIC_POOLS)
    x1 = np.arange(n_pools)
    width1 = 0.38

    rects1_vis = ax1.bar(
        x1 - width1 / 2,
        VISIBLE_FEASIBLE,
        width1,
        label="Visible feasible",
        color=c_visible,
        alpha=0.95,
    )
    rects1_act = ax1.bar(
        x1 + width1 / 2,
        ACTIVE_FEASIBLE,
        width1,
        label="Active feasible",
        color=c_active,
        alpha=0.95,
    )

    ax1.bar_label(rects1_vis, padding=3, fontsize=8)
    ax1.bar_label(rects1_act, padding=3, fontsize=8)

    ax1.set_xticks(x1)
    ax1.set_xticklabels(PUBLIC_POOLS, rotation=35, ha="right", fontsize=9.5)
    ax1.set_ylabel("Feasible Edges (Count)", fontsize=11, fontweight="bold")
    ax1.set_title("Feasibility Graph Density Across Public Pools", fontsize=12, fontweight="bold", pad=10)
    ax1.set_ylim(0, 165)
    ax1.legend(loc="upper right", frameon=True, framealpha=0.9, fontsize=9.5)

    # -------------------------------------------------------------
    # Subplot 2: Generated-world feasibility by scenario family
    # -------------------------------------------------------------
    ax2 = axes[1]
    n_fams = len(SCENARIO_FAMILIES)
    x2 = np.arange(n_fams)
    width2 = 0.27

    rects2_before = ax2.bar(
        x2 - width2,
        BEFORE_CLARIFICATION,
        width2,
        label="Before clarification",
        color=c_visible,
        alpha=0.95,
    )
    rects2_after = ax2.bar(
        x2,
        AFTER_NON_DECLINED,
        width2,
        label="After non-declined",
        color=c_active,
        alpha=0.95,
    )
    rects2_truth = ax2.bar(
        x2 + width2,
        ALL_ARRIVAL_TRUTH,
        width2,
        label="All-arrival truth",
        color=c_truth,
        alpha=0.95,
    )

    ax2.bar_label(rects2_before, fmt="%.1f", padding=3, fontsize=7.5)
    ax2.bar_label(rects2_after, fmt="%.1f", padding=3, fontsize=7.5)
    ax2.bar_label(rects2_truth, fmt="%.1f", padding=3, fontsize=7.5)

    ax2.set_xticks(x2)
    ax2.set_xticklabels(SCENARIO_FAMILIES, rotation=20, ha="right", fontsize=9.5)
    ax2.set_ylabel("Mean Feasible Edges", fontsize=11, fontweight="bold")
    ax2.set_title("Generated-World Feasibility by Scenario Family", fontsize=12, fontweight="bold", pad=10)
    ax2.set_ylim(0, 360)
    ax2.legend(loc="upper left", frameon=True, framealpha=0.9, fontsize=9.5)

    plt.tight_layout()
    save_path = Path(save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, dpi=300)
    plt.close(fig)
    print(f"Figure successfully saved to {save_path}")


if __name__ == "__main__":
    plot_feasibility()
