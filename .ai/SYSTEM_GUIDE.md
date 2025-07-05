# AI Assistant System Guide

## Quick Start Checklist
- [ ] Read `.ai/PROJECT_CONTEXT.md` for project overview
- [ ] Check `.project_memory/current_epic/EPIC_OVERVIEW.md` for current focus
- [ ] Review `.project_memory/progress/todo_tracker.md` for active tasks
- [ ] Select appropriate specialist persona from SPECIALIST_PERSONAS.md
- [ ] Load relevant patterns from `.project_memory/patterns/`

## Memory System Navigation

A visual map of the core directories:
/ (project root)
├── .ai/
│   ├── PROJECT_CONTEXT.md  (High-level vision, goals)
│   ├── SPECIALIST_PERSONAS.md (How to behave)
│   └── SYSTEM_GUIDE.md     (This file: how to use the system)
│
├── .project_memory/
│   ├── current_epic/
│   │   ├── EPIC_OVERVIEW.md
│   │   ├── DECISIONS_LOG.md
│   │   └── sessions/
│   │       └── active_session.md
│   ├── patterns/             (Reusable solutions)
│   └── intelligence/         (Long-term learnings)
│
└── track_progress/
    └── todo_tracker.md       (Immediate tasks)

### Understanding Work Context
1. **Project Level**: Start with `.ai/PROJECT_CONTEXT.md`
2. **Epic Level**: Read `.project_memory/current_epic/EPIC_OVERVIEW.md`
3. **Session Level**: Check `.project_memory/current_epic/sessions/active_session.md`
4. **Task Level**: Use `.project_memory/progress/todo_tracker.md`

### Updating Memory
- **Task Completion**: Update `.project_memory/progress/todo_tracker.md`
- **Decisions**: Log to `.project_memory/current_epic/DECISIONS_LOG.md`
- **Patterns**: Add to `.project_memory/patterns/` when reusable solutions emerge
- **Learning**: Update `.project_memory/intelligence/` with insights

## Response Patterns

### For Architecture Questions
1. Check `.project_memory/patterns/ARCHITECTURE.md`
2. Review recent decisions in `DECISIONS_LOG.md`
3. Apply ARCHITECT MODE persona
4. Suggest patterns that fit project context

### For Implementation Tasks
1. Check current task in `.project_memory/progress/todo_tracker.md`
2. Review relevant code patterns
3. Apply BUILDER MODE persona
4. Provide working code with context
5. Ensure all code adheres to standards in .cursorrules

### For Testing/Quality
1. Check `.project_memory/intelligence/PERFORMANCE.md`
2. Review test patterns and coverage
3. Apply QUALITY MODE persona
4. Suggest comprehensive test cases

## Decision Logging Format
Decision: [What was decided]
Context: [Why this came up]
Options Considered: [Alternatives evaluated]
Rationale: [Why this choice]
Impact: [System implications]
Implementation: [How to do it]
Date: [YYYY-MM-DD]

## Pattern Extraction
When you notice reusable solutions:
1. Document in `.project_memory/patterns/`
2. Tag with: `#database`, `#api`, `#testing`, etc.
3. Include: Problem → Solution → Example
4. Cross-reference in future responses

## Adaptive Communication

### Reading User Patterns
- Check `.ai/WORKING_PATTERNS.md` for communication preferences
- Note the "Technical Growth Tracking" section for mastered concepts
- Adapt explanation depth based on demonstrated understanding
- Update growth tracking when new concepts are mastered

### Adaptation Signals
- ✅ User demonstrates understanding → Increase technical depth
- ❓ User asks clarifying questions → Provide more context
- 🔄 Concept needs reinforcement → Maintain current level

## Multi-Agent Coordination

This project supports both Claude (via CLAUDE.md) and Cursor agents (via .cursorrules). Both systems:
- Read from the same memory files
- Follow the same specialist personas
- Update the same tracking system
- Build on shared patterns and decisions

### Consistency Guidelines
1. **Memory Updates**: Both agents suggest updates to the same files
2. **Pattern Recognition**: Patterns discovered by one agent benefit both
3. **Decision Logging**: All architectural decisions go to the same log
4. **Context Sharing**: Epic and project context is shared

### Agent-Specific Features
- **Claude**: Can directly read/write files, more conversational
- **Cursor**: Integrated with editor, real-time code suggestions

### Handoff Protocol
When switching between agents:
1. Ensure .project_memory/progress/todo_tracker.md is current
2. Commit any pending memory updates
3. Log all significant decisions from the session to DECISIONS_LOG.md
4. The next agent will pick up from the shared context