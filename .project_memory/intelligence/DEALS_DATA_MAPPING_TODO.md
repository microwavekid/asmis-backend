# Deals Data Mapping TODO

## Current Status
**Date**: 2025-01-03
**Issue**: Frontend deals table not displaying data from backend

## Problem Summary
1. **API Route Mismatch**: 
   - Frontend calls: `/api/deals/`
   - Backend serves: `/api/v1/deals/`

2. **Missing Next.js API Routes**: 
   - No bridge between frontend and FastAPI backend
   - Frontend expects Next.js API routes that proxy to backend

3. **Response Format Mismatch**:
   - Backend returns: `DealListResponse[]` (array)
   - Frontend expects: `{ deals: DealIntelligence[], total: number, offset: number, limit: number, hasMore: boolean }`

4. **Missing Data**:
   - Database likely empty (no test deals/accounts/MEDDPICC analyses)
   - Need sample data for development/testing

## Solution Plan

### Phase 1: Create API Route Bridge
Create Next.js API routes in `frontend-linear/app/api/`:

```typescript
// app/api/deals/route.ts
export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  
  // Proxy to backend with /api/v1 prefix
  const backendUrl = `${process.env.BACKEND_URL}/api/v1/deals?${searchParams}`
  const response = await fetch(backendUrl)
  const deals = await response.json()
  
  // Transform to expected format
  return Response.json({
    deals: deals.map(transformToDealIntelligence),
    total: deals.length,
    offset: parseInt(searchParams.get('offset') || '0'),
    limit: parseInt(searchParams.get('limit') || '50'),
    hasMore: false
  })
}
```

### Phase 2: Sample Data Script
Create `backend/scripts/seed_sample_data.py`:
- 3-4 sample accounts
- 6-8 deals in various stages
- 2-3 MEDDPICC analyses
- Stakeholder relationships

### Phase 3: Data Transformation
Map backend `DealListResponse` to frontend `DealIntelligence`:
- Convert flat structure to nested MEDDPICC format
- Add missing fields with defaults
- Transform date strings

## Files to Create
1. `frontend-linear/app/api/deals/route.ts`
2. `frontend-linear/app/api/deals/[id]/route.ts`
3. `frontend-linear/app/api/deals/[id]/meddpicc/route.ts`
4. `frontend-linear/app/api/deals/stats/route.ts`
5. `backend/scripts/seed_sample_data.py`

## Next Steps
1. Create Next.js API routes
2. Run sample data script
3. Test end-to-end data flow
4. Verify deals table displays data

**Time Estimate**: 2 hours
**Blocked By**: Need to implement multi-tenancy first to ensure proper data isolation