from io import BytesIO
from pathlib import Path

import pytest

# API tests
from fastapi.testclient import TestClient
from PIL import Image

from app.main import app
from app.core.config import get_settings
from app.services.image_validator import (
    ImageValidationError,
    validate_image,
)
from app.services.dependencies import get_drink_image_service
# from app.services.drink_images.service import DrinkImageService

settings = get_settings()


def create_test_image(
    image_format: str = "JPEG",
) -> bytes:
    image = Image.new("RGB", (100, 100), color="white")

    buffer = BytesIO()
    image.save(buffer, format=image_format)

    return buffer.getvalue()


# Test JPEG
def test_valid_jpeg_is_accepted() -> None:
    image_bytes = create_test_image("JPEG")

    result = validate_image(
        image_bytes=image_bytes,
        filename="menu.jpg",
        content_type="image/jpeg",
        max_size_bytes=1024 * 1024,
    )

    assert result.filename == "menu.jpg"
    assert result.content_type == "image/jpeg"
    assert result.size_bytes == len(image_bytes)


# Test PNG
def test_valid_png_is_accepted() -> None:
    image_bytes = create_test_image("PNG")

    result = validate_image(
        image_bytes=image_bytes,
        filename="menu.png",
        content_type="image/png",
        max_size_bytes=1024 * 1024,
    )

    assert result.content_type == "image/png"


# Test WebP
def test_valid_webp_is_accepted() -> None:
    image_bytes = create_test_image("WEBP")

    result = validate_image(
        image_bytes=image_bytes,
        filename="menu.webp",
        content_type="image/webp",
        max_size_bytes=1024 * 1024,
    )

    assert result.content_type == "image/webp"


# Test unsupported format
def test_unsupported_mime_type_is_rejected() -> None:
    image_bytes = create_test_image("JPEG")

    with pytest.raises(ImageValidationError):
        validate_image(
            image_bytes=image_bytes,
            filename="menu.gif",
            content_type="image/gif",
            max_size_bytes=1024 * 1024,
        )


# Test empty file
def test_empty_file_is_rejected() -> None:
    with pytest.raises(ImageValidationError):
        validate_image(
            image_bytes=b"",
            filename="menu.jpg",
            content_type="image/jpeg",
            max_size_bytes=1024 * 1024,
        )


# Test oversized image
def test_oversized_file_is_rejected() -> None:
    image_bytes = create_test_image("JPEG")

    with pytest.raises(ImageValidationError):
        validate_image(
            image_bytes=image_bytes,
            filename="menu.jpg",
            content_type="image/jpeg",
            max_size_bytes=10,
        )


# Test corrupted image
def test_corrupted_image_is_rejected() -> None:
    corrupted_bytes = b"this is not actually an image"

    with pytest.raises(ImageValidationError):
        validate_image(
            image_bytes=corrupted_bytes,
            filename="menu.jpg",
            content_type="image/jpeg",
            max_size_bytes=1024 * 1024,
        )


client = TestClient(app)


def test_scan_accepts_valid_image() -> None:
    image_bytes = create_test_image("JPEG")

    response = client.post(
        "/api/scan",
        files={
            "image": (
                "menu.jpg",
                image_bytes,
                "image/jpeg",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert len(data["items"]) == 2

    assert data["items"][0]["name"] == "Negroni"
    assert data["items"][0]["description"] is None
    assert data["items"][0]["category"] == "Cocktail"


# Invalid file test
def test_scan_rejects_unsupported_format() -> None:
    image_bytes = create_test_image("JPEG")

    response = client.post(
        "/api/scan",
        files={
            "image": (
                "menu.gif",
                image_bytes,
                "image/gif",
            )
        },
    )

    assert response.status_code == 400


# API corrupted-image test
def test_scan_rejects_corrupted_image() -> None:
    response = client.post(
        "/api/scan",
        files={
            "image": (
                "menu.jpg",
                b"not an image",
                "image/jpeg",
            )
        },
    )

    assert response.status_code == 400


# Expect a Menu test
def test_scan_returns_menu_from_mock_vision() -> None:
    image_bytes = create_test_image("JPEG")

    response = client.post(
        "/api/scan",
        files={
            "image": (
                "menu.jpg",
                image_bytes,
                "image/jpeg",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["items"]) == 2

    assert data["items"][0]["name"] == "Negroni"

    assert data["items"][1]["name"] == "Old Fashioned"


"""
We can make this even stronger.

Create a test-specific VisionService:

class TestVisionService(VisionService):
    async def extract_menu(self, image: bytes) -> Menu:
        return Menu(
            items=[
                {
                    "name": "Test Drink",
                }
            ]
        )

app.dependency_overrides[get_vision_service] = (
    lambda: TestVisionService()
)
"""


class FakeDrinkImageService:
    def __init__(self, images: dict[str, Path] | None = None) -> None:
        self.images = images or {}

    def find_image(self, drink_name: str) -> Path | None:
        return self.images.get(drink_name)


@pytest.fixture
def fake_drink_image_service():
    app.dependency_overrides[get_drink_image_service] = lambda: FakeDrinkImageService()

    yield

    app.dependency_overrides.pop(get_drink_image_service, None)


def test_scan_returns_menu_with_drink_image() -> None:
    app.dependency_overrides[get_drink_image_service] = lambda: FakeDrinkImageService(
        images={"Negroni": Path("negroni.jpg")}
    )

    try:
        image_bytes = create_test_image("JPEG")

        response = client.post(
            "/api/scan",
            files={
                "image": (
                    "menu.jpg",
                    image_bytes,
                    "image/jpeg",
                )
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["items"][0]["name"] == "Negroni"
        assert data["items"][0]["image_url"] == "/drink-images/negroni.jpg"

        assert data["items"][1]["name"] == "Old Fashioned"
        assert data["items"][1]["image_url"] is None

    finally:
        app.dependency_overrides.pop(
            get_drink_image_service,
            None,
        )


# Write a static-file test
def test_drink_image_is_served_from_cache(
    tmp_path: Path,
) -> None:
    image_path = settings.drink_image_cache_dir / "negroni.jpg"
    image_path.parent.mkdir(parents=True, exist_ok=True)
    image_path.write_bytes(b"fake-image-data")

    try:
        response = client.get("/drink-images/negroni.jpg")

        assert response.status_code == 200
        assert response.content == b"fake-image-data"

    finally:
        image_path.unlink(missing_ok=True)
