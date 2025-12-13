import { useState, useEffect } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { 
  ArrowLeft, 
  Clock, 
  MapPin, 
  Weight, 
  Calendar, 
  TrendingUp, 
  Heart, 
  Share,
  MessageCircle,
  Shield,
  Award
} from 'lucide-react';

interface Bid {
  id: string;
  bidder: string;
  amount: number;
  timestamp: Date;
  isWinning: boolean;
}

interface BiddingScreenProps {
  onBack: () => void;
  livestockItem: any;
}

export function BiddingScreen({ onBack, livestockItem }: BiddingScreenProps) {
  const [bidAmount, setBidAmount] = useState('');
  const [timeLeft, setTimeLeft] = useState('2d 5h 23m');
  const [isLiked, setIsLiked] = useState(false);
  const [bidHistory] = useState<Bid[]>([
    {
      id: '1',
      bidder: 'J. Manyika',
      amount: 1200,
      timestamp: new Date(Date.now() - 300000),
      isWinning: true
    },
    {
      id: '2',
      bidder: 'R. Chigwamba',
      amount: 1150,
      timestamp: new Date(Date.now() - 900000),
      isWinning: false
    },
    {
      id: '3',
      bidder: 'P. Mukamuri',
      amount: 1100,
      timestamp: new Date(Date.now() - 1800000),
      isWinning: false
    },
    {
      id: '4',
      bidder: 'T. Nhongo',
      amount: 1000,
      timestamp: new Date(Date.now() - 3600000),
      isWinning: false
    }
  ]);

  const currentHighestBid = bidHistory[0]?.amount || livestockItem.startingPrice;
  const minimumBid = currentHighestBid + 50;

  useEffect(() => {
    setBidAmount(minimumBid.toString());
  }, [minimumBid]);

  const formatCurrency = (amount: number) => {
    return `$${amount.toLocaleString()}`;
  };

  const formatTimeAgo = (date: Date) => {
    const now = new Date();
    const diffInMinutes = Math.floor((now.getTime() - date.getTime()) / (1000 * 60));
    
    if (diffInMinutes < 1) return 'Just now';
    if (diffInMinutes < 60) return `${diffInMinutes}m ago`;
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`;
    return `${Math.floor(diffInMinutes / 1440)}d ago`;
  };

  const handlePlaceBid = () => {
    const amount = parseInt(bidAmount);
    if (amount >= minimumBid) {
      // Simulate bid placement
      alert(`Bid of ${formatCurrency(amount)} placed successfully!`);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="sticky top-0 z-10 bg-background/95 backdrop-blur-sm border-b">
        <div className="flex items-center justify-between p-4">
          <Button variant="ghost" size="sm" onClick={onBack}>
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back
          </Button>
          <div className="flex gap-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsLiked(!isLiked)}
              className="p-2"
            >
              <Heart className={`w-5 h-5 ${isLiked ? 'fill-red-500 text-red-500' : 'text-gray-600'}`} />
            </Button>
            <Button variant="ghost" size="sm" className="p-2">
              <Share className="w-5 h-5" />
            </Button>
          </div>
        </div>
      </div>

      <div className="pb-32">
        {/* Image */}
        <div className="relative">
          <ImageWithFallback
            src={livestockItem.imageUrl}
            alt={livestockItem.title}
            className="w-full h-64 object-cover"
          />
          <div className="absolute bottom-4 left-4">
            <Badge className="bg-primary/90 text-primary-foreground text-base px-3 py-1">
              🐄 {livestockItem.breed}
            </Badge>
          </div>
          <div className="absolute bottom-4 right-4">
            <Badge variant="destructive" className="bg-red-600 text-base px-3 py-1">
              <Clock className="w-4 h-4 mr-1" />
              {timeLeft}
            </Badge>
          </div>
        </div>

        {/* Content */}
        <div className="p-4 space-y-6">
          {/* Title and Current Bid */}
          <div>
            <h1 className="text-2xl font-bold mb-2">{livestockItem.title}</h1>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Current Highest Bid</p>
                <p className="text-3xl font-bold text-primary">{formatCurrency(currentHighestBid)}</p>
                <p className="text-sm text-muted-foreground">
                  Starting at {formatCurrency(livestockItem.startingPrice)}
                </p>
              </div>
              <div className="text-right">
                <div className="flex items-center gap-1 text-green-600">
                  <TrendingUp className="w-4 h-4" />
                  <span className="text-sm font-medium">
                    +{((currentHighestBid - livestockItem.startingPrice) / livestockItem.startingPrice * 100).toFixed(0)}%
                  </span>
                </div>
                <p className="text-xs text-muted-foreground">{bidHistory.length} bids</p>
              </div>
            </div>
          </div>

          {/* Details */}
          <div className="grid grid-cols-2 gap-4">
            <div className="flex items-center gap-2">
              <Calendar className="w-4 h-4 text-muted-foreground" />
              <div>
                <p className="text-xs text-muted-foreground">Age</p>
                <p className="font-medium">{livestockItem.age}</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Weight className="w-4 h-4 text-muted-foreground" />
              <div>
                <p className="text-xs text-muted-foreground">Weight</p>
                <p className="font-medium">{livestockItem.weight}</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <MapPin className="w-4 h-4 text-muted-foreground" />
              <div>
                <p className="text-xs text-muted-foreground">Location</p>
                <p className="font-medium">{livestockItem.location}</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Shield className="w-4 h-4 text-muted-foreground" />
              <div>
                <p className="text-xs text-muted-foreground">Health</p>
                <p className="font-medium text-green-600">Verified</p>
              </div>
            </div>
          </div>

          {/* Seller Info */}
          <Card>
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Avatar className="w-12 h-12">
                    <AvatarImage src={livestockItem.seller.avatar} />
                    <AvatarFallback>{livestockItem.seller.name.charAt(0)}</AvatarFallback>
                  </Avatar>
                  <div>
                    <p className="font-semibold">{livestockItem.seller.name}</p>
                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                      {livestockItem.seller.verified && (
                        <>
                          <Shield className="w-3 h-3 text-green-600" />
                          <span className="text-green-600">Verified Farmer</span>
                        </>
                      )}
                      <Award className="w-3 h-3" />
                      <span>4.8 rating</span>
                    </div>
                  </div>
                </div>
                <Button variant="outline" size="sm">
                  <MessageCircle className="w-4 h-4 mr-1" />
                  Chat
                </Button>
              </div>
            </CardHeader>
          </Card>

          {/* Bid History */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="w-5 h-5" />
                Bid History
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {bidHistory.map((bid, index) => (
                <div key={bid.id} className="flex items-center justify-between p-2 rounded-lg bg-muted/50">
                  <div className="flex items-center gap-2">
                    <Avatar className="w-8 h-8">
                      <AvatarFallback>{bid.bidder.charAt(0)}</AvatarFallback>
                    </Avatar>
                    <div>
                      <p className="font-medium text-sm">{bid.bidder}</p>
                      <p className="text-xs text-muted-foreground">{formatTimeAgo(bid.timestamp)}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className={`font-bold ${bid.isWinning ? 'text-primary' : 'text-foreground'}`}>
                      {formatCurrency(bid.amount)}
                    </p>
                    {bid.isWinning && (
                      <Badge variant="default" className="text-xs">Winning</Badge>
                    )}
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Fixed Bottom Bidding Section */}
      <div className="fixed bottom-0 left-0 right-0 bg-background border-t p-4 space-y-3">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-muted-foreground">Minimum bid</p>
            <p className="font-bold text-lg">{formatCurrency(minimumBid)}</p>
          </div>
          <div className="text-right">
            <p className="text-sm text-muted-foreground">Auction ends in</p>
            <p className="font-bold text-lg text-red-600">{timeLeft}</p>
          </div>
        </div>
        
        <div className="flex gap-2">
          <div className="flex-1">
            <Input
              type="number"
              value={bidAmount}
              onChange={(e) => setBidAmount(e.target.value)}
              placeholder={`Minimum ${formatCurrency(minimumBid)}`}
              className="h-12 text-center font-semibold"
              min={minimumBid}
            />
          </div>
          <Button 
            className="h-12 px-8"
            onClick={handlePlaceBid}
            disabled={parseInt(bidAmount) < minimumBid}
          >
            Place Bid
          </Button>
        </div>
      </div>
    </div>
  );
}