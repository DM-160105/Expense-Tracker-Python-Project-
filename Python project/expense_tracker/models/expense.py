"""Expense data model with validation and serialization helpers.

Fields:
- id: int | None
- date: str (ISO format YYYY-MM-DD)
- category: str
- amount: float (> 0)
- description: str
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


DATE_FMT = "%Y-%m-%d"


@dataclass
class Expense:
	id: Optional[int]
	date: str
	category: str
	amount: float
	description: str = ""

	def validate(self) -> None:
		"""Validate fields; raises ValueError on invalid data."""
		# Validate date
		try:
			datetime.strptime(self.date, DATE_FMT)
		except Exception as exc:  # noqa: BLE001 - re-raise as ValueError
			raise ValueError(f"Invalid date format, expected YYYY-MM-DD: {self.date}") from exc

		# Validate category
		if not isinstance(self.category, str) or not self.category.strip():
			raise ValueError("Category must be a non-empty string")

		# Validate amount
		try:
			amt = float(self.amount)
		except Exception as exc:  # noqa: BLE001
			raise ValueError("Amount must be numeric") from exc
		if amt <= 0:
			raise ValueError("Amount must be greater than 0")
		self.amount = amt

		# Normalize description
		if self.description is None:
			self.description = ""
		if not isinstance(self.description, str):
			raise ValueError("Description must be a string")

	def to_dict(self) -> Dict[str, Any]:
		"""Serialize to plain dict for storage."""
		return {
			"id": self.id,
			"date": self.date,
			"category": self.category,
			"amount": float(self.amount),
			"description": self.description or "",
		}

	@classmethod
	def from_dict(cls, data: Dict[str, Any]) -> "Expense":
		"""Create instance from dict, tolerant to extra keys."""
		return cls(
			id=_safe_int(data.get("id")),
			date=str(data.get("date", "")).strip(),
			category=str(data.get("category", "")).strip(),
			amount=_safe_float(data.get("amount")),
			description=str(data.get("description", "")),
		)


def _safe_int(value: Any) -> Optional[int]:
	if value in (None, "", "None"):
		return None
	try:
		return int(value)
	except Exception:
		return None


def _safe_float(value: Any) -> float:
	try:
		return float(value)
	except Exception:
		return 0.0
