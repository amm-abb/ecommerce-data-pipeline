# Ecommerce Data Pipeline using Spark, Postgesql, Airflow and dbt

An ecommerce data pipeline baseline with:

- Python and PySpark
- Spark
- PostgreSQL
- Docker Compose
- Airflow DAG
- dbt Analytics
- basic tests

## Install
pip install -e ".[dev]"

## Run locally

```bash
1. cp .env.example .env
# in .env put:
# HOST_NAME=localhost for a db on local machine or HOST_NAME=postgre for a db on docker
# POSTGRES_DB=<your_database_name>
# POSTGRES_USER=<your_database_user>
# POSTGRES_PASSWORD=<your_database_password>

```bash
1. cd dags
2. python3 ecommerce_pipeline.py

# access the database from docker and perform some data analytics
```bash
- docker-compose ps
- docker-compose up -d
- docker exec -it <container_name> psql -U $POSTGRES_USER -d $POSTGRES_DB
- run SQL queries. Example queries can be found under: /sql/analytics.sql

## dbt
dbt run

## tests
# bash
pytest -v
