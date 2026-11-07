import pytest
from atm_withdrawal import withdraw, pin_check, note_breakup


# ================= withdraw =================
def test_simple_withdrawal():
    assert withdraw(5000, 1000, "savings", True) == 4000


def test_unknown_account_type():
    with pytest.raises(ValueError):
        withdraw(5000, 1000, "student", True)


# amount <= 0 (True) and amount % 100 != 0 (True) are separate conditions
def test_zero_amount_invalid():
    with pytest.raises(ValueError):
        withdraw(5000, 0, "savings", True)


def test_negative_amount_invalid():
    with pytest.raises(ValueError):
        withdraw(5000, -100, "savings", True)


def test_amount_not_multiple_of_100():
    with pytest.raises(ValueError):
        withdraw(5000, 150, "savings", True)


# daily-limit branch: True and False, both account types, plus the boundary
def test_savings_limit_exceeded():
    assert withdraw(100000, 25100, "savings", True) == "limit exceeded"


def test_savings_exactly_at_limit_is_allowed():
    assert withdraw(100000, 25000, "savings", True) == 75000


def test_current_limit_exceeded():
    assert withdraw(100000, 50100, "current", True) == "limit exceeded"


def test_current_exactly_at_limit_is_allowed():
    assert withdraw(100000, 50000, "current", True) == 50000


# own_bank False/True x amount > 10000 False/True
def test_other_bank_small_amount_fee_20():
    assert withdraw(5000, 1000, "savings", False) == 3980


def test_other_bank_amount_exactly_10000_no_extra_fee():
    assert withdraw(20000, 10000, "savings", False) == 9980


def test_other_bank_large_amount_fee_30():
    assert withdraw(20000, 15000, "current", False) == 4970


def test_own_bank_large_amount_no_fee():
    assert withdraw(20000, 15000, "current", True) == 5000


# insufficient funds branch: True / False / boundary
def test_insufficient_funds():
    assert withdraw(500, 1000, "savings", True) == "insufficient funds"


def test_insufficient_funds_only_because_of_fee():
    # 1000 + 20 fee = 1020 > 1000
    assert withdraw(1000, 1000, "savings", False) == "insufficient funds"


def test_balance_exactly_equals_amount_plus_fee():
    assert withdraw(1020, 1000, "savings", False) == 0


# ================= pin_check =================
def test_correct_pin():
    assert pin_check(1234, 1234, 0) == "ok"


def test_correct_pin_on_last_allowed_attempt():
    assert pin_check(1234, 1234, 2) == "ok"


def test_blocked_with_three_attempts_even_if_pin_correct():
    assert pin_check(1234, 1234, 3) == "card blocked"


def test_blocked_with_more_than_three_attempts():
    assert pin_check(1111, 1234, 5) == "card blocked"


def test_wrong_pin_third_try_blocks_card():
    assert pin_check(1111, 1234, 2) == "card blocked"


def test_wrong_pin_first_try_retry():
    assert pin_check(1111, 1234, 0) == "retry"


def test_wrong_pin_second_try_retry():
    assert pin_check(1111, 1234, 1) == "retry"


# ================= note_breakup =================
def test_note_breakup_invalid_amount():
    with pytest.raises(ValueError):
        note_breakup(250)


def test_note_breakup_zero():
    assert note_breakup(0) == (0, 0, 0)


def test_note_breakup_only_100s():
    assert note_breakup(100) == (0, 0, 1)


def test_note_breakup_remaining_below_200_takes_else_branch():
    assert note_breakup(600) == (1, 0, 1)


def test_note_breakup_remaining_exactly_200():
    assert note_breakup(700) == (1, 1, 0)


def test_note_breakup_remaining_300_uses_200_and_100():
    assert note_breakup(800) == (1, 1, 1)


def test_note_breakup_remaining_400():
    assert note_breakup(900) == (1, 2, 0)


def test_note_breakup_exact_500s():
    assert note_breakup(1000) == (2, 0, 0)
