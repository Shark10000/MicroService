from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from enum import Enum


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class Roles(Enum):
    client = 'client'
    manager = 'manager'
    admin = 'admin'


class UserIn(BaseModel):
    username: constr(min_length=1, max_length=100)
    email: EmailStr | None = None


class User(UserIn):
    disabled: bool | None = None
    role: str
    created_at: datetime
    updated_at: datetime


class UserInDB(User):
    password_hash: str


class User_create(UserIn):
    password: constr(min_length=8, regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]+$')
