import pandas as pd
import sqlite3

conn = sqlite3.connect("data/ecommerce.db")

# Get the list of all tables in the database
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)

# For each table, show its columns
for table_name in tables["name"]:
    print(f"\n=== {table_name} ===")
    info = pd.read_sql(f"PRAGMA table_info({table_name});", conn)
    print(info[["name", "type"]])

conn.close()