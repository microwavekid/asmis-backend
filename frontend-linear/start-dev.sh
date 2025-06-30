#!/bin/bash

# PATTERN_REF: DEV_SERVER_RELIABILITY_PATTERN
# DECISION_REF: DEC_2025-06-28_FIX_003

echo "Starting ASMIS Linear UI Dev Server..."

# Kill any existing Next.js processes
pkill -f "next dev" 2>/dev/null

# Wait a moment for ports to be released
sleep 1

# Check if port 3000 is available
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null ; then
    echo "Port 3000 is already in use. Attempting to free it..."
    lsof -ti:3000 | xargs kill -9 2>/dev/null
    sleep 2
fi

# Start the dev server
cd "$(dirname "$0")"
echo "Starting Next.js development server..."
npm run dev