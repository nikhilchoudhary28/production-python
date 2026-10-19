"""Pipeline runner script."""

from pathlib import Path
from signup_flow.loader import load_signup_records
from signup_flow.processor import compute_trial_end_dates, count_by_plan


def main() -> None:
    data_path = Path("sample_signups.json")
    records = load_signup_records(data_path)

    print("Signup counts by plan:", count_by_plan(records))
    print("Trial end dates:", compute_trial_end_dates(records))


if __name__ == "__main__":
    main()