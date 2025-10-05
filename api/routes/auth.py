from fastapi import APIRouter , HTTPException ,status ,Response
from sqlmodel import select

from database.config import SessionDep
from database.resSchema import TokenRes, UserCreate
from database.schema import User
from utils.encode import verify_password, create_access_token

auth_route = APIRouter(tags=["Auth"])

@auth_route.post("/login" , response_model=TokenRes)
async def login_auth_user(usr:UserCreate  , session: SessionDep):

    curr_user:User = session.exec(select(User).where(User.email == usr.email)).first()

    if not curr_user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND , detail="Invalid email or password")

    if not verify_password(usr.password , curr_user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid email or password")

    access_token = create_access_token(data={"email":curr_user.email , "role":curr_user.role})

    return {"access_token":access_token , "token_type":"bearer"}
