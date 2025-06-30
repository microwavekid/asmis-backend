# Dev Server Troubleshooting Guide

## Connection Refused on Hard Refresh

If you see "This site can't be reached" after a hard refresh:

### Quick Fix
1. Wait 2-3 seconds and refresh again (the server needs time to recompile)
2. If that doesn't work, the server may have crashed

### To Restart Dev Server
```bash
./start-dev.sh
```

### Manual Steps if Script Fails
```bash
# Kill any stuck processes
pkill -f "next dev"

# Check if port is free
lsof -i :3000

# Start server
npm run dev
```

## Common Issues

### Issue: Server crashes on file save
**Cause**: React 19 compatibility issues or TypeScript errors
**Fix**: Check console for specific errors, fix TypeScript issues

### Issue: Page loads but UI is broken
**Cause**: CSS not loading properly
**Fix**: Hard refresh (Cmd+Shift+R) or clear browser cache

### Issue: Smart Capture not working
**Current Status**: 
- ✅ Autocomplete dropdown now appears when typing @ # +
- ✅ Entity selector buttons work
- ❌ Inline highlighting not yet implemented
- ❌ Entity selection via dropdown click works but needs testing

## Server Logs
Logs are written to `/tmp/nextjs-log.txt` when using start-dev.sh