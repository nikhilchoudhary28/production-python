from collections.abc import Iterator
from price_check.price_checker import check_all_prices

def iter_sku_chunks(skus: list[str], chunk_size: int = 50) -> Iterator[list[str]]:
    """Yields manageable chunks of SKUs without keeping all task objects in RAM."""
    chunk: list[str] = []
    for sku in skus:
        chunk.append(sku)
        if len(chunk) == chunk_size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk

async def check_full_catalog(
    catalog: list[str],
    chunk_size: int = 50,
    max_concurrency: int = 4,
) -> dict[str, float]:
    """Consumes chunks sequentially to avoid memory spikes."""
    all_prices: dict[str, float] = {}

    for i, chunk in enumerate(iter_sku_chunks(catalog, chunk_size=chunk_size), start=1):
        print(f"Processing chunk {i}: {len(chunk)} SKUs")
        chunk_prices = await check_all_prices(chunk, max_concurrency=max_concurrency)
        all_prices.update(chunk_prices)

    return all_prices
