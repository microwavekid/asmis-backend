"""
Deal Repository for ASMIS backend with tenant isolation.
"""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

from sqlalchemy import select, and_, func
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from .tenant_repository import TenantRepository
from ..database.models import Deal, Account, Stakeholder
from ..auth.models import AuthContext

logger = logging.getLogger(__name__)


class DealRepository(TenantRepository[Deal]):
    """Repository for deal management operations with tenant isolation."""
    
    def __init__(self):
        """Initialize deal repository."""
        super().__init__(Deal)
    
    def get_deals_by_stage(
        self, 
        session: Session, 
        stage: str,
        auth: AuthContext
    ) -> List[Deal]:
        """
        Get deals by stage for authenticated tenant.
        
        Args:
            session: Database session
            stage: Deal stage to filter by
            auth: Authentication context
            
        Returns:
            List of deals in specified stage
        """
        try:
            stmt = select(Deal).where(Deal.stage == stage)
            stmt = self._add_tenant_filter(stmt, auth.tenant_id)
            stmt = stmt.order_by(Deal.updated_at.desc())
            
            result = session.execute(stmt)
            return result.scalars().all()
            
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting deals by stage {stage}: {e}")
            raise
    
    def get_deals_by_account(
        self, 
        session: Session, 
        account_id: str,
        auth: AuthContext
    ) -> List[Deal]:
        """
        Get deals for a specific account with tenant filtering.
        
        Args:
            session: Database session
            account_id: Account ID
            auth: Authentication context
            
        Returns:
            List of deals for the account
        """
        try:
            stmt = select(Deal).where(Deal.account_id == account_id)
            stmt = self._add_tenant_filter(stmt, auth.tenant_id)
            stmt = stmt.order_by(Deal.updated_at.desc())
            
            result = session.execute(stmt)
            return result.scalars().all()
            
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting deals by account {account_id}: {e}")
            raise
    
    def get_deal_stats(
        self, 
        session: Session,
        auth: AuthContext
    ) -> Dict[str, Any]:
        """
        Get deal statistics for authenticated tenant.
        
        Args:
            session: Database session
            auth: Authentication context
            
        Returns:
            Dictionary with deal statistics
        """
        try:
            # Base query with tenant filter
            base_query = select(Deal)
            base_query = self._add_tenant_filter(base_query, auth.tenant_id)
            
            # Total deals and value
            total_deals_result = session.execute(
                select(func.count(Deal.id), func.sum(Deal.amount))
                .select_from(base_query.subquery())
            )
            total_deals, total_value = total_deals_result.fetchone() or (0, 0.0)
            
            # Deals by stage
            stage_stats_result = session.execute(
                select(Deal.stage, func.count(Deal.id), func.sum(Deal.amount))
                .select_from(base_query.subquery())
                .group_by(Deal.stage)
            )
            
            deals_by_stage = {}
            for stage, count, value in stage_stats_result:
                deals_by_stage[stage] = {
                    "count": count,
                    "value": float(value or 0.0)
                }
            
            avg_deal_size = float(total_value) / total_deals if total_deals > 0 else 0.0
            
            return {
                "total_deals": total_deals,
                "total_value": float(total_value or 0.0),
                "avg_deal_size": avg_deal_size,
                "deals_by_stage": deals_by_stage,
                "tenant_id": auth.tenant_id
            }
            
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting deal stats: {e}")
            raise
    
    def search_deals(
        self, 
        session: Session, 
        query: str,
        auth: AuthContext,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Deal]:
        """
        Search deals by title/description with tenant filtering.
        
        Args:
            session: Database session
            query: Search query
            auth: Authentication context
            filters: Optional filters (stage, account_id, etc.)
            
        Returns:
            List of matching deals
        """
        try:
            conditions = [
                Deal.name.ilike(f"%{query}%") | Deal.description.ilike(f"%{query}%")
            ]
            
            # Apply additional filters
            if filters:
                if "stage" in filters:
                    conditions.append(Deal.stage == filters["stage"])
                if "account_id" in filters:
                    conditions.append(Deal.account_id == filters["account_id"])
                if "amount_min" in filters:
                    conditions.append(Deal.amount >= filters["amount_min"])
                if "amount_max" in filters:
                    conditions.append(Deal.amount <= filters["amount_max"])
            
            stmt = select(Deal).where(and_(*conditions))
            stmt = self._add_tenant_filter(stmt, auth.tenant_id)
            stmt = stmt.order_by(Deal.updated_at.desc()).limit(50)
            
            result = session.execute(stmt)
            return result.scalars().all()
            
        except SQLAlchemyError as e:
            self.logger.error(f"Error searching deals: {e}")
            raise
    
    def get_recent_deals(
        self, 
        session: Session,
        auth: AuthContext,
        limit: int = 10
    ) -> List[Deal]:
        """
        Get recently updated deals for authenticated tenant.
        
        Args:
            session: Database session
            auth: Authentication context
            limit: Number of deals to return
            
        Returns:
            List of recently updated deals
        """
        try:
            stmt = select(Deal)
            stmt = self._add_tenant_filter(stmt, auth.tenant_id)
            stmt = stmt.order_by(Deal.updated_at.desc()).limit(limit)
            
            result = session.execute(stmt)
            return result.scalars().all()
            
        except SQLAlchemyError as e:
            self.logger.error(f"Error getting recent deals: {e}")
            raise
    
    def update_deal_stage(
        self, 
        session: Session, 
        deal_id: str,
        new_stage: str,
        auth: AuthContext
    ) -> Optional[Deal]:
        """
        Update deal stage with tenant verification.
        
        Args:
            session: Database session
            deal_id: Deal ID
            new_stage: New stage value
            auth: Authentication context
            
        Returns:
            Updated deal or None if not found
        """
        try:
            return self.update_with_auth(
                session, 
                deal_id, 
                auth, 
                stage=new_stage,
                updated_at=datetime.utcnow()
            )
            
        except SQLAlchemyError as e:
            self.logger.error(f"Error updating deal stage {deal_id}: {e}")
            raise


# Repository instance
deal_repository = DealRepository()