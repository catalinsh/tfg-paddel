from sqlalchemy import Column, Integer, String, Boolean, Null

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    removable = Column(Boolean, default=True, nullable=False)

class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    path = Column(String, unique=True, nullable=False)
    selected = Column(Boolean, unique=True, default=None)
