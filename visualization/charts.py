"""
charts.py

Generates comparison charts between
Classical TSP and Quantum QAOA results.

Charts:
    1. Route Cost Comparison
    2. Execution Time Comparison
    3. Distance Savings (Pie)
    4. Overall Combined Dashboard Chart

Reads:
    results/simulator/processed_results.json
    results/classical/classical_result.json

Outputs:
    visualization/outputs/*.png
    results/figures/*.png

Author:
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

SIM_RESULT = (
    BASE_DIR / "results" / "simulator" / "processed_results.json"
)

CLASSICAL_RESULT = (
    BASE_DIR / "results" / "classical" / "classical_result.json"
)

VIZ_OUTPUT = BASE_DIR / "visualization" / "outputs"
FIG_OUTPUT = BASE_DIR / "results" / "figures"

VIZ_OUTPUT.mkdir(parents=True, exist_ok=True)
FIG_OUTPUT.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------
# Color Palette
# ---------------------------------------------------------

COLOR_CLASSICAL = "#2196F3"    # Blue
COLOR_QUANTUM   = "#FF5722"    # Deep Orange
COLOR_SAVING    = "#4CAF50"    # Green
COLOR_REMAINING = "#BDBDBD"    # Grey

STYLE_BG = "#1a1a2e"
STYLE_TEXT = "#FFFFFF"

plt.rcParams.update({
    "figure.facecolor": STYLE_BG,
    "axes.facecolor": "#16213e",
    "axes.edgecolor": "#4a4a8a",
    "axes.labelcolor": STYLE_TEXT,
    "xtick.color": STYLE_TEXT,
    "ytick.color": STYLE_TEXT,
    "text.color": STYLE_TEXT,
    "grid.color": "#2a2a5a",
    "grid.alpha": 0.4,
    "font.family": "DejaVu Sans",
})

# ---------------------------------------------------------
# Load Results
# ---------------------------------------------------------

with open(SIM_RESULT, "r") as f:
    quantum = json.load(f)

quantum_cost = quantum["statistics"].get("route_cost") or 0
quantum_cost = float(quantum_cost) if quantum_cost else 100.0

try:
    with open(CLASSICAL_RESULT, "r") as f:
        classical = json.load(f)
    classical_cost = float(classical.get("route_cost", quantum_cost * 0.95))
    classical_time = float(classical.get("execution_time", 0.05))

except FileNotFoundError:
    print("[charts.py] Classical result not found. Using placeholder values.")
    classical_cost = quantum_cost * 0.95
    classical_time = 0.05

quantum_time = float(quantum["statistics"].get("execution_time", 2.5))
quantum_unique = int(quantum["statistics"].get("unique_solutions", 1))
quantum_prob = float(quantum["statistics"].get("best_probability", 0.1))


# ---------------------------------------------------------
# 1. Route Cost Comparison Bar Chart
# ---------------------------------------------------------

def plot_cost_comparison():
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor(STYLE_BG)

    labels = ["Classical\n(OR-Tools)", "Quantum\n(QAOA)"]
    costs = [classical_cost, quantum_cost]
    colors = [COLOR_CLASSICAL, COLOR_QUANTUM]

    bars = ax.bar(labels, costs, color=colors, width=0.45, edgecolor="white", linewidth=0.5)

    for bar, val in zip(bars, costs):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(costs) * 0.01,
            f"{val:.2f}",
            ha="center", va="bottom",
            color=STYLE_TEXT, fontweight="bold", fontsize=12
        )

    # Annotation
    diff_pct = ((quantum_cost - classical_cost) / classical_cost * 100) if classical_cost > 0 else 0
    ax.set_title(
        f"Route Cost Comparison\n(Quantum is {abs(diff_pct):.1f}% {'higher' if diff_pct > 0 else 'lower'} than Classical)",
        color=STYLE_TEXT, fontsize=14, pad=15
    )
    ax.set_ylabel("Total Route Distance", color=STYLE_TEXT, fontsize=12)
    ax.grid(axis="y", alpha=0.3)
    ax.set_ylim(0, max(costs) * 1.2)

    plt.tight_layout()
    fig.savefig(VIZ_OUTPUT / "route_cost_comparison.png", dpi=200, bbox_inches="tight")
    fig.savefig(FIG_OUTPUT / "route_cost_comparison.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("  [OK] Route cost comparison saved.")


# ---------------------------------------------------------
# 2. Execution Time Comparison
# ---------------------------------------------------------

def plot_execution_time():
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor(STYLE_BG)

    labels = ["Classical\n(OR-Tools)", "Quantum\n(QAOA Sim)"]
    times = [classical_time, quantum_time]
    colors = [COLOR_CLASSICAL, COLOR_QUANTUM]

    bars = ax.bar(labels, times, color=colors, width=0.45, edgecolor="white", linewidth=0.5)

    for bar, val in zip(bars, times):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(times) * 0.01,
            f"{val:.4f}s",
            ha="center", va="bottom",
            color=STYLE_TEXT, fontweight="bold", fontsize=11
        )

    ax.set_title("Execution Time Comparison", color=STYLE_TEXT, fontsize=14, pad=15)
    ax.set_ylabel("Time (seconds)", color=STYLE_TEXT, fontsize=12)
    ax.grid(axis="y", alpha=0.3)
    ax.set_ylim(0, max(times) * 1.25)

    # Note about simulation overhead
    ax.text(
        0.5, 0.02,
        "* QAOA time includes classical optimization loop overhead",
        transform=ax.transAxes, ha="center", color="#AAAAAA", fontsize=9
    )

    plt.tight_layout()
    fig.savefig(VIZ_OUTPUT / "execution_time_comparison.png", dpi=200, bbox_inches="tight")
    fig.savefig(FIG_OUTPUT / "execution_time_comparison.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("  [OK] Execution time comparison saved.")


# ---------------------------------------------------------
# 3. Distance Savings Pie Chart
# ---------------------------------------------------------

def plot_distance_savings():
    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor(STYLE_BG)

    if classical_cost > 0:
        saving_pct = max(0, (classical_cost - quantum_cost) / classical_cost * 100)
    else:
        saving_pct = 0

    remaining_pct = 100 - saving_pct

    wedges, texts, autotexts = ax.pie(
        [saving_pct + 0.01, remaining_pct],
        labels=["Distance\nSaved", "Remaining"],
        autopct="%1.1f%%",
        colors=[COLOR_SAVING, COLOR_REMAINING],
        startangle=90,
        wedgeprops=dict(edgecolor="white", linewidth=1.5),
        textprops=dict(color=STYLE_TEXT, fontsize=12)
    )

    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontweight("bold")

    title = (
        f"Distance Saving: {saving_pct:.1f}%"
        if saving_pct > 0
        else "Classical has better solution"
    )
    ax.set_title(title, color=STYLE_TEXT, fontsize=13, pad=15)

    plt.tight_layout()
    fig.savefig(VIZ_OUTPUT / "distance_savings.png", dpi=200, bbox_inches="tight")
    fig.savefig(FIG_OUTPUT / "distance_savings.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("  [OK] Distance savings pie chart saved.")


# ---------------------------------------------------------
# 4. Overall Combined Comparison Dashboard
# ---------------------------------------------------------

def plot_overall_comparison():
    fig, axes = plt.subplots(1, 3, figsize=(16, 6))
    fig.patch.set_facecolor(STYLE_BG)
    fig.suptitle(
        "Classical TSP vs Quantum QAOA — Overall Comparison",
        color=STYLE_TEXT, fontsize=16, fontweight="bold", y=1.02
    )

    # --- Subplot 1: Costs ---
    ax = axes[0]
    ax.set_facecolor("#16213e")
    labels = ["Classical", "QAOA"]
    costs = [classical_cost, quantum_cost]
    bars = ax.bar(labels, costs, color=[COLOR_CLASSICAL, COLOR_QUANTUM], edgecolor="white", linewidth=0.5)
    for bar, val in zip(bars, costs):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(costs) * 0.01,
            f"{val:.1f}", ha="center", color=STYLE_TEXT, fontweight="bold"
        )
    ax.set_title("Route Cost", color=STYLE_TEXT, fontsize=12)
    ax.set_ylabel("Distance", color=STYLE_TEXT)
    ax.grid(axis="y", alpha=0.3)

    # --- Subplot 2: Time ---
    ax = axes[1]
    ax.set_facecolor("#16213e")
    times = [classical_time, quantum_time]
    bars = ax.bar(labels, times, color=[COLOR_CLASSICAL, COLOR_QUANTUM], edgecolor="white", linewidth=0.5)
    for bar, val in zip(bars, times):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(times) * 0.01,
            f"{val:.2f}s", ha="center", color=STYLE_TEXT, fontweight="bold"
        )
    ax.set_title("Execution Time", color=STYLE_TEXT, fontsize=12)
    ax.set_ylabel("Seconds", color=STYLE_TEXT)
    ax.grid(axis="y", alpha=0.3)

    # --- Subplot 3: Solution Diversity ---
    ax = axes[2]
    ax.set_facecolor("#16213e")
    diversities = [1, quantum_unique]
    bars = ax.bar(labels, diversities, color=[COLOR_CLASSICAL, COLOR_QUANTUM], edgecolor="white", linewidth=0.5)
    for bar, val in zip(bars, diversities):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(diversities) * 0.01,
            f"{val}", ha="center", color=STYLE_TEXT, fontweight="bold"
        )
    ax.set_title("Unique Solutions Found", color=STYLE_TEXT, fontsize=12)
    ax.set_ylabel("Count", color=STYLE_TEXT)
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    fig.savefig(VIZ_OUTPUT / "overall_comparison.png", dpi=200, bbox_inches="tight")
    fig.savefig(FIG_OUTPUT / "overall_comparison.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("  [OK] Overall comparison dashboard saved.")


# ---------------------------------------------------------
# Run All
# ---------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Generating Comparison Charts")
    print("=" * 60)
    print(f"  Classical Cost : {classical_cost:.4f}")
    print(f"  Quantum Cost   : {quantum_cost:.4f}")
    print(f"  Classical Time : {classical_time:.6f}s")
    print(f"  Quantum Time   : {quantum_time:.4f}s")
    print()

    plot_cost_comparison()
    plot_execution_time()
    plot_distance_savings()
    plot_overall_comparison()

    print()
    print("=" * 60)
    print("All charts generated.")
    print(f"  Saved in: {VIZ_OUTPUT}")
    print("=" * 60)