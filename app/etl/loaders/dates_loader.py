"""
Date Dimension Loader

Generates and loads the date dimension into PostgreSQL.
"""

from __future__ import annotations

import pandas as pd

from app.core.logger import get_logger
from app.database.session import get_database_connection
from app.etl.batch_writer import BatchWriter

logger = get_logger(__name__)


class DatesLoader:
    """
    ETL loader for the date dimension.
    """

    def __init__(
        self,
        start_date: str = "2016-01-01",
        end_date: str = "2019-12-31",
    ) -> None:
        """
        Initialize the date loader.
        """

        self.start_date = start_date
        self.end_date = end_date

    def generate(self) -> pd.DataFrame:
        """
        Generate the calendar dimension.
        """

        logger.info(
            "Generating calendar dimension from %s to %s.",
            self.start_date,
            self.end_date,
        )

        dates = pd.date_range(
            start=self.start_date,
            end=self.end_date,
            freq="D",
        )

        dataframe = pd.DataFrame()

        dataframe["full_date"] = dates

        dataframe["date_key"] = (
            dataframe["full_date"]
            .dt.strftime("%Y%m%d")
            .astype(int)
        )

        dataframe["day"] = dataframe["full_date"].dt.day

        dataframe["month"] = dataframe["full_date"].dt.month

        dataframe["month_name"] = (
            dataframe["full_date"]
            .dt.month_name()
        )

        dataframe["quarter"] = (
            dataframe["full_date"]
            .dt.quarter
        )

        dataframe["year"] = (
            dataframe["full_date"]
            .dt.year
        )

        dataframe["week_of_year"] = (
            dataframe["full_date"]
            .dt.isocalendar()
            .week
            .astype(int)
        )

        dataframe["day_of_week"] = (
            dataframe["full_date"]
            .dt.weekday + 1
        )

        dataframe["day_name"] = (
            dataframe["full_date"]
            .dt.day_name()
        )

        dataframe["is_weekend"] = (
            dataframe["day_of_week"] >= 6
        )

        dataframe["full_date"] = (
            dataframe["full_date"]
            .dt.date
        )

        logger.info(
            "Generated %d calendar records.",
            len(dataframe),
        )

        return dataframe

    def load(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Load the date dimension into PostgreSQL.
        """

        logger.info(
            "Preparing date records for insertion."
        )

        # Reorder columns to match the INSERT statement
        dataframe = dataframe[
            [
                "date_key",
                "full_date",
                "day",
                "month",
                "month_name",
                "quarter",
                "year",
                "week_of_year",
                "day_of_week",
                "day_name",
                "is_weekend",
            ]
        ]

        print(dataframe.columns.tolist())
        print(dataframe.iloc[0])

        records = list(
            dataframe.itertuples(index=False, name=None)
        )

        logger.info(
            "Prepared %d date records.",
            len(records),
        )

        insert_query = """
            INSERT INTO dim_dates
            (
                date_key,
                full_date,
                day,
                month,
                month_name,
                quarter,
                year,
                week_of_year,
                day_of_week,
                day_name,
                is_weekend
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
            ON CONFLICT (date_key)
            DO NOTHING;
        """

        with get_database_connection() as connection:

            writer = BatchWriter(connection)

            writer.insert(
                query=insert_query,
                records=records,
            )

        logger.info(
            "Date dimension loaded successfully."
        )

    def run(self) -> None:
        """
        Execute the date dimension ETL.
        """

        logger.info(
            "Starting Date Dimension ETL."
        )

        dataframe = self.generate()

        self.load(dataframe)

        logger.info(
            "Date Dimension ETL completed successfully."
        )


def main() -> None:
    """
    Test the date loader.
    """

    loader = DatesLoader()

    loader.run()


if __name__ == "__main__":
    main()