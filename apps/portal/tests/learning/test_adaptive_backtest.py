import json
import os
import pytest

def test_adaptive_cases_exist():
    fixture_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'adaptive_cases.json')
    assert os.path.exists(fixture_path), "adaptive_cases.json must exist"
    
    with open(fixture_path, 'r', encoding='utf-8') as f:
        cases = json.load(f)
        
    assert len(cases) == 14, "Must contain all 14 cases from A to N"
    
    expected_scenarios = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']
    for case in cases:
        assert case['scenario_id'] in expected_scenarios
        assert 'expected_action' in case
        assert 'description' in case
