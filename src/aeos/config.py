from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    environment: str = "dev"
    log_level: str = "INFO"
    max_agent_retries: int = 3
    workspace_root: str | None = None
    github_api_url: str = "https://api.github.com"
    github_token: str | None = None

    model_config = SettingsConfigDict(
        env_prefix="AEOS_",
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
