"""Idempotent batch processor for warehouse adjustments."""

from datetime import datetime, timezone
import sqlite3
from typing import TypedDict


class Adjustment(TypedDict):
    adjustment_id: str
    sku: str
    quantity_delta: int


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


def apply_batch(
    conn: sqlite3.Connection, adjustments: list[Adjustment]
) -> tuple[int, int]:
    """Processes a list of adjustments, returning (applied_count, skipped_count)."""
    applied = 0
    skipped = 0
    for adj in adjustments:
        if apply_adjustment(conn, adj):
            applied += 1
        else:
            skipped += 1
    return applied, skipped