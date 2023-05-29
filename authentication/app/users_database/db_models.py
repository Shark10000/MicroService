from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean


from .database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    email = Column(String, index=True)
    password_hash = Column(String, index=True)
    role = Column(String, index=True)
    created_at = Column(TIMESTAMP, index=True)
    updated_at = Column(TIMESTAMP, index=True)
    disabled = Column(Boolean)

