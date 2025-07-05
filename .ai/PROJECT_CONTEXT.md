# Project Intelligence Context

## Project Vision
ASMIS (Automated Sales Meeting Intelligence System) is an AI-powered sales intelligence platform that transforms meeting conversations into actionable business insights. The system provides real-time MEDDPIC analysis, stakeholder mapping, deal risk assessment, and strategic campaign orchestration to help sales teams close deals faster through intelligent automation and strategic guidance.

## Current State
**Active Epic**: Foundational Architecture & Database Design (ASMIS-DB-2025)
**Phase**: Week 1 of 2 - Core Schema Design
**Current Session**: Defining storage patterns and relationship models
**Blocking Issues**: Database schema design is the primary blocker for all application-level features, including the upcoming Prompt Migration.
**Next Milestone**: Finalize v1 of the core database schema by 2025-06-28.

## Architecture Overview
ASMIS uses a multi-agent AI system with 10 specialized agents orchestrated by a Meta-Coordinator. Currently migrating from hard-coded prompts to a centralized PostgreSQL database with Redis caching to enable dynamic optimization, A/B testing, and performance tracking.

**Core Components**:
- **10 AI Agents**: Meta-Coordinator, MEDDPIC Analysis, Stakeholder Intelligence, Action Items, Document Analysis, Competitive Intelligence, Technical Requirements, Buying Signals, Strategic Advisor, Risk Assessment
- **Tech Stack**: FastAPI, Python 3.9+, PostgreSQL, Redis, Next.js, TypeScript
- **AI/ML**: OpenAI GPT-4o, Anthropic Claude 4 family with intelligent model selection
- **Integrations**: Salesforce CRM, Microsoft Graph API, ClickUp, Gong/Chorus

## Quick Start for AI Assistants
1. Read this file first for project context
2. Check `.project_memory/current_epic/` for active work
3. Review `.project_memory/progress/todo_tracker.md` for immediate tasks
4. Apply specialist persona from SPECIALIST_PERSONAS.md based on work type
5. Log decisions to appropriate memory location

## Critical Context
- Migration Status: Foundational database schema is in design phase. The upcoming Prompt Migration feature will be the first to be built on this new architecture.
- Database Design: Expanded scope to full ASMIS architecture (multi-tenant, transcripts, vectors)
- ⏳ Memory System: Foundational elements of the Standardized Project Intelligence Framework are in place and being tested. Full system is still in active development.
- Performance Requirements: <2s latency increase, ±10% token usage, 99.9% uptime
- Quality Standards: ±5% confidence score variation, 85% auto-apply threshold

## Technical Constraints
- **Response Time**: <3 seconds for complete multi-agent analysis
- **AI Provider Limits**: OpenAI/Anthropic rate limits and context windows
- **Production Load**: ~500 daily sales meetings, peak 50 concurrent analyses
- **Infrastructure**: Existing PostgreSQL, Redis, FastAPI backend
- **Security**: Prompt injection prevention, sales data protection required

## Business Context
- **Users**: Enterprise B2B sales teams using MEDDPIC methodology
- **Value Prop**: 20% improvement in deal closure rates, 60% reduction in manual CRM updates
- **Success Metrics**: 95% daily active usage, >85% confidence scores
- **Strategic Impact**: Core to ASMIS 2.0 Intelligence Enhancement phase
- **Timeline Pressure**: 6-week window for complete migration

## Current Week Focus (Database Foundation)
**Completed This Session**:
- ✅ Fully integrated `StakeholderIntelligenceAgent` into the main orchestrator.
- ✅ Enhanced `test_system.py` to validate health and output of all core agents.

**Must Complete**:
- ⏳ Memory system architecture (IN PROGRESS - foundational elements complete)
- ✅ Define requirements for multi-tenancy, ownership, and data relationships.
- ⏳ Draft initial schema for core tables (prompts, transcripts, users, deals).
- ❌ Finalize v1 schema and plan for initial migrations.

**Resource Allocation**:
- 50% - Prompt inventory and agent analysis
- 30% - Template system design and implementation
- 15% - Database schema planning
- 5% - Testing framework preparation

## Feature Roadmap (Dependent on Database Foundation)
**Feature 1: Prompt Management & Migration**
   - Migrate all 10 agents from hard-coded prompts to the new database-driven system.

**Feature 2: Enhanced Intelligence & Reporting**
   - Build analytics features on top of the structured data.

## Active Decisions
- **PM-001**: Dependency-based migration order (Critical → Core → Advanced)
- **PM-002**: Memory-optimized project structure implemented
- **PM-003**: Work-stream based session organization

## Risk Items
1. **Prompt Inventory Incomplete** - Blocking template design and schema
2. **Database Migration Complexity** - Alembic migrations could delay Week 3
3. **Agent Quality Degradation** - Parallel testing infrastructure not yet ready