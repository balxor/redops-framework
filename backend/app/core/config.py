from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "RedOps Framework API"
    app_version: str = "0.1.0"
    api_v1_prefix: str = "/api/v1"
    environment: str = "development"
    database_url: str = "sqlite:///./redops.db"
    database_auto_create: bool = True
    jwt_secret_key: str = "change-this-development-secret-key-32-bytes-minimum"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    bootstrap_admin_enabled: bool = True
    bootstrap_admin_email: str = "admin@example.com"
    bootstrap_admin_password: str = "admin-change-me"
    bootstrap_admin_full_name: str = "RedOps Admin"

    model_config = SettingsConfigDict(env_prefix="REDOPS_", env_file=".env")


settings = Settings()
