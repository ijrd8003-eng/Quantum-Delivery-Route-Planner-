"""
circuit_builder.py

Builds the QAOA quantum circuit using
the optimised QAOA parameters.

This module is shared by

• simulator.py
• hardware.py

Author:
"""

import pickle
from pathlib import Path

from qiskit.circuit.library import QAOAAnsatz

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

QAOA_RESULT = (
    BASE_DIR
    / "results"
    / "simulator"
    / "qaoa_result.pkl"
)

# ---------------------------------------------------------
# Build Circuit
# ---------------------------------------------------------

def build_qaoa_circuit(measure=True):
    """
    Builds the optimised QAOA circuit.

    Parameters
    ----------
    measure : bool
        Add measurements to the circuit.

    Returns
    -------
    QuantumCircuit
    """

    # ---------------------------------------------
    # Load optimisation result
    # ---------------------------------------------

    with open(QAOA_RESULT, "rb") as file:

        data = pickle.load(file)

    operator = data["operator"]

    parameters = data["optimal_point"]

    reps = data["reps"]

    # ---------------------------------------------
    # Create Ansatz
    # ---------------------------------------------

    ansatz = QAOAAnsatz(

        cost_operator=operator,

        reps=reps

    )

    # ---------------------------------------------
    # Bind parameters
    # ---------------------------------------------

    circuit = ansatz.assign_parameters(parameters)

    # ---------------------------------------------
    # Add measurements
    # ---------------------------------------------

    if measure:

        circuit.measure_all()

    return circuit


# ---------------------------------------------------------
# Standalone Test
# ---------------------------------------------------------

if __name__ == "__main__":

    qc = build_qaoa_circuit()

    print("=" * 60)
    print("QAOA Circuit")
    print("=" * 60)

    print(qc)

    print()

    print("Number of Qubits :", qc.num_qubits)
    print("Circuit Depth    :", qc.depth())
    print("Gate Count       :", qc.size())