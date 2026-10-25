"""Command-line interface entry point for the capstone ingestion pipeline."""

import click


@click.group()
def cli() -> None:
    """pipeline - Production-grade ingestion and transformation service."""


@cli.command()
@click.option(
    "--date",
    required=True,
    help="Target run date for ingestion (YYYY-MM-DD)."
)
def ingest(date: str) -> None:
    """Ingest records from the mock API for a given date."""
    click.echo(f"Would ingest records for {date} (not implemented yet)")


if __name__ == "__main__":
    cli()