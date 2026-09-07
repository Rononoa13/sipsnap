from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SipSnap"
    app_env: str = "dev"
    log_level: str = "INFO"

    vision_provider: str = "mock"
    gemini_api_key: str | None = None
    vision_model: str = "gemini-3.1-flash-lite"

    max_image_size_mb: int = 10

    drink_image_cache_dir: Path = Path("data/drink_images")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def max_image_size_bytes(self) -> int:
        return self.max_image_size_mb * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    return Settings()
