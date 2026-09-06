import httpx

from app.services.drink_images.cocktaildb import CocktailDBProvider


def test_find_image_returns_url() -> None:
    transport = httpx.MockTransport(
        lambda request: httpx.Response(
            200,
            json={
                "drinks": [
                    {
                        "strDrinkThumb": "https://example.com/image.jpg",
                    }
                ]
            },
        )
    )

    client = httpx.Client(transport=transport)
    provider = CocktailDBProvider(client=client)

    result = provider.find_image("Margarita")

    assert result == "https://example.com/image.jpg"


def test_find_image_returns_none_when_drink_not_found() -> None:
    transport = httpx.MockTransport(
        lambda request: httpx.Response(
            200,
            json={"drinks": None},
        )
    )

    client = httpx.Client(transport=transport)
    provider = CocktailDBProvider(client)

    result = provider.find_image("Unknown Drink")

    assert result is None