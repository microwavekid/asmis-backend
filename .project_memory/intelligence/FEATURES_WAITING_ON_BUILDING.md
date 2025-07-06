# Features Waiting on Building - ASMIS Roadmap & Backlog

**Last Updated:** 2025-07-04
**Current Focus:** MVP Core Features

## Status Legend
- 🔴 Not Started
- 🟡 In Progress  
- 🟢 Complete
- ⏸️ Blocked
- 🔄 In Review

## Effort Scale
- 🟢 Small (1-4 hrs)
- 🟡 Medium (1-3 days)
- 🔴 Large (1+ week)

---

## 🚨 Architectural Blockers (Do These Early)
Features that will be painful to retrofit later:

### 1. Multi-Tenant with Dev Mode - 🔴 Large
- **Status:** 🔴 Not Started (Plan Ready)
- **Why Early:** Every model and API needs tenant isolation from day 1
- **Estimated:** 10-12 hours
- **Business Impact:** Foundation for supporting multiple users/customers
- **References:** MULTI_TENANT_ACCESS_CONTROL_PLAN.md

### 2. Basic Auth System - 🟡 Medium
- **Status:** 🔴 Not Started
- **Why Early:** User identity needed for ownership tracking
- **Estimated:** 4-5 hours (email/password only)
- **Business Impact:** Enables user accounts and data ownership

### 3. Basic Usage Tracking - 🟢 Small
- **Status:** 🔴 Not Started
- **Why Early:** Easier to add from start than retrofit
- **Estimated:** 2 hours
- **Business Impact:** Future billing foundation

---

## 🎯 Current Sprint (Immediate Fixes)

### 1. Deal Data Mapping Fix - 🟢 Small
- **Status:** 🟡 In Progress
- **Active Todo:** DEC_2025-06-26_006
- **Blocker for:** Seeing real deals in UI
- **Next Action:** Create Next.js API routes to bridge frontend/backend

### 2. Entity Dropdown Positioning - 🟢 Small
- **Status:** 🟡 In Progress
- **Active Todo:** DEC_2025-06-26_007
- **Blocker for:** Natural entity selection in Smart Capture
- **Next Action:** Debug z-index and positioning logic

---

## 📊 Core Functionality Backlog (Build Next)
The actual product features users need:

### Deals & Opportunities
- **Deal Detail View** - 🟡 Medium
  - Full MEDDPICC analysis display
  - Evidence linking
  - Activity timeline
  
- **Deal Creation/Edit** - 🟡 Medium
  - Form validation
  - Account/stakeholder linking
  - Stage progression

### Tasks & Actions
- **Tasks UI Foundation** - 🔴 Large
  - Cross-account task aggregation
  - AI-suggested vs human tasks
  - Priority and due date management
  - See: TASKS_UI_ENHANCEMENT_ROADMAP.md

### Accounts & Stakeholders
- **Account Dashboard** - 🟡 Medium
  - Stakeholder org chart
  - Deal pipeline view
  - Engagement history

- **Stakeholder Intelligence View** - 🟡 Medium
  - Influence mapping
  - MEDDPICC role indicators
  - Communication preferences

### Evidence & Intelligence
- **Evidence Linking UI** - 🟡 Medium
  - Connect insights to source transcripts
  - Timestamp navigation
  - Confidence indicators

- **Transcript Upload & Processing** - 🟡 Medium
  - File upload UI
  - Processing status
  - Result display

### Smart Capture Improvements
- **Entity Autocomplete Fix** - 🟢 Small
  - Fix dropdown visibility
  - Add punctuation tolerance
  - Improve trigger detection

---

## 🏗️ Infrastructure & Platform (Do When Needed)

### Performance & Scale
- **API Gateway** - 🔴 Large
  - When: When AI costs become significant
  - Business Impact: 30-50% cost reduction

- **Caching Layer** - 🟡 Medium
  - When: When response times lag
  - Business Impact: Faster user experience

### Security & Enterprise
- **SSO Integration** - 🔴 Large
  - When: First enterprise customer requests
  - Business Impact: Enterprise sales enablement

- **Advanced RBAC** - 🔴 Large
  - When: Teams need granular permissions
  - Business Impact: Team collaboration

- **Envelope Encryption** - 🟡 Medium
  - When: Storing customer API keys
  - Business Impact: Security compliance

---

## 💡 Intelligence Enhancements (Future Vision)

### Advanced AI Features
- **Adaptive MEDDPICC Questions** - 🔴 Large
  - When: Core MEDDPICC proven valuable
  - Business Impact: 30-40% faster sales cycles

- **Timeline Extraction** - 🟡 Medium
  - When: Users request better visibility
  - Business Impact: Deal progression insights

- **Multi-Source Evidence** - 🔴 Large
  - When: Multiple document types supported
  - Business Impact: Complete evidence trail

---

## Quick Wins Board
Low effort, high impact:

1. **Deal Data Mapping** - Fix API route mismatch
2. **Entity Dropdown** - CSS positioning fix
3. **Dev Mode Auth** - Skip auth in development
4. **Sample Data Script** - Load test data easily
5. **Basic Error Toasts** - User feedback on actions

---

## Not Doing Yet (Explicitly Deferred)
- Complex billing system
- API rate limiting (until needed)
- Advanced analytics
- White labeling
- SCIM provisioning
- Custom integrations

---

## Implementation Philosophy
1. **Build what users can see and use** (Deals, Tasks, Accounts)
2. **Address architectural decisions with major downstream implications early** (Multi-tenancy, data models, auth structure)
3. **Add infrastructure only when it blocks progress**
4. **Defer enterprise features until customers need them**
5. **Keep dev experience fast and simple**

### Examples of "Early Architecture" vs "Defer Until Needed"
**Do Early:**
- Tenant isolation (painful to retrofit)
- User/ownership models (affects every feature)
- Core data relationships (Deal->Account->Stakeholder)
- Basic auth structure (even if simple)
- Audit trails (easier from start)

**Defer Until Needed:**
- Complex permissions (start with owner-only)
- SSO (start with email/password)
- API rate limiting (monitor first)
- Advanced caching (measure first)
- Billing integration (track usage only)

---

## References
- MULTI_TENANT_ACCESS_CONTROL_PLAN.md (simplified approach)
- TASKS_UI_ENHANCEMENT_ROADMAP.md
- ENHANCEMENT_ROADMAP.md
- DEALS_DATA_MAPPING_TODO.md