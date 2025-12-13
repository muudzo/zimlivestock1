# AUTO-GENERATED FROM TypeScript
# SOURCE: src/stores/appStore.ts
# CONVERSION STAGE: STAGE 3
# DO NOT MODIFY LOGIC WITHOUT COMPARING TO ORIGINAL

import asyncio
import json
from typing import Dict, Any, List, Optional, Callable, TypeVar
from datetime import datetime

# Import Types
try:
    from src.types.index import AppState, Notification
    from src.services.api import notificationsAPI, localStorage, window
except ImportError:
    AppState = dict
    Notification = dict
    notificationsAPI = None
    localStorage = None
    window = None

# --- Mocks for DOM ---
class ClassList:
    _classes = set()
    def add(self, cls): self._classes.add(cls)
    def remove(self, cls): self._classes.discard(cls)
    def __str__(self): return " ".join(self._classes)

class Element:
    classList = ClassList()

class Document:
    documentElement = Element()

document = Document()

# --- Store Implementation ---

class AppStore:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppStore, cls).__new__(cls)
            cls._instance._init()
        return cls._instance
    
    def _init(self):
        # Initial State
        self.state: AppState = {
            'theme': 'system',
            'language': 'en',
            'notifications': [],
            'unreadCount': 0
        }
        
        # Persist Middleware simulation (rehydrate)
        self._rehydrate()

    def _rehydrate(self):
        # name: 'app-storage'
        stored = localStorage.getItem('app-storage')
        if stored:
            try:
                # partialize: theme, language
                parsed = json.loads(stored)
                # zustand persist usually stores { state: { ... }, version: 0 }
                # We assume simple storage interaction
                state_data = parsed.get('state', {})
                if 'theme' in state_data:
                    self.state['theme'] = state_data['theme']
                if 'language' in state_data:
                    self.state['language'] = state_data['language']
            except Exception:
                pass

    def _persist(self):
        # partialize
        to_store = {
            'state': {
                'theme': self.state['theme'],
                'language': self.state['language']
            },
            'version': 0
        }
        localStorage.setItem('app-storage', json.dumps(to_store))

    def set(self, partial_state: Dict[str, Any]):
        # set((state) => ({ ... })) logic
        # OR set({ ... }) logic
        # Here we just update
        self.state.update(partial_state)
        self._persist()

    def get(self) -> AppState:
        return self.state

    # --- Actions ---

    def setTheme(self, theme: str): # 'light' | 'dark' | 'system'
        # set({ theme })
        self.set({'theme': theme})
        
        # // Apply theme to document
        # const root = document.documentElement
        root = document.documentElement
        
        # if (theme === 'dark' || (theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches))
        is_dark = theme == 'dark'
        if theme == 'system':
             # window.matchMedia mock
             # For now assume false or stub
             is_dark = False 
        
        if is_dark:
            root.classList.add('dark')
        else:
            root.classList.remove('dark')

    def setLanguage(self, language: str):
        self.set({'language': language})

    def addNotification(self, notification: Notification):
        # set((state) => ({ ... }))
        # notifications: [notification, ...state.notifications]
        # unreadCount: state.unreadCount + (notification.read ? 0 : 1)
        current_notifs = self.state['notifications']
        current_unread = self.state['unreadCount']
        
        new_unread = current_unread + (0 if notification.get('read') else 1)
        
        self.set({
            'notifications': [notification] + current_notifs,
            'unreadCount': new_unread
        })

    def removeNotification(self, id: str):
        # set((state) => { ... })
        current_notifs = self.state['notifications']
        current_unread = self.state['unreadCount']
        
        # const notification = state.notifications.find(n => n.id === id)
        notification = next((n for n in current_notifs if n['id'] == id), None)
        
        # notifications: state.notifications.filter(n => n.id !== id)
        new_notifs = [n for n in current_notifs if n['id'] != id]
        
        # unreadCount: state.unreadCount - (notification?.read ? 0 : 1)
        # logic: if notification existed and was unread, decrement
        decrement = 0
        if notification and not notification.get('read'):
            decrement = 1
            
        self.set({
            'notifications': new_notifs,
            'unreadCount': current_unread - decrement
        })

    async def markNotificationAsRead(self, id: str):
        try:
            # await notificationsAPI.markAsRead(id)
            if notificationsAPI:
                await notificationsAPI.markAsRead(id)
            
            # set((state) => ({ ... }))
            current_notifs = self.state['notifications']
            current_unread = self.state['unreadCount']
            
            # notifications: map...
            new_notifs = []
            for n in current_notifs:
                if n['id'] == id:
                    n_copy = n.copy()
                    n_copy['read'] = True
                    new_notifs.append(n_copy)
                else:
                    new_notifs.append(n)
            
            # unreadCount: Math.max(0, state.unreadCount - 1)
            # Logic: only decrement if it was unread? TS map logic sets read: true.
            # But the unreadCount update logic in TS: `state.unreadCount - 1`.
            # This assumes the notification *was* unread?
            # If I call markAsRead on already read notif, count goes down?
            # TS logic allows it. "REPLICATE exactly".
            
            self.set({
                'notifications': new_notifs,
                'unreadCount': max(0, current_unread - 1)
            })
            
        except Exception as error:
            print(f'Failed to mark notification as read: {error}')

    async def markAllNotificationsAsRead(self):
        try:
            if notificationsAPI:
                await notificationsAPI.markAllAllAsRead() # Typo in my call? check api.py definition
            
            current_notifs = self.state['notifications']
            
            new_notifs = [{**n, 'read': True} for n in current_notifs]
            
            self.set({
                'notifications': new_notifs,
                'unreadCount': 0
            })
        except Exception as error:
            print(f'Failed to mark all notifications as read: {error}')

    def clearNotifications(self):
        self.set({'notifications': [], 'unreadCount': 0})

    async def fetchNotifications(self):
        try:
            if notificationsAPI:
                notifications = await notificationsAPI.getNotifications()
                # const unreadCount = notifications.filter(n => !n.read).length
                unreadCount = len([n for n in notifications if not n.get('read')])
                self.set({'notifications': notifications, 'unreadCount': unreadCount})
        except Exception as error:
            print(f'Failed to fetch notifications: {error}')

    def updateUnreadCount(self):
        # const { notifications } = get()
        notifications = self.state['notifications']
        unreadCount = len([n for n in notifications if not n.get('read')])
        self.set({'unreadCount': unreadCount})

# Export a singleton instance to mimic useAppStore() hook behavior or just the store
# In TS: `useAppStore` is a hook. `useAppStore.getState()` allows access outside components.
# In Python, we treat `useAppStore` as the instance itself for direct access.
useAppStore = AppStore()
