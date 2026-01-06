from pathlib import Path

import pytest

from expense_tracker.db.csv_manager import CsvExpenseStorage
from expense_tracker.models.expense import Expense


def test_csv_crud(tmp_path: Path):
	file = tmp_path / "expenses.csv"
	store = CsvExpenseStorage(filepath=file)
	store.init()
	# Add
	e = store.add(Expense(id=None, date="2025-10-01", category="Food", amount=10.0, description=""))
	assert e.id == 1
	# Get
	fetched = store.get(1)
	assert fetched and fetched.category == "Food"
	# Update
	e_updated = store.update(1, Expense(id=None, date="2025-10-02", category="Travel", amount=15.0, description=""))
	assert e_updated and e_updated.category == "Travel"
	# List
	rows = store.list(category="Travel")
	assert len(rows) == 1
	# Delete
	assert store.delete(1) is True
	assert store.get(1) is None
