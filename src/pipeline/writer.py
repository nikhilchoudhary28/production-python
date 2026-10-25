"""Idempotent database writer inserting validated records into PostgreSQL warehouse."""

import json
from typing import Any

import psycopg

from pipeline.models import IngestionRecord

DATABASE_URL = "postgresql://pipeline_user:pipeline_pass_local_only@localhost:5432/warehouse"


def get_db_connection() -> psycopg.Connection[Any]:
    """Establishes connection to the warehouse database."""
    return psycopg.connect(DATABASE_URL)


def upsert_record(conn: psycopg.Connection[Any], record: IngestionRecord) -> bool:
    """Idempotently upserts an IngestionRecord into warehouse.records.

    Returns True if the operation succeeded without violating uniqueness.
    """
    query = """
        INSERT INTO warehouse.records (
            external_id,
            customer_id,
            amount,
            currency,
            status,
            source_created_at,
            source_updated_at,
            payload
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (external_id) DO UPDATE SET
            customer_id = EXCLUDED.customer_id,
            amount = EXCLUDED.amount,
            currency = EXCLUDED.currency,
            status = EXCLUDED.status,
            source_created_at = EXCLUDED.source_created_at,
            source_updated_at = EXCLUDED.source_updated_at,
            payload = EXCLUDED.payload;
    """
    with conn.cursor() as cur:
        cur.execute(
            query,
            (
                record.external_id,
                record.customer_id,
                record.amount,
                record.currency,
                record.status,
                record.source_created_at,
                record.source_updated_at,
                json.dumps(record.payload.model_dump()),
            ),
        )
    conn.commit()
    return True