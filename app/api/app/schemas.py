from typing import Union
from pydantic import BaseModel, validator


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class Model(BaseModel):
    id: int
    name: str
    selected: Union[bool, None]

    @validator('selected')
    def empty_str_to_none(cls, v):
        if v is None:
            return False
        return v

    class Config:
        orm_mode = True
