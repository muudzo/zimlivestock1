import { useState } from 'react';
import { Card, CardContent, CardHeader } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { 
  Clock, 
  Eye, 
  MessageCircle, 
  Edit3, 
  Trash2,
  TrendingUp,
  DollarSign,
  AlertCircle
} from 'lucide-react';

interface Listing {
  id: string;
  title: string;
  breed: string;
  currentBid: number;
  startingPrice: number;
  timeLeft: string;
  imageUrl: string;
  status: 'active' | 'ended' | 'pending' | 'sold';
  bidCount: number;
  views: number;
  category: string;
}

const mockListings: Listing[] = [
  {
    id: '1',
    title: 'Prime Brahman Bull',
    breed: 'Brahman',
    currentBid: 1200,
    startingPrice: 800,
    timeLeft: '2d 5h',
    imageUrl: 'https://images.unsplash.com/photo-1560114928-40f1f1eb26a0?w=400',
    status: 'active',
    bidCount: 8,
    views: 156,
    category: 'cattle'
  },
  {
    id: '2',
    title: 'Dairy Cow - High Milk Production',
    breed: 'Holstein',
    currentBid: 850,
    startingPrice: 600,
    timeLeft: 'Ended',
    imageUrl: 'https://images.unsplash.com/photo-1596003844243-b8ffd9b04095?w=400',
    status: 'sold',
    bidCount: 15,
    views: 234,
    category: 'cattle'
  },
  {
    id: '3',
    title: 'Young Boer Goat Buck',
    breed: 'Boer',
    currentBid: 0,
    startingPrice: 180,
    timeLeft: 'Pending Review',
    imageUrl: 'https://images.unsplash.com/photo-1583337130417-3346a1be7dee?w=400',
    status: 'pending',
    bidCount: 0,
    views: 12,
    category: 'goats'
  }
];

