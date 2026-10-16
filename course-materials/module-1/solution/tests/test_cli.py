import csv

from click.testing import CliRunner

from salesreport.cli import cli


def test_validate_reports_skipped_rows_and_reasons(tmp_path):
    input_path = tmp_path / "sales.csv"
    with input_path.open("w", newline="", encoding="utf-8") as sales_file:
        writer = csv.DictWriter(
            sales_file,
            fieldnames=["store_id", "date", "item", "quantity", "unit_price"],
        )
        writer.writeheader()
        writer.writerows(
            [
                {
                    "store_id": "S001",
                    "date": "2026-07-01",
                    "item": "widget",
                    "quantity": "2",
                    "unit_price": "3.50",
                },
                {
                    "store_id": "",
                    "date": "2026-07-01",
                    "item": "widget",
                    "quantity": "2",
                    "unit_price": "3.50",
                },
                {
                    "store_id": "S002",
                    "date": "2026-07-01",
                    "item": "widget",
                    "quantity": "",
                    "unit_price": "3.50",
                },
                {
                    "store_id": "S003",
                    "date": "2026-07-01",
                    "item": "widget",
                    "quantity": "two",
                    "unit_price": "3.50",
                },
                {
                    "store_id": "",
                    "date": "2026-07-01",
                    "item": "widget",
                    "quantity": "not-a-number",
                    "unit_price": "3.50",
                },
            ]
        )

    result = CliRunner().invoke(cli, ["validate", "--input", str(input_path)])

    assert result.exit_code == 0
    assert result.output == (
        "Rows skipped: 4\n"
        "  missing store_id: 2\n"
        "  missing quantity: 1\n"
        "  invalid quantity: 2\n"
    )
