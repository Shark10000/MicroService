from fastapi import APIRouter, Depends
from schemas.order_schemas import OrderIn
from orders_data_base.database import get_db
from sqlalchemy.orm import Session
from orders_data_base import crud
import httpx
from connect_to_au import connect_function

order_router = APIRouter()


@order_router.post('/order', status_code=200)
async def add_order(order: OrderIn, token: str, db: Session = Depends(get_db)):
    user = await connect_function.get_user(token)
    user_id = user[0]
    await crud.create_order(order, user_id, db)
    return


@order_router.get('/order')
async def get_order(id: int, db: Session = Depends(get_db)):
    return await crud.get_order(db, id)

