import { useState, useMemo, useCallback } from 'react';
import { useQuery } from 'react-query';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { ImageWithFallback } from '@/components/figma/ImageWithFallback';
import { Clock, MapPin, Weight, Calendar, Eye, Heart, MessageCircle, Loader2 } from 'lucide-react';
import { formatCurrency, getCategoryIcon } from '@/lib/utils';
import { livestockAPI } from '@/services/api';
import { LivestockItem } from '@/types';

// Remove duplicate interface - using the one from types

const mockListings: LivestockItem[] = [
  {
    id: '1',
    title: 'Prime Brahman Bull',
    breed: 'Brahman',
    age: '3 years',
    weight: '850kg',
    location: 'Harare',
    currentBid: 1200,
    startingPrice: 800,
    timeLeft: '2d 5h',
    imageUrl: 'https://images.unsplash.com/photo-1560114928-40f1f1eb26a0?w=400&fit=crop&crop=center',
    seller: {
      id: '1',
      name: 'T. Chikwanha',
      verified: true,
      rating: 4.8,
      totalSales: 45,
      location: 'Harare',
      joinedDate: new Date('2022-01-15'),
    },
    bidCount: 8,
    views: 156,
    category: 'cattle',
    description: 'Excellent breeding bull with proven genetics',
    healthStatus: 'verified',
    createdAt: new Date('2024-01-15'),
    updatedAt: new Date('2024-01-15'),
    auctionEndDate: new Date('2024-01-20'),
  },
  {
    id: '2',
    title: 'Productive Dairy Cow',
    breed: 'Holstein Friesian',
    age: '4 years',
    weight: '650kg',
    location: 'Bulawayo',
    currentBid: 950,
    startingPrice: 700,
    timeLeft: '1d 12h',
    imageUrl: 'https://images.unsplash.com/photo-1596003844243-b8ffd9b04095?w=400&fit=crop&crop=center',
    seller: {
      id: '2',
      name: 'M. Ncube',
      verified: true,
      rating: 4.9,
      totalSales: 67,
      location: 'Bulawayo',
      joinedDate: new Date('2021-06-20'),
    },
    bidCount: 12,
    views: 203,
    category: 'cattle',
    description: 'High-yielding dairy cow with excellent health records',
    healthStatus: 'verified',
    createdAt: new Date('2024-01-14'),
    updatedAt: new Date('2024-01-14'),
    auctionEndDate: new Date('2024-01-19'),
  },
  {
    id: '3',
    title: 'Boer Goat Buck',
    breed: 'Boer',
    age: '2 years',
    weight: '85kg',
    location: 'Gweru',
    currentBid: 285,
    startingPrice: 180,
    timeLeft: '3d 8h',
    imageUrl: 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=400&fit=crop&crop=center',
    seller: {
      id: '3',
      name: 'S. Mpofu',
      verified: false,
      rating: 4.2,
      totalSales: 12,
      location: 'Gweru',
      joinedDate: new Date('2023-03-10'),
    },
    bidCount: 5,
    views: 89,
    category: 'goats',
    description: 'Quality Boer goat buck for breeding',
    healthStatus: 'pending',
    createdAt: new Date('2024-01-13'),
    updatedAt: new Date('2024-01-13'),
    auctionEndDate: new Date('2024-01-22'),
  },
  {
    id: '4',
    title: 'Free Range Chickens (10)',
    breed: 'Rhode Island Red',
    age: '8 months',
    weight: '2kg each',
    location: 'Mutare',
    currentBid: 120,
    startingPrice: 80,
    timeLeft: '4h 30m',
    imageUrl: 'https://images.unsplash.com/photo-1548550023-2bdb3c5beed7?w=400&fit=crop&crop=center',
    seller: {
      id: '4',
      name: 'A. Mugabe',
      verified: true,
      rating: 4.7,
      totalSales: 89,
      location: 'Mutare',
      joinedDate: new Date('2020-11-05'),
    },
    bidCount: 15,
    views: 267,
    category: 'chickens',
    description: 'Healthy free-range chickens ready for laying',
    healthStatus: 'verified',
    createdAt: new Date('2024-01-12'),
    updatedAt: new Date('2024-01-12'),
    auctionEndDate: new Date('2024-01-16'),
  },
  {
    id: '5',
    title: 'Dorper Sheep Ram',
    breed: 'Dorper',
    age: '2.5 years',
    weight: '95kg',
    location: 'Masvingo',
    currentBid: 420,
    startingPrice: 300,
    timeLeft: '1d 8h',
    imageUrl: 'https://images.unsplash.com/photo-1500595046743-cd271d694e30?w=400&fit=crop&crop=center',
    seller: {
      id: '5',
      name: 'K. Moyo',
      verified: true,
      rating: 4.6,
      totalSales: 34,
      location: 'Masvingo',
      joinedDate: new Date('2021-09-12'),
    },
    bidCount: 7,
    views: 134,
    category: 'sheep',
    description: 'Premium Dorper ram with excellent meat quality',
    healthStatus: 'verified',
    createdAt: new Date('2024-01-11'),
    updatedAt: new Date('2024-01-11'),
    auctionEndDate: new Date('2024-01-18'),
  },
  {
    id: '6',
    title: 'Large White Pigs (2)',
    breed: 'Large White',
    age: '1 year',
    weight: '120kg each',
    location: 'Chinhoyi',
    currentBid: 380,
    startingPrice: 250,
    timeLeft: '5d 2h',
    imageUrl: 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=400&fit=crop&crop=center',
    seller: {
      id: '6',
      name: 'P. Chitepo',
      verified: true,
      rating: 4.5,
      totalSales: 23,
      location: 'Chinhoyi',
      joinedDate: new Date('2022-04-18'),
    },
    bidCount: 9,
    views: 178,
    category: 'pigs',
    description: 'Healthy Large White pigs ready for breeding',
    healthStatus: 'verified',
    createdAt: new Date('2024-01-10'),
    updatedAt: new Date('2024-01-10'),
    auctionEndDate: new Date('2024-01-25'),
  }
];

