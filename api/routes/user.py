import datetime

from fastapi import HTTPException, Query , Request , APIRouter
from fastapi.params import Depends
from pydantic import EmailStr
from sqlalchemy import func

from sqlmodel import select
from starlette import status

from database.config import SessionDep
from database.resSchema import  UserRes, UserCreate, ReponseG, PaginationG
from database.schema import User
from utils.encode import hash_password, get_current_user

user_route = APIRouter(tags=["User"])

@user_route.get("/")
async def its_running():
    return{"msg": f" We UP My B000000000000000000000yyyyyyyyyyyy{datetime.date}"}


@user_route.get("/users" ,response_model=PaginationG[list[UserRes]]  )
async def get_all_users( session :SessionDep, res :Request , page: int = Query(1 , ge= 1) , page_limit: int= Query(2 , ge=1)):

    all_user = session.exec(select(User).order_by(User.user_id).offset((page - 1) * page_limit).limit(page_limit)).all()

    total = session.exec(select(func.count()).select_from(User)).one()
    base_url = str(res.url).split('?')[0]

    offset = ((page - 1) * page_limit)

    if offset + page_limit < total:
        nxt = f"{base_url}?page={page + 1}&page_limit={page_limit}"
    else:
        nxt = None

    if page > 1 :
        prev = f"{base_url}?page={page - 1}&page_limit={page_limit}"
    else:
        prev= None

    return {"data" :all_user ,
            "next" :nxt,
            "prev" :prev ,
            "count" :total}

@user_route.get("/user/{id}" , response_model=ReponseG[UserRes])
async def get_single_users(id :int  , session :SessionDep):
    data = session.get(User, id)
    if not  data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"user": data}

@user_route.post("/register" ,status_code=201, response_model=ReponseG[UserRes])
async def create_users(usr: UserCreate, session: SessionDep):

    existing_user = session.exec(select(User).where(User.email == usr.email)).first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Email is already used")

    db_user = User.model_validate(usr)
    db_user.password = hash_password(usr.password)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return {"data": db_user}


@user_route.put("/update_user/{id}", response_model=ReponseG[UserRes] )
async def create_users(id: str, usr: UserCreate, session: SessionDep , curr_user:EmailStr = Depends(get_current_user)):
    data = session.get(User, id)

    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    data.email = usr.email

    session.add(data)
    session.commit()
    session.refresh(data)

    return {"data": data}


@user_route.delete("/delete_user/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_users(id: int, session: SessionDep):
    data = session.get(User, id)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    session.delete(data)
    session.commit()