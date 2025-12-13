import { useState } from 'react';
import { Card, CardContent, CardHeader } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar';
import { 
  Bell, 
  TrendingUp, 
  MessageCircle, 
  Clock, 
  Award,
  DollarSign,
  AlertTriangle,
  Check,
  X
} from 'lucide-react';

interface Notification {
  id: string;
  type: 'bid' | 'message' | 'auction_ending' | 'auction_won' | 'auction_lost' | 'verification' | 'payment';
  title: string;
  message: string;
  timestamp: Date;
  isRead: boolean;
  avatar?: string;
  actionUrl?: string;
  priority: 'low' | 'medium' | 'high';
}

const mockNotifications: Notification[] = [
  {
    id: '1',
    type: 'bid',
    title: 'New bid on your Brahman Bull',
    message: 'J. Manyika placed a bid of $1,200',
    timestamp: new Date(Date.now() - 300000),
    isRead: false,
    priority: 'high'
  },
  {
    id: '2',
    type: 'auction_ending',
    title: 'Auction ending soon',
    message: 'Your Dairy Cow auction ends in 2 hours',
    timestamp: new Date(Date.now() - 900000),
    isRead: false,
    priority: 'high'
  },
  {
    id: '3',
    type: 'message',
    title: 'New message',
    message: 'T. Chikwanha: "Is the bull still available for inspection?"',
    timestamp: new Date(Date.now() - 1800000),
    isRead: false,
    priority: 'medium'
  },
  {
    id: '4',
    type: 'auction_won',
    title: 'Congratulations! You won',
    message: 'You won the auction for Holstein Dairy Cow for $950',
    timestamp: new Date(Date.now() - 3600000),
    isRead: true,
    priority: 'high'
  },
  {
    id: '5',
    type: 'verification',
    title: 'Listing approved',
    message: 'Your Boer Goat listing has been approved and is now live',
    timestamp: new Date(Date.now() - 7200000),
    isRead: true,
    priority: 'medium'
  },
  {
    id: '6',
    type: 'payment',
    title: 'Payment reminder',
    message: 'Payment due for Holstein Dairy Cow auction within 24 hours',
    timestamp: new Date(Date.now() - 10800000),
    isRead: false,
    priority: 'high'
  },
  {
    id: '7',
    type: 'auction_lost',
    title: 'Auction ended',
    message: 'You were outbid on the Prime Brahman Bull auction',
    timestamp: new Date(Date.now() - 86400000),
    isRead: true,
    priority: 'low'
  }
];

export function Notifications() {
  const [notifications, setNotifications] = useState(mockNotifications);
  
  const unreadCount = notifications.filter(n => !n.isRead).length;
  
  const markAsRead = (id: string) => {
    setNotifications(prev => 
      prev.map(n => n.id === id ? { ...n, isRead: true } : n)
    );
  };

  const markAllAsRead = () => {
    setNotifications(prev => 
      prev.map(n => ({ ...n, isRead: true }))
    );
  };

  const deleteNotification = (id: string) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  };

  const formatTimeAgo = (date: Date) => {
    const now = new Date();
    const diffInMinutes = Math.floor((now.getTime() - date.getTime()) / (1000 * 60));
    
    if (diffInMinutes < 1) return 'Just now';
    if (diffInMinutes < 60) return `${diffInMinutes}m ago`;
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`;
    return `${Math.floor(diffInMinutes / 1440)}d ago`;
  };

  const getNotificationIcon = (type: string, priority: string) => {
    const iconProps = {
      className: `w-5 h-5 ${
        priority === 'high' ? 'text-red-600' :
        priority === 'medium' ? 'text-yellow-600' : 'text-blue-600'
      }`
    };

    switch (type) {
      case 'bid':
        return <TrendingUp {...iconProps} />;
      case 'message':
        return <MessageCircle {...iconProps} />;
      case 'auction_ending':
        return <Clock {...iconProps} />;
      case 'auction_won':
        return <Award {...iconProps} />;
      case 'auction_lost':
        return <AlertTriangle {...iconProps} />;
      case 'verification':
        return <Check {...iconProps} />;
      case 'payment':
        return <DollarSign {...iconProps} />;
      default:
        return <Bell {...iconProps} />;
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'border-l-red-500';
      case 'medium': return 'border-l-yellow-500';
      case 'low': return 'border-l-blue-500';
      default: return 'border-l-gray-300';
    }
  };

  return (
    <div className="space-y-4 pb-20">
      {/* Header */}
      <div className="sticky top-0 z-10 bg-background/95 backdrop-blur-sm border-b p-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold">Notifications</h1>
            <p className="text-sm text-muted-foreground">
              {unreadCount > 0 ? `${unreadCount} unread notifications` : 'All caught up!'}
            </p>
          </div>
          {unreadCount > 0 && (
            <Button variant="outline" size="sm" onClick={markAllAsRead}>
              Mark all read
            </Button>
          )}
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="px-4">
        <div className="flex gap-2 overflow-x-auto pb-2">
          <Badge variant="default" className="whitespace-nowrap">All</Badge>
          <Badge variant="outline" className="whitespace-nowrap">🔥 High Priority</Badge>
          <Badge variant="outline" className="whitespace-nowrap">💰 Bids</Badge>
          <Badge variant="outline" className="whitespace-nowrap">💬 Messages</Badge>
          <Badge variant="outline" className="whitespace-nowrap">⏰ Auctions</Badge>
        </div>
      </div>

      {/* Notifications */}
      <div className="px-4 space-y-3">
        {notifications.map((notification) => (
          <Card 
            key={notification.id} 
            className={`
              border-l-4 ${getPriorityColor(notification.priority)}
              ${!notification.isRead ? 'bg-primary/5 border-primary/20' : ''}
              cursor-pointer hover:shadow-md transition-shadow
            `}
            onClick={() => markAsRead(notification.id)}
          >
            <CardContent className="p-4">
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 pt-1">
                  {getNotificationIcon(notification.type, notification.priority)}
                </div>
                
                <div className="flex-1 min-w-0">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className={`font-medium ${!notification.isRead ? 'font-semibold' : ''}`}>
                        {notification.title}
                      </h3>
                      <p className="text-sm text-muted-foreground mt-1">
                        {notification.message}
                      </p>
                      <p className="text-xs text-muted-foreground mt-2">
                        {formatTimeAgo(notification.timestamp)}
                      </p>
                    </div>
                    
                    <div className="flex items-center gap-1 ml-2">
                      {!notification.isRead && (
                        <div className="w-2 h-2 bg-primary rounded-full" />
                      )}
                      <Button
                        variant="ghost"
                        size="sm"
                        className="p-1 h-auto text-muted-foreground hover:text-destructive"
                        onClick={(e) => {
                          e.stopPropagation();
                          deleteNotification(notification.id);
                        }}
                      >
                        <X className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {notifications.length === 0 && (
        <div className="text-center py-12">
          <div className="w-24 h-24 mx-auto mb-4 bg-muted rounded-full flex items-center justify-center">
            <Bell className="w-12 h-12 text-muted-foreground" />
          </div>
          <h3 className="font-semibold mb-2">No notifications</h3>
          <p className="text-muted-foreground">We'll notify you when something important happens</p>
        </div>
      )}
    </div>
  );
}