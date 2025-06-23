"""
✅ Applied: AGENT_COMMUNICATION_PATTERN
Competition Inference Engine for MEDDPICCC Analysis

Detects both explicit competitor mentions and infers likely competitors from context,
requirements, and market intelligence signals.

PATTERN_REF: AGENT_COMMUNICATION_PATTERN
ENHANCEMENT: Competition inference beyond explicit mentions
"""

import logging
import re
from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class CompetitionSignalType(Enum):
    """Types of competitive intelligence signals."""
    EXPLICIT_MENTION = "explicit_mention"
    FEATURE_REQUIREMENT = "feature_requirement" 
    INTEGRATION_NEED = "integration_need"
    BUDGET_RANGE = "budget_range"
    INDUSTRY_VERTICAL = "industry_vertical"
    TIMELINE_PRESSURE = "timeline_pressure"
    DECISION_CRITERIA = "decision_criteria"
    PAIN_POINT = "pain_point"


@dataclass
class CompetitionSignal:
    """Individual competitive intelligence signal."""
    signal_type: CompetitionSignalType
    content: str
    confidence: float
    evidence: str
    inferred_competitors: List[str]


@dataclass
class CompetitorInference:
    """Inferred competitor with supporting evidence."""
    competitor_name: str
    confidence_score: float
    inference_reasons: List[str]
    supporting_signals: List[CompetitionSignal]
    market_position: str  # "primary", "secondary", "emerging"
    threat_level: str  # "high", "medium", "low"
    solution_context: Optional[str] = None  # Which solution they compete in


