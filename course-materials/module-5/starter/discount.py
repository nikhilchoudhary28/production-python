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

    try:
        conn.execute(
            "INSERT INTO redemptions (order_id, code, redeemed_at) VALUES (?, ?, ?)",
            (order_id, code, today),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise CouponAlreadyUsedError(f"Coupon {code} has already been used")

    return compute_discounted_total(order_total, discount_percent)
