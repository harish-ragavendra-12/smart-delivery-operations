import pandas as pd


# --------------------------------------------------
# Load datasets
# --------------------------------------------------

customers_df = pd.read_csv(
    "../data/raw/customers.csv"
)

hubs_df = pd.read_csv(
    "../data/raw/hubs.csv"
)

vehicles_df = pd.read_csv(
    "../data/raw/vehicles.csv"
)

employees_df = pd.read_csv(
    "../data/raw/employees.csv"
)

orders_df = pd.read_csv(
    "../data/raw/orders.csv",
    parse_dates=[
        "order_date",
        "promised_delivery_date",
        "actual_delivery_date"
    ]
)

events_df = pd.read_csv(
    "../data/raw/delivery_events.csv",
    parse_dates=[
        "event_timestamp"
    ]
)


print("=" * 60)
print("SMART DELIVERY OPERATIONS - DATA VALIDATION")
print("=" * 60)


# --------------------------------------------------
# 1. Dataset sizes
# --------------------------------------------------

print("\n--- Dataset Sizes ---")

print("Customers:", customers_df.shape)
print("Hubs:", hubs_df.shape)
print("Vehicles:", vehicles_df.shape)
print("Employees:", employees_df.shape)
print("Orders:", orders_df.shape)
print("Delivery Events:", events_df.shape)


# --------------------------------------------------
# 2. Duplicate checks
# --------------------------------------------------

print("\n--- Duplicate Checks ---")

print(
    "Duplicate customer IDs:",
    customers_df["customer_id"].duplicated().sum()
)

print(
    "Duplicate hub IDs:",
    hubs_df["hub_id"].duplicated().sum()
)

print(
    "Duplicate vehicle IDs:",
    vehicles_df["vehicle_id"].duplicated().sum()
)

print(
    "Duplicate employee IDs:",
    employees_df["employee_id"].duplicated().sum()
)

print(
    "Duplicate order IDs:",
    orders_df["order_id"].duplicated().sum()
)

print(
    "Duplicate event IDs:",
    events_df["event_id"].duplicated().sum()
)


# --------------------------------------------------
# 3. Foreign key validation
# --------------------------------------------------

print("\n--- Foreign Key Validation ---")


invalid_order_customers = (
    ~orders_df["customer_id"].isin(
        customers_df["customer_id"]
    )
).sum()

print(
    "Orders with invalid customer ID:",
    invalid_order_customers
)


invalid_order_hubs = (
    ~orders_df["origin_hub_id"].isin(
        hubs_df["hub_id"]
    )
).sum()

print(
    "Orders with invalid hub ID:",
    invalid_order_hubs
)


invalid_order_vehicles = (
    ~orders_df["vehicle_id"].isin(
        vehicles_df["vehicle_id"]
    )
).sum()

print(
    "Orders with invalid vehicle ID:",
    invalid_order_vehicles
)


invalid_order_employees = (
    ~orders_df["assigned_employee_id"].isin(
        employees_df["employee_id"]
    )
).sum()

print(
    "Orders with invalid employee ID:",
    invalid_order_employees
)


invalid_event_orders = (
    ~events_df["order_id"].isin(
        orders_df["order_id"]
    )
).sum()

print(
    "Events with invalid order ID:",
    invalid_event_orders
)


invalid_event_hubs = (
    ~events_df["hub_id"].isin(
        hubs_df["hub_id"]
    )
).sum()

print(
    "Events with invalid hub ID:",
    invalid_event_hubs
)


invalid_event_vehicles = (
    ~events_df["vehicle_id"].isin(
        vehicles_df["vehicle_id"]
    )
).sum()

print(
    "Events with invalid vehicle ID:",
    invalid_event_vehicles
)


invalid_event_employees = (
    ~events_df["employee_id"].isin(
        employees_df["employee_id"]
    )
).sum()

print(
    "Events with invalid employee ID:",
    invalid_event_employees
)


# --------------------------------------------------
# 4. Order date validation
# --------------------------------------------------

print("\n--- Order Date Validation ---")

invalid_order_dates = (
    orders_df["promised_delivery_date"]
    < orders_df["order_date"]
).sum()

print(
    "Promised date before order date:",
    invalid_order_dates
)


invalid_actual_dates = (
    orders_df["actual_delivery_date"].notna()
    &
    (
        orders_df["actual_delivery_date"]
        < orders_df["order_date"]
    )
).sum()

print(
    "Actual delivery before order date:",
    invalid_actual_dates
)


# --------------------------------------------------
# 5. Delivery status validation
# --------------------------------------------------

print("\n--- Delivery Status Validation ---")

cancelled_with_delivery = (
    (orders_df["delivery_status"] == "Cancelled")
    &
    (orders_df["actual_delivery_date"].notna())
).sum()

