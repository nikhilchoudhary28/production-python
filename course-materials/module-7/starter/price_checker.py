import asyncio
from pricing_api import fetch_price

async def fetch_one(sem: asyncio.Semaphore, sku: str) -> tuple[str, float | Exception]:
    """Acquires a semaphore slot before making the API call.
    
    If 4 requests are actively running, any extra task waits here 
    until an active request finishes.
    """
    async with sem:
        try:
            price = await fetch_price(sku)
            return sku, price
        except Exception as e:
            return sku, e

async def check_all_prices(skus: list[str], max_concurrency: int = 4) -> dict[str, float]:
    """Dispatches requests concurrently while strictly bounding concurrency to 4."""
    sem = asyncio.Semaphore(max_concurrency)

    # Pass the semaphore to every worker coroutine
    tasks = [fetch_one(sem, sku) for sku in skus]
    results = await asyncio.gather(*tasks)

    prices: dict[str, float] = {}
    for sku, result in results:
        if isinstance(result, Exception):
            print(f"Failed to price {sku}: {result}")
        else:
            prices[sku] = result

    return prices