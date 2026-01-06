from __future__ import annotations

from typing import Optional

from flask import Flask, render_template, request, redirect, url_for, flash

from ..config import FLASK_SECRET_KEY, DEFAULT_STORAGE
from ..db.csv_manager import CsvExpenseStorage
try:
	from ..db.mysql_manager import MySqlExpenseStorage  # optional
except Exception:
	MySqlExpenseStorage = None  # type: ignore
from ..db.base import ExpenseStorage
from ..models.expense import Expense
from ..utils.analytics import load_dataframe, compute_summary
from ..utils.visualizer import render_category_chart, render_monthly_chart


def _get_storage(mode: Optional[str]) -> ExpenseStorage:
	mode = (mode or DEFAULT_STORAGE).lower()
	if mode == "csv":
		storage = CsvExpenseStorage()
		storage.init()
		return storage
	elif mode == "mysql":
		if MySqlExpenseStorage is None:
			raise RuntimeError("MySQL mode requested but mysql-connector is not available")
		storage = MySqlExpenseStorage()
		storage.init()
		return storage
	raise ValueError(f"Unknown storage mode: {mode}")


def create_app(storage_mode: Optional[str] = None) -> Flask:
	app = Flask(__name__, static_folder="static", template_folder="templates")
	app.secret_key = FLASK_SECRET_KEY
	storage = _get_storage(storage_mode)

	@app.route("/")
	def dashboard():
		category = request.args.get("category") or None
		start_date = request.args.get("start") or None
		end_date = request.args.get("end") or None
		items = storage.list(category=category, start_date=start_date, end_date=end_date)
		df = load_dataframe(storage, category=category, start_date=start_date, end_date=end_date)
		summary = compute_summary(df)
		cat_path = render_category_chart(summary["by_category"], filename="category.png")
		mon_path = render_monthly_chart(df, filename="monthly.png")
		return render_template(
			"dashboard.html",
			items=items,
			summary=summary,
			category=category,
			start_date=start_date,
			end_date=end_date,
			category_chart=url_for("static", filename=f"charts/{cat_path.name}"),
			monthly_chart=url_for("static", filename=f"charts/{mon_path.name}"),
		)

	@app.route("/add", methods=["GET", "POST"])
	def add():
		if request.method == "POST":
			try:
				exp = Expense(
					id=None,
					date=request.form.get("date", "").strip(),
					category=request.form.get("category", "").strip(),
					amount=float(request.form.get("amount", "0") or 0),
					description=request.form.get("description", ""),
				)
				exp.validate()
				storage.add(exp)
				flash("Expense added", "success")
				return redirect(url_for("dashboard"))
			except Exception as e:
				flash(str(e), "danger")
		return render_template("form.html", expense=None)

	@app.route("/edit/<int:expense_id>", methods=["GET", "POST"])
	def edit(expense_id: int):
		current = storage.get(expense_id)
		if not current:
			flash("Expense not found", "warning")
			return redirect(url_for("dashboard"))
		if request.method == "POST":
			try:
				updated = Expense(
					id=current.id,
					date=request.form.get("date", current.date).strip() or current.date,
					category=request.form.get("category", current.category).strip() or current.category,
					amount=float(request.form.get("amount", current.amount) or current.amount),
					description=request.form.get("description", current.description),
				)
				updated.validate()
				if storage.update(expense_id, updated):
					flash("Expense updated", "success")
					return redirect(url_for("dashboard"))
				flash("Update failed", "danger")
			except Exception as e:
				flash(str(e), "danger")
		return render_template("form.html", expense=current)

	@app.route("/delete/<int:expense_id>", methods=["POST"]) 
	def delete(expense_id: int):
		if storage.delete(expense_id):
			flash("Deleted", "success")
		else:
			flash("Not found", "warning")
		return redirect(url_for("dashboard"))

	@app.route("/summary")
	def summary():
		df = load_dataframe(storage)
		summary_data = compute_summary(df)
		cat_path = render_category_chart(summary_data["by_category"], filename="category.png")
		mon_path = render_monthly_chart(df, filename="monthly.png")
		return render_template(
			"summary.html",
			summary=summary_data,
			category_chart=url_for("static", filename=f"charts/{cat_path.name}"),
			monthly_chart=url_for("static", filename=f"charts/{mon_path.name}"),
		)

	return app
