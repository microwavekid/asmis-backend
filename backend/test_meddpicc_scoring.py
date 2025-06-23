#!/usr/bin/env python3
"""
Test script for MEDDPICC Completeness Scoring System
"""

import asyncio
import sys
from app.intelligence.meddpicc_scoring import calculate_meddpicc_score

def test_comprehensive_scoring():
    """Test MEDDPICC scoring with various completeness levels."""
    
    print("🎯 MEDDPICC Completeness Scoring Test")
    print("=" * 50)
    
    # Test Case 1: Well-qualified deal
    print("\n📊 Test Case 1: Well-Qualified Deal")
    print("-" * 30)
    
    well_qualified_data = {
        'metrics': {
            'identified': ['30% conversion improvement', 'ROI within 12 months', '$500K revenue increase'],
            'confidence': 0.9,
            'evidence': ['CFO specified ROI requirements', 'CEO mentioned revenue targets']
        },
        'economic_buyer': {
            'identified': 'Sarah Chen (CFO) - Budget authority confirmed',
            'confidence': 0.95,
            'evidence': 'She said "I control the budget for this initiative"'
        },
        'decision_criteria': {
            'criteria': ['Salesforce integration', 'Security compliance', 'Ease of use', 'ROI within 12 months'],
            'confidence': 0.85,
            'evidence': ['Technical requirements document shared', 'Security checklist provided']
        },
        'decision_process': {
            'steps': ['Technical evaluation', 'Security review', 'Executive approval', 'Legal review'],
            'timeline': 'Decision by December 15th, implementation in Q1',
            'confidence': 0.8,
            'evidence': ['Detailed timeline shared', 'Stakeholder map provided']
        },
        'paper_process': {
            'steps': ['Legal review', 'Procurement approval', 'Contract negotiation'],
            'requirements': ['Security audit', 'Data processing agreement', 'SLA requirements'],
            'confidence': 0.7,
            'evidence': ['Legal team introduced', 'Procurement process explained']
        },
        'implicate_pain': {
            'underlying_issues': ['Cart abandonment', 'Customer churn', 'Competitive pressure'],
            'business_impact': ['$2M annual revenue loss', 'Customer satisfaction decline', 'Market share erosion'],
            'urgency_signals': ['CEO pressure', 'Q4 board presentation', 'Competitor launching similar feature'],
            'confidence': 0.9,
            'evidence': ['CEO email shared showing urgency', 'Competitor analysis discussed']
        },
        'champion': {
            'identified': 'John Williams (VP Marketing) - Strong advocate',
            'strength': 'strong',
            'confidence': 0.85,
            'evidence': 'Prepared internal business case and scheduled executive presentation'
        },
        'competition': {
            'all_competitors': ['Optimizely', 'VWO', 'Adobe Target'],
            'positioning': 'We offer superior Salesforce integration and faster implementation',
            'strengths': ['Better integration', 'Faster deployment'],
            'weaknesses': ['Higher price point'],
            'confidence': 0.8,
            'evidence': ['Competitive comparison spreadsheet shared', 'Previous vendor evaluation discussed']
        }
    }
    
    result1 = calculate_meddpicc_score(well_qualified_data)
    print_score_summary(result1)
    
    # Test Case 2: Early-stage deal with gaps
    print("\n📊 Test Case 2: Early-Stage Deal (Many Gaps)")
    print("-" * 40)
    
    early_stage_data = {
        'metrics': {
            'identified': ['improve performance'],
            'confidence': 0.4,
            'evidence': ['Vague mention of improvement needed']
        },
        'economic_buyer': {
            'identified': '',
            'confidence': 0.1,
            'evidence': []
        },
        'decision_criteria': {
            'criteria': ['must integrate with existing systems'],
            'confidence': 0.5,
            'evidence': ['Basic integration requirement mentioned']
        },
        'decision_process': {
            'steps': [],
            'timeline': '',
            'confidence': 0.2,
            'evidence': []
        },
        'paper_process': {
            'steps': [],
            'requirements': [],
            'confidence': 0.0,
            'evidence': []
        },
        'implicate_pain': {
            'underlying_issues': ['system inefficiencies'],
            'business_impact': [],
            'urgency_signals': [],
            'confidence': 0.3,
            'evidence': ['Mentioned current system is slow']
        },
        'champion': {
            'identified': 'Mike (IT Manager)',
            'strength': 'none',
            'confidence': 0.4,
            'evidence': ['Attended demo but no advocacy shown']
        },
        'competition': {
            'all_competitors': [],
            'positioning': '',
            'confidence': 0.1,
            'evidence': []
        }
    }
    
    result2 = calculate_meddpicc_score(early_stage_data)
    print_score_summary(result2)
    
    print("\n🎯 Scoring System Features Demonstrated:")
    print("✅ Weighted scoring across all MEDDPICC elements")
    print("✅ Multi-dimensional scoring (presence + confidence + completeness)")
    print("✅ Critical gap identification")
    print("✅ Actionable next steps and meeting objectives")
    print("✅ Qualification status determination")

def print_score_summary(result):
    """Print a formatted summary of MEDDPICC scoring results."""
    print(f"Overall Score: {result.overall_score:.1f}% ({result.qualification_status.upper()})")
    
    print("\nElement Scores:")
    for element, score in result.element_scores.items():
        status = "✅" if score.total_score >= 70 else "⚠️" if score.total_score >= 40 else "❌"
        print(f"  {status} {element.replace('_', ' ').title()}: {score.total_score:.1f}/100")
    
    if result.critical_gaps:
        print(f"\nCritical Gaps ({len(result.critical_gaps)}):")
        for gap in result.critical_gaps:
            print(f"  🚨 {gap['element'].replace('_', ' ').title()}: {gap['impact']}")
    
    if result.next_actions:
        print(f"\nNext Actions ({len(result.next_actions)}):")
        for action in result.next_actions[:3]:  # Show top 3
            print(f"  📋 {action['action']} ({action['priority']} priority)")
    
    if result.meeting_objectives:
        print(f"\nNext Meeting Objectives:")
        for i, obj in enumerate(result.meeting_objectives, 1):
            print(f"  {i}. {obj}")

if __name__ == "__main__":
    test_comprehensive_scoring()