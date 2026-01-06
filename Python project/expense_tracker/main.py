"""Expense Tracker entry point.

Usage examples:
- python -m expense_tracker.main --mode cli
- python -m expense_tracker.main --mode web
"""
from __future__ import annotations

import argparse
from typing import Optional

from tabulate import tabulate

from .config import DEFAULT_STORAGE, APP_NAME, VERSION
from .db.csv_manager import CsvExpenseStorage
try:
	from .db.mysql_manager import MySqlExpenseStorage  # optional
except Exception:
	MySqlExpenseStorage = None  # type: ignore
from .db.base import ExpenseStorage
from .models.expense import Expense
from .utils.analytics import load_dataframe, compute_summary
from .web.app import create_app


def _get_storage(kind: Optional[str]) -> ExpenseStorage:
	mode = (kind or DEFAULT_STORAGE).lower()
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


def cli_menu(storage: ExpenseStorage) -> None:
	while True:
		print(f"\n{APP_NAME} v{VERSION} (storage: {type(storage).__name__})")
		print("1) Add  2) Edit  3) Delete  4) View  5) Summary  6) Exit")
		choice = input("Choose an option: ").strip()
		if choice == "1":
			_add_expense(storage)
		elif choice == "2":
			_edit_expense(storage)
		elif choice == "3":
			_delete_expense(storage)
		elif choice == "4":
			_view_expenses(storage)
		elif choice == "5":
			_show_summary(storage)
		elif choice == "6":
			print("Goodbye!")
			break
		else:
			print("Invalid choice.")


def _add_expense(storage: ExpenseStorage) -> None:
	date = input("Date (YYYY-MM-DD): ").strip()
	category = input("Category: ").strip()
	amount = input("Amount: ").strip()
	description = input("Description (optional): ").strip()
	try:
		exp = Expense(id=None, date=date, category=category, amount=float(amount), description=description)
		exp.validate()
		storage.add(exp)
		print("Added.")
	except Exception as e:
		print(f"Error: {e}")


def _edit_expense(storage: ExpenseStorage) -> None:
	try:
		expense_id = int(input("Expense ID to edit: ").strip())
	except Exception:
		print("Invalid ID")
		return
	current = storage.get(expense_id)
	if not current:
		print("Not found.")
		return
	date = input(f"Date [{current.date}]: ").strip() or current.date
	category = input(f"Category [{current.category}]: ").strip() or current.category
	amount_raw = input(f"Amount [{current.amount}]: ").strip()
	amount = float(amount_raw) if amount_raw else current.amount
	description = input(f"Description [{current.description}]: ").strip() or current.description
	try:
		new_exp = Expense(id=current.id, date=date, category=category, amount=amount, description=description)
		new_exp.validate()
		updated = storage.update(expense_id, new_exp)
		print("Updated." if updated else "Update failed.")
	except Exception as e:
		print(f"Error: {e}")


def _delete_expense(storage: ExpenseStorage) -> None:
	try:
		expense_id = int(input("Expense ID to delete: ").strip())
	except Exception:
		print("Invalid ID")
		return
	deleted = storage.delete(expense_id)
	print("Deleted." if deleted else "Not found.")


def _view_expenses(storage: ExpenseStorage) -> None:
	category = input("Filter category (blank for all): ").strip() or None
	start_date = input("Start date YYYY-MM-DD (blank for none): ").strip() or None
	end_date = input("End date YYYY-MM-DD (blank for none): ").strip() or None
	rows = storage.list(category=category, start_date=start_date, end_date=end_date)
	table = [r.to_dict() for r in rows]
	if not table:
		print("No expenses.")
		return
	print(tabulate(table, headers="keys", tablefmt="github", floatfmt=".2f"))


def _show_summary(storage: ExpenseStorage) -> None:
	df = load_dataframe(storage)
	summary = compute_summary(df)
	print("\nTotals:")
	print(tabulate([["Total", summary["total"]], ["Average Daily", summary["average_daily"]]], headers=["Metric", "Value"], tablefmt="github"))
	print("\nBy Category:")
	cat_rows = [[k, v] for k, v in summary["by_category"].items()] or [["-", 0]]
	print(tabulate(cat_rows, headers=["Category", "Amount"], tablefmt="github"))


def main() -> None:
	parser = argparse.ArgumentParser(description=APP_NAME)
	parser.add_argument("--mode", choices=["cli", "web"], default="cli")
	parser.add_argument("--storage", choices=["csv", "mysql"], default=DEFAULT_STORAGE)
	args = parser.parse_args()
	if args.mode == "cli":
		storage = _get_storage(args.storage)
		cli_menu(storage)
	else:
		app = create_app(storage_mode=args.storage)
		app.run(host="127.0.0.1", port=5000, debug=False)


if __name__ == "__main__":
	main()
