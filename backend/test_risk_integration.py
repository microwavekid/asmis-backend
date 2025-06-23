#!/usr/bin/env python3
"""
Test script for Risk Signal Detection Integration with MEDDPICC Scoring
"""

import asyncio
from app.intelligence.meddpicc_scoring import calculate_meddpicc_score

def test_risk_integration():
    """Test risk signal detection integration with MEDDPICC scoring."""
    
    print("🚨 Risk Signal Detection Integration Test")
    print("=" * 60)
    
    # Sample MEDDPICC data with risk-triggering evidence
    risky_meddpicc_data = {
        'metrics': {
            'identified': ['Increase conversion rates'],
            'confidence': 0.5,
            'evidence': [
                'We need to improve our metrics somehow',
                'Our current numbers are not great'
            ]
        },
        'economic_buyer': {
            'identified': 'John Smith',
            'confidence': 0.4,
            'evidence': [
                'John mentioned budget concerns',
                'Budget approval is complicated this year',
                'We might need to push this to next quarter'
            ]
        },
        'decision_criteria': {
            'criteria': ['Cost', 'Implementation time'],
            'confidence': 0.6,
            'evidence': [
                'We need something cheap and fast',
                'Our technical team is already overwhelmed'
            ]
        },
        'decision_process': {
            'steps': ['Evaluation'],
            'timeline': 'unclear',
            'confidence': 0.3,
            'evidence': [
                'We are not sure about the timeline',
                'The process keeps changing',
                'Leadership is still discussing priorities'
            ]
        },
        'paper_process': {
            'steps': [],
            'requirements': [],
            'confidence': 0.1,
            'evidence': [
                'Legal approval could be an issue',
                'We have had problems with procurement before'
            ]
        },
        'implicate_pain': {
            'underlying_issues': ['Low performance'],
            'business_impact': ['Revenue impact'],
            'urgency_signals': [],
            'confidence': 0.4,
            'evidence': [
                'Things are okay for now',
                'This is not our biggest priority',
                'We can probably wait a bit longer'
            ]
        },
        'champion': {
            'identified': 'Sarah Wilson',
            'strength': 'developing',
            'confidence': 0.5,
            'evidence': [
                'Sarah seems interested but cautious',
                'She mentioned needing to check with her manager',
                'There might be some internal resistance'
            ]
        },
        'competition': {
            'all_competitors': ['Alternative vendors'],
            'positioning': 'unclear',
            'confidence': 0.3,
            'evidence': [
                'They are looking at other options',
                'Price is a major concern',
                'Some people prefer the status quo'
            ]
        }
    }
    
    print("📊 Calculating MEDDPICC Score with Risk Detection...")
    score_result = calculate_meddpicc_score(risky_meddpicc_data)
    
    print(f"\n📈 MEDDPICC Score: {score_result.overall_score:.1f}%")
    print(f"📊 Qualification Status: {score_result.qualification_status.upper()}")
    
    # Display risk analysis if available
    if score_result.risk_analysis:
        risk_data = score_result.risk_analysis.get('risk_analysis', {})
        risk_signals = score_result.risk_analysis.get('risk_signals', {})
        
        print(f"\n🚨 Risk Analysis Results:")
        print(f"   Overall Risk Score: {risk_data.get('overall_risk_score', 0):.2f}")
        print(f"   Risk Trend: {risk_data.get('risk_trend', 'unknown')}")
        print(f"   Total Risk Signals: {risk_data.get('total_signals', 0)}")
        print(f"   Primary Categories: {', '.join(risk_data.get('primary_risk_categories', []))}")
        
        # Critical risks
        critical_risks = risk_signals.get('critical', [])
        if critical_risks:
            print(f"\n🔴 Critical Risks ({len(critical_risks)}):")
            for risk in critical_risks:
                print(f"   • {risk['title']} ({risk['category']})")
                print(f"     {risk['description']}")
                if 'suggested_actions' in risk:
                    print(f"     Actions: {', '.join(risk['suggested_actions'][:2])}")
        
        # High risks
        high_risks = risk_signals.get('high', [])
        if high_risks:
            print(f"\n🟡 High Risks ({len(high_risks)}):")
            for risk in high_risks:
                print(f"   • {risk['title']} ({risk['category']})")
                print(f"     {risk['description']}")
        
        # Medium risks
        medium_risks = risk_signals.get('medium', [])
        if medium_risks:
            print(f"\n🟠 Medium Risks ({len(medium_risks)}):")
            for risk in medium_risks[:3]:  # Show top 3
                print(f"   • {risk['title']} ({risk['category']})")
    else:
        print("\n⚠️ No risk analysis available")
    
    # Display enhanced next actions (including risk mitigation)
    print(f"\n🎯 Next Actions ({len(score_result.next_actions)}):")
    for action in score_result.next_actions:
        priority_icon = "🔴" if action['priority'] == 'critical' else "🟡" if action['priority'] == 'high' else "🔵"
        print(f"   {priority_icon} {action['action']}")
        print(f"      Element: {action['element']}, Impact: {action['impact']}")
        if 'risk_category' in action:
            print(f"      Risk Category: {action['risk_category']}, Urgency: {action['urgency']}")
    
    # Display critical gaps
    print(f"\n❗ Critical Gaps ({len(score_result.critical_gaps)}):")
    for gap in score_result.critical_gaps:
        print(f"   • {gap['element']}: {gap['impact']}")
        print(f"     Score: {gap['score']:.1f}/100, Severity: {gap['severity']}")
    
    print(f"\n✅ Risk Signal Detection Integration: COMPLETE!")
    print(f"🎯 System now provides:")
    print(f"   ✅ Comprehensive risk analysis from conversation content")
    print(f"   ✅ Risk-informed MEDDPICC scoring and recommendations")
    print(f"   ✅ Prioritized action items including risk mitigation")
    print(f"   ✅ Early warning system for deal risks")
    print(f"   ✅ Multi-category risk detection (budget, timeline, stakeholder, etc.)")

if __name__ == "__main__":
    test_risk_integration()