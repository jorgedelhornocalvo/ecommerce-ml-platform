import pandas as pd
import sqlite3

# Open the database we just created
conn = sqlite3.connect("data/ecommerce.db")

# Query 1: count how many orders there are
q1 = pd.read_sql("SELECT COUNT(*) AS total_orders FROM orders;", conn)
print("How many orders?")
print(q1)

# Query 2: count orders by status
q2 = pd.read_sql("""
    SELECT order_status, COUNT(*) AS total
    FROM orders
    GROUP BY order_status
    ORDER BY total DESC;
""", conn)
print("\nOrders by status:")
print(q2)

conn.close()