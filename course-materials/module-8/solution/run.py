from report_svc import ReportServiceSettings, fetch_quarterly_revenue


def main() -> None:
    settings = ReportServiceSettings()

    print(f"Connecting to {settings.host}...")
    revenue = fetch_quarterly_revenue(settings.host, settings.password)

    print("Quarterly revenue report:")
    for quarter, total in revenue.items():
        print(f"  {quarter}: ${total:,.2f}")


if __name__ == "__main__":
    main()
