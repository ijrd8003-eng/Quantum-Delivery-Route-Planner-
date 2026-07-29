"""
constraints.py

Validates the VRP dataset before it is used by
Qiskit Optimization and IBM Quantum.
"""

import json
from pathlib import Path

# -------------------------------------------------------
# Project Paths
# -------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_FILE = BASE_DIR / "data" / "processed" / "vrp_dataset.json"


# -------------------------------------------------------
# Load Dataset
# -------------------------------------------------------

def load_dataset():

    with open(DATASET_FILE, "r") as file:
        return json.load(file)


# -------------------------------------------------------
# Validation Functions
# -------------------------------------------------------

def validate_distance_matrix(matrix):

    rows = len(matrix)

    # Matrix must be square
    for row in matrix:
        if len(row) != rows:
            raise ValueError("Distance matrix is not square.")

    # Diagonal must be zero
    for i in range(rows):
        if matrix[i][i] != 0:
            raise ValueError(
                f"Distance matrix diagonal at [{i},{i}] must be zero."
            )

    # Symmetric check
    for i in range(rows):
        for j in range(rows):
            if abs(matrix[i][j] - matrix[j][i]) > 1e-6:
                raise ValueError(
                    "Distance matrix is not symmetric."
                )


def validate_demands(demands):

    for demand in demands:

        if demand < 0:
            raise ValueError(
                "Customer demand cannot be negative."
            )


def validate_vehicle_capacities(capacities):

    if len(capacities) == 0:
        raise ValueError("No vehicles found.")

    for capacity in capacities:

        if capacity <= 0:
            raise ValueError(
                "Vehicle capacity must be greater than zero."
            )


def validate_depot(depot, matrix):

    if depot < 0:
        raise ValueError("Depot index cannot be negative.")

    if depot >= len(matrix):
        raise ValueError("Depot index is outside the distance matrix.")


def validate_matrix_vs_demands(matrix, demands):

    if len(matrix) != len(demands):
        raise ValueError(
            "Distance matrix size and demand list size do not match."
        )


# -------------------------------------------------------
# Run All Validations
# -------------------------------------------------------

def validate_dataset(dataset):

    validate_distance_matrix(dataset["distance_matrix"])

    validate_demands(dataset["demands"])

    validate_vehicle_capacities(dataset["vehicle_capacities"])

    validate_depot(
        dataset["depot"],
        dataset["distance_matrix"]
    )

    validate_matrix_vs_demands(
        dataset["distance_matrix"],
        dataset["demands"]
    )


# -------------------------------------------------------
# Main
# -------------------------------------------------------

if __name__ == "__main__":

    dataset = load_dataset()

    validate_dataset(dataset)

    print("=" * 50)
    print("VRP Dataset Validation Successful")
    print("=" * 50)