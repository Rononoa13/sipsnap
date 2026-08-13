"""
Menu
 └── items[]
       └── MenuItem
             ├── name
             ├── ...
"""

from pydantic import BaseModel, ConfigDict, Field


class MenuItem(BaseModel):
    """
    Represents a single menu item.
    """

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, description="The name of the menu item.")
    description: str | None = None


class Menu(BaseModel):
    """
    Represents a menu containing multiple menu items.
    """

    model_config = ConfigDict(extra="forbid")

    items: list[MenuItem]
