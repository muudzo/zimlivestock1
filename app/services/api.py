# AUTO-GENERATED FROM TypeScript
# SOURCE: src/services/api.ts
# CONVERSION STAGE: STAGE 3
# DO NOT MODIFY LOGIC WITHOUT COMPARING TO ORIGINAL

import os
import json
import httpx
from typing import Optional, Dict, Any, List, Union, TypeVar, Tuple
from datetime import datetime
import asyncio

# Import types
# Assuming the python package structure works (running from root)
# In a real app we might need to adjust python path
try:
    from src.types.index import (
        ApiResponse, PaginatedResponse, LivestockItem, User, Bid, Notification,
        AppState, AuthState   # types mapped in index.py
    )
except ImportError:
    # Fallback/Mock types if import fails (e.g. during scaffolding check)
    ApiResponse = dict
    PaginatedResponse = dict
    LivestockItem = dict
    User = dict
    Bid = dict
    Notification = dict

# --- Mocks for Browser/Environment Globals ---
class LocalStorage:
    _store: Dict[str, str] = {}
    
    @classmethod
    def getItem(cls, key: str) -> Optional[str]:
        return cls._store.get(key)
    
    @classmethod
    def setItem(cls, key: str, value: str):
        cls._store[key] = str(value)
        
    @classmethod
    def removeItem(cls, key: str):
        if key in cls._store:
            del cls._store[key]

localStorage = LocalStorage()

class Window:
    class Location:
        href: str = ""
    location = Location()

window = Window()

# --- API Configuration ---
# const API_BASE_URL = process.env.VITE_API_BASE_URL || 'https://api.zimlivestock.com'
API_BASE_URL = os.environ.get('VITE_API_BASE_URL', 'https://api.zimlivestock.com')
# const API_TIMEOUT = 10000
API_TIMEOUT = 10.0 # seconds in httpx/python

# --- Create Client ---
# const apiClient: AxiosInstance = axios.create(...)
# httpx.AsyncClient is closest to axios instance
apiClient = httpx.AsyncClient(
    base_url=API_BASE_URL,
    timeout=API_TIMEOUT,
    headers={
        'Content-Type': 'application/json',
    }
)

# --- Interceptors ---
# apiClient.interceptors.request.use(...)
async def request_interceptor(request: httpx.Request):
    # const token = localStorage.getItem('auth_token')
    token = localStorage.getItem('auth_token')
    # if (token) {
    if token:
        # config.headers.Authorization = `Bearer ${token}`
        request.headers['Authorization'] = f"Bearer {token}"
    # return config (implicit in httpx hooks)

# apiClient.interceptors.response.use(...)
# httpx doesn't support response interceptors modifying control flow exactly like axios (redirect rejection) easily in hooks.
# But we can misuse response hook or wrap the calls.
# However, for pure logic translation, I'll attach hooks.
# httpx response hook is called after response is received.
async def response_interceptor(response: httpx.Response):
    # if (error.response?.status === 401) ...
    # In httpx hook, we get response. user checks status.
    if response.status_code == 401:
        # Handle unauthorized access
        # localStorage.removeItem('auth_token')
        localStorage.removeItem('auth_token')
        # localStorage.removeItem('user')
        localStorage.removeItem('user')
        # window.location.href = '/login'
        window.location.href = '/login'
        print(f"Redirecting to {window.location.href}")
        # return Promise.reject(error) -> httpx raises if we call raise_for_status, but here we just processed it.
        # Logic says "return Promise.reject(error)". 
        # In calling code, this means it throws.
        # We can simulate by maybe NOT raising here but letting the caller handle or raising?
        # Axios interceptor error handler handles ERROR. 401 is success response usually unless validation fails?
        # Axios treats 4xx as error by default `validateStatus`.
        # So this `(error: AxiosError)` block runs on 401.
        pass

apiClient.event_hooks = {
    'request': [request_interceptor],
    'response': [response_interceptor] 
    # Note: httpx response hook is for valid responses. 401 is valid HTTP response.
    # Axios `(error)` handler handles 401 if it's considered error.
}

