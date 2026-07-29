"""
decoder.py

Decodes the measurement counts produced by the simulator
or IBM Quantum hardware into a binary solution vector
and reconstructs the physical delivery route.

The QAOA uses x(city, position) binary encoding.
For n locations, the bitstring has n*n bits.
x[city][position] = 1 means city is visited at step position.

Author:
"""

import json
import math
from pathlib import Path

import pandas as pd

# -------------------------------------------------------
# Paths
# -------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

COUNTS_FILE = (
    BASE_DIR / "results" / "simulator" / "counts.json"
)

LOCATIONS_FILE = (
    BASE_DIR / "data" / "raw" / "delivery_locations.csv"
)

OUTPUT_FILE = (
    BASE_DIR / "results" / "simulator" / "decoded_solution.json"
)


# -------------------------------------------------------
# Load Data
# -------------------------------------------------------

def load_counts(path: Path) -> dict:
    with open(path, "r") as f:
        return json.load(f)


def load_location_names(path: Path) -> list:
    df = pd.read_csv(path)
    return df["name"].tolist()


# -------------------------------------------------------
# Best Bitstring
# -------------------------------------------------------

def get_best_bitstring(counts: dict) -> str:
    return max(counts, key=counts.get)


# -------------------------------------------------------
# TSP Bitstring Decoder
# -------------------------------------------------------

def decode_tsp_bitstring(bitstring: str, n: int) -> list:
    """
    Decodes a TSP bitstring with n*n bits.
    x[city][position] = bitstring[city * n + position]

    Returns the route as a list of city indices (0..n-1).
    """
    if len(bitstring) != n * n:
        return list(range(n))  # Fallback: identity order

    route_order = []
    for pos in range(n):
        for city in range(n):
            idx = city * n + pos
            if idx < len(bitstring) and bitstring[idx] == "1":
                route_order.append(city)
                break

    # Fill missing cities
    visited = set(route_order)
    for city in range(n):
        if city not in visited:
            route_order.append(city)

    return route_order


# -------------------------------------------------------
# General Bitstring Decoder (any length)
# -------------------------------------------------------

def decode_bitstring_general(bitstring: str, n: int) -> list:
    """
    Fallback: decode n-bit bitstring to selected node indices.
    """
    selected = [i for i, bit in enumerate(bitstring) if bit == "1"]
    return selected[:n]


# -------------------------------------------------------
# Reconstruct Route
# -------------------------------------------------------

def reconstruct_route(city_order: list, location_names: list) -> list:
    """
    Maps a list of city indices to location names.
    Wraps with depot at start and end.
    """
    depot_name = location_names[0] if location_names else "Depot"
    route = [depot_name]

    for city_idx in city_order:
        if city_idx < len(location_names):
            name = location_names[city_idx]
            if name != depot_name:
                route.append(name)

    route.append(depot_name)
    return route


# -------------------------------------------------------
# Main
# -------------------------------------------------------

def main():
    # Load data
    counts = load_counts(COUNTS_FILE)
    location_names = load_location_names(LOCATIONS_FILE)
    n = len(location_names)

    # Best bitstring
    best_bitstring = get_best_bitstring(counts)
    best_count = counts[best_bitstring]
    total_shots = sum(counts.values())

    print("=" * 60)
    print("Quantum Bitstring Decoder")
    print("=" * 60)
    print(f"\nLocations        : {n}")
    print(f"Bitstring Length : {len(best_bitstring)}")
    print(f"Best Bitstring   : {best_bitstring}")
    print(f"Count            : {best_count} / {total_shots}")

    # Decode
    expected_bits = n * n
    if len(best_bitstring) == expected_bits:
        city_order = decode_tsp_bitstring(best_bitstring, n)
        decode_method = "TSP x(city,position)"
    else:
        city_order = decode_bitstring_general(best_bitstring, n - 1)
        # Add depot (0) at front if not present
        if 0 not in city_order:
            city_order = [0] + city_order
        decode_method = "General (index-based)"

    # Reconstruct route
    route = reconstruct_route(city_order, location_names)

    print(f"\nDecode Method    : {decode_method}")
    print(f"City Order       : {city_order}")
    print(f"\nDecoded Route:")
    print("  " + " -> ".join(route))

    # Save
    result = {
        "best_bitstring": best_bitstring,
        "count": best_count,
        "total_shots": total_shots,
        "best_probability": round(best_count / total_shots, 6),
        "decode_method": decode_method,
        "city_order": city_order,
        "decoded_route": route,
        "num_locations": n
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(result, f, indent=4)

    print(f"\nSaved: {OUTPUT_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()