# PATTERN_REF: AGENT_COMMUNICATION_PATTERN
class CompetitionInferenceEngine:
    """
    Analyzes content to detect explicit and implicit competitive intelligence.
    ✅ Applied: AGENT_COMMUNICATION_PATTERN
    """
    
    def __init__(self, tenant_solutions: Optional[Dict[str, Any]] = None):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.tenant_solutions = tenant_solutions or {}
        self._load_competitive_intelligence_database()
        self._initialize_solution_mappings()
    
    def _load_competitive_intelligence_database(self):
        """Load competitive intelligence patterns and mappings."""
        # ENHANCEMENT: Competition inference patterns
        
        # Explicit competitor mention patterns
        self.explicit_patterns = {
            r'\b(salesforce|sf)\b': ['Salesforce'],
            r'\b(hubspot|hub\s*spot)\b': ['HubSpot'],
            r'\b(microsoft\s*dynamics|dynamics\s*365|d365)\b': ['Microsoft Dynamics'],
            r'\b(oracle\s*sales|oracle\s*cloud)\b': ['Oracle Sales Cloud'],
            r'\b(pipedrive)\b': ['Pipedrive'],
            r'\b(zoho\s*crm|zoho)\b': ['Zoho CRM'],
            r'\b(monday\.com|monday)\b': ['Monday.com'],
            r'\b(asana)\b': ['Asana'],
            r'\b(clickup)\b': ['ClickUp'],
            r'\b(notion)\b': ['Notion']
        }
        
        # Feature requirement → competitor mapping
        self.feature_competitor_map = {
            'salesforce integration': ['HubSpot', 'Pipedrive', 'Microsoft Dynamics'],
            'advanced reporting': ['Salesforce', 'HubSpot', 'Microsoft Dynamics'],
            'workflow automation': ['HubSpot', 'Salesforce', 'Monday.com'],
            'email marketing': ['HubSpot', 'Salesforce Marketing Cloud'],
            'lead scoring': ['HubSpot', 'Salesforce', 'Microsoft Dynamics'],
            'mobile app': ['Salesforce', 'HubSpot', 'Pipedrive'],
            'api integration': ['Salesforce', 'HubSpot', 'Microsoft Dynamics'],
            'custom fields': ['Salesforce', 'HubSpot', 'Pipedrive'],
            'team collaboration': ['Monday.com', 'Asana', 'ClickUp'],
            'project management': ['Monday.com', 'Asana', 'ClickUp', 'Notion']
        }
        
        # Integration mentions → competitor mapping  
        self.integration_competitor_map = {
            'outlook integration': ['Microsoft Dynamics', 'HubSpot'],
            'gmail integration': ['HubSpot', 'Pipedrive', 'Salesforce'],
            'slack integration': ['HubSpot', 'Salesforce', 'Monday.com'],
            'teams integration': ['Microsoft Dynamics', 'Monday.com'],
            'zoom integration': ['HubSpot', 'Salesforce'],
            'marketo integration': ['Salesforce'],
            'pardot integration': ['Salesforce'],
            'mailchimp integration': ['HubSpot']
        }
        
        # Budget range → likely competitors
        self.budget_competitor_map = {
            (0, 50000): ['HubSpot', 'Pipedrive', 'Zoho CRM'],
            (50000, 150000): ['HubSpot', 'Salesforce Professional', 'Microsoft Dynamics'],
            (150000, 500000): ['Salesforce Enterprise', 'Microsoft Dynamics', 'Oracle'],
            (500000, float('inf')): ['Salesforce Enterprise+', 'Oracle', 'SAP']
        }
        
        # Industry → common competitor patterns
        self.industry_competitor_map = {
            'financial services': ['Salesforce Financial Cloud', 'Microsoft Dynamics', 'Oracle'],
            'healthcare': ['Salesforce Health Cloud', 'Microsoft Dynamics', 'Epic'],
            'manufacturing': ['Microsoft Dynamics', 'Oracle', 'SAP'],
            'retail': ['Salesforce Commerce Cloud', 'HubSpot', 'Microsoft Dynamics'],
            'technology': ['Salesforce', 'HubSpot', 'Pipedrive'],
            'logistics': ['Oracle', 'SAP', 'Microsoft Dynamics'],
            'education': ['Salesforce Education Cloud', 'HubSpot'],
            'nonprofits': ['Salesforce NPSP', 'HubSpot for Nonprofits']
        }
        
        # Decision criteria → competitor strengths
        self.criteria_competitor_map = {
            'ease of use': ['HubSpot', 'Pipedrive'],
            'customization': ['Salesforce', 'Microsoft Dynamics'],
            'integration capabilities': ['Salesforce', 'HubSpot', 'Microsoft Dynamics'],
            'reporting capabilities': ['Salesforce', 'Microsoft Dynamics'],
            'mobile experience': ['HubSpot', 'Pipedrive', 'Salesforce'],
            'cost effectiveness': ['HubSpot', 'Pipedrive', 'Zoho'],
            'scalability': ['Salesforce', 'Microsoft Dynamics', 'Oracle'],
            'security': ['Salesforce', 'Microsoft Dynamics', 'Oracle'],
            'implementation speed': ['HubSpot', 'Pipedrive'],
            'brand recognition': ['Salesforce', 'Microsoft']
        }
    
    def _initialize_solution_mappings(self):
        """Initialize solution-specific competitor mappings."""
        # Default solution mappings - can be overridden by tenant configuration
        self.solution_mappings = {
            # Example: Multi-solution company like Optimizely
            'experimentation': {
                'keywords': ['a/b test', 'split test', 'experiment', 'variation', 'optimization'],
                'competitors': ['Optimizely', 'VWO', 'Google Optimize', 'Adobe Target', 'Unbounce']
            },
            'personalization': {
                'keywords': ['personalization', 'dynamic content', 'audience targeting', 'behavioral'],
                'competitors': ['Dynamic Yield', 'Monetate', 'Adobe Target', 'Evergage', 'Optimizely']
            },
            'cdp': {
                'keywords': ['customer data platform', 'cdp', 'unified profile', 'data management'],
                'competitors': ['Segment', 'Salesforce CDP', 'Adobe CDP', 'Treasure Data', 'mParticle']
            },
            'cms': {
                'keywords': ['content management', 'cms', 'headless', 'content delivery'],
                'competitors': ['Contentful', 'Sitecore', 'Adobe Experience Manager', 'Drupal', 'WordPress']
            },
            'content_marketing': {
                'keywords': ['content marketing', 'content strategy', 'editorial workflow'],
                'competitors': ['HubSpot', 'Contently', 'CoSchedule', 'Kapost', 'Rock Content']
            },
            'workflows': {
                'keywords': ['workflow', 'automation', 'approval process', 'campaign management'],
                'competitors': ['Marketo', 'HubSpot', 'Pardot', 'Campaign Monitor', 'Mailchimp']
            },
            'commerce': {
                'keywords': ['ecommerce', 'commerce', 'shopping', 'checkout', 'product catalog'],
                'competitors': ['Shopify', 'Magento', 'BigCommerce', 'WooCommerce', 'Salesforce Commerce']
            },
            # General CRM/Sales solutions
            'crm': {
                'keywords': ['crm', 'customer relationship', 'sales management', 'lead tracking'],
                'competitors': ['Salesforce', 'HubSpot', 'Microsoft Dynamics', 'Pipedrive', 'Zoho']
            },
            'sales_intelligence': {
                'keywords': ['sales intelligence', 'deal analysis', 'meddpicc', 'sales coaching'],
                'competitors': ['Gong', 'Chorus', 'Salesloft', 'Outreach', 'Revenue.io']
            }
        }
        
        # Override with tenant-specific mappings if provided
        if self.tenant_solutions:
            self.solution_mappings.update(self.tenant_solutions.get('solution_mappings', {}))
    
    def analyze_competition(self, content: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze content for competitive intelligence signals.
        
        Args:
            content: Text content to analyze
            context: Additional context (budget, industry, etc.)
            
        Returns:
            Comprehensive competition analysis
            
        PATTERN_REF: AGENT_COMMUNICATION_PATTERN
        """
        try:
            # First, determine relevant solutions from content
            relevant_solutions = self._identify_relevant_solutions(content, context)
            
            signals = self._extract_signals(content, context)
            
            # Add solution-specific signals
            if relevant_solutions:
                solution_signals = self._extract_solution_specific_signals(content, relevant_solutions)
                signals.extend(solution_signals)
            
            explicit_competitors = self._find_explicit_mentions(content)
            inferred_competitors = self._infer_competitors(signals, context, relevant_solutions)
            
            # Combine and rank all competitors
            all_competitors = self._combine_competitor_intelligence(
                explicit_competitors, inferred_competitors
            )
            
            # Generate competitive positioning analysis
            competitive_analysis = self._analyze_competitive_position(
                all_competitors, signals, content
            )
            
            return {
                "competition": {
                    "explicit_competitors": explicit_competitors,
                    "inferred_competitors": inferred_competitors,
                    "all_competitors": all_competitors,
                    "relevant_solutions": relevant_solutions,
                    "competitive_signals": [signal.__dict__ for signal in signals],
                    "competitive_analysis": competitive_analysis,
                    "confidence_score": self._calculate_overall_confidence(all_competitors),
                    "threat_assessment": self._assess_threat_levels(all_competitors),
                    "our_position": self._analyze_our_position(all_competitors, signals)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing competition: {e}")
            return {
                "competition": {
                    "error": str(e),
                    "confidence_score": 0.0
                }
            }
    
    def _extract_signals(self, content: str, context: Optional[Dict[str, Any]]) -> List[CompetitionSignal]:
        """Extract competitive intelligence signals from content."""
        signals = []
        content_lower = content.lower()
        
        # Feature requirement signals
        for feature, competitors in self.feature_competitor_map.items():
            if feature in content_lower:
                signals.append(CompetitionSignal(
                    signal_type=CompetitionSignalType.FEATURE_REQUIREMENT,
                    content=feature,
                    confidence=0.7,
                    evidence=f"Mentioned requirement: '{feature}'",
                    inferred_competitors=competitors
                ))
        
        # Integration signals
        for integration, competitors in self.integration_competitor_map.items():
            if integration in content_lower:
                signals.append(CompetitionSignal(
                    signal_type=CompetitionSignalType.INTEGRATION_NEED,
                    content=integration,
                    confidence=0.8,
                    evidence=f"Integration requirement: '{integration}'",
                    inferred_competitors=competitors
                ))
        
        # Decision criteria signals
        for criteria, competitors in self.criteria_competitor_map.items():
            if criteria in content_lower:
                signals.append(CompetitionSignal(
                    signal_type=CompetitionSignalType.DECISION_CRITERIA,
                    content=criteria,
                    confidence=0.6,
                    evidence=f"Decision criteria: '{criteria}'",
                    inferred_competitors=competitors
                ))
        
        # Budget signals (from context)
        if context and 'budget' in context:
            budget = context['budget']
            if isinstance(budget, (int, float)):
                for (min_budget, max_budget), competitors in self.budget_competitor_map.items():
                    if min_budget <= budget <= max_budget:
                        signals.append(CompetitionSignal(
                            signal_type=CompetitionSignalType.BUDGET_RANGE,
                            content=f"${budget:,}",
                            confidence=0.8,
                            evidence=f"Budget range ${min_budget:,}-${max_budget:,}",
                            inferred_competitors=competitors
                        ))
        
        # Industry signals (from context)
        if context and 'industry' in context:
            industry = context['industry'].lower()
            for industry_key, competitors in self.industry_competitor_map.items():
                if industry_key in industry:
                    signals.append(CompetitionSignal(
                        signal_type=CompetitionSignalType.INDUSTRY_VERTICAL,
                        content=industry,
                        confidence=0.7,
                        evidence=f"Industry vertical: '{industry}'",
                        inferred_competitors=competitors
                    ))
        
        return signals
    
    def _extract_solution_specific_signals(self, content: str, relevant_solutions: List[Dict[str, Any]]) -> List[CompetitionSignal]:
        """Extract signals specifically from identified solutions."""
        solution_signals = []
        
        for solution_info in relevant_solutions:
            solution = solution_info.get('solution')
            if solution in self.solution_mappings:
                competitors = self.solution_mappings[solution].get('competitors', [])
                matched_keywords = solution_info.get('matched_keywords', [])
                relevance_score = solution_info.get('relevance_score', 0.0)
                
                # Create a signal for this solution
                solution_signals.append(CompetitionSignal(
                    signal_type=CompetitionSignalType.FEATURE_REQUIREMENT,
                    content=f"{solution} solution keywords: {', '.join(matched_keywords)}",
                    confidence=0.8 * relevance_score,  # Scale confidence by relevance
                    evidence=f"Solution '{solution}' identified from keywords: {matched_keywords}",
                    inferred_competitors=competitors
                ))
        
        return solution_signals
    
    def _identify_relevant_solutions(self, content: str, context: Optional[Dict[str, Any]] = None) -> List[str]:
        """Identify which solutions are relevant based on content and context."""
        relevant_solutions = []
        content_lower = content.lower()
        
        # Check for solution-specific keywords
        for solution, mapping in self.solution_mappings.items():
            keywords = mapping.get('keywords', [])
            keyword_matches = sum(1 for keyword in keywords if keyword in content_lower)
            
            if keyword_matches > 0:
                relevance_score = keyword_matches / len(keywords)
                relevant_solutions.append({
                    'solution': solution,
                    'relevance_score': relevance_score,
                    'matched_keywords': [kw for kw in keywords if kw in content_lower]
                })
        
        # Check context for explicit solution indication
        if context:
            # From Salesforce opportunity products
            if 'opportunity_products' in context:
                products = context['opportunity_products']
                for product in products:
                    for solution in self.solution_mappings.keys():
                        if solution.lower() in product.lower():
                            relevant_solutions.append({
                                'solution': solution,
                                'relevance_score': 1.0,
                                'source': 'opportunity_context'
                            })
            
            # From user indication
            if 'indicated_solutions' in context:
                for solution in context['indicated_solutions']:
                    relevant_solutions.append({
                        'solution': solution,
                        'relevance_score': 1.0,
                        'source': 'user_indication'
                    })
        
        # Sort by relevance score and return solution names
        relevant_solutions.sort(key=lambda x: x['relevance_score'], reverse=True)
        return relevant_solutions
    
    def _find_explicit_mentions(self, content: str) -> List[Dict[str, Any]]:
        """Find explicit competitor mentions in content."""
        explicit_competitors = []
        content_lower = content.lower()
        
        for pattern, competitors in self.explicit_patterns.items():
            matches = re.finditer(pattern, content_lower, re.IGNORECASE)
            for match in matches:
                for competitor in competitors:
                    # Find the actual matched text for evidence
                    matched_text = match.group()
                    
                    explicit_competitors.append({
                        "competitor_name": competitor,
                        "confidence": 0.95,
                        "mention_type": "direct",
                        "evidence": f"Direct mention: '{matched_text}'",
                        "context": self._extract_context_around_match(content, match.start(), match.end())
                    })
        
        return explicit_competitors
    
    def _infer_competitors(self, signals: List[CompetitionSignal], context: Optional[Dict[str, Any]], relevant_solutions: List[str] = None) -> List[CompetitorInference]:
        """Infer likely competitors from signals."""
        competitor_scores = {}
        
        # Aggregate signals by competitor
        for signal in signals:
            for competitor in signal.inferred_competitors:
                if competitor not in competitor_scores:
                    competitor_scores[competitor] = {
                        'total_confidence': 0.0,
                        'signal_count': 0,
                        'signals': [],
                        'reasons': set(),
                        'solution_context': None
                    }
                
                competitor_scores[competitor]['total_confidence'] += signal.confidence
                competitor_scores[competitor]['signal_count'] += 1
                competitor_scores[competitor]['signals'].append(signal)
                competitor_scores[competitor]['reasons'].add(
                    f"{signal.signal_type.value}: {signal.content}"
                )
                
                # Add solution-specific competitor filtering
                if relevant_solutions:
                    for solution_info in relevant_solutions:
                        solution = solution_info.get('solution') if isinstance(solution_info, dict) else solution_info
                        if solution in self.solution_mappings:
                            solution_competitors = self.solution_mappings[solution].get('competitors', [])
                            if competitor in solution_competitors:
                                competitor_scores[competitor]['solution_context'] = solution
                                # Boost confidence for solution-specific matches
                                competitor_scores[competitor]['total_confidence'] *= 1.2
        
        # Convert to CompetitorInference objects
        inferred_competitors = []
        for competitor, data in competitor_scores.items():
            if data['signal_count'] > 0:
                avg_confidence = data['total_confidence'] / data['signal_count']
                
                # Boost confidence for multiple signals
                if data['signal_count'] > 1:
                    avg_confidence = min(0.95, avg_confidence * 1.2)
                
                inferred_competitors.append(CompetitorInference(
                    competitor_name=competitor,
                    confidence_score=avg_confidence,
                    inference_reasons=list(data['reasons']),
                    supporting_signals=data['signals'],
                    market_position=self._determine_market_position(competitor),
                    threat_level=self._determine_threat_level(competitor, avg_confidence),
                    solution_context=data.get('solution_context')
                ))
        
        # Sort by confidence score
        inferred_competitors.sort(key=lambda x: x.confidence_score, reverse=True)
        
        return inferred_competitors
    
    def _combine_competitor_intelligence(self, explicit: List[Dict], inferred: List[CompetitorInference]) -> List[Dict[str, Any]]:
        """Combine explicit and inferred competitor intelligence."""
        combined = {}
        
        # Add explicit competitors (highest confidence)
        for comp in explicit:
            name = comp['competitor_name']
            combined[name] = {
                'competitor_name': name,
                'detection_type': 'explicit',
                'confidence_score': comp['confidence'],
                'evidence': [comp['evidence']],
                'context': comp.get('context', ''),
                'market_position': self._determine_market_position(name),
                'threat_level': 'high'  # Explicit mentions are usually primary threats
            }
        
        # Add inferred competitors (merge if already exists)
        for comp in inferred:
            name = comp.competitor_name
            if name in combined:
                # Boost confidence if both explicit and inferred
                combined[name]['confidence_score'] = min(0.98, 
                    (combined[name]['confidence_score'] + comp.confidence_score) / 2 * 1.3)
                combined[name]['detection_type'] = 'explicit_and_inferred'
                combined[name]['evidence'].extend([
                    f"Inferred from: {reason}" for reason in comp.inference_reasons
                ])
            else:
                combined[name] = {
                    'competitor_name': name,
                    'detection_type': 'inferred',
                    'confidence_score': comp.confidence_score,
                    'evidence': [f"Inferred from: {reason}" for reason in comp.inference_reasons],
                    'context': '',
                    'market_position': comp.market_position,
                    'threat_level': comp.threat_level
                }
        
        # Convert to sorted list
        result = list(combined.values())
        result.sort(key=lambda x: x['confidence_score'], reverse=True)
        
        return result
    
    def _analyze_competitive_position(self, competitors: List[Dict], signals: List[CompetitionSignal], content: str) -> Dict[str, Any]:
        """Analyze our competitive position against identified competitors."""
        if not competitors:
            return {"analysis": "No significant competition detected"}
        
        primary_competitor = competitors[0]
        
        return {
            "primary_threat": primary_competitor['competitor_name'],
            "threat_level": primary_competitor['threat_level'],
            "competitive_landscape": len(competitors),
            "key_battlegrounds": self._identify_battlegrounds(signals),
            "recommended_positioning": self._recommend_positioning(primary_competitor, signals),
            "differentiation_opportunities": self._identify_differentiation_opportunities(competitors, signals)
        }
    
    def _calculate_overall_confidence(self, competitors: List[Dict]) -> float:
        """Calculate overall confidence in competitive analysis."""
        if not competitors:
            return 0.0
        
        # Weight by detection type and number of competitors
        total_weighted = sum(
            comp['confidence_score'] * (1.0 if comp['detection_type'] == 'explicit' else 0.8)
            for comp in competitors
        )
        
        return min(0.95, total_weighted / len(competitors))
    
    def _assess_threat_levels(self, competitors: List[Dict]) -> Dict[str, List[str]]:
        """Assess threat levels of all competitors."""
        threats = {"high": [], "medium": [], "low": []}
        
        for comp in competitors:
            threats[comp['threat_level']].append(comp['competitor_name'])
        
        return threats
    
    def _analyze_our_position(self, competitors: List[Dict], signals: List[CompetitionSignal]) -> Dict[str, Any]:
        """Analyze our competitive position and advantages."""
        # ENHANCEMENT: This would integrate with our product positioning database
        return {
            "competitive_advantages": ["Implementation speed", "Industry specialization", "Cost effectiveness"],
            "areas_of_concern": ["Brand recognition", "Feature breadth"],
            "recommended_approach": "Focus on speed-to-value and industry expertise",
            "confidence": 0.8
        }
    
    # Helper methods
    def _extract_context_around_match(self, content: str, start: int, end: int, window: int = 50) -> str:
        """Extract context around a pattern match."""
        context_start = max(0, start - window)
        context_end = min(len(content), end + window)
        return content[context_start:context_end]
    
    def _determine_market_position(self, competitor: str) -> str:
        """Determine market position of competitor."""
        primary_competitors = ['Salesforce', 'HubSpot', 'Microsoft Dynamics']
        if competitor in primary_competitors:
            return 'primary'
        return 'secondary'
    
    def _determine_threat_level(self, competitor: str, confidence: float) -> str:
        """Determine threat level based on competitor and confidence."""
        if confidence > 0.8:
            return 'high'
        elif confidence > 0.6:
            return 'medium'
        return 'low'
    
    def _identify_battlegrounds(self, signals: List[CompetitionSignal]) -> List[str]:
        """Identify key competitive battlegrounds."""
        battlegrounds = set()
        for signal in signals:
            if signal.signal_type == CompetitionSignalType.DECISION_CRITERIA:
                battlegrounds.add(signal.content)
            elif signal.signal_type == CompetitionSignalType.FEATURE_REQUIREMENT:
                battlegrounds.add(signal.content)
        return list(battlegrounds)
    
    def _recommend_positioning(self, primary_competitor: Dict, signals: List[CompetitionSignal]) -> str:
        """Recommend competitive positioning strategy."""
        competitor_name = primary_competitor['competitor_name']
        
        # ENHANCEMENT: This would be more sophisticated with real competitive intelligence
        positioning_map = {
            'Salesforce': 'Emphasize implementation speed and cost-effectiveness',
            'HubSpot': 'Focus on advanced features and enterprise scalability',
            'Microsoft Dynamics': 'Highlight ease of use and faster time-to-value',
            'Oracle': 'Stress modern technology and user experience'
        }
        
        return positioning_map.get(competitor_name, 'Differentiate on unique value proposition')
    
    def _identify_differentiation_opportunities(self, competitors: List[Dict], signals: List[CompetitionSignal]) -> List[str]:
        """Identify opportunities for competitive differentiation."""
        opportunities = []
        
        # Look for gaps in competitor strengths vs requirements
        mentioned_features = [s.content for s in signals if s.signal_type == CompetitionSignalType.FEATURE_REQUIREMENT]
        
        if 'implementation speed' in ' '.join(mentioned_features):
            opportunities.append('Fast implementation timeline')
        if 'cost' in ' '.join(mentioned_features):
            opportunities.append('Total cost of ownership advantage')
        if 'integration' in ' '.join(mentioned_features):
            opportunities.append('Superior integration capabilities')
        
        return opportunities


# DECISION_REF: TIP_MEDDPICCC_COMPETITION_INFERENCE_001 - Enhanced competition detection with inference capabilities