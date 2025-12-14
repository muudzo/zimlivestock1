# AUTO-GENERATED FROM TypeScript
# SOURCE: components/BottomNavigation.tsx
# CONVERSION STAGE: STAGE 3
# DO NOT MODIFY LOGIC WITHOUT COMPARING TO ORIGINAL

from src.lib.react import React, jsx

# UI Imports
try:
    from components.ui.button import Button
    from components.ui.badge import Badge
except ImportError:
    Button = lambda props, *c: jsx('Button', props, *c)
    Badge = lambda props, *c: jsx('Badge', props, *c)

# Icons
Home = lambda p: jsx('Home', p)
Plus = lambda p: jsx('Plus', p)
List = lambda p: jsx('List', p)
Bell = lambda p: jsx('Bell', p)
MessageCircle = lambda p: jsx('MessageCircle', p)
User = lambda p: jsx('User', p)

def BottomNavigation(props):
    currentTab = props.get('currentTab')
    onTabChange = props.get('onTabChange')
    notificationCount = props.get('notificationCount', 0)
    messageCount = props.get('messageCount', 0)
    
    tabs = [
        { 'id': 'home', 'label': 'Home', 'icon': Home, 'count': 0 },
        { 'id': 'post', 'label': 'Post', 'icon': Plus, 'count': 0 },
        { 'id': 'listings', 'label': 'My Listings', 'icon': List, 'count': 0 },
        { 'id': 'notifications', 'label': 'Alerts', 'icon': Bell, 'count': notificationCount },
        { 'id': 'messages', 'label': 'Messages', 'icon': MessageCircle, 'count': messageCount }
    ]

    return jsx('div', {'className': "fixed bottom-0 left-0 right-0 bg-background border-t"},
        jsx('div', {'className': "grid grid-cols-5"},
            *[jsx(
                Button,
                {
                    'key': tab['id'],
                    'variant': "ghost",
                    'className': f"""
                        h-16 flex flex-col gap-1 rounded-none relative 
                        {'text-primary bg-primary/10' if currentTab == tab['id'] else 'text-muted-foreground hover:text-foreground'}
                    """,
                    'onClick': lambda t=tab: onTabChange(t['id'])
                },
                jsx('div', {'className': "relative"},
                    jsx(tab['icon'], {'className': f"w-5 h-5 {'stroke-2' if currentTab == tab['id'] else 'stroke-1.5'}"}),
                    jsx(Badge, {
                        'variant': "destructive",
                        'className': "absolute -top-2 -right-2 w-5 h-5 text-xs p-0 flex items-center justify-center"
                    }, 
                        "99+" if tab['count'] > 99 else str(tab['count'])
                    ) if tab['count'] > 0 else None
                ),
                jsx('span', {'className': f"text-xs {'font-medium' if currentTab == tab['id'] else 'font-normal'}"},
                    tab['label']
                ),
                jsx('div', {'className': "absolute top-0 left-1/2 transform -translate-x-1/2 w-8 h-0.5 bg-primary rounded-full"}) if currentTab == tab['id'] else None
            ) for tab in tabs]
        )
    )
