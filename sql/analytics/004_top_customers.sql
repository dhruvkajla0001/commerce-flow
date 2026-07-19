/*
===============================================================================
File Name   : 04_top_customers.sql
Project     : CommerceFlow
Module      : Analytics Layer
Author      : Dhruv Kajla

===============================================================================
BUSINESS QUESTION
===============================================================================

Q. Who are the highest-value customers?

Additionally,

• How many order items has each customer purchased?
• How much total revenue has each customer generated?
• What is the customer's average payment?
• Which city and state do our best customers belong to?

Businesses use this report to identify loyal and high-spending customers.

Examples

• Amazon Prime targets high-value customers.
• Flipkart rewards loyal shoppers.
• Marketing teams create personalized campaigns.
• CRM teams build customer retention strategies.

===============================================================================
WHY THIS QUERY EXISTS
===============================================================================

Not every customer contributes equally to revenue.

A small percentage of customers often generates a large percentage
of total sales (Pareto Principle / 80-20 Rule).

This report helps businesses:

✓ Identify VIP customers
✓ Improve customer retention
✓ Create loyalty programs
✓ Increase Customer Lifetime Value (CLV)
✓ Personalize marketing campaigns

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
Stores customer-related descriptive information.

Important Columns

customer_unique_id
customer_city
customer_state

===============================================================================
WHY DO WE JOIN THESE TABLES?
===============================================================================

fact_orders stores only

customer_key

↓

Surrogate Key

Example

1542

This number has no business meaning.

Joining dim_customers allows us to display

• Customer Unique ID
• City
• State

making the report meaningful for business users.

===============================================================================
IMPORTANT DESIGN DECISION
===============================================================================

We GROUP BY customer_unique_id instead of customer_id.

Why?

In the Olist dataset, a customer may have multiple customer_id values
across different orders.

customer_unique_id represents the real customer.

Grouping by customer_id would incorrectly split one customer into
multiple records.

===============================================================================
SQL CONCEPTS USED
===============================================================================

1. INNER JOIN

Purpose

Combines transactional and customer data.

------------------------------------------------------------

2. GROUP BY

Creates one summary row for each customer.

------------------------------------------------------------

3. COUNT(*)

Counts total purchased order items.

------------------------------------------------------------

4. SUM(payment_value)

Calculates total customer spending.

------------------------------------------------------------

5. AVG(payment_value)

Calculates average payment per order item.

------------------------------------------------------------

6. ORDER BY DESC

Sorts customers from highest spender to lowest.

------------------------------------------------------------

7. LIMIT

Returns only the Top 10 customers.

===============================================================================
QUERY EXECUTION ORDER
===============================================================================

1. Read fact_orders

↓

2. Join dim_customers

↓

3. Group by customer_unique_id

↓

4. Calculate COUNT(), SUM(), AVG()

↓

5. Sort by total revenue DESC

↓

6. Return Top 10 customers

===============================================================================
BUSINESS INSIGHTS
===============================================================================

This report answers:

✓ Who spends the most?

✓ Which cities have valuable customers?

✓ Who should receive loyalty rewards?

✓ Which customers contribute the highest revenue?

===============================================================================
PERFORMANCE CONSIDERATIONS
===============================================================================

Join Key

fact_orders.customer_key

↓

dim_customers.customer_key

The join uses surrogate integer keys,
making it efficient for large datasets.

Approximate Complexity

O(n)

===============================================================================
INTERVIEW EXPLANATION
===============================================================================

If asked:

"Explain this query."

You can answer:

"This query joins the fact_orders fact table with the
dim_customers dimension using the surrogate customer_key.
Transactions are grouped by customer_unique_id to avoid
splitting the same customer across multiple customer_id values.
The query then calculates total purchases, total revenue,
and average payment for each customer before returning the
Top 10 highest-value customers."

===============================================================================
FUTURE IMPROVEMENTS
===============================================================================

• Customer Lifetime Value (CLV)

• RFM Analysis
  - Recency
  - Frequency
  - Monetary

• Customer Segmentation

• Top Customers by State

• Customer Growth Trends

===============================================================================
*/

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