"""Database connection and table management."""

import sqlite3


def get_connection(db_path: str = "warehouse.db") -> sqlite3.Connection:
    """Creates a connection and initializes both the domain and tracking tables."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Domain table storing current stock
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            sku TEXT PRIMARY KEY,
            quantity INTEGER NOT NULL DEFAULT 0
        )
    """)

    # Tracking table enforcing atomic idempotency per adjustment_id
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS processed_events (
            adjustment_id TEXT PRIMARY KEY,
            processed_at TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn


def get_quantity(conn: sqlite3.Connection, sku: str) -> int:
    """Returns current inventory quantity for a SKU or 0 if missing."""
    cursor = conn.cursor()
    cursor.execute("SELECT quantity FROM inventory WHERE sku = ?", (sku,))
    row = cursor.fetchone()
    return int(row[0]) if row else 0