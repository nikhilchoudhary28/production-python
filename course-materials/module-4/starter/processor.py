import sqlite3

from db import get_quantity


def apply_adjustment(conn: sqlite3.Connection, adjustment: dict) -> None:
    sku = adjustment["sku"]
    current = get_quantity(conn, sku)
    new_quantity = current + adjustment["quantity_delta"]
    conn.execute(
        """
        INSERT INTO inventory (sku, quantity) VALUES (?, ?)
        ON CONFLICT(sku) DO UPDATE SET quantity = ?
        """,
        (sku, new_quantity, new_quantity),
    )
    conn.commit()


def apply_batch(conn: sqlite3.Connection, adjustments: list[dict]) -> None:
    for adjustment in adjustments:
        apply_adjustment(conn, adjustment)
