from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated


from app import schema,database
from app import crud,appouath2
from app.database import engine, Base

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
Base.metadata.create_all(bind=engine)
user = APIRouter(tags=["user"])


@user.get("/user",
          status_code=status.HTTP_200_OK,
          summary="get all users",
          description="返回包含所有user信息的列表",
          response_model=list[schema.User])
async def get_user(db:Session = Depends(database.get_db),limit:int = 50):
    user = crud.get_users(db,limit=limit)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user.get("/user/{user_id}",
          status_code=status.HTTP_200_OK,
          summary="Get user by id",
          description="以id为键获取用户",
          response_model=schema.User)
async def get_user(user_id:int,db:Session = Depends(database.get_db)):
    return crud.get_user_by_id(db, user_id)

@user.post("/user",
           status_code=status.HTTP_201_CREATED,
           summary="Create user",
           description="返回创建的用户",
           response_model=schema.User)
async def create_user(user:schema.UserCreate,db:Session = Depends(database.get_db)):
    if crud.get_user_by_email(db,user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db,user)

@user.post("/user/{user_id}/history",
          status_code=status.HTTP_200_OK,
          summary="post user history",
          description="为指定user创建历史记录",
          response_model=schema.History)
async def create_history(user_id:int,history:schema.HistoryCreate,db:Session = Depends(database.get_db)):
    return crud.create_history(db,user_id,history)

@user.get("/history",
          status_code=status.HTTP_200_OK,
          summary="get all history",
          response_model=list[schema.History])
async def get_history(limit:int=50,db:Session = Depends(database.get_db)):
    return crud.get_history(db,limit)

@user.get("/current/user",
          status_code=status.HTTP_200_OK,
          summary="get user by token",
          description="根据token获取当前用户信息")
async def get_user_me(db:Session = Depends(database.get_db),
                      token = Depends(oauth2_scheme)):
    payload = appouath2.token_decode(token)
    user_name = payload['sub']
    user = crud.get_user(db,user_name)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user.post("/login",
            status_code=status.HTTP_200_OK,
            summary="authenticate user",
            description="创建token"
            )
async def login(form_data: Annotated[OAuth2PasswordRequestForm,Depends()],
                db:Session = Depends(database.get_db)
                )->schema.Token:
    user_name:str = form_data.username
    user_password:str = form_data.password
    user = appouath2.authenticate_user(user_name, user_password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email or password",
                            headers={"WWW-Authenticate": "Bearer"})
    token_expire_time = appouath2.ACCESS_TOKEN_EXPIRE
    token = appouath2.create_access_token(
        {"sub": user_name},
        expires_delta=token_expire_time
        )
    return schema.Token(access_token=token,token_type="Bearer")
