"""
Customers Dataset Loader

Loads the Olist customers dataset into PostgreSQL.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from app.core.config import RAW_DATA_DIR
from app.core.logger import get_logger
from app.etl.csv_loader import CSVLoader
from app.etl.validators import DataValidator
from app.database.session import get_database_connection
from app.etl.batch_writer import BatchWriter
logger = get_logger(__name__)


class CustomersLoader(CSVLoader):
    """
    ETL loader for the customers dataset.
    """

    def __init__(self) -> None:
        """
        Initialize the customers loader.
        """

        source_file = RAW_DATA_DIR / "olist_customers_dataset.csv"

        super().__init__(source_file)

    def transform(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Validate and transform the customers dataset.
        """

        DataValidator.validate_empty_dataframe(dataframe)

        DataValidator.validate_required_columns(
            dataframe,
            [
                "customer_id",
                "customer_unique_id",
                "customer_zip_code_prefix",
                "customer_city",
                "customer_state",
            ],
        )

        DataValidator.validate_duplicate_rows(dataframe)

        DataValidator.validate_missing_values(dataframe)

        logger.info("Selecting required warehouse columns.")

        dataframe = dataframe[
            [
                "customer_id",
                "customer_unique_id",
                "customer_city",
                "customer_state",
            ]
        ]

        logger.info("Customer dataset transformation completed.")

        return dataframe

    def load(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Load the customer dataset into PostgreSQL.
        """

        logger.info(
            "Preparing customer records for database insertion."
        )

        records = list(
            dataframe.itertuples(index=False, name=None)
        )

        logger.info(
            "Prepared %d customer records.",
            len(records),
        )

        insert_query = """
            INSERT INTO dim_customers
            (
                customer_id,
                customer_unique_id,
                customer_city,
                customer_state
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
            ON CONFLICT (customer_id)
            DO NOTHING;
        """

        with get_database_connection() as connection:

            writer = BatchWriter(connection)

            writer.insert(
                query=insert_query,
                records=records,
            )

        logger.info(
            "Customer data successfully loaded into PostgreSQL."
        )

    def run(self) -> None:
        """
        Execute the customer ETL pipeline.
        """

        logger.info("Starting Customers ETL.")

        dataframe = self.extract()

        dataframe = self.transform(dataframe)

        self.load(dataframe)

        logger.info("Customers ETL completed successfully.")


def main() -> None:
    """
    Test the customer loader.
    """

    loader = CustomersLoader()

    loader.run()


if __name__ == "__main__":
    main()