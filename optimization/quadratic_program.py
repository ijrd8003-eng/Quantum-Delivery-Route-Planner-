"""
quadratic_program.py

Builds a Quadratic Program for a small
delivery route optimisation problem.
"""

import json
from pathlib import Path

from qiskit_optimization import QuadraticProgram

# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET = (
    BASE_DIR
    / "data"
    / "processed"
    / "validated_vrp_dataset.json"
)

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

with open(DATASET, "r") as file:
    data = json.load(file)

distance_matrix = data["distance_matrix"]

num_locations = len(distance_matrix)

# --------------------------------------------------
# Create Quadratic Program
# --------------------------------------------------

qp = QuadraticProgram("Delivery_Route_Planner")

# --------------------------------------------------
# Binary Variables
# --------------------------------------------------
# x_i = 1 if location i is selected

for i in range(num_locations):

    qp.binary_var(name=f"x_{i}")

# --------------------------------------------------
# Objective Function
# --------------------------------------------------

linear = {}

for i in range(num_locations):

    linear[f"x_{i}"] = distance_matrix[0][i]

qp.minimize(linear=linear)

# --------------------------------------------------
# Constraint
# --------------------------------------------------
# Depot must always be selected

qp.linear_constraint(
    linear={"x_0": 1},
    sense="==",
    rhs=1,
    name="Depot"
)

# --------------------------------------------------
# Print Model
# --------------------------------------------------

print(qp.prettyprint())