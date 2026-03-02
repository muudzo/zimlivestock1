import { LivestockItem } from "@/types";
import axios from "axios";

const API_BASE_URL = "http://localhost:8000";

const api = axios.create({
    baseURL: API_BASE_URL,
});

export const livestockAPI = {
    getListings: async (params?: { category?: string; limit?: number }) => {
        const response = await api.get("/livestock", { params });
        return response;
    },
    getListing: async (id: number) => {
        const response = await api.get(`/livestock/${id}`);
        return response;
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
};
