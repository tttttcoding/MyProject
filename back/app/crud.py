from sqlalchemy.orm import Session
from fastapi import HTTPException

from app import models,schema
from app import appouath2

def get_users(db: Session, limit:int):
    return db.query(models.User).limit(limit).all()

def get_user(db: Session, username:str):
    return db.query(models.User).filter(models.User.username == username).first()

def gey_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schema.UserCreate):
    user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=appouath2.create_hashed_password(user.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_history(db: Session, user_id: int ,history: schema.HistoryCreate):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    history = models.History(
        owner_id=user.id,
        content=history.content,
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    return history

def get_history(db: Session,limit:int):
    return db.query(models.History).limit(limit).all()
