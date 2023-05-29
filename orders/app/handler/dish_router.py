from fastapi import APIRouter, Depends, HTTPException
from orders_data_base.database import get_db
from sqlalchemy.orm import Session
from connect_to_au import connect_function
from orders_data_base import crud
from schemas.dish_schemas import NewDishIn, DishIn

dish_router = APIRouter()


@dish_router.post('/dish/new', status_code=200)
async def add_new_dish(token, dish: NewDishIn, db: Session = Depends(get_db)):
    user = await connect_function.get_user(token)
    role = user[1]
    if role == 'manager' or role == 'admin':
        await crud.add_new_dish(db, dish)
    else:
        raise HTTPException(status_code=403, detail="Forbidden")
    return


@dish_router.post('/dish', status_code=200)
async def add_dish_quantity(token, dish: DishIn, db: Session = Depends(get_db)):
    user = await connect_function.get_user(token)
    role = user[1]
    if role == 'manager' or role == 'admin':
        await crud.add_dish_quantity(db, dish)
    else:
        raise HTTPException(status_code=403, detail="Forbidden")
    return


@dish_router.get('/dish', status_code=200)
async def watch_dish_by_id(token, name: str, db: Session = Depends(get_db)):
    user = await connect_function.get_user(token)
    role = user[1]
    if role == 'manager' or role == 'admin':
        return await crud.get_dish_by_name(db, name)
    else:
        raise HTTPException(status_code=403, detail="Forbidden")


@dish_router.delete('/dish', status_code=200)
async def delete_dish(token, name, db: Session = Depends(get_db)):
    user = await connect_function.get_user(token)
    role = user[1]
    if role == 'manager' or role == 'admin':
        try:
            await crud.delete_dish(db, name)
        except:
            raise HTTPException(status_code=400, detail='At first delete all connected entities')
    else:
        raise HTTPException(status_code=403, detail="Forbidden")
    return
