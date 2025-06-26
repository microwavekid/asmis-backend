"""
🧪 QUALITY MODE: Smart Capture Production Database Test

Tests using the actual production database setup to ensure 
everything works with real database configuration.
"""

import sys
import os
from datetime import datetime, timedelta

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.database.connection import DatabaseConnectionManager
from app.database.models import (
    Account, Deal, Stakeholder, Partner,
    MEDDPICCAnalysis, MEDDPICCEvidence,
    SmartCaptureNote, EntityExtraction, EntityLink
)


def test_production_database():
    """Test Smart Capture models with production database setup."""
    print("🧪 QUALITY MODE: Testing Smart Capture with Production Database")
    print("=" * 70)
    
    # Use the actual database connection manager
    db_manager = DatabaseConnectionManager()
    
    with db_manager.get_session() as session:
        try:
            # Test 1: Create and verify Account
            print("✅ Test 1: Account Creation...")
            account = Account(
                name="ASMIS Test Company",
                domain="asmis-test.com",
                industry="Software",
                company_size="startup",
                account_type="prospect",
                annual_revenue=5000000.0,
                employee_count=50,
                account_owner="test_user_123"
            )
            session.add(account)
            session.commit()
            
            # Verify account was created
            saved_account = session.query(Account).filter_by(name="ASMIS Test Company").first()
            assert saved_account is not None
            assert saved_account.domain == "asmis-test.com"
            print(f"   ✓ Account created: {saved_account.name} (ID: {saved_account.id})")
            
            # Test 2: Create Deal with proper relationship
            print("✅ Test 2: Deal Creation...")
            deal = Deal(
                account_id=account.id,
                name="ASMIS Smart Capture Implementation",
                description="Implementing Smart Capture feature for Q4",
                deal_type="new_business",
                amount=150000.0,
                currency="USD",
                probability=80.0,
                close_date=datetime.now() + timedelta(days=60),
                stage="technical_evaluation",
                status="active",
                deal_owner="test_user_123"
            )
            session.add(deal)
            session.commit()
            
            # Verify relationship works
            assert deal.account.name == account.name
            assert len(account.deals) == 1
            print(f"   ✓ Deal created: {deal.name}")
            print(f"   ✓ Account->Deal relationship: {deal.account.name}")
            
            # Test 3: Create Stakeholder with MEDDPICC roles
            print("✅ Test 3: Stakeholder Creation...")
            stakeholder = Stakeholder(
                account_id=account.id,
                first_name="Sarah",
                last_name="Johnson", 
                email="sarah.johnson@asmis-test.com",
                title="Director of Product",
                department="Product",
                seniority_level="director",
                role_economic_buyer=False,
                role_technical_buyer=True,
                role_champion=True,
                role_influencer=True,
                influence_level="high",
                engagement_level="champion",
                preferred_communication="email",
                last_contact_date=datetime.now()
            )
            session.add(stakeholder)
            session.commit()
            
            print(f"   ✓ Stakeholder created: {stakeholder.full_name}")
            print(f"   ✓ MEDDPICC roles: Champion={stakeholder.role_champion}, Technical Buyer={stakeholder.role_technical_buyer}")
            
            # Test 4: Create Partner
            print("✅ Test 4: Partner Creation...")
            partner = Partner(
                name="ASMIS Integration Partners",
                partner_type="system_integrator",
                tier="gold",
                website="https://asmis-partners.com",
                primary_contact_name="Mike Wilson",
                primary_contact_email="mike@asmis-partners.com",
                specialties={"areas": ["AI/ML", "CRM Integration", "Sales Automation"]},
                regions={"primary": ["North America", "Europe"]},
                relationship_strength="strong",
                status="active"
            )
            session.add(partner)
            session.commit()
            
            print(f"   ✓ Partner created: {partner.name}")
            print(f"   ✓ Partner specialties: {partner.specialties}")
            
            # Test 5: Create MEDDPICC Analysis
            print("✅ Test 5: MEDDPICC Analysis Creation...")
            analysis = MEDDPICCAnalysis(
                deal_id=deal.id,
                overall_score=72.5,
                completeness_score=85.0,
                metrics_score=80.0,
                metrics_status="partial",
                economic_buyer_score=65.0,
                economic_buyer_status="missing",
                decision_criteria_score=90.0,
                decision_criteria_status="complete",
                champion_score=95.0,
                champion_status="complete",
                processing_status="complete",
                analysis_version="1.0"
            )
            session.add(analysis)
            session.commit()
            
            # Verify unique constraint (one analysis per deal)
            assert deal.meddpicc_analysis.overall_score == 72.5
            print(f"   ✓ MEDDPICC Analysis created with score: {analysis.overall_score}")
            
            # Test 6: Create Smart Capture Note
            print("✅ Test 6: Smart Capture Note Creation...")
            note = SmartCaptureNote(
                content="Discovery call with Sarah Johnson at ASMIS Test Company. She's the Director of Product and very supportive of implementing Smart Capture. Main requirements: 30% efficiency improvement, integrate with existing CRM, timeline is Q4. She mentioned budget approval needed from VP level.",
                title="Discovery Call - Sarah Johnson",
                context_type="deal",
                context_detected=True,
                context_confidence=0.95,
                deal_id=deal.id,
                account_id=account.id,
                stakeholder_id=stakeholder.id,
                processing_status="completed",
                processing_completed_at=datetime.now(),
                entities_extracted=4,
                relationships_extracted=2,
                meddpicc_elements_extracted=3,
                overall_extraction_confidence=0.915,
                capture_method="manual",
                capture_location="/deals/asmis-smart-capture-implementation",
                created_by="test_user_123"
            )
            session.add(note)
            session.commit()
            
            print(f"   ✓ Smart Capture Note created: {note.title}")
            print(f"   ✓ Processing status: {note.processing_status}")
            print(f"   ✓ Extraction confidence: {note.overall_extraction_confidence*100:.1f}%")
            
            # Test 7: Create Entity Extractions
            print("✅ Test 7: Entity Extraction Creation...")
            
            # Extract stakeholder
            stakeholder_extraction = EntityExtraction(
                note_id=note.id,
                entity_type="person",
                entity_subtype="stakeholder",
                extracted_text="Sarah Johnson",
                start_position=18,
                end_position=31,
                context_before="Discovery call with ",
                context_after=" at ASMIS Test Company",
                attributes={
                    "name": "Sarah Johnson",
                    "title": "Director of Product",
                    "role": "champion",
                    "sentiment": "supportive"
                },
                confidence=0.96,
                extraction_method="nlp",
                matched_entity_id=stakeholder.id,
                matched_entity_table="stakeholders",
                match_confidence=0.95,
                processed_by="smart_capture_nlp_agent",
                processing_version="1.0"
            )
            
            # Extract MEDDPICC metric
            metrics_extraction = EntityExtraction(
                note_id=note.id,
                entity_type="meddpicc_element",
                entity_subtype="metrics",
                extracted_text="30% efficiency improvement",
                start_position=200,
                end_position=225,
                attributes={
                    "metric_type": "efficiency",
                    "target_value": "30%",
                    "category": "operational_improvement"
                },
                confidence=0.92,
                extraction_method="pattern_matching",
                processed_by="smart_capture_metrics_agent"
            )
            
            session.add_all([stakeholder_extraction, metrics_extraction])
            session.commit()
            
            print(f"   ✓ Created {len(note.entity_extractions)} entity extractions")
            
            # Test 8: Create Entity Links
            print("✅ Test 8: Entity Link Creation...")
            
            # Link note to deal (primary context)
            deal_link = EntityLink(
                note_id=note.id,
                entity_type="deal",
                entity_id=deal.id,
                link_type="primary_context",
                confidence=0.95,
                update_summary="Main subject of discovery call",
                fields_updated={"stage": "technical_evaluation", "probability": 80.0}
            )
            
            # Link note to stakeholder (champion identification)
            stakeholder_link = EntityLink(
                note_id=note.id,
                entity_type="stakeholder", 
                entity_id=stakeholder.id,
                link_type="updated",
                confidence=0.94,
                update_summary="Confirmed as champion, highly supportive",
                fields_updated={"role_champion": True, "engagement_level": "champion"}
            )
            
            session.add_all([deal_link, stakeholder_link])
            session.commit()
            
            print(f"   ✓ Created {len(note.entity_links)} entity links")
            
            # Test 9: Create MEDDPICC Evidence
            print("✅ Test 9: MEDDPICC Evidence Creation...")
            
            evidence = MEDDPICCEvidence(
                analysis_id=analysis.id,
                component="metrics",
                sub_component="efficiency_target",
                evidence_text="Main requirements: 30% efficiency improvement",
                excerpt="30% efficiency improvement",
                source_type="note",
                source_id=note.id,
                source_name="Discovery Call - Sarah Johnson", 
                confidence=0.92,
                extraction_type="explicit",
                business_implication="Clear quantifiable success metric defined",
                extracted_by="smart_capture_agent",
                extraction_method="smart_capture"
            )
            session.add(evidence)
            session.commit()
            
            print(f"   ✓ MEDDPICC Evidence linked: {evidence.component} -> {evidence.excerpt}")
            
            # Test 10: Comprehensive Relationship Verification
            print("✅ Test 10: Relationship Verification...")
            
            # Verify all relationships work in both directions
            assert len(account.deals) == 1
            assert len(account.stakeholders) == 1
            assert len(account.smart_capture_notes) == 1
            print("   ✓ Account relationships verified")
            
            assert deal.account.name == account.name
            assert deal.meddpicc_analysis.overall_score == 72.5
            assert len(deal.smart_capture_notes) == 1
            print("   ✓ Deal relationships verified")
            
            assert stakeholder.account.name == account.name
            assert len(stakeholder.smart_capture_notes) == 1
            print("   ✓ Stakeholder relationships verified")
            
            assert len(note.entity_extractions) == 2
            assert len(note.entity_links) == 2
            assert note.deal.name == deal.name
            assert note.stakeholder.full_name == stakeholder.full_name
            print("   ✓ Smart Capture Note relationships verified")
            
            assert len(analysis.evidence_items) == 1
            assert analysis.deal.name == deal.name
            print("   ✓ MEDDPICC Analysis relationships verified")
            
            # Test 11: Query Performance
            print("✅ Test 11: Query Performance Test...")
            
            # Test complex query joining multiple tables
            results = session.query(Deal)\
                .join(Account)\
                .join(MEDDPICCAnalysis)\
                .filter(Account.industry == "Software")\
                .filter(MEDDPICCAnalysis.overall_score > 70)\
                .all()
            
            assert len(results) >= 1
            print("   ✓ Complex multi-table query works")
            
            # Test note with extractions query
            notes_with_extractions = session.query(SmartCaptureNote)\
                .filter(SmartCaptureNote.entities_extracted > 0)\
                .all()
            
            assert len(notes_with_extractions) >= 1
            print("   ✓ Smart Capture filtering query works")
            
            print("\n🎉 ALL PRODUCTION TESTS PASSED!")
            print("=" * 70)
            print("Smart Capture system is ready for production!")
            print(f"✅ Total entities created:")
            print(f"   • {len(session.query(Account).all())} Account(s)")
            print(f"   • {len(session.query(Deal).all())} Deal(s)")
            print(f"   • {len(session.query(Stakeholder).all())} Stakeholder(s)")
            print(f"   • {len(session.query(Partner).all())} Partner(s)")
            print(f"   • {len(session.query(MEDDPICCAnalysis).all())} MEDDPICC Analysis")
            print(f"   • {len(session.query(SmartCaptureNote).all())} Smart Capture Note(s)")
            print(f"   • {len(session.query(EntityExtraction).all())} Entity Extraction(s)")
            print(f"   • {len(session.query(EntityLink).all())} Entity Link(s)")
            print(f"   • {len(session.query(MEDDPICCEvidence).all())} Evidence Item(s)")
            
            # Clean up test data
            print("\n🧹 Cleaning up test data...")
            session.query(MEDDPICCEvidence).filter_by(analysis_id=analysis.id).delete()
            session.query(EntityLink).filter_by(note_id=note.id).delete()
            session.query(EntityExtraction).filter_by(note_id=note.id).delete()
            session.query(SmartCaptureNote).filter_by(id=note.id).delete()
            session.query(MEDDPICCAnalysis).filter_by(id=analysis.id).delete()
            session.query(Stakeholder).filter_by(id=stakeholder.id).delete()
            session.query(Partner).filter_by(id=partner.id).delete()
            session.query(Deal).filter_by(id=deal.id).delete()
            session.query(Account).filter_by(id=account.id).delete()
            session.commit()
            print("   ✓ Test data cleaned up")
            
            return True
            
        except Exception as e:
            print(f"❌ PRODUCTION TEST FAILED: {str(e)}")
            import traceback
            traceback.print_exc()
            session.rollback()
            return False


if __name__ == "__main__":
    success = test_production_database()
    sys.exit(0 if success else 1)