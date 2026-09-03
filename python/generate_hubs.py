import pandas as pd
import random

# Make results reproducible
random.seed(42)

# Hub master data
hubs = [
    ["HUB001", "Bangalore Central Hub", "Bangalore", "Karnataka", "Regional", 2500, "06:00", "22:00"],
    ["HUB002", "Bangalore North Hub", "Bangalore", "Karnataka", "City", 1800, "06:00", "22:00"],
    ["HUB003", "Chennai Central Hub", "Chennai", "Tamil Nadu", "Regional", 2400, "06:00", "22:00"],
    ["HUB004", "Chennai South Hub", "Chennai", "Tamil Nadu", "City", 1600, "06:00", "22:00"],
    ["HUB005", "Hyderabad Central Hub", "Hyderabad", "Telangana", "Regional", 2300, "06:00", "22:00"],
    ["HUB006", "Mumbai Central Hub", "Mumbai", "Maharashtra", "Regional", 3000, "05:00", "23:00"],
    ["HUB007", "Mumbai North Hub", "Mumbai", "Maharashtra", "City", 1900, "06:00", "22:00"],
    ["HUB008", "Pune Central Hub", "Pune", "Maharashtra", "Regional", 2200, "06:00", "22:00"],
    ["HUB009", "Delhi Central Hub", "Delhi", "Delhi", "Regional", 3200, "05:00", "23:00"],
    ["HUB010", "Delhi South Hub", "Delhi", "Delhi", "City", 2000, "06:00", "22:00"],
    ["HUB011", "Kolkata Central Hub", "Kolkata", "West Bengal", "Regional", 2100, "06:00", "22:00"],
    ["HUB012", "Ahmedabad Central Hub", "Ahmedabad", "Gujarat", "Regional", 2000, "06:00", "22:00"],
    ["HUB013", "Coimbatore Hub", "Coimbatore", "Tamil Nadu", "City", 1400, "06:00", "21:00"],
    ["HUB014", "Kochi Central Hub", "Kochi", "Kerala", "Regional", 1700, "06:00", "22:00"],
    ["HUB015", "Mysore Hub", "Mysore", "Karnataka", "City", 1200, "07:00", "21:00"],
    ["HUB016", "Jaipur Central Hub", "Jaipur", "Rajasthan", "Regional", 1800, "06:00", "22:00"],
    ["HUB017", "Lucknow Central Hub", "Lucknow", "Uttar Pradesh", "Regional", 1900, "06:00", "22:00"],
    ["HUB018", "Surat Hub", "Surat", "Gujarat", "City", 1500, "06:00", "21:00"],
    ["HUB019", "Nagpur Hub", "Nagpur", "Maharashtra", "Regional", 1600, "06:00", "21:00"],
    ["HUB020", "Indore Hub", "Indore", "Madhya Pradesh", "Regional", 1500, "06:00", "21:00"]
]

# Column names
columns = [
    "hub_id",
    "hub_name",
    "city",
    "state",
    "hub_type",
    "capacity_per_day",
    "operating_start_time",
    "operating_end_time"
]

# Create DataFrame
hubs_df = pd.DataFrame(hubs, columns=columns)

# Display information
print("Hubs dataset created successfully!")
print("Shape:", hubs_df.shape)

print("\nFirst 5 records:")
print(hubs_df.head())

print("\nHub types:")
print(hubs_df["hub_type"].value_counts())

print("\nTotal daily capacity:")
print(hubs_df["capacity_per_day"].sum())

# Save dataset
hubs_df.to_csv(
    "../data/raw/hubs.csv",
    index=False
)

print("\nSaved to: data/raw/hubs.csv")
