import pytest

from app.schemas.menu import Menu
from app.services.mock_vision import MockVisionService
from app.services.vision import VisionService


@pytest.mark.asyncio
async def test_mock_vision_service_implements_interface() -> None:
    service = MockVisionService()

    assert isinstance(service, VisionService)


@pytest.mark.asyncio
async def test_mock_vision_returns_menu() -> None:
    service = MockVisionService()

    menu = await service.extract_menu(b"fake-image-bytes")

    assert isinstance(menu, Menu)
    assert len(menu.items) == 2
    assert menu.items[0].name == "Negroni"
    assert menu.items[1].name == "Old Fashioned"