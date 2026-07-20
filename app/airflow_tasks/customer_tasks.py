"""
Airflow task wrapper for the Customers ETL pipeline.

This module exposes functions that can be used by Airflow operators
to execute the customer loading process.
"""


from app.core.logger import get_logger
from app.etl.loaders.customers_loader import CustomersLoader

logger = get_logger(__name__)

def load_customers():
    logger.info("Starting Airflow task: Load Customers")

    loader = CustomersLoader()
    loader.run()

    logger.info("Completed Airflow task: Load Customers")