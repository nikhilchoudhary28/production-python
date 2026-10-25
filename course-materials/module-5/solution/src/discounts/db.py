"""Sets up the coupon database. The fix for this module's bug lives in
one word in this file: the UNIQUE constraint is now on `code`, not
`order_id`. Compare this to starter/db.py directly.
"""

import sqlite3


def get_connection(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS coupons (
            code TEXT PRIMARY KEY,
            discount_percent REAL NOT NULL,
            expires_at TEXT NOT NULL,
            min_order_total REAL NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS redemptions (
            code TEXT PRIMARY KEY,
            order_id TEXT NOT NULL,
            redeemed_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    return conn


def seed_coupon(
    conn: sqlite3.Connection,
    code: str,
    discount_percent: float,
    expires_at: str,
    min_order_total: float,
) -> None:
    conn.execute(
        "INSERT OR REPLACE INTO coupons (code, discount_percent, expires_at, min_order_total) "
        "VALUES (?, ?, ?, ?)",
        (code, discount_percent, expires_at, min_order_total),
    )
    conn.commit()
