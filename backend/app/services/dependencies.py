from functools import lru_cache

from app.core.config import get_settings
from app.services.drink_images.cocktaildb import CocktailDBProvider
from app.services.drink_images.service import DrinkImageService
from app.services.gemini_vision import GeminiVisionService
from app.services.mock_vision import MockVisionService
from app.services.vision import VisionService


# Constructs what drinks are on the menu
@lru_cache
def get_vision_service() -> VisionService:
    settings = get_settings()

    print(f"VISION_PROVIDER = {settings.vision_provider}")

    if settings.vision_provider == "mock":
        return MockVisionService()

    if settings.vision_provider == "gemini":
        return GeminiVisionService(
            api_key=settings.gemini_api_key,
            model=settings.vision_model,
        )

    raise ValueError(f"Unsupported vision provider: {settings.vision_provider}")


# Constructs where can I get an image for this drink?
@lru_cache
def get_drink_image_service() -> DrinkImageService:
    settings = get_settings()

    return DrinkImageService(
        providers=[CocktailDBProvider()],
        cache_dir=settings.drink_image_cache_dir,
    )
