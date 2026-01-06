"""Analytics utilities using pandas for summarization and trends."""
from __future__ import annotations

from typing import Dict, List, Optional

import pandas as pd

from ..db.base import ExpenseStorage


def load_dataframe(storage: ExpenseStorage, category: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
	items = storage.list(category=category, start_date=start_date, end_date=end_date)
	records = [e.to_dict() for e in items]
	df = pd.DataFrame.from_records(records, columns=["id", "date", "category", "amount", "description"])  # stable column order
	if df.empty:
		return df
	# Clean types
	df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
	df["date"] = pd.to_datetime(df["date"], errors="coerce")
	df = df.dropna(subset=["date"]).copy()
	df["date"] = df["date"].dt.date
	return df


def compute_summary(df: pd.DataFrame) -> Dict[str, object]:
	if df.empty:
		return {
			"total": 0.0,
			"average_daily": 0.0,
			"by_category": {},
			"daily": [],
			"monthly": [],
			"highest_category": None,
		}
	# Totals
	total = float(df["amount"].sum())
	by_category_series = df.groupby("category")["amount"].sum().sort_values(ascending=False)
	by_category = {k: float(v) for k, v in by_category_series.items()}
	highest_category = next(iter(by_category)) if by_category else None
	# Daily and monthly
	daily_series = df.groupby("date")["amount"].sum().sort_index()
	monthly_series = df.set_index(pd.to_datetime(df["date"]))["amount"].resample("MS").sum()
	# Average daily
	average_daily = float(daily_series.mean()) if not daily_series.empty else 0.0
	return {
		"total": round(total, 2),
		"average_daily": round(average_daily, 2),
		"by_category": {k: round(v, 2) for k, v in by_category.items()},
		"daily": [(str(idx), round(float(val), 2)) for idx, val in daily_series.items()],
		"monthly": [(idx.strftime("%Y-%m"), round(float(val), 2)) for idx, val in monthly_series.items()],
		"highest_category": highest_category,
	}


def monthly_trends(df: pd.DataFrame) -> pd.DataFrame:
	if df.empty:
		return pd.DataFrame(columns=["month", "amount"])  # empty
	df_indexed = df.set_index(pd.to_datetime(df["date"]))
	series = df_indexed["amount"].resample("MS").sum()
	trend_df = series.reset_index()  # columns: ['index' or datetime col, 0]
	trend_df.columns = ["month", "amount"]
	return trend_df
