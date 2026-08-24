import pytest
from pydantic import ValidationError

from app.schemas.menu import Menu


def test_valid_menu() -> None:
    menu = Menu(
        items=[
            {"name": "Negroni", "category": "Cocktail", "description": "None"},
        ]
    )
    assert menu.items[0].name == "Negroni"


def test_optional_fields_can_be_omitted() -> None:
    menu = Menu(
        items=[
            {"name": "Martini"},
        ]
    )
    assert menu.items[0].name == "Martini"
    assert menu.items[0].description is None


def test_empty_name_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Menu(items=[{"name": ""}])


def test_unknown_menu_item_field_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Menu(
            items=[
                {
                    "name": "Negroni",
                    "ingredients": "Gin, Campari, Vermouth",
                }
            ]
        )


def test_unknown_menu_field_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Menu(
            items=[],
            restaurant_name="Bar Bar",
        )


def test_menu_from_json() -> None:
    payload = {
        "items": [
            {"name": "Negroni", "description": "Gin, Campari, and sweet vermouth"},
            {"name": "Old Fashioned"},
        ]
    }
    menu = Menu.model_validate(payload)

    assert len(menu.items) == 2
    assert menu.items[0].name == "Negroni"
    assert menu.items[1].name == "Old Fashioned"
