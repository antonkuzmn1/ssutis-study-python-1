# database.py
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from config import DATABASE_URL
from src.models import Base

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
