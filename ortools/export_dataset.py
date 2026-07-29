"""
export_dataset.py

Loads the VRP dataset, validates it, and exports the
final dataset for the optimization module.
"""

import json
from pathlib import Path

# Import validation function
from constraints import validate_dataset

# -------------------------------------------------------
# Project Paths
# -------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "processed" / "vrp_dataset.json"

OUTPUT_FILE = BASE_DIR / "data" / "processed" / "validated_vrp_dataset.json"

# -------------------------------------------------------
# Load Dataset
# -------------------------------------------------------

with open(INPUT_FILE, "r") as file:
    dataset = json.load(file)

# -------------------------------------------------------
# Validate Dataset
# -------------------------------------------------------

validate_dataset(dataset)

# -------------------------------------------------------
# Dataset Summary
# -------------------------------------------------------

num_locations = len(dataset["distance_matrix"])
num_customers = len(dataset["demands"]) - 1
num_vehicles = dataset["num_vehicles"]

total_demand = sum(dataset["demands"])

vehicle_capacity = sum(dataset["vehicle_capacities"])

print("\n========== DATASET SUMMARY ==========")

print(f"Locations          : {num_locations}")
print(f"Customers          : {num_customers}")
print(f"Vehicles           : {num_vehicles}")
print(f"Total Demand       : {total_demand}")
print(f"Total Capacity     : {vehicle_capacity}")
print(f"Depot              : {dataset['depot']}")

print("=====================================\n")

# -------------------------------------------------------
# Save Validated Dataset
# -------------------------------------------------------

with open(OUTPUT_FILE, "w") as file:

    json.dump(
        dataset,
        file,
        indent=4
    )

print("Validated dataset exported successfully.")

print(f"Saved to:\n{OUTPUT_FILE}")