import { create } from 'zustand';
import { persist } from 'zustand/middleware';

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
                    // Mock login for now or call your API
                    // const response = await fetch('/api/auth/login', { ... });
                    // const data = await response.json();
                    const mockUser = { id: '1', email: 'user@example.com', firstName: 'John', lastName: 'Doe' };
                    set({
                        user: mockUser,
                        token: 'mock-token',
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
                    const mockUser = { id: '1', ...userData };
                    set({
                        user: mockUser,
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
