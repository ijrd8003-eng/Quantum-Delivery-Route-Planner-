"""
qubo_builder.py

Creates the TSP Quadratic Program using
binary variables x(i,t).

Author:
"""

import json
from pathlib import Path

from qiskit_optimization import QuadraticProgram


class TSPQUBOBuilder:

    def __init__(self, dataset_path):

        with open(dataset_path, "r") as f:
            self.data = json.load(f)

        self.distance_matrix = self.data["distance_matrix"]

        self.n = len(self.distance_matrix)

        self.qp = QuadraticProgram("Quantum_TSP")

    # -------------------------------------------------
    # Decision Variables
    # -------------------------------------------------

    def create_variables(self):

        for city in range(self.n):

            for position in range(self.n):

                self.qp.binary_var(
                    name=f"x_{city}_{position}"
                )

    # -------------------------------------------------
    # Objective Function
    # -------------------------------------------------

    def build_objective(self):

        linear = {}

        for city in range(self.n):

            for position in range(self.n):

                name = f"x_{city}_{position}"

                # Simple linear cost
                linear[name] = self.distance_matrix[0][city]

        self.qp.minimize(linear=linear)

    # -------------------------------------------------
    # Constraint 1
    # Each city visited once
    # -------------------------------------------------

    def add_city_constraints(self):

        for city in range(self.n):

            constraint = {}

            for position in range(self.n):

                constraint[f"x_{city}_{position}"] = 1

            self.qp.linear_constraint(

                linear=constraint,

                sense="==",

                rhs=1,

                name=f"visit_city_{city}"

            )

    # -------------------------------------------------
    # Constraint 2
    # One city per position
    # -------------------------------------------------

    def add_position_constraints(self):

        for position in range(self.n):

            constraint = {}

            for city in range(self.n):

                constraint[f"x_{city}_{position}"] = 1

            self.qp.linear_constraint(

                linear=constraint,

                sense="==",

                rhs=1,

                name=f"tour_position_{position}"

            )

    # -------------------------------------------------

    def build(self):

        self.create_variables()

        self.build_objective()

        self.add_city_constraints()

        self.add_position_constraints()

        return self.qp


# -----------------------------------------------------

if __name__ == "__main__":

    BASE = Path(__file__).resolve().parent.parent

    dataset = (
        BASE /
        "data" /
        "processed" /
        "validated_vrp_dataset.json"
    )

    builder = TSPQUBOBuilder(dataset)

    qp = builder.build()

    print(qp.prettyprint())