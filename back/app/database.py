from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session,declarative_base

SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:root@localhost:3306/project'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Session_local = sessionmaker(bind=engine,autocommit=False,autoflush=False)
Session = Session_local()

Base = declarative_base()

def get_db():
    try:
        yield Session
    finally:
        Session.close()
