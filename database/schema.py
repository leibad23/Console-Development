from datetime import datetime, timezone
from typing import Optional, List
from uuid import uuid4
from pydantic import EmailStr


from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    user_id: str = Field(default_factory=lambda: uuid4().hex, primary_key=True)
    email: EmailStr = Field(nullable=False, index=True, unique=True)
    password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=True)
    role: str | None = Field(default="organizer")

    # --- relationships ---
    recipient: Optional[List["Recipient"]] = Relationship(back_populates="user" , cascade_delete=True)
    orders: Optional[List["Order"]] = Relationship(back_populates="user", cascade_delete=True)
    # images: Optional[List["ImgInfo"]] = Relationship(back_populates="user")  # one-to-many


class Order(SQLModel, table=True):
    order_id: str = Field(default_factory=lambda: f"order_{uuid4().hex}", primary_key=True)
    user_id: str = Field(foreign_key="user.user_id" , ondelete="CASCADE")
    recipient_id: str = Field(foreign_key="recipient.rep_id" , ondelete="CASCADE")
    type_of: str = Field(default="lunch")
    time_of_order: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    delivery_time: Optional[datetime] = Field(default=None)

    user: "User" = Relationship(back_populates="orders" )
    recipient: "Recipient" = Relationship(back_populates="orders")


class Recipient(SQLModel, table=True):
    rep_id: str = Field(default_factory=lambda: uuid4().hex, primary_key=True)

    user_id: str = Field(foreign_key="user.user_id" , ondelete="CASCADE" )

    name: str = Field(nullable=False)
    email: EmailStr = Field(nullable=False, unique=True)
    phone_num: str = Field(nullable=False, unique=True)
    address: str = Field(nullable=False)

    # --- relationships ---

    user: "User" = Relationship(back_populates="recipient" )
    orders: List["Order"] = Relationship(back_populates="recipient" )
    # images: List["ImgInfo"] = Relationship(back_populates="recipient")  # one-to-many



class Store(SQLModel, table=True):
    store_id: str = Field(default_factory=lambda: f"store_{uuid4().hex}", primary_key=True)
    store_name: str = Field(default=None, unique=True)
    store_email: EmailStr = Field(default=None)
    type_of: str = Field(default=None, nullable=True)

    addresses: Optional[List["Address"]] = Relationship(back_populates="store",sa_relationship_kwargs={"foreign_keys": "[Address.store_id]"} , cascade_delete=True)

class Address(SQLModel, table=True):
    address_id: str = Field(default_factory=lambda:f"addy_{uuid4().hex}", primary_key=True)

    type: str = Field(default="Home")
    street: str = Field(default="9 E 21st Street")
    floor: Optional[str] = Field(default="1")

    city: str = Field(default="Paterson")
    state: str = Field(default="NJ")
    zip_code: str = Field(default="07504", max_length=5)

    store_id: str = Field(foreign_key="store.store_id" , nullable= False , index=True , ondelete="CASCADE")
    store: "Store" = Relationship(back_populates="addresses" )

# class Item(SQLModel, table=True):
#     item_id: str = Field(default_factory=lambda: uuid4().hex, primary_key=True)
#     store_id: str = Field(foreign_key="store.store.id")
#     price: float = Field(default=0.00, nullable=False)
#     category: str = Field(nullable=False)
#     desc: Optional[str] = Field(default=None)
#
#     images: List["ImgInfo"] = Relationship(back_populates="item")  # one-to-many
#
#
# class ImgInfo(SQLModel, table=True):
#     img_id: str = Field(default_factory=lambda: uuid4().hex, primary_key=True)
#     file_name: str = Field(nullable=False)  # e.g. "burger.png"
#     path: str = Field(nullable=False)  # e.g. "/uploads/burger.png"
#
#     # --- associations ---
#     user_id: Optional[str] = Field(default=None, foreign_key="user.user_id")
#     recipient_id: Optional[str] = Field(default=None, foreign_key="recipient.rep_id")
#     item_id: Optional[str] = Field(default=None, foreign_key="item.item_id")
#
#     # --- relationships ---
#     user: Optional["User"] = Relationship(back_populates="images")
#     recipient: Optional["Recipient"] = Relationship(back_populates="images")
#     item: Optional["Item"] = Relationship(back_populates="images")
#

"""
Side Note - To set up the events portion of the code 

-User

-Event
    -event_id
    -title
    -created_by
    -created_at
    
    participants:list

-Participant
    -id
    -event_id
    -user_id
    -roles
    

-EventInvite


"""
