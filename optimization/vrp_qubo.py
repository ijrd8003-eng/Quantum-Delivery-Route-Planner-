"""
vrp_qubo.py

Creates the QUBO formulation for the
Quantum Delivery Route Planner.

Author : Your Name
"""

import json
from pathlib import Path

from qiskit_optimization import QuadraticProgram


class VRPQuboBuilder:

    def __init__(self, dataset_path):

        with open(dataset_path, "r") as file:
            self.data = json.load(file)

        self.distance_matrix = self.data["distance_matrix"]
        self.demands = self.data["demands"]
        self.vehicle_capacities = self.data["vehicle_capacities"]
        self.num_vehicles = self.data["num_vehicles"]
        self.depot = self.data["depot"]

        self.num_locations = len(self.distance_matrix)

        self.qp = QuadraticProgram(
            "Quantum_Delivery_Route"
        )

    # ------------------------------------------------

    def create_variables(self):
        """
        Binary variable

        x_i = 1

        if customer i is selected.
        """

        for i in range(self.num_locations):

            self.qp.binary_var(name=f"x_{i}")

    # ------------------------------------------------

    def objective_function(self):

        linear = {}

        for i in range(self.num_locations):

            linear[f"x_{i}"] = self.distance_matrix[0][i]

        self.qp.minimize(
            linear=linear
        )

    # ------------------------------------------------

    def depot_constraint(self):

        self.qp.linear_constraint(
            linear={"x_0": 1},
            sense="==",
            rhs=1,
            name="Depot"
        )

    # ------------------------------------------------

    def build(self):

        self.create_variables()

        self.objective_function()

        self.depot_constraint()

        return self.qp


# ----------------------------------------------------

if __name__ == "__main__":

    BASE = Path(__file__).resolve().parent.parent

    dataset = (
        BASE /
        "data" /
        "processed" /
        "validated_vrp_dataset.json"
    )

    builder = VRPQuboBuilder(dataset)

    qp = builder.build()

    print(qp.prettyprint())