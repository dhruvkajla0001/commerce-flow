-- =====================================================
-- Dimension: Customers
-- =====================================================

CREATE TABLE IF NOT EXISTS dim_customers (
    customer_key SERIAL PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL UNIQUE,
    customer_unique_id VARCHAR(50) NOT NULL,
    customer_city VARCHAR(100),
    customer_state VARCHAR(10),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Dimension: Products
-- =====================================================

CREATE TABLE IF NOT EXISTS dim_products (
    product_key SERIAL PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL UNIQUE,

    product_category_name VARCHAR(255),

    product_name_length INTEGER,
    product_description_length INTEGER,
    product_photos_qty INTEGER,

    product_weight_g NUMERIC,
    product_length_cm NUMERIC,
    product_height_cm NUMERIC,
    product_width_cm NUMERIC,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Dimension: Sellers
-- =====================================================

CREATE TABLE IF NOT EXISTS dim_sellers (
    seller_key SERIAL PRIMARY KEY,
    seller_id VARCHAR(50) NOT NULL UNIQUE,

    seller_zip_code_prefix INTEGER,
    seller_city VARCHAR(100),
    seller_state VARCHAR(10),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Dimension: Dates
-- =====================================================

CREATE TABLE IF NOT EXISTS dim_dates (
    date_key INTEGER PRIMARY KEY,

    full_date DATE NOT NULL UNIQUE,

    day INTEGER,
    month INTEGER,
    month_name VARCHAR(20),

    quarter INTEGER,

    year INTEGER,

    week_of_year INTEGER,

    day_of_week INTEGER,
    day_name VARCHAR(20),

    is_weekend BOOLEAN,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- Fact: Orders
-- =====================================================

CREATE TABLE IF NOT EXISTS fact_orders (

    order_key SERIAL PRIMARY KEY,

    order_id VARCHAR(50) NOT NULL,
    order_item_id INTEGER NOT NULL,

    customer_key INTEGER NOT NULL,
    product_key INTEGER NOT NULL,
    seller_key INTEGER NOT NULL,
    date_key INTEGER NOT NULL,

    order_status VARCHAR(30),

    price NUMERIC(10,2),
    freight_value NUMERIC(10,2),
    payment_value NUMERIC(10,2),

    review_score INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);