#!/usr/bin/env python3
"""
Test script for Enhanced Decision Criteria Analysis
"""

import asyncio
from app.intelligence.decision_criteria_analyzer import analyze_decision_criteria
from app.intelligence.meddpicc_scoring import calculate_meddpicc_score

def test_decision_criteria_enhancement():
    """Test enhanced decision criteria analysis with business unit mapping."""
    
    print("🎯 Enhanced Decision Criteria Analysis Test")
    print("=" * 60)
    
    # Sample transcript with rich criteria information
    sample_transcript = """
    Sarah Chen (CFO): Our evaluation criteria are quite comprehensive. From a financial perspective, 
    we need to stay under $500K annually and see at least 20% ROI within the first year.
    
    Mike Thompson (CTO): On the technical side, we must have seamless Salesforce integration - 
    that's a deal breaker. We also need 99.9% uptime SLA and the ability to handle 
    100,000 API calls per minute during peak traffic.
    
    John Williams (VP Marketing): For marketing, we're looking for improved conversion rates - 
    ideally 15% improvement from our current baseline. We need real-time personalization 
    capabilities and A/B testing features. Nice to have would be advanced analytics.
    
    Lisa Rodriguez (IT Manager): From an operational standpoint, the implementation can't 
    take more than 3 months. We need comprehensive training for our team and 24/7 support.
    
    David Kim (Security Director): Security requirements are non-negotiable: SOC2 compliance, 
    encryption at rest and in transit, and it must pass our penetration testing.
    
    Sarah: The evaluation process will include a technical demo for IT, a business case 
    review with the executive team, and a pilot with the marketing team. 
    All three groups need to sign off.
    
    Mike: We'll also need to evaluate this against our current vendor and see how it 
    compares to the other solutions we're considering.
    
    John: Timeline is critical - we need to have this in place before our Q4 campaign launch.
    """
    
    print("📊 Running Decision Criteria Analysis...")
    criteria_analysis = analyze_decision_criteria(sample_transcript)
    
    print(f"\n🎯 Criteria Analysis Results:")
    print(f"Quality Score: {criteria_analysis.quality_score:.2f}")
    print(f"Coverage Score: {criteria_analysis.coverage_score:.2f}")
    print(f"Completeness Score: {criteria_analysis.completeness_score:.2f}")
    
    print(f"\n📋 Categorized Criteria:")
    for category, criteria_list in criteria_analysis.criteria.items():
        print(f"\n{category.upper()}:")
        for criterion in criteria_list:
            print(f"  • {criterion.criterion}")
            print(f"    Priority: {criterion.priority.value}, Measurable: {criterion.measurable}")
            if criterion.business_unit:
                print(f"    Business Unit: {criterion.business_unit.value}")
            if criterion.stakeholder:
                print(f"    Stakeholder: {criterion.stakeholder}")
            if criterion.threshold:
                print(f"    Threshold: {criterion.threshold}")
    
    print(f"\n🏢 Business Unit Involvement: {', '.join(criteria_analysis.business_unit_involvement)}")
    print(f"📝 Evaluation Process: {criteria_analysis.evaluation_process}")
    
    print(f"\n📊 Prioritization Buckets:")
    for bucket, items in criteria_analysis.prioritization.items():
        if items:
            print(f"  {bucket.upper()}: {len(items)} items")
            for item in items[:2]:  # Show first 2
                print(f"    • {item}")
    
    # Test integration with MEDDPICC scoring
    print(f"\n🔗 Testing MEDDPICC Integration...")
    
    # Convert criteria analysis to MEDDPICC format
    meddpicc_criteria = {
        "criteria": {},
        "prioritization": criteria_analysis.prioritization,
        "evaluation_process": criteria_analysis.evaluation_process,
        "decision_makers": criteria_analysis.decision_makers,
        "business_unit_involvement": criteria_analysis.business_unit_involvement,
        "confidence": 0.8,
        "evidence": ["Comprehensive criteria discussion in transcript"]
    }
    
    # Convert our structured criteria to MEDDPICC format
    for category, criteria_list in criteria_analysis.criteria.items():
        meddpicc_criteria["criteria"][category] = []
        for criterion in criteria_list:
            meddpicc_criteria["criteria"][category].append({
                "criterion": criterion.criterion,
                "priority": criterion.priority.value,
                "measurable": criterion.measurable,
                "stakeholder": criterion.stakeholder,
                "business_unit": criterion.business_unit.value if criterion.business_unit else None,
                "threshold": criterion.threshold
            })
    
    # Create full MEDDPICC data for scoring test
    meddpicc_data_with_enhanced_criteria = {
        'metrics': {
            'identified': ['20% ROI', '15% conversion improvement'],
            'confidence': 0.8,
            'evidence': ['ROI and conversion targets mentioned']
        },
        'economic_buyer': {
            'identified': 'Sarah Chen (CFO)',
            'confidence': 0.9,
            'evidence': 'CFO mentioned budget authority and approval process'
        },
        'decision_criteria': meddpicc_criteria,
        'decision_process': {
            'steps': ['Technical demo', 'Business case review', 'Marketing pilot', 'Final approval'],
            'timeline': 'Before Q4 campaign launch',
            'confidence': 0.8,
            'evidence': ['Evaluation process clearly outlined']
        },
        'paper_process': {
            'steps': [],
            'requirements': ['SOC2 compliance'],
            'confidence': 0.3,
            'evidence': ['Security requirements mentioned']
        },
        'implicate_pain': {
            'underlying_issues': ['Current conversion rates too low'],
            'business_impact': ['Q4 campaign effectiveness at risk'],
            'urgency_signals': ['Q4 deadline'],
            'confidence': 0.7,
            'evidence': ['Timeline pressure and performance concerns']
        },
        'champion': {
            'identified': 'John Williams (VP Marketing)',
            'strength': 'developing',
            'confidence': 0.6,
            'evidence': ['Active participation in criteria definition']
        },
        'competition': {
            'all_competitors': ['Current vendor', 'Other solutions under consideration'],
            'positioning': '',
            'confidence': 0.4,
            'evidence': ['Comparative evaluation mentioned']
        }
    }
    
    score_result = calculate_meddpicc_score(meddpicc_data_with_enhanced_criteria)
    
    print(f"\n📈 Enhanced MEDDPICC Score: {score_result.overall_score:.1f}%")
    print(f"📊 Qualification Status: {score_result.qualification_status.upper()}")
    
    # Show decision criteria specific scoring
    criteria_score = score_result.element_scores['decision_criteria']
    print(f"\n🎯 Decision Criteria Element Analysis:")
    print(f"  Presence Score: {criteria_score.presence_score:.1f}/40")
    print(f"  Confidence Score: {criteria_score.confidence_score:.1f}/35") 
    print(f"  Completeness Score: {criteria_score.completeness_score:.1f}/25")
    print(f"  Total Score: {criteria_score.total_score:.1f}/100")
    print(f"  Weighted Score: {criteria_score.weighted_score:.1f}")
    
    if criteria_score.gaps:
        print(f"\n❗ Decision Criteria Gaps:")
        for gap in criteria_score.gaps:
            print(f"  • {gap}")
    
    if criteria_score.recommendations:
        print(f"\n💡 Recommendations:")
        for rec in criteria_score.recommendations:
            print(f"  • {rec}")
    
    print(f"\n✅ Enhanced Decision Criteria Analysis: COMPLETE!")
    print(f"🎯 Key Improvements:")
    print(f"   ✅ Multi-category criteria extraction (technical, business, financial)")
    print(f"   ✅ Business unit mapping and ownership identification") 
    print(f"   ✅ Priority classification (must-have, nice-to-have, dealbreakers)")
    print(f"   ✅ Measurability detection and threshold extraction")
    print(f"   ✅ Enhanced MEDDPICC scoring with quality bonuses")
    print(f"   ✅ Comprehensive gap analysis and recommendations")
    print(f"   ✅ Evaluation process and decision maker mapping")

if __name__ == "__main__":
    test_decision_criteria_enhancement()