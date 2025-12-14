# AUTO-GENERATED FROM TypeScript
# SOURCE: src/hooks/useAuth.ts
# CONVERSION STAGE: STAGE 3
# DO NOT MODIFY LOGIC WITHOUT COMPARING TO ORIGINAL

import asyncio
from typing import Dict, Any, Optional

try:
    from src.stores.authStore import useAuthStore
    from src.lib.utils import validateEmail, validatePhone
except ImportError:
    useAuthStore = None
    validateEmail = lambda x: True
    validatePhone = lambda x: True

class UseAuth:
    def __init__(self):
        # In a real hook, this comes from store state. 
        # Here we access the singleton store directly.
        self.store = useAuthStore
        
        # Auto-refresh logic (mimic useEffect)
        # self._effect_mount() # We don't auto-run effects in pure class init usually unless requested

    @property
    def user(self): return self.store.state['user']
    @property
    def token(self): return self.store.state['token']
    @property
    def isAuthenticated(self): return self.store.state['isAuthenticated']
    @property
    def isLoading(self): return self.store.state['isLoading']

    # Actions wrapped with validation logic
    
    async def login(self, email: str, password: str):
        if not validateEmail(email):
            raise Exception('Please enter a valid email address')
        if len(password) < 6:
            raise Exception('Password must be at least 6 characters long')
            
        await self.store.login(email, password)

    async def register(self, userData: Dict[str, str]):
        # Validation
        firstName = userData.get('firstName', '')
        lastName = userData.get('lastName', '')
        email = userData.get('email', '')
        phone = userData.get('phone', '')
        password = userData.get('password', '')
        confirmPassword = userData.get('confirmPassword', '')
        
        if not firstName.strip(): raise Exception('First name is required')
        if not lastName.strip(): raise Exception('Last name is required')
        if not validateEmail(email): raise Exception('Please enter a valid email address')
        if not validatePhone(phone): raise Exception('Please enter a valid phone number')
        if len(password) < 6: raise Exception('Password must be at least 6 characters long')
        if password != confirmPassword: raise Exception('Passwords do not match')
        
        # const { confirmPassword, ...registerData } = userData
        registerData = userData.copy()
        if 'confirmPassword' in registerData:
            del registerData['confirmPassword']
            
        await self.store.register(registerData)

    async def logout(self):
        await self.store.logout()
    
    async def refreshUser(self):
        await self.store.refreshUser()

    async def updateUser(self, userData: Dict[str, Any]):
        email = userData.get('email')
        phone = userData.get('phone')
        
        if email and not validateEmail(email):
            raise Exception('Please enter a valid email address')
        if phone and not validatePhone(phone):
            raise Exception('Please enter a valid phone number')
            
        await self.store.updateUser(userData)

    def setLoading(self, loading: bool):
        self.store.setLoading(loading)
        
    def clearError(self):
        self.store.clearError()

    # Effect simulation
    async def mount(self):
        if self.isAuthenticated and self.token:
            await self.refreshUser()

def useAuth():
    # Return a new instance to mimic hook call
    instance = UseAuth()
    # In React, effects run after render.
    # We can invoke mount() here if we want immediate check, or let caller do it.
    # Logic: "Auto-refresh user on mount".
    # I'll expose it, but maybe not await it implies async constraint.
    # I'll just return the object.
    return instance
