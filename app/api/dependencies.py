"""
FastAPI Dependencies

Provides reusable dependencies for API routes.
"""

from collections.abc import Generator

from psycopg import Connection

from app.database.connection import get_database_connection


def get_db() -> Generator[Connection, None, None]:
    """
    FastAPI dependency that provides a PostgreSQL connection.
    """

    conn = get_database_connection()

    try:
        yield conn
    finally:
        conn.close()