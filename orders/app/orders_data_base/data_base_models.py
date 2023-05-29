from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, DECIMAL
from sqlalchemy.orm import relationship

from .database import Base


class Dish(Base):
    __tablename__ = 'dish'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(DECIMAL, index=True)
    quantity = Column(Integer, index=True)
    dep = relationship("order_dish", backref='dish')


class Orders(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    status = Column(String, index=True)
    special_requests = Column(String, index=True)
    created_at = Column(TIMESTAMP, index=True)
    updated_at = Column(TIMESTAMP, index=True)
    order_list = relationship("order_dish", backref="orders")


class order_dish(Base):
    __tablename__ = "order_dish"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    dish_id = Column(Integer, ForeignKey('dish.id'))
    quantity = Column(Integer, index=True)
    price = Column(DECIMAL)
