# AUTO-GENERATED FROM TypeScript
# SOURCE: components/HomeFeed.tsx
# CONVERSION STAGE: STAGE 3
# DO NOT MODIFY LOGIC WITHOUT COMPARING TO ORIGINAL

from typing import Set, List, Optional
from datetime import datetime
from src.lib.react import React, jsx
from src.lib.react_query import useQuery
from src.services.api import livestockAPI, window
from src.lib.utils import formatCurrency, getCategoryIcon

# UI Imports
try:
    from components.ui.card import Card, CardContent, CardHeader
    from components.ui.button import Button
    from components.ui.badge import Badge
    from components.ui.avatar import Avatar, AvatarFallback, AvatarImage
    from components.figma.ImageWithFallback import ImageWithFallback
except ImportError:
    # Mocks
    Card = lambda props, *c: jsx('Card', props, *c)
    CardContent = lambda props, *c: jsx('CardContent', props, *c)
    CardHeader = lambda props, *c: jsx('CardHeader', props, *c)
    Button = lambda props, *c: jsx('Button', props, *c)
    Badge = lambda props, *c: jsx('Badge', props, *c)
    Avatar = lambda props, *c: jsx('Avatar', props, *c)
    AvatarFallback = lambda props, *c: jsx('AvatarFallback', props, *c)
    AvatarImage = lambda props, *c: jsx('AvatarImage', props, *c)
    ImageWithFallback = lambda props, *c: jsx('ImageWithFallback', props, *c)

# Icons (Lucide) - Mock
Clock = lambda p: jsx('Clock', p)
MapPin = lambda p: jsx('MapPin', p)
Weight = lambda p: jsx('Weight', p)
Calendar = lambda p: jsx('Calendar', p)
Eye = lambda p: jsx('Eye', p)
Heart = lambda p: jsx('Heart', p)
MessageCircle = lambda p: jsx('MessageCircle', p)
Loader2 = lambda p: jsx('Loader2', p)

mockListings = [
    # Translated mock data structure
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
        'imageUrl': 'https://images.unsplash.com/photo-1560114928-40f1f1eb26a0?w=400&fit=crop&crop=center',
        'seller': {
          'id': '1',
          'name': 'T. Chikwanha',
          'verified': True,
          'rating': 4.8,
          'totalSales': 45,
          'location': 'Harare',
          'joinedDate': datetime(2022, 1, 15),
        },
        'bidCount': 8,
        'views': 156,
        'category': 'cattle',
        'description': 'Excellent breeding bull with proven genetics',
        'healthStatus': 'verified',
        'createdAt': datetime(2024, 1, 15),
        'updatedAt': datetime(2024, 1, 15),
        'auctionEndDate': datetime(2024, 1, 20),
     },
     # ... (Abbreviated for brevity, normally includes all)
]

