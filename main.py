from fastapi import FastAPI, HTTPException
from pydantic import BaseModel  

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float

class NewStore(BaseModel):
    name: str
    items: list[Item] = []

class Store(NewStore):
    id: int


stores: list[Store] = []


@app.get("/")
def get_root():
    return {"is_active": True}

@app.get("/stores")
def get_stores(name: str = None, item: str = None) -> list[Store]:
    data = stores.copy()
    print(item)
    if name:
        data = [store for store in data if store.name == name]
    if item:
        print("filter attempted")
        data = [store for store in data if item in set(item.name for item in store.items)]

    return stores

@app.get("/stores/{store_id}")  
def get_stores_by_id(store_id: int) -> Store:
    for store in stores:
        if store.id == store_id:
            return store
    raise HTTPException(status_code=404, detail="Store not found")

@app.post("/stores")
def create_store(store: NewStore) -> Store:
    store_id = max(store.id for store in stores) + 1 if stores else 1
    new_store = Store(id=store_id, **store.model_dump())

    stores.append(new_store)

    return new_store

@app.put("/stores/{store_id}")  
def update_store(store_id: int, store: NewStore) -> Store:
    curr = None
    for s in stores:
        if s.id == store_id:
            curr = s
            break
    else:
        raise HTTPException(status_code=404, detail="Store not found")

    if store.name:
        curr.name = store.name
    if store.items:
        curr.items = store.items
    return curr