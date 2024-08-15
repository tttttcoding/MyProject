from sqlalchemy.orm import Session

from back.app import models,schema
from back.app import appouath2

def get_users(db: Session, limit:int = 50):
    return db.query(models.User).limit(limit).all()

def gey_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schema.UserCreate):
    user = models.User(
        email=user.email,
        name=user.name,
        hashed_password=appouath2.create_hashed_password(user.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user