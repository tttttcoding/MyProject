from sqlalchemy.orm import Session

from .. import models,schema

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def gey_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()