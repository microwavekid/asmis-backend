# Project Foundation Context

## Project Vision
ASMIS (Automated Sales Meeting Intelligence System) is an AI-powered sales intelligence platform that transforms meeting conversations into actionable business insights. The system provides real-time MEDDPIC analysis, stakeholder mapping, deal risk assessment, and strategic campaign orchestration to help sales teams close deals faster through intelligent automation and strategic guidance.

## Core Architecture Philosophy
ASMIS uses a multi-agent AI system with specialized agents orchestrated by a Meta-Coordinator. The system prioritizes:
- **Multi-tenant isolation** for enterprise security
- **Dynamic AI optimization** through database-driven prompt management
- **Real-time intelligence** with sub-3-second response times
- **Modular agent architecture** for scalability and maintainability

## Technology Stack
**Backend Foundation:**
- **Runtime**: Python 3.9+ with FastAPI framework
- **Database**: PostgreSQL with Redis caching layer
- **AI/ML**: OpenAI GPT-4o, Anthropic Claude 4 family with intelligent model selection
- **Authentication**: JWT-based multi-tenant access control

**Frontend Foundation:**
- **Framework**: Next.js with TypeScript
- **Design System**: Linear-inspired UI components
- **State Management**: React hooks with context patterns

**Integration Layer:**
- **CRM**: Salesforce integration
- **Communication**: Microsoft Graph API
- **Project Management**: ClickUp integration
- **Call Intelligence**: Gong/Chorus connectors

## AI Agent Architecture
**10 Specialized Agents:**
1. Meta-Coordinator (orchestration and routing)
2. MEDDPIC Analysis Agent
3. Stakeholder Intelligence Agent
4. Action Items Agent
5. Document Analysis Agent
6. Competitive Intelligence Agent
7. Technical Requirements Agent
8. Buying Signals Agent
9. Strategic Advisor Agent
10. Risk Assessment Agent

**Coordination Pattern**: Parallel processing with intelligent result synthesis, optimized for cost-efficiency (typically 3 API calls per analysis).

## Business Context
**Target Market**: Enterprise B2B sales teams using MEDDPIC methodology
**Value Proposition**: 
- 20% improvement in deal closure rates
- 60% reduction in manual CRM updates
- Real-time sales intelligence and coaching

**Success Metrics:**
- **Adoption**: 95% daily active usage target
- **Quality**: >85% confidence scores for AI analysis
- **Performance**: <3 seconds for complete multi-agent analysis
- **Reliability**: 99.9% uptime requirement

## Technical Constraints
**Performance Requirements:**
- Response Time: <3 seconds for complete multi-agent analysis
- Token Efficiency: ±10% usage optimization target
- Latency Overhead: <2s increase from prompt centralization

**Scale Requirements:**
- Production Load: ~500 daily sales meetings
- Concurrent Analysis: Peak 50 simultaneous processes
- Multi-tenant Support: Enterprise-grade isolation

**Security & Compliance:**
- Prompt injection prevention
- Sales data encryption and protection
- Multi-tenant data isolation
- Enterprise authentication standards

## Architectural Decisions (Core)
**AD-001: Multi-Agent Orchestration**
- Rationale: Specialized intelligence with parallel processing
- Impact: Enables expert-level analysis in multiple domains simultaneously

**AD-002: Database-Driven Prompt Management**
- Rationale: Enable A/B testing, optimization, and dynamic updates
- Impact: Continuous improvement without code deployments

**AD-003: Multi-Tenant Architecture**
- Rationale: Enterprise security and data isolation requirements
- Impact: Single instance serves multiple organizations securely

**AD-004: JWT Authentication with Role-Based Access**
- Rationale: Scalable authentication for multi-tenant environment
- Impact: Granular permissions and audit trails

## Integration Philosophy
**Linear Integration**: All task tracking, progress management, and roadmap planning is handled through Linear MCP integration. This document focuses on foundational context rather than current work status.

**Memory System**: Behavioral patterns, working preferences, and discovered best practices are maintained in the `.ai/` and `.project_memory/` system for AI assistant optimization.

## Quick Start for AI Assistants
1. Read this file for project foundation and constraints
2. Use Linear MCP integration for current tasks and progress
3. Check `.project_memory/active_session.json` for immediate work context
4. Apply specialist persona from `SPECIALIST_PERSONAS.md` based on work type
5. Follow neural imprint protocols in `NEURAL_IMPRINT.json`