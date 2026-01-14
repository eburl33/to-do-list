from pydantic import BaseModel


class ItemOut(BaseModel):
    item_id: int
    to_do_list_id: int
    description: str
    is_complete: bool


class DeleteStatus(BaseModel):
    status: bool
    message: str


class MoveItem(BaseModel):
    to_do_list_id: int


class ItemCreate(BaseModel):
    description: str
    is_complete: bool = False


class ItemUpdate(BaseModel):
    description: str
    is_complete: bool


class ListOut(BaseModel):
    to_do_list_id: int
    name: str


class ListCreate(BaseModel):
    name: str


class ListRename(BaseModel):
    name: str
