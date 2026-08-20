# import
import os
from pathlib import Path
import logging

from pyspark.sql import SparkSession
from pyspark.sql.functions import (col, round)

from dotenv import load_dotenv
load_dotenv()

host_name = os.getenv("HOST_NAME")
db_name = os.getenv("POSTGRES_DB")
db_user = os.getenv("POSTGRES_USER")
db_password= os.getenv("POSTGRES_PASSWORD")

jdbc_url = "jdbc:postgresql://"+host_name+":5432/"+db_name
connection_properties = {"user": db_user, "password": db_password, "driver": "org.postgresql.Driver"}

# initialise
source_folder_name = Path(__file__).resolve().parent.parent / 'data' / 'raw'
products_file_path = source_folder_name / "products.csv"
customers_file_path = source_folder_name / "customers.csv"
orders_file_path = source_folder_name / "orders.csv"
order_items_file_path = source_folder_name / "order_items.csv"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# spark session
spark = (SparkSession.builder
        .config("spark.jars.packages", "org.postgresql:postgresql:42.7.8")
        .appName("EcommerceTransformation")
        .getOrCreate()
        )

logging.info("loading data to postgresql database ...")

# data reading
if products_file_path.exists():
    products = spark.read.csv(str(products_file_path.resolve()), header=True, inferSchema=True)
    products.write.jdbc(url=jdbc_url, table="products", mode="append", properties=connection_properties)
else:
    logging.error(str(products_file_path.resolve()) + "could not be found")

if customers_file_path.exists():
    customers = spark.read.csv(str(customers_file_path.resolve()), header=True, inferSchema=True)
    customers.write.jdbc(url=jdbc_url, table="customers", mode="append", properties=connection_properties)
else:
    logging.error(str(customers_file_path.resolve()) + "could not be found")

if orders_file_path.exists():
    orders = spark.read.csv(str(orders_file_path.resolve()), header=True, inferSchema=True)
else:
    logging.error(str(orders_file_path.resolve()) + "could not be found")

if order_items_file_path.exists():
    order_items = spark.read.csv(str(order_items_file_path.resolve()), header=True, inferSchema=True)
else:
    logging.error(str(order_items_file_path.resolve()) + "could not be found")


sales = (
    order_items
    .join(orders, on="order_id", how="inner")
    .join(products, on="product_id", how="inner")
    .select(
        "order_id",
        "customer_id",
        "product_id",
        "order_date",
        "quantity",
        "unit_price",
        "status"
    )
    .withColumn(
        "revenue",
        round(col("quantity") * col("unit_price"), 2)
    )
)

sales.write.jdbc(url=jdbc_url, table="sales", mode="append", properties=connection_properties)

spark.stop()

logging.info("loading data to postgresql database ended")