"""Integration test - a real SQLite database, not a mock. This is the
test that actually catches the bug the starter code had: the same
coupon code, redeemed by two different orders, must be rejected the
second time.
"""

from discounts.db import get_connection, seed_coupon
from discounts.discount import CouponAlreadyUsedError, redeem_coupon


def test_same_code_cannot_be_used_by_two_different_orders() -> None:
    conn = get_connection(":memory:")
    seed_coupon(conn, "SAVE10", discount_percent=10.0, expires_at="2026-12-31", min_order_total=20.0)

    first_result = redeem_coupon(conn, "SAVE10", "order-1", 100.0, "2026-07-01")
    assert first_result == 90.0

    try:
        redeem_coupon(conn, "SAVE10", "order-2", 100.0, "2026-07-01")
        assert False, "expected CouponAlreadyUsedError for a second, different order"
    except CouponAlreadyUsedError:
        pass


def test_same_order_can_use_different_codes() -> None:
    """This is the actual, intended rule - one order can legitimately use
    more than one coupon over time, as long as each code is only used
    once, ever. This test would have caught the starter's bug from the
    other direction too: its wrong constraint would have blocked this.
    """
    conn = get_connection(":memory:")
    seed_coupon(conn, "SAVE10", discount_percent=10.0, expires_at="2026-12-31", min_order_total=20.0)
    seed_coupon(conn, "SAVE20", discount_percent=20.0, expires_at="2026-12-31", min_order_total=20.0)

    result_a = redeem_coupon(conn, "SAVE10", "order-1", 100.0, "2026-07-01")
    result_b = redeem_coupon(conn, "SAVE20", "order-1", 100.0, "2026-07-01")

    assert result_a == 90.0
    assert result_b == 80.0
