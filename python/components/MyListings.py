# AUTO-GENERATED FROM TypeScript
# SOURCE: components/MyListings.tsx
# CONVERSION STAGE: STAGE 3
# DO NOT MODIFY LOGIC WITHOUT COMPARING TO ORIGINAL

from src.lib.react import React, jsx

# UI Imports
try:
    from components.ui.card import Card, CardContent, CardHeader
    from components.ui.button import Button
    from components.ui.badge import Badge
    from components.figma.ImageWithFallback import ImageWithFallback
except ImportError:
    # Mocks
    Card = lambda props, *c: jsx('Card', props, *c)
    CardContent = lambda props, *c: jsx('CardContent', props, *c)
    CardHeader = lambda props, *c: jsx('CardHeader', props, *c)
    Button = lambda props, *c: jsx('Button', props, *c)
    Badge = lambda props, *c: jsx('Badge', props, *c)
    ImageWithFallback = lambda props, *c: jsx('ImageWithFallback', props, *c)

# Icons
Clock = lambda p: jsx('Clock', p)
Eye = lambda p: jsx('Eye', p)
MessageCircle = lambda p: jsx('MessageCircle', p)
Edit3 = lambda p: jsx('Edit3', p)
Trash2 = lambda p: jsx('Trash2', p)
TrendingUp = lambda p: jsx('TrendingUp', p)
DollarSign = lambda p: jsx('DollarSign', p)
AlertCircle = lambda p: jsx('AlertCircle', p)
List = lambda p: jsx('List', p)

mockListings = [
  {
    'id': '1',
    'title': 'Prime Brahman Bull',
    'breed': 'Brahman',
    'currentBid': 1200,
    'startingPrice': 800,
    'timeLeft': '2d 5h',
    'imageUrl': 'https://images.unsplash.com/photo-1560114928-40f1f1eb26a0?w=400',
    'status': 'active',
    'bidCount': 8,
    'views': 156,
    'category': 'cattle'
  },
  {
    'id': '2',
    'title': 'Dairy Cow - High Milk Production',
    'breed': 'Holstein',
    'currentBid': 850,
    'startingPrice': 600,
    'timeLeft': 'Ended',
    'imageUrl': 'https://images.unsplash.com/photo-1596003844243-b8ffd9b04095?w=400',
    'status': 'sold',
    'bidCount': 15,
    'views': 234,
    'category': 'cattle'
  },
  {
    'id': '3',
    'title': 'Young Boer Goat Buck',
    'breed': 'Boer',
    'currentBid': 0,
    'startingPrice': 180,
    'timeLeft': 'Pending Review',
    'imageUrl': 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=400',
    'status': 'pending',
    'bidCount': 0,
    'views': 12,
    'category': 'goats'
  }
]

