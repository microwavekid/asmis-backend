# ASMIS Intelligence System Guide

## Quick Start for New Users
1. **Foundation**: Read `.ai/PROJECT_CONTEXT.md` for project overview and constraints
2. **Current Work**: Use Linear MCP integration for tasks, issues, and progress
3. **Session Context**: Check `.project_memory/active_session.json` for current work
4. **Behavioral Mode**: Select persona from `.ai/SPECIALIST_PERSONAS.md`
5. **Begin Work**: Use `initiate` command to start any new session

## Neural Imprint System Overview

### Core Behavioral Control
The ASMIS system uses **neural imprinting** for consistent AI behavior across all interactions:

- **`.ai/NEURAL_IMPRINT.json`**: Master behavioral control (level: "fatal")
- **Behavioral hierarchy**: 5-level precedence system ensures consistent responses
- **Response templates**: Mandatory formats for all AI outputs
- **Pattern enforcement**: All work must reference existing patterns or create new ones

### Behavioral Hierarchy (Precedence Order)
```
Level 1: .ai/NEURAL_IMPRINT.json (HIGHEST - overrides everything)
Level 2: .project_memory/active_session.json
Level 3: .project_memory/progress/ (task tracking)  
Level 4: .project_memory/patterns/ (solution patterns)
Level 5: .ai/ and .project_memory/intelligence/ (general context)
```

## Reserved Commands

### `initiate`
**Purpose**: Start new session with smart cache optimization
**Actions**:
- Reads local task cache for immediate context (fast startup)
- Loads neural imprint and working patterns
- Updates session pointer in `active_session.json`
- Launches async Linear sync check (non-blocking)
- Provides progressive enhancement with fresh data
- Validates pattern index consistency
- Announces session start with cache status

**Performance**: <100ms startup time, cache-first with background sync
**Usage**: Type `initiate` at the start of any new work session

### `REMEMBER [context] [depth]`
**Purpose**: Neural imprinting reflection cycle (analysis only)
**Actions**:
- Analyzes pattern effectiveness and behavioral compliance
- Identifies successful patterns for strengthening  
- Generates improvement proposals with safety validation
- NO MODIFICATIONS - creates proposals for user review

**Parameters**:
- `context`: session|epic|pattern|decision|system (default: session)
- `depth`: surface|deep|meta (default: surface)

**Output**: Proposals with unique IDs for `IMPROVE` command

### `IMPROVE [proposal_id] | ALL | CANCEL`
**Purpose**: Execute approved behavioral improvements (action only)
**Actions**:
- Validates proposal exists from recent `REMEMBER` output
- Requires explicit user approval
- Creates behavioral backup before changes
- Implements approved modifications preserving imprint integrity
- Enables rollback via `REVERT` command

**Usage**: 
- `IMPROVE REM-2025-07-12-001` (specific proposal)
- `IMPROVE ALL` (all pending proposals)
- `IMPROVE CANCEL` (cancel pending)

### `sync`
**Purpose**: Force immediate Linear synchronization and conflict resolution
**Actions**:
- Performs full Linear API sync to fetch current state
- Detects and reports conflicts between local cache and Linear
- Updates local cache with fresh Linear data
- Provides conflict resolution options for divergent data
- Updates sync timestamps and cache status

**Performance**: Blocking operation, use for explicit sync needs
**Usage**: Type `sync` when cache conflicts need resolution or fresh data required

## Memory System Navigation

### File Structure Overview
```
.ai/                          # AI behavioral control
├── NEURAL_IMPRINT.json      # Master behavioral rules (CRITICAL)
├── PROJECT_CONTEXT.md       # Project foundation (stable)
├── SPECIALIST_PERSONAS.md   # AI behavioral modes
├── WORKING_PATTERNS.md      # Best practices & preferences
└── SYSTEM_GUIDE.md          # This file (navigation help)

.project_memory/             # Dynamic project intelligence
├── active_session.json     # Current work context only
├── progress/
│   └── todo_tracker.md      # Smart task cache (performance layer)
├── patterns/                # Reusable solution patterns
│   ├── IMPRINT_PATTERN_INDEX.json
│   ├── PATTERN_EVOLUTION_LOG.md
│   └── [various pattern files]
├── intelligence/            # Long-term project knowledge
├── sessions/                # Session logs (optional)
└── backups/                 # Behavioral state backups
```

### Finding Information (Hybrid Architecture)

**For Current Work (Performance Optimized)**:
1. **Fast Context**: Read `.project_memory/progress/todo_tracker.md` smart cache (immediate)
2. **Session Context**: Review `.project_memory/active_session.json` for current work
3. **Fresh Details**: Use Linear MCP when working on specific issues
4. **Related Patterns**: Look up patterns in `.project_memory/patterns/`

**Performance Tiers**:
- **Instant** (<100ms): Smart cache, session context, patterns
- **Fast** (<500ms): Project foundation, working patterns
- **Fresh** (1-3s): Linear MCP for detailed issue data

**For Project Understanding**:
1. Start with `.ai/PROJECT_CONTEXT.md` for foundation
2. Check `.ai/WORKING_PATTERNS.md` for discovered best practices
3. Review `.project_memory/intelligence/` for specific domain knowledge

**For Behavioral Guidance**:
1. Load `.ai/NEURAL_IMPRINT.json` protocols  
2. Select persona from `.ai/SPECIALIST_PERSONAS.md`
3. Apply patterns from `.project_memory/patterns/`

**Sync Strategy**:
- **Cache First**: Show immediate context from local data
- **Progressive Enhancement**: Enhance with fresh Linear data asynchronously
- **Conflict Detection**: Flag when cache and Linear diverge
- **On-Demand Fresh**: Fetch Linear details only when actively working on issues

