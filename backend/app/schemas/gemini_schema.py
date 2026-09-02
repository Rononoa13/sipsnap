from typing import Any


def make_gemini_schema(model: type) -> dict[str, Any]:
    """
    Create a Gemini schema for the given Pydantic model.

    """
    # Implementation for creating Gemini schema
    schema = model.model_json_schema()
    _remove_unsupported_fields(schema)
    return schema


def _remove_unsupported_fields(value: Any) -> None:
    if isinstance(value, dict):
        value.pop("additionalProperties", None)

        for child in value.values():
            _remove_unsupported_fields(child)

    elif isinstance(value, list):
        for child in value:
            _remove_unsupported_fields(child)
