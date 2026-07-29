"""
route_plot.py

Plots the optimized delivery route obtained
from the decoded QAOA solution.

Input
-----
data/raw/delivery_locations.csv
results/simulator/decoded_solution.json

Output
------
results/simulator/route.png

Author:
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

LOCATION_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "delivery_locations.csv"
)

ROUTE_FILE = (
    BASE_DIR
    / "results"
    / "simulator"
    / "decoded_solution.json"
)

OUTPUT_FILE = (
    BASE_DIR
    / "results"
    / "visualization"
    / "route_qaoa.png"
)
OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

# ---------------------------------------------------------
# Load Data
# ---------------------------------------------------------

locations = pd.read_csv(LOCATION_FILE)

with open(ROUTE_FILE, "r") as f:
    decoded = json.load(f)

route = decoded["decoded_route"]

# ---------------------------------------------------------
# Create lookup table
# ---------------------------------------------------------

location_map = {}

for _, row in locations.iterrows():

    location_map[row["name"]] = (
        row["x"],
        row["y"]
    )

# ---------------------------------------------------------
# Plot Nodes
# ---------------------------------------------------------

plt.figure(figsize=(10, 8))

for _, row in locations.iterrows():

    x = row["x"]
    y = row["y"]
    name = row["name"]

    if row["type"] == "Depot":

        plt.scatter(
            x,
            y,
            s=250,
            color="red",
            marker="s",
            label="Depot"
        )

    else:

        plt.scatter(
            x,
            y,
            s=100,
            color="royalblue"
        )

    plt.text(
        x + 1,
        y + 1,
        name,
        fontsize=9
    )

# ---------------------------------------------------------
# Draw Route
# ---------------------------------------------------------

route_x = []
route_y = []

for node in route:

    if node in location_map:

        x, y = location_map[node]

        route_x.append(x)
        route_y.append(y)

plt.plot(
    route_x,
    route_y,
    linewidth=2.5,
    color="green",
    marker="o",
    label="QAOA Route"
)

# ---------------------------------------------------------
# Style
# ---------------------------------------------------------

plt.title("Optimized Delivery Route (QAOA)")

plt.xlabel("X Coordinate")

plt.ylabel("Y Coordinate")

plt.grid(True)

plt.legend()

plt.tight_layout()

plt.text(
    0.02,
    0.95,
    f"Route Nodes: {len(route)}",
    transform=plt.gca().transAxes
)

# ---------------------------------------------------------
# Save
# ---------------------------------------------------------

plt.savefig(
    OUTPUT_FILE,
    dpi=300
)

print("=" * 60)
print("Optimized Route")
print("=" * 60)

print("Route:")

print(" -> ".join(route))

print("\nSaved:")

print(OUTPUT_FILE)

plt.show()