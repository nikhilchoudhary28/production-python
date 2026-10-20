from fx_client import reset
from rate_fetcher import get_rate_with_retry

PAIRS_NEEDED_FOR_TODAYS_BILLING_RUN = ["USD/EUR", "USD/GBP", "USD/XXX", "USD/INR"]


def main() -> None:
    reset()
    for pair in PAIRS_NEEDED_FOR_TODAYS_BILLING_RUN:
        print(f"Fetching {pair}...")
        try:
            rate = get_rate_with_retry(pair)
            print(f"  ok: {pair} = {rate}")
        except RuntimeError as e:
            print(f"  gave up: {e}")


if __name__ == "__main__":
    main()
