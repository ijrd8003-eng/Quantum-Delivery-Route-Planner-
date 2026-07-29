"""
problem_encoder.py

Reads raw delivery_locations.csv and builds:
  - Distance matrix (Euclidean)
  - Saves data/processed/distance_matrix.csv
  - Saves data/processed/validated_vrp_dataset.json

Author:
"""

import json
import math
from pathlib import Path

import pandas as pd

# -------------------------------------------------------
# Paths
# -------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

LOCATIONS_FILE = (
    BASE_DIR / "data" / "raw" / "delivery_locations.csv"
)

OUTPUT_MATRIX = (
    BASE_DIR / "data" / "processed" / "distance_matrix.csv"
)

OUTPUT_DATASET = (
    BASE_DIR / "data" / "processed" / "validated_vrp_dataset.json"
)

OUTPUT_MATRIX.parent.mkdir(parents=True, exist_ok=True)


# -------------------------------------------------------
# Load Locations
# -------------------------------------------------------

def load_locations(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    return df


# -------------------------------------------------------
# Euclidean Distance
# -------------------------------------------------------

def euclidean_distance(x1, y1, x2, y2) -> float:
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# -------------------------------------------------------
# Build Distance Matrix
# -------------------------------------------------------

def build_distance_matrix(locations: pd.DataFrame) -> list[list[float]]:
    n = len(locations)
    matrix = [[0.0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i == j:
                matrix[i][j] = 0.0
            else:
                xi, yi = locations.iloc[i]["x"], locations.iloc[i]["y"]
                xj, yj = locations.iloc[j]["x"], locations.iloc[j]["y"]
                matrix[i][j] = euclidean_distance(xi, yi, xj, yj)

    return matrix


# -------------------------------------------------------
# Save Distance Matrix CSV
# -------------------------------------------------------

def save_matrix_csv(matrix: list, location_ids: list, output_path: Path):
    df = pd.DataFrame(
        matrix,
        index=location_ids,
        columns=location_ids
    )
    df.index.name = "location_id"
    df.to_csv(output_path)
    print(f"Distance matrix saved to: {output_path}")


# -------------------------------------------------------
# Save VRP Dataset JSON
# -------------------------------------------------------

def save_vrp_dataset(
    locations: pd.DataFrame,
    matrix: list,
    output_path: Path
):
    demands = [0]  # Depot has zero demand

    for i in range(1, len(locations)):
        demands.append(10)  # Default demand per customer

    dataset = {
        "num_locations": len(locations),
        "num_customers": len(locations) - 1,
        "num_vehicles": 2,
        "depot": 0,
        "vehicle_capacities": [50, 50],
        "demands": demands,
        "distance_matrix": matrix,
        "locations": locations.to_dict(orient="records")
    }

    with open(output_path, "w") as f:
        json.dump(dataset, f, indent=4)

    print(f"VRP dataset saved to: {output_path}")


# -------------------------------------------------------
# Main
# -------------------------------------------------------

def main():
    print("=" * 60)
    print("Problem Encoder")
    print("=" * 60)

    # Load
    locations = load_locations(LOCATIONS_FILE)
    print(f"\nLoaded {len(locations)} locations:")
    print(locations.to_string())

    # Build matrix
    matrix = build_distance_matrix(locations)
    location_ids = list(locations["location_id"])

    # Display
    print("\nDistance Matrix:")
    df_matrix = pd.DataFrame(
        matrix,
        index=location_ids,
        columns=location_ids
    )
    print(df_matrix.round(2).to_string())

    # Save
    save_matrix_csv(matrix, location_ids, OUTPUT_MATRIX)
    save_vrp_dataset(locations, matrix, OUTPUT_DATASET)

    print("\nProblem Encoder Complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