interface HomeFeedProps {
  onItemClick: (item: LivestockItem) => void;
}

export function HomeFeed({ onItemClick }: HomeFeedProps) {
  const [likedItems, setLikedItems] = useState<Set<string>>(new Set());
  const [selectedCategory, setSelectedCategory] = useState<string>('all');

  const toggleLike = (itemId: string, e: React.MouseEvent<HTMLButtonElement>) => {
    e.stopPropagation();
    setLikedItems(prev => {
      const newLiked = new Set(prev);
      if (newLiked.has(itemId)) {
        newLiked.delete(itemId);
      } else {
        newLiked.add(itemId);
      }
      return newLiked;
    });
  };

  const filteredListings = selectedCategory === 'all' 
    ? mockListings 
    : mockListings.filter(item => item.category === selectedCategory);

  const categories = [
    { id: 'all', label: 'All', icon: '🐄' },
    { id: 'cattle', label: 'Cattle', icon: '🐄' },
    { id: 'goats', label: 'Goats', icon: '🐐' },
    { id: 'sheep', label: 'Sheep', icon: '🐑' },
    { id: 'pigs', label: 'Pigs', icon: '🐷' },
    { id: 'chickens', label: 'Chickens', icon: '🐔' },
  ];

  return (
    <div className="space-y-4 pb-20">
      {/* Header */}
      <div className="sticky top-0 z-10 bg-background/95 backdrop-blur-sm border-b p-4">
        <h1 className="text-xl font-bold">Livestock Marketplace</h1>
        <p className="text-sm text-muted-foreground">Latest auctions from farmers across Zimbabwe</p>
      </div>

      {/* Filters */}
      <div className="px-4">
        <div className="flex gap-2 overflow-x-auto pb-2">
          {categories.map((category) => (
            <Badge
              key={category.id}
              variant={selectedCategory === category.id ? "default" : "outline"}
              className="whitespace-nowrap cursor-pointer"
              onClick={() => setSelectedCategory(category.id)}
            >
              {category.icon} {category.label}
            </Badge>
          ))}
        </div>
      </div>

      {/* Listings */}
      <div className="px-4 space-y-4">
        {filteredListings.map((item) => (
          <Card 
            key={item.id} 
            className="overflow-hidden cursor-pointer hover:shadow-lg transition-shadow card-interactive"
            onClick={() => onItemClick(item)}
          >
            <div className="relative">
              <ImageWithFallback
                src={item.imageUrl}
                alt={item.title}
                className="w-full h-48 object-cover"
              />
              <div className="absolute top-3 left-3">
                <Badge className="bg-primary/90 text-primary-foreground">
                  {getCategoryIcon(item.category)} {item.breed}
                </Badge>
              </div>
              <div className="absolute top-3 right-3">
                <Button
                  variant="ghost"
                  size="sm"
                  className="bg-white/90 hover:bg-white p-2 h-auto"
                  onClick={(e: React.MouseEvent<HTMLButtonElement>) => toggleLike(item.id, e)}
                >
                  <Heart 
                    className={`w-4 h-4 ${
                      likedItems.has(item.id) 
                        ? 'fill-red-500 text-red-500' 
                        : 'text-gray-600'
                    }`} 
                  />
                </Button>
              </div>
              <div className="absolute bottom-3 right-3">
                <Badge variant="destructive" className="bg-red-600">
                  <Clock className="w-3 h-3 mr-1" />
                  {item.timeLeft}
                </Badge>
              </div>
            </div>
            
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <h3 className="font-semibold text-lg">{item.title}</h3>
                <div className="text-right">
                  <p className="text-xs text-muted-foreground">Current Bid</p>
                  <p className="font-bold text-lg text-primary">{formatCurrency(item.currentBid)}</p>
                </div>
              </div>
              
              <div className="flex items-center gap-4 text-sm text-muted-foreground">
                <div className="flex items-center gap-1">
                  <Calendar className="w-4 h-4" />
                  {item.age}
                </div>
                <div className="flex items-center gap-1">
                  <Weight className="w-4 h-4" />
                  {item.weight}
                </div>
                <div className="flex items-center gap-1">
                  <MapPin className="w-4 h-4" />
                  {item.location}
                </div>
              </div>
            </CardHeader>
            
            <CardContent className="pt-0">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Avatar className="w-8 h-8">
                    <AvatarImage src={item.seller.avatar} />
                    <AvatarFallback>{item.seller.name.charAt(0)}</AvatarFallback>
                  </Avatar>
                  <div>
                    <p className="text-sm font-medium">{item.seller.name}</p>
                    {item.seller.verified && (
                      <p className="text-xs text-primary">✓ Verified</p>
                    )}
                  </div>
                </div>
                
                <div className="flex items-center gap-4 text-xs text-muted-foreground">
                  <div className="flex items-center gap-1">
                    <MessageCircle className="w-3 h-3" />
                    {item.bidCount}
                  </div>
                  <div className="flex items-center gap-1">
                    <Eye className="w-3 h-3" />
                    {item.views}
                  </div>
                </div>
              </div>
              
              <div className="mt-3 flex gap-2">
                <Button variant="outline" size="sm" className="flex-1">
                  <MessageCircle className="w-4 h-4 mr-1" />
                  Message
                </Button>
                <Button size="sm" className="flex-1">
                  Place Bid
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}