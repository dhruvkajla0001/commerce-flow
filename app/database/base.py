"""
Database Base Class

Provides a reusable base class for all database-related components.
"""

from __future__ import annotations

from psycopg import Connection

from app.core.logger import get_logger
from app.database.session import get_database_connection

logger = get_logger(__name__)

class DatabaseBase:
    """
    Base class for all database operations.
    """

    def __init__(self) -> None:
        """
        Initialize the database base class.
        """

        logger.info("DatabaseBase initialized.")

    def get_connection(self) -> Connection:
        """
        Obtain a managed PostgreSQL connection.
        """

        with get_database_connection() as connection:
            return connection    