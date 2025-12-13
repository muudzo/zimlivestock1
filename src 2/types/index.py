# AUTO-GENERATED FROM TypeScript
# SOURCE: src/types/index.ts
# CONVERSION STAGE: STAGE 2
# DO NOT MODIFY LOGIC WITHOUT COMPARING TO ORIGINAL

from typing import TypedDict, List, Optional, Union, Any, Dict, Literal, Generic, TypeVar
from datetime import datetime

T = TypeVar("T")

# export type LivestockCategory = 'cattle' | 'goats' | 'sheep' | 'pigs' | 'chickens' | 'horses' | 'donkeys';
LivestockCategory = Literal['cattle', 'goats', 'sheep', 'pigs', 'chickens', 'horses', 'donkeys']

# export type NotificationType = ...
NotificationType = Literal[
    'bid_placed',
    'bid_outbid',
    'auction_won',
    'auction_ending',
    'new_message',
    'system'
]

class Seller(TypedDict):
    id: str
    name: str
    avatar: Optional[str]
    verified: bool
    rating: Optional[float] # number in TS is float in Python usually
    totalSales: Optional[int]
    location: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    joinedDate: datetime

class LivestockItem(TypedDict):
    id: str
    title: str
    breed: str
    age: str
    weight: str
    location: str
    currentBid: float # number
    startingPrice: float # number
    timeLeft: str
    imageUrl: str
    seller: Seller
    bidCount: int
    views: int
    category: LivestockCategory
    description: Optional[str]
    healthStatus: Optional[Literal['verified', 'pending', 'unverified']]
    createdAt: datetime
    updatedAt: datetime
    auctionEndDate: datetime
    images: Optional[List[str]]
    tags: Optional[List[str]]

class Bid(TypedDict):
    id: str
    livestockId: str
    bidderId: str
    bidderName: str
    amount: float
    timestamp: datetime
    isWinning: bool

class UserNotificationPreferences(TypedDict):
    email: bool
    push: bool
    sms: bool

class PriceRange(TypedDict):
    min: float
    max: float

class UserPreferences(TypedDict):
    notifications: UserNotificationPreferences
    categories: List[LivestockCategory]
    locations: List[str]
    priceRange: PriceRange

class User(TypedDict):
    id: str
    firstName: str
    lastName: str
    email: str
    phone: str
    avatar: Optional[str]
    verified: bool
    location: Optional[str]
    preferences: Optional[UserPreferences]
    createdAt: datetime
    updatedAt: datetime

class Notification(TypedDict):
    id: str
    userId: str
    type: NotificationType
    title: str
    message: str
    read: bool
    createdAt: datetime
    data: Optional[Dict[str, Any]]

class MessageAttachment(TypedDict):
    id: str
    type: Literal['image', 'document']
    url: str
    name: str
    size: float # number

class Message(TypedDict):
    id: str
    senderId: str
    receiverId: str
    content: str
    timestamp: datetime
    read: bool
    attachments: Optional[List[MessageAttachment]]

class ApiResponse(TypedDict, Generic[T]):
    success: bool
    data: Optional[T]
    error: Optional[str]
    message: Optional[str]

class PaginationInfo(TypedDict):
    page: int
    limit: int
    total: int
    totalPages: int

class PaginatedResponse(TypedDict, Generic[T]):
    data: List[T]
    pagination: PaginationInfo

class FilterOptions(TypedDict, total=False): # total=False for optional keys? TS interfaces have optional keys (?)
    # In TS: category?: LivestockCategory. 
    # Python TypedDict doesn't support mixed optional in older versions easily w/o inheritance. 
    # But for "Baseline Integrity" and "Pure Translation", I'll use NotRequired if Py3.11+ or just Optional fields.
    # Actually, TS definition: `category?:` implies key can be missing.
    # Python TypedDict keys are required by default unless `total=False`.
    # `FilterOptions` has ALL optional keys in TS. So `total=False` is appropriate.
    category: LivestockCategory
    location: str
    priceRange: PriceRange
    breed: str
    age: str
    verifiedSeller: bool
    sortBy: Literal['price', 'date', 'popularity', 'ending_soon']
    sortOrder: Literal['asc', 'desc']

class SearchParams(TypedDict, total=False):
    query: str
    filters: FilterOptions
    page: int
    limit: int

class AuthState(TypedDict):
    user: Optional[User]
    token: Optional[str]
    isAuthenticated: bool
    isLoading: bool

class AppState(TypedDict):
    theme: Literal['light', 'dark', 'system']
    language: str
    notifications: List[Notification]
    unreadCount: int

class ErrorState(TypedDict, total=False): # error and errorInfo are optional
    hasError: bool
    error: Optional[Exception] # Error -> Exception
    errorInfo: Any # React.ErrorInfo is opaque here
