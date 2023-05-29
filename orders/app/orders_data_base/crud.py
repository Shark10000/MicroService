import json

from sqlalchemy.orm import Session, joinedload
from . import data_base_models
from datetime import datetime
from fastapi import HTTPException


async def get_order(db: Session, id: int):
    order = db.query(data_base_models.Orders).filter(data_base_models.Orders.id == id).first()
    dishes = db.query(data_base_models.order_dish).filter(data_base_models.order_dish.order_id == order.id).all()
    order = json.dumps({'id': order.id,
                        'user_id': order.user_id,
                        'status': order.status,
                        'special_requests': order.special_requests,
                        'created_at': str(order.created_at),
                        'updated_at': str(order.updated_at),
                        'orders_list': [(dish.dish_id, str(dish.price)) for dish in dishes]})
    return order


async def create_order(order, user_id, db):
    db_order = data_base_models.Orders(user_id=user_id,
                                       status='waiting',
                                       special_requests=order.special_requests,
                                       created_at=datetime.now(),
                                       updated_at=datetime.now(),
                                       )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    for item in order.orders_list:
        dish_info = db.query(data_base_models.Dish).filter(data_base_models.Dish.id == item.dish_id).first()
        if dish_info.quantity < item.quantity:
            db_order.status = 'canceled'
            db.commit()
            db.refresh(db_order)
            return
    for item in order.orders_list:
        dish_info = db.query(data_base_models.Dish).filter(data_base_models.Dish.id == item.dish_id).first()
        dish_info.quantity = dish_info.quantity - item.quantity
        db.commit()
        db.refresh(dish_info)
        db_order_dish = data_base_models.order_dish(
            order_id=db_order.id,
            dish_id=item.dish_id,
            quantity=item.quantity,
            price=dish_info.price
        )
        db.add(db_order_dish)
    db.commit()


async def add_new_dish(db, dish):
    dish = data_base_models.Dish(name=dish.name,
                                 description=dish.description,
                                 price=dish.price,
                                 quantity=dish.quantity)

    db.add(dish)
    db.commit()
    db.refresh(dish)


async def add_dish_quantity(db, dish):
    db_dish = db.query(data_base_models.Dish).filter(data_base_models.Dish.name == dish.name).first()
    if db_dish:
        db_dish.quantity = db_dish.quantity + dish.quantity
        if db_dish.quantity < 0:
            db_dish.quantity = 0
        db.commit()
        db.refresh(db_dish)
    else:
        raise HTTPException(status_code=404, detail='Not found in list of dishes')


async def delete_dish(db, name):
    db.query(data_base_models.Dish).filter(data_base_models.Dish.name == name).delete()
    db.commit()


async def get_dish_by_name(db, name):
    return db.query(data_base_models.Dish).filter(data_base_models.Dish.name == name).first()


async def get_menu(db):
    return db.query(data_base_models.Dish).filter(data_base_models.Dish.quantity != 0).all()


async def manage_orders(db):
    orders = db.query(data_base_models.Orders).filter(
        data_base_models.Orders.status != 'completed' and data_base_models.Orders.status != 'canceled').all()
    for order in orders:
        if order.status == 'waiting':
            order.status = 'in progress'
            order.updated_at = datetime.now()
        elif order.status == 'in progress':
            order.status = 'completed'
            order.updated_at = datetime.now()
        db.commit()
        db.refresh(order)
    return
