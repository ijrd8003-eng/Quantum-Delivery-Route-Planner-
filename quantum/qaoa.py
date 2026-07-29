"""
 qaoa.py

Runs the QAOA algorithm using the
Ising Hamiltonian generated from the
TSP QUBO.

 Author:
 """

import pickle
from pathlib import Path

from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2
from qiskit_algorithms.minimum_eigensolvers import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

# -----------------------------------------------------
 # Paths
 # -----------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

ISING_FILE = (
    BASE_DIR
    / "data"
     / "processed"
     / "ising_model.pkl"
 )

RESULT_DIR = (
    BASE_DIR
    / "results"
     / "simulator"
 )

RESULT_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------
# Load Ising Hamiltonian
# -----------------------------------------------------

with open(ISING_FILE, "rb") as file:

     data = pickle.load(file)

operator = data["operator"]
offset = data["offset"]

# -----------------------------------------------------
# Optimizer
# -----------------------------------------------------

optimizer = COBYLA(
  maxiter=100
)

# -----------------------------------------------------
# Estimator
# -----------------------------------------------------

# Simulator, Transpiler, and Sampler
backend = AerSimulator()
transpiler = generate_preset_pass_manager(1, backend=backend)
sampler = SamplerV2()
 

# -----------------------------------------------------
# Build QAOA
# -----------------------------------------------------

qaoa = QAOA(
    sampler=sampler,
    optimizer=optimizer,
    reps=2,
    transpiler=transpiler
 )

# -----------------------------------------------------
# Solve
# -----------------------------------------------------

print("=" * 60)
print("Running QAOA...")
print("=" * 60)

result = qaoa.compute_minimum_eigenvalue(operator)

# -----------------------------------------------------
 # Print Results
 # -----------------------------------------------------

print("\nOptimal Eigenvalue")
print(result.eigenvalue)

print("\nOptimal Parameters")
print(result.optimal_point)

# -----------------------------------------------------
# Save Results
# -----------------------------------------------------

output = RESULT_DIR / "qaoa_result.pkl"

save_data = {
    "operator": operator,
    "offset": offset,
    "optimal_point": result.optimal_point,
    "eigenvalue": float(result.eigenvalue.real),
    "reps": 2,
    "num_qubits": operator.num_qubits,
    "optimizer": "COBYLA",
    "maxiter": 100,
}

with open(output, "wb") as file:
    pickle.dump(save_data, file)

print("\nResults saved to:")
print(output)