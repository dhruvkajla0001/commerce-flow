/*
===============================================================================
File Name   : 07_order_status_analysis.sql
Project     : CommerceFlow
Module      : Analytics Layer
Author      : Dhruv Kajla

===============================================================================
BUSINESS QUESTION
===============================================================================

Q. How are orders distributed across different order statuses?

Additionally,

• How many order items belong to each order status?
• What percentage of total order items does each status represent?

This report measures the operational health of the e-commerce platform.

Examples

• Operations teams monitor delivery performance.
• Customer support tracks cancelled orders.
• Management measures order fulfillment efficiency.
• Logistics teams identify operational bottlenecks.

===============================================================================
WHY THIS QUERY EXISTS
===============================================================================

Revenue alone does not indicate business success.

A company must also understand:

• How many orders were successfully delivered?
• How many were cancelled?
• How many are still processing?
• Where operational issues occur?

A high cancellation rate may indicate:

✓ Inventory shortages
✓ Payment failures
✓ Logistics issues

A high delivered percentage indicates a healthy fulfillment process.

===============================================================================
TABLE USED
===============================================================================

public.fact_orders

Purpose
-------
Stores transactional order information.

Important Columns

order_status

Possible Values

• delivered
• shipped
• invoiced
• processing
• approved
• unavailable
• canceled
• created

===============================================================================
SQL CONCEPTS USED
===============================================================================

1. GROUP BY

Purpose
-------
Creates one summary row for each order status.

------------------------------------------------------------

2. COUNT(*)

Purpose
-------
Counts the number of order items in each status.

------------------------------------------------------------

3. SUM(COUNT(*)) OVER ()

Purpose
-------
Calculates the total number of order items across all statuses.

Why?

This allows us to calculate percentages without writing a
separate subquery.

This is our first Window Function.

------------------------------------------------------------

4. ROUND()

Formats percentages to two decimal places.

------------------------------------------------------------

5. ORDER BY

Sorts statuses from most common to least common.

===============================================================================
NEW SQL CONCEPT
===============================================================================

WINDOW FUNCTION

SUM(COUNT(*)) OVER ()

Unlike GROUP BY,

Window Functions do NOT collapse rows.

Instead,

they perform calculations across the final grouped result.

Example

Delivered  112000

Cancelled   500

Processing  150

↓

Total

112650

Each row can access this total.

Percentage

Delivered

=

112000 / 112650

===============================================================================
QUERY EXECUTION ORDER
===============================================================================

Step 1

FROM fact_orders

↓

Read transaction records.

------------------------------------------------------------

Step 2

GROUP BY order_status

↓

Create one group per status.

------------------------------------------------------------

Step 3

COUNT(*)

↓

Calculate total order items for each status.

------------------------------------------------------------

Step 4

SUM(COUNT(*)) OVER ()

↓

Calculate grand total.

------------------------------------------------------------

Step 5

Calculate percentage.

------------------------------------------------------------

Step 6

ORDER BY

↓

Sort descending.

===============================================================================
BUSINESS INSIGHTS
===============================================================================

This report answers:

✓ What percentage of orders are delivered?

✓ What percentage are cancelled?

✓ Are operational problems increasing?

✓ Is the fulfillment pipeline healthy?

===============================================================================
PERFORMANCE CONSIDERATIONS
===============================================================================

Table

fact_orders

Grouping Column

order_status

Approximate Complexity

O(n)

Very efficient because only one table is scanned.

===============================================================================
INTERVIEW EXPLANATION
===============================================================================

If asked:

"Explain this query."

You can answer:

"This query groups all order items by order_status to
calculate operational KPIs. Besides counting the number
of order items in each status, it uses a Window Function
to calculate the overall total and derive the percentage
distribution of each status. This type of report helps
operations teams monitor fulfillment performance."

===============================================================================
FUTURE IMPROVEMENTS
===============================================================================

• Order Status by Month

• Cancellation Rate by State

• Delivery Success Trend

• Average Delivery Time

• SLA Monitoring

===============================================================================
*/

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