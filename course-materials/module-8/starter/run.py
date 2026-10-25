from config import get_db_host, get_db_password
from report_db import fetch_quarterly_revenue


def main() -> None:
    host = get_db_host()
    password = get_db_password()

    print(f"Connecting to {host}...")
    revenue = fetch_quarterly_revenue(host, password)

    print("Quarterly revenue report:")
    for quarter, total in revenue.items():
        print(f"  {quarter}: ${total:,.2f}")


if __name__ == "__main__":
    main()
