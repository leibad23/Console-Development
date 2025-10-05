from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy import create_engine

from sqlmodel import SQLModel, Session, select

from database.schema import User
from utils.encode import hash_password
from setting.config_env import Settings

env_info = Settings()

sqlite_file = "database.db"
sqlite_url =f"sqlite:///{env_info.database_name}"
connect_args = {"check_same_thread":False}
engine = create_engine(sqlite_url ,connect_args= connect_args)


async def create_db_table():
    # can remove because im using alembic
    SQLModel.metadata.create_all(engine , checkfirst= True)

async def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session , Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("DB Is CURRENTLY RUNNING")
    await create_db_table()
    with Session(engine) as session:
      if not  session.exec(select(User)).first():
          session.add_all([
              User(email="leibad@gmail.com" , password=hash_password("lovesoup") ),
              User(email="keke33@gmail.com", password=hash_password("lovesoup2"))

          ])

          session.commit()
    yield

