import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { authAPI } from '@/services/api';

interface User {
    id: string;
    email: string;
    firstName: string;
    lastName: string;
    phone?: string;
}

interface AuthState {
    user: User | null;
    token: string | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    login: (contact: string, password: string) => Promise<void>;
    register: (userData: any) => Promise<void>;
    logout: () => Promise<void>;
    setLoading: (loading: boolean) => void;
}

export const useAuthStore = create<AuthState>()(
    persist(
        (set) => ({
            user: null,
            token: null,
            isAuthenticated: false,
            isLoading: false,

            setLoading: (loading) => set({ isLoading: loading }),

            login: async (contact, password) => {
                set({ isLoading: true });
                try {
                    const data = await authAPI.login({ contact, password });
                    // Our fake token is "fake-jwt-token-for-ID"
                    const userId = data.access_token.split('-').pop();
                    set({
                        user: { id: userId, email: contact, firstName: 'User', lastName: 'Name' },
                        token: data.access_token,
                        isAuthenticated: true,
                        isLoading: false
                    });
                } catch (error) {
                    set({ isLoading: false });
                    throw error;
                }
            },

            register: async (userData) => {
                set({ isLoading: true });
                try {
                    const user = await authAPI.register({
                        ...userData,
                        password: userData.password || 'password123' // fallback for mock
                    });
                    set({
                        user,
                        token: 'mock-token',
                        isAuthenticated: true,
                        isLoading: false
                    });
                } catch (error) {
                    set({ isLoading: false });
                    throw error;
                }
            },

            logout: async () => {
                set({ user: null, token: null, isAuthenticated: false });
            },
        }),
        {
            name: 'auth-storage',
        }
    )
);
