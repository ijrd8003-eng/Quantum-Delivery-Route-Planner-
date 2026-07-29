"""
classical_result.py

Loads the classical TSP result and prints
a formatted summary report.

Reads:
    results/classical/classical_result.json

Author:
"""

import json
from pathlib import Path

# -------------------------------------------------------
# Paths
# -------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RESULT_FILE = BASE_DIR / "results" / "classical" / "classical_result.json"


# -------------------------------------------------------
# Load and Display
# -------------------------------------------------------

def display_classical_result(result: dict):
    print("=" * 60)
    print("Classical TSP Result")
    print("=" * 60)
    print(f"Solver    : {result.get('solver', 'Unknown')}")
    print(f"Locations : {result.get('num_locations', '?')}")
    print()
    print("Route:")
    route_names = result.get("route_names", [])
    print("  " + " -> ".join(route_names))
    print()
    print(f"Total Cost : {result.get('route_cost', 0):.4f}")
    print(f"Exec Time  : {result.get('execution_time', 0):.6f} seconds")
    print("=" * 60)


def main():
    with open(RESULT_FILE, "r") as f:
        result = json.load(f)

    display_classical_result(result)


if __name__ == "__main__":
    main()
