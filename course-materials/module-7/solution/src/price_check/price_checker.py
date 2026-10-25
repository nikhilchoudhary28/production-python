import asyncio
from price_check.pricing_api import fetch_price

async def fetch_one(sem: asyncio.Semaphore, sku: str) -> tuple[str, float | Exception]:
    """Acquires a slot in the semaphore before making the API call."""
    async with sem:
        try:
            price = await fetch_price(sku)
            return sku, price
        except Exception as e:
            return sku, e

async def check_all_prices(skus: list[str], max_concurrency: int = 4) -> dict[str, float]:
    """Checks prices concurrently, bounded strictly by max_concurrency."""
    sem = asyncio.Semaphore(max_concurrency)
    tasks = [fetch_one(sem, sku) for sku in skus]
    results = await asyncio.gather(*tasks)

    prices: dict[str, float] = {}
    for sku, result in results:
        if isinstance(result, Exception):
            print(f"Failed to price {sku}: {result}")
        else:
            prices[sku] = result

    return prices
