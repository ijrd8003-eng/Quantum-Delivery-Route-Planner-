"""
compare_results.py

Compares Classical TSP vs Quantum QAOA results.

Reads:
    results/classical/classical_result.json
    results/simulator/processed_results.json

Outputs:
    results/comparison/comparison_result.json

Author:
"""

import json
import sys
from pathlib import Path

# -------------------------------------------------------
# Project Path
# -------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from comparison.metrics import generate_performance_report

# -------------------------------------------------------
# Paths
# -------------------------------------------------------

CLASSICAL_FILE = (
    BASE_DIR / "results" / "classical" / "classical_result.json"
)

QUANTUM_FILE = (
    BASE_DIR / "results" / "simulator" / "processed_results.json"
)

OUTPUT_DIR = BASE_DIR / "results" / "comparison"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "comparison_result.json"


# -------------------------------------------------------
# Load Results
# -------------------------------------------------------

def load_classical(path: Path) -> dict:
    with open(path, "r") as f:
        return json.load(f)


def load_quantum(path: Path) -> dict:
    with open(path, "r") as f:
        return json.load(f)


# -------------------------------------------------------
# Extract Metrics
# -------------------------------------------------------

def extract_classical_metrics(data: dict) -> dict:
    return {
        "solver": data.get("solver", "Unknown"),
        "route_cost": float(data.get("route_cost", 0)),
        "execution_time": float(data.get("execution_time", 0)),
        "route_names": data.get("route_names", []),
        "route_indices": data.get("route_indices", [])
    }


def extract_quantum_metrics(data: dict) -> dict:
    stats = data.get("statistics", {})
    return {
        "route_cost": float(stats.get("route_cost") or 0),
        "execution_time": float(stats.get("execution_time", 2.5)),
        "unique_solutions": int(stats.get("unique_solutions", 1)),
        "best_probability": float(stats.get("best_probability", 0)),
        "best_bitstring": stats.get("best_bitstring", ""),
        "decoded_route": data.get("decoded_route", [])
    }


# -------------------------------------------------------
# Display
# -------------------------------------------------------

def display_comparison(report: dict):
    cost_c = report["classical"]
    cost_q = report["quantum"]
    perf = report["performance"]

    print()
    print("=" * 65)
    print(f"  {'METRIC':<30} {'CLASSICAL':<15} {'QUANTUM':<15}")
    print("=" * 65)
    print(f"  {'Route Cost':<30} {cost_c['route_cost']:<15.4f} {cost_q['route_cost']:<15.4f}")
    print(f"  {'Execution Time (s)':<30} {cost_c['execution_time']:<15.6f} {cost_q['execution_time']:<15.4f}")
    print(f"  {'Unique Solutions':<30} {'1':<15} {cost_q['unique_solutions']:<15}")
    print(f"  {'Best Probability':<30} {'N/A':<15} {cost_q['best_probability']:<15.6f}")
    print("=" * 65)
    print()
    print(f"  Cost Winner      : {perf['summary']['cost_winner']}")
    print(f"  Speed Winner     : {perf['summary']['speed_winner']}")
    print(f"  Quantum Accuracy : {perf['summary']['quantum_accuracy']:.2f}%")
    print(f"  Solution Quality : {perf['summary']['quantum_quality']}")
    print()
    print(f"  Cost Difference  : {perf['cost_comparison']['absolute_diff']:.4f}")
    print(f"  Cost % Diff      : {perf['cost_comparison']['percentage_diff']:.2f}%")
    print(f"  Speed Ratio      : {perf['speed_comparison']['description']}")
    print("=" * 65)


# -------------------------------------------------------
# Main
# -------------------------------------------------------

def main():
    print("=" * 65)
    print("Comparing Classical vs Quantum QAOA Results")
    print("=" * 65)

    # Load
    classical_data = load_classical(CLASSICAL_FILE)
    quantum_data = load_quantum(QUANTUM_FILE)

    classical = extract_classical_metrics(classical_data)
    quantum = extract_quantum_metrics(quantum_data)

    # Generate report
    performance = generate_performance_report(
        classical_cost=classical["route_cost"],
        quantum_cost=quantum["route_cost"],
        classical_time=classical["execution_time"],
        quantum_time=quantum["execution_time"],
        quantum_unique_solutions=quantum["unique_solutions"],
        best_probability=quantum["best_probability"]
    )

    # Build final comparison
    comparison = {
        "classical": classical,
        "quantum": quantum,
        "performance": performance
    }

    # Display
    display_comparison(comparison)

    # Save
    with open(OUTPUT_FILE, "w") as f:
        json.dump(comparison, f, indent=4)

    print(f"\nComparison saved to: {OUTPUT_FILE}")

    return comparison


if __name__ == "__main__":
    main()
