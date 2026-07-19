/*
===============================================================================
File Name   : 11_month_over_month_growth.sql
Project     : CommerceFlow
Module      : Analytics Layer
Author      : Dhruv Kajla

===============================================================================
BUSINESS QUESTION
===============================================================================

Q. How has monthly revenue changed compared to the previous month?

Additionally,

• Which month experienced the highest growth?
• Which month experienced the biggest decline?
• What is the Month-over-Month (MoM) growth percentage?

This report helps businesses monitor growth trends and identify
seasonal patterns or sudden changes in sales.

===============================================================================
WHY THIS QUERY EXISTS
===============================================================================

Looking only at monthly revenue doesn't tell us whether business
performance is improving or declining.

Month-over-Month analysis compares each month's revenue with the
previous month's revenue.

It answers:

✓ Is revenue growing?

✓ How much did revenue increase?

✓ Which months experienced decline?

===============================================================================
TABLES USED
===============================================================================

1. public.fact_orders

Purpose
-------
Stores transaction revenue.

2. public.dim_dates

Purpose
-------
Provides calendar information.

===============================================================================
SQL CONCEPTS USED
===============================================================================

1. INNER JOIN

Joins revenue with date dimension.

------------------------------------------------------------

2. GROUP BY

Calculates monthly revenue.

------------------------------------------------------------

3. CTE

Separates aggregation logic.

------------------------------------------------------------

4. LAG()

Returns previous month's revenue.

------------------------------------------------------------

5. CASE

Handles the first month where no previous revenue exists.

------------------------------------------------------------

6. ROUND()

Formats revenue and growth percentage.

===============================================================================
NEW SQL CONCEPT
===============================================================================

LAG()

Returns the value from the previous row.

Example

Month      Revenue

Jan        100

Feb        150

Mar        120

LAG()

Month      Revenue     Previous

Jan        100         NULL

Feb        150         100

Mar        120         150

===============================================================================
WINDOW FUNCTION EXPLANATION
===============================================================================

LAG(monthly_revenue)

OVER(

ORDER BY year, month

)

Meaning

Take the revenue from the previous chronological month.

===============================================================================
QUERY EXECUTION ORDER
===============================================================================

Read fact_orders

↓

Join dim_dates

↓

Group by Month

↓

Calculate Monthly Revenue

↓

Apply LAG()

↓

Calculate Growth %

===============================================================================
BUSINESS INSIGHTS
===============================================================================

This report identifies:

✓ Months with highest growth

✓ Months with revenue decline

✓ Seasonal trends

✓ Business momentum

===============================================================================
INTERVIEW EXPLANATION
===============================================================================

If asked:

"Why use LAG()?"

Answer:

"LAG() allows us to compare the current row with a previous row without
using a self-join. It is commonly used for trend analysis, growth
calculations, and financial reporting."

===============================================================================
*/

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