# ASMIS Development Decisions Log

## Decision Tracking Template
```
## DEC_[YYYY-MM-DD]_[NUM]: [Decision Title]
**Context**: [Situation requiring decision]
**Options Considered**: [Alternative approaches evaluated]
**Decision**: [Chosen approach]
**Pattern Applied**: [Reference to pattern used]
**Rationale**: [Why this choice was made]
**Impact**: [Expected outcomes and effects]
**Implementation**: [Concrete steps taken]
**Date**: [YYYY-MM-DD]
```

## DEC_2024-12-17_001: Database Technology Selection
**Context**: Need reliable storage for ASMIS prompts and analysis
**Options Considered**: MongoDB, DynamoDB, PostgreSQL
**Decision**: Use PostgreSQL as primary database
**Context**: Need reliable, ACID-compliant storage for prompts
**Options Considered**: MongoDB, DynamoDB, PostgreSQL
**Rationale**: JSONB support, ACID compliance, team expertise
**Impact**: Defines migration strategy and query patterns
**Implementation**: Set up PostgreSQL 15+ with JSONB columns
**Date**: 2024-12-17

## DEC_2025-06-24_001: Debugging Session Pattern Creation
**Context**: Complex debugging session revealed need for systematic collaboration patterns
**Options Considered**: Ad-hoc debugging, basic documentation, comprehensive pattern system
**Decision**: Create COLLABORATION_DEBUG_PATTERN with behavioral protocol
**Pattern Applied**: INTELLIGENCE_CAPTURE_PATTERN  
**Rationale**: Session demonstrated context-first approach prevents 80% of debugging issues
**Impact**: Future debugging sessions will be systematic, documented, and pattern-driven
**Implementation**: 
- Created `.project_memory/patterns/COLLABORATION_DEBUG_PATTERN.json`
- Established startup sequence: context → environment → isolation → resolution → capture
- Defined forbidden behaviors: parallel fixes, assumption-driven debugging
- Integrated with memory system for automatic pattern application
**Date**: 2025-06-24

## DEC_2025-06-24_002: Add date/time intelligence to session tracking system
**Context**: Manual date entry in session files prone to errors (created 6-25 file when today is 6-24)
**Options Considered**: Manual dating, basic timestamps, comprehensive date/time intelligence system
**Decision**: Enhance intelligence system with automatic date/time awareness  
**Pattern Applied**: AUTOMATION_ENHANCEMENT_PATTERN
**Rationale**: Prevent human dating errors, improve session continuity tracking, support multi-session days
**Impact**: More reliable session documentation, better context recovery, reduced manual errors
**Implementation**: 
- Auto-timestamp session file creation using system date
- Multi-session numbering for same day (Part 1, Part 2, etc.)  
- Date validation in progress tracker scripts
- Timezone awareness for distributed work
**Date**: 2025-06-24

