from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "RedOps Framework API"
    app_version: str = "0.1.0"
    api_v1_prefix: str = "/api/v1"
    environment: str = "development"

    model_config = SettingsConfigDict(env_prefix="REDOPS_", env_file=".env")


settings = Settings()

