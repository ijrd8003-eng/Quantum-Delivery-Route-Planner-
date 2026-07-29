"""
tsp_solver.py

Solves the Traveling Salesperson Problem using
Google OR-Tools routing model and fallback
Dynamic Programming (Held-Karp algorithm).

Reads:
    data/processed/distance_matrix.csv

Saves:
    results/classical/classical_result.json

Author:
"""

import json
import math
import time
from itertools import permutations
from pathlib import Path

import pandas as pd

# -------------------------------------------------------
# Paths
# -------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MATRIX_FILE = (
    BASE_DIR / "data" / "processed" / "distance_matrix.csv"
)

LOCATIONS_FILE = (
    BASE_DIR / "data" / "raw" / "delivery_locations.csv"
)

CLASSICAL_DIR = BASE_DIR / "results" / "classical"
CLASSICAL_DIR.mkdir(parents=True, exist_ok=True)

COMPARISON_DIR = BASE_DIR / "results" / "comparison"
COMPARISON_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = CLASSICAL_DIR / "classical_result.json"
COMPARISON_FILE = COMPARISON_DIR / "classical_results.json"


# -------------------------------------------------------
# Load Data
# -------------------------------------------------------

def load_distance_matrix(path: Path) -> list[list[float]]:
    df = pd.read_csv(path, index_col=0)
    return df.values.tolist()


def load_location_names(path: Path) -> dict:
    df = pd.read_csv(path)
    return {
        int(row["location_id"]): row["name"]
        for _, row in df.iterrows()
    }


# -------------------------------------------------------
# Brute Force TSP (for small n)
# -------------------------------------------------------

def brute_force_tsp(matrix: list[list[float]]) -> tuple:
    """
    Solves TSP via brute force for n <= 8.
    Returns (best_route, best_cost)
    """
    n = len(matrix)
    nodes = list(range(1, n))  # All nodes except depot (0)

    best_cost = float("inf")
    best_order = None

    for perm in permutations(nodes):
        route = [0] + list(perm) + [0]
        cost = sum(
            matrix[route[i]][route[i + 1]]
            for i in range(len(route) - 1)
        )
        if cost < best_cost:
            best_cost = cost
            best_order = route

    return best_order, best_cost


# -------------------------------------------------------
# Dynamic Programming TSP (Held-Karp)
# -------------------------------------------------------

def held_karp_tsp(matrix: list[list[float]]) -> tuple:
    """
    Exact TSP via Held-Karp DP algorithm.
    Returns (best_route, best_cost)
    """
    n = len(matrix)
    INF = float("inf")

    # dp[S][i] = min cost to visit all nodes in S, ending at i
    # S is a bitmask
    dp = [[INF] * n for _ in range(1 << n)]
    parent = [[-1] * n for _ in range(1 << n)]

    dp[1][0] = 0  # Start at depot (node 0)

    for S in range(1 << n):
        for u in range(n):
            if dp[S][u] == INF:
                continue
            if not (S >> u & 1):
                continue
            for v in range(n):
                if S >> v & 1:
                    continue
                nS = S | (1 << v)
                new_cost = dp[S][u] + matrix[u][v]
                if new_cost < dp[nS][v]:
                    dp[nS][v] = new_cost
                    parent[nS][v] = u

    full_mask = (1 << n) - 1
    best_cost = INF
    last = -1

    for u in range(1, n):
        cost = dp[full_mask][u] + matrix[u][0]
        if cost < best_cost:
            best_cost = cost
            last = u

    # Reconstruct route
    route = []
    S = full_mask
    u = last

    while u != -1:
        route.append(u)
        prev = parent[S][u]
        S = S ^ (1 << u)
        u = prev

    route.reverse()
    route.append(0)  # Return to depot

    return route, best_cost


# -------------------------------------------------------
# OR-Tools TSP Solver
# -------------------------------------------------------

def ortools_tsp(matrix: list[list[float]]) -> tuple:
    """
    Uses Google OR-Tools to solve TSP.
    Returns (best_route, best_cost)
    """
    try:
        from ortools.constraint_solver import (
            routing_enums_pb2,
            pywrapcp
        )

        n = len(matrix)

        # Convert float to int (OR-Tools requires int)
        int_matrix = [
            [int(matrix[i][j] * 1000) for j in range(n)]
            for i in range(n)
        ]

        manager = pywrapcp.RoutingIndexManager(n, 1, 0)
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return int_matrix[from_node][to_node]

        transit_idx = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_idx)

        search_params = pywrapcp.DefaultRoutingSearchParameters()
        search_params.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        )
        search_params.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        )
        search_params.time_limit.seconds = 10

        solution = routing.SolveWithParameters(search_params)

        if solution:
            route = []
            index = routing.Start(0)
            while not routing.IsEnd(index):
                route.append(manager.IndexToNode(index))
                index = solution.Value(routing.NextVar(index))
            route.append(0)

            cost = sum(
                matrix[route[i]][route[i + 1]]
                for i in range(len(route) - 1)
            )
            return route, cost

    except ImportError:
        pass
    except Exception as e:
        print(f"  OR-Tools failed: {e}")

    return None, None


# -------------------------------------------------------
# Main Solver
# -------------------------------------------------------

def solve_tsp(matrix: list[list[float]]) -> dict:
    """
    Solves TSP with best available method.
    Returns dict with route, cost, time, method.
    """
    n = len(matrix)
    print(f"\nSolving TSP for {n} locations...")

    # Try OR-Tools first
    print("  Trying OR-Tools...")
    start = time.time()
    route, cost = ortools_tsp(matrix)
    elapsed = time.time() - start

    if route is not None:
        print(f"  OR-Tools solved in {elapsed:.4f}s | Cost: {cost:.2f}")
        return {
            "method": "OR-Tools",
            "route": route,
            "route_cost": round(cost, 4),
            "execution_time": round(elapsed, 6)
        }

    # Fallback to Held-Karp DP
    print("  Trying Held-Karp DP...")
    start = time.time()
    route, cost = held_karp_tsp(matrix)
    elapsed = time.time() - start
    print(f"  Held-Karp solved in {elapsed:.4f}s | Cost: {cost:.2f}")

    return {
        "method": "Held-Karp DP",
        "route": route,
        "route_cost": round(cost, 4),
        "execution_time": round(elapsed, 6)
    }


# -------------------------------------------------------
# Main
# -------------------------------------------------------

def main():
    print("=" * 60)
    print("Classical TSP Solver")
    print("=" * 60)

    # Load data
    matrix = load_distance_matrix(MATRIX_FILE)
    name_map = load_location_names(LOCATIONS_FILE)

    n = len(matrix)
    print(f"\nLocations : {n}")
    print(f"Nodes     : {list(name_map.values())}")

    # Solve
    result = solve_tsp(matrix)

    # Map route indices to names
    route_names = [name_map.get(i, f"Node_{i}") for i in result["route"]]

    print(f"\nMethod    : {result['method']}")
    print(f"Route     : {' -> '.join(route_names)}")
    print(f"Cost      : {result['route_cost']:.4f}")
    print(f"Time      : {result['execution_time']:.6f}s")

    # Build output
    output = {
        "solver": result["method"],
        "num_locations": n,
        "route_indices": result["route"],
        "route_names": route_names,
        "route_cost": result["route_cost"],
        "execution_time": result["execution_time"]
    }

    # Save
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=4)

    with open(COMPARISON_FILE, "w") as f:
        json.dump(output, f, indent=4)

    print(f"\nSaved to: {OUTPUT_FILE}")
    print("=" * 60)

    return output


if __name__ == "__main__":
    main()
