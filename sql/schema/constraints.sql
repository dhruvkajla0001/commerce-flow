-- =====================================================
-- Foreign Key Constraints
-- =====================================================

ALTER TABLE fact_orders
ADD CONSTRAINT fk_fact_orders_customer
FOREIGN KEY (customer_key)
REFERENCES dim_customers(customer_key);

ALTER TABLE fact_orders
ADD CONSTRAINT fk_fact_orders_product
FOREIGN KEY (product_key)
REFERENCES dim_products(product_key);

ALTER TABLE fact_orders
ADD CONSTRAINT fk_fact_orders_seller
FOREIGN KEY (seller_key)
REFERENCES dim_sellers(seller_key);

ALTER TABLE fact_orders
ADD CONSTRAINT fk_fact_orders_date
FOREIGN KEY (date_key)
REFERENCES dim_dates(date_key);


-- =====================================================
-- Check Constraints
-- =====================================================

ALTER TABLE fact_orders
ADD CONSTRAINT chk_review_score
CHECK (review_score BETWEEN 1 AND 5);

ALTER TABLE fact_orders
ADD CONSTRAINT chk_price
CHECK (price >= 0);

ALTER TABLE fact_orders
ADD CONSTRAINT chk_freight
CHECK (freight_value >= 0);

ALTER TABLE fact_orders
ADD CONSTRAINT chk_payment
CHECK (payment_value >= 0);