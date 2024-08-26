from pydantic import BaseModel,Field
from typing import List

class UserBase(BaseModel):
    username: str = Field(...,min_length=1,max_length=50)
    email: str = Field(...,min_length=1,max_length=50)

class HistoryBase(BaseModel):
    content: str = Field(...,min_length=1,max_length=50)

class UserCreate(UserBase):
    password: str = Field(...,min_length=1,max_length=50)

class HistoryCreate(HistoryBase):
    pass


class History(HistoryBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

class User(UserBase):
    id: int
    hashed_password: str = Field(...)
    history_list: List[History] = []

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    name: str|None = None
