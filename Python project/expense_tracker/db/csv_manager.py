"""CSV storage backend for expenses.

Uses a simple incremental integer `id` column.
Cleans invalid rows and preserves only validated records.
"""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, List, Optional

from ..models.expense import Expense
from ..config import CSV_FILEPATH
from .base import ExpenseStorage


FIELDNAMES = ["id", "date", "category", "amount", "description"]


class CsvExpenseStorage(ExpenseStorage):
	def __init__(self, filepath: Optional[Path] = None) -> None:
		self.filepath: Path = Path(filepath) if filepath else CSV_FILEPATH

	def init(self) -> None:
		self.filepath.parent.mkdir(parents=True, exist_ok=True)
		if not self.filepath.exists():
			with self.filepath.open("w", newline="", encoding="utf-8") as f:
				writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
				writer.writeheader()

	def _read_all(self) -> List[Expense]:
		if not self.filepath.exists():
			return []
		rows: List[Expense] = []
		with self.filepath.open("r", newline="", encoding="utf-8") as f:
			reader = csv.DictReader(f)
			for row in reader:
				try:
					exp = Expense.from_dict(row)
					exp.validate()
					rows.append(exp)
				except Exception:
					# Skip invalid rows silently to keep file resilient
					continue
		return rows

	def _write_all(self, expenses: List[Expense]) -> None:
		with self.filepath.open("w", newline="", encoding="utf-8") as f:
			writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
			writer.writeheader()
			for e in expenses:
				writer.writerow({
					"id": e.id,
					"date": e.date,
					"category": e.category,
					"amount": f"{float(e.amount):.2f}",
					"description": e.description or "",
				})

	def _next_id(self, expenses: List[Expense]) -> int:
		max_id = 0
		for e in expenses:
			if e.id is not None and e.id > max_id:
				max_id = e.id
		return max_id + 1

	def add(self, expense: Expense) -> Expense:
		expense.validate()
		expenses = self._read_all()
		expense.id = self._next_id(expenses)
		expenses.append(expense)
		self._write_all(expenses)
		return expense

	def update(self, expense_id: int, expense: Expense) -> Optional[Expense]:
		expense.validate()
		expenses = self._read_all()
		updated = None
		for idx, e in enumerate(expenses):
			if e.id == expense_id:
				expense.id = expense_id
				expenses[idx] = expense
				updated = expense
				break
		if updated is not None:
			self._write_all(expenses)
		return updated

	def delete(self, expense_id: int) -> bool:
		expenses = self._read_all()
		new_expenses = [e for e in expenses if e.id != expense_id]
		deleted = len(new_expenses) != len(expenses)
		if deleted:
			self._write_all(new_expenses)
		return deleted

	def list(self, category: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Expense]:
		expenses = self._read_all()
		def in_range(e: Expense) -> bool:
			ok = True
			if category:
				ok = ok and e.category == category
			if start_date:
				ok = ok and e.date >= start_date
			if end_date:
				ok = ok and e.date <= end_date
			return ok
		return [e for e in expenses if in_range(e)]

	def get(self, expense_id: int) -> Optional[Expense]:
		for e in self._read_all():
			if e.id == expense_id:
				return e
		return None

	def bulk_insert(self, expenses: Iterable[Expense]) -> int:
		count = 0
		existing = self._read_all()
		next_id = self._next_id(existing)
		for exp in expenses:
			try:
				exp.validate()
			except Exception:
				continue
			exp.id = next_id
			next_id += 1
			existing.append(exp)
			count += 1
		self._write_all(existing)
		return count
