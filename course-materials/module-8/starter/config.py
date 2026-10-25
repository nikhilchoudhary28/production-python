import os


def get_db_host() -> str:
    return os.environ.get("REPORT_DB_HOST", "localhost")


def get_db_password() -> str:
    return os.environ.get("REPORT_DB_PASSWORD", "dev_only_pw_2019")
