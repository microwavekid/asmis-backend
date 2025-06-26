"""
🧪 QUALITY MODE: Comprehensive Smart Capture Database Models Test Suite

Tests all aspects of the Smart Capture system:
- Core entity models (Account, Deal, Stakeholder, Partner)
- MEDDPICC analysis integration
- Smart Capture note processing
- Entity extraction and linking
- Relationship integrity and performance
"""

import pytest
import uuid
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from app.database.base import Base
from app.database.models import (
    Account, Deal, Stakeholder, Partner,
    MEDDPICCAnalysis, MEDDPICCEvidence,
    SmartCaptureNote, EntityExtraction, EntityLink,
    EntityRecognitionCache
)


class TestSmartCaptureModels:
    """🧪 Comprehensive test suite for Smart Capture database models."""
    
    @pytest.fixture(scope="function")
    def db_session(self):
        """Create a test database session with clean state for each test."""
        # Use in-memory SQLite for fast testing
        engine = create_engine("sqlite:///:memory:", echo=False)
        Base.metadata.create_all(engine)
        
        Session = sessionmaker(bind=engine)
        session = Session()
        
        yield session
        
        session.close()
    
    @pytest.fixture
    def sample_account(self, db_session):
        """Create a sample account for testing."""
        account = Account(
            name="Optimizely Inc",
            domain="optimizely.com",
            industry="Technology",
            company_size="enterprise",
            website="https://optimizely.com",
            headquarters="San Francisco, CA",
            account_type="prospect",
            annual_revenue=100000000.0,
            employee_count=500,
            account_owner="user_123"
        )
        db_session.add(account)
        db_session.commit()
        return account
    
    @pytest.fixture
    def sample_deal(self, db_session, sample_account):
        """Create a sample deal for testing."""
        deal = Deal(
            account_id=sample_account.id,
            name="Q4 Enterprise Implementation",
            description="Full platform implementation for Q4 launch",
            deal_type="new_business",
            amount=250000.0,
            currency="USD",
            probability=75.0,
            close_date=datetime.now() + timedelta(days=90),
            stage="business_evaluation",
            status="active",
            competitive_situation="competitive",
            deal_owner="user_123",
            sales_engineer="user_456"
        )
        db_session.add(deal)
        db_session.commit()
        return deal
    
    @pytest.fixture
    def sample_stakeholder(self, db_session, sample_account):
        """Create a sample stakeholder for testing."""
        stakeholder = Stakeholder(
            account_id=sample_account.id,
            first_name="John",
            last_name="Smith",
            email="john.smith@optimizely.com",
            title="VP of Engineering",
            department="Engineering",
            seniority_level="vp",
            role_economic_buyer=True,
            role_champion=False,
            influence_level="high",
            engagement_level="supporter"
        )
        db_session.add(stakeholder)
        db_session.commit()
        return stakeholder

    # 🧪 CORE ENTITY TESTS
    
    def test_account_creation_and_validation(self, db_session):
        """Test account creation with all required and optional fields."""
        account = Account(
            name="Test Company",
            domain="test.com",
            industry="Software",
            account_type="customer",
            annual_revenue=5000000.0,
            employee_count=100
        )
        
        db_session.add(account)
        db_session.commit()
        
        # Verify creation
        assert account.id is not None
        assert account.name == "Test Company"
        assert account.created_at is not None
        assert account.is_active is True
        assert account.deleted_at is None
        
    def test_deal_account_relationship(self, db_session, sample_account):
        """Test deal-account foreign key relationship."""
        deal = Deal(
            account_id=sample_account.id,
            name="Test Deal",
            stage="discovery",
            status="active"
        )
        
        db_session.add(deal)
        db_session.commit()
        
        # Test relationship navigation
        assert deal.account.name == sample_account.name
        assert len(sample_account.deals) == 1
        assert sample_account.deals[0].name == "Test Deal"
    
    def test_stakeholder_hierarchy(self, db_session, sample_account):
        """Test stakeholder reporting relationships."""
        # Create CEO
        ceo = Stakeholder(
            account_id=sample_account.id,
            first_name="Jane",
            last_name="CEO",
            title="Chief Executive Officer",
            seniority_level="c_level"
        )
        db_session.add(ceo)
        db_session.flush()
        
        # Create VP reporting to CEO
        vp = Stakeholder(
            account_id=sample_account.id,
            first_name="Bob",
            last_name="VP",
            title="VP Engineering",
            seniority_level="vp",
            reports_to_stakeholder_id=ceo.id
        )
        db_session.add(vp)
        db_session.commit()
        
        # Test hierarchy relationships
        assert vp.reports_to.id == ceo.id
        assert len(ceo.direct_reports) == 1
        assert ceo.direct_reports[0].first_name == "Bob"
        
    def test_foreign_key_constraints(self, db_session):
        """Test that foreign key constraints are enforced."""
        # Try to create deal with non-existent account
        deal = Deal(
            account_id="non-existent-id",
            name="Invalid Deal",
            stage="discovery",
            status="active"
        )
        
        db_session.add(deal)
        
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    # 🧪 MEDDPICC ANALYSIS TESTS
    
    def test_meddpicc_analysis_creation(self, db_session, sample_deal):
        """Test MEDDPICC analysis creation and scoring."""
        analysis = MEDDPICCAnalysis(
            deal_id=sample_deal.id,
            overall_score=75.5,
            completeness_score=80.0,
            metrics_score=85.0,
            metrics_status="complete",
            economic_buyer_score=70.0,
            economic_buyer_status="partial",
            processing_status="complete"
        )
        
        db_session.add(analysis)
        db_session.commit()
        
        # Test relationship
        assert analysis.deal.name == sample_deal.name
        assert sample_deal.meddpicc_analysis.overall_score == 75.5
        
    def test_meddpicc_evidence_linking(self, db_session, sample_deal):
        """Test evidence linking to MEDDPICC components."""
        # Create analysis
        analysis = MEDDPICCAnalysis(
            deal_id=sample_deal.id,
            overall_score=60.0
        )
        db_session.add(analysis)
        db_session.flush()
        
        # Create evidence
        evidence = MEDDPICCEvidence(
            analysis_id=analysis.id,
            component="metrics",
            sub_component="roi_target",
            evidence_text="Customer wants 25% ROI within 12 months",
            excerpt="25% ROI within 12 months",
            source_type="note",
            source_id="note_123",
            source_name="Discovery Call Notes",
            confidence=95.0,
            extraction_type="explicit",
            extracted_by="smart_capture_agent"
        )
        
        db_session.add(evidence)
        db_session.commit()
        
        # Test evidence relationship
        assert len(analysis.evidence_items) == 1
        assert analysis.evidence_items[0].component == "metrics"
        assert analysis.evidence_items[0].confidence == 95.0
    
    # 🧪 SMART CAPTURE SYSTEM TESTS
    
    def test_smart_capture_note_creation(self, db_session, sample_deal, sample_account):
        """Test Smart Capture note with context detection."""
        note = SmartCaptureNote(
            content="Met with John Smith from Optimizely. He mentioned they need 25% ROI and Jim is the decision maker.",
            title="Discovery Call - Optimizely",
            context_type="deal",
            context_detected=True,
            context_confidence=92.5,
            deal_id=sample_deal.id,
            account_id=sample_account.id,
            processing_status="completed",
            entities_extracted=3,
            relationships_extracted=1,
            meddpicc_elements_extracted=2,
            overall_extraction_confidence=88.0,
            capture_method="manual",
            created_by="user_123"
        )
        
        db_session.add(note)
        db_session.commit()
        
        # Test relationships
        assert note.deal.name == sample_deal.name
        assert note.account.name == sample_account.name
        assert note.context_detected is True
        
    def test_entity_extraction_workflow(self, db_session, sample_deal):
        """Test complete entity extraction workflow."""
        # Create note
        note = SmartCaptureNote(
            content="Call with John Smith, VP Engineering at Optimizely. Mentioned ROI requirements.",
            processing_status="processing",
            deal_id=sample_deal.id
        )
        db_session.add(note)
        db_session.flush()
        
        # Create entity extraction
        extraction = EntityExtraction(
            note_id=note.id,
            entity_type="person",
            entity_subtype="stakeholder",
            extracted_text="John Smith",
            start_position=10,
            end_position=20,
            attributes={
                "name": "John Smith",
                "title": "VP Engineering",
                "company": "Optimizely"
            },
            confidence=95.0,
            extraction_method="nlp",
            matched_entity_id="stakeholder_456",
            matched_entity_table="stakeholders",
            match_confidence=88.0,
            processed_by="smart_capture_service",
            processing_version="1.0"
        )
        
        db_session.add(extraction)
        db_session.commit()
        
        # Test extraction relationship
        assert len(note.entity_extractions) == 1
        assert note.entity_extractions[0].entity_type == "person"
        assert note.entity_extractions[0].attributes["name"] == "John Smith"
    
    def test_entity_linking_multi_entity(self, db_session, sample_account, sample_deal, sample_stakeholder):
        """Test multi-entity linking from single note."""
        # Create note that mentions multiple entities
        note = SmartCaptureNote(
            content="Met with John about the Q4 deal. He's the champion and Optimizely needs 25% ROI.",
            processing_status="completed",
            entities_extracted=3
        )
        db_session.add(note)
        db_session.flush()
        
        # Link to account
        account_link = EntityLink(
            note_id=note.id,
            entity_type="account",
            entity_id=sample_account.id,
            link_type="mentioned",
            confidence=90.0,
            update_summary="Mentioned in context of ROI requirements"
        )
        
        # Link to deal
        deal_link = EntityLink(
            note_id=note.id,
            entity_type="deal",
            entity_id=sample_deal.id,
            link_type="primary_context",
            confidence=95.0,
            update_summary="Primary subject of discussion"
        )
        
        # Link to stakeholder
        stakeholder_link = EntityLink(
            note_id=note.id,
            entity_type="stakeholder",
            entity_id=sample_stakeholder.id,
            link_type="updated",
            confidence=88.0,
            update_summary="Identified as champion role",
            fields_updated={"role_champion": True}
        )
        
        db_session.add_all([account_link, deal_link, stakeholder_link])
        db_session.commit()
        
        # Test multi-entity links
        assert len(note.entity_links) == 3
        link_types = [link.entity_type for link in note.entity_links]
        assert "account" in link_types
        assert "deal" in link_types
        assert "stakeholder" in link_types
    
    def test_entity_recognition_cache(self, db_session):
        """Test entity recognition caching for performance."""
        import hashlib
        
        input_text = "John Smith Optimizely"
        input_hash = hashlib.sha256(input_text.encode()).hexdigest()
        
        cache_entry = EntityRecognitionCache(
            input_text=input_text,
            input_hash=input_hash,
            recognized_entities={
                "matches": [
                    {"type": "stakeholder", "id": "123", "name": "John Smith", "confidence": 95},
                    {"type": "account", "id": "456", "name": "Optimizely", "confidence": 90}
                ]
            },
            cache_version="1.0",
            hit_count=1,
            expires_at=datetime.now() + timedelta(hours=24)
        )
        
        db_session.add(cache_entry)
        db_session.commit()
        
        # Test cache retrieval
        cached = db_session.query(EntityRecognitionCache).filter_by(input_hash=input_hash).first()
        assert cached is not None
        assert len(cached.recognized_entities["matches"]) == 2
        assert cached.hit_count == 1
    
    # 🧪 PERFORMANCE AND CONSTRAINT TESTS
    
    def test_unique_constraints(self, db_session, sample_deal):
        """Test unique constraints are enforced."""
        # Create first MEDDPICC analysis
        analysis1 = MEDDPICCAnalysis(deal_id=sample_deal.id, overall_score=50.0)
        db_session.add(analysis1)
        db_session.commit()
        
        # Try to create second analysis for same deal (should fail)
        analysis2 = MEDDPICCAnalysis(deal_id=sample_deal.id, overall_score=60.0)
        db_session.add(analysis2)
        
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    def test_index_coverage(self, db_session):
        """Test that critical queries will use indexes efficiently."""
        # This would need actual query plan analysis, but we can test index creation
        engine = db_session.bind
        
        # Check some critical indexes exist
        result = engine.execute(text("""
            SELECT name FROM sqlite_master 
            WHERE type='index' AND name LIKE 'ix_%'
            ORDER BY name
        """))
        
        indexes = [row[0] for row in result]
        
        # Verify critical indexes
        assert "ix_deal_account" in indexes
        assert "ix_stakeholder_account" in indexes
        assert "ix_meddpicc_deal" in indexes
        assert "ix_note_processing" in indexes
        assert "ix_extraction_confidence" in indexes
    
    def test_soft_delete_behavior(self, db_session, sample_account):
        """Test soft delete functionality."""
        # Delete account (soft delete)
        sample_account.deleted_at = datetime.now()
        sample_account.is_active = False
        db_session.commit()
        
        # Verify soft delete
        assert sample_account.deleted_at is not None
        assert sample_account.is_active is False
        
        # Account still exists in database
        account = db_session.query(Account).filter_by(id=sample_account.id).first()
        assert account is not None
        assert account.deleted_at is not None
    
    # 🧪 INTEGRATION TESTS
    
    def test_complete_smart_capture_workflow(self, db_session, sample_account, sample_deal):
        """Test complete end-to-end Smart Capture workflow."""
        # 1. Create Smart Capture note
        note = SmartCaptureNote(
            content="Call with Sarah Chen, CTO at Optimizely. She mentioned John Smith reports to her and they need 30% ROI. Main competitor is Adobe.",
            title="Discovery Call - Oct 25",
            context_type="deal",
            deal_id=sample_deal.id,
            account_id=sample_account.id,
            processing_status="processing",
            capture_method="manual",
            created_by="user_123"
        )
        db_session.add(note)
        db_session.flush()
        
        # 2. Extract entities
        stakeholder_extraction = EntityExtraction(
            note_id=note.id,
            entity_type="person",
            entity_subtype="stakeholder",
            extracted_text="Sarah Chen",
            start_position=10,
            end_position=20,
            attributes={
                "name": "Sarah Chen",
                "title": "CTO",
                "seniority_level": "c_level"
            },
            confidence=92.0,
            extraction_method="nlp",
            processed_by="smart_capture_service"
        )
        
        roi_extraction = EntityExtraction(
            note_id=note.id,
            entity_type="meddpicc_element",
            entity_subtype="metrics",
            extracted_text="30% ROI",
            start_position=80,
            end_position=87,
            attributes={
                "metric_type": "roi",
                "target_value": "30%",
                "priority": "must_have"
            },
            confidence=95.0,
            extraction_method="nlp",
            processed_by="smart_capture_service"
        )
        
        db_session.add_all([stakeholder_extraction, roi_extraction])
        db_session.flush()
        
        # 3. Create MEDDPICC analysis and evidence
        analysis = MEDDPICCAnalysis(
            deal_id=sample_deal.id,
            overall_score=65.0,
            metrics_score=80.0,
            metrics_status="partial"
        )
        db_session.add(analysis)
        db_session.flush()
        
        evidence = MEDDPICCEvidence(
            analysis_id=analysis.id,
            component="metrics",
            sub_component="roi_target",
            evidence_text="30% ROI requirement mentioned by CTO",
            excerpt="30% ROI",
            source_type="note",
            source_id=note.id,
            source_name="Discovery Call - Oct 25",
            confidence=95.0,
            extraction_type="explicit",
            extracted_by="smart_capture_service",
            extraction_method="smart_capture"
        )
        db_session.add(evidence)
        
        # 4. Link entities
        deal_link = EntityLink(
            note_id=note.id,
            entity_type="deal",
            entity_id=sample_deal.id,
            link_type="updated",
            confidence=90.0,
            update_summary="MEDDPICC metrics updated with ROI requirement",
            fields_updated={"metrics_score": 80.0}
        )
        db_session.add(deal_link)
        
        # 5. Update processing status
        note.processing_status = "completed"
        note.entities_extracted = 2
        note.meddpicc_elements_extracted = 1
        note.overall_extraction_confidence = 93.5
        note.processing_completed_at = datetime.now()
        
        db_session.commit()
        
        # 6. Verify complete workflow
        assert note.processing_status == "completed"
        assert len(note.entity_extractions) == 2
        assert len(note.entity_links) == 1
        assert sample_deal.meddpicc_analysis.metrics_score == 80.0
        assert len(analysis.evidence_items) == 1
        assert evidence.source_id == note.id


def run_tests():
    """Run the test suite."""
    import sys
    
    # Run pytest programmatically
    exit_code = pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "--color=yes"
    ])
    
    if exit_code == 0:
        print("🎉 All Smart Capture database model tests passed!")
    else:
        print("❌ Some tests failed. Check output above.")
    
    return exit_code


if __name__ == "__main__":
    run_tests()