from pathlib import Path

import httpx

from app.services.drink_images.base import DrinkImageProvider


class DrinkImageService:
    def __init__(self, providers: list[DrinkImageProvider], cache_dir: Path, client: httpx.Client) -> None:
        self.providers = providers
        self.cache_dir = cache_dir
        self.client = client or httpx.Client()

        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def find_image(self, drink_name: str) -> str | None:
        cache_path = self._cache_path(drink_name)

        if cache_path.exists():
            return cache_path

        image_url = self._find_image_url(drink_name)
        if image_url is None:
            return None

        self._download_image(image_url, cache_path)

        return cache_path

    def _find_image_url(self, drink_name: str) -> str | None:
        for provider in self.providers:
            image_url = provider.find_image(drink_name)
            if image_url is not None:
                return image_url
        return None

    def _cache_path(self, drink_name: str) -> Path:
        filename = drink_name.lower().replace(" ", "-")
        return self.cache_dir / f"{filename}.jpg"

    def _download_image(self, image_url: str, destination: Path) -> None:
        response = self.client.get(image_url)
        response.raise_for_status()

        destination.write_bytes(response.content)
