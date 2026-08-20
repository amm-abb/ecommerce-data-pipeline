# import
import shutil
from pathlib import Path
import logging

from pyspark.sql import SparkSession
from pyspark.sql.functions import (col, round)

# initialise
source_folder_name = Path(__file__).resolve().parent.parent / 'data' / 'raw'
products_file_path = source_folder_name / "products.csv"
orders_file_path = source_folder_name / "orders.csv"
order_items_file_path = source_folder_name / "order_items.csv"

target_file_path = Path(__file__).resolve().parent.parent / 'data' / 'processed' / 'sales'

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# spark session
spark = (SparkSession.builder.appName("EcommerceTransformation").getOrCreate())

if products_file_path.exists():
    products = spark.read.csv(str(products_file_path.resolve()), header=True, inferSchema=True)
else:
    logging.error(str(products_file_path.resolve()) + "could not be found")

if orders_file_path.exists():
    orders = spark.read.csv(str(orders_file_path.resolve()), header=True, inferSchema=True)
else:
    logging.error(str(orders_file_path.resolve()) + "could not be found")

if order_items_file_path.exists():
    order_items = spark.read.csv(str(order_items_file_path.resolve()), header=True, inferSchema=True)
else:
    logging.error(str(order_items_file_path.resolve()) + "could not be found")


logging.info("transforming sales data ...")
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

# save to parquet
if target_file_path.exists():
    shutil.rmtree(target_file_path)
sales.write.mode("overwrite").parquet(str(target_file_path.resolve()))

spark.stop()

logging.info("transforming sales data ended")