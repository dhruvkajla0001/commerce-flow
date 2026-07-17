"""
Products Dataset Loader

Loads the Olist products dataset into PostgreSQL.
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


class ProductsLoader(CSVLoader):
    """
    ETL loader for the products dataset.
    """

    def __init__(self) -> None:
        """
        Initialize the products loader.
        """

        source_file = RAW_DATA_DIR / "olist_products_dataset.csv"

        super().__init__(source_file)

    def transform(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Validate and transform the products dataset.
        """

        DataValidator.validate_empty_dataframe(dataframe)

        DataValidator.validate_required_columns(
            dataframe,
            [
                "product_id",
                "product_category_name",
                "product_name_lenght",
                "product_description_lenght",
                "product_photos_qty",
                "product_weight_g",
                "product_length_cm",
                "product_height_cm",
                "product_width_cm",
            ],
        )

        DataValidator.validate_duplicate_rows(dataframe)

        DataValidator.validate_missing_values(dataframe)

        logger.info("Selecting required warehouse columns.")

        dataframe = dataframe[
            [
                "product_id",
                "product_category_name",
                "product_name_lenght",
                "product_description_lenght",
                "product_photos_qty",
                "product_weight_g",
                "product_length_cm",
                "product_height_cm",
                "product_width_cm",
            ]
        ]

        logger.info("Products dataset transformation completed.")

        print(dataframe["product_name_lenght"].max())
        print(dataframe["product_description_lenght"].max())
        print(dataframe["product_photos_qty"].max())
        print(dataframe["product_weight_g"].max())
        print(dataframe["product_length_cm"].max())
        print(dataframe["product_height_cm"].max())
        print(dataframe["product_width_cm"].max())

        print(dataframe.dtypes)

        return dataframe

    def load(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Load the products dataset into PostgreSQL.
        """

        logger.info(
            "Preparing product records for database insertion."
        )

        records = list(
            dataframe.itertuples(index=False, name=None)
        )

        logger.info(
            "Prepared %d product records.",
            len(records),
        )

        insert_query = """
            INSERT INTO dim_products
            (
                product_id,
                product_category_name,
                product_name_length,
                product_description_length,
                product_photos_qty,
                product_weight_g,
                product_length_cm,
                product_height_cm,
                product_width_cm
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            ON CONFLICT (product_id)
            DO NOTHING;
        """

        with get_database_connection() as connection:

            writer = BatchWriter(connection)

            writer.insert(
                query=insert_query,
                records=records,
            )

        logger.info(
            "Product data successfully loaded into PostgreSQL."
        )

    def run(self) -> None:
        """
        Execute the products ETL pipeline.
        """

        logger.info("Starting Products ETL.")

        dataframe = self.extract()

        dataframe = self.transform(dataframe)

        self.load(dataframe)

        logger.info("Products ETL completed successfully.")


def main() -> None:
    """
    Test the products loader.
    """

    loader = ProductsLoader()

    loader.run()


if __name__ == "__main__":
    main()