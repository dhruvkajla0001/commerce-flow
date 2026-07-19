/*
===============================================================================
File Name   : 02_monthly_revenue.sql
Project     : CommerceFlow
Module      : Analytics Layer
Author      : Dhruv Kajla

===============================================================================
BUSINESS QUESTION
===============================================================================

Q. How much revenue was generated every month?

Additionally,

• How many order items were sold every month?
• What was the average payment amount each month?

These are core business KPIs used to measure business growth,
seasonality, customer purchasing behaviour, and sales performance.

Examples

• Finance teams compare monthly revenue.
• Executives monitor business growth.
• Marketing teams evaluate campaign performance.
• Investors analyze long-term trends.

===============================================================================
WHY THIS QUERY EXISTS
===============================================================================

Looking at total revenue alone does not explain how the business is
performing over time.

Breaking revenue into months helps answer questions like:

• Is revenue increasing?
• Which month performed the best?
• Are there seasonal sales spikes?
• Did promotional events increase revenue?
• Which months require more marketing investment?

This is one of the first reports every BI dashboard provides.

===============================================================================
TABLES USED
===============================================================================

1. public.fact_orders

Purpose
-------
Stores transactional data.

Every row represents one purchased order item.

Important Columns

payment_value
date_key

------------------------------------------------------------

2. public.dim_dates

Purpose
-------
Stores all calendar-related information.

Instead of repeatedly extracting dates from timestamps,
the warehouse stores date attributes in a separate dimension.

Important Columns

year
month
month_name
quarter
day_name
week_of_year
is_weekend

This follows the Star Schema design.

===============================================================================
WHY DO WE USE A DATE DIMENSION?
===============================================================================

Without a Date Dimension

SELECT
    EXTRACT(MONTH FROM order_purchase_timestamp)

Problems

• Harder to read
• Repeated calculations
• Difficult to add fiscal calendars
• Difficult to add holidays
• Difficult to analyse weekends

------------------------------------------------------------

With Date Dimension

JOIN dim_dates

Benefits

• Cleaner SQL
• Better maintainability
• Consistent reporting
• Easier filtering
• Standard Data Warehouse design

===============================================================================
SQL CONCEPTS USED
===============================================================================

1. INNER JOIN

Purpose
-------
Combines data from multiple tables.

Why?

The fact table only stores a date_key.

Human-readable information like

Year
Month
Month Name

exists inside dim_dates.

Example

fact_orders

date_key

↓

20180101

↓

INNER JOIN

↓

dim_dates

↓

2018
January

------------------------------------------------------------

2. COUNT(*)

Purpose
-------
Counts total order-item records.

Why?

Shows business activity during each month.

Higher count

↓

More products sold.

------------------------------------------------------------

3. SUM(payment_value)

Purpose
-------
Adds all customer payments.

Why?

Revenue equals the total amount customers paid.

------------------------------------------------------------

4. AVG(payment_value)

Purpose
-------
Calculates average payment.

Why?

Shows average customer spending.

Formula

Average Payment

=

Total Revenue

/

Number of Order Items

------------------------------------------------------------

5. ROUND()

Purpose

Formats currency values to two decimal places.

Without ROUND()

1583869.0123489

With ROUND()

1583869.01

------------------------------------------------------------

6. GROUP BY

Purpose
-------
Creates one summary row for every unique combination.

In this query

Year

+

Month

↓

One result per month.

Without GROUP BY

Only one total revenue value would be returned.

------------------------------------------------------------

7. ORDER BY

Purpose
-------
Sorts the final report.

Why?

Business reports should appear chronologically.

Instead of

January
March
February

we get

January
February
March

===============================================================================
QUERY EXECUTION ORDER
===============================================================================

Step 1

FROM fact_orders

↓

Read transactional records.

------------------------------------------------------------

Step 2

INNER JOIN dim_dates

↓

Attach calendar information.

------------------------------------------------------------

Step 3

GROUP BY

↓

Create monthly groups.

------------------------------------------------------------

Step 4

COUNT()
SUM()
AVG()

↓

Calculate KPIs for every month.

------------------------------------------------------------

Step 5

ROUND()

↓

Format currency values.

------------------------------------------------------------

Step 6

ORDER BY

↓

Sort chronologically.

------------------------------------------------------------

Step 7

Return final report.

===============================================================================
BUSINESS INSIGHTS FROM OUR RESULTS
===============================================================================

Observations

• Revenue steadily increased during 2017.
• November 2017 shows the highest revenue (~1.58M BRL),
  likely due to Black Friday sales.
• Revenue remained strong throughout 2018.
• September 2018 has unusually low revenue because the
  Olist dataset ends during that month, making it an
  incomplete reporting period.

Important Lesson

A Data Engineer should not only write SQL but also
understand whether unusual values are due to business
events or data limitations.

===============================================================================
TIME COMPLEXITY
===============================================================================

Approximate Complexity

O(n)

Reason

Each row from fact_orders is read once and grouped by month.

With proper indexes and a date dimension,
this query scales efficiently.

===============================================================================
INTERVIEW EXPLANATION
===============================================================================

If asked:

"Explain this query."

You can answer:

"This query joins the fact_orders table with the dim_dates
table using the surrogate date_key. After enriching each
transaction with calendar information, it groups the data by
year and month to calculate monthly KPIs such as total
revenue, order-item count, and average payment. Finally,
the results are sorted chronologically to produce a business
report suitable for dashboards."

===============================================================================
FUTURE IMPROVEMENTS
===============================================================================

• Revenue by Quarter
• Revenue by Week
• Weekend vs Weekday Revenue
• Monthly Growth Percentage
• Running Revenue using Window Functions
• Year-over-Year Growth using LAG()

===============================================================================
*/

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