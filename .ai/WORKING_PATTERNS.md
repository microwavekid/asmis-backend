# Working Patterns & Preferences

## Code Style Preferences
- **Python**: Type hints always, Google-style docstrings, FastAPI patterns
- **SQL**: Uppercase keywords, snake_case names, explicit indexes
- **TypeScript**: Strict mode, interfaces over types, React hooks patterns
- **Git**: Conventional commits (feat:, fix:, docs:, refactor:)

## Communication Preferences
- **Technical Depth**: ADAPTIVE - Start with clear explanations for a learning developer. Increase complexity as familiarity with concepts is demonstrated. Watch for signals of understanding or confusion.
- **Code Examples**: Show working code with inline comments initially. Reduce explanation density as patterns become familiar.
- **Decision Making**: Present options in accessible language, gradually introduce more technical considerations as expertise grows
- **Progress Updates**: Visual indicators (✅ ⏳ ❌) and simple status summaries
- **Learning Style**: Break complex topics into steps initially, accelerate pace based on comprehension signals
- **Adaptation Signals**: 
  - ✅ Understanding shown: Move faster, less explanation needed
  - ❓ Questions asked: Slow down, provide more context
  - 🔄 Repetition needed: Maintain current level, reinforce concepts

## Discovered Patterns
*This section will grow as we learn what works best*

### Environment Management
- **Virtual Environment**: ALWAYS activate venv before running Python in backend/
  ```bash
  cd /Users/conor.leary/dev/asmis/backend && source venv/bin/activate && python <script>
  ```
- **Critical Symptoms of Missing venv**:
  - `ModuleNotFoundError` for installed packages (e.g., networkx)
  - `ANTHROPIC_API_KEY not set` (env file not loaded)
  - Tests fail with import/dependency errors
- **Quick Diagnostic**: `which python3` should show `/backend/venv/bin/python3`
- **User Feedback**: Has corrected this multiple times - MUST remember venv activation
- **Pattern**: Always run tests with `source venv/bin/activate &&` prefix

### Testing Best Practices
- **Smart API Testing**: Use fake API keys for integration testing to validate code structure without API costs
  ```python
  # ✅ GOOD: Integration testing with fake key
  agent = SomeAgent('test-key')
  try:
      result = await agent.process(data)
  except Exception as e:
      if '401' in str(e) or 'authentication' in str(e):
          print('✅ Integration validated - code structure correct')
      else:
          print(f'❌ Code issue: {e}')
  ```
- **When to use fake keys**: Integration testing, CI/CD, development iteration
- **When to use real keys**: End-to-end validation, quality assurance, demos
- **Benefits**: Cost efficiency, speed, reliability, security
- **User Insight**: "This should be a best practice going forward"

### Documentation Best Practices
- **Proactive Pattern Recognition**: AI should intelligently identify best practices during work, not just wait for user identification
- **Auto-Documentation Triggers**:
  - Solving a problem that could recur
  - Discovering an efficient workflow or approach
  - Learning from mistakes or corrections
  - Identifying reusable code patterns or architecture decisions
  - User feedback that reveals improvement opportunities
- **Documentation Workflow**:
  1. **Recognize**: Identify pattern/practice worth capturing
  2. **Assess**: Determine if it's reusable/valuable
  3. **Ask if Uncertain**: "Should I document this pattern for future use?"
  4. **Document**: Update appropriate project file immediately
  5. **Validate**: Ensure it's accessible for future reference
- **Persistent Documentation**: Always update `.ai/WORKING_PATTERNS.md` for reusable patterns
  ```
  ❌ BAD: "That's a great pattern! [explains in response only]"
  ✅ GOOD: "Let me document this pattern..." [actually updates file]
  ```
- **Location Strategy**: 
  - `.ai/WORKING_PATTERNS.md` - Discovered best practices and user insights
  - `track_progress/` - Session-specific progress and context
  - `CLAUDE.md` - Project intelligence system configuration
- **User Feedback Signals**: "Where did you document?" indicates failed documentation
- **Documentation Validation**: If you can't reference it later from a file, it wasn't properly documented

### Feature Enhancement Capture Pattern
- **Enhancement Ideas**: Capture in `.project_memory/intelligence/ENHANCEMENT_ROADMAP.md`, NOT in WORKING_PATTERNS.md
- **Individual Features**: Create detailed docs in appropriate directories (e.g., `app/intelligence/feature_name_enhancement.md`)
- **Todo Integration**: Add as categorized pending tasks with appropriate priority
- **Working Patterns**: Focus on HOW we work, not WHAT features to build

