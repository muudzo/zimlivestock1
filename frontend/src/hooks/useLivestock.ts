import { create } from 'zustand';

interface LivestockItem {
    id: string;
    title: string;
    breed: string;
    category: string;
    startingPrice: number;
    currentBid: number;
    imageUrl: string;
    location: string;
}

interface LivestockState {
    items: LivestockItem[];
    isLoading: boolean;
    getItems: (category?: string) => Promise<void>;
}

const mockLivestock: LivestockItem[] = [
    { id: '1', title: 'Prime Brahman Bull', breed: 'Brahman', category: 'cattle', startingPrice: 1500, currentBid: 1650, imageUrl: 'https://images.unsplash.com/photo-1543955444-20224d98e778', location: 'Harare' },
    { id: '2', title: 'Boer Goat Buck', breed: 'Boer', category: 'goats', startingPrice: 150, currentBid: 180, imageUrl: 'https://images.unsplash.com/photo-1524024973431-2ad916746881', location: 'Bulawayo' },
];

export const useLivestock = () => {
    const items = mockLivestock;
    const isLoading = false;
    const getItems = async () => { };

    return { items, isLoading, getItems };
};
