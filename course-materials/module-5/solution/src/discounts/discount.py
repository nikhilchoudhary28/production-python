import sqlite3


class InvalidCouponError(Exception):
    pass


class ExpiredCouponError(Exception):
    pass


class MinimumOrderNotMetError(Exception):
    pass


class CouponAlreadyUsedError(Exception):
    pass


def compute_discounted_total(order_total: float, discount_percent: float) -> float:
    discounted = order_total * (1 - discount_percent / 100)
    return round(max(0.0, discounted), 2)


def redeem_coupon(
    conn: sqlite3.Connection,
    code: str,
    order_id: str,
    order_total: float,
    today: str,
) -> float:
    row = conn.execute(
        "SELECT discount_percent, expires_at, min_order_total FROM coupons WHERE code = ?",
        (code,),
    ).fetchone()
    if row is None:
        raise InvalidCouponError(f"No such coupon: {code}")

    discount_percent, expires_at, min_order_total = row

    if today > expires_at:
        raise ExpiredCouponError(f"Coupon {code} expired on {expires_at}")

    if order_total < min_order_total:
        raise MinimumOrderNotMetError(
            f"Order total {order_total} is below the minimum {min_order_total} for {code}"
        )

    # The actual fix: atomic insert, same pattern as Module 4. The
    # PRIMARY KEY is on `code` now (see db.py), so this correctly
    # enforces "each code can only be used once" - not "each order can
    # only use one code," which is what the starter's constraint
    # accidentally enforced instead.
    cursor = conn.execute(
        "INSERT INTO redemptions (code, order_id, redeemed_at) "
        "VALUES (?, ?, ?) ON CONFLICT(code) DO NOTHING",
        (code, order_id, today),
    )
    if cursor.rowcount == 0:
        raise CouponAlreadyUsedError(f"Coupon {code} has already been used")

    conn.commit()
    return compute_discounted_total(order_total, discount_percent)
