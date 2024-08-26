from datetime import datetime, timedelta

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app import crud

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "2662403732ae678a385224b1807a9eb3245f33508c9893a918fab707c435b89f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = 3600


def create_hashed_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str,db:Session):
    user = crud.get_user(db, username=username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401,detail="Incorrect username or password")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401,detail="Incorrect password")
    return user

def create_access_token(data: dict,expires_delta:int|None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(seconds=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def token_decode(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Token error",
                            headers={"WWW-Authenticate": "Bearer"})