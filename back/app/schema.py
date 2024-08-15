from pydantic import BaseModel,Field
from typing import List

class UserBase(BaseModel):
    username: str = Field(...,min_length=1,max_length=50)
    email: str = Field(...,min_length=1,max_length=50)

class HistoryBase(BaseModel):
    content: str = Field(...,min_length=1,max_length=50)
    owner_id: int

class UserCreate(UserBase):
    password: str = Field(...,min_length=1,max_length=50)

class HistoryCreate(HistoryBase):
    pass

class User(UserBase):
    id: int
    hashed_password: str = Field(...)
    history_list: List[HistoryBase] = []

    class Config:
        from_attributes = True

class History(HistoryBase):
    id: int

    class Config:
        from_attributes = True