export function MyListings() {
  const [listings] = useState(mockListings);
  
  const formatCurrency = (amount: number) => {
    return `$${amount.toLocaleString()}`;
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800 border-green-200';
      case 'ended': return 'bg-gray-100 text-gray-800 border-gray-200';
      case 'pending': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'sold': return 'bg-blue-100 text-blue-800 border-blue-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'active': return 'Active';
      case 'ended': return 'Ended';
      case 'pending': return 'Under Review';
      case 'sold': return 'Sold';
      default: return status;
    }
  };

  const getCategoryIcon = (category: string) => {
    const icons = {
      cattle: '🐄',
      goats: '🐐', 
      sheep: '🐑',
      pigs: '🐷',
      chickens: '🐔'
    };
    return icons[category as keyof typeof icons] || '🐄';
  };

  const activeListings = listings.filter(l => l.status === 'active').length;
  const totalViews = listings.reduce((sum, l) => sum + l.views, 0);
  const totalBids = listings.reduce((sum, l) => sum + l.bidCount, 0);

  return (
    <div className="space-y-4 pb-20">
      {/* Header */}
      <div className="sticky top-0 z-10 bg-background/95 backdrop-blur-sm border-b p-4">
        <h1 className="text-xl font-bold">My Listings</h1>
        <p className="text-sm text-muted-foreground">Manage your livestock auctions</p>
      </div>

      {/* Stats */}
      <div className="px-4">
        <div className="grid grid-cols-3 gap-4">
          <div className="text-center p-3 bg-primary/10 rounded-lg">
            <p className="text-2xl font-bold text-primary">{activeListings}</p>
            <p className="text-xs text-muted-foreground">Active Auctions</p>
          </div>
          <div className="text-center p-3 bg-accent/20 rounded-lg">
            <p className="text-2xl font-bold text-accent-foreground">{totalViews}</p>
            <p className="text-xs text-muted-foreground">Total Views</p>
          </div>
          <div className="text-center p-3 bg-secondary/20 rounded-lg">
            <p className="text-2xl font-bold text-secondary-foreground">{totalBids}</p>
            <p className="text-xs text-muted-foreground">Total Bids</p>
          </div>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="px-4">
        <div className="flex gap-2 overflow-x-auto pb-2">
          <Badge variant="default" className="whitespace-nowrap">All</Badge>
          <Badge variant="outline" className="whitespace-nowrap">Active</Badge>
          <Badge variant="outline" className="whitespace-nowrap">Ended</Badge>
          <Badge variant="outline" className="whitespace-nowrap">Pending</Badge>
          <Badge variant="outline" className="whitespace-nowrap">Sold</Badge>
        </div>
      </div>

      {/* Listings */}
      <div className="px-4 space-y-4">
        {listings.map((listing) => (
          <Card key={listing.id} className="overflow-hidden">
            <div className="relative">
              <ImageWithFallback
                src={listing.imageUrl}
                alt={listing.title}
                className="w-full h-40 object-cover"
              />
              <div className="absolute top-3 left-3">
                <Badge className="bg-primary/90 text-primary-foreground">
                  {getCategoryIcon(listing.category)} {listing.breed}
                </Badge>
              </div>
              <div className="absolute top-3 right-3">
                <Badge className={`border ${getStatusColor(listing.status)}`}>
                  {getStatusText(listing.status)}
                </Badge>
              </div>
              {listing.status === 'active' && (
                <div className="absolute bottom-3 right-3">
                  <Badge variant="destructive" className="bg-red-600">
                    <Clock className="w-3 h-3 mr-1" />
                    {listing.timeLeft}
                  </Badge>
                </div>
              )}
            </div>
            
            <CardHeader className="pb-3">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <h3 className="font-semibold text-lg">{listing.title}</h3>
                  <div className="flex items-center gap-4 mt-2">
                    {listing.status === 'active' || listing.status === 'ended' || listing.status === 'sold' ? (
                      <div className="flex items-center gap-4">
                        <div>
                          <p className="text-xs text-muted-foreground">
                            {listing.currentBid > 0 ? 'Current Bid' : 'Starting Price'}
                          </p>
                          <p className="font-bold text-lg text-primary">
                            {listing.currentBid > 0 
                              ? formatCurrency(listing.currentBid)
                              : formatCurrency(listing.startingPrice)
                            }
                          </p>
                        </div>
                        {listing.currentBid > 0 && (
                          <div className="flex items-center gap-1 text-green-600">
                            <TrendingUp className="w-4 h-4" />
                            <span className="text-sm font-medium">
                              +{((listing.currentBid - listing.startingPrice) / listing.startingPrice * 100).toFixed(0)}%
                            </span>
                          </div>
                        )}
                      </div>
                    ) : (
                      <div className="flex items-center gap-2 text-yellow-600">
                        <AlertCircle className="w-4 h-4" />
                        <span className="text-sm">Under review - will be live within 24 hours</span>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </CardHeader>
            
            <CardContent className="pt-0 space-y-3">
              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-4 text-muted-foreground">
                  <div className="flex items-center gap-1">
                    <Eye className="w-4 h-4" />
                    {listing.views}
                  </div>
                  <div className="flex items-center gap-1">
                    <MessageCircle className="w-4 h-4" />
                    {listing.bidCount}
                  </div>
                </div>
                
                {listing.status === 'sold' && (
                  <div className="flex items-center gap-1 text-blue-600">
                    <DollarSign className="w-4 h-4" />
                    <span className="font-medium">
                      Sold for {formatCurrency(listing.currentBid)}
                    </span>
                  </div>
                )}
              </div>
              
              <div className="flex gap-2">
                {listing.status === 'active' && (
                  <>
                    <Button variant="outline" size="sm" className="flex-1">
                      <Edit3 className="w-4 h-4 mr-1" />
                      Edit
                    </Button>
                    <Button variant="outline" size="sm" className="flex-1">
                      <MessageCircle className="w-4 h-4 mr-1" />
                      Messages
                    </Button>
                  </>
                )}
                
                {listing.status === 'pending' && (
                  <Button variant="outline" size="sm" className="flex-1">
                    <Edit3 className="w-4 h-4 mr-1" />
                    Edit
                  </Button>
                )}
                
                {(listing.status === 'ended' || listing.status === 'sold') && (
                  <Button variant="outline" size="sm" className="flex-1">
                    <MessageCircle className="w-4 h-4 mr-1" />
                    View Messages
                  </Button>
                )}
                
                <Button variant="ghost" size="sm" className="text-destructive hover:text-destructive p-2">
                  <Trash2 className="w-4 h-4" />
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {listings.length === 0 && (
        <div className="text-center py-12">
          <div className="w-24 h-24 mx-auto mb-4 bg-muted rounded-full flex items-center justify-center">
            <List className="w-12 h-12 text-muted-foreground" />
          </div>
          <h3 className="font-semibold mb-2">No listings yet</h3>
          <p className="text-muted-foreground mb-4">Start by posting your first livestock for auction</p>
          <Button>Post Livestock</Button>
        </div>
      )}
    </div>
  );
}