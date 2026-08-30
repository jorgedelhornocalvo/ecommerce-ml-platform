import pandas as pd
import sqlite3

# Open (and create) the database file
conn = sqlite3.connect("data/ecommerce.db")

# Load two CSV tables into pandas
orders = pd.read_csv("data/olist_orders_dataset.csv")
reviews = pd.read_csv("data/olist_order_reviews_dataset.csv")

# Save each table inside the database
orders.to_sql("orders", conn, if_exists="replace", index=False)
reviews.to_sql("reviews", conn, if_exists="replace", index=False)

# Ask the database which tables it now contains
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
print("Tables in the database:")
print(tables)

conn.close()
print("\nDatabase created successfully.")