"""Property-based test - instead of checking a handful of hand-picked
numbers, this asks hypothesis to generate hundreds of them, and checks
that an invariant holds for all of them: a discounted total should
never be negative, and should never exceed the original order total.
"""

from hypothesis import given
from hypothesis import strategies as st

from discounts.discount import compute_discounted_total


@given(
    order_total=st.floats(min_value=0, max_value=100_000, allow_nan=False, allow_infinity=False),
    discount_percent=st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False),
)
def test_discounted_total_is_always_between_zero_and_original(
    order_total: float, discount_percent: float
) -> None:
    result = compute_discounted_total(order_total, discount_percent)
    assert 0.0 <= result <= round(order_total, 2)
