# Session: 2025-06-24 - Linear UI Debugging & Resolution

## ✅ Completed Tasks

### 1. Major Linear UI Debugging Session
- **Initial Issue**: "Cursor did something and screwed up the work we did for the ui"
- **Symptoms**: ERR_CONNECTION_REFUSED, UI not loading, showing old interface instead of modern Linear UI
- **User Feedback**: "we definitely built it" with GitHub link to separate asmis-frontend repository

### 2. Repository Discovery & Cloning
- **Key Discovery**: Linear UI was in separate repository (github.com/microwavekid/asmis-frontend)
- **Action**: Cloned separate repository to debug the actual Linear UI
- **Lesson**: Initial debugging was on wrong codebase (main repo vs separate Linear UI repo)

### 3. Critical Node.js Version Issue Resolution
- **Root Cause**: Node.js v23 incompatibility with Next.js 15.2.4
- **Error**: Server binding issues causing ERR_CONNECTION_REFUSED
- **Solution**: Downgraded to Node 20 LTS via Homebrew
```bash
brew install node@20
echo 'export PATH="/opt/homebrew/opt/node@20/bin:$PATH"' >> ~/.zshrc
```
- **Verification**: User confirmed "it's working!" after Node version fix

### 4. React Hydration Error Resolution
- **Issue**: "Hydration failed because the server rendered HTML didn't match the client"
- **Root Cause**: ThemeProvider with defaultTheme="system" causing client/server mismatch
- **Solution**: Changed to defaultTheme="light" + suppressHydrationWarning
- **Additional Fix**: Added mounted state check in ThemeProvider component

### 5. MEDDPICC Scoring Display Fix
- **Issue**: NaN% display in MEDDPICC scores (user screenshot)
- **Root Cause**: Mock data used camelCase (overallScore) but component expected snake_case (overall_score)
- **Solution**: Updated all mock data field names to snake_case
- **Files Fixed**: `app/(intelligence)/deals/page.tsx` with corrected mock data structure

### 6. Performance Optimization
- **Enhancement**: Added Turbopack support (--turbo flag)
- **Result**: ~40% faster builds (923ms vs 1297ms)
- **Configuration**: Updated package.json dev script

### 7. Post-Mortem Documentation
- **Created**: `.project_memory/patterns/COLLABORATION_DEBUG_PATTERN.json`
- **Purpose**: Capture debugging session patterns for future sessions
- **Decision**: Added DEC_2025-06-24_001 for pattern documentation

### 8. Setup Documentation
- **Created**: `frontend-linear/SETUP.md` with comprehensive setup guide
- **Content**: Node 20 requirement, troubleshooting, performance features
- **Purpose**: Prevent future version compatibility issues

## 📊 Current Project State

### Frontend Structure
```
frontend/app/
├── (intelligence)/          # New v0 UI with route group
│   ├── deals/              # ✅ Implemented
│   │   └── page.tsx
│   └── layout.tsx          # Modern three-panel layout
├── layout.tsx              # Minimal root layout
├── page.tsx                # Redirects to /deals
└── globals.css             # Includes design-system.css
```

### Active Features in v0 UI
- WorkspaceSelector
- NavigationMenu (with corrected routes)
- AIProcessingStatus
- EvidencePanel
- CommandPalette (Cmd+K)
- Modern Linear-inspired design system

## 🎯 Next Steps (When Returning)
1. **Complete MEDDPICC card components with evidence display** (Priority: High)
2. **Implement backend-frontend integration for deal intelligence** (Priority: High)
3. **Consider creating placeholder pages** for other routes
4. **Add timeline extraction from transcripts** (Priority: Medium)
5. **Add budget range detection capabilities** (Priority: Medium)

## 📋 Key Decisions Made
- Chose to make v0 intelligence UI the primary interface
- Removed all old UI code to avoid confusion
- Fixed routing to use root-level paths instead of /intelligence prefix

## 🔧 Technical Notes
- Dev server runs on standard Next.js setup (no special v0 server)
- Project name "my-v0-project" is just the scaffold name
- All v0 UI components properly integrated with shadcn/ui
- Frontend ready for backend integration

## 🧠 Debugging Patterns Captured

### Repository Confusion Pattern
- **Problem**: Multiple frontend directories causing confusion
- **Learning**: Always confirm correct repository when debugging UI issues
- **Solution**: Clear separation of old vs new UI, focus on correct codebase

### Node.js Compatibility Pattern  
- **Problem**: Bleeding edge Node versions breaking Next.js compatibility
- **Learning**: Stick to LTS versions for production stability
- **Solution**: Documented Node 20 requirement, added setup verification

### React Hydration Pattern
- **Problem**: Server/client state mismatch with theme providers
- **Learning**: Theme detection causes hydration issues
- **Solution**: Default to static theme + mounted state checks

---
**Status**: ✅ Complete - Linear UI fully functional
**Duration**: ~3 hours (extensive debugging)
**Outcome**: Working Linear Intelligence UI with all issues resolved
**Next Session**: Integration planning and intelligence system enhancement