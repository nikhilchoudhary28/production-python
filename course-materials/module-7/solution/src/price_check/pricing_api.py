import asyncio
import random

_IN_FLIGHT_REQUESTS = 0
_MAX_CONCURRENT = 5

async def fetch_price(sku: str) -> float:
    global _IN_FLIGHT_REQUESTS
    _IN_FLIGHT_REQUESTS += 1
    
    if _IN_FLIGHT_REQUESTS > _MAX_CONCURRENT:
        _IN_FLIGHT_REQUESTS -= 1
        raise RuntimeError(
            f"Rejected request for {sku}: {_IN_FLIGHT_REQUESTS + 1} requests in flight, limit is {_MAX_CONCURRENT}"
        )
        
    await asyncio.sleep(0.05 + random.uniform(0.0, 0.02))
    _IN_FLIGHT_REQUESTS -= 1
    return round(10.0 + (hash(sku) % 9000) / 100.0, 2)
