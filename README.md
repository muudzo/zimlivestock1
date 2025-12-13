# ZimLivestock - Zimbabwe's Premier Livestock Marketplace

A modern, responsive web application connecting farmers across Zimbabwe to buy and sell livestock through an intuitive auction system.

## 🚀 Features

### Core Features
- **Livestock Auctions**: Real-time bidding system for cattle, goats, sheep, pigs, and chickens
- **User Authentication**: Secure login/registration with phone and email verification
- **Advanced Search & Filtering**: Find livestock by category, location, price range, and more
- **Real-time Notifications**: Get notified about bids, auction endings, and messages
- **Messaging System**: Direct communication between buyers and sellers
- **Image Upload**: High-quality photo management for livestock listings
- **Mobile-First Design**: Optimized for all devices and screen sizes

### Technical Features
- **TypeScript**: Full type safety and better developer experience
- **React 18**: Latest React features with concurrent rendering
- **Vite**: Fast build tool and development server
- **Tailwind CSS**: Utility-first CSS framework with custom design system
- **Zustand**: Lightweight state management
- **React Query**: Powerful data fetching and caching
- **Error Boundaries**: Graceful error handling
- **PWA Ready**: Progressive Web App capabilities
- **SEO Optimized**: Meta tags, structured data, and performance

## 🛠️ Tech Stack

- **Frontend**: React 18, TypeScript, Vite
- **Styling**: Tailwind CSS, shadcn/ui components
- **State Management**: Zustand, React Query
- **Build Tool**: Vite
- **Testing**: Vitest, React Testing Library
- **Code Quality**: ESLint, Prettier, Husky
- **Deployment**: Vercel, Netlify, or any static hosting

## 📦 Installation

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/zimlivestock.git
   cd zimlivestock
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env.local
   ```
   Edit `.env.local` with your configuration values.

4. **Start development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

5. **Open your browser**
   Navigate to `http://localhost:3000`

## 🧪 Testing

```bash
# Run tests
npm run test

# Run tests with UI
npm run test:ui

# Run tests with coverage
npm run test:coverage
```

## 📝 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run lint:fix` - Fix ESLint errors
- `npm run format` - Format code with Prettier
- `npm run type-check` - Run TypeScript type checking
- `npm run test` - Run tests
- `npm run test:ui` - Run tests with UI
- `npm run test:coverage` - Run tests with coverage

## 🏗️ Project Structure

```
zimlivestock/
├── components/          # React components
│   ├── ui/             # shadcn/ui components
│   ├── figma/          # Figma-specific components
│   └── ...             # Feature components
├── src/
│   ├── hooks/          # Custom React hooks
│   ├── lib/            # Utility functions
│   ├── services/       # API services
│   ├── stores/         # Zustand stores
│   ├── types/          # TypeScript type definitions
│   └── styles/         # Global styles
├── guidelines/         # Project guidelines
├── public/             # Static assets
└── ...                 # Configuration files
```

## 🎨 Design System

The application uses a comprehensive design system built with:
- **Tailwind CSS** for utility-first styling
- **shadcn/ui** for pre-built components
- **Custom CSS variables** for theming
- **Responsive design** principles
- **Accessibility** best practices

### Color Palette
- **Primary**: Green (#16a34a) - Represents agriculture and growth
- **Secondary**: Gray (#64748b) - Neutral and professional
- **Accent**: Blue (#3b82f6) - Trust and reliability
- **Destructive**: Red (#ef4444) - Warnings and errors

## 🔧 Configuration

### Environment Variables

Create a `.env.local` file with the following variables:

```env
# API Configuration
VITE_API_BASE_URL=https://api.zimlivestock.com
VITE_API_TIMEOUT=10000

# Authentication
VITE_AUTH_DOMAIN=auth.zimlivestock.com
VITE_AUTH_CLIENT_ID=your-auth-client-id

# Feature Flags
VITE_ENABLE_CHAT=true
VITE_ENABLE_NOTIFICATIONS=true
VITE_MOCK_API=true
```

### Build Configuration

The project uses Vite for building. Key configurations:

- **TypeScript**: Strict mode enabled
- **Path Aliases**: Configured for clean imports
- **Code Splitting**: Automatic chunk optimization
- **Source Maps**: Enabled for debugging

## 🚀 Deployment

### Vercel (Recommended)

1. Connect your GitHub repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push to main branch

### Netlify

1. Connect your GitHub repository to Netlify
2. Set build command: `npm run build`
3. Set publish directory: `dist`
4. Configure environment variables

### Manual Deployment

```bash
# Build the project
npm run build

# The built files will be in the `dist` directory
# Upload the contents to your web server
```

## 📱 PWA Features

The application is PWA-ready with:
- **Service Worker**: Offline functionality
- **Web App Manifest**: App-like experience
- **Install Prompt**: Add to home screen
- **Offline Support**: Basic offline functionality

## 🔒 Security

- **Input Validation**: All user inputs are validated
- **XSS Protection**: Content Security Policy
- **HTTPS Only**: Secure connections required
- **Token-based Auth**: JWT authentication
- **Rate Limiting**: API rate limiting protection

## 📊 Performance

- **Lazy Loading**: Components and routes
- **Image Optimization**: WebP format support
- **Code Splitting**: Automatic bundle splitting
- **Caching**: React Query caching
- **CDN Ready**: Static asset optimization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Use TypeScript for all new code
- Follow ESLint and Prettier configurations
- Write meaningful commit messages
- Add tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [docs.zimlivestock.com](https://docs.zimlivestock.com)
- **Issues**: [GitHub Issues](https://github.com/your-org/zimlivestock/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/zimlivestock/discussions)
- **Email**: support@zimlivestock.com

## 🙏 Acknowledgments

- [shadcn/ui](https://ui.shadcn.com/) for the component library
- [Tailwind CSS](https://tailwindcss.com/) for the styling framework
- [Vite](https://vitejs.dev/) for the build tool
- [Unsplash](https://unsplash.com/) for stock photos
- All contributors and farmers who provided feedback

---

Built with ❤️ for the Zimbabwe farming community
