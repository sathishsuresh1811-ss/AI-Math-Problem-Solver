"""Unit tests for math_dataset.py verifying dataset integrity."""
import pytest
from math_dataset import PROBLEMS, get_all_problems, get_problem_by_id, get_problems_by_topic

def test_problem_count():
    assert len(PROBLEMS) == 30, f"Expected 30 problems, got {len(PROBLEMS)}"

def test_topic_distribution():
    algebra = [p for p in PROBLEMS if p["topic"] == "Algebra"]
    prob = [p for p in PROBLEMS if p["topic"] == "Probability and Statistics"]
    calc = [p for p in PROBLEMS if p["topic"] == "Calculus"]
    
    assert len(algebra) == 10, f"Expected 10 Algebra problems, got {len(algebra)}"
    assert len(prob) == 10, f"Expected 10 Probability problems, got {len(prob)}"
    assert len(calc) == 10, f"Expected 10 Calculus problems, got {len(calc)}"

def test_difficulty_representation():
    for topic in ["Algebra", "Probability and Statistics", "Calculus"]:
        problems = [p for p in PROBLEMS if p["topic"] == topic]
        difficulties = {p["difficulty"] for p in problems}
        assert "Easy" in difficulties, f"{topic} missing Easy problems"
        assert "Medium" in difficulties, f"{topic} missing Medium problems"
        assert "Hard" in difficulties, f"{topic} missing Hard problems"

def test_required_fields():
    required_keys = [
        "id", "topic", "difficulty", "statement", "final_answer",
        "acceptable_equivalents", "formula", "reference_steps",
        "common_mistakes", "verification_status"
    ]
    seen_ids = set()
    for p in PROBLEMS:
        for key in required_keys:
            assert key in p, f"Problem {p.get('id', 'Unknown')} missing key {key}"
            assert p[key], f"Problem {p['id']} has empty value for {key}"
        
        # Check uniqueness of IDs
        assert p["id"] not in seen_ids, f"Duplicate problem ID: {p['id']}"
        seen_ids.add(p["id"])
        
        # Check reference steps format
        assert isinstance(p["reference_steps"], list), f"{p['id']} reference_steps must be list"
        assert len(p["reference_steps"]) >= 2, f"{p['id']} should have at least 2 steps"
        for step in p["reference_steps"]:
            assert "step_number" in step
            assert "description" in step
            assert "intermediate_result" in step
            assert "formula_used" in step

def test_retrieval_functions():
    p = get_problem_by_id("ALG-01")
    assert p is not None
    assert p["id"] == "ALG-01"
    assert p["final_answer"] == "6"
    
    calc_probs = get_problems_by_topic("Calculus")
    assert len(calc_probs) == 10
