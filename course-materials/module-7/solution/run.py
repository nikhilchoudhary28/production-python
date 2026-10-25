import asyncio
import time
from price_check import check_all_prices, check_full_catalog

SKUS = [f"SKU-{i:04d}" for i in range(1, 51)]

def generate_large_catalog(count: int = 500) -> list[str]:
    return [f"CAT-{i:05d}" for i in range(1, count + 1)]

async def main() -> None:
    # 1. 50 SKUs bounded concurrency run
    start = time.perf_counter()
    prices = await check_all_prices(SKUS)
    elapsed = time.perf_counter() - start
    print(f"Priced {len(prices)} of {len(SKUS)} SKUs in {elapsed:.2f}s\n")

    # 2. Large catalog run with generator chunks
    print("Now processing a much larger catalog in chunks...")
    large_catalog = generate_large_catalog(500)
    start = time.perf_counter()
    catalog_prices = await check_full_catalog(large_catalog, chunk_size=50)
    elapsed = time.perf_counter() - start
    print(f"\nPriced {len(catalog_prices)} of {len(large_catalog)} catalog SKUs in {elapsed:.2f}s")

if __name__ == "__main__":
    asyncio.run(main())
