"""
✅ Applied: RISK_SIGNAL_DETECTION_PATTERN
Risk Signal Detection for MEDDPICC Analysis

Provides early warning system for deal risks through conversation analysis,
stakeholder sentiment monitoring, and process deviation detection.

PATTERN_REF: RISK_SIGNAL_DETECTION_PATTERN
"""

import logging
import re
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class RiskCategory(Enum):
    """Categories of deal risks."""
    BUDGET = "budget"
    TIMELINE = "timeline"
    TECHNICAL = "technical"
    STAKEHOLDER = "stakeholder"
    COMPETITIVE = "competitive"
    PROCESS = "process"
    AUTHORITY = "authority"
    SCOPE = "scope"
    RELATIONSHIP = "relationship"


class RiskSeverity(Enum):
    """Severity levels for risk signals."""
    CRITICAL = "critical"  # Deal-killing risk
    HIGH = "high"         # Major concern requiring immediate action
    MEDIUM = "medium"     # Moderate risk needing attention
    LOW = "low"          # Minor risk to monitor
    WATCH = "watch"      # Early warning signal


class RiskUrgency(Enum):
    """Urgency levels for risk response."""
    IMMEDIATE = "immediate"    # Address within 24 hours
    URGENT = "urgent"         # Address within week
    PLANNED = "planned"       # Address in next meeting
    MONITOR = "monitor"       # Continue monitoring


@dataclass
class RiskSignal:
    """Individual risk signal detected in conversation."""
    signal_id: str
    category: RiskCategory
    severity: RiskSeverity
    urgency: RiskUrgency
    title: str
    description: str
    evidence: str
    confidence: float  # 0-1
    
    # Context
    stakeholder_involved: Optional[str] = None
    timestamp_detected: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    context_before: str = ""
    context_after: str = ""
    
    # Impact assessment
    deal_impact: str = "unknown"  # positive|negative|neutral|unknown
    probability: float = 0.5  # 0-1 likelihood of risk materializing
    business_impact: str = ""  # description of business consequence
    
    # Response
    suggested_actions: List[str] = field(default_factory=list)
    escalation_needed: bool = False
    follow_up_required: bool = True


@dataclass
class RiskProfile:
    """Overall risk profile for a deal/conversation."""
    overall_risk_score: float  # 0-1 (0=low risk, 1=high risk)
    risk_trend: str  # "improving"|"stable"|"deteriorating"|"unknown"
    critical_risks: List[RiskSignal]
    high_risks: List[RiskSignal]
    medium_risks: List[RiskSignal]
    low_risks: List[RiskSignal]
    watch_signals: List[RiskSignal]
    
    # Analysis metadata
    total_signals: int = 0
    confidence_weighted_score: float = 0.0
    primary_risk_categories: List[str] = field(default_factory=list)
    immediate_actions_needed: int = 0
    
    # Recommendations
    next_steps: List[str] = field(default_factory=list)
    escalation_recommended: bool = False
    meeting_objectives: List[str] = field(default_factory=list)


