from sqlalchemy.orm import Session
from . import db_models
from datetime import datetime
from fastapi import HTTPException


async def get_user(db: Session, username):
    if db.query(db_models.User).filter(db_models.User.username == username).first:
        return db.query(db_models.User).filter(db_models.User.username == username).first()
    else:
        return False


async def create_user(db, user):
    new_user = db_models.User(username=user.username,
                              email=user.email,
                              password_hash=user.password,
                              role='client',
                              created_at=datetime.now(),
                              updated_at=datetime.now(),
                              disabled=False)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return


async def change_roles(db, user, password):
    if password == '123':
        user.role = 'manager'
    elif password == '321':
        user.role = 'admin'
    else:
        raise HTTPException(status_code=403)
    db.commit()
