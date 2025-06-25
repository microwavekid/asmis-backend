# ASMIS Linear Intelligence UI - Setup Guide

## 🎯 Overview
Modern Linear-inspired intelligence interface for ASMIS with MEDDPICC analysis, evidence tracking, and advanced deal management.

## 📋 Prerequisites

### Node.js Version (CRITICAL)
- **Required**: Node.js 20 LTS
- **Not Compatible**: Node.js 23+ (causes server binding issues)

```bash
# Install Node 20 via Homebrew (macOS)
brew install node@20
echo 'export PATH="/opt/homebrew/opt/node@20/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify version
node --version  # Should show v20.x.x
```

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone -b feat/linear-intelligence-ui https://github.com/microwavekid/asmis-frontend.git
cd asmis-frontend

# 2. Install dependencies
npm install --legacy-peer-deps

# 3. Start development server with Turbopack
npm run dev

# 4. Access the UI
open http://localhost:3000/deals
```

## ✨ Features

### Core Interface
- **Linear-inspired three-panel layout** with sidebar, main content, and evidence panel
- **Command palette** (Cmd/Ctrl+K) for quick navigation
- **Dark/light theme support** with system preference detection
- **Responsive design** optimized for desktop workflows

### MEDDPICC Intelligence
- **Interactive scoring system** with confidence indicators
- **Evidence tracking** with source attribution and timestamps
- **Strategic recommendations** based on qualification gaps
- **Risk factor analysis** with severity classification
- **Deal health visualization** with progress indicators

### Advanced Features
- **Advanced filtering** by stage, health band, value, and priority
- **Real-time search** across deal names and accounts
- **Sortable data tables** with Linear-style interactions
- **Evidence modal** with detailed source navigation
- **Export capabilities** for deal insights and reports

## 🛠 Development

### Available Scripts
```bash
npm run dev        # Start dev server with Turbopack
npm run build      # Production build
npm run start      # Start production server
npm run lint       # ESLint checking
```

### Performance Features
- **Turbopack enabled** for ~40% faster builds (923ms vs 1297ms)
- **Next.js 15.2.4** with React 19 for latest optimizations
- **Code splitting** and lazy loading for optimal bundle sizes

### Key Directories
```
app/(intelligence)/deals/     # Main deals interface
components/intelligence/      # UI components
types/                       # TypeScript definitions
hooks/                       # React hooks
lib/                        # Utilities and API clients
```

## 🔧 Configuration

### Environment Variables
```bash
# Add to .env.local if needed
NEXT_PUBLIC_API_URL=http://localhost:8000  # Backend API URL
```

### TypeScript
- Strict type checking enabled
- Custom types for MEDDPICC analysis
- Evidence and deal management types

## 🧪 Testing
```bash
# Run type checking
npx tsc --noEmit

# Build test
npm run build
```

## 📝 API Integration
The interface expects a backend API with endpoints for:
- Deal management (`/api/deals`)
- MEDDPICC analysis (`/api/meddpicc`)
- Evidence tracking (`/api/evidence`)

Mock data is currently used for development and testing.

## 🐛 Troubleshooting

### Common Issues

**Server won't bind to port:**
- Ensure Node.js 20 (not 23+)
- Kill existing processes: `pkill -f "next dev"`
- Try different port: `PORT=3001 npm run dev`

**Hydration errors:**
- Fixed in latest version with ThemeProvider updates
- Clear browser cache if persisting

**NaN% in MEDDPICC scores:**
- Fixed in latest version with correct data structure
- Refresh page to see updated scores

**Build errors:**
- Run `npm install --legacy-peer-deps` to resolve peer dependency conflicts
- Ensure Node 20 compatibility

## 🤝 Contributing
1. Create feature branch from `feat/linear-intelligence-ui`
2. Make changes with proper TypeScript types
3. Test locally with `npm run dev`
4. Commit with descriptive messages
5. Push and create pull request

## 📞 Support
For issues or questions about the Linear Intelligence UI:
- Check the troubleshooting section above
- Review commit history for recent fixes
- Create GitHub issue with environment details

---

**Last Updated**: June 2025  
**Version**: 1.0.0 (feat/linear-intelligence-ui)  
**Node Requirement**: 20 LTS  
**Status**: ✅ Working (hydration + NaN% issues resolved)