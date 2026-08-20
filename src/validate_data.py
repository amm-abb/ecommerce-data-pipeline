# import
from pathlib import Path
import logging

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import (col, round)

# initialise
source_folder_name = Path(__file__).resolve().parent.parent / 'data' / 'raw'
products_file_path = source_folder_name / "products.csv"
customers_file_path = source_folder_name / "customers.csv"
orders_file_path = source_folder_name / "orders.csv"
order_items_file_path = source_folder_name / "order_items.csv"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# spark session
spark = (SparkSession.builder.appName("EcommerceTransformation").getOrCreate())

# data reading
if products_file_path.exists():
    products = spark.read.csv(str(products_file_path.resolve()), header=True, inferSchema=True)
else:
    logging.error(str(products_file_path.resolve()) + "could not be found")

if customers_file_path.exists():
    customers = spark.read.csv(str(customers_file_path.resolve()), header=True, inferSchema=True)
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

logging.info("validating products data ...")
products.select(F.count(F.col('product_id')).alias('total'), 
                F.count(F.when(F.col('product_id').isNull(), 1)).alias('invalid IDs'),
                (F.count(F.col('product_id')) - F.count_distinct('product_id')).alias('duplicate IDs'), 
                F.count(F.when(F.col('price') < 0.0, 1)).alias('negative price')).show()

logging.info("validating customers data ...")
customers.select(F.count(F.col('customer_id')).alias('total'),  
                F.count(F.when(F.col('customer_id').isNull(), 1)).alias('invalid IDs'),
                (F.count(F.col('customer_id')) - F.count_distinct('customer_id')).alias('duplicate IDs')).show()

logging.info("validating orders data ...")
orders.select(F.count(F.col('order_id')).alias('total'), 
                F.count(F.when(F.col('order_id').isNull(), 1)).alias('invalid IDs'),
                (F.count(F.col('order_id')) - F.count_distinct('order_id')).alias('duplicate IDs'), 
                F.count(F.when(F.col('customer_id').isNull(), 1)).alias('invalid customer IDs')).show()

logging.info("validating order items data ...")
order_items.select(F.count(F.col('order_id')).alias('total'), 
                F.count(F.when(F.col('order_id').isNull(), 1)).alias('invalid IDs'),  
                F.count(F.when(F.col('product_id').isNull(), 1)).alias('invalid product IDs'), 
                F.count(F.when(F.col('quantity') < 0.0, 1)).alias('negative quantity')).show()

spark.stop()

logging.info("validating data ended")