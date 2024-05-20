# models.py
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL

Base = declarative_base()


class Item(Base):
    __tablename__ = "items"
    position = Column(Integer, primary_key=True)
    full_name = Column(String)
    logo_url = Column(String)
    total_goals = Column(Integer)
    penalty_goals = Column(Integer)
    matches = Column(Integer)


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
