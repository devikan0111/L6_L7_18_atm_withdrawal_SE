import pytest
from atm_withdrawal import withdraw, pin_check, note_breakup


# ---------- withdraw ----------
def test_simple_withdrawal():
    assert withdraw(5000, 1000, "savings", True) == 4000


def test_unknown_account_type():
    with pytest.raises(ValueError):
        withdraw(5000, 1000, "student", True)


def test_amount_not_multiple_of_100():
    with pytest.raises(ValueError):
        withdraw(5000, 150, "savings", True)


def test_savings_limit_exceeded():
    assert withdraw(100000, 30000, "savings", True) == "limit exceeded"


def test_other_bank_large_amount_fee():
    # 15000 + (20 + 10) fee = 15030
    assert withdraw(20000, 15000, "current", False) == 4970


def test_insufficient_funds():
    assert withdraw(500, 1000, "savings", True) == "insufficient funds"


# ---------- pin_check ----------
def test_correct_pin():
    assert pin_check(1234, 1234, 0) == "ok"


def test_card_blocked_after_three_attempts():
    assert pin_check(1234, 1234, 3) == "card blocked"


def test_wrong_pin_third_try_blocks_card():
    assert pin_check(1111, 1234, 2) == "card blocked"


def test_wrong_pin_retry():
    assert pin_check(1111, 1234, 0) == "retry"


# ---------- note_breakup ----------
def test_note_breakup_invalid_amount():
    with pytest.raises(ValueError):
        note_breakup(250)


def test_note_breakup_with_200_notes():
    assert note_breakup(1700) == (3, 1, 0)


def test_note_breakup_without_200_notes():
    assert note_breakup(1000) == (2, 0, 0)