def MyListings(props):
    # const [listings] = useState(mockListings);
    listings = mockListings

    # const formatCurrency = (amount: number) => {...};
    def formatCurrency(amount):
        return f"${amount:,.0f}"

    # const getStatusColor = (status: string) => {...};
    def getStatusColor(status):
        if status == 'active': return 'bg-green-100 text-green-800 border-green-200'
        if status == 'ended': return 'bg-gray-100 text-gray-800 border-gray-200'
        if status == 'pending': return 'bg-yellow-100 text-yellow-800 border-yellow-200'
        if status == 'sold': return 'bg-blue-100 text-blue-800 border-blue-200'
        return 'bg-gray-100 text-gray-800 border-gray-200'

    # const getStatusText = (status: string) => {...};
    def getStatusText(status):
        if status == 'active': return 'Active'
        if status == 'ended': return 'Ended'
        if status == 'pending': return 'Under Review'
        if status == 'sold': return 'Sold'
        return status

    # const getCategoryIcon = (category: string) => {...};
    def getCategoryIcon(category):
        icons = {
            'cattle': '🐄',
            'goats': '🐐',
            'sheep': '🐑',
            'pigs': '🐷',
            'chickens': '🐔'
        }
        return icons.get(category, '🐄')

    # const activeListings = listings.filter(l => l.status === 'active').length;
    activeListings = len([l for l in listings if l['status'] == 'active'])
    
    # const totalViews = listings.reduce((sum, l) => sum + l.views, 0);
    totalViews = sum(l['views'] for l in listings)
    
    # const totalBids = listings.reduce((sum, l) => sum + l.bidCount, 0);
    totalBids = sum(l['bidCount'] for l in listings)

    return jsx('div', {'className': "space-y-4 pb-20"},
        # Header
        jsx('div', {'className': "sticky top-0 z-10 bg-background/95 backdrop-blur-sm border-b p-4"},
            jsx('h1', {'className': "text-xl font-bold"}, "My Listings"),
            jsx('p', {'className': "text-sm text-muted-foreground"}, "Manage your livestock auctions")
        ),

        # Stats
        jsx('div', {'className': "px-4"},
            jsx('div', {'className': "grid grid-cols-3 gap-4"},
                jsx('div', {'className': "text-center p-3 bg-primary/10 rounded-lg"},
                    jsx('p', {'className': "text-2xl font-bold text-primary"}, activeListings),
                    jsx('p', {'className': "text-xs text-muted-foreground"}, "Active Auctions")
                ),
                jsx('div', {'className': "text-center p-3 bg-accent/20 rounded-lg"},
                    jsx('p', {'className': "text-2xl font-bold text-accent-foreground"}, totalViews),
                    jsx('p', {'className': "text-xs text-muted-foreground"}, "Total Views")
                ),
                jsx('div', {'className': "text-center p-3 bg-secondary/20 rounded-lg"},
                    jsx('p', {'className': "text-2xl font-bold text-secondary-foreground"}, totalBids),
                    jsx('p', {'className': "text-xs text-muted-foreground"}, "Total Bids")
                )
            )
        ),

        # Filter Tabs
        jsx('div', {'className': "px-4"},
            jsx('div', {'className': "flex gap-2 overflow-x-auto pb-2"},
                jsx(Badge, {'variant': "default", 'className': "whitespace-nowrap"}, "All"),
                jsx(Badge, {'variant': "outline", 'className': "whitespace-nowrap"}, "Active"),
                jsx(Badge, {'variant': "outline", 'className': "whitespace-nowrap"}, "Ended"),
                jsx(Badge, {'variant': "outline", 'className': "whitespace-nowrap"}, "Pending"),
                jsx(Badge, {'variant': "outline", 'className': "whitespace-nowrap"}, "Sold")
            )
        ),

        # Listings
        jsx('div', {'className': "px-4 space-y-4"},
            *[jsx(
                Card,
                {'key': listing['id'], 'className': "overflow-hidden"},
                jsx('div', {'className': "relative"},
                    jsx(ImageWithFallback, {
                        'src': listing['imageUrl'],
                        'alt': listing['title'],
                        'className': "w-full h-40 object-cover"
                    }),
                    jsx('div', {'className': "absolute top-3 left-3"},
                        jsx(Badge, {'className': "bg-primary/90 text-primary-foreground"},
                            f"{getCategoryIcon(listing['category'])} {listing['breed']}"
                        )
                    ),
                    jsx('div', {'className': "absolute top-3 right-3"},
                        jsx(Badge, {'className': f"border {getStatusColor(listing['status'])}"},
                            getStatusText(listing['status'])
                        )
                    ),
                    jsx('div', {'className': "absolute bottom-3 right-3"},
                        jsx(Badge, {'variant': "destructive", 'className': "bg-red-600"},
                            jsx(Clock, {'className': "w-3 h-3 mr-1"}),
                            listing['timeLeft']
                        )
                    ) if listing['status'] == 'active' else None
                ),
                jsx(CardHeader, {'className': "pb-3"},
                    jsx('div', {'className': "flex items-start justify-between"},
                        jsx('div', {'className': "flex-1"},
                            jsx('h3', {'className': "font-semibold text-lg"}, listing['title']),
                            jsx('div', {'className': "flex items-center gap-4 mt-2"},
                                jsx('div', {'className': "flex items-center gap-4"},
                                    jsx('div', {},
                                        jsx('p', {'className': "text-xs text-muted-foreground"},
                                            "Current Bid" if listing['currentBid'] > 0 else "Starting Price"
                                        ),
                                        jsx('p', {'className': "font-bold text-lg text-primary"},
                                            formatCurrency(listing['currentBid']) if listing['currentBid'] > 0 else formatCurrency(listing['startingPrice'])
                                        )
                                    ),
                                    jsx('div', {'className': "flex items-center gap-1 text-green-600"},
                                        jsx(TrendingUp, {'className': "w-4 h-4"}),
                                        jsx('span', {'className': "text-sm font-medium"},
                                            f"+{((listing['currentBid'] - listing['startingPrice']) / listing['startingPrice'] * 100):.0f}%"
                                        )
                                    ) if listing['currentBid'] > 0 else None
                                ) if listing['status'] in ['active', 'ended', 'sold'] else \
                                jsx('div', {'className': "flex items-center gap-2 text-yellow-600"},
                                    jsx(AlertCircle, {'className': "w-4 h-4"}),
                                    jsx('span', {'className': "text-sm"}, "Under review - will be live within 24 hours")
                                )
                            )
                        )
                    )
                ),
                jsx(CardContent, {'className': "pt-0 space-y-3"},
                    jsx('div', {'className': "flex items-center justify-between text-sm"},
                        jsx('div', {'className': "flex items-center gap-4 text-muted-foreground"},
                            jsx('div', {'className': "flex items-center gap-1"},
                                jsx(Eye, {'className': "w-4 h-4"}), listing['views']
                            ),
                            jsx('div', {'className': "flex items-center gap-1"},
                                jsx(MessageCircle, {'className': "w-4 h-4"}), listing['bidCount']
                            )
                        ),
                        jsx('div', {'className': "flex items-center gap-1 text-blue-600"},
                            jsx(DollarSign, {'className': "w-4 h-4"}),
                            jsx('span', {'className': "font-medium"}, f"Sold for {formatCurrency(listing['currentBid'])}")
                        ) if listing['status'] == 'sold' else None
                    ),
                    jsx('div', {'className': "flex gap-2"},
                        jsx(React.Fragment, {},
                            jsx(Button, {'variant': "outline", 'size': "sm", 'className': "flex-1"},
                                jsx(Edit3, {'className': "w-4 h-4 mr-1"}), "Edit"
                            ),
                            jsx(Button, {'variant': "outline", 'size': "sm", 'className': "flex-1"},
                                jsx(MessageCircle, {'className': "w-4 h-4 mr-1"}), "Messages"
                            )
                        ) if listing['status'] == 'active' else None,
                        
                        jsx(Button, {'variant': "outline", 'size': "sm", 'className': "flex-1"},
                            jsx(Edit3, {'className': "w-4 h-4 mr-1"}), "Edit"
                        ) if listing['status'] == 'pending' else None,
                        
                        jsx(Button, {'variant': "outline", 'size': "sm", 'className': "flex-1"},
                            jsx(MessageCircle, {'className': "w-4 h-4 mr-1"}), "View Messages"
                        ) if listing['status'] in ['ended', 'sold'] else None,
                        
                        jsx(Button, {'variant': "ghost", 'size': "sm", 'className': "text-destructive hover:text-destructive p-2"},
                            jsx(Trash2, {'className': "w-4 h-4"})
                        )
                    )
                )
            ) for listing in listings]
        ),
        
        jsx('div', {'className': "text-center py-12"},
            jsx('div', {'className': "w-24 h-24 mx-auto mb-4 bg-muted rounded-full flex items-center justify-center"},
                jsx(List, {'className': "w-12 h-12 text-muted-foreground"})
            ),
            jsx('h3', {'className': "font-semibold mb-2"}, "No listings yet"),
            jsx('p', {'className': "text-muted-foreground mb-4"}, "Start by posting your first livestock for auction"),
            jsx(Button, {}, "Post Livestock")
        ) if len(listings) == 0 else None
    )