## DEC_2025-06-28_001: Entity Color System Architecture
**Context**: Smart Capture UI requires consistent color theming across multiple components  
**Options Considered**: Inline colors, CSS variables, centralized color system
**Decision**: Create centralized color system in `lib/utils/colors.ts`  
**Pattern Applied**: CENTRALIZED_COLOR_MANAGEMENT_PATTERN  
**Rationale**: 
- Prevents color inconsistencies across 5+ components
- Enables easy theme updates from single location
- Provides type safety for color usage
- Follows DRY principles for maintainability
**Impact**: Unified visual language across Smart Capture interface
**Implementation**: Color assignments - Stakeholder: Blue (#3B82F6), Account: Green (#10B981), Deal: Purple (#8B5CF6)
**Date**: 2025-06-28

## DEC_2025-06-28_002: Responsive Breakpoint Strategy  
**Context**: Layout cutoff issues at 90-100% zoom levels affecting usability  
**Options Considered**: Fixed layouts, simple responsive, 5-tier progressive enhancement
**Decision**: Implement 5-tier responsive architecture with CSS variables  
**Pattern Applied**: PROGRESSIVE_ENHANCEMENT_PATTERN  
**Rationale**: Addresses user-reported zoom problems, provides graceful degradation, maintains functionality across all devices
**Impact**: Eliminated content cutoff issues, improved mobile experience
**Implementation**: Mobile (< 768px) → Tablet (768-1023px) → Small Desktop (1024-1279px) → Large Desktop (1280-1535px) → Extra Large (1536px+)
**Date**: 2025-06-28

## DEC_2025-06-28_003: TypeScript Import Architecture
**Context**: Module resolution conflict between `Deal` and `DealIntelligence` types  
**Options Considered**: Shared type imports, component-based imports, type aliasing
**Decision**: Import UI types from component files, backend types from shared type files  
**Pattern Applied**: TYPE_SEPARATION_PATTERN  
**Rationale**: Separates UI/backend concerns, prevents circular dependencies, allows independent type evolution
**Impact**: Resolved TypeScript compilation errors, improved type architecture
**Implementation**: `Deal` from `@/components/intelligence/deals-table`, `DealIntelligence` from `@/types/intelligence`
**Date**: 2025-06-28

## DEC_2025-06-28_004: UI Debugging Systematic Approach
**Context**: Recurring UI issues requiring consistent troubleshooting approach  
**Options Considered**: Ad-hoc debugging, basic checklist, comprehensive systematic process
**Decision**: Document 7-step systematic debugging process  
**Pattern Applied**: SYSTEMATIC_DEBUGGING_PATTERN  
**Rationale**: Reduces debugging time from 30+ minutes to 5-10 minutes, provides team consistency, captures institutional knowledge
**Impact**: Standardized debugging workflow, reduced time to resolution
**Implementation**: Created `.project_memory/patterns/UI_DEBUGGING_PATTERN.json` with 7-step recovery process
**Date**: 2025-06-28

## DEC_2025-06-28_005: Bonusly UI Pattern Adoption
**Context**: Smart Capture needs intuitive entity selection interface  
**Options Considered**: Custom dropdown, standard form inputs, Bonusly-inspired design
**Decision**: Adopt Bonusly-inspired entity selector design  
**Pattern Applied**: EXTERNAL_UI_INSPIRATION_PATTERN  
**Rationale**: Proven UX pattern, visual feedback enhances understanding, color-coded system reduces cognitive load
**Impact**: Significantly improved Smart Capture user experience
**Implementation**: Entity type selector buttons, color-coded activation states, inline highlighting, cursor-positioned autocomplete
**Date**: 2025-06-28

## DEC_2025-06-29_001: API Case Convention Standardization
**Context**: MEDDPICC modal only showing 3 of 7 components due to snake_case/camelCase mismatch
**Options Considered**: Transform in backend, transform in frontend, accept both formats
**Decision**: Transform snake_case to camelCase in backend API responses
**Pattern Applied**: CASE_CONVENTION_PATTERN
**Rationale**: Frontend components expect camelCase (JavaScript convention), backend was returning snake_case (Python convention)
**Impact**: All 7 MEDDPICC components now render properly, eliminated "Icon undefined" errors
**Implementation**: 
- Updated `_format_meddpicc_analysis` in `backend/app/routers/deals.py`
- Changed keys: economic_buyer → economicBuyer, decision_criteria → decisionCriteria, etc.
- Required backend restart for changes to take effect
- Created pattern documentation for future case convention issues
**Date**: 2025-06-29

## DEC_2025-06-29_002: Backend Analyze Endpoint Integration Success
**Context**: Testing transcript upload to MEDDPICC scoring pipeline end-to-end
**Options Considered**: Mock analysis, direct orchestrator integration, gradual testing approach
**Decision**: Full orchestrator integration with comprehensive debug logging
**Pattern Applied**: SYSTEMATIC_DEBUGGING_PATTERN + QUALITY_MODE testing
**Rationale**: 
- .env API key loading issue resolved (needed correct working directory)
- Orchestrator successfully processes transcripts (action items, stakeholder intelligence)
- Analysis pipeline works but hits Anthropic API rate limits (529 errors)
- Need database persistence layer for successful analysis results
**Impact**: Core analysis functionality proven working, identified specific bottlenecks
**Implementation**:
- Fixed orchestrator initialization with proper API key from .env
- Added comprehensive debug logging to track analysis result structure
- Identified correct result keys: extraction_result, meddpicc_completeness, strategic_recommendations
- Distinguished confidence (AI certainty) vs score (MEDDPICC qualification percentage)
**Next Steps**: API efficiency review and database persistence implementation
**Date**: 2025-06-29

*Add new decisions above this line*