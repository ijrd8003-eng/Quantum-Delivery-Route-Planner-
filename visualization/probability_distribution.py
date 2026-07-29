"""
probability_distribution.py

Plots the probability distribution of
the measured QAOA bitstrings.

Input:
    results/simulator/counts.json

Output:
    results/figures/probability_distribution.png

Author:
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt

# -------------------------------------------------------
# Paths
# -------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

COUNTS_FILE = (
    BASE_DIR
    / "results"
    / "simulator"
    / "counts.json"
)

OUTPUT_DIR = (
    BASE_DIR
    / "results"
    / "figures"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = (
    OUTPUT_DIR
    / "probability_distribution.png"
)

# -------------------------------------------------------
# Load Counts
# -------------------------------------------------------

with open(COUNTS_FILE, "r") as file:
    counts = json.load(file)

# -------------------------------------------------------
# Compute Probabilities
# -------------------------------------------------------

total_shots = sum(counts.values())

probabilities = {
    bitstring: count / total_shots
    for bitstring, count in counts.items()
}

# -------------------------------------------------------
# Top N Solutions
# -------------------------------------------------------

TOP_N = 15

top = sorted(
    probabilities.items(),
    key=lambda x: x[1],
    reverse=True
)[:TOP_N]

labels = [item[0] for item in top]
values = [item[1] for item in top]

# -------------------------------------------------------
# Plot
# -------------------------------------------------------

plt.figure(figsize=(14, 6))

plt.bar(range(len(labels)), values)

plt.xticks(
    range(len(labels)),
    labels,
    rotation=90,
    fontsize=8
)

plt.ylabel("Probability")
plt.xlabel("Measured Bitstring")

plt.title("QAOA Measurement Probability Distribution")

plt.tight_layout()

plt.savefig(
    OUTPUT_FILE,
    dpi=300
)

plt.show()

# -------------------------------------------------------
# Console Output
# -------------------------------------------------------

print("=" * 60)
print("Probability Distribution")
print("=" * 60)

for bitstring, probability in top:
    print(f"{bitstring} : {probability:.6f}")

print("\nSaved Figure:")
print(OUTPUT_FILE)