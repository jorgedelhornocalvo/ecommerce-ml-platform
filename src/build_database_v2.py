import pandas as pd
import sqlite3

# Start a fresh database file for the well-designed version
conn = sqlite3.connect("data/ecommerce_v2.db")
cursor = conn.cursor()

# --- Step 1: define the 'orders' table with SQL ---
# We drop it first so the script can be run again without errors.
cursor.execute("DROP TABLE IF EXISTS orders;")

cursor.execute("""
    CREATE TABLE orders (
        order_id                      TEXT PRIMARY KEY,
        customer_id                   TEXT,
        order_status                  TEXT,
        order_purchase_timestamp      TEXT,
        order_approved_at             TEXT,
        order_delivered_carrier_date  TEXT,
        order_delivered_customer_date TEXT,
        order_estimated_delivery_date TEXT
    );
""")

# --- Step 2: fill it with data from the CSV ---
orders = pd.read_csv("data/olist_orders_dataset.csv")
orders.to_sql("orders", conn, if_exists="append", index=False)

# --- 'customers' table ---
cursor.execute("DROP TABLE IF EXISTS customers;")

cursor.execute("""
    CREATE TABLE customers (
        customer_id              TEXT PRIMARY KEY,
        customer_unique_id       TEXT,
        customer_zip_code_prefix INTEGER,
        customer_city            TEXT,
        customer_state           TEXT
    );
""")

customers = pd.read_csv("data/olist_customers_dataset.csv")
customers.to_sql("customers", conn, if_exists="append", index=False)

# --- 'reviews' table (with a foreign key to orders) ---
cursor.execute("DROP TABLE IF EXISTS reviews;")

cursor.execute("""
    CREATE TABLE reviews (
        review_id               TEXT,
        order_id                TEXT,
        review_score            INTEGER,
        review_comment_title    TEXT,
        review_comment_message  TEXT,
        review_creation_date    TEXT,
        review_answer_timestamp TEXT,
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
    );
""")

reviews = pd.read_csv("data/olist_order_reviews_dataset.csv")
reviews.to_sql("reviews", conn, if_exists="append", index=False)

# --- 'products' table ---
cursor.execute("DROP TABLE IF EXISTS products;")

cursor.execute("""
    CREATE TABLE products (
        product_id                 TEXT PRIMARY KEY,
        product_category_name      TEXT,
        product_name_lenght        REAL,
        product_description_lenght REAL,
        product_photos_qty         REAL,
        product_weight_g           REAL,
        product_length_cm          REAL,
        product_height_cm          REAL,
        product_width_cm           REAL
    );
""")

products = pd.read_csv("data/olist_products_dataset.csv")
products.to_sql("products", conn, if_exists="append", index=False)

# --- 'order_items' table (two foreign keys) ---
cursor.execute("DROP TABLE IF EXISTS order_items;")

cursor.execute("""
    CREATE TABLE order_items (
        order_id            TEXT,
        order_item_id       INTEGER,
        product_id          TEXT,
        seller_id           TEXT,
        shipping_limit_date TEXT,
        price               REAL,
        freight_value       REAL,
        FOREIGN KEY (order_id)   REFERENCES orders(order_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );
""")

order_items = pd.read_csv("data/olist_order_items_dataset.csv")
order_items.to_sql("order_items", conn, if_exists="append", index=False)

# --- 'sellers' table ---
cursor.execute("DROP TABLE IF EXISTS sellers;")

cursor.execute("""
    CREATE TABLE sellers (
        seller_id              TEXT PRIMARY KEY,
        seller_zip_code_prefix INTEGER,
        seller_city            TEXT,
        seller_state           TEXT
    );
""")

sellers = pd.read_csv("data/olist_sellers_dataset.csv")
sellers.to_sql("sellers", conn, if_exists="append", index=False)


# --- 'order_payments' table (foreign key to orders) ---
cursor.execute("DROP TABLE IF EXISTS order_payments;")

cursor.execute("""
    CREATE TABLE order_payments (
        order_id             TEXT,
        payment_sequential   INTEGER,
        payment_type         TEXT,
        payment_installments INTEGER,
        payment_value        REAL,
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
    );
""")

order_payments = pd.read_csv("data/olist_order_payments_dataset.csv")
order_payments.to_sql("order_payments", conn, if_exists="append", index=False)

# --- 'geolocation' table ---
cursor.execute("DROP TABLE IF EXISTS geolocation;")

cursor.execute("""
    CREATE TABLE geolocation (
        geolocation_zip_code_prefix INTEGER,
        geolocation_lat             REAL,
        geolocation_lng             REAL,
        geolocation_city            TEXT,
        geolocation_state           TEXT
    );
""")

geolocation = pd.read_csv("data/olist_geolocation_dataset.csv")
geolocation.to_sql("geolocation", conn, if_exists="append", index=False)

# --- 'category_translation' table ---
cursor.execute("DROP TABLE IF EXISTS category_translation;")

cursor.execute("""
    CREATE TABLE category_translation (
        product_category_name         TEXT PRIMARY KEY,
        product_category_name_english TEXT
    );
""")

category_translation = pd.read_csv("data/product_category_name_translation.csv")
category_translation.to_sql("category_translation", conn, if_exists="append", index=False)

# --- Check: list every table with its row count ---
tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
print("Tables in the database:\n")
for table_name in tables["name"]:
    count = pd.read_sql(f"SELECT COUNT(*) AS total FROM {table_name};", conn)
    print(f"  {table_name:<15} -> {count['total'][0]} rows")

conn.commit()
conn.close()
print("\nDone.")