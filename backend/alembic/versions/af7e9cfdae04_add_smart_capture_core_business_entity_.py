"""Add Smart Capture core business entity models

Revision ID: af7e9cfdae04
Revises: d08b255a1e88
Create Date: 2025-06-25 22:05:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'af7e9cfdae04'
down_revision: Union[str, None] = 'd08b255a1e88'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create accounts table
    op.create_table('accounts',
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('domain', sa.String(length=255), nullable=True),
        sa.Column('industry', sa.String(length=100), nullable=True),
        sa.Column('company_size', sa.String(length=50), nullable=True),
        sa.Column('website', sa.String(length=500), nullable=True),
        sa.Column('headquarters', sa.String(length=255), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('account_type', sa.String(length=50), nullable=False, default='prospect'),
        sa.Column('annual_revenue', sa.Float(), nullable=True),
        sa.Column('employee_count', sa.Integer(), nullable=True),
        sa.Column('external_crm_id', sa.String(length=100), nullable=True),
        sa.Column('crm_source', sa.String(length=50), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('account_owner', sa.String(length=100), nullable=True),
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_account_name', 'accounts', ['name'])
    op.create_index('ix_account_domain', 'accounts', ['domain'])
    op.create_index('ix_account_type', 'accounts', ['account_type'])
    op.create_index('ix_account_owner', 'accounts', ['account_owner'])
    op.create_index('ix_account_industry', 'accounts', ['industry'])

    # Create partners table
    op.create_table('partners',
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('partner_type', sa.String(length=50), nullable=False),
        sa.Column('tier', sa.String(length=20), nullable=True),
        sa.Column('website', sa.String(length=500), nullable=True),
        sa.Column('primary_contact_name', sa.String(length=255), nullable=True),
        sa.Column('primary_contact_email', sa.String(length=255), nullable=True),
        sa.Column('primary_contact_phone', sa.String(length=50), nullable=True),
        sa.Column('specialties', sa.JSON(), nullable=True),
        sa.Column('regions', sa.JSON(), nullable=True),
        sa.Column('certification_level', sa.String(length=50), nullable=True),
        sa.Column('relationship_strength', sa.String(length=20), nullable=True),
        sa.Column('last_collaboration_date', sa.DateTime(), nullable=True),
        sa.Column('deals_influenced', sa.Integer(), nullable=False, default=0),
        sa.Column('total_deal_value', sa.Float(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False, default='active'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_partner_name', 'partners', ['name'])
    op.create_index('ix_partner_type', 'partners', ['partner_type'])
    op.create_index('ix_partner_tier', 'partners', ['tier'])
    op.create_index('ix_partner_status', 'partners', ['status'])

    # Create deals table
    op.create_table('deals',
        sa.Column('account_id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('deal_type', sa.String(length=50), nullable=False, default='new_business'),
        sa.Column('amount', sa.Float(), nullable=True),
        sa.Column('currency', sa.String(length=3), nullable=False, default='USD'),
        sa.Column('probability', sa.Float(), nullable=True),
        sa.Column('close_date', sa.DateTime(), nullable=True),
        sa.Column('sales_cycle_length', sa.Integer(), nullable=True),
        sa.Column('stage', sa.String(length=50), nullable=False, default='discovery'),
        sa.Column('status', sa.String(length=50), nullable=False, default='active'),
        sa.Column('competitive_situation', sa.String(length=100), nullable=True),
        sa.Column('primary_competitors', sa.JSON(), nullable=True),
        sa.Column('external_crm_id', sa.String(length=100), nullable=True),
        sa.Column('crm_source', sa.String(length=50), nullable=True),
        sa.Column('deal_owner', sa.String(length=100), nullable=True),
        sa.Column('sales_engineer', sa.String(length=100), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_deal_account', 'deals', ['account_id'])
    op.create_index('ix_deal_stage', 'deals', ['stage'])
    op.create_index('ix_deal_status', 'deals', ['status'])
    op.create_index('ix_deal_close_date', 'deals', ['close_date'])
    op.create_index('ix_deal_owner', 'deals', ['deal_owner'])
    op.create_index('ix_deal_amount', 'deals', ['amount'])

    # Create stakeholders table
    op.create_table('stakeholders',
        sa.Column('account_id', sa.String(length=36), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=False),
        sa.Column('last_name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('department', sa.String(length=100), nullable=True),
        sa.Column('seniority_level', sa.String(length=50), nullable=True),
        sa.Column('role_economic_buyer', sa.Boolean(), nullable=False, default=False),
        sa.Column('role_technical_buyer', sa.Boolean(), nullable=False, default=False),
        sa.Column('role_champion', sa.Boolean(), nullable=False, default=False),
        sa.Column('role_influencer', sa.Boolean(), nullable=False, default=False),
        sa.Column('role_user', sa.Boolean(), nullable=False, default=False),
        sa.Column('role_blocker', sa.Boolean(), nullable=False, default=False),
        sa.Column('influence_level', sa.String(length=20), nullable=True),
        sa.Column('engagement_level', sa.String(length=20), nullable=True),
        sa.Column('reports_to_stakeholder_id', sa.String(length=36), nullable=True),
        sa.Column('preferred_communication', sa.String(length=50), nullable=True),
        sa.Column('last_contact_date', sa.DateTime(), nullable=True),
        sa.Column('contact_frequency', sa.String(length=20), nullable=True),
        sa.Column('linkedin_url', sa.String(length=500), nullable=True),
        sa.Column('external_contact_id', sa.String(length=100), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id']),
        sa.ForeignKeyConstraint(['reports_to_stakeholder_id'], ['stakeholders.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_stakeholder_account', 'stakeholders', ['account_id'])
    op.create_index('ix_stakeholder_name', 'stakeholders', ['first_name', 'last_name'])
    op.create_index('ix_stakeholder_email', 'stakeholders', ['email'])
    op.create_index('ix_stakeholder_title', 'stakeholders', ['title'])
    op.create_index('ix_stakeholder_roles', 'stakeholders', ['role_economic_buyer', 'role_champion'])
    op.create_index('ix_stakeholder_reports_to', 'stakeholders', ['reports_to_stakeholder_id'])

    # Create MEDDPICC analysis table
    op.create_table('meddpicc_analyses',
        sa.Column('deal_id', sa.String(length=36), nullable=False),
        sa.Column('overall_score', sa.Float(), nullable=False, default=0.0),
        sa.Column('completeness_score', sa.Float(), nullable=False, default=0.0),
        sa.Column('last_scored_at', sa.DateTime(), nullable=True),
        sa.Column('processing_status', sa.String(length=20), nullable=False, default='idle'),
        sa.Column('processing_progress', sa.Float(), nullable=True),
        sa.Column('current_step', sa.String(length=255), nullable=True),
        sa.Column('last_error', sa.Text(), nullable=True),
        sa.Column('metrics_score', sa.Float(), nullable=False, default=0.0),
        sa.Column('economic_buyer_score', sa.Float(), nullable=False, default=0.0),
        sa.Column('decision_criteria_score', sa.Float(), nullable=False, default=0.0),
        sa.Column('decision_process_score', sa.Float(), nullable=False, default=0.0),
        sa.Column('identify_pain_score', sa.Float(), nullable=False, default=0.0),
        sa.Column('champion_score', sa.Float(), nullable=False, default=0.0),
        sa.Column('competition_score', sa.Float(), nullable=False, default=0.0),
        sa.Column('metrics_status', sa.String(length=20), nullable=False, default='missing'),
        sa.Column('economic_buyer_status', sa.String(length=20), nullable=False, default='missing'),
        sa.Column('decision_criteria_status', sa.String(length=20), nullable=False, default='missing'),
        sa.Column('decision_process_status', sa.String(length=20), nullable=False, default='missing'),
        sa.Column('identify_pain_status', sa.String(length=20), nullable=False, default='missing'),
        sa.Column('champion_status', sa.String(length=20), nullable=False, default='missing'),
        sa.Column('competition_status', sa.String(length=20), nullable=False, default='missing'),
        sa.Column('metrics_data', sa.JSON(), nullable=True),
        sa.Column('economic_buyer_data', sa.JSON(), nullable=True),
        sa.Column('decision_criteria_data', sa.JSON(), nullable=True),
        sa.Column('decision_process_data', sa.JSON(), nullable=True),
        sa.Column('identify_pain_data', sa.JSON(), nullable=True),
        sa.Column('champion_data', sa.JSON(), nullable=True),
        sa.Column('competition_data', sa.JSON(), nullable=True),
        sa.Column('key_insights', sa.JSON(), nullable=True),
        sa.Column('risk_factors', sa.JSON(), nullable=True),
        sa.Column('recommendations', sa.JSON(), nullable=True),
        sa.Column('analysis_version', sa.String(length=20), nullable=False, default='1.0'),
        sa.Column('confidence_threshold', sa.Float(), nullable=False, default=0.7),
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.ForeignKeyConstraint(['deal_id'], ['deals.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('deal_id')
    )
    op.create_index('ix_meddpicc_deal', 'meddpicc_analyses', ['deal_id'])
    op.create_index('ix_meddpicc_overall_score', 'meddpicc_analyses', ['overall_score'])
    op.create_index('ix_meddpicc_completeness', 'meddpicc_analyses', ['completeness_score'])
    op.create_index('ix_meddpicc_processing', 'meddpicc_analyses', ['processing_status'])
    op.create_index('ix_meddpicc_scored_at', 'meddpicc_analyses', ['last_scored_at'])

    # Create Smart Capture notes table
    op.create_table('smart_capture_notes',
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=True),
        sa.Column('context_type', sa.String(length=50), nullable=True),
        sa.Column('context_detected', sa.Boolean(), nullable=False, default=False),
        sa.Column('context_confidence', sa.Float(), nullable=True),
        sa.Column('account_id', sa.String(length=36), nullable=True),
        sa.Column('deal_id', sa.String(length=36), nullable=True),
        sa.Column('stakeholder_id', sa.String(length=36), nullable=True),
        sa.Column('partner_id', sa.String(length=36), nullable=True),
        sa.Column('processing_status', sa.String(length=20), nullable=False, default='pending'),
        sa.Column('processing_started_at', sa.DateTime(), nullable=True),
        sa.Column('processing_completed_at', sa.DateTime(), nullable=True),
        sa.Column('processing_error', sa.Text(), nullable=True),
        sa.Column('entities_extracted', sa.Integer(), nullable=False, default=0),
        sa.Column('relationships_extracted', sa.Integer(), nullable=False, default=0),
        sa.Column('meddpicc_elements_extracted', sa.Integer(), nullable=False, default=0),
        sa.Column('overall_extraction_confidence', sa.Float(), nullable=True),
        sa.Column('capture_method', sa.String(length=50), nullable=False, default='manual'),
        sa.Column('capture_location', sa.String(length=255), nullable=True),
        sa.Column('user_agent', sa.String(length=500), nullable=True),
        sa.Column('created_by', sa.String(length=100), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('raw_metadata', sa.JSON(), nullable=True),
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id']),
        sa.ForeignKeyConstraint(['deal_id'], ['deals.id']),
        sa.ForeignKeyConstraint(['partner_id'], ['partners.id']),
        sa.ForeignKeyConstraint(['stakeholder_id'], ['stakeholders.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_note_context', 'smart_capture_notes', ['context_type'])
    op.create_index('ix_note_processing', 'smart_capture_notes', ['processing_status'])
    op.create_index('ix_note_account', 'smart_capture_notes', ['account_id'])
    op.create_index('ix_note_deal', 'smart_capture_notes', ['deal_id'])
    op.create_index('ix_note_stakeholder', 'smart_capture_notes', ['stakeholder_id'])
    op.create_index('ix_note_partner', 'smart_capture_notes', ['partner_id'])
    op.create_index('ix_note_created_by', 'smart_capture_notes', ['created_by'])
    op.create_index('ix_note_capture_method', 'smart_capture_notes', ['capture_method'])

    # Create remaining tables
    op.create_table('entity_recognition_cache',
        sa.Column('input_text', sa.Text(), nullable=False),
        sa.Column('input_hash', sa.String(length=64), nullable=False),
        sa.Column('recognized_entities', sa.JSON(), nullable=False),
        sa.Column('cache_version', sa.String(length=20), nullable=False, default='1.0'),
        sa.Column('hit_count', sa.Integer(), nullable=False, default=0),
        sa.Column('last_hit', sa.DateTime(), nullable=True),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('input_hash')
    )
    op.create_index('ix_cache_hash', 'entity_recognition_cache', ['input_hash'])
    op.create_index('ix_cache_expires', 'entity_recognition_cache', ['expires_at'])
    op.create_index('ix_cache_version', 'entity_recognition_cache', ['cache_version'])

    # Create entity extractions table
    op.create_table('entity_extractions',
        sa.Column('note_id', sa.String(length=36), nullable=False),
        sa.Column('entity_type', sa.String(length=50), nullable=False),
        sa.Column('entity_subtype', sa.String(length=50), nullable=True),
        sa.Column('extracted_text', sa.Text(), nullable=False),
        sa.Column('start_position', sa.Integer(), nullable=False),
        sa.Column('end_position', sa.Integer(), nullable=False),
        sa.Column('context_before', sa.Text(), nullable=True),
        sa.Column('context_after', sa.Text(), nullable=True),
        sa.Column('attributes', sa.JSON(), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=False, default=0.0),
        sa.Column('extraction_method', sa.String(length=50), nullable=False),
        sa.Column('matched_entity_id', sa.String(length=100), nullable=True),
        sa.Column('matched_entity_table', sa.String(length=50), nullable=True),
        sa.Column('match_confidence', sa.Float(), nullable=True),
        sa.Column('requires_disambiguation', sa.Boolean(), nullable=False, default=False),
        sa.Column('processed_by', sa.String(length=100), nullable=False),
        sa.Column('processing_version', sa.String(length=20), nullable=False, default='1.0'),
        sa.Column('validated', sa.Boolean(), nullable=False, default=False),
        sa.Column('validated_by', sa.String(length=100), nullable=True),
        sa.Column('validated_at', sa.DateTime(), nullable=True),
        sa.Column('validation_action', sa.String(length=20), nullable=True),
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.ForeignKeyConstraint(['note_id'], ['smart_capture_notes.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_extraction_note', 'entity_extractions', ['note_id'])
    op.create_index('ix_extraction_type', 'entity_extractions', ['entity_type', 'entity_subtype'])
    op.create_index('ix_extraction_confidence', 'entity_extractions', ['confidence'])
    op.create_index('ix_extraction_matched', 'entity_extractions', ['matched_entity_id', 'matched_entity_table'])
    op.create_index('ix_extraction_requires_disambiguation', 'entity_extractions', ['requires_disambiguation'])
    op.create_index('ix_extraction_validated', 'entity_extractions', ['validated'])

    # Create MEDDPICC evidence table
    op.create_table('meddpicc_evidence',
        sa.Column('analysis_id', sa.String(length=36), nullable=False),
        sa.Column('component', sa.String(length=50), nullable=False),
        sa.Column('sub_component', sa.String(length=100), nullable=True),
        sa.Column('evidence_text', sa.Text(), nullable=False),
        sa.Column('excerpt', sa.Text(), nullable=False),
        sa.Column('source_type', sa.String(length=50), nullable=False),
        sa.Column('source_id', sa.String(length=100), nullable=False),
        sa.Column('source_name', sa.String(length=255), nullable=False),
        sa.Column('source_timestamp', sa.String(length=20), nullable=True),
        sa.Column('source_url', sa.String(length=500), nullable=True),
        sa.Column('start_position', sa.Integer(), nullable=True),
        sa.Column('end_position', sa.Integer(), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=False, default=0.0),
        sa.Column('extraction_type', sa.String(length=50), nullable=False, default='explicit'),
        sa.Column('business_implication', sa.Text(), nullable=True),
        sa.Column('extracted_by', sa.String(length=100), nullable=False),
        sa.Column('extraction_method', sa.String(length=100), nullable=True),
        sa.Column('validated_at', sa.DateTime(), nullable=True),
        sa.Column('validated_by', sa.String(length=100), nullable=True),
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.ForeignKeyConstraint(['analysis_id'], ['meddpicc_analyses.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_meddpicc_evidence_analysis_component', 'meddpicc_evidence', ['analysis_id', 'component'])
    op.create_index('ix_meddpicc_evidence_source', 'meddpicc_evidence', ['source_type', 'source_id'])
    op.create_index('ix_meddpicc_evidence_confidence', 'meddpicc_evidence', ['confidence'])
    op.create_index('ix_meddpicc_evidence_extraction', 'meddpicc_evidence', ['extraction_type'])
    op.create_index('ix_meddpicc_evidence_validated', 'meddpicc_evidence', ['validated_at'])

    # Create entity links table
    op.create_table('entity_links',
        sa.Column('note_id', sa.String(length=36), nullable=False),
        sa.Column('entity_type', sa.String(length=50), nullable=False),
        sa.Column('entity_id', sa.String(length=36), nullable=False),
        sa.Column('link_type', sa.String(length=50), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=False, default=0.0),
        sa.Column('update_summary', sa.Text(), nullable=True),
        sa.Column('fields_updated', sa.JSON(), nullable=True),
        sa.Column('created_by_extraction', sa.Boolean(), nullable=False, default=True),
        sa.Column('extraction_id', sa.String(length=36), nullable=True),
        sa.Column('validated', sa.Boolean(), nullable=False, default=False),
        sa.Column('validated_by', sa.String(length=100), nullable=True),
        sa.Column('validated_at', sa.DateTime(), nullable=True),
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.ForeignKeyConstraint(['extraction_id'], ['entity_extractions.id']),
        sa.ForeignKeyConstraint(['note_id'], ['smart_capture_notes.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('note_id', 'entity_type', 'entity_id', 'link_type', name='uq_entity_link')
    )
    op.create_index('ix_link_note', 'entity_links', ['note_id'])
    op.create_index('ix_link_entity', 'entity_links', ['entity_type', 'entity_id'])
    op.create_index('ix_link_type', 'entity_links', ['link_type'])
    op.create_index('ix_link_confidence', 'entity_links', ['confidence'])
    op.create_index('ix_link_validated', 'entity_links', ['validated'])


def downgrade() -> None:
    # Drop tables in reverse order of creation
    op.drop_table('entity_links')
    op.drop_table('meddpicc_evidence')
    op.drop_table('entity_extractions')
    op.drop_table('entity_recognition_cache')
    op.drop_table('smart_capture_notes')
    op.drop_table('meddpicc_analyses')
    op.drop_table('stakeholders')
    op.drop_table('deals')
    op.drop_table('partners')
    op.drop_table('accounts')