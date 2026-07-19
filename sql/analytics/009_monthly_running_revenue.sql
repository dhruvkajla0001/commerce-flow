/*
===============================================================================
File Name   : 09_monthly_running_revenue.sql
Project     : CommerceFlow
Module      : Analytics Layer
Author      : Dhruv Kajla

===============================================================================
BUSINESS QUESTION
===============================================================================

Q. How has revenue grown over time?

Additionally,

• What is the monthly revenue?
• What is the cumulative (running) revenue?
• Is the business growing consistently?

This report is commonly used by Finance, Management, and BI teams to
monitor long-term business performance.

===============================================================================
WHY THIS QUERY EXISTS
===============================================================================

Monthly revenue shows the revenue generated during a specific month.

However, executives often need to know the total revenue accumulated over
time.

This report answers:

✓ How much revenue has been earned so far?

✓ How quickly is revenue accumulating?

✓ Which months contributed the most?

===============================================================================
TABLES USED
===============================================================================

1. public.fact_orders

Purpose
-------
Stores payment values and transaction records.

2. public.dim_dates

Purpose
-------
Provides Year and Month information for reporting.

===============================================================================
WHY THESE TABLES?
===============================================================================

fact_orders contains revenue.

dim_dates provides calendar attributes such as:

• year
• month
• month_name

Without the date dimension, building consistent time-based reports would
be much more difficult.

===============================================================================
SQL CONCEPTS USED
===============================================================================

1. INNER JOIN

Joins transactions with the Date Dimension.

------------------------------------------------------------

2. GROUP BY

Creates one record for every month.

------------------------------------------------------------

3. SUM()

Calculates monthly revenue.

------------------------------------------------------------

4. WINDOW FUNCTION

SUM(...) OVER()

Calculates cumulative revenue.

------------------------------------------------------------

5. ORDER BY

Ensures months appear chronologically.

===============================================================================
NEW SQL CONCEPT
===============================================================================

RUNNING TOTAL

A Running Total continuously accumulates values.

Example

January      100

February     200

March        300

Running Total

January      100

February     300

March        600

This is heavily used in:

• Sales Dashboards
• Financial Reports
• KPI Tracking
• Executive Dashboards

===============================================================================
WINDOW FUNCTION EXPLANATION
===============================================================================

SUM(monthly_revenue)

OVER (

ORDER BY year, month

)

For every row,

SQL adds the current month's revenue to all previous months.

Unlike GROUP BY,

Window Functions preserve every row while performing calculations across
multiple rows.

===============================================================================
QUERY EXECUTION ORDER
===============================================================================

Step 1

Read fact_orders

↓

Join dim_dates

↓

Group by Year and Month

↓

Calculate Monthly Revenue

↓

Calculate Running Revenue

↓

Sort Chronologically

===============================================================================
BUSINESS INSIGHTS
===============================================================================

This report answers:

✓ Is revenue increasing?

✓ Are there seasonal spikes?

✓ How much revenue has accumulated?

✓ Which periods drove business growth?

===============================================================================
PERFORMANCE CONSIDERATIONS
===============================================================================

Uses

GROUP BY

followed by

Window Function

Complexity remains efficient for analytical reporting.

===============================================================================
INTERVIEW EXPLANATION
===============================================================================

If asked,

"Explain this query."

You can answer:

"This query calculates monthly revenue using GROUP BY and then applies a
window function to compute a running total. Running totals are commonly
used in executive dashboards because they show how revenue accumulates
over time without collapsing individual monthly records."

===============================================================================
FUTURE IMPROVEMENTS
===============================================================================

• Running Revenue by State

• Running Revenue by Product Category

• Quarterly Running Revenue

• Year-over-Year Running Revenue

===============================================================================
*/

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