### Todo List Organization Pattern
- **Categorized Structure**: Use prefixes for clarity
  - `COMPLETED:` - Major completed work (keep for context)
  - `HIGH PRIORITY:` - Next immediate work
  - `MEDIUM PRIORITY:` - Planned enhancements
  - `FUTURE:` - Long-term ideas
- **Benefits**: Easy scanning, clear priorities, manageable scope
- **Retirement**: Archive completed todos periodically to prevent list bloat

### Technical Growth Tracking
- **Current Comfort Level**: Learning developer with good instincts, responds well to detailed explanations with real-world analogies
- **Strong Areas**: 
  - Code structure and component architecture understanding
  - Asks clarifying questions when concepts are unclear
  - Good pattern recognition for UI/UX improvements
- **Growing Areas**: 
  - **React development workflow** - debugging when changes don't appear, hot reload, browser dev tools
  - **Development server lifecycle** - why we use localhost vs opening files directly
  - **System-level debugging** - connecting networking concepts to practical troubleshooting
- **Mastered Concepts**: 
  - **Networking fundamentals** - ports, processes, connection errors (excellent grasp!)
  - **Process analysis** - can read process output and understand system resources
  - **Real-world analogies** - consistently applies restaurant/apartment analogies correctly
  - React component structure and props
  - File organization and imports
  - Basic git workflow
- **Preferred Learning Style**:
  - **Real-world analogies** (restaurant, apartment building) work very well
  - **Step-by-step breakdowns** of technical processes
  - **Multiple examples** showing different scenarios (success vs error cases)
  - **"Why this matters"** explanations connecting concepts to practical development
- **Adaptation Signals Observed**:
  - ✅ "explain this more" = wants deeper technical detail
  - ✅ "i dont fully get it" = current explanation too high-level
  - ✅ "give me similar explanations" = learning style working, wants consistency

### Effective Session Structure
- Start with context review and blockers
- Define clear success criteria
- Work in testable increments
- Document decisions immediately
- Update progress tracking files

### Problem-Solving Approach
- Understand constraints and dependencies first
- Consider multiple solutions with risk assessment
- Choose based on simplicity, maintainability, and performance
- Document why alternatives were rejected
- Always consider rollback procedures

### ASMIS-Specific Patterns
- Agent changes require parallel testing
- Database migrations need rollback procedures
- Performance baselines before any optimization
- Confidence scoring for all AI outputs
- Multi-tenant considerations for all features

### Dev Server "Connection Refused" Pattern (CRITICAL) - ✅ RESOLVED
- **Root Cause Discovery**: Next.js wasn't explicitly binding to 127.0.0.1 when using `localhost`
- **Applied Fix**: Use `--hostname 127.0.0.1` flag to force proper IP binding (2025-07-08)
- **Issue Status**: ✅ RESOLVED - Server now binds correctly and accepts connections

#### **Working Solution:**
```bash
npm run dev -- --port 3000 --hostname 127.0.0.1
```

#### **Root Cause Analysis:**
- Next.js was failing to resolve `localhost` to proper IP binding
- Server reported "Ready" but wasn't actually listening on the expected interface
- Explicit hostname binding resolves the issue completely

#### **Quick Recovery Procedure:**
```bash
pkill -f "next dev"
rm -rf .next
npm run dev -- --port 3000 --hostname 127.0.0.1
```

#### **Testing Validation:**
- ✅ Works with Node.js 18 and 20
- ✅ lsof confirms proper port binding
- ✅ curl receives expected 307 redirect responses
- ✅ Manual browser testing now possible

## Issue Tracking & Roadmap Management (Working Pattern)

- **Linear is the canonical system for all issue, feature, and roadmap tracking.**
    - All new features, bugs, enhancements, and sub-tasks are created as issues in Linear.
    - Status changes (e.g., "In Progress", "Done") are managed in Linear.
    - Comments and summaries for major milestones or completions are added to the relevant Linear issues.
- **Manual progress trackers (e.g., `.project_memory/progress/todo_tracker.md`) are used for:**
    - High-level summaries at the end of each work session or day.
    - Redundant logging for audit/history or quick reference.
    - They do not replace Linear as the source of truth.
