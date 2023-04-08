from typing import Union
from urllib.parse import urlparse

from fastapi import FastAPI

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "asdf"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/times_two/{number}")
def times_two(number: int):
    return {"result": number * 2}
