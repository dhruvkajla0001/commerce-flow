from fastapi import APIRouter, Depends
from psycopg import Connection

from app.api.dependencies import get_db

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check(
    db: Connection = Depends(get_db),
):
    with db.cursor() as cursor:
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]

    return {
        "status": "healthy",
        "database": "connected",
        "postgres_version": version,
    }