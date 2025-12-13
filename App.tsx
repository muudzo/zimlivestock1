import { useState, useEffect } from 'react';
import { AuthScreen } from '@/components/AuthScreen';
import { HomeFeed } from '@/components/HomeFeed';
import { BiddingScreen } from '@/components/BiddingScreen';
import { PostLivestock } from '@/components/PostLivestock';
import { MyListings } from '@/components/MyListings';
import { Notifications } from '@/components/Notifications';
import { BottomNavigation } from '@/components/BottomNavigation';
import { useAuthStore } from '@/stores/authStore';
import { useAppStore } from '@/stores/appStore';
import { LivestockItem } from '@/types';
import { Helmet } from 'react-helmet-async';

export default function App() {
  const { isAuthenticated, user, isLoading } = useAuthStore();
  const { theme, setTheme } = useAppStore();
  const [currentTab, setCurrentTab] = useState('home');
  const [currentScreen, setCurrentScreen] = useState<'main' | 'bidding'>('main');
  const [selectedLivestock, setSelectedLivestock] = useState<LivestockItem | null>(null);

  // Initialize theme on app start
  useEffect(() => {
    setTheme(theme);
  }, [theme, setTheme]);

  const handleLogin = () => {
    // Login is handled by the auth store
  };

  const handleItemClick = (item: LivestockItem) => {
    setSelectedLivestock(item);
    setCurrentScreen('bidding');
  };

  const handleBackToMain = () => {
    setCurrentScreen('main');
    setSelectedLivestock(null);
  };

  // Show loading state while checking authentication
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center space-y-4">
          <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

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
    <>
      <Helmet>
        <title>ZimLivestock - Zimbabwe's Premier Livestock Marketplace</title>
        <meta name="description" content="Connect with farmers across Zimbabwe to buy and sell livestock through our secure auction platform. Cattle, goats, sheep, pigs, and chickens." />
        <meta name="keywords" content="livestock, zimbabwe, farming, cattle, goats, sheep, pigs, chickens, auction, marketplace" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta property="og:title" content="ZimLivestock - Zimbabwe's Premier Livestock Marketplace" />
        <meta property="og:description" content="Connect with farmers across Zimbabwe to buy and sell livestock through our secure auction platform." />
        <meta property="og:type" content="website" />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="ZimLivestock - Zimbabwe's Premier Livestock Marketplace" />
        <meta name="twitter:description" content="Connect with farmers across Zimbabwe to buy and sell livestock through our secure auction platform." />
      </Helmet>
      <div className="min-h-screen bg-background">
        {renderCurrentTab()}
        <BottomNavigation 
          currentTab={currentTab}
          onTabChange={setCurrentTab}
          notificationCount={3}
          messageCount={2}
        />
      </div>
    </>
  );
}