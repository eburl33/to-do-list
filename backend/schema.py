from pydantic import BaseModel


class ItemOut(BaseModel):
    item_id: int
    description: str
    is_complete: bool


class ItemIn(BaseModel):
    description: str
    is_complete: bool


class DeleteStatus(BaseModel):
    status: bool
    message: str
