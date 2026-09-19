"""
Application configuration.

This module centralizes environment-based configuration for the
Communication Coach Agent application.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Attributes:
        app_name: Name of the application.
        app_env: Current application environment.
        debug: Whether debug mode is enabled.
        api_v1_prefix: Prefix used for versioned API routes.
        llm_provider: LLM provider name.
        llm_model: LLM model name.
        llm_api_key: API key used by the configured LLM provider.
        log_level: Application logging level.
    """

    app_name: str = "Communication Coach Agent"
    app_env: str = "development"
    debug: bool = False

    api_v1_prefix: str = "/api/v1"

    llm_provider: str = ""
    llm_model: str = ""
    llm_api_key: str = ""

    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return the cached application settings instance.

    Returns:
        Settings: Application configuration.
    """
    return Settings()