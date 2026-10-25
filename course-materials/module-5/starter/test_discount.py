"""These tests are already in the project. They're all green.
Run them, then read Module 5's lab instructions before assuming
that means the code is correct.
"""

from unittest.mock import MagicMock

from discount import redeem_coupon


def test_redeem_coupon_works():
    mock_conn = MagicMock()
    mock_conn.execute.return_value.fetchone.return_value = (10.0, "2026-12-31", 20.0)

    result = redeem_coupon(mock_conn, "SAVE10", "order-1", 100.0, "2026-07-01")

    assert result is not None


def test_redeem_coupon_rejects_reuse():
    mock_conn = MagicMock()
    mock_conn.execute.return_value.fetchone.return_value = (10.0, "2026-12-31", 20.0)

    # First call succeeds
    redeem_coupon(mock_conn, "SAVE10", "order-1", 100.0, "2026-07-01")

    # Second call with the same order_id and code - simulate the DB
    # rejecting it, the way the real one would on a duplicate.
    import sqlite3
    mock_conn.execute.side_effect = [
        mock_conn.execute.return_value,  # the SELECT
        sqlite3.IntegrityError(),         # the INSERT, mocked to fail
    ]

    try:
        redeem_coupon(mock_conn, "SAVE10", "order-1", 100.0, "2026-07-01")
        assert False, "expected CouponAlreadyUsedError"
    except Exception:
        pass