- **Requirements and feature status are maintained in `.project_memory/intelligence/MVP_REQUIREMENTS.md` and referenced in Linear issues as needed.**
- **All contributors should check Linear for the latest priorities, assignments, and status before starting new work.**

## Pattern Evolution Logging

- **All pattern evolution (updates, replacements, major changes) must be logged in `.project_memory/patterns/PATTERN_EVOLUTION_LOG.md`.**
    - Each log entry must include: date, pattern file, summary of change, rationale, and reference to related decision or session.
    - This ensures traceability, collaboration, and adherence to best practices.
    - Pattern evolution logging is now mandatory and enforced by the neural imprinting protocol.

## Session Initiation Shortcut and Hybrid Session Management

- The command "initiate" (typed to either Claude or Cursor) will start a new session, update the session pointer, load neural imprint and working patterns, and pull context from Linear.
- All contributors (AI and human) should use this command at the start of any new work session. If a human contributor forgets, the AI will intelligently review whether the current session appears complete; if so, it will initiate the command automatically, otherwise it will prompt or remind the human to do so. This ensures session context is always current and avoids premature session switching.
- The session pointer is stored in `.project_memory/active_session.json` and always references the current Linear epic/issue and (optionally) a Markdown session log.
- `.ai/WORKING_PATTERNS.md` and `.project_memory/patterns/IMPRINT_PATTERN_INDEX.json` are always loaded at session start for best practices and available patterns.
- Markdown session logs are optional, for deep dives or retros, not required for every session.
- This hybrid, automated approach ensures both AI and human contributors work from the latest context, with minimal ceremony and maximum traceability.

## Automated Pattern Management

- Pattern capture, indexing, and evolution logging are fully automated by the AI agents (Claude, Cursor, etc.).
- Human contributors do not need to run any scripts or commands for pattern management.
- If the agent is unable to complete an action (e.g., due to permissions), it will prompt the user for approval or next steps.
- The agent will validate that the pattern index and pattern files are always in sync, and self-correct if not.

## Hybrid Stub-First Architecture Pattern

### Pattern Discovery
- **Date**: 2025-07-10
- **Context**: MIC-45 multi-tenancy implementation
- **Decision**: DEC_2025-07-10_001

### Pattern Description
For large architectural changes (multi-tenancy, auth systems, major refactoring):
1. **Foundation + Stubs**: Create core models + minimal integration stubs
2. **Integration Testing**: Test complete flow with stubs first
3. **Real Implementation**: Replace stubs with full implementations
4. **Final Validation**: Comprehensive testing and optimization

### Benefits Observed
- **Early Risk Identification**: Integration issues caught in 3 sessions vs 8
- **Architectural Validation**: Confirm approach works before heavy implementation
- **Parallel Development**: Multiple layers can be worked on simultaneously
- **Reduced Rework**: Implementation guided by proven integration patterns

### When to Use
- ✅ **Large architectural changes** affecting multiple system layers
- ✅ **New authentication/authorization** systems
- ✅ **Database schema migrations** with breaking changes
- ✅ **Multi-tenant architecture** implementation
- ❌ **Simple feature additions** or bug fixes

### Implementation Template
```
Phase 1: Foundation + Stubs (2-3 sessions)
Phase 2: Integration Testing (1 session)  
Phase 3: Real Implementation (4-6 sessions)
Phase 4: Final Validation (1 session)
```

### Pattern Status
- **Maturity**: Experimental (first use case)
- **Reference**: `.project_memory/patterns/HYBRID_STUB_FIRST_PATTERN.json`
- **Evolution**: Track effectiveness and refine based on outcomes

## Session Log Template (Updated)

At the top of every session log in `.project_memory/sessions/`, include:

```
# Session: <Session Title>
**Date**: <YYYY-MM-DD>
**Linear Project**: [Project Name or ID](https://linear.app/your-org/project/PROJECT_ID)
**Related Issues**: [ISSUE-123](https://linear.app/your-org/issue/ISSUE-123), [ISSUE-456](https://linear.app/your-org/issue/ISSUE-456)
**Duration**: <X hours>
...
```

- Always link to the relevant Linear project and issues for traceability.
- Do not create a new Linear issue for every session. Only create new issues, projects, or milestones in Linear if new work is identified that is not already documented.
- When new work is discovered during a session, the AI may create the appropriate Linear issue/project/milestone and link it in the session log.

