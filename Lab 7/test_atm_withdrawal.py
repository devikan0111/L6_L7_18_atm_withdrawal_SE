from hypothesis import given, strategies as st
from atm_withdrawal import notes_needed, mask_card, average_withdrawal


@given(st.text() | st.none())
def test_notes_needed_no_crash(s):
    try:
        notes_needed(s)
    except Exception as e:
        assert False, f"notes_needed crashed with: {e!r}"


@given(st.text() | st.none())
def test_mask_card_no_crash(s):
    try:
        mask_card(s)
    except Exception as e:
        assert False, f"mask_card crashed with: {e!r}"


@given(st.text() | st.none())
def test_average_withdrawal_no_crash(s):
    try:
        average_withdrawal(s)
    except Exception as e:
        assert False, f"average_withdrawal crashed with: {e!r}"


# ---- Extra: valid inputs must still give correct answers ----
@given(st.integers(min_value=0, max_value=10**9))
def test_notes_needed_correct(n):
    assert notes_needed(f"{n:,}") == n // 100


@given(st.lists(st.text(alphabet="0123456789", min_size=4, max_size=4),
                min_size=4, max_size=4))
def test_mask_card_correct(groups):
    assert mask_card(" ".join(groups)) == "XXXX XXXX XXXX " + groups[3]


@given(st.lists(st.integers(min_value=0, max_value=10**6), min_size=1))
def test_average_correct(nums):
    avg = average_withdrawal(",".join(map(str, nums)))
    assert min(nums) <= avg <= max(nums)
