"""MySQL storage backend for expenses (optional).

Requires `mysql-connector-python`. Gracefully degrades if not installed.
"""
from __future__ import annotations

from typing import Iterable, List, Optional

try:
	import mysql.connector  # type: ignore
except Exception:  # pragma: no cover - optional dependency
	mysql = None  # type: ignore
else:
	mysql = mysql

from ..models.expense import Expense
from ..config import MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD
from .base import ExpenseStorage


class MySqlExpenseStorage(ExpenseStorage):
	def __init__(self) -> None:
		if mysql is None:
			raise RuntimeError("mysql-connector-python is not installed")

	def _conn(self):
		return mysql.connector.connect(
			host=MYSQL_HOST,
			port=MYSQL_PORT,
			database=MYSQL_DATABASE,
			user=MYSQL_USER,
			password=MYSQL_PASSWORD,
		)

	def init(self) -> None:
		with self._conn() as conn:
			cur = conn.cursor()
			cur.execute(
				"""
				CREATE TABLE IF NOT EXISTS expenses (
					id INT PRIMARY KEY AUTO_INCREMENT,
					date DATE NOT NULL,
					category VARCHAR(100) NOT NULL,
					amount DECIMAL(12,2) NOT NULL,
					description TEXT
				)
				"""
			)
			conn.commit()

	def add(self, expense: Expense) -> Expense:
		expense.validate()
		with self._conn() as conn:
			cur = conn.cursor()
			cur.execute(
				"INSERT INTO expenses (date, category, amount, description) VALUES (%s,%s,%s,%s)",
				(expense.date, expense.category, float(expense.amount), expense.description),
			)
			expense.id = cur.lastrowid
			conn.commit()
		return expense

	def update(self, expense_id: int, expense: Expense) -> Optional[Expense]:
		expense.validate()
		with self._conn() as conn:
			cur = conn.cursor()
			cur.execute(
				"UPDATE expenses SET date=%s, category=%s, amount=%s, description=%s WHERE id=%s",
				(expense.date, expense.category, float(expense.amount), expense.description, expense_id),
			)
			conn.commit()
			if cur.rowcount:
				expense.id = expense_id
				return expense
		return None

	def delete(self, expense_id: int) -> bool:
		with self._conn() as conn:
			cur = conn.cursor()
			cur.execute("DELETE FROM expenses WHERE id=%s", (expense_id,))
			conn.commit()
			return cur.rowcount > 0

	def list(self, category: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Expense]:
		clauses = []
		args: List[object] = []
		if category:
			clauses.append("category=%s")
			args.append(category)
		if start_date:
			clauses.append("date >= %s")
			args.append(start_date)
		if end_date:
			clauses.append("date <= %s")
			args.append(end_date)
		where = (" WHERE " + " AND ".join(clauses)) if clauses else ""
		query = "SELECT id, date, category, amount, description FROM expenses" + where + " ORDER BY date DESC, id DESC"
		with self._conn() as conn:
			cur = conn.cursor()
			cur.execute(query, tuple(args))
			rows = cur.fetchall()
			return [
				Expense(
					id=row[0],
					date=str(row[1]),
					category=row[2],
					amount=float(row[3]),
					description=row[4] or "",
				)
				for row in rows
			]

	def get(self, expense_id: int) -> Optional[Expense]:
		with self._conn() as conn:
			cur = conn.cursor()
			cur.execute("SELECT id, date, category, amount, description FROM expenses WHERE id=%s", (expense_id,))
			row = cur.fetchone()
			if not row:
				return None
			return Expense(id=row[0], date=str(row[1]), category=row[2], amount=float(row[3]), description=row[4] or "")

	def bulk_insert(self, expenses: Iterable[Expense]) -> int:
		vals = []
		for exp in expenses:
			try:
				exp.validate()
			except Exception:
				continue
			vals.append((exp.date, exp.category, float(exp.amount), exp.description))
		if not vals:
			return 0
		with self._conn() as conn:
			cur = conn.cursor()
			cur.executemany(
				"INSERT INTO expenses (date, category, amount, description) VALUES (%s,%s,%s,%s)",
				vals,
			)
			conn.commit()
			return cur.rowcount or 0
