"""
✅ Applied: STAKEHOLDER_RELATIONSHIP_MAPPING_PATTERN
Enhanced Stakeholder Relationship Mapping for MEDDPICC Analysis

Provides comprehensive stakeholder analysis with relationship hierarchies,
influence networks, and decision pathway mapping.

PATTERN_REF: STAKEHOLDER_RELATIONSHIP_MAPPING_PATTERN
"""

import logging
import re
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import networkx as nx
from datetime import datetime

logger = logging.getLogger(__name__)


class StakeholderRole(Enum):
    """Enhanced stakeholder role classifications."""
    ECONOMIC_BUYER = "economic_buyer"
    TECHNICAL_BUYER = "technical_buyer"
    USER_BUYER = "user_buyer"
    CHAMPION = "champion"
    STRONG_INFLUENCER = "strong_influencer"
    INFLUENCER = "influencer"
    TECHNICAL_DECISION_MAKER = "technical_decision_maker"
    GATEKEEPER = "gatekeeper"
    USER = "user"
    BLOCKER = "blocker"
    NEUTRAL = "neutral"


class RelationshipType(Enum):
    """Types of stakeholder relationships."""
    REPORTS_TO = "reports_to"
    MANAGES = "manages"
    INFLUENCES = "influences"
    COLLABORATES = "collaborates"
    SUPPORTS = "supports"
    OPPOSES = "opposes"
    ADVISES = "advises"
    APPROVES = "approves"
    BUDGET_AUTHORITY = "budget_authority"
    TECHNICAL_AUTHORITY = "technical_authority"


class InfluenceLevel(Enum):
    """Levels of stakeholder influence."""
    CRITICAL = "critical"  # Can kill the deal
    HIGH = "high"         # Major influence on decision
    MEDIUM = "medium"     # Some influence
    LOW = "low"          # Limited influence
    MINIMAL = "minimal"   # Very little influence


@dataclass
class Stakeholder:
    """Enhanced stakeholder representation."""
    name: str
    title: str
    department: str
    role_classification: StakeholderRole
    confidence: float
    evidence: str
    
    # Enhanced attributes
    seniority_level: int = 0  # 1=C-level, 2=VP, 3=Director, 4=Manager, 5=Individual
    budget_authority: bool = False
    technical_authority: bool = False
    influence_level: InfluenceLevel = InfluenceLevel.MEDIUM
    champion_strength: str = "none"  # none|developing|strong
    risk_level: str = "low"  # low|medium|high
    
    # Contact and engagement
    email: Optional[str] = None
    direct_contact: bool = False
    engagement_level: str = "unknown"  # high|medium|low|unknown
    
    # Decision involvement
    involved_in_decision: bool = True
    decision_influence: float = 0.5  # 0-1 scale
    veto_power: bool = False
    
    # Metadata
    first_mentioned: Optional[str] = None
    last_mentioned: Optional[str] = None
    mention_frequency: int = 0


@dataclass
class Relationship:
    """Enhanced relationship representation."""
    from_stakeholder: str
    to_stakeholder: str
    relationship_type: RelationshipType
    strength: float  # 0-1
    confidence: float  # 0-1
    evidence: str
    bidirectional: bool = False
    
    # Enhanced attributes
    formal_relationship: bool = True  # True for org chart, False for informal
    influence_direction: str = "neutral"  # positive|negative|neutral
    communication_frequency: str = "unknown"  # daily|weekly|monthly|occasional|unknown


@dataclass
class DecisionPathway:
    """Represents a decision-making pathway."""
    pathway_id: str
    stakeholders: List[str]
    pathway_type: str  # "approval"|"influence"|"veto"|"recommendation"
    criticality: str  # "critical"|"important"|"helpful"
    confidence: float
    description: str


@dataclass
class InfluenceNetwork:
    """Represents the overall influence network."""
    stakeholders: Dict[str, Stakeholder]
    relationships: List[Relationship]
    decision_pathways: List[DecisionPathway] = field(default_factory=list)
    influence_graph: nx.DiGraph = field(default_factory=nx.DiGraph)
    
    # Network analysis results
    most_influential: Optional[str] = None
    key_approvers: List[str] = field(default_factory=list)
    potential_blockers: List[str] = field(default_factory=list)
    champion_candidates: List[str] = field(default_factory=list)
    economic_buyer_candidates: List[str] = field(default_factory=list)


