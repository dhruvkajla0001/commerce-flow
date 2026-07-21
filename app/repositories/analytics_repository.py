"""
Analytics Repository

Handles analytics-related database queries.
"""

from psycopg import Connection


class AnalyticsRepository:
    """
    Repository for analytics queries.
    """

    def __init__(self, connection: Connection):
        self.connection = connection


    # ==========================================================
    # Revenue Analytics
    # ==========================================================

    def get_total_revenue(self) -> dict:
        """
        Return total revenue statistics.
        """

        query = """
            SELECT
                COUNT(*) AS total_order_items,
                ROUND(SUM(payment_value), 2) AS total_revenue,
                ROUND(AVG(payment_value), 2) AS average_payment,
                ROUND(MAX(payment_value), 2) AS highest_payment,
                ROUND(MIN(payment_value), 2) AS lowest_payment
            FROM public.fact_orders;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query)

            row = cursor.fetchone()

        return {
            "total_orders": row[0],
            "total_revenue": float(row[1]),
            "average_payment": float(row[2]),
            "highest_payment": float(row[3]),
            "lowest_payment": float(row[4]),
        }


    def get_monthly_revenue(self) -> list[dict]:
        """
        Return monthly revenue statistics.
        """

        query = """
            SELECT
                d.year,
                d.month,
                d.month_name,

                COUNT(*) AS total_order_items,

                ROUND(SUM(f.payment_value), 2) AS monthly_revenue,

                ROUND(AVG(f.payment_value), 2) AS average_payment

            FROM public.fact_orders AS f

            INNER JOIN public.dim_dates AS d
                ON f.date_key = d.date_key

            GROUP BY
                d.year,
                d.month,
                d.month_name

            ORDER BY
                d.year,
                d.month;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query)

            rows = cursor.fetchall()

        return [
            {
                "year": row[0],
                "month": row[1],
                "month_name": row[2],
                "total_orders": row[3],
                "monthly_revenue": float(row[4]),
                "average_payment": float(row[5]),
            }
            for row in rows
        ]


    def get_monthly_running_revenue(self) -> list[dict]:
        """
        Return cumulative monthly revenue.
        """

        query = """
            WITH monthly_revenue AS (

                SELECT

                    d.year,

                    d.month,

                    d.month_name,

                    ROUND(SUM(f.payment_value), 2) AS monthly_revenue

                FROM public.fact_orders AS f

                INNER JOIN public.dim_dates AS d
                    ON f.date_key = d.date_key

                GROUP BY

                    d.year,
                    d.month,
                    d.month_name

            )

            SELECT

                year,

                month,

                month_name,

                monthly_revenue,

                ROUND(

                    SUM(monthly_revenue)

                    OVER (

                        ORDER BY year, month

                    ),

                    2

                ) AS running_revenue

            FROM monthly_revenue

            ORDER BY

                year,
                month;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query)

            rows = cursor.fetchall()

        return [
            {
                "year": row[0],
                "month": row[1],
                "monthly_revenue": float(row[2]),
                "running_revenue": float(row[3]),
            }
            for row in rows
        ]


    def get_month_over_month_growth(self) -> list[dict]:
        """
        Return month-over-month revenue growth.
        """

        query = """
            WITH monthly_revenue AS (

                SELECT

                    d.year,
                    d.month,
                    d.month_name,

                    ROUND(SUM(f.payment_value),2) AS monthly_revenue

                FROM public.fact_orders AS f

                INNER JOIN public.dim_dates AS d
                    ON f.date_key = d.date_key

                GROUP BY
                    d.year,
                    d.month,
                    d.month_name

            ),

            monthly_growth AS (

                SELECT

                    year,
                    month,
                    month_name,
                    monthly_revenue,

                    LAG(monthly_revenue)
                    OVER(
                        ORDER BY year, month
                    ) AS previous_month_revenue

                FROM monthly_revenue

            )

            SELECT

                year,

                month,

                month_name,

                monthly_revenue,

                previous_month_revenue,

                ROUND(
                    monthly_revenue - previous_month_revenue,
                    2
                ) AS revenue_difference,

                ROUND(

                    CASE

                        WHEN previous_month_revenue IS NULL THEN NULL

                        WHEN previous_month_revenue = 0 THEN NULL

                        ELSE
                            (
                                (monthly_revenue - previous_month_revenue)
                                / previous_month_revenue
                            ) * 100

                    END,

                    2

                ) AS mom_growth_percentage

            FROM monthly_growth

            ORDER BY
                year,
                month;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query)

            rows = cursor.fetchall()

        return [
            {
                "year": row[0],
                "month": row[1],
                "monthly_revenue": float(row[2]),
                "previous_month_revenue": float(row[3]) if row[3] is not None else None,
                "growth_percentage": float(row[4]) if row[4] is not None else None,
            }
            for row in rows
        ]


    def get_revenue_pareto(self) -> list[dict]:
        """
        Return revenue contribution Pareto analysis.
        """

        query = """
            WITH customer_revenue AS (

                SELECT

                    c.customer_unique_id,

                    ROUND(SUM(f.payment_value),2) AS total_spent

                FROM public.fact_orders AS f

                INNER JOIN public.dim_customers AS c
                    ON f.customer_key = c.customer_key

                GROUP BY
                    c.customer_unique_id

            ),

            revenue_analysis AS (

                SELECT

                    customer_unique_id,

                    total_spent,

                    ROUND(
                        (total_spent /
                        SUM(total_spent) OVER()) * 100,
                        4
                    ) AS revenue_percentage,

                    ROUND(
                        SUM(total_spent)
                        OVER(
                            ORDER BY total_spent DESC
                        ),
                        2
                    ) AS cumulative_revenue

                FROM customer_revenue

            )

            SELECT

                customer_unique_id,

                total_spent,

                revenue_percentage,

                cumulative_revenue,

                ROUND(
                    (cumulative_revenue /
                    MAX(cumulative_revenue) OVER()) * 100,
                    2
                ) AS cumulative_percentage

            FROM revenue_analysis

            ORDER BY total_spent DESC;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query)

            rows = cursor.fetchall()

        return [
            {
                "product_category": row[0],
                "category_revenue": float(row[1]),
                "cumulative_revenue": float(row[2]),
                "cumulative_percentage": float(row[3]),
            }
            for row in rows
        ]
    
    # ==========================================================
    # Product Analytics
    # ==========================================================

    def get_top_products(self) -> list[dict]:
        """
        Return top-performing product categories by revenue.
        """

        query = """
            SELECT
                ROW_NUMBER() OVER (
                    ORDER BY SUM(f.payment_value) DESC
                ) AS revenue_rank,

                p.product_category_name,

                COUNT(*) AS total_order_items,

                ROUND(SUM(f.payment_value), 2) AS total_revenue,

                ROUND(AVG(f.payment_value), 2) AS average_payment

            FROM public.fact_orders AS f

            INNER JOIN public.dim_products AS p
                ON f.product_key = p.product_key

            GROUP BY
                p.product_category_name

            ORDER BY
                total_revenue DESC

            LIMIT 10;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query)

            rows = cursor.fetchall()

        return [
            {
                "product_category": row[0],
                "total_order_items": row[1],
                "total_revenue": float(row[2]),
                "average_payment": float(row[3]),
            }
            for row in rows
        ]


    def get_top_product_category_per_state(self) -> list[dict]:
        """
        Return the highest revenue-generating product category for each state.
        """

        query = """
            WITH state_category_revenue AS (

                SELECT

                    c.customer_state,

                    p.product_category_name,

                    ROUND(SUM(f.payment_value),2) AS total_revenue

                FROM public.fact_orders AS f

                INNER JOIN public.dim_customers AS c
                    ON f.customer_key = c.customer_key

                INNER JOIN public.dim_products AS p
                    ON f.product_key = p.product_key

                GROUP BY

                    c.customer_state,
                    p.product_category_name

            ),

            ranked_categories AS (

                SELECT

                    customer_state,

                    product_category_name,

                    total_revenue,

                    ROW_NUMBER() OVER(

                        PARTITION BY customer_state

                        ORDER BY total_revenue DESC

                    ) AS rank

                FROM state_category_revenue

            )

            SELECT

                customer_state,

                product_category_name,

                total_revenue

            FROM ranked_categories

            WHERE rank = 1

            ORDER BY total_revenue DESC;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query)

            rows = cursor.fetchall()

        return [
            {
                "customer_state": row[0],
                "product_category": row[1],
                "total_revenue": float(row[2]),
                "rank": row[3],
            }
            for row in rows
        ]
    
    # ==========================================================
    # Customer Analytics
    # ==========================================================

    def get_top_customers(self) -> list[dict]:
        """
        Return top customers by total revenue.
        """

        query = """
            SELECT
                c.customer_unique_id,
                c.customer_city,
                c.customer_state,

                COUNT(*) AS total_order_items,

                ROUND(COALESCE(SUM(f.payment_value), 0), 2) AS total_revenue,
                ROUND(COALESCE(AVG(f.payment_value), 0), 2) AS average_payment

            FROM public.fact_orders AS f

            INNER JOIN public.dim_customers AS c
                ON f.customer_key = c.customer_key

            GROUP BY
                c.customer_unique_id,
                c.customer_city,
                c.customer_state

            ORDER BY
                total_revenue DESC

            LIMIT 10;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query)

            rows = cursor.fetchall()

        return [
            {
                "customer_id": row[0],
                "customer_city": row[1],
                "customer_state": row[2],
                "total_orders": row[3],
                "total_revenue": float(row[4]),
            }
            for row in rows
        ]


    def get_customer_segmentation(self) -> list[dict]:
        """
        Return customer segmentation based on spending.
        """

        query = """
            WITH customer_spending AS (

                SELECT

                    c.customer_unique_id,

                    c.customer_state,

                    ROUND(SUM(f.payment_value),2) AS total_spent

                FROM public.fact_orders AS f

                INNER JOIN public.dim_customers AS c
                    ON f.customer_key = c.customer_key

                GROUP BY

                    c.customer_unique_id,
                    c.customer_state

            ),

            customer_segments AS (

                SELECT

                    customer_unique_id,

                    customer_state,

                    total_spent,

                    CASE

                        WHEN total_spent >= 5000 THEN 'Platinum'

                        WHEN total_spent >= 2000 THEN 'Gold'

                        WHEN total_spent >= 1000 THEN 'Silver'

                        ELSE 'Bronze'

                    END AS customer_segment

                FROM customer_spending

            )

            SELECT

                customer_segment,

                COUNT(*) AS total_customers,

                ROUND(SUM(total_spent),2) AS total_revenue,

                ROUND(AVG(total_spent),2) AS average_customer_value

            FROM customer_segments

            GROUP BY customer_segment

            ORDER BY total_revenue DESC;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query)

            rows = cursor.fetchall()

        return [
            {
                "customer_segment": row[0],
                "customer_count": row[1],
                "total_revenue": float(row[2]),
                "average_revenue": float(row[3]),
            }
            for row in rows
        ]
    
    # ==========================================================
    # Seller Analytics
    # ==========================================================

    def get_top_sellers(self) -> list[dict]:
        """
        Return top-performing sellers by revenue.
        """

        query = """
            SELECT
                s.seller_id,
                s.seller_city,
                s.seller_state,

                COUNT(*) AS total_order_items,

                ROUND(COALESCE(SUM(f.payment_value), 0), 2) AS total_revenue,

                ROUND(COALESCE(AVG(f.payment_value), 0), 2) AS average_payment

            FROM public.fact_orders AS f

            INNER JOIN public.dim_sellers AS s
                ON f.seller_key = s.seller_key

            GROUP BY
                s.seller_id,
                s.seller_city,
                s.seller_state

            ORDER BY
                total_revenue DESC

            LIMIT 10;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query)

            rows = cursor.fetchall()

        return [
            {
                "seller_id": row[0],
                "seller_city": row[1],
                "seller_state": row[2],
                "total_orders": row[3],
                "total_revenue": float(row[4]),
            }
            for row in rows
        ]


    # ==========================================================
    # Geographic Analytics
    # ==========================================================

    def get_revenue_by_state(self) -> list[dict]:
        """
        Return revenue grouped by customer state.
        """

        query = """
            SELECT
                c.customer_state,

                COUNT(*) AS total_order_items,

                ROUND(COALESCE(SUM(f.payment_value), 0), 2) AS total_revenue,

                ROUND(COALESCE(AVG(f.payment_value), 0), 2) AS average_payment

            FROM public.fact_orders AS f

            INNER JOIN public.dim_customers AS c
                ON f.customer_key = c.customer_key

            GROUP BY
                c.customer_state

            ORDER BY
                total_revenue DESC;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query)

            rows = cursor.fetchall()

        return [
            {
                "customer_state": row[0],
                "total_orders": row[1],
                "total_revenue": float(row[2]),
                "average_payment": float(row[3]),
            }
            for row in rows
        ]


    def get_top_cities(self) -> list[dict]:
        """
        Return top cities by total revenue.
        """

        query = """
            SELECT
                c.customer_city,
                c.customer_state,

                COUNT(*) AS total_order_items,

                ROUND(COALESCE(SUM(f.payment_value), 0), 2) AS total_revenue,

                ROUND(COALESCE(AVG(f.payment_value), 0), 2) AS average_payment

            FROM public.fact_orders AS f

            INNER JOIN public.dim_customers AS c
                ON f.customer_key = c.customer_key

            GROUP BY
                c.customer_city,
                c.customer_state

            ORDER BY
                total_revenue DESC

            LIMIT 10;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query)

            rows = cursor.fetchall()

        return [
            {
                "customer_city": row[0],
                "customer_state": row[1],
                "total_orders": row[2],
                "total_revenue": float(row[3]),
            }
            for row in rows
        ]


    # ==========================================================
    # Operational Analytics
    # ==========================================================

    def get_order_status(self) -> list[dict]:
        """
        Return order status distribution.
        """

        query = """
            SELECT
                order_status,

                COUNT(*) AS total_order_items,

                ROUND(
                    COUNT(*) * 100.0
                    / SUM(COUNT(*)) OVER (),
                    2
                ) AS percentage_of_orders

            FROM public.fact_orders

            GROUP BY
                order_status

            ORDER BY
                total_order_items DESC;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query)

            rows = cursor.fetchall()

        return [
            {
                "order_status": row[0],
                "total_orders": row[1],
                "percentage_of_orders": float(row[2]),
            }
            for row in rows
        ]


    # ==========================================================
    # Executive Dashboard
    # ==========================================================

    def get_dashboard_kpis(self) -> dict:
        """
        Return executive dashboard KPIs.
        """

        query = """
            SELECT

                ROUND(SUM(payment_value),2) AS total_revenue,

                COUNT(DISTINCT order_id) AS total_orders,

                COUNT(DISTINCT customer_key) AS total_customers,

                COUNT(DISTINCT seller_key) AS total_sellers,

                COUNT(DISTINCT product_key) AS total_products,

                ROUND(
                    SUM(payment_value) /
                    COUNT(DISTINCT order_id),
                    2
                ) AS average_order_value,

                ROUND(
                    AVG(review_score),
                    2
                ) AS average_review_score,

                ROUND(
                    AVG(freight_value),
                    2
                ) AS average_freight_cost

            FROM public.fact_orders;
        """

        with self.connection.cursor() as cursor:
            cursor.execute(query)

            row = cursor.fetchone()

        return {
            "total_revenue": float(row[0]),
            "total_orders": row[1],
            "total_customers": row[2],
            "average_order_value": float(row[3]),
        }