from expense_tracker.models.expense import Expense
import pytest


def test_expense_validation_success():
	exp = Expense(id=None, date="2025-10-01", category="Food", amount=10.5, description="ok")
	exp.validate()


def test_expense_invalid_date():
	exp = Expense(id=None, date="2025/10/01", category="Food", amount=10.0)
	with pytest.raises(ValueError):
		exp.validate()


def test_expense_invalid_amount():
	exp = Expense(id=None, date="2025-10-01", category="Food", amount=0)
	with pytest.raises(ValueError):
		exp.validate()
