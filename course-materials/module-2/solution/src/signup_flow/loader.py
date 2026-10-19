"""Ingestion loader that enforces the schema boundary."""

import json
from pathlib import Path
from pydantic import ValidationError
from signup_flow.models import SignupRecord


def load_signup_records(path: Path) -> list[SignupRecord]:
    """Reads raw JSON and validates each record against the domain model."""
    with open(path, mode="r", encoding="utf-8") as f:
        raw_records = json.load(f)

    validated: list[SignupRecord] = []
    for idx, raw in enumerate(raw_records):
        try:
            validated.append(SignupRecord(**raw))
        except ValidationError as e:
            raise ValueError(
                f"Record at index {idx} is invalid:\n{e}\nRaw record: {raw}"
            ) from e

    return validated