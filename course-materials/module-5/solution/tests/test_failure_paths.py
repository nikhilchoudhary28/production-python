"""Failure-path tests. Each one checks a SPECIFIC rejection reason, not
just 'something raised.' A test that only checks pytest.raises(Exception)
would pass even if the wrong failure path fired for the wrong reason -
these are deliberately more specific than that.
"""

import pytest

from discounts.db import get_connection, seed_coupon
from discounts.discount import (
    ExpiredCouponError,
    InvalidCouponError,
    MinimumOrderNotMetError,
    redeem_coupon,
)


def test_unknown_code_raises_invalid_coupon_error() -> None:
    conn = get_connection(":memory:")

    with pytest.raises(InvalidCouponError):
        redeem_coupon(conn, "DOES-NOT-EXIST", "order-1", 100.0, "2026-07-01")


def test_expired_coupon_raises_expired_coupon_error() -> None:
    conn = get_connection(":memory:")
    seed_coupon(conn, "OLD10", discount_percent=10.0, expires_at="2026-01-01", min_order_total=0.0)

    with pytest.raises(ExpiredCouponError):
        redeem_coupon(conn, "OLD10", "order-1", 100.0, "2026-07-01")


def test_order_below_minimum_raises_minimum_order_not_met_error() -> None:
    conn = get_connection(":memory:")
    seed_coupon(conn, "BIG50", discount_percent=50.0, expires_at="2026-12-31", min_order_total=200.0)

    with pytest.raises(MinimumOrderNotMetError):
        redeem_coupon(conn, "BIG50", "order-1", 50.0, "2026-07-01")


def test_order_exactly_at_minimum_is_accepted() -> None:
    """A boundary case: the minimum itself should be valid, not rejected.
    Worth testing explicitly - '>=' and '>' look almost identical in code
    but behave differently right at this exact value.
    """
    conn = get_connection(":memory:")
    seed_coupon(conn, "BIG50", discount_percent=50.0, expires_at="2026-12-31", min_order_total=200.0)

    result = redeem_coupon(conn, "BIG50", "order-1", 200.0, "2026-07-01")
    assert result == 100.0
