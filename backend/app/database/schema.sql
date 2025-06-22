-- ASMIS Database Schema
-- Generated for PostgreSQL with SQLAlchemy async support

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Prompt Templates Table
-- Stores reusable prompt templates for AI agents
CREATE TABLE prompt_templates (
    id VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    content TEXT NOT NULL,
    agent_type VARCHAR(100) NOT NULL,
    version VARCHAR(50) NOT NULL DEFAULT '1.0.0',
    metadata JSONB DEFAULT '{}',
    variables JSONB DEFAULT '{}',
    usage_count INTEGER NOT NULL DEFAULT 0,
    avg_confidence_score FLOAT,
    is_active BOOLEAN NOT NULL DEFAULT true,
    deleted_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    
    CONSTRAINT uq_template_name_agent UNIQUE (name, agent_type)
);

-- Indexes for prompt_templates
CREATE INDEX ix_template_agent_type ON prompt_templates(agent_type);
CREATE INDEX ix_template_active ON prompt_templates(is_active);
CREATE INDEX ix_template_usage ON prompt_templates(usage_count);

-- Prompt Versions Table
-- Tracks versions of prompt templates with change history
CREATE TABLE prompt_versions (
    id VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    template_id VARCHAR(36) NOT NULL REFERENCES prompt_templates(id) ON DELETE CASCADE,
    version VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    change_notes TEXT,
    is_current BOOLEAN NOT NULL DEFAULT false,
    created_by VARCHAR(255),
    usage_count INTEGER NOT NULL DEFAULT 0,
    avg_confidence_score FLOAT,
    success_rate FLOAT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    
    CONSTRAINT uq_version_template_version UNIQUE (template_id, version)
);

-- Indexes for prompt_versions
CREATE INDEX ix_version_template_id ON prompt_versions(template_id);
CREATE INDEX ix_version_current ON prompt_versions(is_current);
CREATE INDEX ix_version_usage ON prompt_versions(usage_count);

-- Agent Configurations Table
-- Stores agent-specific configuration settings
CREATE TABLE agent_configurations (
    id VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    agent_type VARCHAR(100) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    config_data JSONB NOT NULL DEFAULT '{}',
    environment VARCHAR(50) NOT NULL DEFAULT 'production',
    is_default BOOLEAN NOT NULL DEFAULT false,
    is_active BOOLEAN NOT NULL DEFAULT true,
    deleted_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    
    CONSTRAINT uq_agent_config UNIQUE (agent_type, name, environment)
);

-- Indexes for agent_configurations
CREATE INDEX ix_config_agent_type ON agent_configurations(agent_type);
CREATE INDEX ix_config_environment ON agent_configurations(environment);
CREATE INDEX ix_config_default ON agent_configurations(is_default);

-- Processing Sessions Table
-- Tracks AI processing sessions and results for monitoring and analytics
CREATE TABLE processing_sessions (
    id VARCHAR(36) PRIMARY KEY DEFAULT gen_random_uuid()::text,
    session_type VARCHAR(100) NOT NULL,
    source_type VARCHAR(100) NOT NULL,
    source_id VARCHAR(255),
    agent_type VARCHAR(100) NOT NULL,
    prompt_template_id VARCHAR(36) REFERENCES prompt_templates(id),
    input_data JSONB NOT NULL,
    output_data JSONB,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    confidence_score FLOAT,
    processing_time_ms INTEGER,
    token_usage INTEGER,
    error_message TEXT,
    retry_count INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Indexes for processing_sessions
CREATE INDEX ix_session_type ON processing_sessions(session_type);
CREATE INDEX ix_session_agent_type ON processing_sessions(agent_type);
CREATE INDEX ix_session_status ON processing_sessions(status);
CREATE INDEX ix_session_created_at ON processing_sessions(created_at);
CREATE INDEX ix_session_source ON processing_sessions(source_type, source_id);

-- Triggers for automatic updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_prompt_templates_updated_at BEFORE UPDATE ON prompt_templates
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_prompt_versions_updated_at BEFORE UPDATE ON prompt_versions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_agent_configurations_updated_at BEFORE UPDATE ON agent_configurations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_processing_sessions_updated_at BEFORE UPDATE ON processing_sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Sample data for development (optional)
-- INSERT INTO prompt_templates (name, agent_type, content, description) VALUES
-- ('Default MEDDPIC Analysis', 'meddpic', 'Analyze the following content for MEDDPIC framework elements...', 'Standard MEDDPIC analysis prompt'),
-- ('Stakeholder Intelligence', 'stakeholder', 'Extract stakeholder information from the following content...', 'Stakeholder analysis prompt');

-- Views for common queries
CREATE VIEW active_prompt_templates AS
SELECT * FROM prompt_templates 
WHERE is_active = true AND deleted_at IS NULL;

CREATE VIEW current_prompt_versions AS
SELECT pv.*, pt.name as template_name, pt.agent_type
FROM prompt_versions pv
JOIN prompt_templates pt ON pv.template_id = pt.id
WHERE pv.is_current = true AND pt.is_active = true;

-- Performance monitoring view
CREATE VIEW session_performance_summary AS
SELECT 
    agent_type,
    session_type,
    COUNT(*) as total_sessions,
    AVG(confidence_score) as avg_confidence,
    AVG(processing_time_ms) as avg_processing_time,
    COUNT(CASE WHEN status = 'completed' THEN 1 END) as successful_sessions,
    COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed_sessions
FROM processing_sessions
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY agent_type, session_type
ORDER BY total_sessions DESC;