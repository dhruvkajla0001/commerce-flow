/*
===============================================================================
File Name   : 14_dashboard_kpis.sql
Project     : CommerceFlow
Module      : Analytics Layer
Author      : Dhruv Kajla

===============================================================================
BUSINESS QUESTION
===============================================================================

Q. What are the key business KPIs required for an executive dashboard?

This report provides:

• Total Revenue
• Total Orders
• Total Customers
• Total Sellers
• Total Products Sold
• Average Order Value (AOV)
• Average Review Score
• Average Freight Cost

This query is intended to power executive dashboards and APIs.

===============================================================================
WHY THIS QUERY EXISTS
===============================================================================

Executives don't want dozens of reports.

They want one dashboard showing the health of the business.

This query combines the most important KPIs into a single report.

===============================================================================
TABLES USED
===============================================================================

fact_orders

dim_customers

dim_sellers

dim_products

===============================================================================
SQL CONCEPTS USED
===============================================================================

• COUNT(DISTINCT)

• SUM()

• AVG()

• ROUND()

• Aggregate KPIs

===============================================================================
BUSINESS DEFINITIONS
===============================================================================

Total Revenue
-------------
Sum of all payment values.

Average Order Value
-------------------
Revenue / Number of Orders

Average Review Score
--------------------
Average customer rating.

Average Freight Cost
--------------------
Average shipping cost.

===============================================================================
INTERVIEW EXPLANATION
===============================================================================

This query creates a dashboard-ready KPI layer by aggregating the most
important business metrics into a single dataset. Such queries are commonly
used as the backend for BI dashboards, executive reports, and REST APIs.

===============================================================================
*/

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