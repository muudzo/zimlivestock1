import { useState } from 'react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Label } from './ui/label';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { 
  ArrowLeft, 
  Camera, 
  MapPin, 
  DollarSign, 
  Clock, 
  Upload,
  X
} from 'lucide-react';

interface PostLivestockProps {
  onBack: () => void;
}

export function PostLivestock({ onBack }: PostLivestockProps) {
  const [formData, setFormData] = useState({
    title: '',
    category: '',
    breed: '',
    age: '',
    weight: '',
    description: '',
    location: '',
    startingPrice: '',
    auctionDuration: '',
    healthStatus: ''
  });

  const [images, setImages] = useState<string[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleInputChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleImageUpload = () => {
    // Simulate image upload
    const newImage = `https://images.unsplash.com/photo-1560114928-40f1f1eb26a0?w=400&h=300&fit=crop&crop=center`;
    setImages(prev => [...prev, newImage]);
  };

  const removeImage = (index: number) => {
    setImages(prev => prev.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    setIsSubmitting(false);
    alert('Livestock posted successfully! Your auction will go live within 24 hours after verification.');
    onBack();
  };

  const categories = [
    { value: 'cattle', label: '🐄 Cattle', icon: '🐄' },
    { value: 'goats', label: '🐐 Goats', icon: '🐐' },
    { value: 'sheep', label: '🐑 Sheep', icon: '🐑' },
    { value: 'pigs', label: '🐷 Pigs', icon: '🐷' },
    { value: 'chickens', label: '🐔 Chickens', icon: '🐔' },
    { value: 'other', label: '🦌 Other', icon: '🦌' }
  ];

  const auctionDurations = [
    { value: '1', label: '1 day' },
    { value: '3', label: '3 days' },
    { value: '7', label: '1 week' },
    { value: '14', label: '2 weeks' }
  ];

  const locations = [
    'Harare', 'Bulawayo', 'Chitungwiza', 'Mutare', 'Gweru', 
    'Kwekwe', 'Kadoma', 'Masvingo', 'Chinhoyi', 'Marondera'
  ];

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="sticky top-0 z-10 bg-background/95 backdrop-blur-sm border-b">
        <div className="flex items-center justify-between p-4">
          <Button variant="ghost" size="sm" onClick={onBack}>
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back
          </Button>
          <h1 className="font-semibold">Post Livestock</h1>
          <div className="w-16" />
        </div>
      </div>

      <form onSubmit={handleSubmit} className="p-4 space-y-6 pb-24">
        {/* Photos */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Camera className="w-5 h-5" />
              Photos
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              {images.map((image, index) => (
                <div key={index} className="relative">
                  <img 
                    src={image} 
                    alt={`Upload ${index + 1}`}
                    className="w-full h-32 object-cover rounded-lg border-2 border-border"
                  />
                  <Button
                    type="button"
                    variant="destructive"
                    size="sm"
                    className="absolute top-2 right-2 p-1 h-auto"
                    onClick={() => removeImage(index)}
                  >
                    <X className="w-3 h-3" />
                  </Button>
                </div>
              ))}
              {images.length < 4 && (
                <Button
                  type="button"
                  variant="outline"
                  className="h-32 border-2 border-dashed"
                  onClick={handleImageUpload}
                >
                  <div className="text-center">
                    <Upload className="w-6 h-6 mx-auto mb-2" />
                    <p className="text-sm">Add Photo</p>
                  </div>
                </Button>
              )}
            </div>
            <p className="text-sm text-muted-foreground">
              Add up to 4 high-quality photos. First photo will be the main image.
            </p>
          </CardContent>
        </Card>

        {/* Basic Information */}
        <Card>
          <CardHeader>
            <CardTitle>Basic Information</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="title">Title *</Label>
              <Input
                id="title"
                placeholder="e.g., Prime Brahman Bull"
                value={formData.title}
                onChange={(e) => handleInputChange('title', e.target.value)}
                className="h-12"
                required
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="category">Category *</Label>
                <Select 
                  value={formData.category} 
                  onValueChange={(value) => handleInputChange('category', value)}
                  required
                >
                  <SelectTrigger className="h-12">
                    <SelectValue placeholder="Select category" />
                  </SelectTrigger>
                  <SelectContent>
                    {categories.map((cat) => (
                      <SelectItem key={cat.value} value={cat.value}>
                        {cat.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="breed">Breed *</Label>
                <Input
                  id="breed"
                  placeholder="e.g., Brahman"
                  value={formData.breed}
                  onChange={(e) => handleInputChange('breed', e.target.value)}
                  className="h-12"
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="age">Age *</Label>
                <Input
                  id="age"
                  placeholder="e.g., 3 years"
                  value={formData.age}
                  onChange={(e) => handleInputChange('age', e.target.value)}
                  className="h-12"
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="weight">Weight *</Label>
                <Input
                  id="weight"
                  placeholder="e.g., 850kg"
                  value={formData.weight}
                  onChange={(e) => handleInputChange('weight', e.target.value)}
                  className="h-12"
                  required
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="description">Description</Label>
              <Textarea
                id="description"
                placeholder="Provide additional details about the livestock..."
                value={formData.description}
                onChange={(e) => handleInputChange('description', e.target.value)}
                className="min-h-20"
              />
            </div>
          </CardContent>
        </Card>

        {/* Location & Health */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <MapPin className="w-5 h-5" />
              Location & Health
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="location">Location *</Label>
                <Select 
                  value={formData.location} 
                  onValueChange={(value) => handleInputChange('location', value)}
                  required
                >
                  <SelectTrigger className="h-12">
                    <SelectValue placeholder="Select city" />
                  </SelectTrigger>
                  <SelectContent>
                    {locations.map((location) => (
                      <SelectItem key={location} value={location}>
                        {location}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="health">Health Status *</Label>
                <Select 
                  value={formData.healthStatus} 
                  onValueChange={(value) => handleInputChange('healthStatus', value)}
                  required
                >
                  <SelectTrigger className="h-12">
                    <SelectValue placeholder="Select status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="excellent">Excellent</SelectItem>
                    <SelectItem value="good">Good</SelectItem>
                    <SelectItem value="fair">Fair</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Auction Details */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <DollarSign className="w-5 h-5" />
              Auction Details
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="startingPrice">Starting Price (USD) *</Label>
                <div className="relative">
                  <DollarSign className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                  <Input
                    id="startingPrice"
                    type="number"
                    placeholder="800"
                    value={formData.startingPrice}
                    onChange={(e) => handleInputChange('startingPrice', e.target.value)}
                    className="pl-10 h-12"
                    min="1"
                    required
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="duration">Auction Duration *</Label>
                <Select 
                  value={formData.auctionDuration} 
                  onValueChange={(value) => handleInputChange('auctionDuration', value)}
                  required
                >
                  <SelectTrigger className="h-12">
                    <SelectValue placeholder="Select duration" />
                  </SelectTrigger>
                  <SelectContent>
                    {auctionDurations.map((duration) => (
                      <SelectItem key={duration.value} value={duration.value}>
                        <div className="flex items-center gap-2">
                          <Clock className="w-4 h-4" />
                          {duration.label}
                        </div>
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="bg-muted/50 p-4 rounded-lg">
              <h4 className="font-medium mb-2">Auction Terms</h4>
              <ul className="text-sm text-muted-foreground space-y-1">
                <li>• 5% platform fee on successful sales</li>
                <li>• Payment due within 48 hours of auction end</li>
                <li>• Buyer inspection allowed before payment</li>
                <li>• Free listing for verified farmers</li>
              </ul>
            </div>
          </CardContent>
        </Card>
      </form>

      {/* Fixed Bottom Submit */}
      <div className="fixed bottom-0 left-0 right-0 bg-background border-t p-4">
        <Button 
          type="submit" 
          className="w-full h-12"
          disabled={isSubmitting || !formData.title || !formData.category || !formData.breed}
          onClick={handleSubmit}
        >
          {isSubmitting ? 'Posting...' : 'Post Livestock'}
        </Button>
        <p className="text-center text-xs text-muted-foreground mt-2">
          Your listing will be reviewed and published within 24 hours
        </p>
      </div>
    </div>
  );
}