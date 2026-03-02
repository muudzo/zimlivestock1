import { LivestockItem } from "@/types";

// Mock API for livestock
export const livestockAPI = {
    getListings: async (params?: { category?: string; limit?: number }) => {
        // In a real app, this would fetch from the backend
        // For now, we return a promise that resolves after a short delay
        await new Promise((resolve) => setTimeout(resolve, 500));

        // We expect the caller to handle the data structure
        // HomeFeed structure suggests: listings.data
        return {
            data: [] as LivestockItem[],
        };
    },
};
