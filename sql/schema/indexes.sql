-- =====================================================
-- CommerceFlow Data Warehouse
-- Indexes
-- =====================================================

-- =====================================================
-- Fact Table Indexes
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_fact_orders_order_id
ON fact_orders(order_id);

CREATE INDEX IF NOT EXISTS idx_fact_orders_order_item_id
ON fact_orders(order_item_id);

CREATE INDEX IF NOT EXISTS idx_fact_orders_customer_key
ON fact_orders(customer_key);

CREATE INDEX IF NOT EXISTS idx_fact_orders_product_key
ON fact_orders(product_key);

CREATE INDEX IF NOT EXISTS idx_fact_orders_seller_key
ON fact_orders(seller_key);

CREATE INDEX IF NOT EXISTS idx_fact_orders_date_key
ON fact_orders(date_key);

CREATE INDEX IF NOT EXISTS idx_fact_orders_order_status
ON fact_orders(order_status);

CREATE INDEX IF NOT EXISTS idx_fact_orders_payment_value
ON fact_orders(payment_value);

CREATE INDEX IF NOT EXISTS idx_fact_orders_review_score
ON fact_orders(review_score);

-- =====================================================
-- Dimension Table Indexes
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_dim_customers_customer_id
ON dim_customers(customer_id);

CREATE INDEX IF NOT EXISTS idx_dim_products_product_id
ON dim_products(product_id);

CREATE INDEX IF NOT EXISTS idx_dim_sellers_seller_id
ON dim_sellers(seller_id);

CREATE INDEX IF NOT EXISTS idx_dim_dates_full_date
ON dim_dates(full_date);