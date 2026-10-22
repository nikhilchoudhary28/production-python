"""Automated verification proving that repeat execution produces identical state."""

import sqlite3
from inventory.db import get_quantity
from inventory.processor import Adjustment, apply_batch


def test_batch_idempotency() -> None:
    # Use in-memory SQLite for test isolation
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE inventory (
            sku TEXT PRIMARY KEY,
            quantity INTEGER NOT NULL DEFAULT 0
        )
    """)
    cursor.execute("""
        CREATE TABLE processed_events (
            adjustment_id TEXT PRIMARY KEY,
            processed_at TEXT NOT NULL
        )
    """)
    conn.commit()

    adjustments: list[Adjustment] = [
        {"adjustment_id": "adj-101", "sku": "WIDGET-C", "quantity_delta": 20},
        {"adjustment_id": "adj-102", "sku": "WIDGET-C", "quantity_delta": 5},
    ]

    # First run
    applied_1, skipped_1 = apply_batch(conn, adjustments)
    qty_run_1 = get_quantity(conn, "WIDGET-C")

    # Second run (exact same batch)
    applied_2, skipped_2 = apply_batch(conn, adjustments)
    qty_run_2 = get_quantity(conn, "WIDGET-C")

    # Assertions
    assert applied_1 == 2 and skipped_1 == 0
    assert applied_2 == 0 and skipped_2 == 2
    assert qty_run_1 == 25
    assert qty_run_2 == 25
    assert qty_run_1 == qty_run_2

    conn.close()