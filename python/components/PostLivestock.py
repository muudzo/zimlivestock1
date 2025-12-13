# AUTO-GENERATED FROM TypeScript
# SOURCE: components/PostLivestock.tsx
# CONVERSION STAGE: STAGE 3
# DO NOT MODIFY LOGIC WITHOUT COMPARING TO ORIGINAL

import asyncio
from src.lib.react import React, jsx

# UI Imports
try:
    from components.ui.button import Button
    from components.ui.input import Input
    from components.ui.textarea import Textarea
    from components.ui.label import Label
    from components.ui.card import Card, CardContent, CardHeader, CardTitle
    from components.ui.select import Select, SelectContent, SelectItem, SelectTrigger, SelectValue
except ImportError:
     # Mocks
    Button = lambda props, *c: jsx('Button', props, *c)
    Input = lambda props, *c: jsx('Input', props, *c)
    Textarea = lambda props, *c: jsx('Textarea', props, *c)
    Label = lambda props, *c: jsx('Label', props, *c)
    Card = lambda props, *c: jsx('Card', props, *c)
    CardContent = lambda props, *c: jsx('CardContent', props, *c)
    CardHeader = lambda props, *c: jsx('CardHeader', props, *c)
    CardTitle = lambda props, *c: jsx('CardTitle', props, *c)
    Select = lambda props, *c: jsx('Select', props, *c)
    SelectContent = lambda props, *c: jsx('SelectContent', props, *c)
    SelectItem = lambda props, *c: jsx('SelectItem', props, *c)
    SelectTrigger = lambda props, *c: jsx('SelectTrigger', props, *c)
    SelectValue = lambda props, *c: jsx('SelectValue', props, *c)

# Icons
ArrowLeft = lambda p: jsx('ArrowLeft', p)
Camera = lambda p: jsx('Camera', p)
MapPin = lambda p: jsx('MapPin', p)
DollarSign = lambda p: jsx('DollarSign', p)
Clock = lambda p: jsx('Clock', p)
Upload = lambda p: jsx('Upload', p)
X = lambda p: jsx('X', p)

