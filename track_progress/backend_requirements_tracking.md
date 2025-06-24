# Backend Requirements Tracking - Deal Intelligence Interface

## Status: CRITICAL - Frontend Ahead of Backend Architecture

The new Linear-inspired deals interface has exposed significant gaps in our backend architecture. The frontend is currently using mock data but requires substantial backend development to support real functionality.

## 🚨 Critical Missing Components

### 1. Core Domain Models (BLOCKING)

**Status**: ❌ Missing  
**Priority**: P0 - CRITICAL  
**Impact**: Frontend cannot function with real data

**Required Models:**
```python
# backend/app/database/models.py additions needed:

class Account(Base, UUIDMixin, TimestampMixin):
    name: str
    industry: Optional[str] 
    size: Literal['enterprise', 'mid_market', 'smb']
    created_by: Optional[str]

class Deal(Base, UUIDMixin, TimestampMixin):
    name: str
    account_id: str  # FK to Account
    value: Optional[Decimal]
    stage: DealStage  # Enum needed
    expected_close_date: Optional[Date]
    owner_id: Optional[str]
    priority: Literal['high', 'medium', 'low'] = 'medium'
    # Links to existing evidence system

class DealHealth(Base, UUIDMixin, TimestampMixin):
    deal_id: str  # FK to Deal
    score: Float  # 0-100 for frontend
    trend: Literal['improving', 'stable', 'declining']
    factors: JSON  # For breakdown
    last_calculated: DateTime

class DealAnalysis(Base, UUIDMixin, TimestampMixin):
    deal_id: str  # FK to Deal  
    meddpicc_analysis: JSON  # Links to existing MEDDPICC system
    overall_score: Float
    confidence_score: Float
    last_updated: DateTime
```

### 2. API Layer Architecture (BLOCKING)

**Status**: ❌ Missing  
**Priority**: P0 - CRITICAL  
**Impact**: Frontend table, filtering, sorting all non-functional

**Required Endpoints:**
```python
# backend/app/routers/deals.py (new file needed)

@router.get("/deals")
async def get_deals(
    search: Optional[str] = None,
    stage: Optional[List[str]] = Query(None),
    health_band: Optional[List[str]] = Query(None), 
    value_band: Optional[List[str]] = Query(None),
    priority: Optional[List[str]] = Query(None),
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = "asc",
    skip: int = 0,
    limit: int = 100
) -> DealListResponse

@router.get("/deals/{deal_id}")
async def get_deal(deal_id: str) -> DealDetailResponse

@router.get("/deals/{deal_id}/intelligence") 
async def get_deal_intelligence(deal_id: str) -> DealIntelligenceResponse

@router.post("/deals")
async def create_deal(deal: DealCreateRequest) -> DealResponse

@router.get("/deals/stats")
async def get_deal_stats() -> DealStatsResponse
```

### 3. Data Aggregation Services (HIGH PRIORITY)

**Status**: ❌ Missing  
**Priority**: P1 - HIGH  
**Impact**: MEDDPICC integration, health calculation broken

**Required Services:**
```python
# backend/app/services/deal_intelligence.py (new file)

class DealIntelligenceService:
    """Aggregates all deal intelligence data."""
    async def get_deal_intelligence(self, deal_id: str) -> DealIntelligence
    async def calculate_deal_health(self, deal_id: str) -> DealHealth
    async def get_meddpicc_analysis(self, deal_id: str) -> MEDDPICCAnalysis

# backend/app/services/deal_search.py (new file)
class DealSearchService:
    """Handles complex filtering and search."""
    async def search_deals(self, filters: DealFilters) -> List[Deal]
    async def get_filtered_deals(self, filters: DealFilters) -> PaginatedDeals
```

### 4. Database Migration (IMMEDIATE)

**Status**: ❌ Missing  
**Priority**: P0 - IMMEDIATE  
**Impact**: No data persistence possible

