import pandas as pd
import random
from faker import Faker

# Initialize Faker
fake = Faker("en_IN")

# Reproducible results
random.seed(42)

# Number of employees
NUM_EMPLOYEES = 300

# Employee roles
roles = [
    "Delivery Executive",
    "Dispatcher",
    "Operations Executive",
    "Hub Manager"
]

# Employment types
employment_types = [
    "Full Time",
    "Contract"
]

# Hub IDs
hub_ids = [f"HUB{i:03d}" for i in range(1, 21)]

employees = []

for i in range(1, NUM_EMPLOYEES + 1):

    role = random.choice(roles)

    # Managers generally have more experience
    if role == "Hub Manager":
        experience = random.randint(5, 15)
    elif role == "Operations Executive":
        experience = random.randint(2, 10)
    elif role == "Dispatcher":
        experience = random.randint(1, 8)
    else:
        experience = random.randint(0, 7)

    employee = {
        "employee_id": f"EMP{i:04d}",
        "employee_name": fake.name(),
        "role": role,
        "hub_id": random.choice(hub_ids),
        "experience_years": experience,
        "employment_type": random.choice(employment_types)
    }

    employees.append(employee)

# Create DataFrame
employees_df = pd.DataFrame(employees)

# Display information
print("Employees dataset created successfully!")
print("Shape:", employees_df.shape)

print("\nFirst 5 records:")
print(employees_df.head())

print("\nEmployee roles:")
print(employees_df["role"].value_counts())

print("\nEmployment type:")
print(employees_df["employment_type"].value_counts())

print("\nEmployees by hub:")
print(employees_df["hub_id"].value_counts().head())

# Save dataset
employees_df.to_csv(
    "../data/raw/employees.csv",
    index=False
)

print("\nSaved to: data/raw/employees.csv")