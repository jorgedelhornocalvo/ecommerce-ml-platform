import pandas as pd

# Load the orders table from the data folder
orders = pd.read_csv("data/olist_orders_dataset.csv")

# How many rows and columns does it have?
print("Shape (rows, columns):", orders.shape)

# What are the column names?
print("\nColumns:")
print(orders.columns.tolist())

# A peek at the first 5 rows
print("\nFirst rows:")
print(orders.head()) 