from pydantic import BaseModel


class DishIn(BaseModel):
    name: str
    quantity: int


class NewDishIn(DishIn):
    description: str | None = None
    price: float

