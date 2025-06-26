"""
🧪 QUALITY MODE: Smart Capture Constraints and Edge Cases Test

Tests foreign key constraints, unique constraints, and edge cases.
"""

import sys
import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.database.base import Base
from app.database.models import (
    Account, Deal, Stakeholder, MEDDPICCAnalysis
)


def test_constraints_and_edge_cases():
    """Test database constraints and edge cases."""
    print("🧪 QUALITY MODE: Testing Database Constraints and Edge Cases")
    print("=" * 70)
    
    # Create in-memory test database
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Setup: Create a valid account and deal
        account = Account(name="Test Company", account_type="prospect")
        session.add(account)
        session.commit()
        
        deal = Deal(
            account_id=account.id,
            name="Test Deal",
            stage="discovery",
            status="active"
        )
        session.add(deal)
        session.commit()
        
        # Test 1: Foreign Key Constraints
        print("✅ Test 1: Foreign Key Constraints...")
        
        try:
            # Try to create deal with non-existent account
            invalid_deal = Deal(
                account_id="non-existent-id",
                name="Invalid Deal",
                stage="discovery",
                status="active"
            )
            session.add(invalid_deal)
            session.commit()
            print("   ❌ Foreign key constraint should have failed!")
            return False
        except IntegrityError:
            print("   ✓ Foreign key constraint properly enforced")
            session.rollback()
        
        # Test 2: Unique Constraints
        print("✅ Test 2: Unique Constraints...")
        
        # Create first MEDDPICC analysis
        analysis1 = MEDDPICCAnalysis(deal_id=deal.id, overall_score=50.0)
        session.add(analysis1)
        session.commit()
        print("   ✓ First MEDDPICC analysis created")
        
        try:
            # Try to create second analysis for same deal
            analysis2 = MEDDPICCAnalysis(deal_id=deal.id, overall_score=60.0)
            session.add(analysis2)
            session.commit()
            print("   ❌ Unique constraint should have failed!")
            return False
        except IntegrityError:
            print("   ✓ Unique constraint properly enforced (one analysis per deal)")
            session.rollback()
        
        # Test 3: Required Fields
        print("✅ Test 3: Required Fields...")
        
        try:
            # Try to create account without required name
            invalid_account = Account(account_type="prospect")  # Missing name
            session.add(invalid_account)
            session.commit()
            print("   ❌ Should require account name!")
            return False
        except IntegrityError:
            print("   ✓ Required fields properly enforced")
            session.rollback()
        
        # Test 4: Stakeholder Hierarchy (Self-Reference)
        print("✅ Test 4: Stakeholder Hierarchy...")
        
        # Create CEO
        ceo = Stakeholder(
            account_id=account.id,
            first_name="Jane",
            last_name="CEO",
            title="Chief Executive Officer",
            seniority_level="c_level"
        )
        session.add(ceo)
        session.flush()  # Get ID without committing
        
        # Create VP reporting to CEO
        vp = Stakeholder(
            account_id=account.id,
            first_name="Bob", 
            last_name="VP",
            title="VP Engineering",
            seniority_level="vp",
            reports_to_stakeholder_id=ceo.id
        )
        session.add(vp)
        session.commit()
        
        # Test hierarchy navigation
        assert vp.reports_to.id == ceo.id
        assert len(ceo.direct_reports) == 1
        assert ceo.direct_reports[0].first_name == "Bob"
        print("   ✓ Stakeholder hierarchy working correctly")
        
        # Test 5: Soft Delete Behavior
        print("✅ Test 5: Soft Delete Behavior...")
        
        # Create new account for soft delete test
        soft_delete_account = Account(name="Soft Delete Test", account_type="prospect")
        session.add(soft_delete_account)
        session.commit()
        
        original_id = soft_delete_account.id
        assert soft_delete_account.is_active is True
        assert soft_delete_account.deleted_at is None
        
        # Perform soft delete
        soft_delete_account.deleted_at = datetime.now()
        soft_delete_account.is_active = False
        session.commit()
        
        # Verify soft delete
        deleted_account = session.query(Account).filter_by(id=original_id).first()
        assert deleted_account is not None  # Still exists in DB
        assert deleted_account.deleted_at is not None
        assert deleted_account.is_active is False
        print("   ✓ Soft delete working correctly")
        
        # Test 6: Timestamp Behavior
        print("✅ Test 6: Timestamp Behavior...")
        
        timestamp_account = Account(name="Timestamp Test", account_type="prospect")
        session.add(timestamp_account)
        session.commit()
        
        # Check timestamps were set
        assert timestamp_account.created_at is not None
        assert timestamp_account.updated_at is not None
        print("   ✓ Timestamps automatically set")
        
        # Test 7: JSON Field Behavior
        print("✅ Test 7: JSON Field Behavior...")
        
        json_account = Account(
            name="JSON Test",
            account_type="prospect",
            tags={"industry": "tech", "priority": "high"},
            primary_competitors={"adobe": {"status": "active"}}
        )
        session.add(json_account)
        session.commit()
        
        # Retrieve and verify JSON
        retrieved = session.query(Account).filter_by(name="JSON Test").first()
        assert retrieved.tags["industry"] == "tech"
        print("   ✓ JSON fields working correctly")
        
        # Test 8: Default Values
        print("✅ Test 8: Default Values...")
        
        default_deal = Deal(
            account_id=account.id,
            name="Default Values Test"
            # Not setting stage, status, currency - should use defaults
        )
        session.add(default_deal)
        session.commit()
        
        assert default_deal.stage == "discovery"
        assert default_deal.status == "active"
        assert default_deal.currency == "USD"
        assert default_deal.deal_type == "new_business"
        print("   ✓ Default values working correctly")
        
        # Test 9: Boolean Field Behavior
        print("✅ Test 9: Boolean Field Behavior...")
        
        stakeholder_with_roles = Stakeholder(
            account_id=account.id,
            first_name="Test",
            last_name="Stakeholder",
            role_economic_buyer=True,
            role_champion=False,
            role_influencer=True
        )
        session.add(stakeholder_with_roles)
        session.commit()
        
        # Test boolean queries
        economic_buyers = session.query(Stakeholder).filter_by(role_economic_buyer=True).all()
        assert len(economic_buyers) >= 1
        print("   ✓ Boolean fields and queries working correctly")
        
        print("\n🎉 ALL CONSTRAINT TESTS PASSED!")
        print("=" * 70)
        print("Database constraints and edge cases are working correctly!")
        
        return True
        
    except Exception as e:
        print(f"❌ CONSTRAINT TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        session.close()


if __name__ == "__main__":
    success = test_constraints_and_edge_cases()
    sys.exit(0 if success else 1)