returned_with_delivery = (
    (orders_df["delivery_status"] == "Returned")
    &
    (orders_df["actual_delivery_date"].notna())
).sum()

delivered_without_date = (
    orders_df["delivery_status"].isin(
        ["Delivered", "Delayed"]
    )
    &
    orders_df["actual_delivery_date"].isna()
).sum()

print(
    "Cancelled orders with delivery date:",
    cancelled_with_delivery
)

print(
    "Returned orders with delivery date:",
    returned_with_delivery
)

print(
    "Delivered/Delayed orders without delivery date:",
    delivered_without_date
)


# --------------------------------------------------
# 6. Delivery event sequence validation
# --------------------------------------------------

print("\n--- Event Sequence Validation ---")

duplicate_event_sequences = (
    events_df
    .duplicated(
        subset=["order_id", "event_seq"]
    )
    .sum()
)

print(
    "Duplicate event sequences:",
    duplicate_event_sequences
)


# --------------------------------------------------
# 7. Event timestamp validation
# --------------------------------------------------

print("\n--- Event Timestamp Validation ---")

events_sorted = events_df.sort_values(
    ["order_id", "event_seq"]
).copy()


events_sorted["previous_timestamp"] = (
    events_sorted
    .groupby("order_id")["event_timestamp"]
    .shift(1)
)


invalid_event_timestamps = (
    events_sorted["previous_timestamp"].notna()
    &
    (
        events_sorted["event_timestamp"]
        < events_sorted["previous_timestamp"]
    )
).sum()


print(
    "Events with timestamp before previous event:",
    invalid_event_timestamps
)


# --------------------------------------------------
# 8. Event status validation
# --------------------------------------------------

print("\n--- Event Status Validation ---")


cancelled_delivered_events = (
    events_df[
        events_df["order_id"].isin(
            orders_df.loc[
                orders_df["delivery_status"] == "Cancelled",
                "order_id"
            ]
        )
    ]["event_type"]
    == "Delivered"
).sum()


returned_delivered_events = (
    events_df[
        events_df["order_id"].isin(
            orders_df.loc[
                orders_df["delivery_status"] == "Returned",
                "order_id"
            ]
        )
    ]["event_type"]
    == "Delivered"
).sum()


print(
    "Cancelled orders with Delivered event:",
    cancelled_delivered_events
)

print(
    "Returned orders with Delivered event:",
    returned_delivered_events
)


# --------------------------------------------------
# 9. Delay validation
# --------------------------------------------------

print("\n--- Delay Validation ---")

negative_delays = (
    events_df["delay_minutes"] < 0
).sum()

print(
    "Negative delay minutes:",
    negative_delays
)


delay_reason_without_delay = (
    events_df["delay_reason"].notna()
    &
    (events_df["delay_minutes"] <= 0)
).sum()

print(
    "Delay reason without delay minutes:",
    delay_reason_without_delay
)


delay_without_reason = (
    (events_df["delay_minutes"] > 0)
    &
    events_df["delay_reason"].isna()
).sum()

print(
    "Delay minutes without delay reason:",
    delay_without_reason
)


# --------------------------------------------------
# 10. Numeric validation
# --------------------------------------------------

print("\n--- Numeric Validation ---")

negative_package_weights = (
    orders_df["package_weight_kg"] < 0
).sum()

negative_order_values = (
    orders_df["order_value"] < 0
).sum()

negative_route_distances = (
    orders_df["route_distance_km"] < 0
).sum()

print(
    "Negative package weights:",
    negative_package_weights
)

print(
    "Negative order values:",
    negative_order_values
)

print(
    "Negative route distances:",
    negative_route_distances
)


# --------------------------------------------------
# 11. Order and event relationship
# --------------------------------------------------

print("\n--- Order/Event Relationship ---")

orders_with_events = (
    events_df["order_id"]
    .nunique()
)

print(
    "Orders:",
    orders_df["order_id"].nunique()
)

print(
    "Orders represented in events:",
    orders_with_events
)

print(
    "Orders without events:",
    orders_df["order_id"]
    .nunique() - orders_with_events
)


# --------------------------------------------------
# 12. Event count per order
# --------------------------------------------------

print("\n--- Events Per Order ---")

events_per_order = (
    events_df
    .groupby("order_id")
    .size()
)

print(
    "Minimum events per order:",
    events_per_order.min()
)

print(
    "Maximum events per order:",
    events_per_order.max()
)

print(
    "Average events per order:",
    round(events_per_order.mean(), 2)
)


# --------------------------------------------------
# Final message
# --------------------------------------------------

print("\n" + "=" * 60)
print("DATA VALIDATION COMPLETED")
print("=" * 60)