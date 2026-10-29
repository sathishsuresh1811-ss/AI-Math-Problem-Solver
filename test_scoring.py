"""Unit tests for scoring.py."""
import pytest
from scoring import (
    evaluate_steps,
    classify_errors,
    analyze_self_verification,
    ERROR_CATEGORIES
)
from math_dataset import get_problem_by_id

def test_evaluate_steps():
    problem = get_problem_by_id("ALG-01")
    # A response that has 3x = 18 and x = 6
    good_response = "First add 7 to both sides: 3x = 18. Then divide by 3: x = 6."
    step_evals, acc = evaluate_steps(good_response, problem["reference_steps"])
    assert acc >= 90.0
    assert len(step_evals) == 2
    assert step_evals[0]["status"] == "correct"

def test_confident_incorrect_classification():
    problem = get_problem_by_id("ALG-01")
    bad_confident_response = "It is obviously true and definitely guaranteed that x = 99."
    step_evals, acc = evaluate_steps(bad_confident_response, problem["reference_steps"])
    errors = classify_errors(bad_confident_response, problem, is_correct=0, step_evals=step_evals)
    
    categories = [e["category"] for e in errors]
    assert "Confident but incorrect reasoning" in categories

def test_self_verification_fixed_error():
    problem = get_problem_by_id("ALG-01")
    # Response that initially made a mistake (x = 4/3), then verified and corrected to x = 6
    response = """
    Initial Work:
    3x - 7 = 11
    3x = 4
    x = 4/3
    The answer is 4/3.

    --- VERIFICATION ---
    Let us check by substitution:
    3*(4/3) - 7 = 4 - 7 = -3 != 11. An error was made!
    Let's re-solve: 3x = 11 + 7 = 18, so x = 6.
    Check: 3*6 - 7 = 18 - 7 = 11.
    Final Answer: 6
    """
    initial_ans, final_ans, effect = analyze_self_verification(response, problem)
    assert effect == 1  # Verified and fixed error!
    assert "6" in final_ans
