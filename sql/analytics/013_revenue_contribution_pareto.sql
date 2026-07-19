/*
===============================================================================
File Name   : 13_revenue_contribution_pareto.sql
Project     : CommerceFlow
Module      : Analytics Layer
Author      : Dhruv Kajla

===============================================================================
BUSINESS QUESTION
===============================================================================

Q. Which customers contribute the most revenue?

Additionally,

• What percentage of total revenue does each customer contribute?
• What is the cumulative revenue contribution?
• Does the business follow the Pareto Principle (80/20 Rule)?

This report helps businesses identify high-value customers and determine
whether a small percentage of customers generate most of the revenue.

===============================================================================
WHY THIS QUERY EXISTS
===============================================================================

Many businesses observe that approximately:

20% of customers
↓

Generate nearly 80% of revenue.

This is known as the Pareto Principle.

Understanding customer revenue contribution helps prioritize retention,
VIP programs, and marketing investments.

===============================================================================
TABLES USED
===============================================================================

1. public.fact_orders

Purpose
-------
Stores transaction revenue.

Important Columns

customer_key
payment_value

------------------------------------------------------------

2. public.dim_customers

Purpose
-------
Stores customer information.

Important Columns

customer_unique_id

===============================================================================
SQL CONCEPTS USED
===============================================================================

1. INNER JOIN

2. GROUP BY

3. SUM()

4. Window Functions

5. SUM() OVER()

6. ORDER BY

7. CTE

===============================================================================
NEW SQL CONCEPT
===============================================================================

Cumulative Revenue

Example

Customer A   100

Customer B   80

Customer C   40

Running Total

100

180

220

Revenue Contribution %

Customer Revenue

/

Total Revenue

===============================================================================
WINDOW FUNCTION EXPLANATION
===============================================================================

SUM(total_spent)

OVER(

ORDER BY total_spent DESC

)

Creates a running total of revenue from the highest spending customers.

===============================================================================
QUERY EXECUTION ORDER
===============================================================================

Read fact_orders

↓

Join dim_customers

↓

Calculate customer spending

↓

Sort by spending

↓

Calculate cumulative revenue

↓

Calculate revenue contribution %

===============================================================================
BUSINESS INSIGHTS
===============================================================================

This report identifies

✓ Highest-value customers

✓ Revenue concentration

✓ VIP customers

✓ Pareto distribution

===============================================================================
INTERVIEW EXPLANATION
===============================================================================

This query combines aggregation with window functions to calculate
individual customer contribution and cumulative revenue percentage,
allowing businesses to identify whether a small customer base drives
most of the revenue.

===============================================================================
*/

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