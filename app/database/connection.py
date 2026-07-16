"""
PostgreSQL Connection Manager

Provides a reusable database connection for the entire application.
"""

from __future__ import annotations

from typing import Optional

import psycopg
from psycopg import Connection

from app.core.config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)

from app.core.logger import get_logger

logger = get_logger(__name__)


class DatabaseConnection:
    """
    PostgreSQL database connection manager.
    """

    """
    PostgreSQL database connection manager.
    """

    def __init__(self) -> None:
        """
        Initialize database configuration.
        """

        self.host: str = DB_HOST
        self.port: int = DB_PORT
        self.database: str = DB_NAME
        self.user: str = DB_USER
        self.password: str = DB_PASSWORD

        self.connection: Optional[Connection] = None

        logger.info(
            "DatabaseConnection initialized for database '%s'.",
            self.database,
        )

    def connect(self) -> Connection:
        """
        Establish a connection to PostgreSQL.
        """

        try:
            logger.info(
                "Connecting to PostgreSQL database '%s'...",
                self.database,
            )

            self.connection = psycopg.connect(
                host=self.host,
                port=self.port,
                dbname=self.database,
                user=self.user,
                password=self.password,
            )

            logger.info("Database connection established successfully.")

            return self.connection

        except Exception:
            logger.exception("Failed to connect to PostgreSQL.")
            raise

    def disconnect(self) -> None:
        """
        Close the active database connection.
        """

        if self.connection is not None:
            self.connection.close()

            logger.info("Database connection closed successfully.")

            self.connection = None

        else:
            logger.warning("No active database connection to close.")

    def health_check(self) -> bool:
        """
        Verify that the database connection is healthy.
        """

        try:
            if self.connection is None:
                logger.warning("No active database connection.")
                return False

            with self.connection.cursor() as cursor:
                cursor.execute("SELECT 1;")
                cursor.fetchone()

            logger.info("Database health check passed.")

            return True

        except Exception:
            logger.exception("Database health check failed.")
            return False

def main() -> None:
    """
    Test the database connection.
    """
    database = DatabaseConnection()
    database.connect()
    database.health_check()
    database.disconnect()


if __name__ == "__main__":
    main()
