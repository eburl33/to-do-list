from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

# from datetime import datetime // establish date at a later time
from schema import ItemIn, ItemOut


db = "react_mvp"

engine = create_engine(f"postgresql://postgres:postgres@postgres_db:5432/{db}")
SessionLocal = sessionmaker(engine)


class Base(DeclarativeBase):
    pass


class Item(Base):
    __tablename__ = "item"
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column()
    is_complete: Mapped[bool] = mapped_column()


def get_all_items() -> list[ItemOut]:
    items = []
    with SessionLocal() as db:
        stmt = select(Item)
        db_items = db.scalars(stmt).all()
        for db_item in db_items:
            items.append

    return items


def add_item(item_in: ItemIn) -> ItemOut:
    with SessionLocal() as db:
        db_item = Item(**item_in.model_dump())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
    return ItemOut(
        item_id=db_item.id,
        description=db_item.description,
        is_complete=db_item.is_complete,
    )


def get_item(item_id: int) -> ItemOut | None:
    with SessionLocal() as db:
        stmt = select(Item).where(Item.id == item_id)
        item = db.scalar(stmt)
        if item:
            return ItemOut(
                item_id=item.id,
                is_complete=item.is_complete,
                description=item.description,
            )
    return None


def delete_item(item_id: int) -> bool:
    with SessionLocal() as db:
        stmt = select(Item).where(Item.id == item_id)
        item = db.scalar(stmt)
        if item_id is None:
            return False
        db.delete(item)
        db.commit()

    return True


def update_item(item_id: int, updates: ItemIn) -> ItemOut:
    with SessionLocal() as db:
        stmt = select(Item).where(Item.id == item_id)
        item = db.scalar(stmt)
        data = Item(**updates.model_dump())
        db.commit()
        db.refresh(item)

        return ItemOut(
            item_id=data.id,
            description=data.description,
            is_complete=data.is_complete,
        )