def PostLivestock(props):
    onBack = props.get('onBack')

    # const [formData, setFormData] = useState({...});
    formData = {
        'title': '',
        'category': '',
        'breed': '',
        'age': '',
        'weight': '',
        'description': '',
        'location': '',
        'startingPrice': '',
        'auctionDuration': '',
        'healthStatus': ''
    }
    def setFormData(val_or_fn): pass # Mock setter

    # const [images, setImages] = useState<string[]>([]);
    images = []
    def setImages(val_or_fn): pass

    # const [isSubmitting, setIsSubmitting] = useState(false);
    isSubmitting = False
    def setIsSubmitting(val): pass

    # const handleInputChange = (field: string, value: string) => {...};
    def handleInputChange(field, value):
        # setFormData(prev => ({ ...prev, [field]: value }));
        formData[field] = value

    # const handleImageUpload = () => {...};
    def handleImageUpload():
        newImage = "https://images.unsplash.com/photo-1560114928-40f1f1eb26a0?w=400&h=300&fit=crop&crop=center"
        images.append(newImage)

    # const removeImage = (index: number) => {...};
    def removeImage(index):
        if 0 <= index < len(images):
            images.pop(index)

    # const handleSubmit = async (e: React.FormEvent) => {...};
    async def handleSubmit(e):
        e.preventDefault()
        setIsSubmitting(True)
        
        # await new Promise(resolve => setTimeout(resolve, 2000));
        await asyncio.sleep(2)
        
        setIsSubmitting(False)
        print('Livestock posted successfully! Your auction will go live within 24 hours after verification.') # Alert mock
        if onBack: onBack()

    categories = [
        {'value': 'cattle', 'label': '🐄 Cattle', 'icon': '🐄'},
        {'value': 'goats', 'label': '🐐 Goats', 'icon': '🐐'},
        {'value': 'sheep', 'label': '🐑 Sheep', 'icon': '🐑'},
        {'value': 'pigs', 'label': '🐷 Pigs', 'icon': '🐷'},
        {'value': 'chickens', 'label': '🐔 Chickens', 'icon': '🐔'},
        {'value': 'other', 'label': '🦌 Other', 'icon': '🦌'}
    ]

    auctionDurations = [
        {'value': '1', 'label': '1 day'},
        {'value': '3', 'label': '3 days'},
        {'value': '7', 'label': '1 week'},
        {'value': '14', 'label': '2 weeks'}
    ]

    locations = [
        'Harare', 'Bulawayo', 'Chitungwiza', 'Mutare', 'Gweru', 
        'Kwekwe', 'Kadoma', 'Masvingo', 'Chinhoyi', 'Marondera'
    ]

    return jsx('div', {'className': "min-h-screen bg-background"},
        # Header
        jsx('div', {'className': "sticky top-0 z-10 bg-background/95 backdrop-blur-sm border-b"},
            jsx('div', {'className': "flex items-center justify-between p-4"},
                jsx(Button, {'variant': "ghost", 'size': "sm", 'onClick': onBack},
                    jsx(ArrowLeft, {'className': "w-4 h-4 mr-2"}), "Back"
                ),
                jsx('h1', {'className': "font-semibold"}, "Post Livestock"),
                jsx('div', {'className': "w-16"})
            )
        ),

        jsx('form', {'onSubmit': handleSubmit, 'className': "p-4 space-y-6 pb-24"},
            # Photos
            jsx(Card, {},
                jsx(CardHeader, {},
                    jsx(CardTitle, {'className': "flex items-center gap-2"},
                        jsx(Camera, {'className': "w-5 h-5"}), "Photos"
                    )
                ),
                jsx(CardContent, {'className': "space-y-4"},
                    jsx('div', {'className': "grid grid-cols-2 gap-4"},
                        *[jsx('div', {'key': index, 'className': "relative"},
                            jsx('img', {
                                'src': image,
                                'alt': f"Upload {index + 1}",
                                'className': "w-full h-32 object-cover rounded-lg border-2 border-border"
                            }),
                            jsx(Button, {
                                'type': "button",
                                'variant': "destructive",
                                'size': "sm",
                                'className': "absolute top-2 right-2 p-1 h-auto",
                                'onClick': lambda i=index: removeImage(i)
                            }, jsx(X, {'className': "w-3 h-3"}))
                        ) for index, image in enumerate(images)],
                        
                        jsx(Button, {
                            'type': "button",
                            'variant': "outline",
                            'className': "h-32 border-2 border-dashed",
                            'onClick': handleImageUpload
                        },
                            jsx('div', {'className': "text-center"},
                                jsx(Upload, {'className': "w-6 h-6 mx-auto mb-2"}),
                                jsx('p', {'className': "text-sm"}, "Add Photo")
                            )
                        ) if len(images) < 4 else None
                    ),
                    jsx('p', {'className': "text-sm text-muted-foreground"},
                        "Add up to 4 high-quality photos. First photo will be the main image."
                    )
                )
            ),

            # Basic Information
            jsx(Card, {},
                jsx(CardHeader, {},
                    jsx(CardTitle, {}, "Basic Information")
                ),
                jsx(CardContent, {'className': "space-y-4"},
                    jsx('div', {'className': "space-y-2"},
                        jsx(Label, {'htmlFor': "title"}, "Title *"),
                        jsx(Input, {
                            'id': "title",
                            'placeholder': "e.g., Prime Brahman Bull",
                            'value': formData['title'],
                            'onChange': lambda e: handleInputChange('title', e['target']['value']),
                            'className': "h-12",
                            'required': True
                        })
                    ),
                    
                    jsx('div', {'className': "grid grid-cols-2 gap-4"},
                        jsx('div', {'className': "space-y-2"},
                            jsx(Label, {'htmlFor': "category"}, "Category *"),
                            jsx(Select, {
                                'value': formData['category'],
                                'onValueChange': lambda value: handleInputChange('category', value),
                                'required': True
                            },
                                jsx(SelectTrigger, {'className': "h-12"},
                                    jsx(SelectValue, {'placeholder': "Select category"})
                                ),
                                jsx(SelectContent, {},
                                    *[jsx(SelectItem, {'key': cat['value'], 'value': cat['value']}, cat['label']) for cat in categories]
                                )
                            )
                        ),
                        jsx('div', {'className': "space-y-2"},
                             jsx(Label, {'htmlFor': "breed"}, "Breed *"),
                             jsx(Input, {
                                 'id': "breed",
                                 'placeholder': "e.g., Brahman",
                                 'value': formData['breed'],
                                 'onChange': lambda e: handleInputChange('breed', e['target']['value']),
                                 'className': "h-12",
                                 'required': True
                             })
                        )
                    ),
                    
                    # Age & Weight ...
                    jsx('div', {'className': "grid grid-cols-2 gap-4"},
                        jsx('div', {'className': "space-y-2"},
                            jsx(Label, {'htmlFor': "age"}, "Age *"),
                            jsx(Input, {
                                'id': "age",
                                'placeholder': "e.g., 3 years",
                                'value': formData['age'],
                                'onChange': lambda e: handleInputChange('age', e['target']['value']),
                                'className': "h-12",
                                'required': True
                            })
                        ),
                        jsx('div', {'className': "space-y-2"},
                            jsx(Label, {'htmlFor': "weight"}, "Weight *"),
                            jsx(Input, {
                                'id': "weight",
                                'placeholder': "e.g., 850kg",
                                'value': formData['weight'],
                                'onChange': lambda e: handleInputChange('weight', e['target']['value']),
                                'className': "h-12",
                                'required': True
                            })
                        )
                    ),

                    jsx('div', {'className': "space-y-2"},
                        jsx(Label, {'htmlFor': "description"}, "Description"),
                        jsx(Textarea, {
                            'id': "description",
                            'placeholder': "Provide additional details about the livestock...",
                            'value': formData['description'],
                            'onChange': lambda e: handleInputChange('description', e['target']['value']),
                            'className': "min-h-20"
                        })
                    )
                )
            ),

            # Location & Health (Skipped detail code for brevity but Logic is preserved implicitly by following pattern)
            # Actually I must be meticulous.
            jsx(Card, {},
                jsx(CardHeader, {},
                    jsx(CardTitle, {'className': "flex items-center gap-2"},
                        jsx(MapPin, {'className': "w-5 h-5"}), "Location & Health"
                    )
                ),
                jsx(CardContent, {'className': "space-y-4"},
                    jsx('div', {'className': "grid grid-cols-2 gap-4"},
                        jsx('div', {'className': "space-y-2"},
                            jsx(Label, {'htmlFor': "location"}, "Location *"),
                            jsx(Select, {
                                'value': formData['location'],
                                'onValueChange': lambda value: handleInputChange('location', value),
                                'required': True
                            },
                                jsx(SelectTrigger, {'className': "h-12"},
                                    jsx(SelectValue, {'placeholder': "Select city"})
                                ),
                                jsx(SelectContent, {},
                                    *[jsx(SelectItem, {'key': loc, 'value': loc}, loc) for loc in locations]
                                )
                            )
                        ),
                        jsx('div', {'className': "space-y-2"},
                             jsx(Label, {'htmlFor': "health"}, "Health Status *"),
                             jsx(Select, {
                                 'value': formData['healthStatus'],
                                 'onValueChange': lambda value: handleInputChange('healthStatus', value),
                                 'required': True
                             },
                                 jsx(SelectTrigger, {'className': "h-12"},
                                     jsx(SelectValue, {'placeholder': "Select status"})
                                 ),
                                 jsx(SelectContent, {},
                                     jsx(SelectItem, {'value': "excellent"}, "Excellent"),
                                     jsx(SelectItem, {'value': "good"}, "Good"),
                                     jsx(SelectItem, {'value': "fair"}, "Fair")
                                 )
                             )
                        )
                    )
                )
            ),

            # Auction Details
            jsx(Card, {},
                jsx(CardHeader, {},
                    jsx(CardTitle, {'className': "flex items-center gap-2"},
                        jsx(DollarSign, {'className': "w-5 h-5"}), "Auction Details"
                    )
                ),
                jsx(CardContent, {'className': "space-y-4"},
                     jsx('div', {'className': "grid grid-cols-2 gap-4"},
                         jsx('div', {'className': "space-y-2"},
                             jsx(Label, {'htmlFor': "startingPrice"}, "Starting Price (USD) *"),
                             jsx('div', {'className': "relative"},
                                 jsx(DollarSign, {'className': "absolute left-3 top-3 h-4 w-4 text-muted-foreground"}),
                                 jsx(Input, {
                                     'id': "startingPrice",
                                     'type': "number",
                                     'placeholder': "800",
                                     'value': formData['startingPrice'],
                                     'onChange': lambda e: handleInputChange('startingPrice', e['target']['value']),
                                     'className': "pl-10 h-12",
                                     'min': "1",
                                     'required': True
                                 })
                             )
                         ),
                         jsx('div', {'className': "space-y-2"},
                             jsx(Label, {'htmlFor': "duration"}, "Auction Duration *"),
                             jsx(Select, {
                                 'value': formData['auctionDuration'],
                                 'onValueChange': lambda value: handleInputChange('auctionDuration', value),
                                 'required': True
                             },
                                 jsx(SelectTrigger, {'className': "h-12"},
                                     jsx(SelectValue, {'placeholder': "Select duration"})
                                 ),
                                 jsx(SelectContent, {},
                                     *[jsx(SelectItem, {'key': dur['value'], 'value': dur['value']},
                                         jsx('div', {'className': "flex items-center gap-2"},
                                             jsx(Clock, {'className': "w-4 h-4"}),
                                             dur['label']
                                         )
                                     ) for dur in auctionDurations]
                                 )
                             )
                         )
                     ),
                     jsx('div', {'className': "bg-muted/50 p-4 rounded-lg"},
                         jsx('h4', {'className': "font-medium mb-2"}, "Auction Terms"),
                         jsx('ul', {'className': "text-sm text-muted-foreground space-y-1"},
                             jsx('li', {}, "• 5% platform fee on successful sales"),
                             jsx('li', {}, "• Payment due within 48 hours of auction end"),
                             jsx('li', {}, "• Buyer inspection allowed before payment"),
                             jsx('li', {}, "• Free listing for verified farmers")
                         )
                     )
                )
            )
        ),

        # Fixed Bottom Submit
        jsx('div', {'className': "fixed bottom-0 left-0 right-0 bg-background border-t p-4"},
            jsx(Button, {
                'type': "submit",
                'className': "w-full h-12",
                'disabled': isSubmitting or not formData['title'] or not formData['category'] or not formData['breed'],
                'onClick': handleSubmit
            }, "Posting..." if isSubmitting else "Post Livestock"),
            jsx('p', {'className': "text-center text-xs text-muted-foreground mt-2"},
                "Your listing will be reviewed and published within 24 hours"
            )
        )
    )
