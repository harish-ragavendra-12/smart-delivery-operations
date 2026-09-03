import pandas as pd
import numpy as np
import random
from datetime import timedelta

# --------------------------------------------------
# Reproducible results
# --------------------------------------------------

random.seed(42)
np.random.seed(42)


# --------------------------------------------------
# Load data
# --------------------------------------------------

orders_df = pd.read_csv(
    "../data/raw/orders.csv",
    parse_dates=[
        "order_date",
        "promised_delivery_date",
        "actual_delivery_date"
    ]
)

hubs_df = pd.read_csv("../data/raw/hubs.csv")
vehicles_df = pd.read_csv("../data/raw/vehicles.csv")
employees_df = pd.read_csv("../data/raw/employees.csv")


print("Data loaded successfully!")

print("Orders:", len(orders_df))
print("Hubs:", len(hubs_df))
print("Vehicles:", len(vehicles_df))
print("Employees:", len(employees_df))


# --------------------------------------------------
# Create lookup dictionaries
# --------------------------------------------------

hub_info = (
    hubs_df
    .set_index("hub_id")
    .to_dict("index")
)

vehicle_info = (
    vehicles_df
    .set_index("vehicle_id")
    .to_dict("index")
)


# --------------------------------------------------
# Event types
# --------------------------------------------------

event_types = [
    "Order Placed",
    "Pickup Scheduled",
    "Picked Up",
    "Arrived at Origin Hub",
    "Processing at Hub",
    "Departed Origin Hub",
    "Arrived at Destination Hub",
    "Out for Delivery",
    "Delivery Attempted",
    "Delivered"
]


# --------------------------------------------------
# Delay reasons
# --------------------------------------------------

delay_reasons = [
    "Traffic",
    "Weather",
    "Vehicle Breakdown",
    "Hub Congestion",
    "Staff Shortage",
    "Address Issue",
    "Incorrect Sorting",
    "Customer Unavailable",
    "Route Planning Issue",
    "System Issue"
]


# --------------------------------------------------
# Generate delivery events
# --------------------------------------------------

events = []

event_id = 1


