"""Developer utility to validate live mock API batches against IngestionRecord."""

import json
import urllib.request

from pydantic import ValidationError

from pipeline.models import IngestionRecord


def main() -> None:
    url = "http://localhost:8000/records?date=2026-07-01&page=1"
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        payload = json.loads(response.read().decode("utf-8"))

    records = payload.get("records", [])
    valid_count = 0
    rejected_count = 0

    for idx, raw in enumerate(records):
        try:
            IngestionRecord(**raw)
            valid_count += 1
        except ValidationError as err:
            rejected_count += 1
            print(f"\n[REJECTED] Record at index {idx} failed validation:")
            print(err)

    print(f"\nSummary: {valid_count} valid, {rejected_count} rejected out of {len(records)} records.")


if __name__ == "__main__":
    main()