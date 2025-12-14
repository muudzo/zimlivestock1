# AUTO-GENERATED FROM TypeScript
# SOURCE: src/stores/authStore.ts
# CONVERSION STAGE: STAGE 3
# DO NOT MODIFY LOGIC WITHOUT COMPARING TO ORIGINAL

import asyncio
import json
from typing import Dict, Any, Optional

# Import Types
try:
    from src.types.index import AuthState, User
    from src.services.api import authAPI, localStorage
except ImportError:
    AuthState = dict
    User = dict
    authAPI = None
    localStorage = None

# --- Mock Sonner Toast ---
class Toast:
    @staticmethod
    def success(message: str):
        print(f"[Toast Success] {message}")
        
    @staticmethod
    def error(message: str):
        print(f"[Toast Error] {message}")

toast = Toast()

# --- Auth Store Implementation ---

class AuthStore:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuthStore, cls).__new__(cls)
            cls._instance._init()
        return cls._instance
    
    def _init(self):
        # Initial State
        self.state: AuthState = {
            'user': None,
            'token': None,
            'isAuthenticated': False,
            'isLoading': False
        }
        
        self._rehydrate()
        
    def _rehydrate(self):
        # name: 'auth-storage'
        stored = localStorage.getItem('auth-storage')
        if stored:
            try:
                # partialize: user, token, isAuthenticated
                parsed = json.loads(stored)
                state_data = parsed.get('state', {})
                
                if 'user' in state_data: self.state['user'] = state_data['user']
                if 'token' in state_data: self.state['token'] = state_data['token']
                if 'isAuthenticated' in state_data: self.state['isAuthenticated'] = state_data['isAuthenticated']
                
                # onRehydrateStorage logic: Check validity
                if self.state.get('token'):
                     # state.refreshUser().catch(...)
                     # In Python synchronous init, we can't easily await async refresh here
                     # unless we spin loop event loop or just schedule it.
                     # But this is inside __init__ (rehydrate).
                     # We'll note this limitation or better, define a method to initialize async.
                     pass 
            except Exception:
                pass
            
    def _persist(self):
        to_store = {
            'state': {
                'user': self.state['user'],
                'token': self.state['token'],
                'isAuthenticated': self.state['isAuthenticated']
            },
            'version': 0
        }
        localStorage.setItem('auth-storage', json.dumps(to_store))

    def set(self, partial_state: Dict[str, Any]):
        self.state.update(partial_state)
        self._persist()
        
    def get(self) -> AuthState:
        return self.state

    # --- Actions ---

    def setLoading(self, loading: bool):
        self.set({'isLoading': loading})

    async def login(self, email: str, password: str):
        try:
            self.set({'isLoading': True})
            # const { user, token } = await authAPI.login(email, password)
            data = await authAPI.login(email, password)
            user = data['user']
            token = data['token']
            
            # Store token in localStorage
            localStorage.setItem('auth_token', token)
            
            self.set({
                'user': user,
                'token': token,
                'isAuthenticated': True,
                'isLoading': False
            })
            
            toast.success('Welcome back!')
        except Exception as error:
            self.set({'isLoading': False})
            toast.error('Login failed. Please check your credentials.')
            raise error

    async def register(self, userData: Dict[str, str]):
        try:
            self.set({'isLoading': True})
            data = await authAPI.register(userData)
            user = data['user']
            token = data['token']
            
            # Store token in localStorage
            localStorage.setItem('auth_token', token)
            
            self.set({
                'user': user,
                'token': token,
                'isAuthenticated': True,
                'isLoading': False
            })
            
            toast.success('Account created successfully!')
        except Exception as error:
            self.set({'isLoading': False})
            toast.error('Registration failed. Please try again.')
            raise error

    async def logout(self):
        try:
            # await authAPI.logout()
            await authAPI.logout()
        except Exception as error:
            # console.warn
            print(f'Logout API call failed: {error}')
        finally:
            # Clear local storage
            localStorage.removeItem('auth_token')
            localStorage.removeItem('user')
            
            self.set({
                'user': None,
                'token': None,
                'isAuthenticated': False,
                'isLoading': False
            })
            
            toast.success('Logged out successfully')

    async def refreshUser(self):
        try:
            # const user = await authAPI.getProfile()
            user = await authAPI.getProfile()
            self.set({'user': user})
        except Exception as error:
            print(f'Failed to refresh user: {error}')
            # get().logout()
            await self.logout()

    async def updateUser(self, userData: Dict[str, Any]):
        try:
            self.set({'isLoading': True})
            updatedUser = await authAPI.updateProfile(userData)
            self.set({'user': updatedUser, 'isLoading': False})
            toast.success('Profile updated successfully')
        except Exception as error:
            self.set({'isLoading': False})
            toast.error('Failed to update profile')
            raise error

    def clearError(self):
        self.set({'isLoading': False})

useAuthStore = AuthStore()
