"""
Scoring and Error Classification Module.
Implements:
1. Granular Step Evaluation based on reference steps
2. Normalized Step-Accuracy percentage calculation
3. 11-Category Error Classification with supporting evidence
4. Self-Verification Before/After comparative delta analysis
"""

import re
from typing import Dict, List, Any, Tuple, Optional
from answer_checker import (
    extract_answer_candidate,
    evaluate_final_answer,
    check_numeric_equivalence,
    normalize_text
)

ERROR_CATEGORIES = [
    "Arithmetic slip",
    "Wrong formula",
    "Algebraic manipulation error",
    "Conceptual misunderstanding",
    "Probability-rule error",
    "Differentiation or integration rule error",
    "Missing reasoning step",
    "Invalid conclusion",
    "Confident but incorrect reasoning",
    "Answer-format or parsing issue",
    "Unverifiable or ambiguous output"
]

CONFIDENCE_KEYWORDS = [
    "clearly", "obviously", "without doubt", "definitely", "guaranteed",
    "trivial", "it is trivial", "it is proven that", "trivially", "certainly"
]

def evaluate_steps(
    ai_response: str,
    reference_steps: List[Dict[str, Any]]
) -> Tuple[List[Dict[str, Any]], float]:
    """
    Evaluate intermediate steps of the AI response against reference steps.
    Returns:
        evaluations: List of step evaluations with status, score, feedback
        step_accuracy_pct: Normalized step accuracy percentage (0.0 to 100.0)
    """
    if not ai_response or not reference_steps:
        return [], 0.0
        
    response_lower = ai_response.lower()
    step_evals = []
    total_score = 0.0
    max_score = float(len(reference_steps))
    
    for step in reference_steps:
        step_num = step.get("step_number", len(step_evals) + 1)
        desc = step.get("description", "")
        intermediate = str(step.get("intermediate_result", "")).lower()
        formula = str(step.get("formula_used", "")).lower()
        
        # Check if the intermediate key tokens or result appear in the AI text
        clean_intermediate = normalize_text(intermediate).replace(' ', '')
        clean_response = normalize_text(response_lower).replace(' ', '')
        
        found_intermediate = (clean_intermediate in clean_response) if clean_intermediate else False
        
        # Extract keywords from description
        desc_keywords = [w for w in re.findall(r'\b[a-zA-Z]{4,}\b', desc.lower()) 
                         if w not in {'find', 'then', 'with', 'using', 'from', 'into', 'both', 'sides'}]
        matched_keywords = sum(1 for kw in desc_keywords if kw in response_lower)
        keyword_ratio = (matched_keywords / len(desc_keywords)) if desc_keywords else 1.0
        
        if found_intermediate or keyword_ratio >= 0.7:
            status = "correct"
            score = 1.0
            feedback = f"Step {step_num} successfully demonstrated."
        elif keyword_ratio >= 0.4:
            status = "partially_correct"
            score = 0.5
            feedback = f"Step {step_num} partially shown; some intermediate details omitted."
        else:
            status = "missing"
            score = 0.0
            feedback = f"Step {step_num} missing or calculation omitted."
            
        step_evals.append({
            "step_number": step_num,
            "step_description": desc,
            "intermediate_result": step.get("intermediate_result", ""),
            "status": status,
            "score": score,
            "feedback": feedback
        })
        total_score += score
        
    step_accuracy_pct = round((total_score / max_score) * 100.0, 2) if max_score > 0 else 0.0
    return step_evals, step_accuracy_pct

