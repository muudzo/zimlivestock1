# AUTO-GENERATED FROM TypeScript
# SOURCE: components/BiddingScreen.tsx
# CONVERSION STAGE: STAGE 3
# DO NOT MODIFY LOGIC WITHOUT COMPARING TO ORIGINAL

import math
from datetime import datetime, timedelta
from src.lib.react import React, jsx
from src.lib.utils import formatCurrency as formatCurrencyUtil # Reuse util if available or redefine locally as per component logic

# UI Imports
try:
    from components.ui.button import Button
    from components.ui.input import Input
    from components.ui.card import Card, CardContent, CardHeader, CardTitle
    from components.ui.badge import Badge
    from components.ui.avatar import Avatar, AvatarFallback, AvatarImage
    from components.figma.ImageWithFallback import ImageWithFallback
except ImportError:
    # Mocks
    Button = lambda props, *c: jsx('Button', props, *c)
    Input = lambda props, *c: jsx('Input', props, *c)
    Card = lambda props, *c: jsx('Card', props, *c)
    CardContent = lambda props, *c: jsx('CardContent', props, *c)
    CardHeader = lambda props, *c: jsx('CardHeader', props, *c)
    CardTitle = lambda props, *c: jsx('CardTitle', props, *c)
    Badge = lambda props, *c: jsx('Badge', props, *c)
    Avatar = lambda props, *c: jsx('Avatar', props, *c)
    AvatarFallback = lambda props, *c: jsx('AvatarFallback', props, *c)
    AvatarImage = lambda props, *c: jsx('AvatarImage', props, *c)
    ImageWithFallback = lambda props, *c: jsx('ImageWithFallback', props, *c)

# Icons
ArrowLeft = lambda p: jsx('ArrowLeft', p)
Clock = lambda p: jsx('Clock', p)
MapPin = lambda p: jsx('MapPin', p)
Weight = lambda p: jsx('Weight', p)
Calendar = lambda p: jsx('Calendar', p)
TrendingUp = lambda p: jsx('TrendingUp', p)
Heart = lambda p: jsx('Heart', p)
Share = lambda p: jsx('Share', p)
MessageCircle = lambda p: jsx('MessageCircle', p)
Shield = lambda p: jsx('Shield', p)
Award = lambda p: jsx('Award', p)

