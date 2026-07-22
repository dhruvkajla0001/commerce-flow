"""
Dashboard Service

Provides all data required by the Operations Center dashboard.
"""

from app.services.analytics_services import AnalyticsService
from app.repositories.analytics_repository import AnalyticsRepository


class DashboardService:

    def __init__(self, analytics_service):
        self.analytics = analytics_service

    def get_dashboard_data(self):

        kpis = self.analytics.get_dashboard_kpis()

        monthly_revenue = self.analytics.get_monthly_revenue()

        return {
            "kpis": kpis,
            "monthly_revenue": monthly_revenue,
            "order_status": self.analytics.get_order_status(),
            "top_products": self.analytics.get_top_products(),
            "revenue_by_state": self.analytics.get_revenue_by_state()
        }