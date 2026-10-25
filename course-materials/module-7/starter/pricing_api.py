"""A simulated third-party pricing service. You don't need to edit this
file. It has a real limit on how many requests it can handle at the
same time - exactly like a real service with a finite connection pool.
Send it too many requests at once, and it starts rejecting them.
"""

import asyncio

MAX_CONCURRENT_REQUESTS = 5

_in_flight = 0
_lock = asyncio.Lock()


class TooManyConcurrentRequestsError(Exception):
    pass


async def fetch_price(sku: str) -> float:
    global _in_flight

    async with _lock:
        _in_flight += 1
        current = _in_flight

    try:
        if current > MAX_CONCURRENT_REQUESTS:
            raise TooManyConcurrentRequestsError(
                f"Rejected request for {sku}: {current} requests in flight, "
                f"limit is {MAX_CONCURRENT_REQUESTS}"
            )
        await asyncio.sleep(0.05)
        return round(10.0 + (hash(sku) % 9000) / 100, 2)
    finally:
        async with _lock:
            _in_flight -= 1
