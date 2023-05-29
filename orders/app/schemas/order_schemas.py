from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class Status(Enum):
    waiting = 'waiting'
    in_progress = 'in progress'
    canceled = 'canceled'
    completed = 'completed'


class OrderItem(BaseModel):
    dish_id: int
    quantity: int


class OrderIn(BaseModel):
    orders_list: list[OrderItem]
    special_requests: str


class Order(OrderIn):
    id: int | None = None
    user_id: int
    status: Status
    created_at: datetime
    updated_at: datetime
