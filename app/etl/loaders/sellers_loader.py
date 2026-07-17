"""
Sellers Dataset Loader

Loads the Olist sellers dataset into PostgreSQL.
"""

from __future__ import annotations

import pandas as pd

from app.core.config import RAW_DATA_DIR
from app.core.logger import get_logger
from app.database.session import get_database_connection
from app.etl.batch_writer import BatchWriter
from app.etl.csv_loader import CSVLoader
from app.etl.validators import DataValidator

logger = get_logger(__name__)


class SellersLoader(CSVLoader):
    """
    ETL loader for the sellers dataset.
    """

    def __init__(self) -> None:
        """
        Initialize the sellers loader.
        """

        source_file = RAW_DATA_DIR / "olist_sellers_dataset.csv"

        super().__init__(source_file)

    def transform(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Validate and transform the sellers dataset.
        """

        DataValidator.validate_empty_dataframe(dataframe)

        DataValidator.validate_required_columns(
            dataframe,
            [
                "seller_id",
                "seller_zip_code_prefix",
                "seller_city",
                "seller_state",
            ],
        )

        DataValidator.validate_duplicate_rows(dataframe)

        DataValidator.validate_missing_values(dataframe)

        logger.info(
            "Selecting required warehouse columns."
        )

        dataframe = dataframe[
            [
                "seller_id",
                "seller_zip_code_prefix",
                "seller_city",
                "seller_state",
            ]
        ]

        logger.info(
            "Sellers dataset transformation completed."
        )

        return dataframe

    def load(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Load the sellers dataset into PostgreSQL.
        """

        logger.info(
            "Preparing seller records for database insertion."
        )

        records = list(
            dataframe.itertuples(index=False, name=None)
        )

        logger.info(
            "Prepared %d seller records.",
            len(records),
        )

        insert_query = """
            INSERT INTO dim_sellers
            (
                seller_id,
                seller_zip_code_prefix,
                seller_city,
                seller_state
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
            ON CONFLICT (seller_id)
            DO NOTHING;
        """

        with get_database_connection() as connection:

            writer = BatchWriter(connection)

            writer.insert(
                query=insert_query,
                records=records,
            )

        logger.info(
            "Seller data successfully loaded into PostgreSQL."
        )

    def run(self) -> None:
        """
        Execute the sellers ETL pipeline.
        """

        logger.info(
            "Starting Sellers ETL."
        )

        dataframe = self.extract()

        dataframe = self.transform(dataframe)

        self.load(dataframe)

        logger.info(
            "Sellers ETL completed successfully."
        )


def main() -> None:
    """
    Test the sellers loader.
    """

    loader = SellersLoader()

    loader.run()


if __name__ == "__main__":
    main()