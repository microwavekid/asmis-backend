"""
🧪 QUALITY MODE: Basic Smart Capture Models Test

Quick validation test to ensure our models work correctly.
"""

import sys
import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.database.base import Base
from app.database.models import (
    Account, Deal, Stakeholder, Partner,
    MEDDPICCAnalysis, MEDDPICCEvidence,
    SmartCaptureNote, EntityExtraction, EntityLink
)


def test_smart_capture_models():
    """Test basic Smart Capture model functionality."""
    print("🧪 QUALITY MODE: Testing Smart Capture Database Models")
    print("=" * 60)
    
    # Create in-memory test database
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Test 1: Create Account
        print("✅ Test 1: Creating Account...")
        account = Account(
            name="Optimizely Inc",
            domain="optimizely.com",
            industry="Technology", 
            company_size="enterprise",
            account_type="prospect",
            annual_revenue=100000000.0,
            employee_count=500
        )
        session.add(account)
        session.commit()
        print(f"   Account created: {account.name} (ID: {account.id})")
        
        # Test 2: Create Deal
        print("✅ Test 2: Creating Deal...")
        deal = Deal(
            account_id=account.id,
            name="Q4 Enterprise Implementation",
            description="Full platform implementation",
            deal_type="new_business",
            amount=250000.0,
            stage="business_evaluation",
            status="active"
        )
        session.add(deal)
        session.commit()
        print(f"   Deal created: {deal.name} (ID: {deal.id})")
        print(f"   Deal account: {deal.account.name}")
        
        # Test 3: Create Stakeholder
        print("✅ Test 3: Creating Stakeholder...")
        stakeholder = Stakeholder(
            account_id=account.id,
            first_name="John",
            last_name="Smith",
            email="john.smith@optimizely.com",
            title="VP of Engineering",
            role_economic_buyer=True,
            influence_level="high"
        )
        session.add(stakeholder)
        session.commit()
        print(f"   Stakeholder created: {stakeholder.full_name} (ID: {stakeholder.id})")
        
        # Test 4: Create MEDDPICC Analysis
        print("✅ Test 4: Creating MEDDPICC Analysis...")
        analysis = MEDDPICCAnalysis(
            deal_id=deal.id,
            overall_score=75.5,
            completeness_score=80.0,
            metrics_score=85.0,
            metrics_status="complete",
            processing_status="complete"
        )
        session.add(analysis)
        session.commit()
        print(f"   MEDDPICC Analysis created for deal: {analysis.deal.name}")
        print(f"   Overall score: {analysis.overall_score}")
        
        # Test 5: Create Smart Capture Note
        print("✅ Test 5: Creating Smart Capture Note...")
        note = SmartCaptureNote(
            content="Met with John Smith from Optimizely. He mentioned they need 25% ROI and timeline is Q4.",
            title="Discovery Call - Optimizely",
            context_type="deal",
            context_detected=True,
            context_confidence=92.5,
            deal_id=deal.id,
            account_id=account.id,
            processing_status="completed",
            entities_extracted=2,
            meddpicc_elements_extracted=1,
            capture_method="manual"
        )
        session.add(note)
        session.commit()
        print(f"   Smart Capture Note created: {note.title} (ID: {note.id})")
        print(f"   Content: {note.content[:50]}...")
        
        # Test 6: Create Entity Extraction
        print("✅ Test 6: Creating Entity Extraction...")
        extraction = EntityExtraction(
            note_id=note.id,
            entity_type="person",
            entity_subtype="stakeholder",
            extracted_text="John Smith",
            start_position=9,
            end_position=19,
            attributes={
                "name": "John Smith",
                "title": "VP of Engineering",
                "company": "Optimizely"
            },
            confidence=95.0,
            extraction_method="nlp",
            processed_by="smart_capture_service"
        )
        session.add(extraction)
        session.commit()
        print(f"   Entity Extraction created: {extraction.extracted_text}")
        print(f"   Confidence: {extraction.confidence}%")
        
        # Test 7: Create Entity Link
        print("✅ Test 7: Creating Entity Link...")
        link = EntityLink(
            note_id=note.id,
            entity_type="stakeholder",
            entity_id=stakeholder.id,
            link_type="mentioned",
            confidence=90.0,
            update_summary="Mentioned as key contact for ROI requirements"
        )
        session.add(link)
        session.commit()
        print(f"   Entity Link created: Note -> {link.entity_type}")
        print(f"   Link confidence: {link.confidence}%")
        
        # Test 8: Create MEDDPICC Evidence
        print("✅ Test 8: Creating MEDDPICC Evidence...")
        evidence = MEDDPICCEvidence(
            analysis_id=analysis.id,
            component="metrics",
            sub_component="roi_target",
            evidence_text="Customer mentioned they need 25% ROI",
            excerpt="25% ROI",
            source_type="note",
            source_id=note.id,
            source_name="Discovery Call Notes",
            confidence=95.0,
            extraction_type="explicit",
            extracted_by="smart_capture_agent"
        )
        session.add(evidence)
        session.commit()
        print(f"   MEDDPICC Evidence created for: {evidence.component}")
        print(f"   Evidence: {evidence.excerpt}")
        
        # Test 9: Verify Relationships
        print("✅ Test 9: Verifying Relationships...")
        
        # Account -> Deals relationship
        assert len(account.deals) == 1
        assert account.deals[0].name == "Q4 Enterprise Implementation"
        print(f"   ✓ Account has {len(account.deals)} deal(s)")
        
        # Account -> Stakeholders relationship  
        assert len(account.stakeholders) == 1
        assert account.stakeholders[0].full_name == "John Smith"
        print(f"   ✓ Account has {len(account.stakeholders)} stakeholder(s)")
        
        # Deal -> MEDDPICC Analysis relationship
        assert deal.meddpicc_analysis is not None
        assert deal.meddpicc_analysis.overall_score == 75.5
        print(f"   ✓ Deal has MEDDPICC analysis with score: {deal.meddpicc_analysis.overall_score}")
        
        # Note -> Extractions relationship
        assert len(note.entity_extractions) == 1
        assert note.entity_extractions[0].entity_type == "person"
        print(f"   ✓ Note has {len(note.entity_extractions)} extraction(s)")
        
        # Note -> Links relationship
        assert len(note.entity_links) == 1
        assert note.entity_links[0].entity_type == "stakeholder"
        print(f"   ✓ Note has {len(note.entity_links)} entity link(s)")
        
        # Analysis -> Evidence relationship
        assert len(analysis.evidence_items) == 1
        assert analysis.evidence_items[0].component == "metrics"
        print(f"   ✓ Analysis has {len(analysis.evidence_items)} evidence item(s)")
        
        # Test 10: Performance Check
        print("✅ Test 10: Performance Check...")
        
        # Test query performance with relationships
        deal_with_analysis = session.query(Deal).filter_by(id=deal.id).first()
        assert deal_with_analysis.meddpicc_analysis.overall_score == 75.5
        print("   ✓ Deal -> MEDDPICC query works")
        
        note_with_extractions = session.query(SmartCaptureNote).filter_by(id=note.id).first()
        assert len(note_with_extractions.entity_extractions) == 1
        print("   ✓ Note -> Extractions query works")
        
        print("\n🎉 ALL TESTS PASSED!")
        print("=" * 60)
        print("Smart Capture database models are working correctly!")
        print(f"✅ Created {len(session.query(Account).all())} account(s)")
        print(f"✅ Created {len(session.query(Deal).all())} deal(s)")
        print(f"✅ Created {len(session.query(Stakeholder).all())} stakeholder(s)")
        print(f"✅ Created {len(session.query(MEDDPICCAnalysis).all())} MEDDPICC analysis")
        print(f"✅ Created {len(session.query(SmartCaptureNote).all())} Smart Capture note(s)")
        print(f"✅ Created {len(session.query(EntityExtraction).all())} entity extraction(s)")
        print(f"✅ Created {len(session.query(EntityLink).all())} entity link(s)")
        print(f"✅ Created {len(session.query(MEDDPICCEvidence).all())} evidence item(s)")
        
        return True
        
    except Exception as e:
        print(f"❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        session.close()


if __name__ == "__main__":
    success = test_smart_capture_models()
    sys.exit(0 if success else 1)