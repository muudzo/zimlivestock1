from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from typing import Literal

# Enums (re-defined or imported from types if useful, but for Models we define them or use str)
# SQLite doesn't strictly enforce Enums easily without extra work, storing as str is fine for MVP.

class UserBase(SQLModel):
    firstName: str
    lastName: str
    email: str = Field(index=True, unique=True)
    phone: str
    avatar: Optional[str] = None
    location: Optional[str] = None
    verified: bool = False
    
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    livestock_items: List["LivestockItem"] = Relationship(back_populates="seller")
    bids: List["Bid"] = Relationship(back_populates="bidder")

class LivestockItemBase(SQLModel):
    title: str
    breed: str
    age: str
    weight: str
    location: str
    startingPrice: float
    currentBid: float = 0.0
    category: str # Enum in logic
    description: Optional[str] = None
    imageUrl: str
    auctionEndDate: datetime
    healthStatus: str = "pending"

class LivestockItem(LivestockItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    seller_id: Optional[int] = Field(default=None, foreign_key="user.id")
    seller: Optional[User] = Relationship(back_populates="livestock_items")
    
    bids: List["Bid"] = Relationship(back_populates="livestock")

class BidBase(SQLModel):
    amount: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class Bid(BidBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    isWinning: bool = False
    
    bidder_id: Optional[int] = Field(default=None, foreign_key="user.id")
    bidder: Optional[User] = Relationship(back_populates="bids")
    
    livestock_id: Optional[int] = Field(default=None, foreign_key="livestockitem.id")
    livestock: Optional[LivestockItem] = Relationship(back_populates="bids")
