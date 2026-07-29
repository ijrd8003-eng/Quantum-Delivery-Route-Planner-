"""
result_processor.py

Processes the decoded QAOA solution and computes
statistics for the simulator or IBM Quantum results.

Outputs:
- Route cost
- Measurement probabilities
- Top solutions
- Summary statistics

Author:
"""

import json
from pathlib import Path

import pandas as pd

# -----------------------------------------------------
# Paths
# -----------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

COUNTS_FILE = (
    BASE_DIR
    / "results"
    / "simulator"
    / "counts.json"
)

DECODED_FILE = (
    BASE_DIR
    / "results"
    / "simulator"
    / "decoded_solution.json"
)

DISTANCE_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "distance_matrix.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "results"
    / "simulator"
    / "processed_results.json"
)

# -----------------------------------------------------
# Load files
# -----------------------------------------------------

with open(COUNTS_FILE, "r") as f:
    counts = json.load(f)

with open(DECODED_FILE, "r") as f:
    decoded = json.load(f)

distance_matrix = pd.read_csv(
    DISTANCE_FILE,
    index_col=0
)

# -----------------------------------------------------
# Total shots
# -----------------------------------------------------

total_shots = sum(counts.values())

# -----------------------------------------------------
# Best bitstring
# -----------------------------------------------------

best_bitstring = decoded["best_bitstring"]

best_count = counts[best_bitstring]

best_probability = best_count / total_shots

# -----------------------------------------------------
# Probability Distribution
# -----------------------------------------------------

probabilities = {}

for bitstring, count in counts.items():

    probabilities[bitstring] = round(
        count / total_shots,
        6
    )

# -----------------------------------------------------
# Top 10 solutions
# -----------------------------------------------------

top_solutions = sorted(
    counts.items(),
    key=lambda x: x[1],
    reverse=True
)[:10]

top_results = []

for bitstring, count in top_solutions:

    top_results.append({

        "bitstring": bitstring,

        "count": count,

        "probability": round(
            count / total_shots,
            6
        )

    })

# -----------------------------------------------------
# Route Cost (using location name -> index map)
# -----------------------------------------------------

route = decoded["decoded_route"]

route_cost = None

try:
    # Load location names to build name->index map
    locations_file = (
        BASE_DIR / "data" / "raw" / "delivery_locations.csv"
    )
    locations_df = pd.read_csv(locations_file)
    name_to_idx = {
        row["name"]: int(row["location_id"])
        for _, row in locations_df.iterrows()
    }

    # Map route names to indices (skip unknown names)
    route_indices = [
        name_to_idx[node]
        for node in route
        if node in name_to_idx
    ]

    # Compute cost using distance matrix
    if len(route_indices) >= 2:
        route_cost = 0.0
        for i in range(len(route_indices) - 1):
            a = route_indices[i]
            b = route_indices[i + 1]
            route_cost += float(distance_matrix.iloc[a, b])
        route_cost = round(route_cost, 4)

except Exception as e:
    print(f"[result_processor] Route cost error: {e}")
    route_cost = None

# -----------------------------------------------------
# Statistics
# -----------------------------------------------------

statistics = {

    "total_shots": total_shots,

    "unique_solutions": len(counts),

    "best_probability": round(
        best_probability,
        6
    ),

    "route_cost": route_cost,

    "best_bitstring": best_bitstring

}

# -----------------------------------------------------
# Final Report
# -----------------------------------------------------

report = {

    "statistics": statistics,

    "decoded_route": route,

    "top_solutions": top_results,

    "probabilities": probabilities

}

with open(
    OUTPUT_FILE,
    "w"
) as f:

    json.dump(
        report,
        f,
        indent=4
    )

# -----------------------------------------------------
# Print
# -----------------------------------------------------

print("=" * 60)
print("Quantum Result Summary")
print("=" * 60)

print(f"Total Shots      : {total_shots}")
print(f"Unique Solutions : {len(counts)}")
print(f"Best Probability : {best_probability:.4f}")
print(f"Route Cost       : {route_cost}")

print("\nBest Route")

print(" -> ".join(route))

print("\nTop Solutions")

for i, solution in enumerate(top_results, start=1):

    print(
        f"{i}. "
        f"{solution['bitstring']} | "
        f"Count={solution['count']} | "
        f"P={solution['probability']:.4f}"
    )

print("\nSaved")

print(OUTPUT_FILE)