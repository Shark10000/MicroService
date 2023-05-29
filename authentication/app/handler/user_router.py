from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from users_database.database import get_db
from typing import Annotated
from schemas.user_schemas import User, User_create, Token
from logic.check_user import authenticate_user, get_current_active_user, get_password_hash, get_current_user_by_token
from users_database.crud import create_user, change_roles

user_router = APIRouter()


@user_router.get("/users/me", response_model=User)
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user.__dict__


@user_router.get("/users/me/role", status_code=200)
async def read_own_items(
        current_user: Annotated[User, Depends(get_current_active_user)]
):
    return [current_user.id, current_user.role]


@user_router.post("/users", status_code=200)
async def sign_up(user: User_create, db: Session = Depends(get_db)):
    user.password = get_password_hash(user.password)
    await create_user(db, user)
    return


@user_router.get('/users/check', status_code=200)
async def get_user_by_token(token: str, db: Session = Depends(get_db)):
    user = await get_current_user_by_token(token, db)
    user_id = user.id
    role = user.role
    return [user_id, role]


@user_router.post('/users/me/role', status_code=200)
async def change_role(password: str,
                      current_user: Annotated[User, Depends(get_current_active_user)], db: Session = Depends(get_db)
                      ):
    await change_roles(db, current_user, password)
    return
