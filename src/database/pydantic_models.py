from pydantic import BaseModel


class MenuAndSubmenuItem(BaseModel):
    title: str | None
    description: str | None


class DishItem(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None