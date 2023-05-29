from fastapi import FastAPI
from users_database.database import engine
from users_database import db_models
from handler.user_router import user_router
from handler.token_router import token_router


db_models.Base.metadata.create_all(bind=engine)


def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(token_router, tags=['authentication'])
    application.include_router(user_router, tags=['authentication'])
    return application


app = get_application()
