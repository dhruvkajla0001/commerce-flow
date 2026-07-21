"""
Analytics API Routes
"""

from fastapi import APIRouter, Depends
from psycopg import Connection

from app.api.dependencies import get_db
from app.repositories.analytics_repository import AnalyticsRepository
from app.services.analytics_services import AnalyticsService



router = APIRouter(
    prefix="/analytics",
)


def get_analytics_service(
    db: Connection = Depends(get_db),
) -> AnalyticsService:
    """
    Dependency to create AnalyticsService.
    """
    repository = AnalyticsRepository(db)
    return AnalyticsService(repository)


# ==========================================================
# Revenue Analytics
# ==========================================================

@router.get(
    "/revenue",
    tags=["💰 Revenue Analytics"],
)
def get_revenue(
    service: AnalyticsService = Depends(get_analytics_service),
):
    """
    Get revenue summary.
    """
    return service.get_total_revenue()


@router.get(
    "/monthly-revenue",
    tags=["💰 Revenue Analytics"],
)
def get_monthly_revenue(
    service: AnalyticsService = Depends(get_analytics_service),
):
    """
    Get monthly revenue statistics.
    """
    return service.get_monthly_revenue()


@router.get(
    "/monthly-running-revenue",
    tags=["💰 Revenue Analytics"],
)
def get_monthly_running_revenue(
    service: AnalyticsService = Depends(get_analytics_service),
):
    """
    Get cumulative monthly revenue.
    """
    return service.get_monthly_running_revenue()


@router.get(
    "/month-over-month-growth",
    tags=["💰 Revenue Analytics"],
)
def get_month_over_month_growth(
    service: AnalyticsService = Depends(get_analytics_service),
):
    """
    Get month-over-month revenue growth.
    """
    return service.get_month_over_month_growth()


@router.get(
    "/revenue-pareto",
    tags=["💰 Revenue Analytics"],
)
def get_revenue_pareto(
    service: AnalyticsService = Depends(get_analytics_service),
):
    """
    Get revenue Pareto analysis.
    """
    return service.get_revenue_pareto()


# ==========================================================
# Product Analytics
# ==========================================================

@router.get(
    "/top-products",
    tags=["📦 Product Analytics"],
)
def get_top_products(
    service: AnalyticsService = Depends(get_analytics_service),
):
    """
    Get top-performing products.
    """
    return service.get_top_products()


@router.get(
    "/top-product-category-per-state",
    tags=["📦 Product Analytics"],
)
def get_top_product_category_per_state(
    service: AnalyticsService = Depends(get_analytics_service),
):
    """
    Get top product category for each state.
    """
    return service.get_top_product_category_per_state()


# ==========================================================
# Customer Analytics
# ==========================================================

@router.get(
    "/top-customers",
    tags=["👥 Customer Analytics"],
)

def get_top_customers(
    service: AnalyticsService = Depends(get_analytics_service),
):
    """
    Get top customers by revenue.
    """
    return service.get_top_customers()


@router.get(
    "/customer-segmentation",
    tags=["👥 Customer Analytics"],
)
def get_customer_segmentation(
    service: AnalyticsService = Depends(get_analytics_service),
):
    """
    Get customer segmentation.
    """
    return service.get_customer_segmentation()


# ==========================================================
# Seller Analytics
# ==========================================================

@router.get(
    "/top-sellers",
    tags=["🏪 Seller Analytics"],
)
def get_top_sellers(
    service: AnalyticsService = Depends(get_analytics_service),
):
    """
    Get top-performing sellers.
    """
    return service.get_top_sellers()


# ==========================================================
# Geographic Analytics
# ==========================================================

@router.get(
    "/revenue-by-state",
    tags=["🌍 Geographic Analytics"],
)
def get_revenue_by_state(
    service: AnalyticsService = Depends(get_analytics_service),
):
    """
    Get revenue by customer state.
    """
    return service.get_revenue_by_state()


@router.get(
    "/top-cities",
    tags=["🌍 Geographic Analytics"],
)
def get_top_cities(
    service: AnalyticsService = Depends(get_analytics_service),
):
    """
    Get top cities by revenue.
    """
    return service.get_top_cities()


# ==========================================================
# Operational Analytics
# ==========================================================

@router.get(
    "/order-status",
    tags=["⚙️ Operational Analytics"],
)
def get_order_status(
    service: AnalyticsService = Depends(get_analytics_service),
):
    """
    Get order status distribution.
    """
    return service.get_order_status()


# ==========================================================
# Executive Dashboard
# ==========================================================

@router.get(
    "/dashboard",
    tags=["📊 Dashboard KPIs"],
)
def get_dashboard_kpis(
    service: AnalyticsService = Depends(get_analytics_service),
):
    """
    Get executive dashboard KPIs.
    """
    return service.get_dashboard_kpis()