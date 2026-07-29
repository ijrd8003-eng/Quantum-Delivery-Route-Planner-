"""
ansatz.py

Builds the QAOA Ansatz circuit for the
Delivery Route Planner.

This module is shared by:
    - qaoa.py
    - simulator.py
    - hardware.py

Author:
"""

from qiskit.circuit.library import QAOAAnsatz


class QAOABuilder:
    """
    Builds a parameterized QAOA circuit.
    """

    def __init__(self, operator, reps=2):

        self.operator = operator
        self.reps = reps

    # ---------------------------------------------------------
    # Build Parameterized Circuit
    # ---------------------------------------------------------

    def build(self):

        circuit = QAOAAnsatz(
            cost_operator=self.operator,
            reps=self.reps
        )

        return circuit

    # ---------------------------------------------------------
    # Assign Optimized Parameters
    # ---------------------------------------------------------

    def assign_parameters(self, parameters):

        circuit = self.build()

        circuit = circuit.assign_parameters(parameters)

        return circuit

    # ---------------------------------------------------------
    # Build Measured Circuit
    # ---------------------------------------------------------

    def measured_circuit(self, parameters):

        circuit = self.assign_parameters(parameters)

        circuit.measure_all()

        return circuit