def classify_errors(
    ai_response: str,
    problem: Dict[str, Any],
    is_correct: int,
    step_evals: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Classify errors into the 11 documented categories with evidence.
    """
    errors = []
    response_lower = ai_response.lower() if ai_response else ""
    
    # If final answer is correct and steps are high, no core error
    if is_correct == 1 and all(s["status"] == "correct" for s in step_evals):
        return []
        
    # Check 1: Answer-format or parsing issue
    if is_correct == -1:
        errors.append({
            "category": "Answer-format or parsing issue",
            "evidence": "Candidate final answer could not be confidently matched or contained complex non-standard formatting.",
            "severity": "medium"
        })
        return errors
        
    # Check 2: Confident but incorrect reasoning (Observable rubric)
    if is_correct == 0:
        found_confident_words = [w for w in CONFIDENCE_KEYWORDS if re.search(rf'\b{re.escape(w)}\b', response_lower)]
        if found_confident_words:
            errors.append({
                "category": "Confident but incorrect reasoning",
                "evidence": f"Model used assertive certainty language ({', '.join(found_confident_words)}) while producing an empirically incorrect answer.",
                "severity": "high"
            })

    # Check 3: Domain-specific errors
    topic = problem.get("topic", "")
    
    if topic == "Probability and Statistics" and is_correct == 0:
        # Check for typical probability rule violations (e.g., probability > 1 or base rate fallacy)
        prob_matches = re.findall(r'\b(0\.\d+|\d+/\d+|\d+%)\b', ai_response)
        if any(w in response_lower for w in ["p(a and b)", "p(a|b)", "bayes", "conditional"]):
            errors.append({
                "category": "Probability-rule error",
                "evidence": "Flawed application of conditional probability, independence multiplication, or sample space cardinality.",
                "severity": "high"
            })
            
    if topic == "Calculus" and is_correct == 0:
        if any(w in response_lower for w in ["derivative", "integral", "chain rule", "product rule"]):
            errors.append({
                "category": "Differentiation or integration rule error",
                "evidence": "Calculus derivation deviated from differentiation/integration rules or omitted inner chain derivative.",
                "severity": "high"
            })
            
    if topic == "Algebra" and is_correct == 0:
        errors.append({
            "category": "Algebraic manipulation error",
            "evidence": "Improper sign distribution, invalid factoring, or improper exponent/logarithm simplification.",
            "severity": "medium"
        })

    # Check 4: Missing reasoning step
    missing_steps = [s for s in step_evals if s["status"] == "missing"]
    if missing_steps:
        errors.append({
            "category": "Missing reasoning step",
            "evidence": f"Failed to provide {len(missing_steps)} required intermediate derivation step(s).",
            "severity": "medium"
        })

    # Check 5: Arithmetic slip vs Conceptual misunderstanding
    if is_correct == 0:
        # Check if known common mistakes match
        common_mistakes = problem.get("common_mistakes", [])
        matched_mistake = None
        for cm in common_mistakes:
            # check if numbers from mistake appear
            nums = re.findall(r'\d+', cm)
            if nums and all(n in ai_response for n in nums[:2]):
                matched_mistake = cm
                break
                
        if matched_mistake:
            errors.append({
                "category": "Conceptual misunderstanding",
                "evidence": f"Aligned with documented misconception: {matched_mistake}",
                "severity": "high"
            })
        else:
            # If formulas were cited correctly but answer was wrong, likely arithmetic slip
            if any(s["status"] == "correct" for s in step_evals):
                errors.append({
                    "category": "Arithmetic slip",
                    "evidence": "Intermediate formulation was valid, but calculation or simplification yielded an erroneous terminal value.",
                    "severity": "low"
                })
            else:
                errors.append({
                    "category": "Wrong formula",
                    "evidence": f"Did not properly apply expected formula: {problem.get('formula', 'N/A')}",
                    "severity": "high"
                })

    # Fallback if no specific category matched
    if not errors and is_correct == 0:
        errors.append({
            "category": "Invalid conclusion",
            "evidence": "Derived conclusion is inconsistent with established reference solution.",
            "severity": "medium"
        })
        
    return errors

def analyze_self_verification(
    ai_response: str,
    problem: Dict[str, Any]
) -> Tuple[str, str, int]:
    """
    Analyze response from self-verification condition.
    Splits into pre-verification generation and post-verification check.
    Returns:
        initial_answer: Answer parsed from pre-verification phase
        final_answer: Answer parsed from post-verification / conclusion phase
        verification_effect:
            1: Fixed an error (Initial incorrect -> Final correct)
           -1: Introduced an error (Initial correct -> Final incorrect)
            0: Unchanged (Both correct or both incorrect)
    """
    ref_ans = problem.get("final_answer", "")
    equivalents = problem.get("acceptable_equivalents", [])
    
    # Split response around verification headers
    split_patterns = [
        r'(?:Verification|Independent\s*Check|Check|Alternative\s*Method|Substituting\s*back)[:\n\-]+',
        r'---\s*VERIFICATION\s*---',
        r'Let\s*us\s*verify',
        r'To\s*verify\s*this\s*result'
    ]
    
    pre_text = ai_response
    post_text = ai_response
    
    for pat in split_patterns:
        match = re.search(pat, ai_response, re.IGNORECASE)
        if match:
            pre_text = ai_response[:match.start()]
            post_text = ai_response[match.start():]
            break
            
    initial_candidate = extract_answer_candidate(pre_text)
    final_candidate = extract_answer_candidate(post_text) or extract_answer_candidate(ai_response)
    
    score_initial, _, _ = evaluate_final_answer(initial_candidate, ref_ans, equivalents)
    score_final, _, _ = evaluate_final_answer(final_candidate, ref_ans, equivalents)
    
    if score_initial == 0 and score_final == 1:
        verification_effect = 1  # Fixed an error!
    elif score_initial == 1 and score_final == 0:
        verification_effect = -1 # Introduced an error!
    else:
        verification_effect = 0  # Unchanged
        
    return initial_candidate, final_candidate, verification_effect
