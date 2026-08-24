from app.schemas.menu import Menu
from app.services.vision import VisionService


class MockVisionService(VisionService):
    """Deterministic vision service for development and tests."""

    async def extract_menu(self, image: bytes) -> Menu:
        return Menu(
            items=[
                {
                    "name": "Negroni",
                    "category": "Cocktail",
                    "description": None,
                },
                {
                    "name": "Old Fashioned",
                    "category": "Cocktail",
                    "description": None,
                },
            ]
        )