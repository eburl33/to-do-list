from datetime import date
from fastapi import HTTPException, Query
from sqlalchemy import create_engine, select, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

# from datetime import datetime // establish date at a later time
from schema import (
    ItemOut,
    MoveItem,
    ItemCreate,
    ItemUpdate,
    ListOut,
    ListRename,
)


db = "react_mvp"

engine = create_engine(f"postgresql://postgres:postgres@localhost:5432/{db}")
SessionLocal = sessionmaker(engine)


class Base(DeclarativeBase):
    pass


class ToDoList(Base):
    __tablename__ = "to_do_lists"
    to_do_list_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    date_added: Mapped[date] = mapped_column(Date, server_default=func.current_date())


class Item(Base):
    __tablename__ = "items"
    item_id: Mapped[int] = mapped_column(primary_key=True)
    to_do_list_id: Mapped[int] = mapped_column()
    description: Mapped[str] = mapped_column()
    is_complete: Mapped[bool] = mapped_column()


def get_lists() -> list[ListOut]:
    with SessionLocal() as db:
        stmt = select(ToDoList)
        lists = db.scalars(stmt).all()
        return [
            ListOut(to_do_list_id=list.to_do_list_id, name=list.name) for list in lists
        ]


def get_items(
    to_do_list_id: int, include_completed: bool = Query(False)
) -> list[ItemOut]:
    with SessionLocal() as db:
        stmt = select(Item).where(Item.to_do_list_id == to_do_list_id)
        if not include_completed:
            stmt = stmt.where(Item.is_complete == False)
        items = db.scalars(stmt).all()
        return [
            ItemOut(
                item_id=item.item_id,
                to_do_list_id=item.to_do_list_id,
                description=item.description,
                is_complete=item.is_complete,
            )
            for item in items
        ]


def get_items_for_list(to_do_list_id: int) -> list[ItemOut]:
    with SessionLocal() as db:
        stmt = select(Item).where(
            Item.to_do_list_id == to_do_list_id, Item.is_complete == False
        )
        items = db.scalars(stmt).all()
    return [
        ItemOut(
            item_id=i.item_id,
            to_do_list_id=i.to_do_list_id,
            description=i.description,
            is_complete=i.is_complete,
        )
        for i in items
    ]


def create_list():
    with SessionLocal() as db:
        new_list = ToDoList()
        db.add(new_list)
        db.commit()
        db.refresh(new_list)
    return ListOut(to_do_list_id=new_list.to_do_list_id, name=new_list.name)


def add_item(to_do_list_id: int, item_in: ItemCreate) -> ItemOut:
    with SessionLocal() as db:
        item = Item(
            to_do_list_id=to_do_list_id,
            description=item_in.description,
            is_complete=item_in.is_complete,
        )
        db.add(item)
        db.commit()
        db.refresh(item)
    return ItemOut(
        item_id=item.item_id,
        to_do_list_id=item.to_do_list_id,
        description=item.description,
        is_complete=item.is_complete,
    )


def get_item_in_list(to_do_list_id: int, item_id: int) -> ItemOut | None:
    with SessionLocal() as db:
        stmt = select(Item).where(
            Item.to_do_list_id == to_do_list_id, Item.item_id == item_id
        )
        item = db.scalar(stmt)
        if item:
            return ItemOut(
                item_id=item.item_id,
                to_do_list_id=item.to_do_list_id,
                is_complete=item.is_complete,
                description=item.description,
            )
    return None


def delete_item(item_id: int) -> bool:
    with SessionLocal() as db:
        stmt = select(Item).where(Item.item_id == item_id)
        item = db.scalar(stmt)
        if item_id is None:
            return False
        db.delete(item)
        db.commit()

    return True


def update_item(to_do_list_id: int, item_id: int, updates: ItemUpdate) -> ItemOut:
    with SessionLocal() as db:
        stmt = select(Item).where(
            Item.to_do_list_id == to_do_list_id, Item.item_id == item_id
        )
        item = db.scalar(stmt)
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        item.description = updates.description
        item.is_complete = updates.is_complete
        db.commit()
        db.refresh(item)

        return ItemOut(
            item_id=item.item_id,
            to_do_list_id=item.to_do_list_id,
            description=item.description,
            is_complete=item.is_complete,
        )


def move_item_to_list(item_id: int, payload: MoveItem) -> ItemOut | None:
    with SessionLocal() as db:
        item = db.get(Item, item_id)
        if item:
            item.to_do_list_id = payload.to_do_list_id
            db.commit()
            db.refresh(item)
            return ItemOut(
                item_id=item.item_id,
                to_do_list_id=item.to_do_list_id,
                is_complete=item.is_complete,
                description=item.description,
            )
    return None


def rename_list(to_do_list_id, payload: ListRename) -> ListOut:
    with SessionLocal() as db:
        stmt = select(ToDoList).where(ToDoList.to_do_list_id == to_do_list_id)
        todo_list = db.scalar(stmt)
        if not todo_list:
            raise HTTPException(status_code=404, detail="List not found")
        name = payload.name.strip()
        todo_list.name = name
        db.commit()
        db.refresh(todo_list)
        return ListOut(to_do_list_id=todo_list.to_do_list_id, name=todo_list.name)
