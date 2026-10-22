"""Sets up the inventory database. Given as-is - you don't need to edit
this file, you're extending what applies changes to it.
"""

import sqlite3


def get_connection(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS inventory (
            sku TEXT PRIMARY KEY,
            quantity INTEGER NOT NULL DEFAULT 0
        )
        """
    )
    conn.commit()
    return conn


def get_quantity(conn: sqlite3.Connection, sku: str) -> int:
    row = conn.execute("SELECT quantity FROM inventory WHERE sku = ?", (sku,)).fetchone()
    return row[0] if row else 0
