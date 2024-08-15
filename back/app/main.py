from fastapi import FastAPI

from back.app.user import user
app = FastAPI()
app.include_router(user.router)