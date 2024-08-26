from sqlalchemy import Column, Integer, String , ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    email = Column(String(255), unique=True, index=True)
    username = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    history = relationship("History", back_populates="owner")

class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(255))

    owner = relationship("User", back_populates="history")
    owner_id = Column(Integer, ForeignKey("users.id"))