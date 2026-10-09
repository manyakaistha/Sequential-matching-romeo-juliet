#!/usr/bin/env python3
"""
Figure 3: Outcome Funnel: Introduction to Qualified MSMI.

Horizontal funnel bar chart showing conversion stages from introductions
down to qualified MSMI for simple_fifo across 240 confirmation episodes,
with a reference marker for the greedy baseline.
"""

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import seaborn as sns


# Output paths
OUTPUT_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = OUTPUT_DIR / "fig3_funnel.png"

# Confirmation policy data (simple_fifo, 240 episodes)
STAGES = [
    "Introductions",
    "Both responded",
    "Mutual acceptance",
    "Date occurred",
    "Both second-meeting positive",
    "Qualified MSMI",
]
COUNTS_FIFO = [18133, 10576, 2434, 1912, 489, 159]
FIFO_TOTAL = COUNTS_FIFO[0]
PCTS_FIFO = [c / FIFO_TOTAL * 100 for c in COUNTS_FIFO]

# Greedy baseline data (same seed set, 240 episodes)
GREEDY_TOTAL = 17954
GREEDY_MUTUAL = 2428
GREEDY_DATES = 1849
GREEDY_QUALIFIED = 179
GREEDY_QUALIFIED_PCT = GREEDY_QUALIFIED / GREEDY_TOTAL * 100


def plot_funnel(save_path: Path = OUTPUT_FILE) -> None:
    """Generate and save publication-quality Figure 3 funnel chart."""
    # Seaborn whitegrid style
    sns.set_theme(style="whitegrid")

    # Sequential blue palette getting darker at each stage
    palette = sns.color_palette("Blues", 8)[2:]

    fig, ax = plt.subplots(figsize=(10, 5))
    y_pos = np.arange(len(STAGES))

    # Horizontal bars
    bars = ax.barh(
        y_pos,
        COUNTS_FIFO,
        color=palette,
        edgecolor="#1e3d59",
        linewidth=0.8,
        height=0.55,
    )

    # Invert y-axis so funnel progresses from top to bottom
    ax.invert_yaxis()

    # Stage value labels (count and percentage of introductions)
    for i, (count, pct) in enumerate(zip(COUNTS_FIFO, PCTS_FIFO)):
        pct_str = f"{pct:.2f}%" if pct < 1.0 else f"{pct:.1f}%"
        label_text = f"{count:,} ({pct_str})"
        # Offset to prevent visual collision with greedy reference marker at stage 5
        offset = 600 if i == 5 else 350
        ax.text(
            count + offset,
            i,
            label_text,
            va="center",
            ha="left",
            fontsize=10,
            fontweight="bold",
            color="#1f2937",
        )

    # Greedy qualified count reference marker at Qualified MSMI stage
    q_y = 5
    marker_color = "#d95f02"  # Colorblind-friendly vermillion/orange
    ax.vlines(
        GREEDY_QUALIFIED,
        q_y - 0.38,
        q_y + 0.38,
        color=marker_color,
        linestyle="--",
        linewidth=2.0,
        zorder=5,
    )
    ax.plot(
        GREEDY_QUALIFIED,
        q_y,
        marker="D",
        markersize=8,
        color=marker_color,
        markeredgecolor="black",
        markeredgewidth=0.8,
        zorder=6,
    )

    # Configure axes
    ax.set_yticks(y_pos)
    ax.set_yticklabels(STAGES, fontsize=10.5)
    ax.set_xlabel("Count", fontsize=11, fontweight="bold")
    ax.set_title(
        "Outcome Funnel: Introduction to Qualified MSMI",
        fontsize=13,
        fontweight="bold",
        pad=14,
    )
    ax.set_xlim(0, 22500)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))

    # Legend for reference marker
    legend_elements = [
        Line2D(
            [0],
            [0],
            color=marker_color,
            linestyle="--",
            linewidth=2.0,
            marker="D",
            markersize=8,
            markerfacecolor=marker_color,
            markeredgecolor="black",
            markeredgewidth=0.8,
            label=f"Greedy qualified: {GREEDY_QUALIFIED} ({GREEDY_QUALIFIED_PCT:.2f}%)",
        )
    ]
    ax.legend(
        handles=legend_elements,
        loc="lower right",
        frameon=True,
        framealpha=0.95,
        facecolor="white",
        edgecolor="#cbd5e1",
        fontsize=10,
    )

    plt.tight_layout()

    save_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, dpi=300)
    plt.close(fig)
    print(f"Saved funnel chart to: {save_path}")


if __name__ == "__main__":
    plot_funnel()