class RiskSignalDetector:
    """
    Risk Signal Detection Engine for MEDDPICC Analysis.
    ✅ Applied: RISK_SIGNAL_DETECTION_PATTERN
    
    Detects early warning signals and potential deal risks through
    conversation analysis, sentiment monitoring, and pattern recognition.
    """
    
    def __init__(self):
        """Initialize the risk signal detector."""
        self.logger = logging.getLogger(self.__class__.__name__)
        self._initialize_risk_patterns()
    
    def _initialize_risk_patterns(self):
        """Initialize patterns for detecting various risk signals."""
        
        # Budget risk patterns
        self.budget_risk_patterns = {
            'critical': [
                r'\bno\s+budget\b',
                r'\bbudget\s+(cut|frozen|eliminated)\b',
                r'\bcan\'?t\s+afford\b',
                r'\btoo\s+expensive\b',
                r'\bover\s+budget\b',
                r'\bbudget\s+concerns?\b'
            ],
            'high': [
                r'\bbudget\s+(tight|limited|constrained)\b',
                r'\bneed\s+to\s+(reduce|lower)\s+cost\b',
                r'\blooking\s+for\s+cheaper\b',
                r'\bprice\s+is\s+an?\s+issue\b',
                r'\bbudget\s+approval\s+(difficult|challenging)\b'
            ],
            'medium': [
                r'\bwhat\'?s\s+the\s+cost\b',
                r'\bhow\s+much\s+(will\s+this\s+)?cost\b',
                r'\bbudget\s+planning\b',
                r'\bneed\s+to\s+see\s+pricing\b'
            ]
        }
        
        # Timeline risk patterns
        self.timeline_risk_patterns = {
            'critical': [
                r'\bno\s+rush\b',
                r'\bnot\s+urgent\b',
                r'\bmight\s+delay\b',
                r'\bpushing\s+(back|out)\b',
                r'\bpostponing\b',
                r'\bon\s+hold\b'
            ],
            'high': [
                r'\btight\s+timeline\b',
                r'\bneed\s+more\s+time\b',
                r'\btimeline\s+(aggressive|challenging)\b',
                r'\bdeadline\s+(might\s+)?slip\b',
                r'\brushed?\s+timeline\b'
            ],
            'medium': [
                r'\bwhen\s+do\s+we\s+need\s+this\b',
                r'\btimeline\s+(unclear|flexible)\b',
                r'\bdepends\s+on\s+timing\b'
            ]
        }
        
        # Technical risk patterns
        self.technical_risk_patterns = {
            'critical': [
                r'\bwon\'?t\s+integrate\b',
                r'\btechnical\s+(blocker|issue)\b',
                r'\bsecurity\s+(concern|risk)\b',
                r'\barchitecture\s+conflict\b',
                r'\bcan\'?t\s+support\b'
            ],
            'high': [
                r'\bintegration\s+(complex|difficult|challenging)\b',
                r'\btechnical\s+(concerns?|challenges?)\b',
                r'\bsecurity\s+(review|evaluation)\s+needed\b',
                r'\bperformance\s+(issues?|concerns?)\b',
                r'\bscalability\s+(questions?|issues?)\b'
            ],
            'medium': [
                r'\bhow\s+does\s+(this\s+)?integrate\b',
                r'\btechnical\s+requirements\b',
                r'\bneed\s+technical\s+review\b'
            ]
        }
        
        # Stakeholder risk patterns  
        self.stakeholder_risk_patterns = {
            'critical': [
                r'\bi\s+don\'?t\s+(like|want|support)\b',
                r'\bthis\s+won\'?t\s+work\b',
                r'\bnot\s+the\s+right\s+(solution|fit)\b',
                r'\bstrongly\s+(oppose|disagree)\b',
                r'\bveto\b'
            ],
            'high': [
                r'\bi\s+have\s+(concerns?|doubts?|reservations?)\b',
                r'\bnot\s+convinced\b',
                r'\bskeptical\b',
                r'\bworried\s+about\b',
                r'\bunsure\s+about\b',
                r'\breluctant\b'
            ],
            'medium': [
                r'\bneed\s+to\s+(think|consider)\b',
                r'\blet\s+me\s+(think|review)\b',
                r'\bhave\s+questions?\b',
                r'\bneed\s+more\s+information\b'
            ]
        }
        
        # Competitive risk patterns
        self.competitive_risk_patterns = {
            'critical': [
                r'\balready\s+(decided|chosen)\b',
                r'\bgoing\s+with\s+\w+\b',
                r'\bsigned\s+with\b',
                r'\bcommitted\s+to\b'
            ],
            'high': [
                r'\bconsidering\s+other\s+(options|vendors)\b',
                r'\blooking\s+at\s+\w+\s+(too|also)\b',
                r'\bcomparing\s+(you\s+)?(with|to)\b',
                r'\bbetter\s+(offer|proposal)\b',
                r'\b\w+\s+is\s+cheaper\b'
            ],
            'medium': [
                r'\bwhat\s+makes\s+you\s+different\b',
                r'\bhow\s+do\s+you\s+compare\b',
                r'\bother\s+options\b'
            ]
        }
        
        # Authority risk patterns
        self.authority_risk_patterns = {
            'critical': [
                r'\bi\s+don\'?t\s+(decide|choose)\b',
                r'\bnot\s+my\s+(decision|call)\b',
                r'\bsomeone\s+else\s+decides\b'
            ],
            'high': [
                r'\bneed\s+approval\s+from\b',
                r'\bhave\s+to\s+(check|ask)\b',
                r'\bnot\s+sure\s+i\s+can\s+(approve|decide)\b',
                r'\babove\s+my\s+(level|authority)\b'
            ],
            'medium': [
                r'\bwho\s+makes\s+the\s+(final\s+)?decision\b',
                r'\bdecision\s+process\b'
            ]
        }
        
        # Process risk patterns
        self.process_risk_patterns = {
            'high': [
                r'\b(legal|compliance|procurement)\s+review\s+required\b',
                r'\bcomplex\s+(approval\s+)?process\b',
                r'\bmultiple\s+approvals?\s+needed\b',
                r'\blong\s+(approval\s+)?process\b'
            ],
            'medium': [
                r'\bneed\s+to\s+follow\s+process\b',
                r'\bapproval\s+process\b',
                r'\binternal\s+procedures?\b'
            ]
        }
        
        # Positive signals (risk mitigation)
        self.positive_signals = [
            r'\bexcited\s+about\b',
            r'\bperfect\s+(fit|solution)\b',
            r'\bexactly\s+what\s+we\s+need\b',
            r'\bi\s+love\s+(this|it)\b',
            r'\blets?\s+(move\s+)?forward\b',
            r'\bwhen\s+can\s+we\s+(start|begin)\b',
            r'\bhow\s+soon\s+can\s+we\b'
        ]
        
        # Sentiment indicators
        self.negative_sentiment_words = [
            'concerned', 'worried', 'doubt', 'skeptical', 'hesitant', 'reluctant',
            'disappointed', 'frustrated', 'confused', 'uncertain', 'unsure'
        ]
        
        self.positive_sentiment_words = [
            'excited', 'impressed', 'confident', 'optimistic', 'enthusiastic',
            'pleased', 'satisfied', 'convinced', 'ready', 'committed'
        ]
    
    def detect_risk_signals(self, content: str, stakeholder_data: Optional[Dict[str, Any]] = None,
                           meddpicc_data: Optional[Dict[str, Any]] = None) -> RiskProfile:
        """
        Detect risk signals from conversation content.
        
        Args:
            content: Transcript or conversation content
            stakeholder_data: Optional stakeholder analysis data
            meddpicc_data: Optional MEDDPICC analysis data
            
        Returns:
            Comprehensive risk profile with detected signals
        """
        try:
            signals = []
            content_lower = content.lower()
            
            # Detect category-specific risks
            signals.extend(self._detect_budget_risks(content, content_lower))
            signals.extend(self._detect_timeline_risks(content, content_lower))
            signals.extend(self._detect_technical_risks(content, content_lower))
            signals.extend(self._detect_stakeholder_risks(content, content_lower))
            signals.extend(self._detect_competitive_risks(content, content_lower))
            signals.extend(self._detect_authority_risks(content, content_lower))
            signals.extend(self._detect_process_risks(content, content_lower))
            
            # Enhance with stakeholder data if available
            if stakeholder_data:
                signals.extend(self._detect_stakeholder_based_risks(stakeholder_data))
            
            # Enhance with MEDDPICC data if available
            if meddpicc_data:
                signals.extend(self._detect_meddpicc_based_risks(meddpicc_data))
            
            # Detect sentiment-based risks
            signals.extend(self._detect_sentiment_risks(content, content_lower))
            
            # Build risk profile
            risk_profile = self._build_risk_profile(signals, content)
            
            return risk_profile
            
        except Exception as e:
            self.logger.error(f"Error detecting risk signals: {e}")
            return RiskProfile(
                overall_risk_score=0.5,
                risk_trend="unknown",
                critical_risks=[],
                high_risks=[],
                medium_risks=[],
                low_risks=[],
                watch_signals=[]
            )
    
    def _detect_budget_risks(self, content: str, content_lower: str) -> List[RiskSignal]:
        """Detect budget-related risk signals."""
        signals = []
        
        for severity, patterns in self.budget_risk_patterns.items():
            for pattern in patterns:
                matches = list(re.finditer(pattern, content_lower))
                for match in matches:
                    context = self._extract_context(content, match.start(), match.end())
                    
                    signal = RiskSignal(
                        signal_id=f"budget_{severity}_{len(signals)}",
                        category=RiskCategory.BUDGET,
                        severity=RiskSeverity(severity),
                        urgency=self._determine_urgency(RiskSeverity(severity), RiskCategory.BUDGET),
                        title=f"Budget concern detected",
                        description=f"Budget-related risk signal: {match.group()}",
                        evidence=match.group(),
                        confidence=self._calculate_confidence(severity, pattern, content_lower),
                        context_before=context['before'],
                        context_after=context['after'],
                        deal_impact="negative",
                        probability=self._estimate_probability(severity, RiskCategory.BUDGET),
                        suggested_actions=self._get_budget_risk_actions(severity)
                    )
                    signals.append(signal)
        
        return signals
    
    def _detect_timeline_risks(self, content: str, content_lower: str) -> List[RiskSignal]:
        """Detect timeline-related risk signals."""
        signals = []
        
        for severity, patterns in self.timeline_risk_patterns.items():
            for pattern in patterns:
                matches = list(re.finditer(pattern, content_lower))
                for match in matches:
                    context = self._extract_context(content, match.start(), match.end())
                    
                    signal = RiskSignal(
                        signal_id=f"timeline_{severity}_{len(signals)}",
                        category=RiskCategory.TIMELINE,
                        severity=RiskSeverity(severity),
                        urgency=self._determine_urgency(RiskSeverity(severity), RiskCategory.TIMELINE),
                        title=f"Timeline concern detected",
                        description=f"Timeline-related risk signal: {match.group()}",
                        evidence=match.group(),
                        confidence=self._calculate_confidence(severity, pattern, content_lower),
                        context_before=context['before'],
                        context_after=context['after'],
                        deal_impact="negative",
                        probability=self._estimate_probability(severity, RiskCategory.TIMELINE),
                        suggested_actions=self._get_timeline_risk_actions(severity)
                    )
                    signals.append(signal)
        
        return signals
    
    def _detect_technical_risks(self, content: str, content_lower: str) -> List[RiskSignal]:
        """Detect technical-related risk signals."""
        signals = []
        
        for severity, patterns in self.technical_risk_patterns.items():
            for pattern in patterns:
                matches = list(re.finditer(pattern, content_lower))
                for match in matches:
                    context = self._extract_context(content, match.start(), match.end())
                    
                    signal = RiskSignal(
                        signal_id=f"technical_{severity}_{len(signals)}",
                        category=RiskCategory.TECHNICAL,
                        severity=RiskSeverity(severity),
                        urgency=self._determine_urgency(RiskSeverity(severity), RiskCategory.TECHNICAL),
                        title=f"Technical concern detected",
                        description=f"Technical risk signal: {match.group()}",
                        evidence=match.group(),
                        confidence=self._calculate_confidence(severity, pattern, content_lower),
                        context_before=context['before'],
                        context_after=context['after'],
                        deal_impact="negative",
                        probability=self._estimate_probability(severity, RiskCategory.TECHNICAL),
                        suggested_actions=self._get_technical_risk_actions(severity)
                    )
                    signals.append(signal)
        
        return signals
    
    def _detect_stakeholder_risks(self, content: str, content_lower: str) -> List[RiskSignal]:
        """Detect stakeholder-related risk signals."""
        signals = []
        
        for severity, patterns in self.stakeholder_risk_patterns.items():
            for pattern in patterns:
                matches = list(re.finditer(pattern, content_lower))
                for match in matches:
                    context = self._extract_context(content, match.start(), match.end())
                    
                    signal = RiskSignal(
                        signal_id=f"stakeholder_{severity}_{len(signals)}",
                        category=RiskCategory.STAKEHOLDER,
                        severity=RiskSeverity(severity),
                        urgency=self._determine_urgency(RiskSeverity(severity), RiskCategory.STAKEHOLDER),
                        title=f"Stakeholder concern detected",
                        description=f"Stakeholder resistance signal: {match.group()}",
                        evidence=match.group(),
                        confidence=self._calculate_confidence(severity, pattern, content_lower),
                        context_before=context['before'],
                        context_after=context['after'],
                        deal_impact="negative",
                        probability=self._estimate_probability(severity, RiskCategory.STAKEHOLDER),
                        suggested_actions=self._get_stakeholder_risk_actions(severity)
                    )
                    signals.append(signal)
        
        return signals
    
    def _detect_competitive_risks(self, content: str, content_lower: str) -> List[RiskSignal]:
        """Detect competitive-related risk signals."""
        signals = []
        
        for severity, patterns in self.competitive_risk_patterns.items():
            for pattern in patterns:
                matches = list(re.finditer(pattern, content_lower))
                for match in matches:
                    context = self._extract_context(content, match.start(), match.end())
                    
                    signal = RiskSignal(
                        signal_id=f"competitive_{severity}_{len(signals)}",
                        category=RiskCategory.COMPETITIVE,
                        severity=RiskSeverity(severity),
                        urgency=self._determine_urgency(RiskSeverity(severity), RiskCategory.COMPETITIVE),
                        title=f"Competitive threat detected",
                        description=f"Competitive risk signal: {match.group()}",
                        evidence=match.group(),
                        confidence=self._calculate_confidence(severity, pattern, content_lower),
                        context_before=context['before'],
                        context_after=context['after'],
                        deal_impact="negative",
                        probability=self._estimate_probability(severity, RiskCategory.COMPETITIVE),
                        suggested_actions=self._get_competitive_risk_actions(severity)
                    )
                    signals.append(signal)
        
        return signals
    
    def _detect_authority_risks(self, content: str, content_lower: str) -> List[RiskSignal]:
        """Detect authority-related risk signals."""
        signals = []
        
        for severity, patterns in self.authority_risk_patterns.items():
            for pattern in patterns:
                matches = list(re.finditer(pattern, content_lower))
                for match in matches:
                    context = self._extract_context(content, match.start(), match.end())
                    
                    signal = RiskSignal(
                        signal_id=f"authority_{severity}_{len(signals)}",
                        category=RiskCategory.AUTHORITY,
                        severity=RiskSeverity(severity),
                        urgency=self._determine_urgency(RiskSeverity(severity), RiskCategory.AUTHORITY),
                        title=f"Authority concern detected",
                        description=f"Decision authority risk: {match.group()}",
                        evidence=match.group(),
                        confidence=self._calculate_confidence(severity, pattern, content_lower),
                        context_before=context['before'],
                        context_after=context['after'],
                        deal_impact="negative",
                        probability=self._estimate_probability(severity, RiskCategory.AUTHORITY),
                        suggested_actions=self._get_authority_risk_actions(severity)
                    )
                    signals.append(signal)
        
        return signals
    
    def _detect_process_risks(self, content: str, content_lower: str) -> List[RiskSignal]:
        """Detect process-related risk signals."""
        signals = []
        
        for severity, patterns in self.process_risk_patterns.items():
            for pattern in patterns:
                matches = list(re.finditer(pattern, content_lower))
                for match in matches:
                    context = self._extract_context(content, match.start(), match.end())
                    
                    signal = RiskSignal(
                        signal_id=f"process_{severity}_{len(signals)}",
                        category=RiskCategory.PROCESS,
                        severity=RiskSeverity(severity),
                        urgency=self._determine_urgency(RiskSeverity(severity), RiskCategory.PROCESS),
                        title=f"Process complexity detected",
                        description=f"Process risk signal: {match.group()}",
                        evidence=match.group(),
                        confidence=self._calculate_confidence(severity, pattern, content_lower),
                        context_before=context['before'],
                        context_after=context['after'],
                        deal_impact="negative",
                        probability=self._estimate_probability(severity, RiskCategory.PROCESS),
                        suggested_actions=self._get_process_risk_actions(severity)
                    )
                    signals.append(signal)
        
        return signals
    
    def _detect_sentiment_risks(self, content: str, content_lower: str) -> List[RiskSignal]:
        """Detect sentiment-based risk signals."""
        signals = []
        
        # Count negative vs positive sentiment words
        negative_count = sum(1 for word in self.negative_sentiment_words if word in content_lower)
        positive_count = sum(1 for word in self.positive_sentiment_words if word in content_lower)
        
        if negative_count > positive_count and negative_count >= 2:
            sentiment_ratio = negative_count / max(positive_count, 1)
            
            if sentiment_ratio >= 3:
                severity = RiskSeverity.HIGH
            elif sentiment_ratio >= 2:
                severity = RiskSeverity.MEDIUM
            else:
                severity = RiskSeverity.LOW
            
            signal = RiskSignal(
                signal_id=f"sentiment_negative_{len(signals)}",
                category=RiskCategory.RELATIONSHIP,
                severity=severity,
                urgency=self._determine_urgency(severity, RiskCategory.RELATIONSHIP),
                title="Negative sentiment detected",
                description=f"Overall negative sentiment in conversation (ratio: {sentiment_ratio:.1f})",
                evidence=f"Negative words: {negative_count}, Positive words: {positive_count}",
                confidence=min(0.8, sentiment_ratio / 4),
                deal_impact="negative",
                probability=0.6,
                suggested_actions=["Address concerns directly", "Improve relationship building", "Schedule follow-up to clarify issues"]
            )
            signals.append(signal)
        
        return signals
    
    def _detect_stakeholder_based_risks(self, stakeholder_data: Dict[str, Any]) -> List[RiskSignal]:
        """Detect risks based on stakeholder analysis."""
        signals = []
        
        # Check for potential blockers
        network_analysis = stakeholder_data.get('network_analysis', {})
        potential_blockers = network_analysis.get('potential_blockers', [])
        
        if potential_blockers:
            signal = RiskSignal(
                signal_id=f"stakeholder_blockers_{len(signals)}",
                category=RiskCategory.STAKEHOLDER,
                severity=RiskSeverity.HIGH,
                urgency=RiskUrgency.URGENT,
                title="Potential blockers identified",
                description=f"Stakeholder analysis identified {len(potential_blockers)} potential blockers",
                evidence=f"Potential blockers: {', '.join(potential_blockers)}",
                confidence=0.8,
                deal_impact="negative",
                probability=0.7,
                suggested_actions=[
                    "Develop strategies to address blocker concerns",
                    "Schedule 1:1 meetings with potential blockers",
                    "Prepare counter-arguments and alternatives"
                ]
            )
            signals.append(signal)
        
        # Check for lack of champions
        champion_candidates = network_analysis.get('champion_candidates', [])
        if len(champion_candidates) == 0:
            signal = RiskSignal(
                signal_id=f"no_champions_{len(signals)}",
                category=RiskCategory.STAKEHOLDER,
                severity=RiskSeverity.HIGH,
                urgency=RiskUrgency.URGENT,
                title="No champion candidates identified",
                description="Stakeholder analysis found no strong champion candidates",
                evidence="Champion candidates: 0",
                confidence=0.9,
                deal_impact="negative",
                probability=0.8,
                suggested_actions=[
                    "Identify and cultivate potential champions",
                    "Provide enablement materials to supportive stakeholders",
                    "Build stronger relationships with key influencers"
                ]
            )
            signals.append(signal)
        
        return signals
    
    def _detect_meddpicc_based_risks(self, meddpicc_data: Dict[str, Any]) -> List[RiskSignal]:
        """Detect risks based on MEDDPICC analysis."""
        signals = []
        
        # Check for missing economic buyer
        economic_buyer = meddpicc_data.get('economic_buyer', {})
        if not economic_buyer.get('identified') or economic_buyer.get('confidence', 0) < 0.5:
            signal = RiskSignal(
                signal_id=f"missing_economic_buyer_{len(signals)}",
                category=RiskCategory.AUTHORITY,
                severity=RiskSeverity.HIGH,
                urgency=RiskUrgency.URGENT,
                title="Economic buyer not identified",
                description="No clear economic buyer identified in MEDDPICC analysis",
                evidence=f"Economic buyer confidence: {economic_buyer.get('confidence', 0):.2f}",
                confidence=0.9,
                deal_impact="negative",
                probability=0.8,
                suggested_actions=[
                    "Map organizational structure to find budget authority",
                    "Request introduction to decision maker",
                    "Clarify budget approval process"
                ]
            )
            signals.append(signal)
        
        # Check for weak champion
        champion = meddpicc_data.get('champion', {})
        champion_strength = champion.get('strength', 'none')
        if champion_strength == 'none':
            signal = RiskSignal(
                signal_id=f"weak_champion_{len(signals)}",
                category=RiskCategory.STAKEHOLDER,
                severity=RiskSeverity.MEDIUM,
                urgency=RiskUrgency.PLANNED,
                title="No strong champion identified",
                description="MEDDPICC analysis shows no strong champion support",
                evidence=f"Champion strength: {champion_strength}",
                confidence=0.8,
                deal_impact="negative",
                probability=0.6,
                suggested_actions=[
                    "Identify potential champion candidates",
                    "Build stronger advocacy within organization",
                    "Provide champion enablement materials"
                ]
            )
            signals.append(signal)
        
        return signals
    
    def _extract_context(self, content: str, start: int, end: int, window: int = 100) -> Dict[str, str]:
        """Extract context around a match for better analysis."""
        before_start = max(0, start - window)
        after_end = min(len(content), end + window)
        
        return {
            'before': content[before_start:start],
            'after': content[end:after_end]
        }
    
    def _calculate_confidence(self, severity: str, pattern: str, content: str) -> float:
        """Calculate confidence score for a risk signal."""
        base_confidence = {
            'critical': 0.9,
            'high': 0.8,
            'medium': 0.7,
            'low': 0.6
        }.get(severity, 0.5)
        
        # Adjust based on pattern specificity
        if len(pattern) > 20:  # More specific patterns get higher confidence
            base_confidence += 0.1
        
        # Adjust based on frequency
        pattern_count = len(re.findall(pattern, content))
        if pattern_count > 1:
            base_confidence += min(0.1, pattern_count * 0.02)
        
        return min(1.0, base_confidence)
    
    def _determine_urgency(self, severity: RiskSeverity, category: RiskCategory) -> RiskUrgency:
        """Determine urgency based on severity and category."""
        if severity == RiskSeverity.CRITICAL:
            return RiskUrgency.IMMEDIATE
        elif severity == RiskSeverity.HIGH:
            if category in [RiskCategory.BUDGET, RiskCategory.STAKEHOLDER, RiskCategory.COMPETITIVE]:
                return RiskUrgency.URGENT
            else:
                return RiskUrgency.PLANNED
        elif severity == RiskSeverity.MEDIUM:
            return RiskUrgency.PLANNED
        else:
            return RiskUrgency.MONITOR
    
    def _estimate_probability(self, severity: str, category: RiskCategory) -> float:
        """Estimate probability of risk materializing."""
        base_probability = {
            'critical': 0.8,
            'high': 0.6,
            'medium': 0.4,
            'low': 0.2
        }.get(severity, 0.3)
        
        # Adjust based on category
        if category in [RiskCategory.BUDGET, RiskCategory.STAKEHOLDER]:
            base_probability += 0.1
        
        return min(1.0, base_probability)
    
    def _get_budget_risk_actions(self, severity: str) -> List[str]:
        """Get suggested actions for budget risks."""
        actions = {
            'critical': [
                "Explore alternative pricing models",
                "Discuss phased implementation approach",
                "Present ROI calculator and business case",
                "Consider reducing scope to fit budget"
            ],
            'high': [
                "Provide detailed cost breakdown",
                "Demonstrate clear ROI and payback period",
                "Explore financing options",
                "Present competitive pricing analysis"
            ],
            'medium': [
                "Prepare pricing proposal",
                "Schedule budget discussion meeting",
                "Provide cost-benefit analysis"
            ]
        }
        return actions.get(severity, ["Monitor budget discussions"])
    
    def _get_timeline_risk_actions(self, severity: str) -> List[str]:
        """Get suggested actions for timeline risks."""
        actions = {
            'critical': [
                "Reassess timeline requirements",
                "Propose phased implementation",
                "Identify critical path dependencies",
                "Consider interim solutions"
            ],
            'high': [
                "Create detailed implementation timeline",
                "Identify potential accelerators",
                "Discuss resource allocation",
                "Plan risk mitigation strategies"
            ],
            'medium': [
                "Clarify timeline expectations",
                "Provide implementation roadmap",
                "Schedule timeline planning session"
            ]
        }
        return actions.get(severity, ["Monitor timeline discussions"])
    
    def _get_technical_risk_actions(self, severity: str) -> List[str]:
        """Get suggested actions for technical risks."""
        actions = {
            'critical': [
                "Schedule technical deep-dive session",
                "Involve technical architects",
                "Provide alternative technical approaches",
                "Consider custom integration development"
            ],
            'high': [
                "Conduct technical assessment",
                "Provide detailed integration documentation",
                "Schedule proof-of-concept",
                "Engage technical support team"
            ],
            'medium': [
                "Schedule technical review meeting",
                "Provide technical documentation",
                "Answer technical questions"
            ]
        }
        return actions.get(severity, ["Monitor technical discussions"])
    
    def _get_stakeholder_risk_actions(self, severity: str) -> List[str]:
        """Get suggested actions for stakeholder risks."""
        actions = {
            'critical': [
                "Schedule immediate stakeholder meeting",
                "Address concerns directly",
                "Provide alternative solutions",
                "Escalate to senior leadership"
            ],
            'high': [
                "Schedule 1:1 meeting with concerned stakeholder",
                "Prepare objection handling materials",
                "Involve champion to address concerns",
                "Provide additional information/demos"
            ],
            'medium': [
                "Follow up on concerns",
                "Provide clarifying information",
                "Schedule follow-up meeting"
            ]
        }
        return actions.get(severity, ["Monitor stakeholder sentiment"])
    
    def _get_competitive_risk_actions(self, severity: str) -> List[str]:
        """Get suggested actions for competitive risks."""
        actions = {
            'critical': [
                "Immediate competitive response required",
                "Provide superior proposal",
                "Highlight unique differentiators",
                "Consider price/terms adjustment"
            ],
            'high': [
                "Develop competitive battle card",
                "Schedule competitive comparison session",
                "Highlight unique value proposition",
                "Prepare competitive analysis"
            ],
            'medium': [
                "Research mentioned competitors",
                "Prepare differentiation materials",
                "Schedule competitive discussion"
            ]
        }
        return actions.get(severity, ["Monitor competitive mentions"])
    
    def _get_authority_risk_actions(self, severity: str) -> List[str]:
        """Get suggested actions for authority risks."""
        actions = {
            'critical': [
                "Identify and engage actual decision maker",
                "Request introduction to budget authority",
                "Map complete decision-making process",
                "Escalate to appropriate level"
            ],
            'high': [
                "Map organizational decision structure",
                "Request meeting with decision makers",
                "Understand approval process",
                "Engage executive sponsors"
            ],
            'medium': [
                "Clarify decision-making process",
                "Identify key stakeholders",
                "Request stakeholder introductions"
            ]
        }
        return actions.get(severity, ["Monitor authority discussions"])
    
    def _get_process_risk_actions(self, severity: str) -> List[str]:
        """Get suggested actions for process risks."""
        actions = {
            'high': [
                "Map complete approval process",
                "Prepare for extended timeline",
                "Identify process accelerators",
                "Engage legal/procurement early"
            ],
            'medium': [
                "Understand internal processes",
                "Prepare required documentation",
                "Schedule process discussion"
            ]
        }
        return actions.get(severity, ["Monitor process requirements"])
    
    def _build_risk_profile(self, signals: List[RiskSignal], content: str) -> RiskProfile:
        """Build comprehensive risk profile from detected signals."""
        # Categorize signals by severity
        critical_risks = [s for s in signals if s.severity == RiskSeverity.CRITICAL]
        high_risks = [s for s in signals if s.severity == RiskSeverity.HIGH]
        medium_risks = [s for s in signals if s.severity == RiskSeverity.MEDIUM]
        low_risks = [s for s in signals if s.severity == RiskSeverity.LOW]
        watch_signals = [s for s in signals if s.severity == RiskSeverity.WATCH]
        
        # Calculate overall risk score
        risk_weights = {
            RiskSeverity.CRITICAL: 1.0,
            RiskSeverity.HIGH: 0.7,
            RiskSeverity.MEDIUM: 0.4,
            RiskSeverity.LOW: 0.2,
            RiskSeverity.WATCH: 0.1
        }
        
        total_weighted_risk = sum(
            risk_weights[signal.severity] * signal.confidence * signal.probability
            for signal in signals
        )
        max_possible_risk = len(signals) * 1.0 if signals else 1.0
        overall_risk_score = min(1.0, total_weighted_risk / max_possible_risk)
        
        # Determine primary risk categories
        category_counts = {}
        for signal in signals:
            category = signal.category.value
            category_counts[category] = category_counts.get(category, 0) + 1
        
        primary_categories = sorted(category_counts.keys(), 
                                  key=lambda x: category_counts[x], 
                                  reverse=True)[:3]
        
        # Generate next steps
        next_steps = []
        immediate_actions = sum(1 for s in signals if s.urgency == RiskUrgency.IMMEDIATE)
        
        if critical_risks:
            next_steps.append("Address critical risks immediately")
        if high_risks:
            next_steps.append("Develop action plans for high-risk items")
        if medium_risks:
            next_steps.append("Monitor and plan responses for medium risks")
        
        # Meeting objectives
        meeting_objectives = []
        if critical_risks or high_risks:
            meeting_objectives.append("Address primary risk concerns")
            meeting_objectives.append("Clarify stakeholder positions")
        if any(s.category == RiskCategory.AUTHORITY for s in signals):
            meeting_objectives.append("Identify decision makers and approval process")
        if any(s.category == RiskCategory.BUDGET for s in signals):
            meeting_objectives.append("Discuss budget and pricing options")
        
        return RiskProfile(
            overall_risk_score=overall_risk_score,
            risk_trend="unknown",  # Would need historical data to determine trend
            critical_risks=critical_risks,
            high_risks=high_risks,
            medium_risks=medium_risks,
            low_risks=low_risks,
            watch_signals=watch_signals,
            total_signals=len(signals),
            confidence_weighted_score=total_weighted_risk,
            primary_risk_categories=primary_categories,
            immediate_actions_needed=immediate_actions,
            next_steps=next_steps,
            escalation_recommended=len(critical_risks) > 0 or len(high_risks) > 2,
            meeting_objectives=meeting_objectives
        )


