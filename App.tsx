import { useState } from 'react';
import { AuthScreen } from '@/components/AuthScreen';
import { HomeFeed } from '@/components/HomeFeed';
import { BiddingScreen } from '@/components/BiddingScreen';
import { PostLivestock } from '@/components/PostLivestock';
import { MyListings } from '@/components/MyListings';
import { Notifications } from '@/components/Notifications';
import { BottomNavigation } from '@/components/BottomNavigation';

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [currentTab, setCurrentTab] = useState('home');
  const [currentScreen, setCurrentScreen] = useState<'main' | 'bidding'>('main');
  const [selectedLivestock, setSelectedLivestock] = useState<any>(null);

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleItemClick = (item: any) => {
    setSelectedLivestock(item);
    setCurrentScreen('bidding');
  };

  const handleBackToMain = () => {
    setCurrentScreen('main');
    setSelectedLivestock(null);
  };

  if (!isAuthenticated) {
    return <AuthScreen onLogin={handleLogin} />;
  }

  if (currentScreen === 'bidding' && selectedLivestock) {
    return (
      <BiddingScreen 
        onBack={handleBackToMain}
        livestockItem={selectedLivestock}
      />
    );
  }

  const renderCurrentTab = () => {
    switch (currentTab) {
      case 'home':
        return <HomeFeed onItemClick={handleItemClick} />;
      case 'post':
        return <PostLivestock onBack={() => setCurrentTab('home')} />;
      case 'listings':
        return <MyListings />;
      case 'notifications':
        return <Notifications />;
      case 'messages':
        return (
          <div className="flex items-center justify-center min-h-screen pb-20">
            <div className="text-center space-y-4">
              <div className="w-24 h-24 mx-auto bg-muted rounded-full flex items-center justify-center">
                💬
              </div>
              <h2 className="text-xl font-semibold">Messages</h2>
              <p className="text-muted-foreground max-w-sm">
                Chat with other farmers about livestock deals. This feature will be available soon with real-time messaging.
              </p>
            </div>
          </div>
        );
      default:
        return <HomeFeed onItemClick={handleItemClick} />;
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {renderCurrentTab()}
      <BottomNavigation 
        currentTab={currentTab}
        onTabChange={setCurrentTab}
        notificationCount={3}
        messageCount={2}
      />
    </div>
  );
}