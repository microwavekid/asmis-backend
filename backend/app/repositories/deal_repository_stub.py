"""
Deal Repository Stub for ASMIS Multi-Tenancy Integration Testing.

TODO: This is a STUB implementation for early integration testing.
Real DealRepository will be updated in Phase 3 (MIC-69).
"""

from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from app.database.stubs import BaseRepositoryStub


# Mock deal data organized by tenant
STUB_DEALS_DATA = {
    "acme-corp": [
        {
            "id": "deal-acme-1",
            "title": "Enterprise Software License",
            "description": "Large enterprise deal for software licensing",
            "stage": "proposal",
            "value": 125000.00,
            "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
            "account_id": "account-acme-1",
            "created_at": "2025-07-01T10:00:00Z",
            "updated_at": "2025-07-10T15:30:00Z"
        },
        {
            "id": "deal-acme-2", 
            "title": "Cloud Migration Services",
            "description": "Multi-year cloud migration and consulting",
            "stage": "negotiation",
            "value": 250000.00,
            "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
            "account_id": "account-acme-2",
            "created_at": "2025-06-15T14:20:00Z",
            "updated_at": "2025-07-09T09:15:00Z"
        },
        {
            "id": "deal-acme-3",
            "title": "Support Contract Renewal", 
            "description": "Annual support contract renewal",
            "stage": "closed_won",
            "value": 45000.00,
            "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
            "account_id": "account-acme-1",
            "created_at": "2025-05-20T11:45:00Z",
            "updated_at": "2025-07-05T16:00:00Z"
        }
    ],
    "beta-industries": [
        {
            "id": "deal-beta-1",
            "title": "Manufacturing System Integration",
            "description": "ERP system integration for manufacturing",
            "stage": "discovery",
            "value": 180000.00,
            "tenant_id": "550e8400-e29b-41d4-a716-446655440002",
            "account_id": "account-beta-1",
            "created_at": "2025-07-08T09:30:00Z",
            "updated_at": "2025-07-10T14:45:00Z"
        },
        {
            "id": "deal-beta-2",
            "title": "Security Audit Services",
            "description": "Comprehensive security audit and remediation",
            "stage": "proposal", 
            "value": 75000.00,
            "tenant_id": "550e8400-e29b-41d4-a716-446655440002",
            "account_id": "account-beta-2",
            "created_at": "2025-06-28T13:15:00Z",
            "updated_at": "2025-07-09T10:30:00Z"
        }
    ],
    "gamma-solutions": [
        {
            "id": "deal-gamma-1",
            "title": "Startup Technology Package",
            "description": "Complete technology stack for startup",
            "stage": "qualification",
            "value": 35000.00,
            "tenant_id": "550e8400-e29b-41d4-a716-446655440003",
            "account_id": "account-gamma-1", 
            "created_at": "2025-07-02T16:20:00Z",
            "updated_at": "2025-07-08T11:10:00Z"
        }
    ]
}


class DealRepositoryStub(BaseRepositoryStub):
    """
    STUB: Deal repository with tenant filtering for integration testing.
    TODO: Replace with real DealRepository updates in Phase 3.
    """
    
    def __init__(self):
        super().__init__(STUB_DEALS_DATA)
    
    def get_deals_by_stage(self, session: Session, tenant_id: str, stage: str) -> List[Dict[str, Any]]:
        """
        STUB: Get deals by stage for tenant.
        TODO: Replace with real SQLAlchemy query in Phase 3.
        """
        tenant_deals = self.get_all(session, tenant_id)
        return [deal for deal in tenant_deals if deal["stage"] == stage]
    
    def get_deal_stats(self, session: Session, tenant_id: str) -> Dict[str, Any]:
        """
        STUB: Get deal statistics for tenant.
        TODO: Replace with real aggregation queries in Phase 3.
        """
        tenant_deals = self.get_all(session, tenant_id)
        
        if not tenant_deals:
            return {
                "total_deals": 0,
                "total_value": 0.0,
                "avg_deal_size": 0.0,
                "deals_by_stage": {}
            }
        
        total_value = sum(deal["value"] for deal in tenant_deals)
        deals_by_stage = {}
        
        for deal in tenant_deals:
            stage = deal["stage"]
            if stage not in deals_by_stage:
                deals_by_stage[stage] = {"count": 0, "value": 0.0}
            deals_by_stage[stage]["count"] += 1
            deals_by_stage[stage]["value"] += deal["value"]
        
        return {
            "total_deals": len(tenant_deals),
            "total_value": total_value,
            "avg_deal_size": total_value / len(tenant_deals),
            "deals_by_stage": deals_by_stage
        }


# Singleton instance for testing
deal_repository_stub = DealRepositoryStub()