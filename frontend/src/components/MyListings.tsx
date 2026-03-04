import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader } from './ui/card';
import { Button } from './ui/button';
import { PaynowButton } from './PaynowButton';
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
  AlertCircle,
  CreditCard,
  ShoppingBag,
  List as ListIcon
} from 'lucide-react';
import { livestockAPI, paymentAPI } from '@/services/api';
import { useAuthStore } from '@/stores/authStore';
import { toast } from 'sonner';

export function MyListings() {
  const { user } = useAuthStore();
  const [activeView, setActiveView] = useState<'selling' | 'buying'>('selling');
  const [listings, setListings] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      try {
        const response = await livestockAPI.getListings();
        // Since we don't have a specific 'my-listings' endpoint yet, 
        // we'll filter on the frontend for this MVP.
        const allItems = response.data;
        if (activeView === 'selling') {
          setListings(allItems.filter((item: any) => item.seller_id === Number(user?.id)));
        } else {
          // Buying/Won logic: Items where current user is the winning bidder 
          // and item status is 'ended' or 'pending-payment'
          // For now, let's mock the "won" items or just show items where user bid
          setListings(allItems.filter((item: any) =>
            item.healthStatus === 'sold' && item.winner_id === Number(user?.id)
          ));
        }
      } catch (error) {
        console.error('Failed to fetch listings:', error);
        toast.error('Failed to load your listings');
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [activeView, user?.id]);

  const handlePay = async (item: any) => {
    toast.info('Preparing payment...');

    // ask which method the user wants
    let method = window.prompt("Payment method? (web/ecocash/onemoney)", "web");
    if (!method) {
      toast.error('Payment cancelled');
      return;
    }
    method = method.toLowerCase();
    if (!['web', 'ecocash', 'onemoney'].includes(method)) {
      toast.error('Unsupported method');
      return;
    }

    let phone: string | undefined;
    if (method !== 'web') {
      phone = window.prompt('Enter phone number for mobile payment', user?.phone || '') || undefined;
      if (!phone) {
        toast.error('Phone number required for mobile payments');
        return;
      }
    }

    toast.info('Initiating payment...');
    try {
      const payload: any = {
        livestock_id: item.id,
        bid_id: 0, // placeholder; real logic should supply bid id
        payer_id: Number(user?.id),
        payment_method: method,
      };
      if (phone) payload.phone = phone;

      const response = await paymentAPI.initiate(payload);

      if (response.redirect_url) {
        window.location.href = response.redirect_url;
      } else if (response.instructions) {
        toast.success('Follow instructions sent to your phone');
      } else {
        toast.error('Payment initiation failed: no actionable result');
      }
    } catch (error: any) {
      console.error('Payment error:', error);
      toast.error(error.response?.data?.detail || 'Failed to initiate payment');
    }
  };

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

  return (
    <div className="space-y-4 pb-20">
      {/* Header */}
      <div className="sticky top-0 z-10 bg-background/95 backdrop-blur-sm border-b p-4">
        <h1 className="text-xl font-bold">My Marketplace</h1>
        <p className="text-sm text-muted-foreground">Manage your activities</p>
      </div>

      {/* Switcher */}
      <div className="px-4">
        <div className="flex bg-muted p-1 rounded-lg">
          <Button
            variant={activeView === 'selling' ? 'default' : 'ghost'}
            className="flex-1 text-sm h-9"
            onClick={() => setActiveView('selling')}
          >
            <ShoppingBag className="w-4 h-4 mr-2" />
            Selling
          </Button>
          <Button
            variant={activeView === 'buying' ? 'default' : 'ghost'}
            className="flex-1 text-sm h-9"
            onClick={() => setActiveView('buying')}
          >
            <DollarSign className="w-4 h-4 mr-2" />
            Won items
          </Button>
        </div>
      </div>

      {/* Listings */}
      <div className="px-4 space-y-4">
        {isLoading ? (
          <div className="text-center py-12">
            <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-muted-foreground text-sm">Loading your items...</p>
          </div>
        ) : listings.length > 0 ? (
          listings.map((listing) => (
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
                  <Badge className={`border ${getStatusColor(listing.healthStatus)}`}>
                    {getStatusText(listing.healthStatus)}
                  </Badge>
                </div>
              </div>

              <CardHeader className="pb-3">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="font-semibold text-lg">{listing.title}</h3>
                    <div className="flex items-center gap-4 mt-2">
                      <div>
                        <p className="text-xs text-muted-foreground">Price</p>
                        <p className="font-bold text-lg text-primary">
                          {formatCurrency(listing.currentBid || listing.startingPrice)}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </CardHeader>

              <CardContent className="pt-0 space-y-3">
                <div className="flex gap-2">
                  {activeView === 'selling' ? (
                    <>
                      <Button variant="outline" size="sm" className="flex-1">
                        <Edit3 className="w-4 h-4 mr-1" />
                        Edit
                      </Button>
                      <Button variant="ghost" size="sm" className="text-destructive hover:text-destructive p-2">
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </>
                  ) : (
                    <>
                      {listing.healthStatus === 'sold' && (
                        <PaynowButton
                          className="flex-1"
                          onClick={() => handlePay(listing)}
                        />
                      )}
                      <Button variant="outline" size="sm" className="flex-1">
                        <MessageCircle className="w-4 h-4 mr-1" />
                        Chat Seller
                      </Button>
                    </>
                  )}
                </div>
              </CardContent>
            </Card>
          ))
        ) : (
          <div className="text-center py-12">
            <div className="w-24 h-24 mx-auto mb-4 bg-muted rounded-full flex items-center justify-center">
              <ListIcon className="w-12 h-12 text-muted-foreground" />
            </div>
            <h3 className="font-semibold mb-2">
              {activeView === 'selling' ? 'No selling items' : 'No won auctions'}
            </h3>
            <p className="text-muted-foreground mb-4">
              {activeView === 'selling'
                ? 'Start by posting your first livestock for auction'
                : 'Browse the feed and place your first bid!'}
            </p>
            {activeView === 'selling' && <Button>Post Livestock</Button>}
          </div>
        )}
      </div>
    </div>
  );
}
