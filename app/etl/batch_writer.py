"""
Batch Writer

Provides efficient batch insertion into PostgreSQL.
"""

from __future__ import annotations

from typing import Any

from psycopg import Connection

from app.core.logger import get_logger

logger = get_logger(__name__)


class BatchWriter:
    """
    Utility class for batch database inserts.
    """

    def __init__(
        self,
        connection: Connection,
        batch_size: int = 1000,
    ) -> None:
        """
        Initialize the batch writer.
        """

        self.connection = connection
        self.batch_size = batch_size

        logger.info(
            "BatchWriter initialized (batch size=%d).",
            self.batch_size,
        )

    def insert(
        self,
        query: str,
        records: list[tuple[Any, ...]],
    ) -> None:
        """
        Insert records into PostgreSQL in batches.
        """

        if not records:
            logger.warning("No records to insert.")
            return

        try:
            with self.connection.cursor() as cursor:

                for index in range(
                    0,
                    len(records),
                    self.batch_size,
                ):
                    batch = records[
                        index:index + self.batch_size
                    ]

                    cursor.executemany(
                        query,
                        batch,
                    )

                    logger.info(
                        "Inserted batch %d-%d.",
                        index + 1,
                        index + len(batch),
                    )

            self.connection.commit()

            logger.info(
                "Successfully inserted %d records.",
                len(records),
            )

        except Exception:

            self.connection.rollback()

            logger.exception(
                "Batch insert failed."
            )

            raise