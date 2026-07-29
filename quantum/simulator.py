"""
simulator.py

Runs the optimized QAOA circuit on the
Qiskit Aer Simulator and saves the
measurement counts.

Author:
"""

import json
import pickle
from pathlib import Path

from qiskit import transpile
from qiskit.circuit.library import QAOAAnsatz

from qiskit_aer import AerSimulator
from qiskit_aer.primitives import SamplerV2

from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from circuit_builder import build_qaoa_circuit

# --------------------------------------------------------
# Paths
# --------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

QAOA_RESULT = (
    BASE_DIR
    / "results"
    / "simulator"
    / "qaoa_result.pkl"
)

OUTPUT_DIR = (
    BASE_DIR
    / "results"
    / "simulator"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------------
# Load QAOA Result
# --------------------------------------------------------

with open(QAOA_RESULT, "rb") as file:

    result = pickle.load(file)

#operator = result["operator"]

#parameters = result["optimal_point"]

#reps = result["reps"]

# --------------------------------------------------------
# Build QAOA Circuit
# --------------------------------------------------------

#ansatz = QAOAAnsatz(

#    cost_operator=operator,

#    reps=reps

#)

# Assign optimized parameters

#circuit = ansatz.assign_parameters(parameters)

# Add measurements

#circuit.measure_all()
circuit = build_qaoa_circuit()
print()

print("=" * 60)

print("QAOA Circuit")

print("=" * 60)

print(circuit)

# --------------------------------------------------------
# Aer Simulator
# --------------------------------------------------------

backend = AerSimulator()

compiled = transpile(

    circuit,

    backend

)

# --------------------------------------------------------
# Execute
# --------------------------------------------------------
# --------------------------------------------------------
# Sampler V2
# --------------------------------------------------------

pass_manager = generate_preset_pass_manager(
    optimization_level=1,
    backend=backend
)

compiled = pass_manager.run(circuit)

sampler = SamplerV2()

job = sampler.run([compiled])

result_sampler = job.result()

# --------------------------------------------------------
# Extract Counts
# --------------------------------------------------------

counts = {}

try:

    pub_result = result_sampler[0]

    data = pub_result.data

    counts = data.meas.get_counts()

except Exception as e:

    print(e)

# --------------------------------------------------------
# Print
# --------------------------------------------------------

print()

print("=" * 60)

print("Measurement Counts")

print("=" * 60)

print(counts)

# --------------------------------------------------------
# Save
# --------------------------------------------------------

with open(

    OUTPUT_DIR / "counts.json",

    "w"

) as file:

    json.dump(

        counts,

        file,

        indent=4

    )

print()

print("Counts saved.")

print(OUTPUT_DIR / "counts.json")