class StakeholderRelationshipMapper:
    """
    Enhanced stakeholder relationship mapping engine.
    ✅ Applied: STAKEHOLDER_RELATIONSHIP_MAPPING_PATTERN
    
    Provides comprehensive stakeholder analysis with relationship hierarchies,
    influence networks, and decision pathway identification.
    """
    
    def __init__(self):
        """Initialize the relationship mapper."""
        self.logger = logging.getLogger(self.__class__.__name__)
        self._initialize_patterns()
    
    def _initialize_patterns(self):
        """Initialize patterns for stakeholder and relationship detection."""
        
        # Seniority level detection patterns
        self.seniority_patterns = {
            1: [r'\b(ceo|chief executive|president|founder|owner)\b', r'\bcfo\b', r'\bcto\b', r'\bcoo\b'],
            2: [r'\bvp\b', r'\bvice president\b', r'\bsvp\b', r'\bsenior vice president\b'],
            3: [r'\bdirector\b', r'\bhead of\b', r'\bsenior director\b'],
            4: [r'\bmanager\b', r'\bteam lead\b', r'\blead\b', r'\bsupervisor\b'],
            5: [r'\banalyst\b', r'\bspecialist\b', r'\bassociate\b', r'\bcoordinator\b']
        }
        
        # Authority detection patterns
        self.budget_authority_patterns = [
            r'\bbudget\s+(authority|control|approval|responsible)\b',
            r'\bsigns?\s+off\s+on\s+budget\b',
            r'\bpurchasing\s+authority\b',
            r'\bcan\s+approve\s+spending\b',
            r'\bbudget\s+holder\b',
            r'\bfinancial\s+authority\b'
        ]
        
        self.technical_authority_patterns = [
            r'\btechnical\s+(authority|approval|decision)\b',
            r'\barchitecture\s+decisions?\b',
            r'\btechnology\s+choices?\b',
            r'\bsecurity\s+approval\b',
            r'\bintegration\s+decisions?\b',
            r'\btechnical\s+requirements\b'
        ]
        
        # Champion indicators
        self.champion_indicators = {
            'strong': [
                r'\bi\s+will\s+(champion|advocate|support|push)\b',
                r'\bi\s+am\s+(advocating|supporting|championing)\b',
                r'\bthis\s+is\s+exactly\s+what\s+we\s+need\b',
                r'\bi\s+will\s+help\s+(sell|convince|persuade)\b'
            ],
            'developing': [
                r'\bthis\s+looks\s+(good|promising|interesting)\b',
                r'\bi\s+like\s+this\s+(solution|approach)\b',
                r'\bwe\s+should\s+consider\s+this\b',
                r'\blets?\s+move\s+forward\b'
            ]
        }
        
        # Risk indicators
        self.risk_indicators = {
            'high': [
                r'\bi\s+have\s+concerns?\s+about\b',
                r'\bnot\s+sure\s+(this|if)\b',
                r'\bworried\s+about\b',
                r'\bmight\s+be\s+too\s+(expensive|complex|risky)\b',
                r'\bneed\s+to\s+think\s+about\s+this\b'
            ],
            'medium': [
                r'\bwhat\s+about\s+the\s+(cost|timeline|complexity)\b',
                r'\bhow\s+does\s+this\s+compare\s+to\b',
                r'\bwhat\s+are\s+the\s+alternatives\b'
            ]
        }
        
        # Relationship detection patterns
        self.relationship_patterns = {
            'reports_to': [
                r'(\w+)\s+reports\s+to\s+(\w+)',
                r'(\w+)\s+works\s+for\s+(\w+)',
                r'(\w+)\'s\s+manager\s+is\s+(\w+)',
                r'(\w+)\s+is\s+(\w+)\'s\s+boss'
            ],
            'manages': [
                r'(\w+)\s+manages\s+(\w+)',
                r'(\w+)\s+is\s+(\w+)\'s\s+manager',
                r'(\w+)\s+leads\s+(\w+)\'s\s+team',
                r'(\w+)\s+supervises\s+(\w+)'
            ],
            'collaborates': [
                r'(\w+)\s+and\s+(\w+)\s+work\s+together',
                r'(\w+)\s+collaborates\s+with\s+(\w+)',
                r'(\w+)\s+partners\s+with\s+(\w+)'
            ],
            'influences': [
                r'(\w+)\s+has\s+influence\s+over\s+(\w+)',
                r'(\w+)\s+advises\s+(\w+)',
                r'(\w+)\s+guides\s+(\w+)\'s\s+decisions?'
            ]
        }
    
    def enhance_stakeholder_analysis(self, basic_stakeholder_data: Dict[str, Any], 
                                   transcript: str) -> InfluenceNetwork:
        """
        Enhance basic stakeholder data with relationship mapping and influence analysis.
        
        Args:
            basic_stakeholder_data: Output from existing stakeholder intelligence agent
            transcript: Original transcript for additional analysis
            
        Returns:
            Enhanced influence network with relationships and pathways
        """
        try:
            # Extract stakeholders and enhance them
            stakeholders = self._enhance_stakeholders(
                basic_stakeholder_data.get('stakeholders', []), 
                transcript
            )
            
            # Extract and enhance relationships
            basic_relationships = basic_stakeholder_data.get('relationships', [])
            enhanced_relationships = self._enhance_relationships(
                basic_relationships, stakeholders, transcript
            )
            
            # Detect additional relationships from transcript
            inferred_relationships = self._infer_relationships_from_transcript(
                stakeholders, transcript
            )
            
            # Combine all relationships
            all_relationships = enhanced_relationships + inferred_relationships
            
            # Build influence network
            influence_network = self._build_influence_network(
                stakeholders, all_relationships
            )
            
            # Analyze decision pathways
            decision_pathways = self._analyze_decision_pathways(influence_network)
            influence_network.decision_pathways = decision_pathways
            
            # Perform network analysis
            self._perform_network_analysis(influence_network)
            
            return influence_network
            
        except Exception as e:
            self.logger.error(f"Error enhancing stakeholder analysis: {e}")
            # Return minimal network on error
            return InfluenceNetwork(
                stakeholders={},
                relationships=[],
                decision_pathways=[]
            )
    
    def _enhance_stakeholders(self, basic_stakeholders: List[Dict[str, Any]], 
                             transcript: str) -> Dict[str, Stakeholder]:
        """Enhance basic stakeholder data with additional analysis."""
        enhanced = {}
        
        for basic in basic_stakeholders:
            stakeholder = Stakeholder(
                name=basic.get('name', ''),
                title=basic.get('title', ''),
                department=basic.get('department', ''),
                role_classification=StakeholderRole(basic.get('role_classification', 'neutral')),
                confidence=basic.get('confidence', 0.0),
                evidence=basic.get('evidence', '')
            )
            
            # Enhance with additional analysis
            self._analyze_seniority_level(stakeholder)
            self._analyze_authority(stakeholder, transcript)
            self._analyze_champion_strength(stakeholder, transcript)
            self._analyze_influence_level(stakeholder)
            self._analyze_risk_level(stakeholder, transcript)
            self._analyze_engagement(stakeholder, transcript)
            
            enhanced[stakeholder.name] = stakeholder
        
        return enhanced
    
    def _analyze_seniority_level(self, stakeholder: Stakeholder):
        """Analyze stakeholder seniority level from title."""
        title_lower = stakeholder.title.lower()
        
        for level, patterns in self.seniority_patterns.items():
            for pattern in patterns:
                if re.search(pattern, title_lower):
                    stakeholder.seniority_level = level
                    return
        
        # Default to individual contributor level
        stakeholder.seniority_level = 5
    
    def _analyze_authority(self, stakeholder: Stakeholder, transcript: str):
        """Analyze budget and technical authority indicators."""
        # Create context around stakeholder mentions
        context = self._extract_stakeholder_context(stakeholder.name, transcript)
        context_lower = context.lower()
        
        # Check for budget authority
        for pattern in self.budget_authority_patterns:
            if re.search(pattern, context_lower):
                stakeholder.budget_authority = True
                break
        
        # Check for technical authority
        for pattern in self.technical_authority_patterns:
            if re.search(pattern, context_lower):
                stakeholder.technical_authority = True
                break
        
        # Infer from role and seniority
        if stakeholder.seniority_level <= 2:  # C-level or VP
            stakeholder.budget_authority = True
        
        if 'cto' in stakeholder.title.lower() or 'technical' in stakeholder.title.lower():
            stakeholder.technical_authority = True
    
    def _analyze_champion_strength(self, stakeholder: Stakeholder, transcript: str):
        """Analyze champion strength indicators."""
        context = self._extract_stakeholder_context(stakeholder.name, transcript)
        context_lower = context.lower()
        
        # Check for strong champion indicators
        for pattern in self.champion_indicators['strong']:
            if re.search(pattern, context_lower):
                stakeholder.champion_strength = 'strong'
                stakeholder.role_classification = StakeholderRole.CHAMPION
                return
        
        # Check for developing champion indicators
        for pattern in self.champion_indicators['developing']:
            if re.search(pattern, context_lower):
                stakeholder.champion_strength = 'developing'
                return
        
        # Default to none
        stakeholder.champion_strength = 'none'
    
    def _analyze_influence_level(self, stakeholder: Stakeholder):
        """Analyze overall influence level based on multiple factors."""
        influence_score = 0
        
        # Seniority contributes to influence
        if stakeholder.seniority_level == 1:  # C-level
            influence_score += 0.4
        elif stakeholder.seniority_level == 2:  # VP
            influence_score += 0.3
        elif stakeholder.seniority_level == 3:  # Director
            influence_score += 0.2
        
        # Authority contributes to influence
        if stakeholder.budget_authority:
            influence_score += 0.3
        if stakeholder.technical_authority:
            influence_score += 0.2
        
        # Champion strength contributes
        if stakeholder.champion_strength == 'strong':
            influence_score += 0.2
        elif stakeholder.champion_strength == 'developing':
            influence_score += 0.1
        
        # Map to influence level
        if influence_score >= 0.7:
            stakeholder.influence_level = InfluenceLevel.CRITICAL
        elif influence_score >= 0.5:
            stakeholder.influence_level = InfluenceLevel.HIGH
        elif influence_score >= 0.3:
            stakeholder.influence_level = InfluenceLevel.MEDIUM
        elif influence_score >= 0.1:
            stakeholder.influence_level = InfluenceLevel.LOW
        else:
            stakeholder.influence_level = InfluenceLevel.MINIMAL
        
        stakeholder.decision_influence = min(1.0, influence_score)
    
    def _analyze_risk_level(self, stakeholder: Stakeholder, transcript: str):
        """Analyze risk level (likelihood of being a blocker)."""
        context = self._extract_stakeholder_context(stakeholder.name, transcript)
        context_lower = context.lower()
        
        # Check for high risk indicators
        for pattern in self.risk_indicators['high']:
            if re.search(pattern, context_lower):
                stakeholder.risk_level = 'high'
                return
        
        # Check for medium risk indicators
        for pattern in self.risk_indicators['medium']:
            if re.search(pattern, context_lower):
                stakeholder.risk_level = 'medium'
                return
        
        # Default to low risk
        stakeholder.risk_level = 'low'
    
    def _analyze_engagement(self, stakeholder: Stakeholder, transcript: str):
        """Analyze engagement level from transcript."""
        # Count mentions and speaking time
        mentions = len(re.findall(rf'\b{re.escape(stakeholder.name)}\b', transcript, re.IGNORECASE))
        stakeholder.mention_frequency = mentions
        
        # Simple engagement assessment
        if mentions >= 10:
            stakeholder.engagement_level = 'high'
        elif mentions >= 5:
            stakeholder.engagement_level = 'medium'
        elif mentions >= 1:
            stakeholder.engagement_level = 'low'
        else:
            stakeholder.engagement_level = 'unknown'
    
    def _extract_stakeholder_context(self, stakeholder_name: str, transcript: str, 
                                   context_window: int = 200) -> str:
        """Extract context around stakeholder mentions for analysis."""
        contexts = []
        
        # Find all mentions of the stakeholder
        for match in re.finditer(rf'\b{re.escape(stakeholder_name)}\b', transcript, re.IGNORECASE):
            start = max(0, match.start() - context_window)
            end = min(len(transcript), match.end() + context_window)
            context = transcript[start:end]
            contexts.append(context)
        
        return ' '.join(contexts)
    
    def _enhance_relationships(self, basic_relationships: List[Dict[str, Any]], 
                             stakeholders: Dict[str, Stakeholder], 
                             transcript: str) -> List[Relationship]:
        """Enhance basic relationships with additional analysis."""
        enhanced = []
        
        for basic in basic_relationships:
            relationship = Relationship(
                from_stakeholder=basic.get('from_stakeholder', ''),
                to_stakeholder=basic.get('to_stakeholder', ''),
                relationship_type=RelationshipType(basic.get('relationship_type', 'collaborates')),
                strength=basic.get('strength', 0.5),
                confidence=basic.get('confidence', 0.5),
                evidence=basic.get('evidence', ''),
                bidirectional=basic.get('bidirectional', False)
            )
            
            # Enhance with additional analysis
            self._analyze_relationship_formality(relationship, stakeholders)
            self._analyze_influence_direction(relationship, transcript)
            
            enhanced.append(relationship)
        
        return enhanced
    
    def _infer_relationships_from_transcript(self, stakeholders: Dict[str, Stakeholder], 
                                           transcript: str) -> List[Relationship]:
        """Infer additional relationships from transcript analysis."""
        inferred = []
        
        # Use relationship patterns to find additional relationships
        for rel_type, patterns in self.relationship_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, transcript, re.IGNORECASE)
                for match in matches:
                    from_name = match.group(1)
                    to_name = match.group(2)
                    
                    # Verify stakeholders exist
                    if from_name in stakeholders and to_name in stakeholders:
                        relationship = Relationship(
                            from_stakeholder=from_name,
                            to_stakeholder=to_name,
                            relationship_type=RelationshipType(rel_type),
                            strength=0.7,  # Moderate strength for inferred
                            confidence=0.6,  # Lower confidence for inferred
                            evidence=match.group(0),
                            formal_relationship=True
                        )
                        
                        inferred.append(relationship)
        
        return inferred
    
    def _analyze_relationship_formality(self, relationship: Relationship, 
                                      stakeholders: Dict[str, Stakeholder]):
        """Analyze if relationship is formal (org chart) or informal."""
        from_stakeholder = stakeholders.get(relationship.from_stakeholder)
        to_stakeholder = stakeholders.get(relationship.to_stakeholder)
        
        if not from_stakeholder or not to_stakeholder:
            return
        
        # Formal relationships based on seniority and type
        formal_types = {RelationshipType.REPORTS_TO, RelationshipType.MANAGES, 
                       RelationshipType.APPROVES, RelationshipType.BUDGET_AUTHORITY}
        
        if relationship.relationship_type in formal_types:
            relationship.formal_relationship = True
        elif abs(from_stakeholder.seniority_level - to_stakeholder.seniority_level) >= 2:
            relationship.formal_relationship = True
        else:
            relationship.formal_relationship = False
    
    def _analyze_influence_direction(self, relationship: Relationship, transcript: str):
        """Analyze the direction of influence in the relationship."""
        # Extract context around the relationship
        evidence_context = relationship.evidence.lower()
        
        # Look for positive/negative indicators
        positive_indicators = ['supports', 'advocates', 'recommends', 'endorses']
        negative_indicators = ['opposes', 'concerns', 'worried', 'against']
        
        if any(indicator in evidence_context for indicator in positive_indicators):
            relationship.influence_direction = 'positive'
        elif any(indicator in evidence_context for indicator in negative_indicators):
            relationship.influence_direction = 'negative'
        else:
            relationship.influence_direction = 'neutral'
    
    def _build_influence_network(self, stakeholders: Dict[str, Stakeholder], 
                               relationships: List[Relationship]) -> InfluenceNetwork:
        """Build the influence network graph."""
        network = InfluenceNetwork(
            stakeholders=stakeholders,
            relationships=relationships,
            decision_pathways=[]
        )
        
        # Build NetworkX graph for analysis
        G = nx.DiGraph()
        
        # Add nodes with attributes
        for name, stakeholder in stakeholders.items():
            G.add_node(name, 
                      influence=stakeholder.decision_influence,
                      seniority=stakeholder.seniority_level,
                      authority=stakeholder.budget_authority or stakeholder.technical_authority)
        
        # Add edges with weights
        for relationship in relationships:
            if relationship.from_stakeholder in G and relationship.to_stakeholder in G:
                G.add_edge(relationship.from_stakeholder, 
                          relationship.to_stakeholder,
                          weight=relationship.strength,
                          type=relationship.relationship_type.value)
        
        network.influence_graph = G
        return network
    
    def _analyze_decision_pathways(self, network: InfluenceNetwork) -> List[DecisionPathway]:
        """Analyze potential decision-making pathways."""
        pathways = []
        
        # Find approval pathways (budget authority chains)
        budget_holders = [name for name, stakeholder in network.stakeholders.items() 
                         if stakeholder.budget_authority]
        
        for holder in budget_holders:
            pathway = DecisionPathway(
                pathway_id=f"budget_approval_{holder}",
                stakeholders=[holder],
                pathway_type="approval",
                criticality="critical",
                confidence=0.8,
                description=f"Budget approval pathway through {holder}"
            )
            pathways.append(pathway)
        
        # Find influence pathways (champion to decision maker)
        champions = [name for name, stakeholder in network.stakeholders.items() 
                    if stakeholder.champion_strength in ['strong', 'developing']]
        
        for champion in champions:
            # Find path to budget holders
            for holder in budget_holders:
                if champion != holder:
                    try:
                        if nx.has_path(network.influence_graph, champion, holder):
                            path = nx.shortest_path(network.influence_graph, champion, holder)
                            pathway = DecisionPathway(
                                pathway_id=f"influence_{champion}_to_{holder}",
                                stakeholders=path,
                                pathway_type="influence",
                                criticality="important",
                                confidence=0.6,
                                description=f"Influence pathway from {champion} to {holder}"
                            )
                            pathways.append(pathway)
                    except nx.NetworkXNoPath:
                        continue
        
        return pathways
    
    def _perform_network_analysis(self, network: InfluenceNetwork):
        """Perform network analysis to identify key stakeholders."""
        G = network.influence_graph
        
        if len(G) == 0:
            return
        
        try:
            # Find most influential (highest weighted centrality)
            if len(G) > 1:
                centrality = nx.eigenvector_centrality(G, weight='weight', max_iter=1000)
                network.most_influential = max(centrality, key=centrality.get)
            
            # Identify key approvers (budget authority + high influence)
            network.key_approvers = [
                name for name, stakeholder in network.stakeholders.items()
                if stakeholder.budget_authority and stakeholder.influence_level in 
                [InfluenceLevel.CRITICAL, InfluenceLevel.HIGH]
            ]
            
            # Identify potential blockers (high influence + high risk)
            network.potential_blockers = [
                name for name, stakeholder in network.stakeholders.items()
                if stakeholder.influence_level in [InfluenceLevel.CRITICAL, InfluenceLevel.HIGH] 
                and stakeholder.risk_level == 'high'
            ]
            
            # Identify champion candidates
            network.champion_candidates = [
                name for name, stakeholder in network.stakeholders.items()
                if stakeholder.champion_strength in ['strong', 'developing'] or
                (stakeholder.influence_level in [InfluenceLevel.HIGH, InfluenceLevel.MEDIUM] 
                 and stakeholder.risk_level == 'low')
            ]
            
            # Identify economic buyer candidates
            network.economic_buyer_candidates = [
                name for name, stakeholder in network.stakeholders.items()
                if stakeholder.budget_authority and stakeholder.seniority_level <= 2
            ]
            
        except Exception as e:
            self.logger.error(f"Error in network analysis: {e}")


