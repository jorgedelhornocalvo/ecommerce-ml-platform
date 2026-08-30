import pandas as pd
import sqlite3

# Open (and create) the database file
conn = sqlite3.connect("data/ecommerce.db")

# Map each CSV file to the table name it will have in the database
csv_files = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
}

# Loop through every file and load it into the database
for table_name, file_name in csv_files.items():
    df = pd.read_csv(f"data/{file_name}")
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"Loaded '{table_name}'  ->  {df.shape[0]} rows, {df.shape[1]} columns")

# Confirm all tables are in the database
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
print("\nTables now in the database:")
print(tables)

conn.close()
print("\nDatabase built successfully.")