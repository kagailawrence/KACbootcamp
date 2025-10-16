"""
What is Boilerplate Code?

Boilerplate is repetitive setup code for example, class definitions, constructors,
 or getters and setters.

AI tools like ChatGPT, GitHub Copilot, or Cursor IDE
can automatically generate boilerplate,
saving time.
"""

# Example: Generating boilerplate code for a class
from __future__ import annotations

"""
Boilerplate banking system classes.

This module contains simple, well-typed class definitions suitable for a
teaching/example project: Account (base), CheckingAccount, SavingsAccount,
Transaction, Bank, and a few custom exceptions. It intentionally avoids I/O and
persistence concerns so it's easy to test.

Design contract (brief):
- Inputs: numeric amounts (float) for money operations, account IDs as str.
- Outputs: methods return updated balance or Transaction instances.
- Error modes: raises ValueError for invalid amounts, InsufficientFunds for
  when a withdrawal cannot be completed, and KeyError when account IDs are
  unknown.

Edge cases considered:
- Negative or zero deposit/withdraw amounts
- Overdraft behavior for checking accounts
- Interest application for savings accounts
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


class InsufficientFunds(Exception):
	"""Raised when an account has insufficient funds for an operation."""


class InvalidAmount(ValueError):
	"""Raised when a provided monetary amount is invalid (<= 0)."""


@dataclass
class Transaction:
	"""Represents a single account transaction."""

	account_id: str
	amount: float
	kind: str  # 'deposit', 'withdraw', 'transfer'
	timestamp: datetime = field(default_factory=datetime.utcnow)
	note: Optional[str] = None


class Account:
	"""Base account class with basic operations and in-memory transaction log."""

	def __init__(self, account_id: str, owner: str, starting_balance: float = 0.0) -> None:
		if starting_balance < 0:
			raise InvalidAmount("starting_balance must be non-negative")
		self.account_id = account_id
		self.owner = owner
		self._balance = float(starting_balance)
		self.transactions: List[Transaction] = []

	@property
	def balance(self) -> float:
		return self._balance

	def deposit(self, amount: float, note: Optional[str] = None) -> Transaction:
		if amount <= 0:
			raise InvalidAmount("deposit amount must be > 0")
		self._balance += amount
		t = Transaction(self.account_id, amount, "deposit", note=note)
		self.transactions.append(t)
		return t

	def withdraw(self, amount: float, note: Optional[str] = None) -> Transaction:
		if amount <= 0:
			raise InvalidAmount("withdraw amount must be > 0")
		if amount > self._balance:
			raise InsufficientFunds(f"Account {self.account_id} has insufficient funds")
		self._balance -= amount
		t = Transaction(self.account_id, -amount, "withdraw", note=note)
		self.transactions.append(t)
		return t

	def add_transaction(self, transaction: Transaction) -> None:
		"""Append an externally created transaction and update balance.

		This method is low-level and assumes the transaction amount sign is
		correct (positive for deposit, negative for withdrawal).
		"""
		self._balance += transaction.amount
		self.transactions.append(transaction)


class CheckingAccount(Account):
	"""Checking account supports a limited overdraft facility."""

	def __init__(self, account_id: str, owner: str, starting_balance: float = 0.0, overdraft_limit: float = 0.0) -> None:
		super().__init__(account_id, owner, starting_balance)
		self.overdraft_limit = float(overdraft_limit)

	def withdraw(self, amount: float, note: Optional[str] = None) -> Transaction:
		if amount <= 0:
			raise InvalidAmount("withdraw amount must be > 0")
		if amount > self._balance + self.overdraft_limit:
			raise InsufficientFunds(f"Account {self.account_id} exceeds overdraft limit")
		self._balance -= amount
		t = Transaction(self.account_id, -amount, "withdraw", note=note)
		self.transactions.append(t)
		return t


class SavingsAccount(Account):
	"""Savings account with a simple interest application method."""

	def __init__(self, account_id: str, owner: str, starting_balance: float = 0.0, interest_rate: float = 0.01) -> None:
		super().__init__(account_id, owner, starting_balance)
		if interest_rate < 0:
			raise ValueError("interest_rate must be non-negative")
		self.interest_rate = float(interest_rate)

	def apply_interest(self) -> Transaction:
		"""Apply interest to the account and return the corresponding transaction."""
		if self._balance <= 0:
			# no interest on non-positive balances
			t = Transaction(self.account_id, 0.0, "interest", note="no interest applied")
			self.transactions.append(t)
			return t
		interest = self._balance * self.interest_rate
		self._balance += interest
		t = Transaction(self.account_id, interest, "interest")
		self.transactions.append(t)
		return t


class Bank:
	"""Simple in-memory bank managing multiple accounts and transfers."""

	def __init__(self) -> None:
		self.accounts: Dict[str, Account] = {}

	def add_account(self, account: Account) -> None:
		if account.account_id in self.accounts:
			raise KeyError(f"Account {account.account_id} already exists")
		self.accounts[account.account_id] = account

	def get_account(self, account_id: str) -> Account:
		try:
			return self.accounts[account_id]
		except KeyError:
			raise KeyError(f"Account {account_id} not found")

	def transfer(self, from_id: str, to_id: str, amount: float, note: Optional[str] = None) -> List[Transaction]:
		if amount <= 0:
			raise InvalidAmount("transfer amount must be > 0")
		src = self.get_account(from_id)
		dst = self.get_account(to_id)
		# perform withdraw then deposit; if withdraw raises, deposit won't run
		w = src.withdraw(amount, note=f"transfer to {to_id}: {note or ''}".strip())
		d = dst.deposit(amount, note=f"transfer from {from_id}: {note or ''}".strip())
		return [w, d]


def _demo() -> None:
	"""Small demo showing how to use the classes. Not run on import."""
	bank = Bank()
	c1 = CheckingAccount("c-001", "Alice", starting_balance=100.0, overdraft_limit=50.0)
	s1 = SavingsAccount("s-001", "Bob", starting_balance=200.0, interest_rate=0.02)
	bank.add_account(c1)
	bank.add_account(s1)
	c1.deposit(50)
	try:
		bank.transfer("c-001", "s-001", 120)
	except InsufficientFunds:
		print("Transfer failed: insufficient funds")
	s1.apply_interest()
	print(f"{c1.owner} balance: {c1.balance}")
	print(f"{s1.owner} balance: {s1.balance}")


if __name__ == "__main__":
	_demo()


