from fastapi import APIRouter, Depends
from orders_data_base.database import get_db
from sqlalchemy.orm import Session
from orders_data_base import crud


menu_router = APIRouter()


@menu_router.get('/menu', status_code=200)
async def get_menu(db: Session = Depends(get_db)):
    return await crud.get_menu(db)
