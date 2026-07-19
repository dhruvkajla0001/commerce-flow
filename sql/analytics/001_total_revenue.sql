/*
===============================================================================
File Name   : 01_total_revenue.sql
Project     : CommerceFlow
Module      : Analytics Layer
Author      : Dhruv Kajla

===============================================================================
BUSINESS QUESTION
===============================================================================

Q. What is the overall revenue generated from all customer payments?

This is one of the most important Key Performance Indicators (KPIs) for any
e-commerce company. It helps management understand the total amount of money
received from customers.

Examples:
- Amazon checks daily revenue.
- Flipkart monitors revenue during sales events.
- Finance teams compare revenue month-over-month.

===============================================================================
WHY THIS QUERY EXISTS
===============================================================================

The warehouse stores one record for each order item.

Instead of manually calculating totals in Excel, SQL allows us to:

• Calculate total revenue instantly
• Measure average payment amount
• Identify highest-value transactions
• Identify smallest transactions
• Count the total number of order items

These metrics become the foundation for dashboards and business reports.

===============================================================================
TABLE USED
===============================================================================

public.fact_orders

Why?

This table stores transactional data.

Every row represents one purchased order item.

Important columns:

payment_value   → Amount paid by the customer
price           → Product price
freight_value   → Shipping cost
order_status    → Order lifecycle
review_score    → Customer rating

===============================================================================
SQL FUNCTIONS USED
===============================================================================

1. COUNT(*)

Purpose
-------
Counts the total number of rows.

Why?
----
We want to know how many order-item records exist.

Example

10 rows
↓

COUNT(*) = 10

---------------------------------------------------------

2. SUM(payment_value)

Purpose
-------
Adds every payment together.

Why?
----
Revenue is simply the sum of every customer payment.

Example

100
200
300

↓

SUM = 600

---------------------------------------------------------

3. AVG(payment_value)

Purpose
-------
Calculates the arithmetic average.

Why?
----
Shows the average amount customers pay per order item.

Formula

Average = Total Payments / Number of Rows

---------------------------------------------------------

4. MAX(payment_value)

Purpose
-------
Returns the largest payment.

Why?
----
Useful for understanding high-value purchases and spotting
premium orders or unusual transactions.

---------------------------------------------------------

5. MIN(payment_value)

Purpose
-------
Returns the smallest payment.

Why?
----
Useful for understanding the lowest-priced completed purchase
and detecting unusually small transactions.

---------------------------------------------------------

6. ROUND(value, 2)

Purpose
-------
Rounds decimal values to two digits.

Why?
----
Currency values are normally displayed with two decimal places.

Without ROUND()

20308134.7138471

With ROUND()

20308134.71

===============================================================================
QUERY EXECUTION ORDER (How PostgreSQL thinks)
===============================================================================

1. FROM public.fact_orders

   PostgreSQL reads every row from the fact table.

↓

2. Aggregate Functions

COUNT()
SUM()
AVG()
MAX()
MIN()

All rows are scanned once.

↓

3. ROUND()

Formats numeric results.

↓

4. Final Result Returned

===============================================================================
TIME COMPLEXITY
===============================================================================

Current Complexity

O(n)

Reason

Every row must be read once.

For this project:

112,650 rows

This is extremely fast.

===============================================================================
INTERVIEW EXPLANATION
===============================================================================

If asked:

"Explain this query."

You can answer:

"This query calculates the overall business KPIs from the fact_orders table.
COUNT(*) returns the number of order items, SUM(payment_value) calculates total
revenue, AVG() gives the average payment, MAX() and MIN() identify the payment
range, and ROUND() formats currency values. Since all metrics come from the
same table without joins, PostgreSQL performs a single table scan."

===============================================================================
*/

SELECT
    COUNT(*) AS total_order_items,
    ROUND(SUM(payment_value), 2) AS total_revenue,
    ROUND(AVG(payment_value), 2) AS average_payment,
    ROUND(MAX(payment_value), 2) AS highest_payment,
    ROUND(MIN(payment_value), 2) AS lowest_payment
FROM public.fact_orders;