for _, order in orders_df.iterrows():

    order_id = order["order_id"]
    order_date = order["order_date"]
    actual_delivery_date = order["actual_delivery_date"]

    origin_hub_id = order["origin_hub_id"]
    vehicle_id = order["vehicle_id"]
    employee_id = order["assigned_employee_id"]

    destination_city = order["destination_city"]
    delivery_status = order["delivery_status"]

    route_distance = order["route_distance_km"]

    vehicle = vehicle_info[vehicle_id]
    hub = hub_info[origin_hub_id]


    # --------------------------------------------------
    # Determine event count
    # --------------------------------------------------

    if delivery_status == "Cancelled":

        current_events = [
            "Order Placed",
            "Pickup Scheduled"
        ]

    elif delivery_status == "Returned":

        current_events = [
            "Order Placed",
            "Pickup Scheduled",
            "Picked Up",
            "Arrived at Origin Hub",
            "Processing at Hub",
            "Departed Origin Hub",
            "Arrived at Destination Hub",
            "Out for Delivery",
            "Delivery Attempted"
        ]

    else:

        current_events = event_types


    # --------------------------------------------------
    # Calculate total delivery duration
    # --------------------------------------------------

    if pd.notna(actual_delivery_date):

        total_hours = (
            actual_delivery_date - order_date
        ).total_seconds() / 3600

    else:

        total_hours = random.uniform(4, 48)


    # Prevent extremely small durations
    total_hours = max(total_hours, 2)


    # --------------------------------------------------
    # Create timestamps across the delivery process
    # --------------------------------------------------

    number_of_events = len(current_events)

    if number_of_events > 1:

        interval_hours = (
            total_hours / (number_of_events - 1)
        )

    else:

        interval_hours = 0


    for seq, event_type in enumerate(current_events, start=1):

        event_timestamp = (
            order_date
            + timedelta(
                hours=interval_hours * (seq - 1)
            )
        )


        # --------------------------------------------------
        # Determine delay
        # --------------------------------------------------

        delay_minutes = 0
        delay_reason = None


        # Delayed orders get operational delay events
        if delivery_status == "Delayed":

            # Some events receive delays
            if random.random() < 0.35:

                possible_reasons = delay_reasons.copy()


                # Older vehicles are more likely to break down
                vehicle_age = 2026 - vehicle["registration_year"]

                if vehicle_age < 5:
                    possible_reasons.remove(
                        "Vehicle Breakdown"
                    )


                # Longer routes have higher traffic risk
                if route_distance < 300:
                    if "Traffic" in possible_reasons:
                        possible_reasons.remove("Traffic")


                # Low-capacity hubs have more congestion
                hub_capacity = hub["capacity_per_day"]

                if hub_capacity >= 2200:
                    if "Hub Congestion" in possible_reasons:
                        possible_reasons.remove(
                            "Hub Congestion"
                        )


                delay_reason = random.choice(
                    possible_reasons
                )


                # Generate delay minutes
                if delay_reason == "Traffic":
                    delay_minutes = random.randint(30, 240)

                elif delay_reason == "Weather":
                    delay_minutes = random.randint(60, 360)

                elif delay_reason == "Vehicle Breakdown":
                    delay_minutes = random.randint(120, 480)

                elif delay_reason == "Hub Congestion":
                    delay_minutes = random.randint(60, 300)

                elif delay_reason == "Staff Shortage":
                    delay_minutes = random.randint(60, 240)

                elif delay_reason == "Address Issue":
                    delay_minutes = random.randint(30, 180)

                elif delay_reason == "Incorrect Sorting":
                    delay_minutes = random.randint(60, 360)

                elif delay_reason == "Customer Unavailable":
                    delay_minutes = random.randint(30, 180)

                elif delay_reason == "Route Planning Issue":
                    delay_minutes = random.randint(30, 240)

                elif delay_reason == "System Issue":
                    delay_minutes = random.randint(15, 120)


        # Returned deliveries can have customer issues
        if delivery_status == "Returned":

            if event_type == "Delivery Attempted":

                delay_reason = "Customer Unavailable"
                delay_minutes = random.randint(30, 180)


        # --------------------------------------------------
        # Remarks
        # --------------------------------------------------

        remarks = None

        if delay_reason == "Traffic":
            remarks = "Heavy traffic caused delivery delay"

        elif delay_reason == "Weather":
            remarks = "Adverse weather conditions"

        elif delay_reason == "Vehicle Breakdown":
            remarks = "Vehicle required maintenance"

        elif delay_reason == "Hub Congestion":
            remarks = "High volume at hub"

        elif delay_reason == "Staff Shortage":
            remarks = "Insufficient operational staff"

        elif delay_reason == "Address Issue":
            remarks = "Customer address required clarification"

        elif delay_reason == "Incorrect Sorting":
            remarks = "Package incorrectly sorted"

        elif delay_reason == "Customer Unavailable":
            remarks = "Customer unavailable during delivery attempt"

        elif delay_reason == "Route Planning Issue":
            remarks = "Route required operational adjustment"

        elif delay_reason == "System Issue":
            remarks = "Temporary system issue"


        # --------------------------------------------------
        # Location
        # --------------------------------------------------

        if event_type in [
            "Order Placed",
            "Pickup Scheduled",
            "Picked Up"
        ]:

            location_city = hub["city"]

        elif event_type in [
            "Arrived at Origin Hub",
            "Processing at Hub",
            "Departed Origin Hub"
        ]:

            location_city = hub["city"]

        else:

            location_city = destination_city


        # --------------------------------------------------
        # Create event record
        # --------------------------------------------------

        event = {

            "event_id": f"EVT{event_id:07d}",

            "order_id": order_id,

            "event_seq": seq,

            "event_type": event_type,

            "event_timestamp": event_timestamp,

            "hub_id": origin_hub_id,

            "vehicle_id": vehicle_id,

            "employee_id": employee_id,

            "location_city": location_city,

            "delay_minutes": delay_minutes,

            "delay_reason": delay_reason,

            "remarks": remarks
        }


        events.append(event)

        event_id += 1


# --------------------------------------------------
# Convert to DataFrame
# --------------------------------------------------

events_df = pd.DataFrame(events)


# --------------------------------------------------
# Sort events
# --------------------------------------------------

events_df = events_df.sort_values(
    ["order_id", "event_seq"]
).reset_index(drop=True)


# --------------------------------------------------
# Save
# --------------------------------------------------

events_df.to_csv(
    "../data/raw/delivery_events.csv",
    index=False
)


# --------------------------------------------------
# Validation
# --------------------------------------------------

print("\nDelivery events generated successfully!")

print("Shape:", events_df.shape)

print("\nFirst 10 events:")
print(events_df.head(10))

print("\nEvent type distribution:")
print(events_df["event_type"].value_counts())

print("\nTotal delay minutes:")
print(events_df["delay_minutes"].sum())

print("\nDelay reason distribution:")
print(
    events_df["delay_reason"]
    .value_counts(dropna=False)
)

print("\nUnique orders:")
print(events_df["order_id"].nunique())

print("\nDuplicate event IDs:")
print(
    events_df["event_id"].duplicated().sum()
)

print("\nMissing values:")
print(events_df.isnull().sum())

print("\nSaved to: data/raw/delivery_events.csv")