def BiddingScreen(props):
    onBack = props.get('onBack')
    livestockItem = props.get('livestockItem')

    # const [bidAmount, setBidAmount] = useState('');
    bidAmount = ''
    def setBidAmount(val): pass

    # const [timeLeft, setTimeLeft] = useState('2d 5h 23m');
    timeLeft = '2d 5h 23m'
    def setTimeLeft(val): pass

    # const [isLiked, setIsLiked] = useState(false);
    isLiked = False
    def setIsLiked(val): pass

    # const [bidHistory] = useState<Bid[]>([...]);
    # Mock data initialization
    bidHistory = [
        {
            'id': '1', 'bidder': 'J. Manyika', 'amount': 1200,
            'timestamp': datetime.now() - timedelta(minutes=5),
            'isWinning': True
        },
        {
            'id': '2', 'bidder': 'R. Chigwamba', 'amount': 1150,
            'timestamp': datetime.now() - timedelta(minutes=15),
            'isWinning': False
        },
        {
            'id': '3', 'bidder': 'P. Mukamuri', 'amount': 1100,
            'timestamp': datetime.now() - timedelta(minutes=30),
            'isWinning': False
        },
        {
            'id': '4', 'bidder': 'T. Nhongo', 'amount': 1000,
            'timestamp': datetime.now() - timedelta(minutes=60),
            'isWinning': False
        }
    ]

    # const currentHighestBid = bidHistory[0]?.amount || livestockItem.startingPrice;
    currentHighestBid = bidHistory[0]['amount'] if bidHistory else livestockItem['startingPrice']
    
    # const minimumBid = currentHighestBid + 50;
    minimumBid = currentHighestBid + 50

    # useEffect(() => { setBidAmount(minimumBid.toString()); }, [minimumBid]);
    # Logic applied immediately usually for translation unless event driven
    # setBidAmount(str(minimumBid))

    # const formatCurrency = (amount: number) => { return `$${amount.toLocaleString()}`; };
    def formatCurrency(amount):
        return f"${amount:,.0f}" # basic formatting

    # const formatTimeAgo = (date: Date) => { ... };
    def formatTimeAgo(date):
        now = datetime.now()
        diffInMinutes = math.floor((now.timestamp() - date.timestamp()) / 60)
        
        if diffInMinutes < 1: return 'Just now'
        if diffInMinutes < 60: return f"{diffInMinutes}m ago"
        if diffInMinutes < 1440: return f"{math.floor(diffInMinutes / 60)}h ago"
        return f"{math.floor(diffInMinutes / 1440)}d ago"

    # const handlePlaceBid = () => { ... };
    def handlePlaceBid():
        try:
            amount = int(bidAmount)
            if amount >= minimumBid:
                print(f"Bid of {formatCurrency(amount)} placed successfully!") # alert mock
        except ValueError:
            pass

    return jsx('div', {'className': "min-h-screen bg-background"},
        # Header
        jsx('div', {'className': "sticky top-0 z-10 bg-background/95 backdrop-blur-sm border-b"},
            jsx('div', {'className': "flex items-center justify-between p-4"},
                jsx(Button, {'variant': "ghost", 'size': "sm", 'onClick': onBack},
                    jsx(ArrowLeft, {'className': "w-4 h-4 mr-2"}), "Back"
                ),
                jsx('div', {'className': "flex gap-2"},
                    jsx(Button, {
                        'variant': "ghost",
                        'size': "sm",
                        'onClick': lambda: setIsLiked(not isLiked),
                        'className': "p-2"
                    }, jsx(Heart, {'className': f"w-5 h-5 {'fill-red-500 text-red-500' if isLiked else 'text-gray-600'}"})),
                    jsx(Button, {'variant': "ghost", 'size': "sm", 'className': "p-2"},
                        jsx(Share, {'className': "w-5 h-5"})
                    )
                )
            )
        ),
        
        jsx('div', {'className': "pb-32"},
            # Image
            jsx('div', {'className': "relative"},
                jsx(ImageWithFallback, {
                    'src': livestockItem['imageUrl'],
                    'alt': livestockItem['title'],
                    'className': "w-full h-64 object-cover"
                }),
                jsx('div', {'className': "absolute bottom-4 left-4"},
                    jsx(Badge, {'className': "bg-primary/90 text-primary-foreground text-base px-3 py-1"},
                        f"🐄 {livestockItem['breed']}"
                    )
                ),
                jsx('div', {'className': "absolute bottom-4 right-4"},
                    jsx(Badge, {'variant': "destructive", 'className': "bg-red-600 text-base px-3 py-1"},
                        jsx(Clock, {'className': "w-4 h-4 mr-1"}),
                        timeLeft
                    )
                )
            ),

            # Content
            jsx('div', {'className': "p-4 space-y-6"},
                # Title and Current Bid
                jsx('div', {},
                    jsx('h1', {'className': "text-2xl font-bold mb-2"}, livestockItem['title']),
                    jsx('div', {'className': "flex items-center justify-between"},
                        jsx('div', {},
                            jsx('p', {'className': "text-sm text-muted-foreground"}, "Current Highest Bid"),
                            jsx('p', {'className': "text-3xl font-bold text-primary"}, formatCurrency(currentHighestBid)),
                            jsx('p', {'className': "text-sm text-muted-foreground"},
                                f"Starting at {formatCurrency(livestockItem['startingPrice'])}"
                            )
                        ),
                        jsx('div', {'className': "text-right"},
                            jsx('div', {'className': "flex items-center gap-1 text-green-600"},
                                jsx(TrendingUp, {'className': "w-4 h-4"}),
                                jsx('span', {'className': "text-sm font-medium"},
                                    f"+{((currentHighestBid - livestockItem['startingPrice']) / livestockItem['startingPrice'] * 100):.0f}%"
                                )
                            ),
                            jsx('p', {'className': "text-xs text-muted-foreground"}, f"{len(bidHistory)} bids")
                        )
                    )
                ),

                # Details
                jsx('div', {'className': "grid grid-cols-2 gap-4"},
                    jsx('div', {'className': "flex items-center gap-2"},
                         jsx(Calendar, {'className': "w-4 h-4 text-muted-foreground"}),
                         jsx('div', {},
                             jsx('p', {'className': "text-xs text-muted-foreground"}, "Age"),
                             jsx('p', {'className': "font-medium"}, livestockItem['age'])
                         )
                    ),
                    jsx('div', {'className': "flex items-center gap-2"},
                         jsx(Weight, {'className': "w-4 h-4 text-muted-foreground"}),
                         jsx('div', {},
                             jsx('p', {'className': "text-xs text-muted-foreground"}, "Weight"),
                             jsx('p', {'className': "font-medium"}, livestockItem['weight'])
                         )
                    ),
                    jsx('div', {'className': "flex items-center gap-2"},
                         jsx(MapPin, {'className': "w-4 h-4 text-muted-foreground"}),
                         jsx('div', {},
                             jsx('p', {'className': "text-xs text-muted-foreground"}, "Location"),
                             jsx('p', {'className': "font-medium"}, livestockItem['location'])
                         )
                    ),
                    jsx('div', {'className': "flex items-center gap-2"},
                         jsx(Shield, {'className': "w-4 h-4 text-muted-foreground"}),
                         jsx('div', {},
                             jsx('p', {'className': "text-xs text-muted-foreground"}, "Health"),
                             jsx('p', {'className': "font-medium text-green-600"}, "Verified")
                         )
                    )
                ),

                # Seller Info
                jsx(Card, {},
                    jsx(CardHeader, {'className': "pb-3"},
                        jsx('div', {'className': "flex items-center justify-between"},
                            jsx('div', {'className': "flex items-center gap-3"},
                                jsx(Avatar, {'className': "w-12 h-12"},
                                    jsx(AvatarImage, {'src': livestockItem['seller'].get('avatar')}),
                                    jsx(AvatarFallback, {}, livestockItem['seller']['name'][0])
                                ),
                                jsx('div', {},
                                    jsx('p', {'className': "font-semibold"}, livestockItem['seller']['name']),
                                    jsx('div', {'className': "flex items-center gap-2 text-sm text-muted-foreground"},
                                        jsx(React.Fragment, {},
                                            jsx(Shield, {'className': "w-3 h-3 text-green-600"}),
                                            jsx('span', {'className': "text-green-600"}, "Verified Farmer")
                                        ) if livestockItem['seller'].get('verified') else None,
                                        jsx(Award, {'className': "w-3 h-3"}),
                                        jsx('span', {}, "4.8 rating")
                                    )
                                )
                            ),
                            jsx(Button, {'variant': "outline", 'size': "sm"},
                                jsx(MessageCircle, {'className': "w-4 h-4 mr-1"}), "Chat"
                            )
                        )
                    )
                ),

                # Bid History
                jsx(Card, {},
                    jsx(CardHeader, {},
                        jsx(CardTitle, {'className': "flex items-center gap-2"},
                            jsx(TrendingUp, {'className': "w-5 h-5"}), "Bid History"
                        )
                    ),
                    jsx(CardContent, {'className': "space-y-3"},
                        *[jsx('div', {'key': bid['id'], 'className': "flex items-center justify-between p-2 rounded-lg bg-muted/50"},
                             jsx('div', {'className': "flex items-center gap-2"},
                                 jsx(Avatar, {'className': "w-8 h-8"},
                                     jsx(AvatarFallback, {}, bid['bidder'][0])
                                 ),
                                 jsx('div', {},
                                     jsx('p', {'className': "font-medium text-sm"}, bid['bidder']),
                                     jsx('p', {'className': "text-xs text-muted-foreground"}, formatTimeAgo(bid['timestamp']))
                                 )
                             ),
                             jsx('div', {'className': "text-right"},
                                 jsx('p', {'className': f"font-bold {'text-primary' if bid['isWinning'] else 'text-foreground'}"},
                                     formatCurrency(bid['amount'])
                                 ),
                                 jsx(Badge, {'variant': "default", 'className': "text-xs"}, "Winning") if bid['isWinning'] else None
                             )
                        ) for bid in bidHistory]
                    )
                )
            )
        ),

        # Fixed Bottom Bidding Section
        jsx('div', {'className': "fixed bottom-0 left-0 right-0 bg-background border-t p-4 space-y-3"},
            jsx('div', {'className': "flex items-center justify-between"},
                jsx('div', {},
                    jsx('p', {'className': "text-sm text-muted-foreground"}, "Minimum bid"),
                    jsx('p', {'className': "font-bold text-lg"}, formatCurrency(minimumBid))
                ),
                jsx('div', {'className': "text-right"},
                    jsx('p', {'className': "text-sm text-muted-foreground"}, "Auction ends in"),
                    jsx('p', {'className': "font-bold text-lg text-red-600"}, timeLeft)
                )
            ),
            
            jsx('div', {'className': "flex gap-2"},
                jsx('div', {'className': "flex-1"},
                    jsx(Input, {
                        'type': "number",
                        'value': bidAmount,
                        'onChange': lambda e: setBidAmount(e['target']['value']), # Mock event access
                        'placeholder': f"Minimum {formatCurrency(minimumBid)}",
                        'className': "h-12 text-center font-semibold",
                        'min': minimumBid
                    })
                ),
                jsx(Button, {
                    'className': "h-12 px-8",
                    'onClick': handlePlaceBid,
                    # Logic: disabled={parseInt(bidAmount) < minimumBid}
                    'disabled': (int(bidAmount) if bidAmount.isdigit() else 0) < minimumBid
                }, "Place Bid")
            )
        )
    )
