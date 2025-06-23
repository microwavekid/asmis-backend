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