def enhance_stakeholder_relationships(basic_data: Dict[str, Any], transcript: str) -> Dict[str, Any]:
    """
    Convenience function to enhance stakeholder data with relationship mapping.
    
    Args:
        basic_data: Basic stakeholder data from existing agent
        transcript: Original transcript
        
    Returns:
        Enhanced stakeholder data with relationship mapping
    """
    mapper = StakeholderRelationshipMapper()
    network = mapper.enhance_stakeholder_analysis(basic_data, transcript)
    
    # Convert back to dictionary format
    return {
        'enhanced_stakeholders': {
            name: {
                'name': s.name,
                'title': s.title,
                'department': s.department,
                'role_classification': s.role_classification.value,
                'confidence': s.confidence,
                'evidence': s.evidence,
                'seniority_level': s.seniority_level,
                'budget_authority': s.budget_authority,
                'technical_authority': s.technical_authority,
                'influence_level': s.influence_level.value,
                'champion_strength': s.champion_strength,
                'risk_level': s.risk_level,
                'engagement_level': s.engagement_level,
                'decision_influence': s.decision_influence,
                'mention_frequency': s.mention_frequency
            } for name, s in network.stakeholders.items()
        },
        'enhanced_relationships': [
            {
                'from_stakeholder': r.from_stakeholder,
                'to_stakeholder': r.to_stakeholder,
                'relationship_type': r.relationship_type.value,
                'strength': r.strength,
                'confidence': r.confidence,
                'evidence': r.evidence,
                'bidirectional': r.bidirectional,
                'formal_relationship': r.formal_relationship,
                'influence_direction': r.influence_direction
            } for r in network.relationships
        ],
        'decision_pathways': [
            {
                'pathway_id': p.pathway_id,
                'stakeholders': p.stakeholders,
                'pathway_type': p.pathway_type,
                'criticality': p.criticality,
                'confidence': p.confidence,
                'description': p.description
            } for p in network.decision_pathways
        ],
        'network_analysis': {
            'most_influential': network.most_influential,
            'key_approvers': network.key_approvers,
            'potential_blockers': network.potential_blockers,
            'champion_candidates': network.champion_candidates,
            'economic_buyer_candidates': network.economic_buyer_candidates
        }
    }