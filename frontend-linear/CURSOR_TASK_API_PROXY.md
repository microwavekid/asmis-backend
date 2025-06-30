# Task: Connect Frontend to FastAPI Backend

## Current Issue
The Next.js frontend at `/frontend-linear/app/api/deals/route.ts` is returning hardcoded mock data instead of proxying to the FastAPI backend running on `http://localhost:8000`.

## Required Changes
Update the Next.js API route to proxy requests to the FastAPI backend:
- Replace mock data with actual fetch calls to `http://localhost:8000/api/v1/deals/`
- Handle CORS properly (backend already has CORS configured)
- Transform the response to match frontend expectations
- Maintain error handling with fallback to mock data if backend is unavailable

## Files to Modify
1. `/frontend-linear/app/api/deals/route.ts` - Update to proxy to backend
2. `/frontend-linear/app/api/deals/stats/route.ts` - Update to proxy to backend (if exists)

## Backend Endpoints Available
- `GET http://localhost:8000/api/v1/deals/` - List all deals
- `GET http://localhost:8000/api/v1/deals/{id}` - Get specific deal
- `GET http://localhost:8000/api/v1/deals/{id}/meddpicc` - Get MEDDPICC analysis

## Expected Behavior
When user visits `http://localhost:3000/deals`, they should see:
- "Smart Capture POC" deal from the database (not "Q4 Implementation")
- Real MEDDPICC score of 68%
- $75,000 value
- Data fetched from FastAPI backend

## Success Criteria
1. Remove hardcoded mock data
2. Implement proper proxy to backend
3. Handle errors gracefully
4. Maintain TypeScript types
5. Test that real data appears in UI

## Example Implementation Pattern
```typescript
const backendUrl = process.env.BACKEND_URL || 'http://localhost:8000'
const response = await fetch(`${backendUrl}/api/v1/deals/`)
```

Please implement this proxy connection now.