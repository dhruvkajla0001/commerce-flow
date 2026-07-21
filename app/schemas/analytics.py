"""
Analytics Response Schemas
"""

from pydantic import BaseModel, ConfigDict


# ==========================================================
# Revenue Analytics
# ==========================================================

class RevenueResponse(BaseModel):
    total_orders: int
    total_revenue: float
    average_payment: float
    highest_payment: float
    lowest_payment: float

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_orders": 112650,
                "total_revenue": 20308134.71,
                "average_payment": 180.28,
                "highest_payment": 13664.08,
                "lowest_payment": 9.59,
            }
        }
    )


class MonthlyRevenueResponse(BaseModel):
    month: str
    revenue: float

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "month": "2018-08",
                "revenue": 945231.52,
            }
        }
    )


class MonthlyRunningRevenueResponse(BaseModel):
    month: str
    monthly_revenue: float
    running_revenue: float

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "month": "2018-08",
                "monthly_revenue": 945231.52,
                "running_revenue": 15892341.75,
            }
        }
    )


class MonthGrowthResponse(BaseModel):
    month: str
    revenue: float
    growth_percent: float

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "month": "2018-08",
                "revenue": 945231.52,
                "growth_percent": 8.74,
            }
        }
    )


class RevenueParetoResponse(BaseModel):
    category: str
    revenue: float
    cumulative_percentage: float

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "category": "bed_bath_table",
                "revenue": 2458123.91,
                "cumulative_percentage": 37.82,
            }
        }
    )


# ==========================================================
# Product Analytics
# ==========================================================

class TopProductResponse(BaseModel):
    product_category: str
    revenue: float
    total_orders: int


class ProductCategoryStateResponse(BaseModel):
    customer_state: str
    product_category: str
    revenue: float


# ==========================================================
# Customer Analytics
# ==========================================================

class TopCustomerResponse(BaseModel):
    customer_id: str
    revenue: float
    total_orders: int


class CustomerSegmentationResponse(BaseModel):
    segment: str
    customers: int
    revenue: float


# ==========================================================
# Seller Analytics
# ==========================================================

class TopSellerResponse(BaseModel):
    seller_id: str
    revenue: float
    total_orders: int


# ==========================================================
# Geographic Analytics
# ==========================================================

class RevenueByStateResponse(BaseModel):
    customer_state: str
    revenue: float


class TopCityResponse(BaseModel):
    customer_city: str
    revenue: float


# ==========================================================
# Operational Analytics
# ==========================================================

class OrderStatusResponse(BaseModel):
    order_status: str
    total_orders: int
    percentage: float


# ==========================================================
# Dashboard
# ==========================================================

class DashboardResponse(BaseModel):
    total_orders: int
    total_customers: int
    total_products: int
    total_sellers: int
    total_revenue: float