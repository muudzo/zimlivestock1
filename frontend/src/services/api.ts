import { LivestockItem } from "@/types";
import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

let internalToken: string | null = null;

export const setAuthToken = (token: string | null) => {
    internalToken = token;
};

const api = axios.create({
    baseURL: API_BASE_URL,
});

// Add a request interceptor to attach the token
api.interceptors.request.use(
    (config) => {
        // Prefer in-memory token, then fall back to localStorage
        let token = internalToken;

        if (!token) {
            const authData = localStorage.getItem('auth-storage');
            if (authData) {
                try {
                    const { state } = JSON.parse(authData);
                    token = state.token;
                } catch (error) {
                    console.error('Error parsing auth-storage', error);
                }
            }
        }

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export const livestockAPI = {
    getListings: async (params?: { category?: string; limit?: number }) => {
        const response = await api.get("/livestock", { params });
        return response;
    },
    getListing: async (id: number) => {
        const response = await api.get(`/livestock/${id}`);
        return response;
    },
    getBidsForItem: async (id: number) => {
        const response = await api.get(`/bids/livestock/${id}`);
        return response;
    },
    createListing: async (data: any) => {
        const response = await api.post("/livestock", data);
        return response.data;
    },
    placeBid: async (data: { livestock_id: number; amount: number }) => {
        const response = await api.post("/bids", data);
        return response.data;
    },
};

export const authAPI = {
    login: async (credentials: any) => {
        const response = await api.post("/auth/login", credentials);
        return response.data;
    },
    register: async (userData: any) => {
        const response = await api.post("/auth/register", userData);
        return response.data;
    },
    me: async () => {
        const response = await api.get("/auth/me");
        return response.data;
    },
};

export const paymentAPI = {
    initiate: async (data: any) => {
        const response = await api.post("/payments/initiate", data);
        return response.data;
    },
    getStatus: async (reference: string) => {
        const response = await api.get(`/payments/status/${reference}`);
        return response.data;
    },
    getUserPayments: async () => {
        const response = await api.get("/payments/history");
        return response.data;
    },
};
