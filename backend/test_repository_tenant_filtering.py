#!/usr/bin/env python3
"""
Test script for repository tenant filtering functionality.
"""

import sqlite3
from app.repositories.deal_repository import deal_repository
from app.auth.models import AuthContext
from app.database.connection import db_manager

def test_repository_tenant_filtering():
    """Test that repositories properly filter by tenant_id."""
    
    print("🧪 Repository Tenant Filtering Test")
    print("=" * 40)
    
    # Check current data in database
    conn = sqlite3.connect('asmis.db')
    cursor = conn.cursor()
    
    # Check deals data
    cursor.execute("SELECT id, name, tenant_id FROM deals")
    deals = cursor.fetchall()
    print(f"📊 Database has {len(deals)} deals:")
    for deal_id, name, tenant_id in deals:
        print(f"   {deal_id[:8]}: {name} (tenant: {tenant_id[:8]})")
    
    # Get tenant IDs
    cursor.execute("SELECT DISTINCT tenant_id FROM deals")
    tenant_ids = [row[0] for row in cursor.fetchall()]
    print(f"\n🏢 Found {len(tenant_ids)} unique tenant(s)")
    
    if not tenant_ids:
        print("❌ No tenants found - database migration may not have run")
        return
    
    # Test repository filtering
    print(f"\n🔍 Testing repository filtering:")
    
    # Create auth contexts for testing
    test_tenant_id = tenant_ids[0]
    fake_tenant_id = "00000000-0000-0000-0000-000000000000"
    
    real_auth = AuthContext(
        user_id="test-user-1",
        tenant_id=test_tenant_id,
        email="test@real-tenant.com"
    )
    
    fake_auth = AuthContext(
        user_id="test-user-2", 
        tenant_id=fake_tenant_id,
        email="test@fake-tenant.com"
    )
    
    # Initialize database connection
    db_manager.initialize()
    
    # Test with database session
    try:
        with db_manager.get_session() as session:
            # Test get_all_with_auth
            real_deals = deal_repository.get_all_with_auth(session, real_auth)
            fake_deals = deal_repository.get_all_with_auth(session, fake_auth)
            
            print(f"   Real tenant ({test_tenant_id[:8]}): {len(real_deals)} deals")
            print(f"   Fake tenant ({fake_tenant_id[:8]}): {len(fake_deals)} deals")
            
            if len(real_deals) > 0 and len(fake_deals) == 0:
                print("   ✅ Tenant filtering working correctly")
            else:
                print("   ❌ Tenant filtering may not be working")
            
            # Test get_deal_stats
            if len(real_deals) > 0:
                stats = deal_repository.get_deal_stats(session, real_auth)
                print(f"\n📈 Deal stats for real tenant:")
                print(f"   Total deals: {stats['total_deals']}")
                print(f"   Total value: ${stats['total_value']:,.2f}")
                print(f"   Avg deal size: ${stats['avg_deal_size']:,.2f}")
                print(f"   Tenant ID: {stats['tenant_id'][:8]}")
                
            # Test individual deal access
            if len(real_deals) > 0:
                first_deal = real_deals[0]
                
                # Should find deal with correct tenant
                found_deal = deal_repository.get_by_id_with_auth(session, first_deal.id, real_auth)
                not_found_deal = deal_repository.get_by_id_with_auth(session, first_deal.id, fake_auth)
                
                print(f"\n🔍 Individual deal access test:")
                print(f"   Real tenant can access deal: {'✅' if found_deal else '❌'}")
                print(f"   Fake tenant cannot access deal: {'✅' if not not_found_deal else '❌'}")
                
        print(f"\n✅ Repository tenant filtering test completed!")
        
    except Exception as e:
        print(f"❌ Error during repository test: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        conn.close()

if __name__ == "__main__":
    test_repository_tenant_filtering()