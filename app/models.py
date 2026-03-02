from typing import Optional, List, Literal
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

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
    
    livestock_items: List["LivestockItem"] = Relationship(
        back_populates="seller",
        sa_relationship_kwargs={"foreign_keys": "[LivestockItem.seller_id]"}
    )
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
    seller: Optional[User] = Relationship(
        back_populates="livestock_items", 
        sa_relationship_kwargs={"foreign_keys": "[LivestockItem.seller_id]"}
    )
    
    winner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
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


# ─── Paynow Payment ───────────────────────────────────────────────────────────

PaymentStatus = Literal["pending", "paid", "failed", "cancelled", "refunded"]
PaymentMethod = Literal["web", "ecocash", "onemoney", "telecash", "card", "zipit"]


class Payment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Who is paying
    payer_id: int = Field(foreign_key="user.id")

    # What they are paying for
    livestock_id: Optional[int] = Field(default=None, foreign_key="livestockitem.id")
    bid_id: Optional[int] = Field(default=None, foreign_key="bid.id")

    # Payment details
    amount: float
    currency: str = "USD"
    payment_method: Optional[str] = None  # ecocash | onemoney | web | etc.

    # Internal unique reference (e.g. ZL-5-A1B2C3D4)
    merchant_reference: str = Field(unique=True, index=True)

    # Paynow-returned values
    paynow_reference: Optional[str] = None
    paynow_poll_url: Optional[str] = None
    paynow_redirect_url: Optional[str] = None
    paynow_instructions: Optional[str] = None

    # Status
    status: str = "pending"  # pending | paid | failed | cancelled | refunded

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    paid_at: Optional[datetime] = None
