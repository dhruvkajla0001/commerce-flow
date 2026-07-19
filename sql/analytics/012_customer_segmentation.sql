/*
===============================================================================
File Name   : 12_customer_segmentation.sql
Project     : CommerceFlow
Module      : Analytics Layer
Author      : Dhruv Kajla

===============================================================================
BUSINESS QUESTION
===============================================================================

Q. How can customers be segmented based on their total spending?

Additionally,

• Which customers are the highest-value customers?
• How many customers belong to each segment?
• Which segment contributes the most revenue?

Customer segmentation helps businesses personalize marketing,
increase customer retention, and improve loyalty programs.

===============================================================================
WHY THIS QUERY EXISTS
===============================================================================

Not all customers contribute equally.

A small percentage of customers often generate a large share of revenue.

This report categorizes customers into business-friendly segments
based on their lifetime spending.

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
customer_city
customer_state

===============================================================================
SQL CONCEPTS USED
===============================================================================

1. INNER JOIN

2. GROUP BY

3. SUM()

4. CASE

5. COUNT()

6. ORDER BY

===============================================================================
SEGMENT DEFINITIONS
===============================================================================

Platinum : >= 5000 BRL

Gold     : 2000 - 4999 BRL

Silver   : 1000 - 1999 BRL

Bronze   : < 1000 BRL

These thresholds can be adjusted based on business requirements.

===============================================================================
BUSINESS INSIGHTS
===============================================================================

This report identifies:

✓ High-value customers

✓ Customer distribution

✓ Revenue contribution by segment

✓ Marketing opportunities

===============================================================================
INTERVIEW EXPLANATION
===============================================================================

Customer segmentation allows businesses to allocate marketing
resources efficiently by identifying high-value customers and
designing targeted retention strategies.

===============================================================================
*/

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