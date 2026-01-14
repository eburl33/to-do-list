from fastapi import FastAPI, HTTPException, Response, Query

# from fastapi.staticfiles import StaticFiles
from schema import (
    ItemOut,
    MoveItem,
    ItemCreate,
    ItemUpdate,
    ListOut,
    ListRename,
)
from db import (
    add_item,
    delete_item,
    get_lists,
    get_items,
    get_items_for_list,
    get_item_in_list,
    update_item,
    move_item_to_list,
    rename_list,
)


app = FastAPI()


@app.get("/api/lists")
def get_lists_endpoint() -> list[ListOut]:
    return get_lists()


@app.get("/api/lists/{to_do_list_id}/items")
def endpoint_get_items_for_list(to_do_list_id: int) -> list[ItemOut]:
    return get_items_for_list(to_do_list_id)


@app.get("/api/lists/{to_do_list_id}/items")
def endpoint_get_items(to_do_list_id: int, include_completed: bool = Query(False)):
    return get_items(to_do_list_id, include_completed)


@app.post("/api/lists/{to_do_list_id}/items")
async def endpoint_new(to_do_list_id: int, item_in: ItemCreate) -> ItemOut:
    item = add_item(to_do_list_id=to_do_list_id, item_in=item_in)
    return item


@app.get("/api/lists/{to_do_list_id}/items/{item_id}")
def endpoint_get_item(to_do_list_id: int, item_id: int) -> ItemOut:
    item = get_item_in_list(to_do_list_id, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.delete("/api/lists/{to_do_list_id}/items/{item_id}")
def endpoint_delete_item(item_id: int) -> Response:
    deleted = delete_item(item_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return Response(status_code=204)


@app.put("/api/lists/{to_do_list_id}/items/{item_id}")
def end_update(to_do_list_id: int, item_id: int, updates: ItemUpdate) -> ItemOut:
    updated = update_item(to_do_list_id, item_id, updates)
    return updated


@app.patch("/api/items/{item_id}/move")
def endpoint_move_item(item_id: int, payload: MoveItem) -> ItemOut:
    item = move_item_to_list(item_id, payload)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.patch("/api/lists/{to_do_list_id}")
def rename_list_endpoint(to_do_list_id, payload: ListRename) -> ListOut:
    name = rename_list(to_do_list_id, payload)
    if name is None:
        raise HTTPException(status_code=404, detail="Name cannot be empty")
    return name


# app.mount("/", StaticFiles(directory="static", html=True), name="static")