def HomeFeed(props):
    onItemClick = props.get('onItemClick')
    
    # const [likedItems, setLikedItems] = useState<Set<string>>(new Set());
    likedItems = set() 
    def setLikedItems_mock(val_or_fn): pass # Logic placeholder
    
    # const [selectedCategory, setSelectedCategory] = useState<string>('all');
    selectedCategory = 'all'
    def setSelectedCategory(val): pass

    # Fetch livestock listings with React Query
    # const { data: listings, isLoading, error } = useQuery(...)
    query_result = useQuery(
        ['livestock', selectedCategory],
        lambda: livestockAPI.getListings({
            'category': None if selectedCategory == 'all' else selectedCategory,
            'limit': 20
        }),
        {
            'staleTime': 5 * 60 * 1000,
            'cacheTime': 10 * 60 * 1000,
            'retry': 2
        }
    )
    listings = query_result.data
    isLoading = query_result.isLoading
    error = query_result.error

    # const toggleLike = useCallback(...)
    def toggleLike(itemId, e):
        # Logic representation
        if hasattr(e, 'stopPropagation'): e.stopPropagation()
        if itemId in likedItems:
            likedItems.remove(itemId)
        else:
            likedItems.add(itemId)

    # const filteredListings = useMemo(...)
    filteredListings = []
    if listings and listings.get('data'):
        data_list = listings['data']
        if selectedCategory == 'all':
            filteredListings = data_list
        else:
            filteredListings = [item for item in data_list if item['category'] == selectedCategory]
    else:
        filteredListings = mockListings
    
    # Loading state
    if isLoading:
        return jsx('div', {'className': "space-y-4 pb-20"},
            jsx('div', {'className': "sticky top-0 z-10 bg-background/95 backdrop-blur-sm border-b p-4"},
                jsx('h1', {'className': "text-xl font-bold"}, "Livestock Marketplace"),
                jsx('p', {'className': "text-sm text-muted-foreground"}, "Latest auctions from farmers across Zimbabwe")
            ),
            jsx('div', {'className': "flex items-center justify-center py-12"},
                jsx('div', {'className': "text-center space-y-4"},
                    jsx(Loader2, {'className': "w-8 h-8 animate-spin mx-auto text-primary"}),
                    jsx('p', {'className': "text-muted-foreground"}, "Loading livestock listings...")
                )
            )
        )

    # Error state
    if error:
        return jsx('div', {'className': "space-y-4 pb-20"},
            jsx('div', {'className': "sticky top-0 z-10 bg-background/95 backdrop-blur-sm border-b p-4"},
                jsx('h1', {'className': "text-xl font-bold"}, "Livestock Marketplace"),
                jsx('p', {'className': "text-sm text-muted-foreground"}, "Latest auctions from farmers across Zimbabwe")
            ),
            jsx('div', {'className': "flex items-center justify-center py-12"},
                jsx('div', {'className': "text-center space-y-4"},
                    jsx('div', {'className': "w-16 h-16 bg-destructive/10 rounded-full flex items-center justify-center mx-auto"},
                        jsx('span', {'className': "text-2xl"}, "⚠️")
                    ),
                    jsx('h3', {'className': "text-lg font-semibold"}, "Failed to load listings"),
                    jsx('p', {'className': "text-muted-foreground"}, "Please try again later"),
                    jsx(Button, {'onClick': lambda: window.location.reload()}, "Retry")
                )
            )
        )

    categories = [
        {'id': 'all', 'label': 'All', 'icon': '🐄'},
        {'id': 'cattle', 'label': 'Cattle', 'icon': '🐄'},
        {'id': 'goats', 'label': 'Goats', 'icon': '🐐'},
        {'id': 'sheep', 'label': 'Sheep', 'icon': '🐑'},
        {'id': 'pigs', 'label': 'Pigs', 'icon': '🐷'},
        {'id': 'chickens', 'label': 'Chickens', 'icon': '🐔'}
    ]

    return jsx('div', {'className': "space-y-4 pb-20"},
        # Header
        jsx('div', {'className': "sticky top-0 z-10 bg-background/95 backdrop-blur-sm border-b p-4"},
            jsx('h1', {'className': "text-xl font-bold"}, "Livestock Marketplace"),
            jsx('p', {'className': "text-sm text-muted-foreground"}, "Latest auctions from farmers across Zimbabwe")
        ),
        
        # Filters
        jsx('div', {'className': "px-4"},
            jsx('div', {'className': "flex gap-2 overflow-x-auto pb-2"},
                *[jsx(Badge, {
                    'key': cat['id'],
                    'variant': "default" if selectedCategory == cat['id'] else "outline",
                    'className': "whitespace-nowrap cursor-pointer",
                    'onClick': lambda c=cat: setSelectedCategory(c['id'])
                  }, f"{cat['icon']} {cat['label']}") for cat in categories]
            )
        ),

        # Listings
        jsx('div', {'className': "px-4 space-y-4"},
            *[jsx(
                Card,
                {
                    'key': item['id'],
                    'className': "overflow-hidden cursor-pointer hover:shadow-lg transition-shadow card-interactive",
                    'onClick': lambda i=item: onItemClick(i)
                },
                jsx('div', {'className': "relative"},
                    jsx(ImageWithFallback, {
                        'src': item['imageUrl'],
                        'alt': item['title'],
                        'className': "w-full h-48 object-cover"
                    }),
                    jsx('div', {'className': "absolute top-3 left-3"},
                        jsx(Badge, {'className': "bg-primary/90 text-primary-foreground"},
                            f"{getCategoryIcon(item['category'])} {item['breed']}"
                        )
                    ),
                    jsx('div', {'className': "absolute top-3 right-3"},
                        jsx(Button, {
                            'variant': "ghost",
                            'size': "sm",
                            'className': "bg-white/90 hover:bg-white p-2 h-auto",
                            'onClick': lambda e, i=item: toggleLike(i['id'], e)
                        }, jsx(Heart, {
                            'className': f"w-4 h-4 {'fill-red-500 text-red-500' if item['id'] in likedItems else 'text-gray-600'}"
                        }))
                    ),
                    jsx('div', {'className': "absolute bottom-3 right-3"},
                        jsx(Badge, {'variant': "destructive", 'className': "bg-red-600"},
                            jsx(Clock, {'className': "w-3 h-3 mr-1"}),
                            item['timeLeft']
                        )
                    )
                ),
                jsx(CardHeader, {'className': "pb-3"},
                    jsx('div', {'className': "flex items-center justify-between"},
                        jsx('h3', {'className': "font-semibold text-lg"}, item['title']),
                        jsx('div', {'className': "text-right"},
                            jsx('p', {'className': "text-xs text-muted-foreground"}, "Current Bid"),
                            jsx('p', {'className': "font-bold text-lg text-primary"}, formatCurrency(item['currentBid']))
                        )
                    ),
                    jsx('div', {'className': "flex items-center gap-4 text-sm text-muted-foreground"},
                        jsx('div', {'className': "flex items-center gap-1"}, jsx(Calendar, {'className': "w-4 h-4"}), item['age']),
                        jsx('div', {'className': "flex items-center gap-1"}, jsx(Weight, {'className': "w-4 h-4"}), item['weight']),
                        jsx('div', {'className': "flex items-center gap-1"}, jsx(MapPin, {'className': "w-4 h-4"}), item['location'])
                    )
                ),
                jsx(CardContent, {'className': "pt-0"},
                    jsx('div', {'className': "flex items-center justify-between"},
                        jsx('div', {'className': "flex items-center gap-2"},
                            jsx(Avatar, {'className': "w-8 h-8"},
                                jsx(AvatarImage, {'src': item['seller'].get('avatar')}),
                                jsx(AvatarFallback, {}, item['seller']['name'][0])
                            ),
                            jsx('div', {},
                                jsx('p', {'className': "text-sm font-medium"}, item['seller']['name']),
                                jsx('p', {'className': "text-xs text-primary"}, "✓ Verified") if item['seller']['verified'] else None
                            )
                        ),
                        jsx('div', {'className': "flex items-center gap-4 text-xs text-muted-foreground"},
                            jsx('div', {'className': "flex items-center gap-1"}, jsx(MessageCircle, {'className': "w-3 h-3"}), item['bidCount']),
                            jsx('div', {'className': "flex items-center gap-1"}, jsx(Eye, {'className': "w-3 h-3"}), item['views'])
                        )
                    ),
                    jsx('div', {'className': "mt-3 flex gap-2"},
                        jsx(Button, {'variant': "outline", 'size': "sm", 'className': "flex-1"},
                            jsx(MessageCircle, {'className': "w-4 h-4 mr-1"}), "Message"
                        ),
                        jsx(Button, {'size': "sm", 'className': "flex-1"}, "Place Bid")
                    )
                )
            ) for item in filteredListings]
        )
    )
