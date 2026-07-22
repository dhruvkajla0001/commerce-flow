"""
Dashboard Routes

Serves the CommerceFlow Operations Center pages.
"""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from psycopg import Connection

from app.api.dependencies import get_db
from app.repositories.analytics_repository import AnalyticsRepository
from app.services.analytics_services import AnalyticsService
from app.services.dashboard_services import DashboardService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)

templates = Jinja2Templates(directory="app/templates")


def get_dashboard_service(
    db: Connection = Depends(get_db),
) -> DashboardService:
    """
    Dependency to create DashboardService.
    """

    repository = AnalyticsRepository(db)
    analytics_service = AnalyticsService(repository)

    return DashboardService(analytics_service)


@router.get("", response_class=HTMLResponse)
async def dashboard_home(
    request: Request,
    dashboard_service: DashboardService = Depends(get_dashboard_service),
):
    """
    Render the Operations Center homepage.
    """

    dashboard_data = dashboard_service.get_dashboard_data()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            "title": "CommerceFlow Operations Center",
            "dashboard": dashboard_data["kpis"],
            "monthly_revenue": dashboard_data["monthly_revenue"],
            "order_status": dashboard_data["order_status"],
            "top_products": dashboard_data["top_products"],
            "revenue_by_state": dashboard_data["revenue_by_state"],
        },
    )