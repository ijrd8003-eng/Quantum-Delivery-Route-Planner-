import os
import random
import pandas as pd

# -----------------------------
# Configuration
# -----------------------------
NUM_CUSTOMERS = 3
NUM_VEHICLES = 2
VEHICLE_CAPACITY = 25
MAP_WIDTH = 100
MAP_HEIGHT = 100
RANDOM_SEED = 42

random.seed(RANDOM_SEED)

RAW_DIR = "data/raw"
os.makedirs(RAW_DIR, exist_ok=True)

# -----------------------------
# Depot
# -----------------------------
depot = {
    "depot_id": 0,
    "name": "Main Warehouse",
    "x": 50,
    "y": 50
}

pd.DataFrame([depot]).to_csv(
    os.path.join(RAW_DIR, "depot.csv"),
    index=False
)

# -----------------------------
# Customer Locations
# -----------------------------
customers = []

for i in range(1, NUM_CUSTOMERS + 1):

    customers.append({
        "customer_id": i,
        "customer_name": f"Customer_{i}",
        "x": random.randint(0, MAP_WIDTH),
        "y": random.randint(0, MAP_HEIGHT)
    })

locations = []

locations.append({
    "location_id": 0,
    "name": depot["name"],
    "type": "Depot",
    "x": depot["x"],
    "y": depot["y"]
})

for customer in customers:

    locations.append({
        "location_id": customer["customer_id"],
        "name": customer["customer_name"],
        "type": "Customer",
        "x": customer["x"],
        "y": customer["y"]
    })

pd.DataFrame(locations).to_csv(
    os.path.join(RAW_DIR, "delivery_locations.csv"),
    index=False
)

# -----------------------------
# Customer Demands
# -----------------------------
demands = []

for customer in customers:

    demands.append({
        "customer_id": customer["customer_id"],
        "packages": random.randint(1,5),
        "weight_kg": round(random.uniform(1.0,10.0),2)
    })

pd.DataFrame(demands).to_csv(
    os.path.join(RAW_DIR, "customer_demands.csv"),
    index=False
)

# -----------------------------
# Vehicles
# -----------------------------
vehicles = []

for i in range(1, NUM_VEHICLES + 1):

    vehicles.append({
        "vehicle_id": i,
        "vehicle_type": "Van",
        "capacity_packages": VEHICLE_CAPACITY,
        "capacity_weight_kg": 100,
        "start_depot": 0,
        "end_depot": 0
    })

pd.DataFrame(vehicles).to_csv(
    os.path.join(RAW_DIR, "vehicles.csv"),
    index=False
)

print("Dataset Generated Successfully")