# --- Generic API response handler ---
T = TypeVar("T")
def handleApiResponse(response: httpx.Response) -> Any: # Returns T
    # if (response.data.success) ...
    # Axios response.data is the JSON body.
    try:
        data = response.json()
    except Exception:
        # mimic axios error if json fails
        raise Exception('API request failed: Invalid JSON')
        
    if data.get('success'):
        return data.get('data') # ! logic
    
    # throw new Error(response.data.error || 'API request failed')
    error_msg = data.get('error') or 'API request failed'
    raise Exception(error_msg)


# --- Auth API ---
class AuthAPI:
    @staticmethod
    async def login(email: str, password: str) -> Dict[str, Any]: # { user: User; token: string }
        # const response = await apiClient.post<...>(...)
        response = await apiClient.post('/auth/login', json={
            'email': email,
            'password': password,
        })
        return handleApiResponse(response)

    @staticmethod
    async def register(userData: Dict[str, str]) -> Dict[str, Any]:
        # const response = await apiClient.post<...>(...)
        response = await apiClient.post('/auth/register', json=userData)
        return handleApiResponse(response)

    @staticmethod
    async def logout() -> None:
        # await apiClient.post('/auth/logout')
        await apiClient.post('/auth/logout')
        # localStorage.removeItem('auth_token')
        localStorage.removeItem('auth_token')
        # localStorage.removeItem('user')
        localStorage.removeItem('user')

    @staticmethod
    async def refreshToken() -> Dict[str, str]: # { token: string }
        response = await apiClient.post('/auth/refresh')
        return handleApiResponse(response)

    @staticmethod
    async def getProfile() -> User:
        response = await apiClient.get('/auth/profile')
        return handleApiResponse(response)

    @staticmethod
    async def updateProfile(userData: Dict[str, Any]) -> User:
        response = await apiClient.put('/auth/profile', json=userData)
        return handleApiResponse(response)

authAPI = AuthAPI()


# --- Livestock API ---
class LivestockAPI:
    @staticmethod
    async def getListings(params: Optional[Dict[str, Any]] = None) -> PaginatedResponse:
        # const response = await apiClient.get(...)
        # axios params are query params
        response = await apiClient.get('/livestock', params=params)
        return handleApiResponse(response)

    @staticmethod
    async def getListing(id: str) -> LivestockItem:
        response = await apiClient.get(f'/livestock/{id}')
        return handleApiResponse(response)

    @staticmethod
    async def createListing(listingData: Dict[str, Any]) -> LivestockItem:
        response = await apiClient.post('/livestock', json=listingData)
        return handleApiResponse(response)

    @staticmethod
    async def updateListing(id: str, listingData: Dict[str, Any]) -> LivestockItem:
        response = await apiClient.put(f'/livestock/{id}', json=listingData)
        return handleApiResponse(response)

    @staticmethod
    async def deleteListing(id: str) -> None:
        await apiClient.delete(f'/livestock/{id}')

    @staticmethod
    async def searchListings(query: str, filters: Any = None) -> PaginatedResponse:
        # params: { query, ...filters }
        params = {'query': query}
        if filters:
            params.update(filters) # assumes filters is dict
            
        response = await apiClient.get('/livestock/search', params=params)
        return handleApiResponse(response)

    @staticmethod
    async def getMyListings() -> List[LivestockItem]:
        response = await apiClient.get('/livestock/my-listings')
        return handleApiResponse(response)

    @staticmethod
    async def uploadImage(file: Any) -> Dict[str, string]: # { url: string }
        # const formData = new FormData()
        # formData.append('image', file)
        # httpx handles multipart if 'files' is passed
        files = {'image': file}
        
        # const response = await apiClient.post(..., { headers: { 'Content-Type': 'multipart/form-data' } })
        # httpx sets multipart boundary automatically if files provided.
        # Manually setting content-type often breaks boundary in httpx/requests.
        # TS code explicitly sets it. I will let httpx handle it to be "correct" structurally,
        # OR I should mimic explicit header?
        # If I strictly follow:
        # request headers...
        # But httpx overrides it. I will trust httpx behavior for "upload logic".
        
        response = await apiClient.post('/livestock/upload-image', files=files) 
        return handleApiResponse(response)

livestockAPI = LivestockAPI()


