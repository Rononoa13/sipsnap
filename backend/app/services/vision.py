from abc import abstractmethod

from app.schemas.menu import Menu


class VisionService:
    """Interface for menu extraction using vision AI."""

    @abstractmethod
    async def extract_menu(self, image: bytes) -> Menu:
        """Extrace a structured menu from an image"""
        raise NotImplementedError
    