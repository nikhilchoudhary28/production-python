"""Idempotent batch processor for warehouse adjustments."""

from collections.abc import Sequence
from datetime import datetime, timezone
import sqlite3
from typing import TypedDict


class Adjustment(TypedDict):
    adjustment_id: str
    sku: str
    quantity_delta: int


class Recount(TypedDict):
    recount_id: str
    sku: str
    quantity: int


def apply_adjustment(conn: sqlite3.Connection, adjustment: Adjustment) -> bool:
    """Atomically records the adjustment ID. If new, updates inventory."""
    cursor = conn.cursor()
    now = datetime.now(timezone.utc).isoformat()

    # 1. Atomic gatekeeper: insert event ID
    cursor.execute(
        """
        INSERT INTO processed_events (adjustment_id, processed_at)
        VALUES (?, ?)
        ON CONFLICT (adjustment_id) DO NOTHING
        """,
        (adjustment["adjustment_id"], now),
    )

    # 2. Check if a conflict occurred (row already processed)
    if cursor.rowcount == 0:
        conn.commit()
        return False

    # 3. Event is guaranteed fresh: apply quantity delta
    sku = adjustment["sku"]
    delta = adjustment["quantity_delta"]

    cursor.execute(
        """
        INSERT INTO inventory (sku, quantity)
        VALUES (?, ?)
        ON CONFLICT (sku) DO UPDATE SET quantity = inventory.quantity + excluded.quantity
        """,
        (sku, delta),
    )
    conn.commit()
    return True


def apply_recount(conn: sqlite3.Connection, recount: Recount) -> bool:
    """Atomically records the recount ID. If new, sets the inventory quantity."""
    cursor = conn.cursor()
    now = datetime.now(timezone.utc).isoformat()

    cursor.execute(
        """
        INSERT INTO processed_recounts (recount_id, processed_at)
        VALUES (?, ?)
        ON CONFLICT (recount_id) DO NOTHING
        """,
        (recount["recount_id"], now),
    )

    if cursor.rowcount == 0:
        conn.commit()
        return False

    cursor.execute(
        """
        INSERT INTO inventory (sku, quantity)
        VALUES (?, ?)
        ON CONFLICT (sku) DO UPDATE SET quantity = excluded.quantity
        """,
        (recount["sku"], recount["quantity"]),
    )
    conn.commit()
    return True


def apply_batch(
    conn: sqlite3.Connection, adjustments: Sequence[Adjustment | Recount]
) -> tuple[int, int]:
    """Processes adjustments and recounts, returning applied and skipped counts."""
    applied = 0
    skipped = 0
    for adj in adjustments:
        if "recount_id" in adj:
            was_applied = apply_recount(conn, adj)
        else:
            was_applied = apply_adjustment(conn, adj)
        if was_applied:
            applied += 1
        else:
            skipped += 1
    return applied, skipped