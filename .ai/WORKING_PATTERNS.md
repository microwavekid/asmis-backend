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
- **Common Issue**: Forgetting venv activation leads to module import errors
- **User Feedback**: Has corrected this multiple times - MUST remember venv activation

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

### Technical Growth Tracking
- **Current Comfort Level**: Learning developer with good instincts
- **Strong Areas**: [AI will update based on demonstrated understanding]
- **Growing Areas**: [AI will note topics where more explanation helps]
- **Mastered Concepts**: [AI will track what no longer needs basic explanation]

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