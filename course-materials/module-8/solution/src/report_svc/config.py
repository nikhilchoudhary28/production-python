from pydantic_settings import BaseSettings, SettingsConfigDict


class ReportServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="REPORT_DB_",
        extra="ignore",
    )

    host: str = "localhost"
    password: str  # Mandatory: No fallback allowed
