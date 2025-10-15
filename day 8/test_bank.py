"""Unit tests for the simple banking boilerplate classes."""

import pytest

from GenerateBoilerplateClassCodeAI import (
    Bank,
    CheckingAccount,
    SavingsAccount,
    InvalidAmount,
    InsufficientFunds,
)


def test_deposit_withdraw():
    acc = CheckingAccount("t-1", "Test", starting_balance=100.0)
    acc.deposit(50)
    assert acc.balance == 150.0
    acc.withdraw(20)
    assert acc.balance == 130.0


def test_invalid_amounts():
    acc = CheckingAccount("t-2", "Test", starting_balance=0.0)
    with pytest.raises(InvalidAmount):
        acc.deposit(0)
    with pytest.raises(InvalidAmount):
        acc.withdraw(-10)


def test_overdraft_limit():
    acc = CheckingAccount("t-3", "Test", starting_balance=50.0, overdraft_limit=25.0)
    acc.withdraw(70)  # allowed: uses overdraft
    assert acc.balance == -20.0
    with pytest.raises(InsufficientFunds):
        acc.withdraw(10)  # would exceed overdraft


def test_transfer_and_accounts():
    bank = Bank()
    a = CheckingAccount("a", "A", starting_balance=100.0)
    b = SavingsAccount("b", "B", starting_balance=50.0)
    bank.add_account(a)
    bank.add_account(b)
    bank.transfer("a", "b", 30)
    assert a.balance == 70.0
    assert b.balance == 80.0


def test_savings_interest():
    s = SavingsAccount("s", "S", starting_balance=100.0, interest_rate=0.05)
    t = s.apply_interest()
    assert round(s.balance, 6) == round(100.0 * 1.05, 6)
    assert t.kind == "interest"
