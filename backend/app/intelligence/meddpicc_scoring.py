"""
✅ Applied: MEDDPICC_COMPLETENESS_SCORING_PATTERN
MEDDPICC Completeness Scoring Engine

Provides comprehensive scoring and gap analysis for MEDDPICC qualification data.
Calculates weighted completeness scores and generates actionable recommendations.

PATTERN_REF: MEDDPICC_COMPLETENESS_SCORING_PATTERN
"""

import logging
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Risk signal detection integration
from .risk_signal_detection import detect_deal_risks

logger = logging.getLogger(__name__)


class GapSeverity(Enum):
    """Severity levels for MEDDPICC gaps."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class ElementScore:
    """Individual MEDDPICC element score breakdown."""
    element: str
    presence_score: float  # 0-40 points
    confidence_score: float  # 0-35 points
    completeness_score: float  # 0-25 points
    total_score: float  # 0-100 points
    weight: float  # Element importance weight
    weighted_score: float  # total_score * weight
    gaps: List[str]
    recommendations: List[str]


@dataclass
class MEDDPICCScoreResult:
    """Complete MEDDPICC scoring result."""
    overall_score: float  # 0-100
    element_scores: Dict[str, ElementScore]
    critical_gaps: List[Dict[str, Any]]
    next_actions: List[Dict[str, Any]]
    meeting_objectives: List[str]
    qualification_status: str  # "qualified", "developing", "weak", "unqualified"
    risk_analysis: Optional[Any] = None  # Risk profile from risk signal detection


class MEDDPICCScoring:
    """
    MEDDPICC Completeness Scoring Engine.
    ✅ Applied: MEDDPICC_COMPLETENESS_SCORING_PATTERN
    
    Provides weighted scoring across all MEDDPICC elements with actionable
    gap analysis and next steps for sales teams.
    """
    
    # Element weights based on sales methodology best practices
    ELEMENT_WEIGHTS = {
        "metrics": 0.15,  # Success criteria - important for ROI justification
        "economic_buyer": 0.20,  # Budget control - critical for deal closure
        "decision_criteria": 0.15,  # Selection factors - important for positioning
        "decision_process": 0.10,  # Timeline/steps - helpful for planning
        "paper_process": 0.10,  # Contracting - important for execution
        "implicate_pain": 0.15,  # Business problems - critical for urgency
        "champion": 0.15,  # Internal support - critical for influence
        "competition": 0.10   # Competitive intel - helpful for positioning
    }
    
    # Scoring thresholds
    QUALIFICATION_THRESHOLDS = {
        "qualified": 80.0,
        "developing": 60.0,
        "weak": 40.0,
        "unqualified": 0.0
    }
    
    def __init__(self):
        """Initialize the MEDDPICC scoring engine."""
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def calculate_completeness_score(self, meddpicc_data: Dict[str, Any]) -> MEDDPICCScoreResult:
        """
        Calculate comprehensive MEDDPICC completeness score.
        
        Args:
            meddpicc_data: Extracted MEDDPICC data from analysis
            
        Returns:
            Complete scoring result with gaps and recommendations
        """
        try:
            element_scores = {}
            total_weighted_score = 0.0
            
            # Score each MEDDPICC element
            for element, weight in self.ELEMENT_WEIGHTS.items():
                element_data = meddpicc_data.get(element, {})
                score = self._score_element(element, element_data)
                element_scores[element] = score
                total_weighted_score += score.weighted_score
            
            # Generate gap analysis
            critical_gaps = self._identify_critical_gaps(element_scores)
            next_actions = self._generate_next_actions(element_scores)
            meeting_objectives = self._generate_meeting_objectives(element_scores)
            
            # Detect risk signals for enhanced recommendations
            risk_analysis = None
            try:
                # Extract transcript if available for risk analysis
                transcript = ""
                for element_data in meddpicc_data.values():
                    if isinstance(element_data, dict) and 'evidence' in element_data:
                        evidence = element_data['evidence']
                        if isinstance(evidence, list):
                            transcript += " ".join(evidence) + " "
                        elif isinstance(evidence, str):
                            transcript += evidence + " "
                
                if transcript.strip():
                    risk_analysis = detect_deal_risks(transcript, None, meddpicc_data)
                    # Enhance recommendations with risk-based actions
                    risk_actions = self._extract_risk_actions(risk_analysis)
                    next_actions.extend(risk_actions)
            except Exception as e:
                logger.warning(f"Risk analysis integration failed: {e}")
            
            # Determine qualification status
            qualification_status = self._determine_qualification_status(total_weighted_score)
            
            result = MEDDPICCScoreResult(
                overall_score=total_weighted_score,
                element_scores=element_scores,
                critical_gaps=critical_gaps,
                next_actions=next_actions,
                meeting_objectives=meeting_objectives,
                qualification_status=qualification_status,
                risk_analysis=risk_analysis
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error calculating MEDDPICC score: {e}")
            # Return minimal score result on error
            return MEDDPICCScoreResult(
                overall_score=0.0,
                element_scores={},
                critical_gaps=[{"error": str(e)}],
                next_actions=[],
                meeting_objectives=[],
                qualification_status="unqualified"
            )
    
    def _score_element(self, element: str, element_data: Dict[str, Any]) -> ElementScore:
        """Score an individual MEDDPICC element."""
        presence_score = self._calculate_presence_score(element, element_data)
        confidence_score = self._calculate_confidence_score(element_data)
        completeness_score = self._calculate_completeness_score(element, element_data)
        
        total_score = presence_score + confidence_score + completeness_score
        weight = self.ELEMENT_WEIGHTS[element]
        weighted_score = total_score * weight
        
        gaps = self._identify_element_gaps(element, element_data, total_score)
        recommendations = self._get_element_recommendations(element, gaps)
        
        return ElementScore(
            element=element,
            presence_score=presence_score,
            confidence_score=confidence_score,
            completeness_score=completeness_score,
            total_score=total_score,
            weight=weight,
            weighted_score=weighted_score,
            gaps=gaps,
            recommendations=recommendations
        )
    
    def _calculate_presence_score(self, element: str, data: Dict[str, Any]) -> float:
        """Calculate presence score (0-40 points) based on data availability."""
        if not data:
            return 0.0
        
        # Element-specific presence logic
        if element == "metrics":
            identified = data.get("identified", [])
            return min(40.0, len(identified) * 10.0) if identified else 0.0
        
        elif element == "economic_buyer":
            identified = data.get("identified", "")
            return 40.0 if identified and identified.strip() else 0.0
        
        elif element == "decision_criteria":
            # Handle both old format (list) and new format (structured dict)
            criteria_data = data.get("criteria", [])
            
            if isinstance(criteria_data, list):
                # Old format - simple list
                return min(40.0, len(criteria_data) * 8.0) if criteria_data else 0.0
            elif isinstance(criteria_data, dict):
                # New format - structured criteria
                total_criteria = 0
                quality_bonus = 0.0
                
                # Count criteria across all categories
                for category, criteria_list in criteria_data.items():
                    if isinstance(criteria_list, list):
                        total_criteria += len(criteria_list)
                        
                        # Quality bonuses for structured criteria
                        for criterion in criteria_list:
                            if isinstance(criterion, dict):
                                # Bonus for measurable criteria
                                if criterion.get('measurable', False):
                                    quality_bonus += 2.0
                                # Bonus for priority specification
                                if criterion.get('priority') in ['must_have', 'dealbreaker']:
                                    quality_bonus += 1.0
                                # Bonus for business unit mapping
                                if criterion.get('business_unit'):
                                    quality_bonus += 1.0
                                # Bonus for stakeholder mapping
                                if criterion.get('stakeholder'):
                                    quality_bonus += 0.5
                
                # Base score from count + quality bonuses
                base_score = min(25.0, total_criteria * 5.0)
                bonus_score = min(15.0, quality_bonus)
                return base_score + bonus_score
            else:
                return 0.0
        
        elif element == "decision_process":
            steps = data.get("steps", [])
            timeline = data.get("timeline", "")
            score = 0.0
            if steps:
                score += min(25.0, len(steps) * 5.0)
            if timeline and timeline.strip():
                score += 15.0
            return score
        
        elif element == "paper_process":
            steps = data.get("steps", [])
            requirements = data.get("requirements", [])
            score = 0.0
            if steps:
                score += min(25.0, len(steps) * 8.0)
            if requirements:
                score += min(15.0, len(requirements) * 5.0)
            return score
        
        elif element == "implicate_pain":
            underlying = data.get("underlying_issues", [])
            impact = data.get("business_impact", [])
            urgency = data.get("urgency_signals", [])
            score = 0.0
            if underlying:
                score += min(15.0, len(underlying) * 5.0)
            if impact:
                score += min(15.0, len(impact) * 5.0)
            if urgency:
                score += min(10.0, len(urgency) * 3.0)
            return score
        
        elif element == "champion":
            identified = data.get("identified", "")
            strength = data.get("strength", "none")
            score = 20.0 if identified and identified.strip() else 0.0
            if strength == "strong":
                score += 20.0
            elif strength == "developing":
                score += 10.0
            return score
        
        elif element == "competition":
            competitors = data.get("all_competitors", [])
            positioning = data.get("positioning", "")
            score = min(25.0, len(competitors) * 5.0) if competitors else 0.0
            if positioning and positioning.strip():
                score += 15.0
            return score
        
        return 0.0
    
    def _calculate_confidence_score(self, data: Dict[str, Any]) -> float:
        """Calculate confidence score (0-35 points) based on extraction confidence."""
        confidence = data.get("confidence", 0.0)
        return confidence * 35.0
    
    def _calculate_completeness_score(self, element: str, data: Dict[str, Any]) -> float:
        """Calculate completeness score (0-25 points) based on data depth."""
        if not data:
            return 0.0
        
        evidence = data.get("evidence", [])
        evidence_score = min(15.0, len(evidence) * 3.0) if evidence else 0.0
        
        # Element-specific completeness factors
        detail_score = 0.0
        
        if element == "metrics":
            # Check for quantified metrics
            identified = data.get("identified", [])
            quantified_count = sum(1 for metric in identified if any(char.isdigit() for char in str(metric)))
            detail_score = min(10.0, quantified_count * 5.0)
        
        elif element == "economic_buyer":
            # Check for role and authority indicators
            identified = data.get("identified", "")
            if "cfo" in identified.lower() or "ceo" in identified.lower() or "budget" in identified.lower():
                detail_score = 10.0
            elif identified and identified.strip():
                detail_score = 5.0
            
            # Bonus for enhanced stakeholder analysis
            if 'relationship_mapping' in data:
                economic_candidates = data['relationship_mapping'].get('network_analysis', {}).get('economic_buyer_candidates', [])
                if economic_candidates:
                    detail_score += min(10.0, len(economic_candidates) * 3.0)
        
        elif element == "champion":
            # Check for strength indicators
            strength = data.get("strength", "none")
            if strength == "strong":
                detail_score = 10.0
            elif strength == "developing":
                detail_score = 5.0
            
            # Bonus for enhanced stakeholder analysis
            if 'relationship_mapping' in data:
                champion_candidates = data['relationship_mapping'].get('network_analysis', {}).get('champion_candidates', [])
                if champion_candidates:
                    detail_score += min(5.0, len(champion_candidates) * 2.0)
        
        elif element == "decision_criteria":
            # Enhanced scoring for new structured criteria format
            criteria_data = data.get("criteria", [])
            if isinstance(criteria_data, dict):
                # New structured format
                category_coverage = len(criteria_data)  # Number of categories covered
                total_criteria = sum(len(criteria_list) for criteria_list in criteria_data.values() if isinstance(criteria_list, list))
                
                # Bonus for category diversity
                detail_score = min(5.0, category_coverage * 2.0)
                
                # Bonus for criteria depth
                detail_score += min(5.0, total_criteria * 1.0)
                
                # Check for business unit coverage
                business_units = data.get("business_unit_involvement", [])
                if business_units:
                    detail_score += min(5.0, len(business_units) * 1.0)
                
                # Check for evaluation process
                if data.get("evaluation_process") and data.get("evaluation_process") != "Not specified":
                    detail_score += 2.0
                
                # Check for decision makers
                decision_makers = data.get("decision_makers", [])
                if decision_makers:
                    detail_score += min(3.0, len(decision_makers) * 1.0)
            else:
                # Old format or simple list
                criteria_list = criteria_data if isinstance(criteria_data, list) else []
                detail_score = min(10.0, len(criteria_list) * 2.0)
        
        elif element == "competition":
            # Check for competitive intelligence depth
            strengths = data.get("strengths", [])
            weaknesses = data.get("weaknesses", [])
            detail_score = min(10.0, (len(strengths) + len(weaknesses)) * 2.0)
        
        else:
            # Generic detail scoring for other elements
            all_fields = [v for v in data.values() if isinstance(v, (list, str)) and v]
            detail_score = min(10.0, len(all_fields) * 2.0)
        
        return evidence_score + detail_score
    
    def _identify_element_gaps(self, element: str, data: Dict[str, Any], score: float) -> List[str]:
        """Identify specific gaps for an element."""
        gaps = []
        
        if score < 30:  # Major gaps
            if element == "economic_buyer":
                if not data.get("identified"):
                    gaps.append("economic_buyer_not_identified")
                if data.get("confidence", 0) < 0.7:
                    gaps.append("economic_buyer_confidence_low")
                
                # Check enhanced stakeholder analysis
                if 'relationship_mapping' in data:
                    economic_candidates = data['relationship_mapping'].get('network_analysis', {}).get('economic_buyer_candidates', [])
                    if not economic_candidates:
                        gaps.append("no_budget_authority_identified")
            
            elif element == "champion":
                if not data.get("identified"):
                    gaps.append("champion_not_identified")
                if data.get("strength") == "none":
                    gaps.append("no_champion_support")
                elif data.get("strength") == "developing":
                    gaps.append("champion_strength_weak")
                
                # Check enhanced stakeholder analysis
                if 'relationship_mapping' in data:
                    champion_candidates = data['relationship_mapping'].get('network_analysis', {}).get('champion_candidates', [])
                    potential_blockers = data['relationship_mapping'].get('network_analysis', {}).get('potential_blockers', [])
                    
                    if not champion_candidates:
                        gaps.append("no_champion_candidates_identified")
                    if potential_blockers:
                        gaps.append("potential_blockers_identified")
            
            elif element == "metrics":
                if not data.get("identified"):
                    gaps.append("success_metrics_undefined")
                if data.get("confidence", 0) < 0.7:
                    gaps.append("metrics_not_quantified")
            
            elif element == "decision_criteria":
                criteria_data = data.get("criteria", [])
                if isinstance(criteria_data, dict):
                    # New structured format gaps
                    total_criteria = sum(len(criteria_list) for criteria_list in criteria_data.values() if isinstance(criteria_list, list))
                    if total_criteria == 0:
                        gaps.append("no_decision_criteria_identified")
                    elif total_criteria < 3:
                        gaps.append("limited_criteria_depth")
                    
                    # Check for category coverage
                    if len(criteria_data) < 2:
                        gaps.append("limited_criteria_categories")
                    
                    # Check for business unit mapping
                    business_units = data.get("business_unit_involvement", [])
                    if not business_units:
                        gaps.append("no_business_unit_ownership_identified")
                    
                    # Check for evaluation process
                    if not data.get("evaluation_process") or data.get("evaluation_process") == "Not specified":
                        gaps.append("evaluation_process_unclear")
                    
                    # Check for priority classification
                    has_priorities = False
                    for criteria_list in criteria_data.values():
                        if isinstance(criteria_list, list):
                            for criterion in criteria_list:
                                if isinstance(criterion, dict) and criterion.get('priority'):
                                    has_priorities = True
                                    break
                    if not has_priorities:
                        gaps.append("criteria_priorities_unclear")
                else:
                    # Old format gaps
                    criteria_list = criteria_data if isinstance(criteria_data, list) else []
                    if not criteria_list:
                        gaps.append("decision_criteria_not_identified")
                    elif len(criteria_list) < 3:
                        gaps.append("limited_criteria_identified")
            
            elif element == "implicate_pain":
                if not data.get("underlying_issues"):
                    gaps.append("underlying_pain_not_identified")
                if not data.get("business_impact"):
                    gaps.append("business_impact_unclear")
            
            elif element == "paper_process":
                if not data.get("steps"):
                    gaps.append("contracting_process_unknown")
                if not data.get("requirements"):
                    gaps.append("legal_requirements_unclear")
        
        return gaps
    
    def _get_element_recommendations(self, element: str, gaps: List[str]) -> List[str]:
        """Get specific recommendations for element gaps."""
        recommendations = []
        
        for gap in gaps:
            if gap == "economic_buyer_not_identified":
                recommendations.append("Map organizational chart to identify budget authority")
            elif gap == "champion_not_identified":
                recommendations.append("Build relationships with potential internal advocates")
            elif gap == "champion_strength_weak":
                recommendations.append("Provide champion with enablement materials and business case")
            elif gap == "no_budget_authority_identified":
                recommendations.append("Map stakeholder relationships to identify budget decision maker")
            elif gap == "no_champion_candidates_identified":
                recommendations.append("Analyze stakeholder influence network to identify potential champions")
            elif gap == "potential_blockers_identified":
                recommendations.append("Develop strategy to address concerns of potential blockers")
            elif gap == "success_metrics_undefined":
                recommendations.append("Conduct metrics definition workshop with stakeholders")
            elif gap == "no_decision_criteria_identified":
                recommendations.append("Conduct criteria discovery workshop with stakeholders")
            elif gap == "limited_criteria_depth":
                recommendations.append("Probe for additional evaluation criteria and requirements")
            elif gap == "limited_criteria_categories":
                recommendations.append("Explore technical, business, and financial requirements separately")
            elif gap == "no_business_unit_ownership_identified":
                recommendations.append("Map criteria ownership to specific business units and stakeholders")
            elif gap == "evaluation_process_unclear":
                recommendations.append("Clarify the evaluation process and timeline with key stakeholders")
            elif gap == "criteria_priorities_unclear":
                recommendations.append("Establish must-have vs nice-to-have criteria with stakeholders")
            elif gap == "limited_criteria_identified":
                recommendations.append("Conduct more detailed requirements gathering sessions")
            elif gap == "decision_criteria_not_identified":
                recommendations.append("Schedule discovery call to understand evaluation criteria")
            elif gap == "underlying_pain_not_identified":
                recommendations.append("Ask deeper discovery questions about business challenges")
            elif gap == "contracting_process_unknown":
                recommendations.append("Understand procurement and legal approval process")
        
        return recommendations
    
    def _identify_critical_gaps(self, element_scores: Dict[str, ElementScore]) -> List[Dict[str, Any]]:
        """Identify the most critical gaps affecting deal progression."""
        critical_gaps = []
        
        # High-impact elements with low scores
        high_impact_elements = ["economic_buyer", "champion", "implicate_pain"]
        
        for element in high_impact_elements:
            score = element_scores.get(element)
            if score and score.total_score < 50:
                critical_gaps.append({
                    "element": element,
                    "severity": GapSeverity.CRITICAL.value,
                    "score": score.total_score,
                    "impact": f"Missing {element.replace('_', ' ')} creates {score.weight*100:.0f}% deal risk",
                    "gaps": score.gaps,
                    "recommendations": score.recommendations
                })
        
        return critical_gaps
    
    def _generate_next_actions(self, element_scores: Dict[str, ElementScore]) -> List[Dict[str, Any]]:
        """Generate prioritized next actions based on gaps."""
        actions = []
        
        # Sort elements by weighted impact of gaps
        sorted_elements = sorted(
            element_scores.items(),
            key=lambda x: (100 - x[1].total_score) * x[1].weight,
            reverse=True
        )
        
        for element, score in sorted_elements[:3]:  # Top 3 priority gaps
            if score.total_score < 70:  # Only show actions for incomplete elements
                for rec in score.recommendations[:2]:  # Max 2 actions per element
                    actions.append({
                        "element": element,
                        "action": rec,
                        "priority": "high" if score.weight > 0.15 else "medium",
                        "impact": f"{score.weight*100:.0f}% of qualification score"
                    })
        
        return actions
    
    def _generate_meeting_objectives(self, element_scores: Dict[str, ElementScore]) -> List[str]:
        """Generate specific objectives for next customer meeting."""
        objectives = []
        
        for element, score in element_scores.items():
            if score.total_score < 60:  # Focus on weak areas
                if element == "economic_buyer":
                    objectives.append("Identify and request introduction to budget decision maker")
                elif element == "champion":
                    objectives.append("Strengthen champion relationship and advocacy")
                elif element == "metrics":
                    objectives.append("Define specific success metrics and current baselines")
                elif element == "implicate_pain":
                    objectives.append("Uncover deeper business impact of current challenges")
                elif element == "paper_process":
                    objectives.append("Map out contracting and procurement requirements")
        
        return objectives[:4]  # Limit to 4 key objectives
    
    def _extract_risk_actions(self, risk_analysis) -> List[Dict[str, Any]]:
        """Extract actionable recommendations from risk analysis."""
        risk_actions = []
        
        if isinstance(risk_analysis, dict):
            risk_signals = risk_analysis.get('risk_signals', {})
            
            # Process critical risks
            critical_risks = risk_signals.get('critical', [])
            for risk in critical_risks:
                for action in risk.get('suggested_actions', [])[:1]:  # Max 1 action per critical risk
                    risk_actions.append({
                        "element": "risk_mitigation",
                        "action": action,
                        "priority": "critical",
                        "impact": f"Mitigate {risk['category']} risk: {risk['title']}",
                        "risk_category": risk['category'],
                        "urgency": risk.get('urgency', 'immediate')
                    })
            
            # Process high risks
            high_risks = risk_signals.get('high', [])
            for risk in high_risks:
                for action in risk.get('suggested_actions', [])[:1]:  # Max 1 action per high risk
                    risk_actions.append({
                        "element": "risk_mitigation", 
                        "action": action,
                        "priority": "high",
                        "impact": f"Address {risk['category']} concern",
                        "risk_category": risk['category'],
                        "urgency": risk.get('urgency', 'urgent')
                    })
        
        return risk_actions[:3]  # Limit to top 3 risk actions
    
    def _determine_qualification_status(self, overall_score: float) -> str:
        """Determine deal qualification status based on overall score."""
        for status, threshold in self.QUALIFICATION_THRESHOLDS.items():
            if overall_score >= threshold:
                return status
        return "unqualified"


# Convenience function for external use
def calculate_meddpicc_score(meddpicc_data: Dict[str, Any]) -> MEDDPICCScoreResult:
    """Calculate MEDDPICC completeness score from extracted data."""
    scorer = MEDDPICCScoring()
    return scorer.calculate_completeness_score(meddpicc_data)