"""
✅ Applied: DECISION_CRITERIA_ENHANCEMENT_PATTERN
Decision Criteria Analysis for MEDDPICC Enhancement

Provides enhanced extraction and analysis of decision criteria from sales conversations,
including categorization, prioritization, business unit mapping, and quality scoring.

PATTERN_REF: DECISION_CRITERIA_ENHANCEMENT_PATTERN
"""

import logging
import re
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class CriteriaCategory(Enum):
    """Categories of decision criteria."""
    TECHNICAL = "technical"
    BUSINESS = "business"
    FINANCIAL = "financial"
    COMPLIANCE = "compliance"
    INTEGRATION = "integration"
    OPERATIONAL = "operational"


class CriteriaPriority(Enum):
    """Priority levels for criteria."""
    DEALBREAKER = "dealbreaker"
    MUST_HAVE = "must_have"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NICE_TO_HAVE = "nice_to_have"


class BusinessUnit(Enum):
    """Business units that typically own criteria."""
    MARKETING = "Marketing"
    IT = "IT"
    FINANCE = "Finance"
    SALES = "Sales"
    OPERATIONS = "Operations"
    LEGAL = "Legal"
    SECURITY = "Security"
    HR = "HR"
    EXECUTIVE = "Executive"
    PROCUREMENT = "Procurement"


@dataclass
class DecisionCriterion:
    """Individual decision criterion with metadata."""
    criterion: str
    category: CriteriaCategory
    priority: CriteriaPriority
    stakeholder: Optional[str] = None
    business_unit: Optional[BusinessUnit] = None
    measurable: bool = False
    threshold: Optional[str] = None
    dealbreaker: bool = False
    evidence: str = ""
    confidence: float = 0.0


@dataclass
class CriteriaAnalysis:
    """Complete decision criteria analysis result."""
    criteria: Dict[str, List[DecisionCriterion]] = field(default_factory=dict)
    prioritization: Dict[str, List[str]] = field(default_factory=dict)
    evaluation_process: str = ""
    decision_makers: List[str] = field(default_factory=list)
    business_unit_involvement: List[str] = field(default_factory=list)
    quality_score: float = 0.0
    coverage_score: float = 0.0
    completeness_score: float = 0.0


