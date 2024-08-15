from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from back.app import schema,database
from back.app import crud
from back.app.database import engine, Base

Base.metadata.create_all(bind=engine)
user = APIRouter(tags=["user"])

@user.get("/user",response_model=schema.User)
async def get_user(db:Session = Depends(database.get_db())):
    user = crud.get_users()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.get_users(db)

@user.get("/user/{user_id}",response_model=schema.User)
async def get_user(user_id:int,db:Session = Depends(database.get_db())):
    return crud.get_user_by_id(db, user_id)

@user.post("/user",response_model=schema.User)
async def create_user(user:schema.UserCreate,db:Session = Depends(database.get_db())):
    pass