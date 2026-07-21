"""
Analytics Service

Business logic for analytics.
"""

from app.repositories.analytics_repository import AnalyticsRepository


class AnalyticsService:
    """
    Service layer for analytics.
    """

    def __init__(self, repository: AnalyticsRepository):
        self.repository = repository

    # ==========================================================
    # Revenue Analytics
    # ==========================================================

    def get_total_revenue(self) -> dict:
        """
        Get revenue statistics.
        """

        return self.repository.get_total_revenue()

    def get_monthly_revenue(self) -> list[dict]:
        """
        Get monthly revenue statistics.
        """

        return self.repository.get_monthly_revenue()

    def get_monthly_running_revenue(self) -> list[dict]:
        """
        Get cumulative monthly revenue.
        """

        return self.repository.get_monthly_running_revenue()

    def get_month_over_month_growth(self) -> list[dict]:
        """
        Get month-over-month revenue growth.
        """

        return self.repository.get_month_over_month_growth()

    def get_revenue_pareto(self) -> list[dict]:
        """
        Get Pareto analysis of revenue contribution.
        """

        return self.repository.get_revenue_pareto()

    # ==========================================================
    # Product Analytics
    # ==========================================================

    def get_top_products(self) -> list[dict]:
        """
        Get top-performing product categories.
        """

        return self.repository.get_top_products()

    def get_top_product_category_per_state(self) -> list[dict]:
        """
        Get top product category for each state.
        """

        return self.repository.get_top_product_category_per_state()

    # ==========================================================
    # Customer Analytics
    # ==========================================================

    def get_top_customers(self) -> list[dict]:
        """
        Get top customers by revenue.
        """

        return self.repository.get_top_customers()

    def get_customer_segmentation(self) -> list[dict]:
        """
        Get customer segmentation.
        """

        return self.repository.get_customer_segmentation()

    # ==========================================================
    # Seller Analytics
    # ==========================================================

    def get_top_sellers(self) -> list[dict]:
        """
        Get top-performing sellers.
        """

        return self.repository.get_top_sellers()

    # ==========================================================
    # Geographic Analytics
    # ==========================================================

    def get_revenue_by_state(self) -> list[dict]:
        """
        Get revenue grouped by state.
        """

        return self.repository.get_revenue_by_state()

    def get_top_cities(self) -> list[dict]:
        """
        Get top cities by revenue.
        """

        return self.repository.get_top_cities()

    # ==========================================================
    # Operational Analytics
    # ==========================================================

    def get_order_status(self) -> list[dict]:
        """
        Get order status distribution.
        """

        return self.repository.get_order_status()

    # ==========================================================
    # Executive Dashboard
    # ==========================================================

    def get_dashboard_kpis(self) -> dict:
        """
        Get executive dashboard KPIs.
        """

        return self.repository.get_dashboard_kpis()