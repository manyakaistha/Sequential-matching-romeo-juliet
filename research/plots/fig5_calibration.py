#!/usr/bin/env python3
"""Calibration reliability diagram for the simple_fifo terminal model.

Plots unconditional funnel calibration across 5 funnel stages and reliability
diagram for the terminal model across two prediction bins (n = 18,133 introductions).
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# Confirmation stage empirical data (18,133 introductions)
FUNNEL_STAGES = [
    {"stage": "Qualified terminal", "predicted": 0.0115, "observed": 0.0088},
    {"stage": "Both positive 2nd", "predicted": 0.032, "observed": 0.027},
    {"stage": "Date", "predicted": 0.138, "observed": 0.105},
    {"stage": "Both accept", "predicted": 0.177, "observed": 0.134},
    {"stage": "Both respond", "predicted": 0.585, "observed": 0.583},
]

TERMINAL_BINS = [
    {"bin": 1, "n": 2143, "predicted": 0.00623, "observed": 0.00840},
    {"bin": 2, "n": 15990, "predicted": 0.01219, "observed": 0.00882},
]

SIGNED_ERROR = -0.00281


def plot_calibration(output_path: Path) -> None:
    """Generate and save the two-panel calibration reliability figure."""
    sns.set_theme(style="whitegrid")
    palette = sns.color_palette("colorblind")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # -------------------------------------------------------------
    # Left subplot: Unconditional funnel calibration (log-log scale)
    # -------------------------------------------------------------
    funnel_preds = [d["predicted"] for d in FUNNEL_STAGES]
    funnel_obs = [d["observed"] for d in FUNNEL_STAGES]

    # Perfect calibration reference diagonal
    ax1.plot(
        [0.005, 1.0],
        [0.005, 1.0],
        linestyle="--",
        color="0.45",
        linewidth=1.5,
        label="Perfect calibration (y = x)",
        zorder=2,
    )

    # Funnel stages line and points
    ax1.plot(
        funnel_preds,
        funnel_obs,
        marker="o",
        markersize=7,
        color=palette[0],
        linewidth=2,
        label="Funnel stages",
        zorder=3,
    )

    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_xlim(0.006, 1.0)
    ax1.set_ylim(0.006, 1.0)

    # Clean scalar tick format for log scale
    formatter = ticker.FuncFormatter(lambda val, _: f"{val:g}")
    ax1.xaxis.set_major_formatter(formatter)
    ax1.yaxis.set_major_formatter(formatter)

    ax1.set_xlabel("Predicted Probability", fontsize=11, fontweight="bold")
    ax1.set_ylabel("Observed Probability", fontsize=11, fontweight="bold")
    ax1.set_title("Unconditional Funnel Calibration", fontsize=12, fontweight="bold")
    ax1.legend(loc="upper left", frameon=True, framealpha=0.95)

    # Stage annotations with directional offsets to prevent collisions
    label_offsets = {
        "Qualified terminal": ((10, -12), "left", "top"),
        "Both positive 2nd": ((-12, 10), "right", "bottom"),
        "Date": ((10, -14), "left", "top"),
        "Both accept": ((-12, 10), "right", "bottom"),
        "Both respond": ((-12, 10), "right", "bottom"),
    }

    for item in FUNNEL_STAGES:
        name = item["stage"]
        p, o = item["predicted"], item["observed"]
        offset, ha, va = label_offsets[name]
        ax1.annotate(
            name,
            xy=(p, o),
            xytext=offset,
            textcoords="offset points",
            fontsize=9,
            ha=ha,
            va=va,
            arrowprops=dict(
                arrowstyle="->",
                color="0.35",
                lw=0.8,
                shrinkA=2,
                shrinkB=3,
            ),
        )

    # -------------------------------------------------------------
    # Right subplot: Terminal model reliability diagram (binned bars)
    # -------------------------------------------------------------
    bin_preds = [b["predicted"] for b in TERMINAL_BINS]
    bin_obs = [b["observed"] for b in TERMINAL_BINS]
    bin_ns = [b["n"] for b in TERMINAL_BINS]

    diag_max = 0.016
    bar_width = 0.0024

    # Perfect calibration reference diagonal
    ax2.plot(
        [0, diag_max],
        [0, diag_max],
        linestyle="--",
        color="0.45",
        linewidth=1.5,
        label="Perfect calibration (y = x)",
        zorder=2,
    )

    # Bins as vertical bars centered at predicted probability
    ax2.bar(
        bin_preds,
        bin_obs,
        width=bar_width,
        color=palette[0],
        edgecolor="0.2",
        alpha=0.85,
        label="Observed (by bin)",
        zorder=3,
    )

    # Bin labels positioned above bars
    for i, b in enumerate(TERMINAL_BINS):
        ax2.text(
            bin_preds[i],
            bin_obs[i] + 0.0004,
            f"Bin {b['bin']}\n(n = {bin_ns[i]:,})",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
            zorder=4,
        )

    ax2.set_xlim(0, diag_max)
    ax2.set_ylim(0, diag_max)
    ax2.set_xlabel("Predicted Probability", fontsize=11, fontweight="bold")
    ax2.set_ylabel("Observed Probability", fontsize=11, fontweight="bold")
    ax2.set_title("Terminal Prediction Reliability Diagram", fontsize=12, fontweight="bold")

    # Annotate signed error
    ax2.annotate(
        f"Signed error: {SIGNED_ERROR:.5f}",
        xy=(0.05, 0.90),
        xycoords="axes fraction",
        fontsize=10,
        fontweight="bold",
        bbox=dict(
            boxstyle="round,pad=0.4",
            facecolor="white",
            edgecolor="0.6",
            alpha=0.95,
        ),
    )

    ax2.legend(loc="lower right", frameon=True, framealpha=0.95)

    plt.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=300)
    plt.close(fig)


def main() -> None:
    output_path = (
        Path(__file__).resolve().parent / "fig5_calibration.png"
    )
    plot_calibration(output_path)
    print(f"Calibration plot successfully saved to {output_path}")


if __name__ == "__main__":
    main()
