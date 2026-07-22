"""
CommerceFlow FastAPI Application

Main application entry point.
"""

from fastapi import FastAPI

from app.api.routes.analytics import router as analytics_router
from app.api.routes.health import router as health_router
from app.api.routes.dashboard import router as dashboard_router
from fastapi.staticfiles import StaticFiles

# ==========================================================
# OpenAPI Tags Metadata
# ==========================================================

tags_metadata = [
    {
        "name": "System",
        "description": "System information and API entry point.",
    },
    {
        "name": "Health",
        "description": "Health monitoring endpoints used for application readiness and database connectivity checks.",
    },
    {
        "name": "Revenue Analytics",
        "description": """
Business revenue analytics including:

- Overall Revenue KPIs
- Monthly Revenue
- Running Revenue
- Month-over-Month Growth
- Revenue Pareto Analysis
""",
    },
    {
        "name": "Product Analytics",
        "description": """
Product performance analytics.

Includes top-performing product categories and
highest revenue-generating categories by state.
""",
    },
    {
        "name": "Customer Analytics",
        "description": """
Customer-focused business intelligence.

Includes customer rankings and spending segmentation.
""",
    },
    {
        "name": "Seller Analytics",
        "description": """
Seller performance metrics.

Identify the highest revenue-generating sellers.
""",
    },
    {
        "name": "Geographic Analytics",
        "description": """
Revenue distribution across states and cities.

Useful for regional business analysis.
""",
    },
    {
        "name": "Operational Analytics",
        "description": """
Operational KPIs including order lifecycle and status distribution.
""",
    },
    {
        "name": "Dashboard KPIs",
        "description": """
Executive-level dashboard metrics combining the most important
business KPIs into a single endpoint.
""",
    },
]

# ==========================================================
# FastAPI Application
# ==========================================================

app = FastAPI(
    title="CommerceFlow API",
    summary="Production-inspired Business Intelligence & Analytics API",
    description="""
# CommerceFlow API

CommerceFlow is a production-inspired **Data Engineering** project that demonstrates
how modern analytics platforms expose business intelligence through REST APIs.

---

## Project Highlights

- Production-inspired FastAPI architecture
- PostgreSQL Data Warehouse
- Apache Airflow Orchestration
- SQL Analytics Layer
- Repository-Service Pattern
- Dockerized Infrastructure
- Business Intelligence APIs

---

## Analytics Categories

- Revenue Analytics
- Product Analytics
- Customer Analytics
- Seller Analytics
- Geographic Analytics
- Operational Analytics
- Dashboard KPIs

---

## Technology Stack

- Python
- FastAPI
- PostgreSQL
- Apache Airflow
- Docker
- SQL

---

## Architecture

Client

↓

FastAPI Routes

↓

Service Layer

↓

Repository Layer

↓

PostgreSQL Data Warehouse

---

Built as a portfolio project to demonstrate production-ready
backend engineering and data engineering practices.
""",
    version="1.0.0",
    contact={
        "name": "Dhruv Kajla",
        "url": "https://github.com/dhruvkajla0001",
    },
    license_info={
        "name": "MIT License",
    },
    openapi_tags=tags_metadata,
    servers=[
        {
            "url": "http://127.0.0.1:8000",
            "description": "Local Development Server",
        }
    ],
)

# ==========================================================
# Static Files
# ==========================================================

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)

# ==========================================================
# Register API Routers
# ==========================================================

app.include_router(health_router)
app.include_router(analytics_router)
app.include_router(dashboard_router)

# ==========================================================
# Root Endpoint
# ==========================================================


@app.get(
    "/",
    tags=["System"],
    summary="API Information",
    description="Returns basic information about the CommerceFlow API.",
)
def root():
    """
    Root endpoint.
    """

    return {
        "application": "CommerceFlow API",
        "version": "1.0.0",
        "status": "running",
        "documentation": "/docs",
        "redoc": "/redoc",
    }