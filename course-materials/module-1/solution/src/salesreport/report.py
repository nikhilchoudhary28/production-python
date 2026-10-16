"""Core business logic for calculating sales reports."""

import csv
import math
from pathlib import Path


def read_sales_rows(path: Path) -> list[dict[str, str]]:
    """Reads rows from a sales CSV file into a list of dictionaries.
    
    Using Path instead of str enforces type safety and prevents OS-specific slash errors.
    """
    rows: list[dict[str, str]] = []
    with open(path, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def validate_sales_rows(
    rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], dict[str, int]]:
    """Return valid rows and counts of each validation issue."""
    valid_rows: list[dict[str, str]] = []
    issue_counts = {
        "missing store_id": 0,
        "missing quantity": 0,
        "invalid quantity": 0,
    }

    for row in rows:
        row_issues: list[str] = []
        if not (row.get("store_id") or "").strip():
            row_issues.append("missing store_id")

        quantity = row.get("quantity")
        if not (quantity or "").strip():
            row_issues.append("missing quantity")
        else:
            try:
                valid_quantity = math.isfinite(float(quantity))
            except ValueError:
                valid_quantity = False
            if not valid_quantity:
                row_issues.append("invalid quantity")

        if row_issues:
            for issue in row_issues:
                issue_counts[issue] += 1
        else:
            valid_rows.append(row)

    return valid_rows, issue_counts


def sales_validation_summary(path: Path) -> str:
    """Build a summary of rows skipped during sales CSV validation."""
    rows = read_sales_rows(path)
    valid_rows, issue_counts = validate_sales_rows(rows)
    skipped = len(rows) - len(valid_rows)
    lines = [f"Rows skipped: {skipped}"]
    if not skipped:
        lines.append("  No invalid rows.")
    else:
        lines.extend(
            f"  {issue}: {count}"
            for issue, count in issue_counts.items()
            if count
        )
    return "\n".join(lines)


def total_revenue_by_store(rows: list[dict[str, str]]) -> dict[str, float]:
    """Calculates total revenue aggregated per store_id."""
    totals: dict[str, float] = {}
    for row in rows:
        store = row["store_id"]
        qty = int(row["quantity"])
        price = float(row["unit_price"])
        totals[store] = totals.get(store, 0.0) + (qty * price)
    return totals