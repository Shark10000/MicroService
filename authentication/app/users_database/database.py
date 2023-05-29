from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URI')
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:example@db/postgres"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db2 = SessionLocal()
    try:
        yield db2
    finally:
        db2.close()
