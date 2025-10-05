from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Relationship
from typing_extensions import TypeVar, Generic

class UserRes(BaseModel):
    user_id: str
    email: str
    role:str
    created_at: datetime

class AddressCre(SQLModel):
    type:str
    street: str
    city: str
    floor: Optional[str] = None   # cleaner syntax
    state: str
    zip_code: str

class Store_Info(BaseModel):
    store_name: str
    store_email: EmailStr
    type_of: Optional[str]

class AddressRead(SQLModel):
    address_id: str
    type:str = "Home"
    street: str
    city: str
    floor: Optional[str] = "1"
    state: str
    zip_code: str


class StoreRead(SQLModel):
    store_id : str
    store_name: str
    store_email: EmailStr
    type_of: Optional[str]
    addresses: List[AddressRead] = []

class StoreCre(SQLModel):
    store_name: str
    store_email: EmailStr
    type_of: str
    addresses: Optional[List[AddressCre]] = None

class TokenRes(BaseModel):
    access_token:str
    token_type: Optional[str] = "bearer"

class TokenData(BaseModel):
    email:EmailStr
    role:Optional[str]

class UpdateStore(SQLModel):   # Use SQLModel instead of BaseModel for consistency
    store_name: str
    store_email: EmailStr
    type_of: str

class UpdateAddress(SQLModel):
    address_id: str  # ID of the address to update
    type: Optional[str] = None
    street: Optional[str] = None
    floor: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None



class PatchStore(SQLModel):
    store_name: Optional[str] = None
    store_email: Optional[EmailStr] = None
    type_of: Optional[str] = None
    addresses: Optional[List[UpdateAddress]] = None


class UserCreate(SQLModel):
    email:EmailStr
    password:str

T = TypeVar("T")
class ReponseG(BaseModel, Generic [T]):
    data: T


class PaginationG(BaseModel , Generic[T]):
    data:T
    next:Optional[str]
    prev:Optional[str]
    count: int

