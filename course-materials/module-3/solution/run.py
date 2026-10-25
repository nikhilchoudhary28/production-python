"""Driver script processing billing currency pairs with dead-letter isolation."""

from fx_rates.dead_letter import DeadLetter
from fx_rates.exceptions import RateServiceError
from fx_rates.fx_client import reset
from fx_rates.rate_fetcher import get_rate

PAIRS = ["USD/EUR", "USD/GBP", "USD/XXX", "USD/INR"]


def main() -> None:
    reset()
    dead_letter = DeadLetter()
    results: dict[str, float] = {}

    for pair in PAIRS:
        print(f"Fetching {pair}...")
        try:
            rate = get_rate(pair)
            results[pair] = rate
            print(f"  ok: {pair} = {rate}") 
        except RateServiceError as exc:
            dead_letter.add(pair, str(exc))
            print(f"  [DEAD-LETTER] {pair}: {exc}")

    print(f"\nFetched {len(results)} rates successfully.")
    print(f"{len(dead_letter)} pair(s) sent to dead-letter:")
    for entry in dead_letter.entries:
        print(f"  - {entry['identifier']}: {entry['reason']}")


if __name__ == "__main__":
    main()