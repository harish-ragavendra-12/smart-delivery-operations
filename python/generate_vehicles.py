import pandas as pd
import random

random.seed(42)

# Number of vehicles
NUM_VEHICLES = 150

vehicle_types = {
    "Bike": (20, 2020, 2025),
    "Van": (500, 2019, 2025),
    "Mini Truck": (1500, 2018, 2025),
    "Truck": (5000, 2017, 2025)
}

vehicle_statuses = [
    "Active",
    "Active",
    "Active",
    "Maintenance",
    "Inactive"
]

# Hub IDs
hub_ids = [f"HUB{i:03d}" for i in range(1, 21)]

vehicles = []

for i in range(1, NUM_VEHICLES + 1):

    vehicle_type = random.choice(list(vehicle_types.keys()))

    capacity, min_year, max_year = vehicle_types[vehicle_type]

    vehicle = {
        "vehicle_id": f"VEH{i:04d}",
        "vehicle_type": vehicle_type,
        "capacity_kg": capacity,
        "registration_year": random.randint(min_year, max_year),
        "hub_id": random.choice(hub_ids),
        "status": random.choice(vehicle_statuses)
    }

    vehicles.append(vehicle)

# Create DataFrame
vehicles_df = pd.DataFrame(vehicles)

print("Vehicles dataset created successfully!")
print("Shape:", vehicles_df.shape)

print("\nFirst 5 records:")
print(vehicles_df.head())

print("\nVehicle types:")
print(vehicles_df["vehicle_type"].value_counts())

print("\nVehicle status:")
print(vehicles_df["status"].value_counts())

print("\nVehicles by hub:")
print(vehicles_df["hub_id"].value_counts().head())

# Save
vehicles_df.to_csv(
    "../data/raw/vehicles.csv",
    index=False
)

print("\nSaved to: data/raw/vehicles.csv")