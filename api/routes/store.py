from fastapi import APIRouter, HTTPException , status
from fastapi.params import Query
from sqlmodel import select


from database.config import SessionDep
from database.resSchema import StoreCre, StoreRead, ReponseG, UpdateStore, PatchStore
from database.schema import Store, Address

store_route = APIRouter(tags=["Store"])
@store_route.get("/stores", response_model=list[StoreRead])
def get_stores(
    session: SessionDep,
    page: int = Query(1, ge=1),
    per_page: int = Query(2, ge=1)
):
    data = (
        session.exec(
            select(Store)
            .order_by(Store.store_id)
            .offset((page - 1) * per_page)
            .limit(per_page)
        ).all()
    )


    return data   # ✅ no need to wrap in {"data": ...}, response_model handles it


@store_route.get("/store/{id}", response_model=StoreRead)
def get_store_by_id(id: str, session: SessionDep):
    store = session.get(Store, id)
    if not store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return store   # ✅ ORM auto-converts via response_model


@store_route.post("/create", response_model=StoreRead, status_code=status.HTTP_201_CREATED)
def create_store(store: StoreCre, session: SessionDep):
    db_addresses = [Address(**addr.dict()) for addr in (store.addresses or [])]

    new_store = Store(
        store_name=store.store_name,
        store_email=store.store_email,
        type_of=store.type_of,
        addresses=db_addresses
    )

    session.add(new_store)
    session.commit()
    session.refresh(new_store)
    return new_store

@store_route.patch("/update_store/{store_id}", response_model=StoreRead)
def patch_store(store_id: str, store_in: PatchStore, session: SessionDep):
    store = session.get(Store, store_id)
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")

    # --- Update store fields dynamically ---
    store_data = store_in.dict(exclude_unset=True, exclude={"addresses"})
    for key, value in store_data.items():
        setattr(store, key, value)

    # --- Update addresses if provided ---
    if store_in.addresses:
        for addr_in in store_in.addresses:
            address = session.get(Address, addr_in.address_id)
            if not address or address.store_id != store_id:
                raise HTTPException(
                    status_code=404,
                    detail=f"Address {addr_in.address_id} not found for this store"
                )

            addr_data = addr_in.dict(exclude_unset=True)
            for key, value in addr_data.items():
                setattr(address, key, value)

            session.add(address)

    session.add(store)
    session.commit()
    session.refresh(store)
    return store

@store_route.delete("/delete/{id}" , status_code=status.HTTP_204_NO_CONTENT)
async def delete_store(id:str , session:SessionDep):
    existing_store = session.get(Store , id)
    if not existing_store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    session.delete(existing_store)
    session.commit()



