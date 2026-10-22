"""Demonstration script showing repeatable, idempotent execution."""

import os
from inventory.db import get_connection, get_quantity
from inventory.processor import Adjustment, apply_batch

ADJUSTMENTS: list[Adjustment] = [
    {"adjustment_id": "adj-001", "sku": "WIDGET-A", "quantity_delta": 10},
    {"adjustment_id": "adj-002", "sku": "WIDGET-A", "quantity_delta": -3},
    {"adjustment_id": "adj-003", "sku": "WIDGET-B", "quantity_delta": 25},
]


def main() -> None:
    db_file = "warehouse.db"
    if os.path.exists(db_file):
        os.remove(db_file)

    conn = get_connection(db_file)

    print("Applying batch (first run)...")
    applied, skipped = apply_batch(conn, ADJUSTMENTS)
    print(f"  Batch 1: applied={applied}, skipped={skipped}")
    print(f"  WIDGET-A: {get_quantity(conn, 'WIDGET-A')}")
    print(f"  WIDGET-B: {get_quantity(conn, 'WIDGET-B')}")

    print("\nApplying the SAME batch again (e.g. a retry after a timeout)...")
    applied, skipped = apply_batch(conn, ADJUSTMENTS)
    print(f"  Batch 2: applied={applied}, skipped={skipped}")
    print(f"  WIDGET-A: {get_quantity(conn, 'WIDGET-A')}")
    print(f"  WIDGET-B: {get_quantity(conn, 'WIDGET-B')}")

    conn.close()


if __name__ == "__main__":
    main()