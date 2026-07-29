
from pathlib import Path
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA = BASE_DIR / "data" / "raw" / "delivery_locations.csv"

locations = pd.read_csv(RAW_DATA)

coordinates = locations[["x", "y"]].values

distance_matrix = cdist(coordinates, coordinates, metric="euclidean")

distance_df = pd.DataFrame(
    distance_matrix,
    index=locations["location_id"],
    columns=locations["location_id"]
)

OUTPUT = BASE_DIR / "data" / "processed" / "distance_matrix.csv"

distance_df.to_csv(OUTPUT)

print("Distance matrix generated successfully.")