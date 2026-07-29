import json
from pathlib import Path

import pandas as pd

# -------------------------------------------------------
# Project Paths
# -------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# -------------------------------------------------------
# Load CSV Files
# -------------------------------------------------------

locations = pd.read_csv(RAW_DIR / "delivery_locations.csv")

vehicles = pd.read_csv(RAW_DIR / "vehicles.csv")

demands = pd.read_csv(RAW_DIR / "customer_demands.csv")

distance_matrix = pd.read_csv(
    PROCESSED_DIR / "distance_matrix.csv",
    index_col=0
)

# -------------------------------------------------------
# Convert to Python Lists
# -------------------------------------------------------

distance_matrix = distance_matrix.values.tolist()

customer_demands = [0]

customer_demands.extend(
    demands["packages"].tolist()
)

vehicle_capacities = vehicles[
    "capacity_packages"
].tolist()

num_vehicles = len(vehicle_capacities)

depot = 0

# -------------------------------------------------------
# Build Data Model
# -------------------------------------------------------

vrp_data = {

    "distance_matrix": distance_matrix,

    "demands": customer_demands,

    "vehicle_capacities": vehicle_capacities,

    "num_vehicles": num_vehicles,

    "depot": depot
}

# -------------------------------------------------------
# Save JSON
# -------------------------------------------------------

output_file = PROCESSED_DIR / "vrp_dataset.json"

with open(output_file, "w") as file:

    json.dump(
        vrp_data,
        file,
        indent=4
    )

print("VRP Dataset Created Successfully")
print(f"Saved to: {output_file}")