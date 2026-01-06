"""Storage abstraction for expenses.

Defines the interface used by CLI and web layers.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, List, Optional

from ..models.expense import Expense


class ExpenseStorage(ABC):
	"""Abstract storage for expenses."""

	@abstractmethod
	def init(self) -> None:
		"""Initialize underlying storage (e.g., create files/tables)."""

	@abstractmethod
	def add(self, expense: Expense) -> Expense:
		"""Insert new expense and return with assigned id."""

	@abstractmethod
	def update(self, expense_id: int, expense: Expense) -> Optional[Expense]:
		"""Update expense by id; returns updated expense or None if not found."""

	@abstractmethod
	def delete(self, expense_id: int) -> bool:
		"""Delete expense by id; returns True if deleted."""

	@abstractmethod
	def list(self, category: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Expense]:
		"""List expenses with optional filters."""

	@abstractmethod
	def get(self, expense_id: int) -> Optional[Expense]:
		"""Get expense by id or None."""

	@abstractmethod
	def bulk_insert(self, expenses: Iterable[Expense]) -> int:
		"""Insert many expenses; returns count inserted."""
