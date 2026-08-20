# import
import sys
from pathlib import Path
import logging

from faker import Faker
import random
import pandas as pd
from datetime import datetime, timedelta

# getting target folder path and target file paths
target_folder_name = Path(__file__).resolve().parent.parent / 'data' / 'raw'
products_file_path = target_folder_name / "products.csv"
customers_file_path = target_folder_name / "customers.csv"
orders_file_path = target_folder_name / "orders.csv"
order_items_file_path = target_folder_name / "order_items.csv"

# initialise
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
fake = Faker()

products = []
customers = []
orders = []
order_items = []

product_names = ['Laptop', 'Phone', 'Tablet', 'Headphones']
statuses = ['completed', 'cancelled', 'returned']

start_date = datetime(2000, 1, 1)
end_date = datetime.today()

logging.info("generating e-commerce data ...")

# generate random prducts
for product_id in range(1, 501):
    products.append({
        "product_id": product_id,
        "product_name": random.choice(product_names),
        "price": round(random.uniform(5, 1000), 2)
    })

products_df = pd.DataFrame(products)
if products_file_path.exists():
    products_file_path.unlink(missing_ok=True)

if products_df.to_csv(products_file_path.resolve(), index=False) is not None:
    logging.error("error writing products dataframe into csv file")

# generate random customers
for customer_id in range(1, 50001):
    customers.append({
        "customer_id": customer_id,
        "name": fake.name(),
        "email": fake.email()
    })

customers_df = pd.DataFrame(customers)
if customers_file_path.exists():
    customers_file_path.unlink(missing_ok=True)

if customers_df.to_csv(customers_file_path.resolve(), index=False) is not None:
    logging.error("error writing customers dataframe into csv file")

# generate random orders and order_items
for order_id in range(1, 250001):
    days = (end_date - start_date).days
    order_date = start_date + timedelta(days=random.randint(0, days))
    orders.append({
        "order_id": order_id,
        "customer_id": random.choice(customers_df['customer_id']),
        "order_date": order_date.date(),
        "status": random.choice(statuses)
    })

    # order items
    selected_products = products_df.sample(random.randint(1, 5), replace=False)
    for _, product in selected_products.iterrows():

        quantity = random.randint(1, 5)

        order_items.append({
            "order_id": order_id,
            "product_id": product["product_id"],
            "quantity": quantity,
            "unit_price": product["price"]
        })

orders_df = pd.DataFrame(orders)
if orders_file_path.exists():
    orders_file_path.unlink(missing_ok=True)

if orders_df.to_csv(orders_file_path.resolve(), index=False) is not None:
    logging.error("error writing orders dataframe into csv file")

order_items_df = pd.DataFrame(order_items)
if order_items_file_path.exists():
    order_items_file_path.unlink(missing_ok=True)

if order_items_df.to_csv(order_items_file_path.resolve(), index=False) is not None:
    logging.error("error writing order items dataframe into csv file")

logging.info("generating e-commerce data ended")