from fastapi import FastAPI, Request
from . import dish_router
from . import order_router
from . import menu_router
from orders_data_base import data_base_models
from orders_data_base.database import engine
import asyncio
from orders_data_base import crud
from orders_data_base import database

info = {}

data_base_models.Base.metadata.create_all(bind=engine)


def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(order_router.order_router, prefix='/orderservice', tags=['orders'])
    application.include_router(menu_router.menu_router, prefix='/orderservice', tags=['orders'])
    application.include_router(dish_router.dish_router, prefix='/orderservice', tags=['orders'])
    return application


app = get_application()


async def manage_orders():
    while True:
        db = database.SessionLocal()
        await crud.manage_orders(db)
        db.close()
        await asyncio.sleep(180)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(manage_orders())

