# Expense Tracker – Personal Finance App

A modular Python app to record, manage, and analyze expenses. Supports CLI and a Flask web dashboard. Data stored in CSV by default, with optional MySQL backend.

## Features
- Add/Edit/Delete expenses (date, category, amount, description)
- Filters by category and date range
- Analytics: totals, category-wise, monthly trends
- Charts rendered with matplotlib (PNG)
- CLI (tabulate) and Web UI (Flask + Bootstrap)

## Project Structure
See `expense.plan.md` for detailed plan. Key paths:
- `expense_tracker/main.py` – entry point (CLI/Web)
- `expense_tracker/db/` – storage backends
- `expense_tracker/utils/` – analytics & charts
- `expense_tracker/web/` – Flask app, templates, static
- `expense_tracker/data/expenses.csv` – CSV storage

## Setup

### 1) Create virtual environment and install dependencies
```bash
cd \
"/Users/devangmakwana/Library/Mobile Documents/com~apple~CloudDocs/Documents/VS code/Python project"
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r expense_tracker/requirements.txt
```

### 2) Run CLI
```bash
python -m expense_tracker.main --mode cli --storage csv
```

### 3) Run Web App
```bash
python -m expense_tracker.main --mode web --storage csv
# Open http://127.0.0.1:5000
```

## Switch to MySQL (Optional)
- Install driver: `pip install mysql-connector-python`
- Set env vars: `MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD`
- Run with `--storage mysql`. The schema auto-creates.

## Tests
```bash
pytest -q
```

## Notes
- Default storage: CSV (configurable via `EXPENSE_TRACKER_STORAGE` env var)
- Charts are saved in `expense_tracker/web/static/charts/`
