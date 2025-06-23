#!/usr/bin/env python3
"""
Test Template Imprinting Protocol Pattern System
✅ Applied: TEMPLATE_IMPRINTING_PROTOCOL
"""

import json
import os
from pathlib import Path
from typing import Dict, Any

# PATTERN_REF: TEMPLATE_IMPRINTING_PROTOCOL
def test_neural_imprint_loading():
    """Test that neural imprint loads correctly."""
    neural_imprint_path = Path(".ai/NEURAL_IMPRINT.json")
    assert neural_imprint_path.exists(), "Neural imprint file missing"
    
    with open(neural_imprint_path, 'r') as f:
        neural_imprint = json.load(f)
    
    # Validate required sections
    required_sections = ["imprint_mode", "behavioral_hierarchy", "response_templates", "neural_anchors"]
    for section in required_sections:
        assert section in neural_imprint, f"Missing section: {section}"
    
    print("✅ Neural imprint loaded successfully")
    return neural_imprint

# PATTERN_REF: TEMPLATE_IMPRINTING_PROTOCOL  
def test_session_contract_loading():
    """Test that session contract loads correctly."""
    session_path = Path(".project_memory/current_epic/active_session.json")
    assert session_path.exists(), "Session contract missing"
    
    with open(session_path, 'r') as f:
        session = json.load(f)
    
    # Validate session contract structure
    required_sections = ["session_contract", "behavioral_contract", "neural_anchors"]
    for section in required_sections:
        assert section in session, f"Missing session section: {section}"
    
    print("✅ Session contract loaded successfully")
    return session

# PATTERN_REF: TEMPLATE_IMPRINTING_PROTOCOL
def test_pattern_registry_loading():
    """Test that pattern registry loads correctly."""
    registry_path = Path(".project_memory/patterns/IMPRINT_PATTERN_INDEX.json")
    assert registry_path.exists(), "Pattern registry missing"
    
    with open(registry_path, 'r') as f:
        registry = json.load(f)
    
    # Validate registry structure
    assert "available_patterns" in registry, "Missing available_patterns"
    assert "pattern_selection_rules" in registry, "Missing pattern_selection_rules"
    
    patterns = registry["available_patterns"]
    expected_patterns = ["DATABASE_ACCESS_PATTERN", "AGENT_COMMUNICATION_PATTERN", "CACHING_PATTERN"]
    
    for pattern in expected_patterns:
        assert pattern in patterns, f"Missing pattern: {pattern}"
        pattern_data = patterns[pattern]
        assert "file" in pattern_data, f"Pattern {pattern} missing file reference"
        assert "token_count" in pattern_data, f"Pattern {pattern} missing token_count"
        assert "adherence_requirement" in pattern_data, f"Pattern {pattern} missing adherence_requirement"
    
    print("✅ Pattern registry loaded successfully")
    return registry

# PATTERN_REF: TEMPLATE_IMPRINTING_PROTOCOL
def test_individual_patterns():
    """Test that individual pattern files load correctly."""
    patterns_dir = Path(".project_memory/patterns")
    pattern_files = [
        "DATABASE_ACCESS_IMPRINT.json",
        "AGENT_COMMUNICATION_IMPRINT.json", 
        "CACHING_IMPRINT.json"
    ]
    
    loaded_patterns = {}
    
    for pattern_file in pattern_files:
        pattern_path = patterns_dir / pattern_file
        assert pattern_path.exists(), f"Pattern file missing: {pattern_file}"
        
        with open(pattern_path, 'r') as f:
            pattern = json.load(f)
        
        # Validate pattern structure
        required_sections = [
            "imprint_mode", 
            "behavioral_contract", 
            "imprinting_tokens",
            "template_structure",
            "neural_anchors",
            "validation_rules",
            "adherence_scoring"
        ]
        
        for section in required_sections:
            assert section in pattern, f"Pattern {pattern_file} missing section: {section}"
        
        # Validate imprinting tokens length
        token_count = pattern.get("token_count", 0)
        actual_tokens = len(pattern["imprinting_tokens"])
        assert actual_tokens <= 200, f"Pattern {pattern_file} imprinting tokens too long: {actual_tokens} chars"
        
        pattern_id = pattern["imprint_mode"]["pattern_id"]
        loaded_patterns[pattern_id] = pattern
        print(f"✅ Pattern loaded: {pattern_id} ({actual_tokens} chars)")
    
    return loaded_patterns

# PATTERN_REF: TEMPLATE_IMPRINTING_PROTOCOL
def test_behavioral_adherence():
    """Test behavioral adherence scoring."""
    patterns = test_individual_patterns()
    
    for pattern_id, pattern in patterns.items():
        adherence = pattern["adherence_scoring"]
        
        # Validate adherence scoring
        assert "full_compliance" in adherence, f"Pattern {pattern_id} missing full_compliance score"
        assert adherence["full_compliance"] == 1.0, f"Pattern {pattern_id} full_compliance should be 1.0"
        assert "no_pattern_usage" in adherence, f"Pattern {pattern_id} missing no_pattern_usage score" 
        assert adherence["no_pattern_usage"] == 0.0, f"Pattern {pattern_id} no_pattern_usage should be 0.0"
        
        print(f"✅ Adherence scoring validated: {pattern_id}")

# PATTERN_REF: TEMPLATE_IMPRINTING_PROTOCOL
def simulate_pattern_application():
    """Simulate applying patterns to code generation."""
    patterns = test_individual_patterns()
    
    # Simulate database code generation
    db_pattern = patterns["DATABASE_ACCESS_PATTERN"]
    db_template = db_pattern["template_structure"]["class_template"]
    
    # Generate code using pattern
    generated_code = f"""# PATTERN_REF: DATABASE_ACCESS_PATTERN
{db_template.format(Entity="Prompt")}
# DECISION_REF: TIP_DB_001
"""
    
    print("✅ Database pattern applied:")
    print(generated_code[:100] + "...")
    
    # Simulate agent code generation  
    agent_pattern = patterns["AGENT_COMMUNICATION_PATTERN"]
    agent_neural_anchor = agent_pattern["neural_anchors"]["success_indicator"]
    
    print(f"✅ Agent pattern neural anchor: {agent_neural_anchor}")
    
    return True

# PATTERN_REF: TEMPLATE_IMPRINTING_PROTOCOL
def main():
    """Run all Template Imprinting Protocol tests."""
    print("🧪 Testing Template Imprinting Protocol System")
    print("=" * 50)
    
    try:
        # Test core system loading
        neural_imprint = test_neural_imprint_loading()
        session = test_session_contract_loading() 
        registry = test_pattern_registry_loading()
        
        # Test individual patterns
        patterns = test_individual_patterns()
        
        # Test behavioral adherence
        test_behavioral_adherence()
        
        # Test pattern application simulation
        simulate_pattern_application()
        
        print("=" * 50)
        print("🎯 Template Imprinting Protocol System: FULLY OPERATIONAL")
        print(f"📊 Neural Imprint: {neural_imprint['imprint_mode']['level']}")
        print(f"📋 Session Type: {session['session_contract']['session_type']}")
        print(f"🔧 Patterns Available: {len(patterns)}")
        print("✅ Applied: TEMPLATE_IMPRINTING_PROTOCOL | 📋 Decision: TIP_VALIDATION_001")
        
        return True
        
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"💥 Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)