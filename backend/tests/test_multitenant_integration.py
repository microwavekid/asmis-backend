"""
End-to-End Multi-Tenant Integration Tests

Tests complete multi-tenant flow with HTTP requests against FastAPI server.
Validates tenant isolation, authentication, and CRUD operations.
"""

import os
import pytest
import pytest_asyncio
import httpx
import asyncio
from typing import Dict, Any

# Set stub mode for testing
os.environ['USE_STUB_ROUTERS'] = 'true'

# Configure pytest-asyncio
pytestmark = pytest.mark.asyncio

# Test configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

# Test users and their auth headers
TEST_USERS = {
    "alice": {
        "email": "alice@acme.com",
        "tenant_id": "550e8400-e29b-41d4-a716-446655440001",
        "header": "Bearer stub-token-alice@acme.com",
        "expected_deals": 3
    },
    "david": {
        "email": "david@beta.com", 
        "tenant_id": "550e8400-e29b-41d4-a716-446655440002",
        "header": "Bearer stub-token-david@beta.com",
        "expected_deals": 2
    },
    "frank": {
        "email": "frank@gamma.com",
        "tenant_id": "550e8400-e29b-41d4-a716-446655440003", 
        "header": "Bearer stub-token-frank@gamma.com",
        "expected_deals": 1
    }
}


@pytest_asyncio.fixture
async def client():
    """HTTP client for API testing."""
    async with httpx.AsyncClient() as client:
        yield client


class TestAuthentication:
    """Test authentication and tenant context."""
    
    async def test_tenant_info_endpoint(self, client):
        """Test that tenant info endpoint returns correct context."""
        for user_name, user_data in TEST_USERS.items():
            response = await client.get(
                f"{API_BASE}/deals/test/tenant-info",
                headers={"Authorization": user_data["header"]}
            )
            
            assert response.status_code == 200
            data = response.json()
            
            assert data["email"] == user_data["email"]
            assert data["tenant_id"] == user_data["tenant_id"]
            assert data["message"] == "Auth context working correctly"
    
    async def test_missing_auth_header(self, client):
        """Test that missing auth header uses default user."""
        response = await client.get(f"{API_BASE}/deals/test/tenant-info")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should default to alice@acme.com
        assert data["email"] == "alice@acme.com"
        assert data["tenant_id"] == TEST_USERS["alice"]["tenant_id"]


class TestTenantIsolation:
    """Test that tenant data is properly isolated."""
    
    async def test_deal_list_isolation(self, client):
        """Test that each user only sees their tenant's deals."""
        for user_name, user_data in TEST_USERS.items():
            response = await client.get(
                f"{API_BASE}/deals/",
                headers={"Authorization": user_data["header"]}
            )
            
            assert response.status_code == 200
            deals = response.json()
            
            # Check correct number of deals
            assert len(deals) == user_data["expected_deals"], \
                f"{user_name} should see {user_data['expected_deals']} deals, got {len(deals)}"
            
            # Check all deals belong to correct tenant
            for deal in deals:
                assert deal["tenant_id"] == user_data["tenant_id"], \
                    f"Deal {deal['id']} has wrong tenant_id for {user_name}"
    
    async def test_cross_tenant_deal_access(self, client):
        """Test that users cannot access deals from other tenants."""
        # Try to access Acme deal with Beta user credentials
        acme_deal_id = "deal-acme-1"
        david_header = TEST_USERS["david"]["header"]
        
        response = await client.get(
            f"{API_BASE}/deals/{acme_deal_id}",
            headers={"Authorization": david_header}
        )
        
        # Should return 404 (not found) due to tenant filtering
        assert response.status_code == 404
        assert "Deal not found" in response.json()["detail"]
    
    async def test_stats_isolation(self, client):
        """Test that statistics are tenant-specific."""
        # Get stats for Alice (Acme Corp)
        alice_response = await client.get(
            f"{API_BASE}/deals/stats",
            headers={"Authorization": TEST_USERS["alice"]["header"]}
        )
        
        assert alice_response.status_code == 200
        alice_stats = alice_response.json()
        
        # Get stats for David (Beta Industries)
        david_response = await client.get(
            f"{API_BASE}/deals/stats",
            headers={"Authorization": TEST_USERS["david"]["header"]}
        )
        
        assert david_response.status_code == 200
        david_stats = david_response.json()
        
        # Verify stats are different and tenant-specific
        assert alice_stats["total_deals"] == 3
        assert david_stats["total_deals"] == 2
        assert alice_stats["tenant_id"] != david_stats["tenant_id"]
        assert alice_stats["total_value"] != david_stats["total_value"]


