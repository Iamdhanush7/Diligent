# generate_data.py
import csv
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

N_USERS = 300
N_PRODUCTS = 150
N_ORDERS = 700
MAX_ITEMS_PER_ORDER = 5

# users.csv
with open("users.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["user_id","name","email","signup_date","country"])
    for i in range(1, N_USERS+1):
        w.writerow([i, fake.name(), fake.email(),
                    (datetime.now() - timedelta(days=random.randint(0,1500))).strftime("%Y-%m-%d"),
                    fake.country()])

# products.csv
categories = ["Electronics","Clothing","Home","Beauty","Sports","Toys"]
with open("products.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["product_id","name","category","price","stock"])
    for i in range(1, N_PRODUCTS+1):
        price = round(random.uniform(5, 500), 2)
        stock = random.randint(0, 500)
        w.writerow([i, f"{fake.word().capitalize()} Product {i}", random.choice(categories), price, stock])

# orders.csv and order_items.csv
order_id = 1
with open("orders.csv", "w", newline="", encoding="utf-8") as fo, \
     open("order_items.csv", "w", newline="", encoding="utf-8") as fi:
    wo = csv.writer(fo); wi = csv.writer(fi)
    wo.writerow(["order_id","user_id","order_date","total_amount","payment_method"])
    wi.writerow(["item_id","order_id","product_id","quantity","price_each"])
    item_id = 1
    pay_methods = ["card","paypal","netbanking","cod"]
    for _ in range(N_ORDERS):
        uid = random.randint(1, N_USERS)
        order_date = (datetime.now() - timedelta(days=random.randint(0,365))).strftime("%Y-%m-%d")
        items_count = random.randint(1, MAX_ITEMS_PER_ORDER)
        total = 0.0
        this_items = []
        for _ in range(items_count):
            pid = random.randint(1, N_PRODUCTS)
            qty = random.randint(1, 4)
            price_each = round(random.uniform(5, 500), 2)
            total += qty * price_each
            this_items.append((item_id, order_id, pid, qty, price_each))
            item_id += 1
        wo.writerow([order_id, uid, order_date, round(total,2), random.choice(pay_methods)])
        for it in this_items:
            wi.writerow(it)
        order_id += 1

# reviews.csv
with open("reviews.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["review_id","user_id","product_id","rating","review_text","review_date"])
    rid = 1
    for _ in range(800):
        w.writerow([rid, random.randint(1,N_USERS), random.randint(1,N_PRODUCTS),
                    random.randint(1,5), fake.sentence(nb_words=12),
                    (datetime.now() - timedelta(days=random.randint(0,365))).strftime("%Y-%m-%d")])
        rid += 1

print("CSV files generated: users.csv, products.csv, orders.csv, order_items.csv, reviews.csv")
