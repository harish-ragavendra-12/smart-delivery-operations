import pandas as pd
import numpy as np
from faker import Faker
import random

# Initialize Faker
fake = Faker("en_IN")

# Make results reproducible
random.seed(42)
np.random.seed(42)

# Number of customers
NUM_CUSTOMERS = 10000

# Customer options
customer_types = [
    "Individual",
    "Business"
]

customer_segments = [
    "Retail",
    "SMB",
    "Enterprise"
]

# Indian cities
cities = [
    "Bangalore",
    "Chennai",
    "Hyderabad",
    "Mumbai",
    "Pune",
    "Delhi",
    "Kolkata",
    "Ahmedabad",
    "Coimbatore",
    "Kochi",
    "Mysore",
    "Jaipur"
]

# States corresponding to the cities
city_state = {
    "Bangalore": "Karnataka",
    "Chennai": "Tamil Nadu",
    "Hyderabad": "Telangana",
    "Mumbai": "Maharashtra",
    "Pune": "Maharashtra",
    "Delhi": "Delhi",
    "Kolkata": "West Bengal",
    "Ahmedabad": "Gujarat",
    "Coimbatore": "Tamil Nadu",
    "Kochi": "Kerala",
    "Mysore": "Karnataka",
    "Jaipur": "Rajasthan"
}


# Generate customers
customers = []

for i in range(1, NUM_CUSTOMERS + 1):

    city = random.choice(cities)

    customer = {
        "customer_id": f"CUST{i:05d}",
        "customer_name": fake.name(),
        "customer_type": random.choice(customer_types),
        "city": city,
        "state": city_state[city],
        "customer_segment": random.choice(customer_segments),
        "registration_date": fake.date_between(
            start_date="-5y",
            end_date="today"
        )
    }

    customers.append(customer)


# Convert to DataFrame
customers_df = pd.DataFrame(customers)


# Display basic information
print("Customers dataset created successfully!")
print("Shape:", customers_df.shape)

print("\nFirst 5 records:")
print(customers_df.head())

print("\nCustomer segments:")
print(customers_df["customer_segment"].value_counts())


# Save dataset
customers_df.to_csv(
    "../data/raw/customers.csv",
    index=False
)

print("\nSaved to: data/raw/customers.csv")