# --- Bidding API ---
class BiddingAPI:
    @staticmethod
    async def placeBid(livestockId: str, amount: float) -> Bid:
        response = await apiClient.post(f'/livestock/{livestockId}/bid', json={'amount': amount})
        return handleApiResponse(response)

    @staticmethod
    async def getBidHistory(livestockId: str) -> List[Bid]:
        response = await apiClient.get(f'/livestock/{livestockId}/bids')
        return handleApiResponse(response)

    @staticmethod
    async def getMyBids() -> List[Bid]:
        response = await apiClient.get('/bids/my-bids')
        return handleApiResponse(response)

    @staticmethod
    async def retractBid(bidId: str) -> None:
        await apiClient.delete(f'/bids/{bidId}')

biddingAPI = BiddingAPI()


# --- Notifications API ---
class NotificationsAPI:
    @staticmethod
    async def getNotifications() -> List[Notification]:
        response = await apiClient.get('/notifications')
        return handleApiResponse(response)

    @staticmethod
    async def markAsRead(notificationId: str) -> None:
        await apiClient.put(f'/notifications/{notificationId}/read')

    @staticmethod
    async def markAllAsRead() -> None:
        await apiClient.put('/notifications/mark-all-read')

    @staticmethod
    async def deleteNotification(notificationId: str) -> None:
        await apiClient.delete(f'/notifications/{notificationId}')

    @staticmethod
    async def getUnreadCount() -> int:
        response = await apiClient.get('/notifications/unread-count')
        data = handleApiResponse(response)
        return data['count']

notificationsAPI = NotificationsAPI()


# --- Messages API ---
class MessagesAPI:
    @staticmethod
    async def getConversations() -> List[Any]:
        response = await apiClient.get('/messages/conversations')
        return handleApiResponse(response)

    @staticmethod
    async def getMessages(conversationId: str) -> List[Any]:
        response = await apiClient.get(f'/messages/conversations/{conversationId}')
        return handleApiResponse(response)

    @staticmethod
    async def sendMessage(receiverId: str, content: str, attachments: List[Any] = None) -> Any:
        # const formData = new FormData()
        data = {
            'receiverId': receiverId,
            'content': content
        }
        
        files = []
        if attachments:
            for file in attachments:
                # files needs to be list of tuples for multiple files with same key 'attachments'
                # ('attachments', file)
                files.append(('attachments', file))
        
        # httpx post(..., data=data, files=files)
        response = await apiClient.post('/messages/send', data=data, files=files if files else None)
        return handleApiResponse(response)

    @staticmethod
    async def markAsRead(messageId: str) -> None:
        await apiClient.put(f'/messages/{messageId}/read')

messagesAPI = MessagesAPI()


# --- Analytics API ---
class AnalyticsAPI:
    @staticmethod
    async def getListingStats(listingId: str) -> Any:
        response = await apiClient.get(f'/analytics/listing/{listingId}')
        return handleApiResponse(response)

    @staticmethod
    async def getUserStats() -> Any:
        response = await apiClient.get('/analytics/user')
        return handleApiResponse(response)

analyticsAPI = AnalyticsAPI()


# --- Mock data for development ---
class MockAPI:
    @staticmethod
    def getMockListings() -> List[LivestockItem]:
        # Return list of mocked dictionaries matching LifecycleItem structure
        return [
            {
                'id': '1',
                'title': 'Prime Brahman Bull',
                'breed': 'Brahman',
                'age': '3 years',
                'weight': '850kg',
                'location': 'Harare',
                'currentBid': 1200,
                'startingPrice': 800,
                'timeLeft': '2d 5h',
                'imageUrl': 'https://images.unsplash.com/photo-1560114928-40f1f1eb26a0?w=400',
                'seller': {
                    'id': '1',
                    'name': 'T. Chikwanha',
                    'verified': True,
                    'rating': 4.8,
                    'totalSales': 45,
                    'location': 'Harare',
                    'joinedDate': datetime.fromisoformat('2022-01-15T00:00:00'), # new Date('...')
                },
                'bidCount': 8,
                'views': 156,
                'category': 'cattle',
                'description': 'Excellent breeding bull with proven genetics',
                'healthStatus': 'verified',
                'createdAt': datetime.fromisoformat('2024-01-15T00:00:00'),
                'updatedAt': datetime.fromisoformat('2024-01-15T00:00:00'),
                'auctionEndDate': datetime.fromisoformat('2024-01-20T00:00:00'),
            },
            # Add more mock data as needed
        ]

mockAPI = MockAPI()
