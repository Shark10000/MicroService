from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from users_database.database import get_db
from logic.create_tokens import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from schemas.user_schemas import Token
from typing import Annotated
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from logic.check_user import authenticate_user, get_current_active_user, get_password_hash


token_router = APIRouter()


@token_router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}