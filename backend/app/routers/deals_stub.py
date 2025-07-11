"""
Deals API Router Stub - Multi-Tenancy Integration Testing

TODO: This is a STUB implementation for early integration testing.
Real deal endpoints will be updated in Phase 4 (MIC-70).

Purpose: Test complete multi-tenant flow with auth dependencies
before implementing real database changes.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..auth import AuthContext, get_auth_context_stub
from ..database.repository_context import get_repository_for_tenant
from ..repositories.deal_repository_stub import deal_repository_stub


# Create stub router with same prefix as real router
router = APIRouter(prefix="/api/v1/deals", tags=["deals-stub"])


def get_session_stub():
    """
    STUB: Mock database session for testing.
    TODO: Replace with real session in Phase 4.
    """
    return None  # Stub repositories don't use session


@router.get("/")
async def list_deals(
    auth: AuthContext = Depends(get_auth_context_stub),
    session: Session = Depends(get_session_stub)
) -> List[Dict[str, Any]]:
    """
    STUB: List deals for authenticated tenant.
    TODO: Replace with real implementation in Phase 4.
    """
    try:
        # Get tenant-aware repository wrapper
        repo = get_repository_for_tenant(deal_repository_stub, auth.tenant_id)
        
        # Get all deals for tenant
        deals = repo.get_all(session)
        
        # Convert MockModel objects to dicts for JSON response
        return [
            {
                "id": deal.id,
                "title": deal.title,
                "description": deal.description,
                "stage": deal.stage,
                "value": deal.value,
                "account_id": deal.account_id,
                "tenant_id": deal.tenant_id,
                "created_at": deal.created_at,
                "updated_at": getattr(deal, 'updated_at', deal.created_at)  # Fallback to created_at
            }
            for deal in deals
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing deals: {str(e)}")


@router.get("/stats")
async def get_deal_stats(
    auth: AuthContext = Depends(get_auth_context_stub),
    session: Session = Depends(get_session_stub)
) -> Dict[str, Any]:
    """
    STUB: Get deal statistics for authenticated tenant.
    TODO: Replace with real implementation in Phase 4.
    """
    try:
        # Use the stub repository directly for stats
        stats = deal_repository_stub.get_deal_stats(session, auth.tenant_id)
        
        return {
            "total_deals": stats["total_deals"],
            "total_value": stats["total_value"],
            "avg_deal_size": stats["avg_deal_size"],
            "deals_by_stage": stats["deals_by_stage"],
            "tenant_id": auth.tenant_id,
            "calculated_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating stats: {str(e)}")


@router.get("/{deal_id}")
async def get_deal(
    deal_id: str,
    auth: AuthContext = Depends(get_auth_context_stub),
    session: Session = Depends(get_session_stub)
) -> Dict[str, Any]:
    """
    STUB: Get specific deal with tenant ownership check.
    TODO: Replace with real implementation in Phase 4.
    """
    try:
        # Get tenant-aware repository wrapper
        repo = get_repository_for_tenant(deal_repository_stub, auth.tenant_id)
        
        # Get deal by ID (tenant filtering enforced)
        deal = repo.get_by_id(session, deal_id)
        
        if not deal:
            raise HTTPException(status_code=404, detail="Deal not found")
        
        return {
            "id": deal.id,
            "title": deal.title,
            "description": deal.description,
            "stage": deal.stage,
            "value": deal.value,
            "account_id": deal.account_id,
            "tenant_id": deal.tenant_id,
            "created_at": deal.created_at,
            "updated_at": getattr(deal, 'updated_at', deal.created_at)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching deal: {str(e)}")


@router.post("/")
async def create_deal(
    deal_data: Dict[str, Any],
    auth: AuthContext = Depends(get_auth_context_stub),
    session: Session = Depends(get_session_stub)
) -> Dict[str, Any]:
    """
    STUB: Create new deal for authenticated tenant.
    TODO: Replace with real implementation in Phase 4.
    """
    try:
        # Get tenant-aware repository wrapper
        repo = get_repository_for_tenant(deal_repository_stub, auth.tenant_id)
        
        # Create deal (tenant_id automatically injected)
        new_deal = repo.create(
            session,
            title=deal_data.get("title", "New Deal"),
            description=deal_data.get("description", ""),
            stage=deal_data.get("stage", "qualification"),
            value=deal_data.get("value", 0.0),
            account_id=deal_data.get("account_id", "default-account")
        )
        
        return {
            "id": new_deal.id,
            "title": new_deal.title,
            "description": new_deal.description,
            "stage": new_deal.stage,
            "value": new_deal.value,
            "account_id": new_deal.account_id,
            "tenant_id": new_deal.tenant_id,
            "created_at": new_deal.created_at,
            "message": "Deal created successfully (STUB)"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating deal: {str(e)}")


# Test endpoint to verify tenant isolation
@router.get("/test/tenant-info")
async def get_tenant_info(
    auth: AuthContext = Depends(get_auth_context_stub)
) -> Dict[str, Any]:
    """
    STUB: Test endpoint to verify auth context.
    TODO: Remove in production.
    """
    return {
        "user_id": auth.user_id,
        "tenant_id": auth.tenant_id,
        "email": auth.email,
        "role": auth.role,
        "message": "Auth context working correctly"
    }