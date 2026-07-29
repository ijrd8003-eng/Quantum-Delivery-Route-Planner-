# """
# ising_converter.py

# Converts the Quadratic Program into an
# Ising Hamiltonian that can be solved
# using QAOA.
# """

# from pathlib import Path
# import sys

# # ----------------------------------------------------
# # Allow importing from optimisation folder
# # ----------------------------------------------------

# BASE_DIR = Path(__file__).resolve().parent.parent
# sys.path.append(str(BASE_DIR))

# # ----------------------------------------------------
# # Imports
# # ----------------------------------------------------

# from optimization.quadratic_program import qp
# from qiskit_optimization.converters import QuadraticProgramToQubo
# # ----------------------------------------------------
# # Convert to Ising
# # ----------------------------------------------------
# converter = QuadraticProgramToQubo()
# qubo = converter.convert(qp)
# operator, offset = qubo.to_ising()
# #operator, offset = converter.convert(qp)

# # ----------------------------------------------------
# # Display Results
# # ----------------------------------------------------

# print("=" * 60)
# print("Ising Hamiltonian")
# print("=" * 60)

# print(operator)

# print("\nOffset:")
# print(offset)

# print("=" * 60)

"""
ising_converter.py

Converts a QUBO formulation into an
Ising Hamiltonian that can be solved
using QAOA.

Author:
"""

from pathlib import Path
import sys
import pickle

# -------------------------------------------------------
# Project Path
# -------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# -------------------------------------------------------
# Import QUBO Builder
# -------------------------------------------------------

from optimization.qubo_builder import TSPQUBOBuilder
from qiskit_optimization.converters import QuadraticProgramToQubo

# -------------------------------------------------------
# Dataset
# -------------------------------------------------------

DATASET = (
    BASE_DIR /
    "data" /
    "processed" /
    "validated_vrp_dataset.json"
)

# -------------------------------------------------------
# Build Quadratic Program
# -------------------------------------------------------

builder = TSPQUBOBuilder(DATASET)

qp = builder.build()

# -------------------------------------------------------
# Convert to QUBO
# -------------------------------------------------------

converter = QuadraticProgramToQubo()

qubo = converter.convert(qp)

# -------------------------------------------------------
# Convert to Ising
# -------------------------------------------------------

operator, offset = qubo.to_ising()

# -------------------------------------------------------
# Display Information
# -------------------------------------------------------

print("=" * 70)
print("ISING HAMILTONIAN")
print("=" * 70)

print(operator)

print()

print("Offset")

print(offset)

print("=" * 70)

# -------------------------------------------------------
# Save Model
# -------------------------------------------------------

OUTPUT = (
    BASE_DIR /
    "data" /
    "processed" /
    "ising_model.pkl"
)

with open(OUTPUT, "wb") as file:

    pickle.dump(
        {
            "operator": operator,
            "offset": offset
        },
        file
    )

print()

print("Ising model saved successfully.")

print(OUTPUT)