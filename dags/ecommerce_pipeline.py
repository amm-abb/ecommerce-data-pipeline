# import
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

from src import validate_data, load_postgres

with DAG(
    dag_id="ecommerce_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule='@daily',
    catchup=False,
) as dag:

    validate_task = SparkSubmitOperator(
        task_id="validate",
        application="validate_data",
        conn_id="spark_default",
        name="ecommerce_sales",
        verbose=True,
    )

    load_task = SparkSubmitOperator(
        task_id="load",
        application="../src/load_postgres.py",
        conn_id="spark_default",
        name="ecommerce_sales",
        packages="org.postgresql:postgresql:42.7.8",
        verbose=True,
    )