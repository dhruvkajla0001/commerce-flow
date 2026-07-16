"""
Database Session Manager

Provides a reusable context manager for PostgreSQL connections.
"""

from __future__ import annotations

from contextlib import contextmanager

from psycopg import Connection

from app.core.logger import get_logger
from app.database.connection import DatabaseConnection

logger = get_logger(__name__)

@contextmanager
def get_database_connection() -> Connection:
    """
    Provide a managed PostgreSQL database connection.
    """

    database = DatabaseConnection()

    try:
        connection = database.connect()

        logger.info("Database session started.")

        yield connection

    finally:
        database.disconnect()

        logger.info("Database session closed.")

def main() -> None:
    """
    Test the database session manager.
    """

    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")

            version = cursor.fetchone()

            logger.info("PostgreSQL Version: %s", version[0])


if __name__ == "__main__":
    main()
