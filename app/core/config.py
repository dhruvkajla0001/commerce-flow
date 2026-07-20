from pathlib import Path
import os

# --------------------------------------------------
# Project Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

APP_DIR = PROJECT_ROOT / "app"

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

REPORTS_DIR = PROJECT_ROOT / "reports"
PROFILING_REPORTS_DIR = REPORTS_DIR / "profiling"

LOG_DIR = PROJECT_ROOT / "logs"

DOCS_DIR = PROJECT_ROOT / "docs"

# --------------------------------------------------
# Default Settings
# --------------------------------------------------

DEFAULT_ENCODING = "utf-8"

CSV_SEPARATOR = ","

DATE_FORMAT = "%Y-%m-%d"

# --------------------------------------------------
# Automatically Create Required Directories
# --------------------------------------------------

for directory in [
    REPORTS_DIR,
    PROFILING_REPORTS_DIR,
    LOG_DIR,
    PROCESSED_DATA_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Database Configuration
# --------------------------------------------------

import os

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "commerce_flow")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
