from app.schemas.gemini_schema import make_gemini_schema
from app.schemas.menu import Menu


def test_gemini_schema_removes_additional_properties():
    schema = make_gemini_schema(Menu)

    assert "additionalProperties" not in schema

    menu_item_schema = schema["$defs"]["MenuItem"]

    assert "additionalProperties" not in menu_item_schema


def test_gemini_schema_preserves_menu_structure():
    schema = make_gemini_schema(Menu)

    assert schema["type"] == "object"
    assert "items" in schema["properties"]

    items_schema = schema["properties"]["items"]

    assert items_schema["type"] == "array"
    assert "$ref" in items_schema["items"]


def test_gemini_schema_preserves_menu_item_fields():
    schema = make_gemini_schema(Menu)

    menu_item_schema = schema["$defs"]["MenuItem"]

    properties = menu_item_schema["properties"]

    assert "name" in properties
    assert "category" in properties
    assert "description" in properties

    assert "price" not in properties
