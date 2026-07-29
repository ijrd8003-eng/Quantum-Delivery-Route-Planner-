"""
cost_function.py

Computes the objective value (total route distance)
for a given delivery route.
"""

import json
from pathlib import Path

# --------------------------------------------------
# Project Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_FILE = (
    BASE_DIR /
    "data" /
    "processed" /
    "validated_vrp_dataset.json"
)

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

def load_dataset():

    with open(DATASET_FILE, "r") as file:
        return json.load(file)

# --------------------------------------------------
# Compute Route Distance
# --------------------------------------------------

def calculate_route_distance(route, distance_matrix):
    """
    Parameters
    ----------
    route : list
        Example:
        [0, 2, 4, 1, 3, 0]

    distance_matrix : list

    Returns
    -------
    float
        Total route distance
    """

    total_distance = 0

    for i in range(len(route) - 1):

        start = route[i]
        end = route[i + 1]

        total_distance += distance_matrix[start][end]

    return round(total_distance, 2)

# --------------------------------------------------
# Example
# --------------------------------------------------

if __name__ == "__main__":

    dataset = load_dataset()

    distance_matrix = dataset["distance_matrix"]

    # Example Route
    example_route = [0, 1, 2, 3, 4, 5, 0]

    cost = calculate_route_distance(
        example_route,
        distance_matrix
    )

    print("=" * 50)
    print("Route :", example_route)
    print("Total Distance :", cost)
    print("=" * 50)