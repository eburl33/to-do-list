from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from schema import ItemIn, ItemOut
from db import (
    add_item,
    delete_item,
    get_all_items,
    get_item,
    update_item,
)


app = FastAPI()


@app.get("/api/items")
def endpoint_get_all_items() -> list[ItemOut]:
    return get_all_items()


@app.post("/api/items")
async def endpoint_new_item(item_in: ItemIn) -> ItemOut:
    item = add_item(item_in=item_in)
    return item


@app.get("/api/items/{item_id}")
def endpoint_get_item(item_id: int) -> ItemOut:
    item = get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.delete("/api/items/{item_id}", status_code=204)
def endpoint_delete_item(item_id: int) -> bool:
    deleted = delete_item(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return True


@app.put("/api/items/{item_id}")
def endpoint_update_item(item_id: int, updates: ItemIn) -> ItemOut:
    item = get_item(item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    updated = update_item(item_id, updates)
    return updated


app.mount("/", StaticFiles(directory="static", html=True), name="static")
