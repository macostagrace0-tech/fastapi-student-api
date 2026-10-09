from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Item
from app.schemas import ItemCreate, ItemRead, ItemUpdate


router = APIRouter(
    prefix="/items",
    tags=["Items"],
)


@router.post(
    "",
    response_model=ItemRead,
    status_code=status.HTTP_201_CREATED,
)
def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
):
    new_item = Item(
        name=item.name,
        description=item.description,
        price=item.price,
        is_active=item.is_active,
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


@router.get("", response_model=list[ItemRead])
def list_items(
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: int = 20,
    active: bool | None = None,
):
    query = db.query(Item)

    if active is not None:
        query = query.filter(Item.is_active == active)

    return query.offset(offset).limit(min(limit, 100)).all()


@router.get("/{item_id}", response_model=ItemRead)
def get_item(
    item_id: int,
    db: Session = Depends(get_db),
):
    item = db.query(Item).filter(Item.id == item_id).first()

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
        )

    return item


@router.patch("/{item_id}", response_model=ItemRead)
def update_item(
    item_id: int,
    item_data: ItemUpdate,
    db: Session = Depends(get_db),
):
    item = db.query(Item).filter(Item.id == item_id).first()

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
        )

    update_data = item_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)

    return item


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
):
    item = db.query(Item).filter(Item.id == item_id).first()

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
        )

    db.delete(item)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
