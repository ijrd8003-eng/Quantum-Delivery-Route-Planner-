"""
graph_encoder.py

Builds a weighted delivery graph from the
validated VRP dataset.

Author:
"""

import json
from pathlib import Path

import networkx as nx

# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET = (
    BASE_DIR /
    "data" /
    "processed" /
    "validated_vrp_dataset.json"
)

OUTPUT = (
    BASE_DIR /
    "data" /
    "processed" /
    "graph.json"
)

# --------------------------------------------------
# Graph Encoder
# --------------------------------------------------


class GraphEncoder:

    def __init__(self):

        with open(DATASET, "r") as file:

            self.data = json.load(file)

        self.distance_matrix = self.data["distance_matrix"]

        self.demands = self.data["demands"]

        self.vehicle_capacities = self.data["vehicle_capacities"]

        self.depot = self.data["depot"]

        self.num_nodes = len(self.distance_matrix)

        self.graph = nx.Graph()

    # ----------------------------------------------

    def create_nodes(self):

        for node in range(self.num_nodes):

            self.graph.add_node(

                node,

                demand=self.demands[node]

            )

    # ----------------------------------------------

    def create_edges(self):

        for i in range(self.num_nodes):

            for j in range(i + 1, self.num_nodes):

                distance = self.distance_matrix[i][j]

                self.graph.add_edge(

                    i,

                    j,

                    weight=distance

                )

    # ----------------------------------------------

    def adjacency_matrix(self):

        return nx.to_numpy_array(

            self.graph,

            weight="weight"

        ).tolist()

    # ----------------------------------------------

    def edge_list(self):

        edges = []

        for u, v, data in self.graph.edges(data=True):

            edges.append({

                "from": u,

                "to": v,

                "distance": data["weight"]

            })

        return edges

    # ----------------------------------------------

    def export(self):

        graph_data = {

            "num_nodes": self.num_nodes,

            "depot": self.depot,

            "vehicle_capacities": self.vehicle_capacities,

            "nodes": [

                {

                    "id": n,

                    "demand": self.graph.nodes[n]["demand"]

                }

                for n in self.graph.nodes()

            ],

            "edges": self.edge_list(),

            "adjacency_matrix": self.adjacency_matrix()

        }

        with open(OUTPUT, "w") as file:

            json.dump(

                graph_data,

                file,

                indent=4

            )

        print()

        print("=" * 50)

        print("Delivery Graph Created")

        print("=" * 50)

        print(f"Nodes : {self.num_nodes}")

        print(f"Edges : {len(self.graph.edges())}")

        print()

        print("Saved to")

        print(OUTPUT)

        print("=" * 50)

    # ----------------------------------------------

    def build(self):

        self.create_nodes()

        self.create_edges()

        self.export()


# --------------------------------------------------

if __name__ == "__main__":

    encoder = GraphEncoder()

    encoder.build()