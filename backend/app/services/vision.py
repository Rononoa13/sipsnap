from abc import ABC, abstractmethod

from app.schemas.menu import Menu


class VisionProviderError(Exception):
    """Custom exception for vision provider errors."""


class VisionService(ABC):
    """Interface for menu extraction using vision AI."""

    @abstractmethod
    async def extract_menu(self, image: bytes, content_type: str) -> Menu:
        """Extrace a structured menu from an image"""
        raise NotImplementedError
