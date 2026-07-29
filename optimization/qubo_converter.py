"""
qubo_converter.py

Converts a constrained Quadratic Program
into an unconstrained QUBO formulation.

Author:
"""

from pathlib import Path
import sys

from qiskit_optimization.converters import QuadraticProgramToQubo

# -----------------------------------------------------
# Allow importing project modules
# -----------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# -----------------------------------------------------
# Import QUBO Builder
# -----------------------------------------------------

from optimization.qubo_builder import TSPQUBOBuilder

# -----------------------------------------------------
# Load Dataset
# -----------------------------------------------------

DATASET = (
    BASE_DIR
    / "data"
    / "processed"
    / "validated_vrp_dataset.json"
)

# -----------------------------------------------------
# Build Quadratic Program
# -----------------------------------------------------

builder = TSPQUBOBuilder(DATASET)

qp = builder.build()

print("=" * 70)
print("Original Quadratic Program")
print("=" * 70)

print(qp.prettyprint())

# -----------------------------------------------------
# Convert to QUBO
# -----------------------------------------------------

converter = QuadraticProgramToQubo()

qubo = converter.convert(qp)

print()

print("=" * 70)
print("Converted QUBO")
print("=" * 70)

print(qubo.prettyprint())

# -----------------------------------------------------
# Statistics
# -----------------------------------------------------

print()

print("=" * 70)
print("QUBO Statistics")
print("=" * 70)

print(f"Variables : {qubo.get_num_binary_vars()}")

print(f"Constraints : {qubo.get_num_linear_constraints()}")

print("=" * 70)