## Pattern System

### Pattern Discovery & Management
- **Automatic Creation**: AI agents automatically identify and capture reusable patterns
- **Pattern Index**: All patterns maintained in `IMPRINT_PATTERN_INDEX.json`
- **Evolution Tracking**: Changes logged in `PATTERN_EVOLUTION_LOG.md`
- **Weight System**: Successful patterns get priority boosts via `REMEMBER`/`IMPROVE` cycle

### Pattern Application Rules
```json
{
  "mandatory": "All code generation must reference pattern_id in comments",
  "decision_logging": "All choices must log pattern application",
  "compliance_scoring": "Pattern adherence measured for effectiveness",
  "forbidden": "Code without pattern reference not allowed"
}
```

### Pattern Categories
- **Architectural**: System design patterns (database, API, auth)
- **Implementation**: Code patterns (testing, debugging, UI)
- **Behavioral**: AI response patterns (communication, decision-making)
- **Workflow**: Process patterns (session management, collaboration)

## Multi-Agent Coordination

### Agent Types & Roles
- **Claude**: Conversational assistance, file operations, strategic planning
- **Cursor**: Real-time code assistance, editor integration
- **Linear MCP**: Task tracking, issue management, roadmap planning

### Coordination Protocols
1. **Shared Memory**: All agents read/write same memory files
2. **Pattern Consistency**: All agents follow same behavioral patterns  
3. **Session Handoff**: Use `active_session.json` for context transfer
4. **Decision Logging**: Architectural decisions go to shared logs

### Handoff Checklist
When switching between AI agents:
- [ ] Update `.project_memory/active_session.json` with current context
- [ ] Update smart cache in `todo_tracker.md` with local changes
- [ ] Commit any pattern discoveries to pattern index
- [ ] Log significant decisions to appropriate memory files
- [ ] Sync with Linear if significant progress made (`sync` command)
- [ ] Flag any cache conflicts for next agent

## Performance Patterns & Hybrid Workflows

### Smart Cache Architecture

**Cache-First Pattern**:
1. Always read local cache first for immediate context
2. Show cached data with status indicators
3. Enhance with fresh data asynchronously
4. Never block for non-critical data

**Progressive Enhancement Workflow**:
```
Startup: Cache (0ms) → Background sync → Conflict detection → User notification
Work Session: Cached context → On-demand fresh details → Update cache
Session End: Local changes → Batch sync → Conflict resolution
```

### When to Use Each Layer

**Smart Cache (Instant)**:
- Session startup context
- Task prioritization and planning
- Quick status checks
- Cross-session handoffs

**Linear MCP (Fresh)**:
- Starting work on specific issues
- Detailed requirements review
- Cross-team coordination
- Status verification before commits

**Hybrid Strategy**:
- Cache for overview, fresh for details
- Progressive enhancement during active work
- Batch sync at natural boundaries
- Conflict resolution when detected

### Performance Guarantees

**Response Time Targets**:
- Session startup: <100ms (cache read)
- Context switching: <200ms (local data)
- Fresh details: <3s (Linear API)
- Conflict detection: Background, non-blocking

**Cache Coherence Strategy**:
- Sync points at session boundaries
- Async conflict detection during work
- User-guided conflict resolution
- Automatic cache expiration based on activity

### Workflow Optimization

**High-Frequency Operations** (No Linear calls):
- Task status updates
- Work planning and breakdown
- Pattern application
- Progress tracking

**Low-Frequency Operations** (Fresh Linear data):
- Issue detail fetching
- Cross-team coordination
- Final status verification
- Conflict resolution

## Tool Usage Patterns

### File Operations
- **Reading**: Use Read tool for specific files, Grep for searching content
- **Writing**: Prefer Edit over Write for existing files
- **Navigation**: Use LS for directory exploration, Glob for pattern matching

### Information Gathering
- **Project Context**: Start with PROJECT_CONTEXT.md
- **Current Tasks**: Query Linear MCP integration
- **Code Search**: Use Grep with appropriate patterns
- **Pattern Discovery**: Check IMPRINT_PATTERN_INDEX.json

### Decision Making
- **Architecture**: Log to `.project_memory/projects/current_project/DECISIONS_LOG.md`
- **Implementation**: Reference in code comments with pattern IDs
- **Patterns**: Update PATTERN_EVOLUTION_LOG.md for reusable solutions

## Error Recovery

### Common Issues
- **Pattern Not Found**: Create new pattern using PATTERN_CAPTURE_META_PATTERN
- **Unclear Requirements**: Ask specific questions, avoid freestyle solutions  
- **Context Conflicts**: Reference neural imprint and session contract for guidance
- **Missing Dependencies**: Check environment setup in WORKING_PATTERNS.md

### Rollback Procedures
- **Behavioral Changes**: Use `REVERT [backup_id]` command
- **Code Changes**: Standard git revert procedures
- **Pattern Changes**: Reference PATTERN_EVOLUTION_LOG.md for history

## System Health & Maintenance

### Regular Maintenance Tasks
- **Pattern Index Validation**: Automatic at session start
- **Behavioral Backup Creation**: Automatic before `IMPROVE` commands  
- **Evolution Log Updates**: Automatic with pattern changes
- **Session Context Updates**: Manual via `initiate` command

### Performance Monitoring
- **Pattern Effectiveness**: Tracked via `REMEMBER` cycle analysis
- **Response Template Compliance**: Measured in behavioral analysis
- **Neural Anchor Usage**: Monitored for consistency

This guide serves as the definitive reference for navigating and using the ASMIS intelligence system effectively.