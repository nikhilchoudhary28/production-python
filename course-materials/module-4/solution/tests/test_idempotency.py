"""Automated verification proving that repeat execution produces identical state."""

import sqlite3
from inventory.db import get_connection, get_quantity
from inventory.processor import Adjustment, Recount, apply_batch


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


def test_recount_idempotency() -> None:
    conn = get_connection(":memory:")
    recounts: list[Recount] = [
        {"recount_id": "rec-101", "sku": "WIDGET-C", "quantity": 12},
    ]

    applied_1, skipped_1 = apply_batch(conn, recounts)
    qty_run_1 = get_quantity(conn, "WIDGET-C")

    applied_2, skipped_2 = apply_batch(conn, recounts)
    qty_run_2 = get_quantity(conn, "WIDGET-C")

    assert applied_1 == 1 and skipped_1 == 0
    assert applied_2 == 0 and skipped_2 == 1
    assert qty_run_1 == 12
    assert qty_run_2 == 12

    conn.close()


def test_recount_sets_quantity_instead_of_applying_delta() -> None:
    conn = get_connection(":memory:")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO inventory (sku, quantity) VALUES (?, ?)",
        ("WIDGET-C", 30),
    )
    conn.commit()

    applied, skipped = apply_batch(
        conn,
        [{"recount_id": "rec-102", "sku": "WIDGET-C", "quantity": 12}],
    )

    assert applied == 1 and skipped == 0
    assert get_quantity(conn, "WIDGET-C") == 12

    conn.close()