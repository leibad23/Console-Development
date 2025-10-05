from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.store import store_route
from api.routes.user import user_route
from api.routes.auth import auth_route
from database.config import lifespan

app = FastAPI(root_path="/api/v1" , lifespan=lifespan)
app.add_middleware(CORSMiddleware ,allow_credentials=True,
allow_origin=["*"] , allow_methods=["*"]  , allow_header=["*"])

app.include_router(user_route)
app.include_router(store_route)
app.include_router(auth_route)