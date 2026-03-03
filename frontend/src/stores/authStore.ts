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
    checkAuth: () => Promise<void>;
}

export const useAuthStore = create<AuthState>()(
    persist(
        (set, get) => ({
            user: null,
            token: null,
            isAuthenticated: false,
            isLoading: false,

            setLoading: (loading) => set({ isLoading: loading }),

            login: async (contact, password) => {
                set({ isLoading: true });
                try {
                    const data = await authAPI.login({ contact, password });
                    const token = data.access_token;
                    set({ token }); // Store token first so interceptor can use it

                    const user = await authAPI.me();
                    // make sure id is stored as string (frontend expects string)
                    const normalizedUser = {
                        ...user,
                        id: String(user.id),
                    };

                    set({
                        user: normalizedUser,
                        isAuthenticated: true,
                        isLoading: false
                    });
                } catch (error) {
                    set({ isLoading: false, token: null, isAuthenticated: false });
                    throw error;
                }
            },

            register: async (userData) => {
                set({ isLoading: true });
                try {
                    await authAPI.register({
                        ...userData,
                        password: userData.password // no more mock fallback
                    });

                    // Auto-login after registration
                    const loginContact = userData.email || userData.phone;
                    const loginPassword = userData.password;

                    const data = await authAPI.login({ contact: loginContact, password: loginPassword });
                    const token = data.access_token;
                    set({ token });

                    const user = await authAPI.me();
                    const normalizedUser = {
                        ...user,
                        id: String(user.id),
                    };

                    set({
                        user: normalizedUser,
                        isAuthenticated: true,
                        isLoading: false
                    });
                } catch (error) {
                    set({ isLoading: false });
                    throw error;
                }
            },

            checkAuth: async () => {
                const { token } = get();
                if (!token) return;

                set({ isLoading: true });
                try {
                    const user = await authAPI.me();
                    set({
                        user: { ...user, id: String(user.id) },
                        isAuthenticated: true,
                        isLoading: false
                    });
                } catch (error) {
                    set({ user: null, token: null, isAuthenticated: false, isLoading: false });
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