class DecisionCriteriaAnalyzer:
    """
    Enhanced Decision Criteria Analysis Engine.
    ✅ Applied: DECISION_CRITERIA_ENHANCEMENT_PATTERN
    
    Extracts, categorizes, and analyzes decision criteria from sales conversations
    with business unit mapping and quality scoring.
    """
    
    def __init__(self):
        """Initialize the decision criteria analyzer."""
        self.logger = logging.getLogger(self.__class__.__name__)
        self._init_patterns()
    
    def _init_patterns(self):
        """Initialize pattern libraries for criteria detection."""
        
        # Priority signal patterns - order matters for precedence
        self.priority_patterns = {
            'dealbreaker': [
                r'\b(deal.?breaker|deal.breaker)\b',
                r'\b(non.?negotiable|absolute requirement)\b',
                r'\b(without this.*can\'t|show.?stopper)\b'
            ],
            'must_have': [
                r'\b(must have|must be|required|essential|mandatory)\b',
                r'\b(need to have|have to have|critical)\b',
                r'\b(can\'t work without|won\'t work without)\b'
            ],
            'high': [
                r'\b(important|priority|high priority|key requirement)\b',
                r'\b(really need|definitely need|very important)\b',
                r'\b(looking for|need)\b'
            ],
            'medium': [
                r'\b(would like|prefer|important to have)\b',
                r'\b(medium priority|somewhat important)\b',
                r'\b(want|hoping for)\b'
            ],
            'nice_to_have': [
                r'\b(nice to have|would be good|bonus|extra)\b',
                r'\b(low priority|not critical|if possible)\b',
                r'\b(ideally|preferably)\b'
            ]
        }
        
        # Business unit patterns
        self.business_unit_patterns = {
            BusinessUnit.MARKETING: [
                r'\b(marketing|brand|campaign|conversion|engagement|leads)\b',
                r'\b(cmo|marketing director|marketing manager|marketing team)\b',
                r'\b(roi|roas|customer acquisition|lead generation)\b'
            ],
            BusinessUnit.IT: [
                r'\b(it|technical|infrastructure|system|integration|api)\b',
                r'\b(cto|it director|technical team|developers|engineers)\b',
                r'\b(scalability|performance|uptime|reliability)\b'
            ],
            BusinessUnit.FINANCE: [
                r'\b(finance|financial|cost|budget|pricing|payment)\b',
                r'\b(cfo|finance director|finance team|accounting)\b',
                r'\b(roi|cost savings|budget|expenses|financial impact)\b'
            ],
            BusinessUnit.SALES: [
                r'\b(sales|revenue|pipeline|deals|opportunities)\b',
                r'\b(sales director|sales manager|sales team|account manager)\b',
                r'\b(quota|targets|conversion rates|sales process)\b'
            ],
            BusinessUnit.OPERATIONS: [
                r'\b(operations|operational|efficiency|process|workflow)\b',
                r'\b(coo|operations director|operations team|process manager)\b',
                r'\b(automation|streamline|optimize|efficiency)\b'
            ],
            BusinessUnit.LEGAL: [
                r'\b(legal|compliance|contract|terms|regulatory)\b',
                r'\b(legal team|counsel|legal director|compliance officer)\b',
                r'\b(gdpr|hipaa|soc2|privacy|data protection)\b'
            ],
            BusinessUnit.SECURITY: [
                r'\b(security|secure|protection|audit|vulnerability)\b',
                r'\b(ciso|security director|security team|security officer)\b',
                r'\b(pen test|security review|encryption|authentication)\b'
            ],
            BusinessUnit.EXECUTIVE: [
                r'\b(executive|leadership|board|ceo|president|c.level)\b',
                r'\b(strategic|vision|company.wide|enterprise)\b'
            ]
        }
        
        # Category patterns
        self.category_patterns = {
            CriteriaCategory.TECHNICAL: [
                r'\b(api|integration|scalability|performance|uptime|speed)\b',
                r'\b(technical|technology|platform|system|infrastructure)\b',
                r'\b(database|cloud|security|authentication|backup)\b'
            ],
            CriteriaCategory.BUSINESS: [
                r'\b(business|strategy|process|workflow|efficiency|productivity)\b',
                r'\b(user experience|customer|training|support|adoption)\b',
                r'\b(growth|expansion|market|competitive|advantage)\b'
            ],
            CriteriaCategory.FINANCIAL: [
                r'\b(cost|price|budget|roi|savings|investment|value)\b',
                r'\b(financial|money|payment|billing|subscription)\b',
                r'\b(affordable|expensive|cheap|worth)\b'
            ],
            CriteriaCategory.COMPLIANCE: [
                r'\b(compliance|regulatory|audit|certification|standard)\b',
                r'\b(gdpr|hipaa|soc2|iso|pci|privacy|data protection)\b',
                r'\b(legal|terms|contract|agreement)\b'
            ]
        }
        
        # Measurable indicators
        self.measurable_patterns = [
            r'\b\d+%\b',  # Percentages
            r'\b\d+\s*(second|minute|hour|day|week|month|year)s?\b',  # Time
            r'\$\d+',  # Money
            r'\b\d+\s*(user|customer|transaction|request)s?\b',  # Quantities
            r'\b(faster|slower|more|less|better|worse)\s+than\b',  # Comparisons
            r'\b(at least|minimum|maximum|up to)\s+\d+\b'  # Thresholds
        ]
    
    def analyze_criteria(self, content: str, stakeholder_data: Optional[Dict[str, Any]] = None) -> CriteriaAnalysis:
        """
        Analyze decision criteria from conversation content.
        
        Args:
            content: Conversation/transcript content
            stakeholder_data: Optional stakeholder analysis data
            
        Returns:
            Complete criteria analysis with categorization and scoring
        """
        try:
            # Extract raw criteria mentions
            raw_criteria = self._extract_raw_criteria(content)
            
            # Analyze each criterion
            analyzed_criteria = []
            for criterion_text in raw_criteria:
                criterion = self._analyze_single_criterion(criterion_text, content)
                if criterion:
                    analyzed_criteria.append(criterion)
            
            # Categorize criteria
            categorized_criteria = self._categorize_criteria(analyzed_criteria)
            
            # Extract evaluation process and decision makers
            evaluation_process = self._extract_evaluation_process(content)
            decision_makers = self._extract_decision_makers(content, stakeholder_data)
            
            # Determine business unit involvement
            business_units = self._determine_business_units(analyzed_criteria, content)
            
            # Create prioritization buckets
            prioritization = self._create_prioritization_buckets(analyzed_criteria)
            
            # Calculate quality scores
            quality_score = self._calculate_quality_score(analyzed_criteria)
            coverage_score = self._calculate_coverage_score(categorized_criteria)
            completeness_score = self._calculate_completeness_score(analyzed_criteria, content)
            
            return CriteriaAnalysis(
                criteria=categorized_criteria,
                prioritization=prioritization,
                evaluation_process=evaluation_process,
                decision_makers=decision_makers,
                business_unit_involvement=business_units,
                quality_score=quality_score,
                coverage_score=coverage_score,
                completeness_score=completeness_score
            )
            
        except Exception as e:
            self.logger.error(f"Error analyzing decision criteria: {e}")
            return CriteriaAnalysis()
    
    def _extract_raw_criteria(self, content: str) -> List[str]:
        """Extract potential criteria mentions from content."""
        criteria = []
        
        # More precise criteria introduction patterns
        criteria_patterns = [
            r'(?:our|the|key|main)\s+(?:requirement|criteria|need)[s]?\s+(?:are?|is|include)[:\s]+([^.!?]{15,150})',
            r'(?:we|i)\s+(?:need|want|require|must have|are looking for)[:\s]+([^.!?]{15,150})',
            r'(?:deal breaker|non.negotiable|must have|critical)[:\s]+([^.!?]{15,150})',
            r'from a (?:technical|business|financial|security)\s+(?:perspective|standpoint)[,:]?\s+([^.!?]{20,200})',
            r'(?:ideally|minimum|at least|up to)\s+([^.!?]{10,100})',
            r'we need to\s+(?:see|have|achieve|get)\s+([^.!?]{10,150})',
            r'(?:must|need to|have to)\s+(?:have|be|support|provide|include)\s+([^.!?]{15,150})',
            r'(?:evaluation|demo|pilot|trial)\s+(?:criteria|requirements?|process)\s+(?:include|are)[:\s]+([^.!?]{20,200})'
        ]
        
        content_lower = content.lower()
        for pattern in criteria_patterns:
            matches = re.finditer(pattern, content_lower)
            for match in matches:
                criterion = match.group(1).strip()
                # More selective filtering
                if (len(criterion) >= 15 and 
                    len(criterion) <= 200 and 
                    not criterion.startswith(('and', 'or', 'but', 'that', 'this', 'the'))):
                    criteria.append(criterion)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_criteria = []
        for criterion in criteria:
            if criterion not in seen:
                seen.add(criterion)
                unique_criteria.append(criterion)
        
        return unique_criteria
    
    def _analyze_single_criterion(self, criterion_text: str, full_content: str) -> Optional[DecisionCriterion]:
        """Analyze a single criterion for metadata."""
        try:
            # Detect category
            category = self._detect_category(criterion_text)
            
            # Detect priority
            priority = self._detect_priority(criterion_text, full_content)
            
            # Detect business unit
            business_unit = self._detect_business_unit(criterion_text, full_content)
            
            # Check if measurable
            measurable = self._is_measurable(criterion_text)
            
            # Extract threshold if present
            threshold = self._extract_threshold(criterion_text)
            
            # Determine if dealbreaker
            dealbreaker = priority == CriteriaPriority.DEALBREAKER
            
            # Calculate confidence
            confidence = self._calculate_criterion_confidence(criterion_text, full_content)
            
            return DecisionCriterion(
                criterion=criterion_text,
                category=category,
                priority=priority,
                business_unit=business_unit,
                measurable=measurable,
                threshold=threshold,
                dealbreaker=dealbreaker,
                evidence=criterion_text,
                confidence=confidence
            )
            
        except Exception as e:
            self.logger.warning(f"Error analyzing criterion '{criterion_text}': {e}")
            return None
    
    def _detect_category(self, criterion_text: str) -> CriteriaCategory:
        """Detect the category of a criterion."""
        criterion_lower = criterion_text.lower()
        
        # Score each category based on pattern matches
        category_scores = {}
        for category, patterns in self.category_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, criterion_lower))
                score += matches
            category_scores[category] = score
        
        # Return category with highest score
        if category_scores:
            best_category = max(category_scores.items(), key=lambda x: x[1])
            if best_category[1] > 0:
                return best_category[0]
        
        return CriteriaCategory.BUSINESS  # Default
    
    def _detect_priority(self, criterion_text: str, full_content: str) -> CriteriaPriority:
        """Detect the priority level of a criterion."""
        text_lower = (criterion_text + " " + full_content).lower()
        
        # Score each priority based on pattern matches
        priority_scores = {}
        for priority, patterns in self.priority_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text_lower))
                score += matches
            priority_scores[priority] = score
        
        # Return priority with highest score
        if priority_scores:
            best_priority = max(priority_scores.items(), key=lambda x: x[1])
            if best_priority[1] > 0:
                return CriteriaPriority(best_priority[0])
        
        return CriteriaPriority.MEDIUM  # Default
    
    def _detect_business_unit(self, criterion_text: str, full_content: str) -> Optional[BusinessUnit]:
        """Detect the business unit associated with a criterion."""
        text_lower = (criterion_text + " " + full_content).lower()
        
        # Score each business unit based on pattern matches
        unit_scores = {}
        for unit, patterns in self.business_unit_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text_lower))
                score += matches
            unit_scores[unit] = score
        
        # Return unit with highest score
        if unit_scores:
            best_unit = max(unit_scores.items(), key=lambda x: x[1])
            if best_unit[1] > 0:
                return best_unit[0]
        
        return None
    
    def _is_measurable(self, criterion_text: str) -> bool:
        """Check if a criterion contains measurable elements."""
        criterion_lower = criterion_text.lower()
        
        for pattern in self.measurable_patterns:
            if re.search(pattern, criterion_lower):
                return True
        
        return False
    
    def _extract_threshold(self, criterion_text: str) -> Optional[str]:
        """Extract specific thresholds from criterion text."""
        threshold_patterns = [
            r'\$[\d,]+',  # Money amounts
            r'\b\d+%\b',  # Percentages
            r'\b(?:at least|minimum|maximum|up to)\s+[\d,]+\b',  # Numeric thresholds
            r'\b\d+\s*(?:second|minute|hour|day|week|month|year)s?\b'  # Time thresholds
        ]
        
        for pattern in threshold_patterns:
            match = re.search(pattern, criterion_text.lower())
            if match:
                return match.group()
        
        return None
    
    def _calculate_criterion_confidence(self, criterion_text: str, full_content: str) -> float:
        """Calculate confidence score for a criterion."""
        confidence = 0.5  # Base confidence
        
        # Increase confidence for specific language
        if any(word in criterion_text.lower() for word in ['must', 'required', 'critical', 'need']):
            confidence += 0.2
        
        # Increase confidence for measurable criteria
        if self._is_measurable(criterion_text):
            confidence += 0.1
        
        # Increase confidence for detailed criteria
        if len(criterion_text) > 30:
            confidence += 0.1
        
        # Increase confidence if mentioned multiple times
        mentions = full_content.lower().count(criterion_text.lower())
        if mentions > 1:
            confidence += min(0.1 * mentions, 0.2)
        
        return min(confidence, 1.0)
    
    def _categorize_criteria(self, criteria: List[DecisionCriterion]) -> Dict[str, List[DecisionCriterion]]:
        """Group criteria by category."""
        categorized = {}
        
        for criterion in criteria:
            category_key = criterion.category.value
            if category_key not in categorized:
                categorized[category_key] = []
            categorized[category_key].append(criterion)
        
        return categorized
    
    def _extract_evaluation_process(self, content: str) -> str:
        """Extract information about the evaluation process."""
        process_patterns = [
            r'(?:evaluation|demo|trial|pilot|test|proof of concept)',
            r'(?:rfp|request for proposal|proposal process)',
            r'(?:selection process|decision process|review process)'
        ]
        
        content_lower = content.lower()
        processes = []
        
        for pattern in process_patterns:
            matches = re.findall(pattern, content_lower)
            processes.extend(matches)
        
        return ", ".join(set(processes)) if processes else "Not specified"
    
    def _extract_decision_makers(self, content: str, stakeholder_data: Optional[Dict[str, Any]]) -> List[str]:
        """Extract decision makers from content and stakeholder data."""
        decision_makers = []
        
        # Extract from stakeholder data if available
        if stakeholder_data:
            stakeholders = stakeholder_data.get('stakeholders', [])
            for stakeholder in stakeholders:
                role = stakeholder.get('role_classification', '')
                if 'decision' in role.lower() or 'buyer' in role.lower():
                    name = stakeholder.get('name', 'Unknown')
                    title = stakeholder.get('title', '')
                    decision_makers.append(f"{name} ({title})" if title else name)
        
        # Extract from content using patterns
        decision_patterns = [
            r'(?:decision maker|final decision|approver|sign off|budget authority)',
            r'(?:ceo|cfo|cto|cmo|president|director|manager) (?:will|needs to|has to) (?:approve|decide|sign)'
        ]
        
        content_lower = content.lower()
        for pattern in decision_patterns:
            matches = re.findall(pattern, content_lower)
            for match in matches:
                if match not in decision_makers:
                    decision_makers.append(match)
        
        return decision_makers
    
    def _determine_business_units(self, criteria: List[DecisionCriterion], content: str) -> List[str]:
        """Determine involved business units from criteria and content."""
        units = set()
        
        # From criteria
        for criterion in criteria:
            if criterion.business_unit:
                units.add(criterion.business_unit.value)
        
        # From content patterns
        content_lower = content.lower()
        for unit, patterns in self.business_unit_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content_lower):
                    units.add(unit.value)
                    break
        
        return sorted(list(units))
    
    def _create_prioritization_buckets(self, criteria: List[DecisionCriterion]) -> Dict[str, List[str]]:
        """Create prioritization buckets for criteria."""
        buckets = {
            'must_have': [],
            'nice_to_have': [],
            'dealbreakers': []
        }
        
        for criterion in criteria:
            if criterion.dealbreaker:
                buckets['dealbreakers'].append(criterion.criterion)
            elif criterion.priority in [CriteriaPriority.DEALBREAKER, CriteriaPriority.MUST_HAVE, CriteriaPriority.HIGH]:
                buckets['must_have'].append(criterion.criterion)
            else:
                buckets['nice_to_have'].append(criterion.criterion)
        
        return buckets
    
    def _calculate_quality_score(self, criteria: List[DecisionCriterion]) -> float:
        """Calculate overall quality score for criteria."""
        if not criteria:
            return 0.0
        
        total_score = 0.0
        for criterion in criteria:
            score = 0.0
            
            # Specificity (detailed criteria score higher)
            if len(criterion.criterion) > 30:
                score += 0.3
            elif len(criterion.criterion) > 15:
                score += 0.2
            else:
                score += 0.1
            
            # Measurability
            if criterion.measurable:
                score += 0.3
            
            # Priority clarity
            if criterion.priority in [CriteriaPriority.DEALBREAKER, CriteriaPriority.MUST_HAVE]:
                score += 0.2
            elif criterion.priority != CriteriaPriority.MEDIUM:  # Not default
                score += 0.1
            
            # Business unit mapping
            if criterion.business_unit:
                score += 0.2
            
            total_score += score
        
        return min(total_score / len(criteria), 1.0)
    
    def _calculate_coverage_score(self, categorized_criteria: Dict[str, List[DecisionCriterion]]) -> float:
        """Calculate coverage score based on category diversity."""
        if not categorized_criteria:
            return 0.0
        
        # Score based on category coverage
        total_categories = len(CriteriaCategory)
        covered_categories = len(categorized_criteria)
        
        coverage_ratio = covered_categories / total_categories
        
        # Bonus for balanced coverage
        if covered_categories >= 3:
            coverage_ratio += 0.1
        
        return min(coverage_ratio, 1.0)
    
    def _calculate_completeness_score(self, criteria: List[DecisionCriterion], content: str) -> float:
        """Calculate completeness score based on criteria depth and evidence."""
        if not criteria:
            return 0.0
        
        completeness_factors = []
        
        # Criteria count (more is better, up to a point)
        count_score = min(len(criteria) / 10.0, 0.4)
        completeness_factors.append(count_score)
        
        # Average confidence
        avg_confidence = sum(c.confidence for c in criteria) / len(criteria)
        completeness_factors.append(avg_confidence * 0.3)
        
        # Evidence quality (based on content length and detail)
        evidence_score = min(len(content) / 1000.0, 0.3)
        completeness_factors.append(evidence_score)
        
        return sum(completeness_factors)


# Convenience function for external use
def analyze_decision_criteria(content: str, stakeholder_data: Optional[Dict[str, Any]] = None) -> CriteriaAnalysis:
    """Analyze decision criteria from conversation content."""
    analyzer = DecisionCriteriaAnalyzer()
    return analyzer.analyze_criteria(content, stakeholder_data)