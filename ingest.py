# ingest.py
import sqlite3
import csv
from pathlib import Path

DB = "ecommerce.db"

schema = {
    "users": """
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        signup_date TEXT,
        country TEXT
    )""",
    "products": """
    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY,
        name TEXT,
        category TEXT,
        price REAL,
        stock INTEGER
    )""",
    "orders": """
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        order_date TEXT,
        total_amount REAL,
        payment_method TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )""",
    "order_items": """
    CREATE TABLE IF NOT EXISTS order_items (
        item_id INTEGER PRIMARY KEY,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        price_each REAL,
        FOREIGN KEY(order_id) REFERENCES orders(order_id),
        FOREIGN KEY(product_id) REFERENCES products(product_id)
    )""",
    "reviews": """
    CREATE TABLE IF NOT EXISTS reviews (
        review_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        product_id INTEGER,
        rating INTEGER,
        review_text TEXT,
        review_date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id),
        FOREIGN KEY(product_id) REFERENCES products(product_id)
    )"""
}

def create_db(conn):
    cur = conn.cursor()
    for name, ddl in schema.items():
        cur.execute(ddl)
    conn.commit()

def load_csv_into_table(conn, csv_path, table, columns):
    cur = conn.cursor()
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = []
        for r in reader:
            rows.append(tuple(r[col] for col in columns))
    placeholders = ",".join(["?"] * len(columns))
    sql = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})"
    cur.executemany(sql, rows)
    conn.commit()
    print(f"Inserted {len(rows)} rows into {table}")

def main():
    conn = sqlite3.connect(DB)
    create_db(conn)

    load_csv_into_table(conn, "users.csv", "users", ["user_id","name","email","signup_date","country"])
    load_csv_into_table(conn, "products.csv", "products", ["product_id","name","category","price","stock"])
    load_csv_into_table(conn, "orders.csv", "orders", ["order_id","user_id","order_date","total_amount","payment_method"])
    load_csv_into_table(conn, "order_items.csv", "order_items", ["item_id","order_id","product_id","quantity","price_each"])
    load_csv_into_table(conn, "reviews.csv", "reviews", ["review_id","user_id","product_id","rating","review_text","review_date"])
    conn.close()
    print("Done. Database:", DB)

if __name__ == "__main__":
    main()
