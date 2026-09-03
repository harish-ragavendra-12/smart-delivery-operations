import pandas as pd
import numpy as np
import random
from datetime import timedelta

# Reproducible results
random.seed(42)
np.random.seed(42)

# Number of orders
NUM_ORDERS = 50000

# Load master data
customers_df = pd.read_csv("../data/raw/customers.csv")
hubs_df = pd.read_csv("../data/raw/hubs.csv")
vehicles_df = pd.read_csv("../data/raw/vehicles.csv")
employees_df = pd.read_csv("../data/raw/employees.csv")

# Possible shipping priorities
shipping_priorities = [
    "Standard",
    "Express",
    "Same Day"
]

# Possible delivery statuses
delivery_statuses = [
    "Delivered",
    "Delayed",
    "Cancelled",
    "Returned"
]

# Create lookup lists
customer_ids = customers_df["customer_id"].tolist()
hub_ids = hubs_df["hub_id"].tolist()

# Group vehicles by hub
vehicles_by_hub = (
    vehicles_df
    .groupby("hub_id")["vehicle_id"]
    .apply(list)
    .to_dict()
)

# Group employees by hub
employees_by_hub = (
    employees_df
    .groupby("hub_id")["employee_id"]
    .apply(list)
    .to_dict()
)

# Destination cities
destination_cities = hubs_df["city"].unique().tolist()

print("Master data loaded successfully!")

print("Customers:", len(customer_ids))
print("Hubs:", len(hub_ids))
print("Vehicles:", len(vehicles_df))
print("Employees:", len(employees_df))


# Generate orders
orders = []

start_date = pd.Timestamp("2025-01-01")
end_date = pd.Timestamp("2026-08-31")

for i in range(1, NUM_ORDERS + 1):

    # Select customer
    customer_id = random.choice(customer_ids)

    # Select origin hub
    origin_hub_id = random.choice(hub_ids)

    # Select destination city
    destination_city = random.choice(destination_cities)

    # Select vehicle and employee from the same hub
    vehicle_id = random.choice(
        vehicles_by_hub[origin_hub_id]
    )

    employee_id = random.choice(
        employees_by_hub[origin_hub_id]
    )

    # Generate order date
    order_date = start_date + pd.Timedelta(
        days=random.randint(0, (end_date - start_date).days),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )

    # Shipping priority
    shipping_priority = random.choices(
        ["Standard", "Express", "Same Day"],
        weights=[70, 25, 5],
        k=1
    )[0]

    # Package weight
    package_weight_kg = round(
        np.random.gamma(shape=2.0, scale=2.5),
        2
    )

    # Keep package weight realistic
    package_weight_kg = min(package_weight_kg, 25)

    # Order value
    order_value = round(
        np.random.lognormal(mean=7.5, sigma=0.7),
        2
    )

    # Generate promised delivery time
    if shipping_priority == "Same Day":
        promised_days = 0
    elif shipping_priority == "Express":
        promised_days = 1
    else:
        promised_days = random.randint(2, 5)

    promised_delivery_date = (
        order_date
        + timedelta(days=promised_days)
    )

    # Generate actual delivery time
    delivery_days = promised_days + random.randint(-1, 3)

    if delivery_days < 0:
        delivery_days = 0

    actual_delivery_date = (
        order_date
        + timedelta(days=delivery_days)
    )

    # Delivery status
    status = random.choices(
        delivery_statuses,
        weights=[75, 15, 6, 4],
        k=1
    )[0]

    # Cancelled / returned orders may not have delivery date
    if status in ["Cancelled", "Returned"]:
        actual_delivery_date = pd.NaT

    order = {
        "order_id": f"ORD{i:06d}",
        "customer_id": customer_id,
        "order_date": order_date,
        "promised_delivery_date": promised_delivery_date,
        "actual_delivery_date": actual_delivery_date,
        "origin_hub_id": origin_hub_id,
        "destination_city": destination_city,
        "vehicle_id": vehicle_id,
        "assigned_employee_id": employee_id,
        "package_weight_kg": package_weight_kg,
        "shipping_priority": shipping_priority,
        "order_value": order_value,
        "delivery_status": status
    }

    orders.append(order)


# Convert to DataFrame
orders_df = pd.DataFrame(orders)

print("\nOrders generated successfully!")
print("Shape:", orders_df.shape)

print("\nFirst 5 orders:")
print(orders_df.head())

print("\nDelivery status:")
print(orders_df["delivery_status"].value_counts())

print("\nShipping priority:")
print(orders_df["shipping_priority"].value_counts())

print("\nTotal order value:")
print(round(orders_df["order_value"].sum(), 2))

# Save orders
orders_df.to_csv(
    "../data/raw/orders.csv",
    index=False
)

print("\nSaved to: data/raw/orders.csv")


print("\n--- Data Validation ---")

# Check duplicate order IDs
print(
    "Duplicate order IDs:",
    orders_df["order_id"].duplicated().sum()
)

# Check missing values
print("\nMissing values:")
print(orders_df.isnull().sum())

# Check date range
print("\nOrder date range:")
print(
    orders_df["order_date"].min(),
    "to",
    orders_df["order_date"].max()
)

# Check negative order values
print(
    "\nNegative order values:",
    (orders_df["order_value"] < 0).sum()
)

# Check negative package weights
print(
    "Negative package weights:",
    (orders_df["package_weight_kg"] < 0).sum()
)

# Check unique customers used
print(
    "\nUnique customers used:",
    orders_df["customer_id"].nunique()
)

# Check unique hubs used
print(
    "Unique hubs used:",
    orders_df["origin_hub_id"].nunique()
)

# Check unique vehicles used
print(
    "Unique vehicles used:",
    orders_df["vehicle_id"].nunique()
)

# Check unique employees used
print(
    "Unique employees used:",
    orders_df["assigned_employee_id"].nunique()
)