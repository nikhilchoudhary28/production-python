import os

from db import get_connection, get_quantity
from processor import apply_batch

DB_PATH = "warehouse.db"

ADJUSTMENTS = [
    {"adjustment_id": "adj-001", "sku": "WIDGET-A", "quantity_delta": 10},
    {"adjustment_id": "adj-002", "sku": "WIDGET-A", "quantity_delta": -3},
    {"adjustment_id": "adj-003", "sku": "WIDGET-B", "quantity_delta": 25},
]


def print_inventory(conn):
    print(f"  WIDGET-A: {get_quantity(conn, 'WIDGET-A')}")
    print(f"  WIDGET-B: {get_quantity(conn, 'WIDGET-B')}")


def main() -> None:
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = get_connection(DB_PATH)

    print("Applying batch (first run)...")
    apply_batch(conn, ADJUSTMENTS)
    print_inventory(conn)

    print()
    print("Applying the SAME batch again (e.g. a retry after a timeout)...")
    apply_batch(conn, ADJUSTMENTS)
    print_inventory(conn)


if __name__ == "__main__":
    main()
