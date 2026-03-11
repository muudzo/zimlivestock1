export interface LivestockItem {
    id: string;
    title: string;
    breed: string;
    age: string;
    weight: string;
    location: string;
    currentBid: number;
    startingPrice: number;
    timeLeft: string;
    imageUrl: string;
    seller: {
        id: string;
        name: string;
        avatar?: string;
        verified: boolean;
        rating: number;
        totalSales: number;
        location: string;
        joinedDate: Date;
    };
    bidCount: number;
    views: number;
    category: 'cattle' | 'goats' | 'sheep' | 'pigs' | 'chickens';
    description: string;
    healthStatus: 'verified' | 'pending' | 'rejected' | 'sold';
    createdAt: Date;
    updatedAt: Date;
    auctionEndDate: Date;
}

export interface User {
    id: string;
    name: string;
    email: string;
    avatar?: string;
    role: 'farmer' | 'buyer' | 'admin';
}
