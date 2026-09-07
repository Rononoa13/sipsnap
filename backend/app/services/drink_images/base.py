from abc import ABC, abstractmethod


class DrinkImageProvider(ABC):
    @abstractmethod
    def find_image(self, drink_name: str) -> str | None:
        """Return an image URL for a drink, if available."""
        raise NotImplementedError
