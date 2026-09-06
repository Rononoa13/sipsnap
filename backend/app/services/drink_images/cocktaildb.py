import httpx

from app.services.drink_images.base import DrinkImageProvider


class CocktailDBProvider(DrinkImageProvider):
    BASE_URL = "https://www.thecocktaildb.com/api/json/v1/1"

    def __init__(self, client: httpx.Client | None = None) -> None:
        self.client = client or httpx.Client()

    def find_image(self, drink_name: str) -> str | None:
        response = self.client.get(
            f"{self.BASE_URL}/search.php",
            params={"s": drink_name},
        )
        response.raise_for_status()

        data = response.json()
        drinks = data.get("drinks")

        if not drinks:
            return None

        return drinks[0].get("strDrinkThumb")