"""
Test script for multi-tenant stub integration.

Usage: 
    export USE_STUB_ROUTERS=true
    python test_stub_integration.py
"""

import os
os.environ['USE_STUB_ROUTERS'] = 'true'

import asyncio
from app.auth import get_auth_context_stub
from app.routers.deals_stub import list_deals, get_deal_stats, get_deal, create_deal


class MockRequest:
    """Mock request object for testing."""
    def __init__(self, auth_header=None):
        self.headers = {"Authorization": auth_header} if auth_header else {}


async def test_multi_tenant_integration():
    """Test complete multi-tenant flow with stubs."""
    
    print("🧪 Testing Multi-Tenant Stub Integration")
    print("=" * 50)
    
    # Test 1: Alice from Acme Corp
    print("\n1️⃣ Testing Alice (Acme Corp):")
    alice_request = MockRequest("Bearer stub-token-alice@acme.com")
    alice_auth = await get_auth_context_stub(alice_request)
    print(f"   Auth: {alice_auth.email} | Tenant: {alice_auth.tenant_id}")
    
    alice_deals = await list_deals(auth=alice_auth, session=None)
    print(f"   ✅ Deals found: {len(alice_deals)}")
    for deal in alice_deals:
        print(f"      - {deal['title']}: ${deal['value']:,.2f}")
    
    # Test 2: David from Beta Industries  
    print("\n2️⃣ Testing David (Beta Industries):")
    david_request = MockRequest("Bearer stub-token-david@beta.com")
    david_auth = await get_auth_context_stub(david_request)
    print(f"   Auth: {david_auth.email} | Tenant: {david_auth.tenant_id}")
    
    david_deals = await list_deals(auth=david_auth, session=None)
    print(f"   ✅ Deals found: {len(david_deals)}")
    for deal in david_deals:
        print(f"      - {deal['title']}: ${deal['value']:,.2f}")
    
    # Test 3: Stats for each tenant
    print("\n3️⃣ Testing Deal Statistics:")
    alice_stats = await get_deal_stats(auth=alice_auth, session=None)
    david_stats = await get_deal_stats(auth=david_auth, session=None)
    
    print(f"   Acme Corp: {alice_stats['total_deals']} deals, ${alice_stats['total_value']:,.2f} total")
    print(f"   Beta Industries: {david_stats['total_deals']} deals, ${david_stats['total_value']:,.2f} total")
    
    # Test 4: Cross-tenant isolation
    print("\n4️⃣ Testing Tenant Isolation:")
    # Try to access Acme deal with Beta auth
    acme_deal_id = "deal-acme-1"
    try:
        deal = await get_deal(deal_id=acme_deal_id, auth=david_auth, session=None)
        print(f"   ❌ SECURITY ISSUE: Beta user accessed Acme deal!")
    except Exception:
        print(f"   ✅ Tenant isolation working: Beta cannot access Acme deals")
    
    # Test 5: Create new deal
    print("\n5️⃣ Testing Deal Creation:")
    new_deal_data = {
        "title": "Test Integration Deal",
        "description": "Created during stub testing",
        "stage": "qualification",
        "value": 50000.0
    }
    
    new_deal = await create_deal(deal_data=new_deal_data, auth=alice_auth, session=None)
    print(f"   ✅ Deal created: {new_deal['title']} (ID: {new_deal['id']})")
    print(f"   Tenant ID: {new_deal['tenant_id']}")
    
    print("\n" + "=" * 50)
    print("✅ Multi-tenant stub integration test complete!")


if __name__ == "__main__":
    asyncio.run(test_multi_tenant_integration())