"""
Fact Orders Loader

Builds and loads the fact_orders table by combining
multiple Olist datasets.
"""

from __future__ import annotations

import pandas as pd

from app.core.config import RAW_DATA_DIR
from app.core.logger import get_logger
from app.database.session import get_database_connection
from app.etl.batch_writer import BatchWriter

logger = get_logger(__name__)


class FactOrdersLoader:
    """
    ETL loader for the fact_orders table.
    """

    def __init__(self) -> None:
        """
        Initialize source dataset locations.
        """

        self.orders_file = (
            RAW_DATA_DIR
            / "olist_orders_dataset.csv"
        )

        self.order_items_file = (
            RAW_DATA_DIR
            / "olist_order_items_dataset.csv"
        )

        self.payments_file = (
            RAW_DATA_DIR
            / "olist_order_payments_dataset.csv"
        )

        self.reviews_file = (
            RAW_DATA_DIR
            / "olist_order_reviews_dataset.csv"
        )

    def extract(
        self,
    ) -> tuple[
        pd.DataFrame,
        pd.DataFrame,
        pd.DataFrame,
        pd.DataFrame,
    ]:
        """
        Extract all required datasets.
        """

        logger.info(
            "Extracting Olist datasets."
        )

        orders_df = pd.read_csv(
            self.orders_file,
        )

        order_items_df = pd.read_csv(
            self.order_items_file,
        )

        payments_df = pd.read_csv(
            self.payments_file,
        )

        reviews_df = pd.read_csv(
            self.reviews_file,
        )

        logger.info(
            "Orders dataset: %d rows, %d columns.",
            *orders_df.shape,
        )

        logger.info(
            "Order Items dataset: %d rows, %d columns.",
            *order_items_df.shape,
        )

        logger.info(
            "Payments dataset: %d rows, %d columns.",
            *payments_df.shape,
        )

        logger.info(
            "Reviews dataset: %d rows, %d columns.",
            *reviews_df.shape,
        )

        return (
            orders_df,
            order_items_df,
            payments_df,
            reviews_df,
        )

    def build_lookup_tables(
        self,
    ) -> tuple[
        dict[str, int],
        dict[str, int],
        dict[str, int],
        dict,
    ]:
        """
        Build lookup tables for dimension tables.
        """

        logger.info(
            "Building lookup tables."
        )

        with get_database_connection() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT
                        customer_id,
                        customer_key
                    FROM dim_customers;
                    """
                )

                customer_rows = cursor.fetchall()
                customer_lookup = {
                    customer_id: customer_key
                    for customer_id, customer_key in customer_rows
                }

                logger.info(
                    "Customer lookup contains %d records.",
                    len(customer_lookup),
                )

                cursor.execute(
                    """
                    SELECT
                        product_id,
                        product_key
                    FROM dim_products;
                    """
                )

                product_rows = cursor.fetchall()

                product_lookup = {
                    product_id: product_key
                    for product_id, product_key in product_rows
                }

                logger.info(
                    "Product lookup contains %d records.",
                    len(product_lookup),
                )

                cursor.execute(
                    """
                    SELECT
                        seller_id,
                        seller_key
                    FROM dim_sellers;
                    """
                )

                seller_rows = cursor.fetchall()

                seller_lookup = {
                    seller_id: seller_key
                    for seller_id, seller_key in seller_rows
                }

                logger.info(
                    "Seller lookup contains %d records.",
                    len(seller_lookup),
                )

                cursor.execute(
                    """
                    SELECT
                        full_date,
                        date_key
                    FROM dim_dates;
                    """
                )

                date_rows = cursor.fetchall()

                date_lookup = {
                    full_date: date_key
                    for full_date, date_key in date_rows
                }

                logger.info(
                    "Date lookup contains %d records.",
                    len(date_lookup),
                )

        return (
            customer_lookup,
            product_lookup,
            seller_lookup,
            date_lookup,
        )        

    def transform(
        self,
        orders_df: pd.DataFrame,
        order_items_df: pd.DataFrame,
        payments_df: pd.DataFrame,
        reviews_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Merge Olist datasets into a single dataframe.
        """

        (
            customer_lookup,
            product_lookup,
            seller_lookup,
            date_lookup,
        ) = self.build_lookup_tables()

        logger.info(
            "Merging orders and order items."
        )

        dataframe = orders_df.merge(
            order_items_df,
            on="order_id",
            how="inner",
        )

        logger.info(
            "Rows after orders + items: %d",
            len(dataframe),
        )

        logger.info(
            "Aggregating payments."
        )

        payments_df = (
            payments_df
            .groupby(
                "order_id",
                as_index=False,
            )
            .agg(
                {
                    "payment_value": "sum",
                }
            )
        )

        logger.info(
            "Aggregated payments: %d rows.",
            len(payments_df),
        )

        logger.info(
            "Merging aggregated payments."
        )

        dataframe = dataframe.merge(
            payments_df,
            on="order_id",
            how="left",
        )

        logger.info(
            "Rows after payments: %d",
            len(dataframe),
        )

        logger.info(
            "Aggregating reviews."
        )

        reviews_df = (
            reviews_df
            .sort_values("review_creation_date")
            .drop_duplicates(
                subset="order_id",
                keep="first",
            )
        )

        logger.info(
            "Aggregated reviews: %d rows.",
            len(reviews_df),
        )

        logger.info(
            "Merging aggregated reviews."
        )

        dataframe = dataframe.merge(
            reviews_df[
                [
                    "order_id",
                    "review_score",
                ]
            ],
            on="order_id",
            how="left",
        )

        logger.info(
            "Rows after reviews: %d",
            len(dataframe),
        )

        logger.info(
            "Generating customer surrogate keys."
        )

        dataframe["customer_key"] = (
            dataframe["customer_id"]
            .map(customer_lookup)
        )

        logger.info(
            "Customer surrogate keys generated."
        )

        logger.info(
            "Generating product surrogate keys."
        )

        dataframe["product_key"] = (
            dataframe["product_id"]
            .map(product_lookup)
        )

        logger.info(
            "Product surrogate keys generated."
        )

        logger.info(
            "Generating seller surrogate keys."
        )

        dataframe["seller_key"] = (
            dataframe["seller_id"]
            .map(seller_lookup)
        )

        logger.info(
            "Seller surrogate keys generated."
        )

        logger.info(
            "Generating date surrogate keys."
        )

        dataframe["purchase_date"] = (
            pd.to_datetime(
                dataframe["order_purchase_timestamp"]
            ).dt.date
        )

        dataframe["date_key"] = (
            dataframe["purchase_date"]
            .map(date_lookup)
        )

        logger.info(
            "Date surrogate keys generated."
        )

        logger.info(
            "Missing customer keys: %d",
            dataframe["customer_key"].isna().sum(),
        )

        logger.info(
            "Missing product keys: %d",
            dataframe["product_key"].isna().sum(),
        )

        logger.info(
            "Missing seller keys: %d",
            dataframe["seller_key"].isna().sum(),
        )

        logger.info(
            "Missing date keys: %d",
            dataframe["date_key"].isna().sum(),
        )

        logger.info(
            "Selecting warehouse fact columns."
        )

        dataframe = dataframe[
        [
            "order_id",
            "order_item_id",
            "customer_key",
            "product_key",
            "seller_key",
            "date_key",
            "order_status",
            "price",
            "freight_value",
            "payment_value",
            "review_score",
        ]
        ]

        logger.info(
            "Warehouse fact table contains %d rows and %d columns.",
            *dataframe.shape,
        )

        duplicates = dataframe.duplicated(
            subset=[
                "order_id",
                "order_item_id",
            ]
        ).sum()

        logger.info(
            "Duplicate (order_id, order_item_id): %d",
            duplicates,
        )

        return dataframe

    def load(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Load the fact_orders table.
        """

        logger.info(
            "Preparing fact records for database insertion."
        )

        records = list(
            dataframe.itertuples(
                index=False,
                name=None,
            )
        )

        logger.info(
            "Prepared %d fact records.",
            len(records),
        )

        insert_query = """
            INSERT INTO fact_orders
            (
                order_id,
                order_item_id,
                customer_key,
                product_key,
                seller_key,
                date_key,
                order_status,
                price,
                freight_value,
                payment_value,
                review_score
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
                %s,
                %s,
                %s
            )
            ON CONFLICT
            (
                order_id,
                order_item_id
            )
            DO NOTHING;
        """

        with get_database_connection() as connection:

            writer = BatchWriter(connection)

            writer.insert(
                query=insert_query,
                records=records,
            )

        logger.info(
            "Fact orders loaded successfully."
        )

    def run(
        self,
    ) -> None:
        """
        Execute the fact_orders ETL pipeline.
        """

        logger.info(
            "Starting Fact Orders ETL."
        )

        (
            orders_df,
            order_items_df,
            payments_df,
            reviews_df,
        ) = self.extract()

        fact_dataframe = self.transform(
            orders_df,
            order_items_df,
            payments_df,
            reviews_df,
        )

        self.load(
            fact_dataframe,
        )

        logger.info(
            "Fact Orders ETL completed successfully."
        )


def main() -> None:
    """
    Run the fact_orders loader.
    """

    loader = FactOrdersLoader()

    loader.run()


if __name__ == "__main__":
    main()