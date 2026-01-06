from expense_tracker.db.csv_manager import CsvExpenseStorage
from expense_tracker.models.expense import Expense
from expense_tracker.utils.analytics import load_dataframe, compute_summary


def test_compute_summary(tmp_path):
	store = CsvExpenseStorage(filepath=tmp_path / "data.csv")
	store.init()
	store.add(Expense(id=None, date="2025-10-01", category="Food", amount=10.0))
	store.add(Expense(id=None, date="2025-10-01", category="Travel", amount=20.0))
	store.add(Expense(id=None, date="2025-10-02", category="Food", amount=5.0))
	df = load_dataframe(store)
	summary = compute_summary(df)
	assert round(summary["total"], 2) == 35.0
	assert summary["highest_category"] in {"Food", "Travel"}
	assert len(summary["monthly"]) >= 1
