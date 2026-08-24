from functools import lru_cache

from app.core.config import get_settings
from app.services.mock_vision import MockVisionService
from app.services.vision import VisionService


@lru_cache
def get_vision_service() -> VisionService:
    settings = get_settings()

    if settings.vision_provider == "mock":
        return MockVisionService()

    raise ValueError(
        f"Unsupported vision provider: {settings.vision_provider}"
    )
