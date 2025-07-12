"""
Comprehensive CRUD Tests for Deal Management API

Tests all deal endpoints including the newly implemented PUT and DELETE operations.
Validates multi-tenant isolation, authentication, and error handling.

PATTERN_REF: RIGOROUS_STUB_BASED_TESTING_PATTERN
"""

import os
import pytest
import pytest_asyncio
import httpx
import asyncio
from typing import Dict, Any
from datetime import datetime, timedelta

# Set real routers mode for testing actual implementation
os.environ['USE_STUB_ROUTERS'] = 'false'
os.environ['USE_JWT_AUTH'] = 'true'

# Configure pytest-asyncio
pytestmark = pytest.mark.asyncio

# Test configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

# Test authentication tokens (you'll need to implement a fixture to generate these)
TEST_TOKENS = {
    "alice_acme": "test-jwt-alice-acme",
    "bob_acme": "test-jwt-bob-acme", 
    "david_beta": "test-jwt-david-beta"
}


class TestDealsCRUD:
    """Test suite for Deal Management CRUD operations."""
    
    @pytest_asyncio.fixture
    async def client(self):
        """HTTP client for API testing."""
        async with httpx.AsyncClient() as client:
            yield client
    
    @pytest_asyncio.fixture
    async def auth_headers(self):
        """Authentication headers for different users."""
        # In a real test, you'd generate actual JWT tokens
        # For now, we'll use the stub auth
        return {
            "alice_acme": {"Authorization": "Bearer stub-token-alice@acme.com"},
            "bob_acme": {"Authorization": "Bearer stub-token-bob@acme.com"},
            "david_beta": {"Authorization": "Bearer stub-token-david@beta.com"}
        }
    
    @pytest_asyncio.fixture
    async def test_deal_data(self):
        """Sample deal data for testing."""
        return {
            "name": "Test Deal Enterprise",
            "description": "Test deal for CRUD operations",
            "account_id": "550e8400-e29b-41d4-a716-446655440001",  # Acme Corp
            "amount": 150000.0,
            "currency": "USD",
            "probability": 75.0,
            "close_date": (datetime.now() + timedelta(days=45)).isoformat(),
            "stage": "technical_evaluation",
            "status": "active",
            "deal_owner": "alice@acme.com",
            "notes": "Test deal created by automated tests"
        }
    
    # ========== CREATE Tests ==========
    
    async def test_create_deal_success(self, client, auth_headers, test_deal_data):
        """Test successful deal creation."""
        response = await client.post(
            f"{API_BASE}/deals/",
            json=test_deal_data,
            headers=auth_headers["alice_acme"]
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == test_deal_data["name"]
        assert data["account_name"] == "Acme Corporation"  # Should join with account
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
        
        # Store deal ID for other tests
        return data["id"]
    
    async def test_create_deal_missing_auth(self, client, test_deal_data):
        """Test deal creation without authentication."""
        response = await client.post(
            f"{API_BASE}/deals/",
            json=test_deal_data
        )
        assert response.status_code == 401
    
    async def test_create_deal_invalid_data(self, client, auth_headers):
        """Test deal creation with invalid data."""
        invalid_data = {
            "name": "",  # Empty name should fail validation
            "account_id": "invalid-uuid"
        }
        response = await client.post(
            f"{API_BASE}/deals/",
            json=invalid_data,
            headers=auth_headers["alice_acme"]
        )
        assert response.status_code == 422  # Validation error
    
    # ========== READ Tests ==========
    
    async def test_get_deal_success(self, client, auth_headers):
        """Test getting a specific deal."""
        # First create a deal
        create_response = await client.post(
            f"{API_BASE}/deals/",
            json=await self.test_deal_data(),
            headers=auth_headers["alice_acme"]
        )
        deal_id = create_response.json()["id"]
        
        # Now get the deal
        response = await client.get(
            f"{API_BASE}/deals/{deal_id}",
            headers=auth_headers["alice_acme"]
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == deal_id
        assert "meddpicc_analysis" in data
        assert "stakeholders" in data
    
    async def test_get_deal_cross_tenant_denied(self, client, auth_headers):
        """Test that users cannot access deals from other tenants."""
        # Create deal as Alice (Acme Corp)
        create_response = await client.post(
            f"{API_BASE}/deals/",
            json=await self.test_deal_data(),
            headers=auth_headers["alice_acme"]
        )
        deal_id = create_response.json()["id"]
        
        # Try to access as David (Beta Industries)
        response = await client.get(
            f"{API_BASE}/deals/{deal_id}",
            headers=auth_headers["david_beta"]
        )
        
        assert response.status_code == 404  # Should not find deal from other tenant
    
    # ========== UPDATE Tests ==========
    
    async def test_update_deal_success(self, client, auth_headers):
        """Test successful deal update with partial data."""
        # Create a deal first
        create_response = await client.post(
            f"{API_BASE}/deals/",
            json=await self.test_deal_data(),
            headers=auth_headers["alice_acme"]
        )
        deal_id = create_response.json()["id"]
        original_name = create_response.json()["name"]
        
        # Update with partial data
        update_data = {
            "name": "Updated Test Deal",
            "amount": 200000.0,
            "stage": "negotiation"
        }
        
        response = await client.put(
            f"{API_BASE}/deals/{deal_id}",
            json=update_data,
            headers=auth_headers["alice_acme"]
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Test Deal"
        assert data["amount"] == 200000.0
        assert data["stage"] == "negotiation"
        assert data["description"] is not None  # Other fields preserved
    
    async def test_update_deal_not_found(self, client, auth_headers):
        """Test updating non-existent deal."""
        response = await client.put(
            f"{API_BASE}/deals/non-existent-id",
            json={"name": "Updated"},
            headers=auth_headers["alice_acme"]
        )
        assert response.status_code == 404
    
    async def test_update_deal_cross_tenant_denied(self, client, auth_headers):
        """Test that users cannot update deals from other tenants."""
        # Create deal as Alice
        create_response = await client.post(
            f"{API_BASE}/deals/",
            json=await self.test_deal_data(),
            headers=auth_headers["alice_acme"]
        )
        deal_id = create_response.json()["id"]
        
        # Try to update as David
        response = await client.put(
            f"{API_BASE}/deals/{deal_id}",
            json={"name": "Hacked Deal"},
            headers=auth_headers["david_beta"]
        )
        
        assert response.status_code == 404
    
    async def test_update_deal_invalid_data(self, client, auth_headers):
        """Test update with invalid data."""
        # Create deal first
        create_response = await client.post(
            f"{API_BASE}/deals/",
            json=await self.test_deal_data(),
            headers=auth_headers["alice_acme"]
        )
        deal_id = create_response.json()["id"]
        
        # Try invalid update
        response = await client.put(
            f"{API_BASE}/deals/{deal_id}",
            json={"probability": 150.0},  # Invalid: > 100
            headers=auth_headers["alice_acme"]
        )
        assert response.status_code == 422
    
    async def test_update_deal_missing_auth(self, client):
        """Test update without authentication."""
        response = await client.put(
            f"{API_BASE}/deals/some-id",
            json={"name": "Updated"}
        )
        assert response.status_code == 401
    
    # ========== DELETE Tests ==========
    
    async def test_delete_deal_success(self, client, auth_headers):
        """Test successful deal deletion (soft delete)."""
        # Create a deal first
        create_response = await client.post(
            f"{API_BASE}/deals/",
            json=await self.test_deal_data(),
            headers=auth_headers["alice_acme"]
        )
        deal_id = create_response.json()["id"]
        
        # Delete the deal
        response = await client.delete(
            f"{API_BASE}/deals/{deal_id}",
            headers=auth_headers["alice_acme"]
        )
        
        assert response.status_code == 204
        assert response.content == b''  # No content
        
        # Verify soft delete by trying to get the deal
        # (In a real implementation, deleted deals might return 404 or have status="deleted")
        get_response = await client.get(
            f"{API_BASE}/deals/{deal_id}",
            headers=auth_headers["alice_acme"]
        )
        # Depending on implementation, either 404 or status="deleted"
        if get_response.status_code == 200:
            assert get_response.json()["status"] == "deleted"
    
    async def test_delete_deal_not_found(self, client, auth_headers):
        """Test deleting non-existent deal."""
        response = await client.delete(
            f"{API_BASE}/deals/non-existent-id",
            headers=auth_headers["alice_acme"]
        )
        assert response.status_code == 404
    
    async def test_delete_deal_cross_tenant_denied(self, client, auth_headers):
        """Test that users cannot delete deals from other tenants."""
        # Create deal as Alice
        create_response = await client.post(
            f"{API_BASE}/deals/",
            json=await self.test_deal_data(),
            headers=auth_headers["alice_acme"]
        )
        deal_id = create_response.json()["id"]
        
        # Try to delete as David
        response = await client.delete(
            f"{API_BASE}/deals/{deal_id}",
            headers=auth_headers["david_beta"]
        )
        
        assert response.status_code == 404
    
    async def test_delete_deal_missing_auth(self, client):
        """Test delete without authentication."""
        response = await client.delete(f"{API_BASE}/deals/some-id")
        assert response.status_code == 401
    
    # ========== End-to-End CRUD Flow Test ==========
    
    async def test_full_crud_lifecycle(self, client, auth_headers):
        """Test complete CRUD lifecycle: Create → Read → Update → Delete → Verify."""
        # 1. CREATE
        deal_data = await self.test_deal_data()
        create_response = await client.post(
            f"{API_BASE}/deals/",
            json=deal_data,
            headers=auth_headers["alice_acme"]
        )
        assert create_response.status_code == 200
        deal_id = create_response.json()["id"]
        
        # 2. READ
        read_response = await client.get(
            f"{API_BASE}/deals/{deal_id}",
            headers=auth_headers["alice_acme"]
        )
        assert read_response.status_code == 200
        assert read_response.json()["name"] == deal_data["name"]
        
        # 3. UPDATE
        update_response = await client.put(
            f"{API_BASE}/deals/{deal_id}",
            json={"name": "Updated Deal", "amount": 300000.0},
            headers=auth_headers["alice_acme"]
        )
        assert update_response.status_code == 200
        assert update_response.json()["name"] == "Updated Deal"
        assert update_response.json()["amount"] == 300000.0
        
        # 4. DELETE
        delete_response = await client.delete(
            f"{API_BASE}/deals/{deal_id}",
            headers=auth_headers["alice_acme"]
        )
        assert delete_response.status_code == 204
        
        # 5. VERIFY
        verify_response = await client.get(
            f"{API_BASE}/deals/{deal_id}",
            headers=auth_headers["alice_acme"]
        )
        # Either 404 or status="deleted" depending on implementation
        if verify_response.status_code == 200:
            assert verify_response.json()["status"] == "deleted"
    
    # ========== Performance Test ==========
    
    async def test_update_performance(self, client, auth_headers):
        """Test that updates complete within performance requirements (<200ms)."""
        import time
        
        # Create a deal
        create_response = await client.post(
            f"{API_BASE}/deals/",
            json=await self.test_deal_data(),
            headers=auth_headers["alice_acme"]
        )
        deal_id = create_response.json()["id"]
        
        # Measure update time
        start_time = time.time()
        response = await client.put(
            f"{API_BASE}/deals/{deal_id}",
            json={"name": "Performance Test Deal"},
            headers=auth_headers["alice_acme"]
        )
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 0.2  # Less than 200ms


# ========== Helper Functions ==========

async def run_tests_with_server():
    """Run tests against a running FastAPI server."""
    print("Make sure the FastAPI server is running on http://localhost:8000")
    print("You can start it with: uvicorn app.main:app --reload")
    
    # Run pytest programmatically
    pytest.main([__file__, "-v", "--asyncio-mode=auto"])


if __name__ == "__main__":
    # For manual testing
    asyncio.run(run_tests_with_server())