**Required Migration:**
```sql
-- Create migration: add_deal_and_account_tables

CREATE TABLE accounts (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(500) NOT NULL,
    industry VARCHAR(100),
    size VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_account_name (name)
);

CREATE TABLE deals (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(500) NOT NULL,
    account_id VARCHAR(36) NOT NULL,
    value DECIMAL(15,2),
    stage VARCHAR(50) NOT NULL,
    expected_close_date DATE,
    priority VARCHAR(20) DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(id),
    INDEX idx_deal_stage (stage),
    INDEX idx_deal_close_date (expected_close_date),
    INDEX idx_deal_value (value),
    INDEX idx_deal_name (name)
);

CREATE TABLE deal_health_history (
    id VARCHAR(36) PRIMARY KEY,
    deal_id VARCHAR(36) NOT NULL,
    score FLOAT NOT NULL,
    trend VARCHAR(20),
    factors JSON,
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (deal_id) REFERENCES deals(id),
    INDEX idx_deal_health_deal_id (deal_id),
    INDEX idx_deal_health_calculated (calculated_at)
);
```

## 🔄 Integration Requirements

### Link Existing Systems to New Deal Architecture

**Evidence System Integration:**
```python
# Modify backend/app/database/models.py
class IntelligenceEvidence(Base, UUIDMixin, TimestampMixin):
    # ADD: deal_id field to link evidence to deals
    deal_id: Optional[str]  # FK to Deal
    
    # Update repository to filter evidence by deal
```

**MEDDPICC System Integration:**
```python
# Update backend/app/agents/meddpic_orchestrator.py
class MEDDPICOrchestrator:
    # ADD: deal_id parameter to all analysis methods
    async def analyze_deal_meddpicc(self, deal_id: str, transcript_data: str) -> MEDDPICCAnalysis
    
    # Link analysis results to DealAnalysis table
```

## 📊 Frontend-Backend Interface Mapping

**Current Frontend Types → Backend Models Needed:**

| Frontend Interface | Backend Model | Status | Priority |
|-------------------|---------------|---------|----------|
| `Deal` | `Deal` + `Account` | ❌ Missing | P0 |
| `MEDDPICCAnalysis` | `DealAnalysis` | ❌ Missing | P0 |
| `DealIntelligence` | Aggregation Service | ❌ Missing | P1 |
| `FilterState` | Query Parameters | ❌ Missing | P1 |
| Evidence linking | `IntelligenceEvidence.deal_id` | ❌ Missing | P1 |

## 🎯 Implementation Roadmap

### Phase 1: Foundation (Week 1)
- [ ] Add Deal and Account models
- [ ] Create database migration
- [ ] Build basic CRUD repositories
- [ ] Create core API endpoints

### Phase 2: Intelligence Integration (Week 2)  
- [ ] Build DealIntelligenceService
- [ ] Connect MEDDPICC system to deals
- [ ] Add evidence linking via deal_id
- [ ] Implement health calculation

### Phase 3: Advanced Features (Week 3)
- [ ] Add search and filtering APIs
- [ ] Implement sorting and pagination
- [ ] Add deal timeline and activity tracking
- [ ] Build dashboard statistics endpoints

### Phase 4: Real-time Features (Week 4)
- [ ] WebSocket integration for live updates
- [ ] Background job processing for analysis
- [ ] Advanced analytics and reporting

## ⚠️ Current Technical Debt

1. **Frontend using mock data** - All deal data is hardcoded
2. **No persistent Deal storage** - Cannot save deal information
3. **MEDDPICC analysis isolated** - Not connected to deal entities
4. **Evidence not deal-linked** - Cannot show deal-specific evidence
5. **No real filtering/sorting** - All done client-side on mock data

## 📈 Business Impact

**Immediate (Missing P0 items):**
- Cannot demo real deal data
- Cannot persist deal changes
- Cannot integrate with MEDDPICC analysis
- Cannot use evidence system effectively

**Short-term (Missing P1 items):**
- Limited scalability for multiple deals
- No real-time collaboration
- No advanced analytics capabilities

**Long-term (Missing P2 items):**
- Cannot build advanced AI features
- Limited reporting capabilities
- No workflow automation

---

**Next Action Required:** Begin Phase 1 implementation to unblock frontend functionality.