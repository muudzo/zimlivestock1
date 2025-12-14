from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import Bid, BidBase, LivestockItem, User, LivestockItemBase
from typing import List

router = APIRouter(prefix="/bids", tags=["bids"])

class BidRead(BidBase):
    id: int
    bidder_id: int
    livestock_id: int
    isWinning: bool

class BidCreate(BidBase):
    livestock_id: int
    bidder_id: int

@router.get("/livestock/{item_id}", response_model=List[BidRead])
def read_bids_for_item(item_id: int, session: Session = Depends(get_session)):
    query = select(Bid).where(Bid.livestock_id == item_id).order_by(Bid.amount.desc())
    bids = session.exec(query).all()
    return bids

@router.post("/", response_model=BidRead)
def place_bid(bid: BidCreate, session: Session = Depends(get_session)):
    item = session.get(LivestockItem, bid.livestock_id)
    if not item:
        raise HTTPException(status_code=404, detail="Livestock item not found")
        
    user = session.get(User, bid.bidder_id)
    if not user:
        raise HTTPException(status_code=404, detail="Bidder not found")
        
    # Validation: Bid must be higher than current bid + min increment (e.g. 50? Logic from frontend TS: current + 50)
    # Backend should strictly enforce logic.
    min_bid = (item.currentBid or item.startingPrice) + 0 # Simple check for now, logic enhancement later
    if bid.amount <= item.currentBid:
         raise HTTPException(status_code=400, detail="Bid must be higher than current bid")

    db_bid = Bid.from_orm(bid)
    
    # Update Livestock current bid
    item.currentBid = bid.amount
    session.add(item)
    
    session.add(db_bid)
    session.commit()
    session.refresh(db_bid)
    return db_bid
