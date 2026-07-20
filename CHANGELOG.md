# Changelog

All notable changes to **CommerceFlow** will be documented in this file.

The format follows the principles of **Keep a Changelog** and uses Semantic Versioning concepts for project milestones.

---

# [v1.0.0-alpha.5] - 2026-07-20

## 🚀 Milestone 5 – Apache Airflow Orchestration

### Added

- Integrated Apache Airflow using LocalExecutor.
- Created production-ready Dockerized Airflow environment.
- Added Airflow Scheduler, Webserver and Initialization services.
- Implemented CommerceFlow DAG for complete pipeline orchestration.
- Added modular Airflow task wrappers for:
  - Customer ETL
  - Product ETL
  - Seller ETL
  - Date Dimension ETL
  - Fact Orders ETL
  - Analytics Pipeline
- Added automatic execution of Analytics Pipeline from Airflow.
- Added automatic CSV report generation after analytics execution.
- Added execution summaries and pipeline statistics.

### Improved

- Refactored AnalyticsRunner for production deployment.
- Automatic SQL discovery using project root.
- Structured logging throughout analytics pipeline.
- Improved SQL execution engine.
- Improved PostgreSQL connection management.
- Better exception handling and execution metrics.
- Cleaner Docker project mounting.

### Fixed

- Fixed Airflow Broken DAG import issues.
- Fixed Python module resolution using PYTHONPATH.
- Fixed PostgreSQL connection helper.
- Fixed SQL directory resolution inside Docker.
- Fixed analytics execution inside Airflow containers.
- Fixed Docker volume mappings.
- Fixed analytics report exports.

### Validation

- Successfully orchestrated complete ETL pipeline.
- Executed all analytics queries automatically.
- Generated analytics CSV reports.
- Verified Docker deployment.
- Achieved 100% successful Airflow execution.

---

# [v1.0.0-alpha.4] - 2026-07-18

## 📊 Milestone 4 – Analytics Layer

### Added

- Production-ready Analytics module.
- SQL execution engine.
- Analytics result formatter.
- Analytics report exporter.
- Analytics runner.
- Analytics models.
- Custom analytics exceptions.

### Analytics Reports

Implemented 14 business analytics reports:

1. Total Revenue
2. Monthly Revenue
3. Top Products
4. Top Customers
5. Top Sellers
6. Revenue by State
7. Order Status Analysis
8. Top Cities by Revenue
9. Monthly Running Revenue
10. Top Product Category per State
11. Month-over-Month Growth
12. Customer Segmentation
13. Pareto Revenue Analysis
14. Dashboard KPI Summary

### Added

- Automatic CSV exports.
- Execution time measurement.
- Structured logging.
- Result preview formatting.

---

# [v1.0.0-alpha.3] - 2026-07-17

## 🏗 Milestone 3 – ETL Framework

### Added

- Generic ETL framework.
- Base Loader abstraction.
- CSV Loader.
- Batch Writer.
- Data Validator.
- Data Profiler.

### Dimension Loaders

- Customer Loader
- Product Loader
- Seller Loader
- Date Dimension Loader

### Fact Loader

- Fact Orders Loader
- Multi-table joins
- Surrogate key lookups
- Incremental loading support

### Improved

- Logging
- Error handling
- Batch inserts
- Validation framework

---

# [v1.0.0-alpha.2] - 2026-07-16

## 🗄 Milestone 2 – Data Warehouse

### Added

Star Schema Design

Dimension Tables

- dim_customers
- dim_products
- dim_sellers
- dim_dates

Fact Table

- fact_orders

### Added

- Primary Keys
- Foreign Keys
- Constraints
- Indexes
- Database initialization scripts

### Improved

- PostgreSQL schema organization.
- Warehouse performance.

---

# [v1.0.0-alpha.1] - 2026-07-15

## 🏗 Milestone 1 – Project Foundation

### Added

Project structure

```
app/
pipelines/
sql/
docs/
tests/
configs/
docker/
monitoring/
airflow/
data/
```

### Added

Core modules

- Configuration management
- Logging
- Database package
- Utilities
- Models
- API package

### Added

Project files

- README
- LICENSE
- CONTRIBUTING
- CHANGELOG
- PROJECT_PLAN
- DATA_DICTIONARY
- ARCHITECTURE
- DECISIONS
- LEARNINGS

### Added

Docker support

- PostgreSQL
- Docker Compose
- Environment configuration

---

# [v1.0.0-alpha.0] - 2026-07-14

## 📋 Milestone 0 – Planning

### Planned

- CommerceFlow Architecture
- Star Schema
- ETL Pipeline
- Analytics Layer
- Airflow Orchestration
- FastAPI Backend
- Monitoring
- Documentation
- Docker Deployment
- Future Streaming Platform (v2)

### Defined

Project Goals

- Production-inspired Data Engineering platform.
- End-to-end ETL workflows.
- Data Warehouse.
- Business Analytics.
- API Layer.
- Airflow Orchestration.
- Monitoring.
- Portfolio-quality architecture.