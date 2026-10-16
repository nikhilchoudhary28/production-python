"""Command-line interface for the salesreport tool."""

from pathlib import Path
import click

from salesreport.report import (
    read_sales_rows,
    sales_validation_summary,
    total_revenue_by_store,
)


@click.group()
def cli() -> None:
    """salesreport - daily store revenue reporting CLI."""
    pass


@cli.command()
@click.option(
    "--input",
    "input_path",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Path to the sales CSV file."
)
def generate(input_path: Path) -> None:
    """Print total revenue per store from a sales CSV."""
    rows = read_sales_rows(input_path)
    # 1. Execute core logic
    totals = total_revenue_by_store(rows)

    # 2. Format and present output
    click.echo("Revenue by store:")
    for store, revenue in totals.items():
        click.echo(f"  {store}: ${revenue:,.2f}")


@cli.command()
@click.option(
    "--input",
    "input_path",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Path to the sales CSV file.",
)
def validate(input_path: Path) -> None:
    """Check a sales CSV and report skipped rows and validation issues."""
    click.echo(sales_validation_summary(input_path))


if __name__ == "__main__":
    cli()