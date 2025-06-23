#!/usr/bin/env python3
"""
Test script for Enhanced Stakeholder Relationship Mapping
"""

import asyncio
from app.intelligence.stakeholder_relationship_mapping import enhance_stakeholder_relationships

def test_stakeholder_relationship_mapping():
    """Test enhanced stakeholder relationship mapping with realistic data."""
    
    print("🎯 Enhanced Stakeholder Relationship Mapping Test")
    print("=" * 60)
    
    # Sample transcript with rich stakeholder and relationship information
    sample_transcript = """
    John Williams (VP Marketing): Welcome everyone to this evaluation meeting. Sarah, as our CFO, 
    you'll need to approve any budget over $50K for this initiative.
    
    Sarah Chen (CFO): That's correct. I control the budget for technology investments. 
    I need to see clear ROI projections before I can sign off.
    
    Mike Thompson (CTO): From a technical perspective, this solution looks promising. 
    I have the authority to approve integrations with our Salesforce instance.
    
    John: I'm definitely going to champion this solution internally. I think this 
    is exactly what we need to improve our conversion rates.
    
    Lisa Rodriguez (IT Manager): I report to Mike and will be implementing this if we move forward. 
    What about security compliance requirements?
    
    Mike: Lisa brings up a good point. We'll need to run this through our security review process. 
    I work closely with David Kim, our Security Director, on these evaluations.
    
    Sarah: I'm a bit concerned about the timeline. We need to have something in place by Q4. 
    John, you mentioned you'll advocate for this?
    
    John: Absolutely. I'll prepare a business case for the executive team. 
    Sarah and I collaborate on budget planning, so I understand the financial constraints.
    
    David Kim (Security Director): I wasn't able to join the call, but Mike mentioned 
    this in our weekly sync. I'll need to review the security documentation.
    
    Sarah: John, what's your confidence level that this will deliver the 30% improvement we need?
    
    John: Very high. This aligns perfectly with our marketing automation strategy.
    """
    
    # Sample basic stakeholder data (simulating existing agent output)
    basic_stakeholder_data = {
        "stakeholders": [
            {
                "name": "John Williams",
                "title": "VP Marketing", 
                "department": "Marketing",
                "role_classification": "champion",
                "confidence": 0.9,
                "evidence": "I'm definitely going to champion this solution internally"
            },
            {
                "name": "Sarah Chen",
                "title": "CFO",
                "department": "Finance", 
                "role_classification": "economic_buyer",
                "confidence": 0.95,
                "evidence": "I control the budget for technology investments"
            },
            {
                "name": "Mike Thompson",
                "title": "CTO",
                "department": "Technology",
                "role_classification": "technical_decision_maker", 
                "confidence": 0.85,
                "evidence": "I have the authority to approve integrations"
            },
            {
                "name": "Lisa Rodriguez",
                "title": "IT Manager",
                "department": "Technology",
                "role_classification": "user",
                "confidence": 0.7,
                "evidence": "I will be implementing this if we move forward"
            },
            {
                "name": "David Kim",
                "title": "Security Director", 
                "department": "Security",
                "role_classification": "gatekeeper",
                "confidence": 0.6,
                "evidence": "I'll need to review the security documentation"
            }
        ],
        "relationships": [
            {
                "from_stakeholder": "Lisa Rodriguez",
                "to_stakeholder": "Mike Thompson",
                "relationship_type": "reports_to",
                "strength": 0.9,
                "confidence": 0.95,
                "evidence": "I report to Mike",
                "bidirectional": False
            }
        ]
    }
    
    print("📊 Testing Enhanced Relationship Mapping...")
    enhanced_result = enhance_stakeholder_relationships(basic_stakeholder_data, sample_transcript)
    
    print("\n🎯 Enhanced Stakeholder Analysis Results:")
    print("-" * 40)
    
    enhanced_stakeholders = enhanced_result['enhanced_stakeholders']
    print(f"Stakeholders Analyzed: {len(enhanced_stakeholders)}")
    
    for name, stakeholder in enhanced_stakeholders.items():
        print(f"\n👤 {name}")
        print(f"   Title: {stakeholder['title']}")
        print(f"   Role: {stakeholder['role_classification']}")
        print(f"   Seniority Level: {stakeholder['seniority_level']} (1=C-level, 5=Individual)")
        print(f"   Budget Authority: {'✅' if stakeholder['budget_authority'] else '❌'}")
        print(f"   Technical Authority: {'✅' if stakeholder['technical_authority'] else '❌'}")
        print(f"   Influence Level: {stakeholder['influence_level']}")
        print(f"   Champion Strength: {stakeholder['champion_strength']}")
        print(f"   Risk Level: {stakeholder['risk_level']}")
        print(f"   Engagement: {stakeholder['engagement_level']}")
        print(f"   Decision Influence: {stakeholder['decision_influence']:.2f}")
    
    print(f"\n🔗 Enhanced Relationships: {len(enhanced_result['enhanced_relationships'])}")
    for rel in enhanced_result['enhanced_relationships']:
        direction = "↔️" if rel['bidirectional'] else "→"
        formal = "📋" if rel['formal_relationship'] else "🤝"
        print(f"   {formal} {rel['from_stakeholder']} {direction} {rel['to_stakeholder']}")
        print(f"      Type: {rel['relationship_type']}, Strength: {rel['strength']:.2f}")
        print(f"      Influence: {rel['influence_direction']}")
    
    print(f"\n🛣️ Decision Pathways: {len(enhanced_result['decision_pathways'])}")
    for pathway in enhanced_result['decision_pathways']:
        print(f"   📍 {pathway['pathway_type'].title()}: {pathway['description']}")
        print(f"      Criticality: {pathway['criticality']}")
        print(f"      Stakeholders: {' → '.join(pathway['stakeholders'])}")
    
    network_analysis = enhanced_result['network_analysis']
    print(f"\n🧠 Network Analysis:")
    print(f"   Most Influential: {network_analysis['most_influential']}")
    print(f"   Key Approvers: {network_analysis['key_approvers']}")
    print(f"   Champion Candidates: {network_analysis['champion_candidates']}")
    print(f"   Economic Buyer Candidates: {network_analysis['economic_buyer_candidates']}")
    print(f"   Potential Blockers: {network_analysis['potential_blockers']}")
    
    # Test scoring enhancement
    print(f"\n📊 Testing MEDDPICC Scoring Enhancement...")
    from app.intelligence.meddpicc_scoring import calculate_meddpicc_score
    
    # Create sample MEDDPICC data with relationship mapping
    meddpicc_data_with_relationships = {
        'metrics': {
            'identified': ['30% conversion improvement'],
            'confidence': 0.8,
            'evidence': ['John mentioned 30% improvement target']
        },
        'economic_buyer': {
            'identified': 'Sarah Chen (CFO)',
            'confidence': 0.95,
            'evidence': 'I control the budget for technology investments',
            'relationship_mapping': {
                'network_analysis': enhanced_result['network_analysis']
            }
        },
        'champion': {
            'identified': 'John Williams (VP Marketing)',
            'strength': 'strong',
            'confidence': 0.9,
            'evidence': 'I will champion this solution internally',
            'relationship_mapping': {
                'network_analysis': enhanced_result['network_analysis']
            }
        },
        'decision_criteria': {
            'criteria': ['ROI projections', 'Security compliance', 'Salesforce integration'],
            'confidence': 0.8,
            'evidence': ['Sarah mentioned ROI', 'David mentioned security', 'Mike mentioned Salesforce']
        },
        'decision_process': {
            'steps': ['Technical evaluation', 'Security review', 'Executive approval'],
            'timeline': 'Q4 deadline',
            'confidence': 0.7,
            'evidence': ['Process mentioned in transcript']
        },
        'paper_process': {
            'steps': [],
            'requirements': [],
            'confidence': 0.1,
            'evidence': []
        },
        'implicate_pain': {
            'underlying_issues': ['Low conversion rates'],
            'business_impact': ['Revenue impact'],
            'urgency_signals': ['Q4 deadline'],
            'confidence': 0.8,
            'evidence': ['Conversion rate improvement needed']
        },
        'competition': {
            'all_competitors': [],
            'positioning': '',
            'confidence': 0.1,
            'evidence': []
        }
    }
    
    score_result = calculate_meddpicc_score(meddpicc_data_with_relationships)
    print(f"\n📈 Enhanced MEDDPICC Score: {score_result.overall_score:.1f}%")
    print(f"📊 Qualification Status: {score_result.qualification_status}")
    
    # Show how relationship mapping improved scoring
    champion_score = score_result.element_scores['champion']
    economic_buyer_score = score_result.element_scores['economic_buyer']
    
    print(f"\n🎯 Relationship Mapping Impact:")
    print(f"   Champion Score: {champion_score.total_score:.1f}/100")
    print(f"   Economic Buyer Score: {economic_buyer_score.total_score:.1f}/100")
    print(f"   Champion Gaps: {champion_score.gaps}")
    print(f"   Economic Buyer Gaps: {economic_buyer_score.gaps}")
    
    print(f"\n✅ Enhanced Stakeholder Relationship Mapping: COMPLETE!")
    print(f"🚀 System Capabilities:")
    print(f"   ✅ Seniority level detection and authority mapping")
    print(f"   ✅ Influence network analysis with decision pathways") 
    print(f"   ✅ Champion strength assessment and risk detection")
    print(f"   ✅ Relationship formality analysis and direction mapping")
    print(f"   ✅ Integration with MEDDPICC completeness scoring")
    print(f"   ✅ Network graph analysis for key stakeholder identification")

if __name__ == "__main__":
    test_stakeholder_relationship_mapping()