def detect_deal_risks(content: str, stakeholder_data: Optional[Dict[str, Any]] = None,
                     meddpicc_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Convenience function to detect deal risks from conversation content.
    
    Args:
        content: Conversation/transcript content
        stakeholder_data: Optional stakeholder analysis data
        meddpicc_data: Optional MEDDPICC analysis data
        
    Returns:
        Risk analysis results in dictionary format
    """
    detector = RiskSignalDetector()
    risk_profile = detector.detect_risk_signals(content, stakeholder_data, meddpicc_data)
    
    return {
        'risk_analysis': {
            'overall_risk_score': risk_profile.overall_risk_score,
            'risk_trend': risk_profile.risk_trend,
            'total_signals': risk_profile.total_signals,
            'primary_risk_categories': risk_profile.primary_risk_categories,
            'immediate_actions_needed': risk_profile.immediate_actions_needed,
            'escalation_recommended': risk_profile.escalation_recommended
        },
        'risk_signals': {
            'critical': [
                {
                    'title': signal.title,
                    'category': signal.category.value,
                    'description': signal.description,
                    'evidence': signal.evidence,
                    'confidence': signal.confidence,
                    'probability': signal.probability,
                    'suggested_actions': signal.suggested_actions
                } for signal in risk_profile.critical_risks
            ],
            'high': [
                {
                    'title': signal.title,
                    'category': signal.category.value,
                    'description': signal.description,
                    'evidence': signal.evidence,
                    'confidence': signal.confidence,
                    'probability': signal.probability,
                    'suggested_actions': signal.suggested_actions
                } for signal in risk_profile.high_risks
            ],
            'medium': [
                {
                    'title': signal.title,
                    'category': signal.category.value,
                    'description': signal.description,
                    'evidence': signal.evidence,
                    'confidence': signal.confidence,
                    'suggested_actions': signal.suggested_actions
                } for signal in risk_profile.medium_risks
            ]
        },
        'recommendations': {
            'next_steps': risk_profile.next_steps,
            'meeting_objectives': risk_profile.meeting_objectives
        }
    }