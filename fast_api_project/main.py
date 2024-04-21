from typing import Union, Dict

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from models import User

app = FastAPI()
users_db: Dict[int, dict] = {}


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.post("/users/", response_model=User)
async def create_user(user: User):
    user_id = len(users_db) + 1
    users_db[user_id] = user.dict()
    return user

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: User):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[user_id].update(user.dict())
    return user