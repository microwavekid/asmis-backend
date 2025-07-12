#!/usr/bin/env python3
"""
Simple CRUD Tests for Deal Management API

A standalone test script that can be run directly to test the new PUT and DELETE endpoints.
Uses stub authentication for easy testing.

Usage: python test_deals_crud_simple.py
"""

import os
import asyncio
import httpx
from datetime import datetime, timedelta
import json

# Use stub authentication for easy testing
os.environ['USE_STUB_ROUTERS'] = 'false'  # Use real endpoints
os.environ['USE_JWT_AUTH'] = 'false'      # Use stub auth

# Test configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

# Test users with stub auth tokens
TEST_USERS = {
    "alice": {
        "email": "alice@acme.com",
        "header": {"Authorization": "Bearer stub-token-alice@acme.com"},
        "tenant": "Acme Corp"
    },
    "david": {
        "email": "david@beta.com", 
        "header": {"Authorization": "Bearer stub-token-david@beta.com"},
        "tenant": "Beta Industries"
    }
}


class TestRunner:
    """Simple test runner for deal CRUD operations."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.created_deal_id = None
    
    def log_test(self, test_name: str, passed: bool, details: str = ""):
        """Log test results."""
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"\n{status} - {test_name}")
        if details:
            print(f"  Details: {details}")
        
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    async def test_create_deal(self, client: httpx.AsyncClient):
        """Test creating a new deal."""
        print("\n🧪 Testing CREATE Deal...")
        
        deal_data = {
            "name": "Test Deal Enterprise",
            "description": "Test deal for CRUD operations",
            "account_id": "550e8400-e29b-41d4-a716-446655440001",  # Test account ID
            "amount": 150000.0,
            "probability": 75.0,
            "close_date": (datetime.now() + timedelta(days=45)).isoformat(),
            "stage": "technical_evaluation",
            "deal_owner": "alice@acme.com"
        }
        
        try:
            response = await client.post(
                f"{API_BASE}/deals/",
                json=deal_data,
                headers=TEST_USERS["alice"]["header"]
            )
            
            if response.status_code == 200:
                data = response.json()
                self.created_deal_id = data.get("id")
                self.log_test(
                    "Create Deal", 
                    True, 
                    f"Created deal with ID: {self.created_deal_id}"
                )
                return self.created_deal_id
            else:
                self.log_test(
                    "Create Deal", 
                    False, 
                    f"Status {response.status_code}: {response.text}"
                )
        except Exception as e:
            self.log_test("Create Deal", False, str(e))
        
        return None
    
    async def test_get_deal(self, client: httpx.AsyncClient, deal_id: str):
        """Test getting a specific deal."""
        print("\n🧪 Testing GET Deal...")
        
        try:
            response = await client.get(
                f"{API_BASE}/deals/{deal_id}",
                headers=TEST_USERS["alice"]["header"]
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_test(
                    "Get Deal", 
                    True, 
                    f"Retrieved deal: {data['name']}"
                )
            else:
                self.log_test(
                    "Get Deal", 
                    False, 
                    f"Status {response.status_code}: {response.text}"
                )
        except Exception as e:
            self.log_test("Get Deal", False, str(e))
    
    async def test_update_deal(self, client: httpx.AsyncClient, deal_id: str):
        """Test updating a deal."""
        print("\n🧪 Testing UPDATE Deal...")
        
        update_data = {
            "name": "Updated Test Deal",
            "amount": 200000.0,
            "stage": "negotiation",
            "probability": 85.0
        }
        
        try:
            response = await client.put(
                f"{API_BASE}/deals/{deal_id}",
                json=update_data,
                headers=TEST_USERS["alice"]["header"]
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_test(
                    "Update Deal", 
                    True, 
                    f"Updated: name='{data['name']}', amount={data['amount']}"
                )
                
                # Verify partial update (other fields preserved)
                if data.get("description"):
                    print("  ✓ Partial update confirmed - description preserved")
            else:
                self.log_test(
                    "Update Deal", 
                    False, 
                    f"Status {response.status_code}: {response.text}"
                )
        except Exception as e:
            self.log_test("Update Deal", False, str(e))
    
    async def test_update_cross_tenant(self, client: httpx.AsyncClient, deal_id: str):
        """Test that cross-tenant updates are blocked."""
        print("\n🧪 Testing Cross-Tenant UPDATE Protection...")
        
        try:
            response = await client.put(
                f"{API_BASE}/deals/{deal_id}",
                json={"name": "Hacked by David"},
                headers=TEST_USERS["david"]["header"]  # Different tenant
            )
            
            if response.status_code == 404:
                self.log_test(
                    "Cross-Tenant Update Protection", 
                    True, 
                    "Correctly blocked with 404"
                )
            else:
                self.log_test(
                    "Cross-Tenant Update Protection", 
                    False, 
                    f"Expected 404, got {response.status_code}"
                )
        except Exception as e:
            self.log_test("Cross-Tenant Update Protection", False, str(e))
    
    async def test_delete_deal(self, client: httpx.AsyncClient, deal_id: str):
        """Test deleting a deal."""
        print("\n🧪 Testing DELETE Deal...")
        
        try:
            response = await client.delete(
                f"{API_BASE}/deals/{deal_id}",
                headers=TEST_USERS["alice"]["header"]
            )
            
            if response.status_code == 204:
                self.log_test(
                    "Delete Deal", 
                    True, 
                    "Successfully deleted (soft delete)"
                )
                
                # Verify the deal is marked as deleted
                verify_response = await client.get(
                    f"{API_BASE}/deals/{deal_id}",
                    headers=TEST_USERS["alice"]["header"]
                )
                if verify_response.status_code == 200:
                    data = verify_response.json()
                    if data.get("status") == "deleted":
                        print("  ✓ Soft delete confirmed - status is 'deleted'")
            else:
                self.log_test(
                    "Delete Deal", 
                    False, 
                    f"Status {response.status_code}: {response.text}"
                )
        except Exception as e:
            self.log_test("Delete Deal", False, str(e))
    
    async def test_delete_cross_tenant(self, client: httpx.AsyncClient):
        """Test that cross-tenant deletes are blocked."""
        print("\n🧪 Testing Cross-Tenant DELETE Protection...")
        
        # First create a deal as Alice
        deal_data = {
            "name": "Alice's Protected Deal",
            "account_id": "550e8400-e29b-41d4-a716-446655440001",
            "amount": 50000.0
        }
        
        try:
            # Create as Alice
            create_response = await client.post(
                f"{API_BASE}/deals/",
                json=deal_data,
                headers=TEST_USERS["alice"]["header"]
            )
            
            if create_response.status_code == 200:
                deal_id = create_response.json()["id"]
                
                # Try to delete as David
                delete_response = await client.delete(
                    f"{API_BASE}/deals/{deal_id}",
                    headers=TEST_USERS["david"]["header"]
                )
                
                if delete_response.status_code == 404:
                    self.log_test(
                        "Cross-Tenant Delete Protection", 
                        True, 
                        "Correctly blocked with 404"
                    )
                else:
                    self.log_test(
                        "Cross-Tenant Delete Protection", 
                        False, 
                        f"Expected 404, got {delete_response.status_code}"
                    )
        except Exception as e:
            self.log_test("Cross-Tenant Delete Protection", False, str(e))
    
    async def test_missing_auth(self, client: httpx.AsyncClient):
        """Test endpoints without authentication."""
        print("\n🧪 Testing Authentication Requirements...")
        
        endpoints = [
            ("PUT", f"{API_BASE}/deals/test-id", {"name": "Test"}),
            ("DELETE", f"{API_BASE}/deals/test-id", None)
        ]
        
        for method, url, data in endpoints:
            try:
                if method == "PUT":
                    response = await client.put(url, json=data)
                else:
                    response = await client.delete(url)
                
                if response.status_code == 401:
                    self.log_test(
                        f"{method} without auth", 
                        True, 
                        "Correctly requires authentication"
                    )
                else:
                    self.log_test(
                        f"{method} without auth", 
                        False, 
                        f"Expected 401, got {response.status_code}"
                    )
            except Exception as e:
                self.log_test(f"{method} without auth", False, str(e))
    
    async def run_all_tests(self):
        """Run all tests in sequence."""
        print("=" * 60)
        print("🚀 Deal Management API - CRUD Tests")
        print("=" * 60)
        print(f"Server: {BASE_URL}")
        print(f"Auth Mode: Stub Authentication")
        print("=" * 60)
        
        async with httpx.AsyncClient() as client:
            # Test authentication requirements
            await self.test_missing_auth(client)
            
            # Test CRUD operations
            deal_id = await self.test_create_deal(client)
            
            if deal_id:
                await self.test_get_deal(client, deal_id)
                await self.test_update_deal(client, deal_id)
                await self.test_update_cross_tenant(client, deal_id)
                await self.test_delete_deal(client, deal_id)
            
            # Test cross-tenant protection
            await self.test_delete_cross_tenant(client)
        
        # Summary
        print("\n" + "=" * 60)
        print(f"📊 Test Summary: {self.passed} passed, {self.failed} failed")
        print("=" * 60)
        
        return self.failed == 0


async def check_server():
    """Check if the server is running."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/docs")
            return response.status_code == 200
    except:
        return False


async def main():
    """Main test runner."""
    print("🔍 Checking if server is running...")
    
    if not await check_server():
        print("\n❌ Server is not running!")
        print("Please start the server with:")
        print("  cd backend")
        print("  uvicorn app.main:app --reload")
        return
    
    print("✅ Server is running!\n")
    
    runner = TestRunner()
    success = await runner.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️  Some tests failed. Check the details above.")


if __name__ == "__main__":
    asyncio.run(main())