class TestCRUDOperations:
    """Test CRUD operations with tenant isolation."""
    
    async def test_create_deal(self, client):
        """Test creating deals assigns correct tenant_id."""
        new_deal = {
            "title": "Test Deal Creation",
            "description": "Integration test deal",
            "stage": "qualification",
            "value": 75000.0
        }
        
        # Create deal as Alice
        response = await client.post(
            f"{API_BASE}/deals/",
            json=new_deal,
            headers={"Authorization": TEST_USERS["alice"]["header"]}
        )
        
        assert response.status_code == 200
        created_deal = response.json()
        
        # Verify deal has correct tenant_id
        assert created_deal["tenant_id"] == TEST_USERS["alice"]["tenant_id"]
        assert created_deal["title"] == new_deal["title"]
        assert "STUB" in created_deal["message"]
    
    async def test_get_specific_deal(self, client):
        """Test getting specific deals respects tenant boundaries."""
        # Get a known Acme deal as Alice
        response = await client.get(
            f"{API_BASE}/deals/deal-acme-1",
            headers={"Authorization": TEST_USERS["alice"]["header"]}
        )
        
        assert response.status_code == 200
        deal = response.json()
        
        assert deal["id"] == "deal-acme-1"
        assert deal["tenant_id"] == TEST_USERS["alice"]["tenant_id"]
        assert "Enterprise Software License" in deal["title"]


class TestPerformance:
    """Test performance baselines for stub implementation."""
    
    async def test_response_times(self, client):
        """Test that stub responses are fast."""
        import time
        
        # Test deal list endpoint
        start_time = time.time()
        response = await client.get(
            f"{API_BASE}/deals/",
            headers={"Authorization": TEST_USERS["alice"]["header"]}
        )
        end_time = time.time()
        
        assert response.status_code == 200
        response_time = (end_time - start_time) * 1000  # Convert to ms
        
        # Should be very fast with stubs
        assert response_time < 100, f"Response time too slow: {response_time}ms"
    
    async def test_concurrent_requests(self, client):
        """Test concurrent requests from different tenants."""
        import asyncio
        
        async def make_request(user_data):
            response = await client.get(
                f"{API_BASE}/deals/",
                headers={"Authorization": user_data["header"]}
            )
            return response.status_code, len(response.json())
        
        # Make concurrent requests
        tasks = [make_request(user_data) for user_data in TEST_USERS.values()]
        results = await asyncio.gather(*tasks)
        
        # All requests should succeed
        for status_code, deal_count in results:
            assert status_code == 200
            assert deal_count > 0


class TestErrorHandling:
    """Test error handling and edge cases."""
    
    async def test_invalid_deal_id(self, client):
        """Test accessing non-existent deal."""
        response = await client.get(
            f"{API_BASE}/deals/nonexistent-deal",
            headers={"Authorization": TEST_USERS["alice"]["header"]}
        )
        
        assert response.status_code == 404
        assert "Deal not found" in response.json()["detail"]
    
    async def test_malformed_auth_header(self, client):
        """Test malformed authorization header."""
        response = await client.get(
            f"{API_BASE}/deals/test/tenant-info",
            headers={"Authorization": "Invalid Token Format"}
        )
        
        # Should fall back to default user (alice)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "alice@acme.com"


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])