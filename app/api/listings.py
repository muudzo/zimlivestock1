from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.database import get_session
from app.models import LivestockItem, LivestockItemBase, User
from typing import List, Optional

router = APIRouter(prefix="/livestock", tags=["livestock"])

class LivestockItemRead(LivestockItemBase):
    id: int
    seller_id: Optional[int] = None
    bids: List[int] = [] # simplified list of bid IDs

    class Config:
        orm_mode = True

class LivestockItemCreate(LivestockItemBase):
    seller_id: int

@router.get("/", response_model=List[LivestockItemRead])
def read_listings(
    offset: int = 0,
    limit: int = 20,
    category: Optional[str] = None,
    session: Session = Depends(get_session)
):
    query = select(LivestockItem)
    if category:
        query = query.where(LivestockItem.category == category)
    query = query.offset(offset).limit(limit)
    listings = session.exec(query).all()
    return listings

@router.post("/", response_model=LivestockItemRead)
def create_listing(item: LivestockItemCreate, session: Session = Depends(get_session)):
    # Verify seller exists
    user = session.get(User, item.seller_id)
    if not user:
        raise HTTPException(status_code=404, detail="Seller not found")
        
    db_item = LivestockItem.from_orm(item)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

@router.get("/{item_id}", response_model=LivestockItemRead)
def read_listing(item_id: int, session: Session = Depends(get_session)):
    item = session.get(LivestockItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Listing not found")
    return item

@router.delete("/{item_id}")
def delete_listing(item_id: int, session: Session = Depends(get_session)):
    item = session.get(LivestockItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Listing not found")
    session.delete(item)
    session.commit()
    return {"ok": True}
