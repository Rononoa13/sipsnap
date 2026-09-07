from pathlib import Path

import httpx

from app.services.drink_images.service import DrinkImageService


class FakeProvider:
    def find_image(self, drink_name: str) -> str | None:
        return "https://example.com/mojito.jpg"


# Cache miss
def test_downloads_and_caches_image(tmp_path: Path) -> None:
    transport = httpx.MockTransport(
        lambda request: httpx.Response(
            200,
            content=b"fake-image-data",
        )
    )

    client = httpx.Client(transport=transport)

    service = DrinkImageService(
        providers=[FakeProvider()],
        cache_dir=tmp_path,
        client=client,
    )

    result = service.find_image("Mojito")

    assert result == tmp_path / "mojito.jpg"
    assert result.read_bytes() == b"fake-image-data"


def test_returns_cached_image_without_calling_provider(
    tmp_path: Path,
) -> None:
    class FailingProvider:
        def find_image(self, drink_name: str) -> str | None:
            raise AssertionError("Provider should not be called")

    cached_image = tmp_path / "mojito.jpg"
    cached_image.write_bytes(b"cached-image")

    service = DrinkImageService(
        providers=[FailingProvider()],
        cache_dir=tmp_path,
        client=httpx.Client(
            transport=httpx.MockTransport(
                lambda request: httpx.Response(200, content=b"fake-image-data")
            )
        ),
    )

    result = service.find_image("Mojito")
    assert result == cached_image
    assert result.read_bytes() == b"cached-image"


#  Add provider fallback test
def test_uses_next_provider_when_first_provider_has_no_image(
    tmp_path: Path,
) -> None:
    class EmptyProvider:
        def find_image(self, drink_name: str) -> str | None:
            return None

    class SecondProvider:
        def find_image(self, drink_name: str) -> str | None:
            return "https://example.com/mojito.jpg"

    transport = httpx.MockTransport(
        lambda request: httpx.Response(
            200,
            content=b"fake-image-data",
        )
    )

    client = httpx.Client(transport=transport)

    service = DrinkImageService(
        providers=[
            EmptyProvider(),
            SecondProvider(),
        ],
        cache_dir=tmp_path,
        client=client,
    )

    result = service.find_image("Mojito")

    assert result == tmp_path / "mojito.jpg"
    assert result.read_bytes() == b"fake-image-data"


# Add the no-image test
def test_returns_none_when_no_provider_has_image(
    tmp_path: Path,
) -> None:
    class EmptyProvider:
        def find_image(self, drink_name: str) -> str | None:
            return None

    service = DrinkImageService(
        providers=[EmptyProvider()],
        cache_dir=tmp_path,
        client=httpx.Client(
            transport=httpx.MockTransport(
                lambda request: httpx.Response(200, content=b"fake-image-data")
            )
        ),
    )

    result = service.find_image("Unknown Drink")

    assert result is None
