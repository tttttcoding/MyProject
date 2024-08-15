from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..schema import User
from .. import crud

user = APIRouter(tags=["user"])

@user.get("/user")
async def get_user(db:Session = Depends()):
    return crud.get_user(db)

@user.get("/user/{user_id}")
async def get_user(user_id:int,db:Session = Depends()):
    return crud.get_user_by_id(db, user_id)

@user.post("/user")
async def create_user(user:User,db:Session = Depends()):
    return crud.create_user(db,user)