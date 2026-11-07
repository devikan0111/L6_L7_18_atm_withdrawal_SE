# ATM Withdrawal: Lab 6 (Code and Branch Coverage) and Lab 7 (Fuzz Testing)

**Name:** Devika N
**SRN:** PES1UG24AM080
**Course:** Software Engineering

This repository contains my work for Lab 6 and Lab 7 on the ATM withdrawal module.

## Repository structure

```
Lab 6/
  atm_withdrawal.py                      Module under test
  test_atm_withdrawal.py                 Starter tests (2 tests)
  CodeCoverageTest_atm_withdrawal.py     Tests for line coverage (13 tests)
  BranchCoverageTest_atm_withdrawal.py   Tests for branch coverage (31 tests)
  code_coverage.PNG                      Screenshot: line coverage report
  branch_coverage.PNG                    Screenshot: branch coverage report
Lab 7/
  atm_withdrawal.py                      Fixed (hardened) code
  test_atm_withdrawal.py                 Hypothesis fuzz tests
  1_buggy_output.png ... 4_passing_tests.png   Screenshots
  PES1UG24AM080_ScreenShots_Lab7.pdf     Screenshots PDF
```

## Setup

```
pip install coverage pytest hypothesis
```

---

## Lab 6: Code and Branch Coverage

The module `atm_withdrawal.py` has three functions:

| Function | What it does |
|----------|--------------|
| `withdraw(balance, amount, account_type, own_bank)` | Checks account type, amount validity, daily limit, other-bank fees and balance |
| `pin_check(entered, actual, attempts)` | Returns `ok`, `retry` or `card blocked` |
| `note_breakup(amount)` | Splits an amount into 500, 200 and 100 notes |

### How to run

Line coverage:
```
cd "Lab 6"
python -m coverage erase
python -m coverage run -m pytest CodeCoverageTest_atm_withdrawal.py
python -m coverage report -m
```

Branch coverage:
```
python -m coverage erase
python -m coverage run --branch -m pytest BranchCoverageTest_atm_withdrawal.py
python -m coverage report -m
```

### Results

| Stage | Tests | Coverage of `atm_withdrawal.py` |
|-------|-------|---------------------------------|
| Starter tests | 2 | 38% line |
| `CodeCoverageTest_atm_withdrawal.py` | 13 | 100% line |
| `BranchCoverageTest_atm_withdrawal.py` | 31 | 100% branch (22 of 22 branches) |

### What the branch tests add

Line coverage reached 100% with 13 tests, but branch coverage on the same tests still missed one branch (`14->16`, other bank with an amount of 10000 or less). The branch tests add:

- zero and negative amounts, and amounts that are not a multiple of 100
- daily limits for both account types, including the exact limit boundary
- other-bank fees: Rs. 20 for amounts up to 10000, Rs. 30 above 10000, and no fee for own bank
- balance exactly equal to amount plus fee, and insufficient funds caused only by the fee
- PIN checks on every attempt count, including a correct PIN after the card is already blocked
- note breakup for 0, 100, remainders below 200, exactly 200, 300 and 400

---

## Lab 7: Fuzz Testing with Hypothesis

The module has three functions that take text input: `notes_needed`, `mask_card` and `average_withdrawal`.

### How to run

```
cd "Lab 7"
python atm_withdrawal.py
python -m pytest test_atm_withdrawal.py
```

### Tests

`test_atm_withdrawal.py` has six Hypothesis tests:

- **Three no-crash tests**, one per function, using `st.text() | st.none()`. Each fails if the function raises any exception.
- **Three correctness tests** that check valid inputs still give the right answers.

### Bugs found by fuzzing

| Function | Input | Error in the original code |
|----------|-------|----------------------------|
| `notes_needed` | `''` | `ValueError` |
| `notes_needed` | `None` | `AttributeError` |
| `mask_card` | `''` | `IndexError` |
| `mask_card` | `None` | `AttributeError` |
| `average_withdrawal` | `''` | `ValueError` |
| `average_withdrawal` | `None` | `AttributeError` |

### Fix

Each function now checks that the input is a string, validates its format (digits only, or exactly 4 groups of 4 digits for a card number), and returns `None` for invalid input. `main()` prints `Invalid input` in that case.

### Results

| Version | Result |
|---------|--------|
| Original code | 3 failed, 3 passed |
| Fixed code | 6 passed |

---

## Notes

- Commands use `python -m coverage` and `python -m pytest` so they work even when the scripts folder is not on PATH (Windows).
- Cache files (`__pycache__`, `.coverage`, `.hypothesis`) are excluded with `.gitignore`.
