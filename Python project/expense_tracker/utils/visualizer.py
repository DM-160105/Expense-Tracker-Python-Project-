"""Visualization utilities using matplotlib.

Generates static PNG files under web/static/charts.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

import matplotlib

matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt  # noqa: E402

from .analytics import monthly_trends
from ..config import CHARTS_DIR


def render_category_chart(by_category: Dict[str, float], filename: str = "category.png") -> Path:
	CHARTS_DIR.mkdir(parents=True, exist_ok=True)
	labels = list(by_category.keys())
	values = list(by_category.values())
	plt.figure(figsize=(6, 4))
	plt.bar(labels, values, color="#4e79a7")
	plt.xticks(rotation=30, ha="right")
	plt.ylabel("Amount")
	plt.title("Spending by Category")
	plt.tight_layout()
	out = CHARTS_DIR / filename
	plt.savefig(out)
	plt.close()
	return out


def render_monthly_chart(df, filename: str = "monthly.png") -> Path:
	CHARTS_DIR.mkdir(parents=True, exist_ok=True)
	trend_df = monthly_trends(df)
	plt.figure(figsize=(6, 4))
	if not trend_df.empty:
		plt.plot(trend_df["month"], trend_df["amount"], marker="o", color="#f28e2b")
		plt.xticks(rotation=30, ha="right")
		plt.ylabel("Amount")
		plt.title("Monthly Spending")
	else:
		plt.text(0.5, 0.5, "No Data", ha="center", va="center")
	plt.tight_layout()
	out = CHARTS_DIR / filename
	plt.savefig(out)
	plt.close()
	return out
