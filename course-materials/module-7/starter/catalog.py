from collections.abc import Iterator
from price_checker import check_all_prices


def iter_sku_chunks(skus: list[str], chunk_size: int = 50) -> Iterator[list[str]]:
    """Yields manageable slices of SKUs without holding the entire catalog's

    coroutine tasks in memory at once.
    """
    chunk: list[str] = []
    for sku in skus:
        chunk.append(sku)
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []
    # Yield any remaining tail items
    if chunk:
        yield chunk


async def check_full_catalog(
    catalog: list[str],
    chunk_size: int = 50,
    max_concurrency: int = 4,
) -> dict[str, float]:
    """Processes large catalogs safely:

    1. Generator yields 50 SKUs at a time.
    2. Check_all_prices processes those 50 with Semaphore(4).
    3. Results are aggregated, memory for those tasks is freed, and the next chunk runs.
    """
    all_prices: dict[str, float] = {}

    for i, chunk in enumerate(
        iter_sku_chunks(catalog, chunk_size=chunk_size), start=1
    ):
        print(f"Processing chunk {i}: {len(chunk)} SKUs")
        chunk_prices = await check_all_prices(
            chunk, max_concurrency=max_concurrency
        )
        all_prices.update(chunk_prices)

    return all_prices