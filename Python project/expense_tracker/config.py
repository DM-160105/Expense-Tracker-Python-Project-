"""Global configuration for the Expense Tracker application.

This module centralizes feature flags, defaults, and environment-based configuration.
"""
from __future__ import annotations

from pathlib import Path
import os

# Base paths
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
CHARTS_DIR = PROJECT_ROOT / "web" / "static" / "charts"

# Ensure required directories exist at import time
DATA_DIR.mkdir(parents=True, exist_ok=True)
CHARTS_DIR.mkdir(parents=True, exist_ok=True)

# Storage mode: "csv" (default) or "mysql"
DEFAULT_STORAGE: str = os.getenv("EXPENSE_TRACKER_STORAGE", "csv").lower()

# CSV file path
CSV_FILEPATH: Path = DATA_DIR / "expenses.csv"

# Optional default categories (can be edited by users in UI)
DEFAULT_CATEGORIES = [
	"Food",
	"Travel",
	"Bills",
	"Entertainment",
	"Groceries",
	"Health",
	"Shopping",
	"Utilities",
	"Other",
]

# MySQL configuration (used only if storage == "mysql")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "expense_tracker")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")

# Flask configuration
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "change-this-in-production")
DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"

# App metadata
APP_NAME = "Expense Tracker"
VERSION = "1.0.0"

