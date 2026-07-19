/*
===============================================================================
File Name   : 08_top_cities_by_revenue.sql
Project     : CommerceFlow
Module      : Analytics Layer
Author      : Dhruv Kajla

===============================================================================
BUSINESS QUESTION
===============================================================================

Q. Which cities generate the highest revenue for the business?

Additionally,

• Which cities place the most order items?
• Which cities contribute the highest revenue?
• What is the average payment made by customers in each city?

Businesses use this report to identify their strongest local markets
for marketing, logistics, warehouse expansion, and customer acquisition.

===============================================================================
WHY THIS QUERY EXISTS
===============================================================================

State-level analysis provides a broad regional overview, but cities are
where business decisions are often made.

This report helps answer:

✓ Which cities generate the highest revenue?
✓ Where should new warehouses be established?
✓ Which cities deserve larger marketing budgets?
✓ Which cities have the highest customer demand?

===============================================================================
TABLES USED
===============================================================================

1. public.fact_orders

Purpose
-------
Stores transactional sales data.

Important Columns

customer_key
payment_value

------------------------------------------------------------

2. public.dim_customers

Purpose
-------
Stores customer information.

Important Columns

customer_city
customer_state

===============================================================================
WHY DO WE JOIN THESE TABLES?
===============================================================================

fact_orders stores only the surrogate customer_key.

Joining dim_customers allows us to retrieve the customer's
city and state for geographical reporting.

===============================================================================
SQL CONCEPTS USED
===============================================================================

1. INNER JOIN

Combines transactional data with customer information.

------------------------------------------------------------

2. GROUP BY

Groups records by customer city and state.

------------------------------------------------------------

3. COUNT(*)

Counts total order items.

------------------------------------------------------------

4. SUM(payment_value)

Calculates total revenue.

------------------------------------------------------------

5. AVG(payment_value)

Calculates average payment.

------------------------------------------------------------

6. COALESCE()

Replaces NULL values with zero.

------------------------------------------------------------

7. ORDER BY DESC

Sorts cities from highest revenue to lowest.

------------------------------------------------------------

8. LIMIT

Returns the Top 10 cities.

===============================================================================
QUERY EXECUTION ORDER
===============================================================================

1. Read fact_orders

↓

2. Join dim_customers

↓

3. Group by city and state

↓

4. Calculate KPIs

↓

5. Sort by revenue

↓

6. Return Top 10 cities

===============================================================================
BUSINESS INSIGHTS
===============================================================================

This report answers:

✓ Which cities generate the most revenue?

✓ Which cities have the largest customer base?

✓ Which locations should receive additional investment?

✓ Which cities should be prioritized for warehouse expansion?

===============================================================================
PERFORMANCE CONSIDERATIONS
===============================================================================

Join Key

fact_orders.customer_key

↓

dim_customers.customer_key

Uses surrogate keys for efficient joins.

Approximate Complexity

O(n)

===============================================================================
INTERVIEW EXPLANATION
===============================================================================

If asked:

"Explain this query."

You can answer:

"This query joins the fact_orders table with the
customer dimension to perform city-level sales analysis.
It calculates order volume, total revenue, and average
payment for each city and ranks them by revenue. This
helps businesses identify their strongest local markets."

===============================================================================
FUTURE IMPROVEMENTS
===============================================================================

• Revenue by City per Month

• Top Cities by Product Category

• City Growth Rate

• Revenue Heat Maps

• Top Cities using DENSE_RANK()

===============================================================================
*/

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