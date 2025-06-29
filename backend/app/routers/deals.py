"""
Deals API Router - MVP Backend-Frontend Integration
Connects Linear UI to real MEDDPICC data.

PATTERN_REF: MVP_FIRST_BUILDING_BLOCKS_PATTERN
DECISION_REF: DEC_2025-06-29_MVP_PIVOT_001
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

from ..database.connection import get_async_db_session
from ..database.models import Deal, Account, MEDDPICCAnalysis, Stakeholder
from ..schemas.deals import DealResponse, DealCreate, DealUpdate, MEDDPICCResponse, DealListResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/deals", tags=["deals"])


@router.get("/", response_model=List[DealListResponse])
async def list_deals(
    stage: Optional[str] = Query(None, description="Filter by deal stage"),
    account_id: Optional[str] = Query(None, description="Filter by account"),
    limit: int = Query(50, le=100, description="Maximum number of deals to return"),
    offset: int = Query(0, description="Number of deals to skip"),
    db: AsyncSession = Depends(get_async_db_session)
):
    """
    List deals with optional filtering and pagination.
    Returns data compatible with Linear UI deals table.
    """
    try:
        # Build query with joins
        query = select(
            Deal,
            Account.name.label("account_name"),
            MEDDPICCAnalysis.overall_score.label("meddpicc_score"),
            MEDDPICCAnalysis.completeness_score.label("health_score")
        ).join(
            Account, Deal.account_id == Account.id
        ).outerjoin(
            MEDDPICCAnalysis, Deal.id == MEDDPICCAnalysis.deal_id
        )
        
        # Apply filters
        if stage:
            query = query.where(Deal.stage == stage)
        if account_id:
            query = query.where(Deal.account_id == account_id)
        
        # Apply pagination
        query = query.offset(offset).limit(limit)
        
        result = await db.execute(query)
        rows = result.all()
        
        # Transform to frontend format
        deals = []
        for row in rows:
            deal = row.Deal
            account_name = row.account_name
            meddpicc_score = row.meddpicc_score or 0.0
            health_score = row.health_score or 0.0
            
            # Calculate priority based on close date and amount
            priority = _calculate_priority(deal.close_date, deal.amount)
            
            deals.append(DealListResponse(
                id=deal.id,
                name=deal.name,
                account=account_name,
                stage=deal.stage,
                health=int(health_score),  # Convert to 0-100 integer
                value=deal.amount or 0,
                closeDate=deal.close_date.isoformat() if deal.close_date else None,
                meddpiccScore=int(meddpicc_score),  # Convert to 0-100 integer
                confidence=deal.probability or 0,
                priority=priority,
                nextActions=[],  # TODO: Add from MEDDPICC recommendations
                risks=[]  # TODO: Add from MEDDPICC risk factors
            ))
        
        return deals
        
    except Exception as e:
        logger.error(f"Error listing deals: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to list deals")


@router.get("/{deal_id}", response_model=DealResponse)
async def get_deal(
    deal_id: str,
    db: AsyncSession = Depends(get_async_db_session)
):
    """Get detailed deal information including MEDDPICC analysis."""
    try:
        # Get deal with account and MEDDPICC data
        query = select(Deal, Account, MEDDPICCAnalysis).join(
            Account, Deal.account_id == Account.id
        ).outerjoin(
            MEDDPICCAnalysis, Deal.id == MEDDPICCAnalysis.deal_id
        ).where(Deal.id == deal_id)
        
        result = await db.execute(query)
        row = result.first()
        
        if not row:
            raise HTTPException(status_code=404, detail="Deal not found")
        
        deal, account, meddpicc = row
        
        # Get stakeholders
        stakeholders_query = select(Stakeholder).where(Stakeholder.account_id == account.id)
        stakeholders_result = await db.execute(stakeholders_query)
        stakeholders = stakeholders_result.scalars().all()
        
        return DealResponse(
            id=deal.id,
            name=deal.name,
            description=deal.description,
            account_id=deal.account_id,
            account_name=account.name,
            stage=deal.stage,
            status=deal.status,
            amount=deal.amount,
            currency=deal.currency,
            probability=deal.probability,
            close_date=deal.close_date,
            deal_owner=deal.deal_owner,
            sales_engineer=deal.sales_engineer,
            competitive_situation=deal.competitive_situation,
            primary_competitors=deal.primary_competitors or {},
            notes=deal.notes,
            tags=deal.tags or {},
            created_at=deal.created_at,
            updated_at=deal.updated_at,
            meddpicc_analysis=_format_meddpicc_analysis(meddpicc) if meddpicc else None,
            stakeholders=[_format_stakeholder(s) for s in stakeholders]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting deal {deal_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get deal")


@router.post("/", response_model=DealResponse)
async def create_deal(
    deal_data: DealCreate,
    db: AsyncSession = Depends(get_async_db_session)
):
    """Create a new deal."""
    try:
        # Verify account exists
        account_query = select(Account).where(Account.id == deal_data.account_id)
        account_result = await db.execute(account_query)
        account = account_result.scalar_one_or_none()
        
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        # Create deal
        deal = Deal(
            name=deal_data.name,
            description=deal_data.description,
            account_id=deal_data.account_id,
            deal_type=deal_data.deal_type or "new_business",
            amount=deal_data.amount,
            currency=deal_data.currency or "USD",
            probability=deal_data.probability,
            close_date=deal_data.close_date,
            stage=deal_data.stage or "discovery",
            status=deal_data.status or "active",
            competitive_situation=deal_data.competitive_situation,
            deal_owner=deal_data.deal_owner,
            sales_engineer=deal_data.sales_engineer,
            notes=deal_data.notes,
            tags=deal_data.tags or {}
        )
        
        db.add(deal)
        await db.commit()
        await db.refresh(deal)
        
        # Return formatted response
        return DealResponse(
            id=deal.id,
            name=deal.name,
            description=deal.description,
            account_id=deal.account_id,
            account_name=account.name,
            stage=deal.stage,
            status=deal.status,
            amount=deal.amount,
            currency=deal.currency,
            probability=deal.probability,
            close_date=deal.close_date,
            deal_owner=deal.deal_owner,
            sales_engineer=deal.sales_engineer,
            competitive_situation=deal.competitive_situation,
            primary_competitors=deal.primary_competitors or {},
            notes=deal.notes,
            tags=deal.tags or {},
            created_at=deal.created_at,
            updated_at=deal.updated_at,
            meddpicc_analysis=None,
            stakeholders=[]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating deal: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create deal")


@router.get("/{deal_id}/meddpicc", response_model=MEDDPICCResponse)
async def get_deal_meddpicc(
    deal_id: str,
    db: AsyncSession = Depends(get_async_db_session)
):
    """Get MEDDPICC analysis for a specific deal."""
    try:
        # Get MEDDPICC analysis
        query = select(MEDDPICCAnalysis).where(MEDDPICCAnalysis.deal_id == deal_id)
        result = await db.execute(query)
        meddpicc = result.scalar_one_or_none()
        
        if not meddpicc:
            raise HTTPException(status_code=404, detail="MEDDPICC analysis not found")
        
        return _format_meddpicc_response(meddpicc)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting MEDDPICC for deal {deal_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get MEDDPICC analysis")


@router.post("/{deal_id}/analyze")
async def analyze_deal_transcript(
    deal_id: str,
    content: str,
    db: AsyncSession = Depends(get_async_db_session)
):
    """
    Analyze transcript content for a deal and update MEDDPICC data.
    This is the key integration point between upload and intelligence.
    """
    try:
        # Verify deal exists
        deal_query = select(Deal).where(Deal.id == deal_id)
        deal_result = await db.execute(deal_query)
        deal = deal_result.scalar_one_or_none()
        
        if not deal:
            raise HTTPException(status_code=404, detail="Deal not found")
        
        # TODO: Integrate with MEDDPICC orchestrator
        # This is where we'll call the orchestrator and save results
        
        # For now, return success
        return {"message": "Analysis started", "deal_id": deal_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing transcript for deal {deal_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to analyze transcript")


# Helper functions

def _calculate_priority(close_date: Optional[datetime], amount: Optional[float]) -> str:
    """Calculate deal priority based on close date and amount."""
    if not close_date and not amount:
        return "low"
    
    # High priority: closes within 30 days or high value
    if close_date and close_date <= datetime.now() + timedelta(days=30):
        return "high"
    if amount and amount >= 100000:
        return "high"
    
    # Medium priority: closes within 60 days or medium value
    if close_date and close_date <= datetime.now() + timedelta(days=60):
        return "medium"
    if amount and amount >= 50000:
        return "medium"
    
    return "low"


def _format_meddpicc_analysis(meddpicc: MEDDPICCAnalysis) -> Dict[str, Any]:
    """Format MEDDPICC analysis for frontend consumption."""
    if not meddpicc:
        return None
    
    return {
        "overall_score": int(meddpicc.overall_score),
        "completeness_score": int(meddpicc.completeness_score),
        "processing_status": meddpicc.processing_status,
        "last_scored_at": meddpicc.last_scored_at.isoformat() if meddpicc.last_scored_at else None,
        "components": {
            "metrics": {
                "score": int(meddpicc.metrics_score),
                "status": meddpicc.metrics_status,
                "data": meddpicc.metrics_data or {}
            },
            "economic_buyer": {
                "score": int(meddpicc.economic_buyer_score),
                "status": meddpicc.economic_buyer_status,
                "data": meddpicc.economic_buyer_data or {}
            },
            "decision_criteria": {
                "score": int(meddpicc.decision_criteria_score),
                "status": meddpicc.decision_criteria_status,
                "data": meddpicc.decision_criteria_data or {}
            },
            "decision_process": {
                "score": int(meddpicc.decision_process_score),
                "status": meddpicc.decision_process_status,
                "data": meddpicc.decision_process_data or {}
            },
            "identify_pain": {
                "score": int(meddpicc.identify_pain_score),
                "status": meddpicc.identify_pain_status,
                "data": meddpicc.identify_pain_data or {}
            },
            "champion": {
                "score": int(meddpicc.champion_score),
                "status": meddpicc.champion_status,
                "data": meddpicc.champion_data or {}
            },
            "competition": {
                "score": int(meddpicc.competition_score),
                "status": meddpicc.competition_status,
                "data": meddpicc.competition_data or {}
            }
        },
        "insights": meddpicc.key_insights or {},
        "risks": meddpicc.risk_factors or {},
        "recommendations": meddpicc.recommendations or {}
    }


def _format_meddpicc_response(meddpicc: MEDDPICCAnalysis) -> MEDDPICCResponse:
    """Format MEDDPICC analysis as response model."""
    return MEDDPICCResponse(
        deal_id=meddpicc.deal_id,
        overall_score=int(meddpicc.overall_score),
        completeness_score=int(meddpicc.completeness_score),
        processing_status=meddpicc.processing_status,
        last_scored_at=meddpicc.last_scored_at,
        components=_format_meddpicc_analysis(meddpicc)["components"],
        insights=meddpicc.key_insights or {},
        risks=meddpicc.risk_factors or {},
        recommendations=meddpicc.recommendations or {}
    )


def _format_stakeholder(stakeholder: Stakeholder) -> Dict[str, Any]:
    """Format stakeholder for frontend consumption."""
    return {
        "id": stakeholder.id,
        "name": stakeholder.full_name,
        "title": stakeholder.title,
        "email": stakeholder.email,
        "department": stakeholder.department,
        "seniority_level": stakeholder.seniority_level,
        "roles": {
            "economic_buyer": stakeholder.role_economic_buyer,
            "technical_buyer": stakeholder.role_technical_buyer,
            "champion": stakeholder.role_champion,
            "influencer": stakeholder.role_influencer,
            "user": stakeholder.role_user,
            "blocker": stakeholder.role_blocker
        },
        "influence_level": stakeholder.influence_level,
        "engagement_level": stakeholder.engagement_level,
        "last_contact_date": stakeholder.last_contact_date.isoformat() if stakeholder.last_contact_date else None
    }