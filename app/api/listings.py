from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.database import get_session
from app.models import LivestockItem, LivestockItemBase, User, UserBase
from app.api.auth import get_current_user
from typing import List, Optional
from pydantic import BaseModel, computed_field
from datetime import datetime
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/livestock", tags=["livestock"])

class UserPublic(BaseModel):
    id: int
    firstName: str
    lastName: str
    avatar: Optional[str] = None
    verified: bool = False
    location: Optional[str] = None
    created_at: datetime
    
    @computed_field
    @property
    def name(self) -> str:
        return f"{self.firstName} {self.lastName}"
        
    @computed_field
    @property
    def joinedDate(self) -> datetime:
        return self.created_at

class LivestockItemRead(LivestockItemBase):
    id: int
    seller: Optional[UserPublic] = None
    views: int = 0
    
    @computed_field
    @property
    def bidCount(self) -> int:
        return len(self.bids) if hasattr(self, 'bids') and self.bids is not None else 0

    @computed_field
    @property
    def timeLeft(self) -> str:
        if not self.auctionEndDate:
            return "Unknown"
        now = datetime.utcnow()
        if self.auctionEndDate <= now:
            return "Ended"
        diff = self.auctionEndDate - now
        days = diff.days
        hours = diff.seconds // 3600
        if days > 0:
            return f"{days}d {hours}h"
        minutes = (diff.seconds % 3600) // 60
        return f"{hours}h {minutes}m"

    class Config:
        from_attributes = True

class LivestockItemCreate(LivestockItemBase):
    pass # seller_id will be taken from token

@router.get("/", response_model=List[LivestockItemRead])
def read_listings(
    offset: int = 0,
    limit: int = 20,
    category: Optional[str] = None,
    session: Session = Depends(get_session)
):
    query = select(LivestockItem).options(
        selectinload(LivestockItem.seller),
        selectinload(LivestockItem.bids)
    )
    if category:
        query = query.where(LivestockItem.category == category)
    query = query.offset(offset).limit(limit)
    listings = session.exec(query).all()
    
    return listings

@router.post("/", response_model=LivestockItemRead)
def create_listing(
    item: LivestockItemCreate, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    db_item = LivestockItem.from_orm(item)
    db_item.seller_id = current_user.id
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

@router.get("/{item_id}", response_model=LivestockItemRead)
def read_listing(item_id: int, session: Session = Depends(get_session)):
    query = select(LivestockItem).where(LivestockItem.id == item_id).options(
        selectinload(LivestockItem.seller),
        selectinload(LivestockItem.bids)
    )
    item = session.exec(query).first()
    if not item:
        raise HTTPException(status_code=404, detail="Listing not found")
    return item

@router.delete("/{item_id}")
def delete_listing(
    item_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    item = session.get(LivestockItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    # Check ownership
    if item.seller_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this listing")
        
    session.delete(item)
    session.commit()
    return {"ok": True}
