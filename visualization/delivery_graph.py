"""
delivery_graph.py

Visualize the delivery network generated for
the Quantum Delivery Route Planner.

Author:
"""

from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "delivery_locations.csv"
)

OUTPUT_DIR = (
    BASE_DIR
    / "results"
    / "visualization"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------
# Load Dataset
# ---------------------------------------------------------

locations = pd.read_csv(DATA_FILE)

print("\nDataset Loaded Successfully\n")
print(locations.head())

# ---------------------------------------------------------
# Build Graph
# ---------------------------------------------------------

G = nx.Graph()

positions = {}

for _, row in locations.iterrows():

    node = int(row["location_id"])

    G.add_node(
        node,
        name=row["name"],
        node_type=row["type"]
    )

    positions[node] = (
        row["x"],
        row["y"]
    )

# ---------------------------------------------------------
# Create Complete Graph
# ---------------------------------------------------------

nodes = list(G.nodes())

for i in range(len(nodes)):
    for j in range(i + 1, len(nodes)):
        G.add_edge(nodes[i], nodes[j])

# ---------------------------------------------------------
# Separate Depot and Customers
# ---------------------------------------------------------

depot_nodes = [
    n for n, d in G.nodes(data=True)
    if d["node_type"] == "Depot"
]

customer_nodes = [
    n for n, d in G.nodes(data=True)
    if d["node_type"] == "Customer"
]

# ---------------------------------------------------------
# Labels
# ---------------------------------------------------------

labels = {}

for node, data in G.nodes(data=True):

    labels[node] = data["name"]

# ---------------------------------------------------------
# Draw Graph
# ---------------------------------------------------------

plt.figure(figsize=(10, 8))

nx.draw_networkx_edges(
    G,
    positions,
    alpha=0.25,
    width=1
)

nx.draw_networkx_nodes(
    G,
    positions,
    nodelist=customer_nodes,
    node_size=450,
    label="Customers"
)

nx.draw_networkx_nodes(
    G,
    positions,
    nodelist=depot_nodes,
    node_size=800,
    label="Depot"
)

nx.draw_networkx_labels(
    G,
    positions,
    labels,
    font_size=8
)

plt.title("Delivery Network")

plt.xlabel("X Coordinate")

plt.ylabel("Y Coordinate")

plt.grid(True)

plt.legend()

plt.tight_layout()

# ---------------------------------------------------------
# Save Figure
# ---------------------------------------------------------

output = OUTPUT_DIR / "delivery_network.png"

plt.savefig(
    output,
    dpi=300,
    bbox_inches="tight"
)

print("\nFigure saved to:")
print(output)

plt.show()