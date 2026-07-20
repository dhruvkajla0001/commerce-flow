"""
CommerceFlow ETL Pipeline

Apache Airflow DAG for orchestrating the CommerceFlow
Data Engineering pipeline.
"""

from __future__ import annotations

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from app.airflow_tasks.analytics_tasks import run_analytics
from app.airflow_tasks.customer_tasks import load_customers
from app.airflow_tasks.date_tasks import load_dates
from app.airflow_tasks.fact_tasks import load_fact_orders
from app.airflow_tasks.product_tasks import load_products
from app.airflow_tasks.seller_tasks import load_sellers

# ------------------------------------------------------------------
# Default DAG Configuration
# ------------------------------------------------------------------

default_args = {
    "owner": "Dhruv Kajla",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

# ------------------------------------------------------------------
# DAG Definition
# ------------------------------------------------------------------

with DAG(
    dag_id="commerceflow_pipeline",
    description="CommerceFlow End-to-End ETL Pipeline",
    default_args=default_args,
    start_date=datetime(2026, 7, 20),
    schedule=None,
    catchup=False,
    tags=["commerceflow", "etl", "postgres"],
) as dag:

    # --------------------------------------------------------------
    # Pipeline Start
    # --------------------------------------------------------------

    start = EmptyOperator(
        task_id="start_pipeline",
    )

    health_check = EmptyOperator(
        task_id="health_check",
    )

    # --------------------------------------------------------------
    # Dimension Loading Tasks
    # --------------------------------------------------------------

    customers = PythonOperator(
        task_id="load_customers",
        python_callable=load_customers,
    )

    products = PythonOperator(
        task_id="load_products",
        python_callable=load_products,
    )

    sellers = PythonOperator(
        task_id="load_sellers",
        python_callable=load_sellers,
    )

    dates = PythonOperator(
        task_id="load_dates",
        python_callable=load_dates,
    )

    # --------------------------------------------------------------
    # Fact Loading Task
    # --------------------------------------------------------------

    fact_orders = PythonOperator(
        task_id="load_fact_orders",
        python_callable=load_fact_orders,
    )

    # --------------------------------------------------------------
    # Analytics Task
    # --------------------------------------------------------------

    analytics = PythonOperator(
        task_id="run_analytics",
        python_callable=run_analytics,
    )

    # --------------------------------------------------------------
    # Pipeline End
    # --------------------------------------------------------------

    end = EmptyOperator(
        task_id="end_pipeline",
    )

    # --------------------------------------------------------------
    # Pipeline Flow
    # --------------------------------------------------------------

    (
        start
        >> health_check
        >> customers
        >> products
        >> sellers
        >> dates
        >> fact_orders
        >> analytics
        >> end
    )