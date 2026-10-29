"""Unit tests for answer_checker.py."""
import pytest
from answer_checker import (
    extract_answer_candidate,
    check_numeric_equivalence,
    check_symbolic_equivalence,
    evaluate_final_answer
)

def test_extract_answer_candidate():
    text1 = "Here is the work.\nStep 1: 3x = 18.\nFinal Answer: 6"
    assert extract_answer_candidate(text1) == "6"
    
    text2 = "Therefore, \\boxed{\\frac{1}{2}} is our result."
    assert extract_answer_candidate(text2) == "\\frac{1}{2}"
    
    text3 = "Hence the answer is 15x^2 - 8x + 7."
    assert "15x" in extract_answer_candidate(text3)

def test_numeric_equivalence():
    # Fractions vs Decimals
    assert check_numeric_equivalence("0.5", "1/2")
    assert check_numeric_equivalence("50%", "1/2")
    assert check_numeric_equivalence("0.25", "1/4")
    assert check_numeric_equivalence("19/118", "0.1610", tolerance=0.005)
    
    # Negative cases
    assert not check_numeric_equivalence("0.75", "1/2")

def test_symbolic_equivalence():
    # Factorization
    assert check_symbolic_equivalence("(x - 4)*(x - 5)", "x^2 - 9*x + 20")
    
    # Derivative product
    assert check_symbolic_equivalence("(x**2 + 2*x)*exp(x)", "2*x*exp(x) + x**2*exp(x)")
    
    # Polynomial identity
    assert check_symbolic_equivalence("4*x**2 + 12*x*y + 9*y**2", "(2*x + 3*y)**2")

def test_evaluate_final_answer_correct():
    score, rationale, review = evaluate_final_answer(
        candidate_answer="x = 6",
        reference_answer="6",
        acceptable_equivalents=["6", "x = 6"]
    )
    assert score == 1

def test_evaluate_final_answer_incorrect():
    score, rationale, review = evaluate_final_answer(
        candidate_answer="x = 14",
        reference_answer="6",
        acceptable_equivalents=["6", "x = 6"]
    )
    assert score == 0

def test_evaluate_final_answer_probability():
    score, _, _ = evaluate_final_answer(
        candidate_answer="0.5",
        reference_answer="1/2",
        acceptable_equivalents=["1/2", "0.5", "50%"]
    )
    assert score == 1
