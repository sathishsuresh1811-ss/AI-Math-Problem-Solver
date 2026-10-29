"""
Answer Accuracy Checker Module.
Implements robust, safe mathematical equivalence checking:
- Safe regex-based answer extraction
- Numeric equivalence (fractions, decimals, percentages, tolerances)
- Symbolic equivalence via SymPy without unsafe eval()
- Strict categorization: 1 (Correct), 0 (Incorrect), -1 (Unscorable / Needs Review)
"""

import re
import math
from typing import Tuple, List, Optional
import sympy as sp

# Safe symbols for SymPy evaluation
x, y, t, u, C = sp.symbols('x y t u C', real=True)
SAFE_SYMBOLS = {'x': x, 'y': y, 't': t, 'u': u, 'C': C, 'c': C}

def normalize_text(text: str) -> str:
    """Normalize mathematical strings for comparison."""
    if not text:
        return ""
    cleaned = text.strip()
    # Remove markdown formatting and LaTeX wrappers
    cleaned = re.sub(r'\\boxed\{([^}]+)\}', r'\1', cleaned)
    cleaned = re.sub(r'\\mathbf\{([^}]+)\}', r'\1', cleaned)
    cleaned = re.sub(r'\\text\{([^}]+)\}', r'\1', cleaned)
    cleaned = re.sub(r'\$', '', cleaned)
    cleaned = cleaned.replace('\\times', '*').replace('\\cdot', '*')
    cleaned = cleaned.replace('^', '**')
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def extract_boxed(text: str) -> Optional[str]:
    """Extract content inside \\boxed{...} handling nested braces."""
    idx = text.find('\\boxed{')
    if idx == -1:
        return None
    start = idx + len('\\boxed{')
    depth = 1
    for i in range(start, len(text)):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                return text[start:i]
    return text[start:]

def extract_answer_candidate(ai_response: str) -> str:
    """
    Extract the candidate final answer from an AI's response text.
    Searches for common declaration patterns, boxed answers, or terminal conclusions.
    """
    if not ai_response:
        return ""
        
    lines = [line.strip() for line in ai_response.splitlines() if line.strip()]
    
    # 1. Look for LaTeX boxed expression with nested brace handling
    boxed_val = extract_boxed(ai_response)
    if boxed_val:
        return normalize_text(boxed_val)
        
    # 2. Look for explicit Final Answer statements
    patterns = [
        r'(?:The\s+final\s+answer\s+is|The\s+answer\s+is|Final\s+Answer|Final\s+Result|Answer|Result)[:=\s]*(?:is\s+)?([^\n\r]+)',
        r'(?:Therefore|Hence|Thus)[,\s]+(?:the\s*answer\s*is\s*)?([^\n\r]+)',
        r'(?:x\s*=\s*[-0-9\./]+)',
    ]
    for pattern in patterns:
        matches = re.findall(pattern, ai_response, re.IGNORECASE)
        if matches:
            candidate = matches[-1].strip()
            # Clean leading copulas
            candidate = re.sub(r'^(?:is\s+|equal\s+to\s+|equals\s+|be\s+)', '', candidate, flags=re.IGNORECASE).strip()
            # Clean trailing periods or explanatory text
            candidate = re.split(r'[\.\n;]', candidate)[0].strip()
            if candidate:
                return normalize_text(candidate)

    # 3. If response is short (<= 3 lines), take the last non-empty line
    if len(lines) <= 3 and lines:
        return normalize_text(lines[-1])
        
    # 4. Fallback: inspect last line of response
    if lines:
        last_line = lines[-1]
        if len(last_line) < 80:
            return normalize_text(last_line)
            
    return ""

def parse_percentage_or_fraction(val_str: str) -> Optional[float]:
    """Parse percentage or fractional string into a float safely."""
    val = val_str.strip()
    if val.endswith('%'):
        try:
            num = float(val[:-1].strip())
            return num / 100.0
        except ValueError:
            return None
            
    # Check fraction p/q
    frac_match = re.match(r'^\s*([+-]?\d+)\s*/\s*([+-]?\d+)\s*$', val)
    if frac_match:
        numerator = float(frac_match.group(1))
        denominator = float(frac_match.group(2))
        if denominator != 0:
            return numerator / denominator
            
    try:
        return float(val)
    except ValueError:
        return None

def check_numeric_equivalence(candidate: str, reference: str, tolerance: float = 0.005) -> bool:
    """Check if candidate and reference are numerically equivalent within tolerance."""
    c_clean = candidate.replace('$', '').replace('x =', '').replace('x=', '').strip()
    r_clean = reference.replace('$', '').replace('x =', '').replace('x=', '').strip()
    
    c_val = parse_percentage_or_fraction(c_clean)
    r_val = parse_percentage_or_fraction(r_clean)
    
    if c_val is not None and r_val is not None:
        return abs(c_val - r_val) <= tolerance
    return False

def check_symbolic_equivalence(candidate: str, reference: str) -> Optional[bool]:
    """
    Check symbolic equivalence using SymPy without using eval().
    Returns True if equivalent, False if distinctly not equivalent, None if unparseable.
    """
    c_expr = normalize_text(candidate)
    r_expr = normalize_text(reference)
    
    # Strip common prefixes like f'(x) = or y = or x =
    c_expr = re.sub(r'^[a-zA-Z_\'\s]+\s*=\s*', '', c_expr)
    r_expr = re.sub(r'^[a-zA-Z_\'\s]+\s*=\s*', '', r_expr)
    
    # Also ignore arbitrary constant of integration (+ C) for comparison
    c_expr = re.sub(r'\s*\+\s*C\b', '', c_expr, flags=re.IGNORECASE)
    r_expr = re.sub(r'\s*\+\s*C\b', '', r_expr, flags=re.IGNORECASE)
    
    try:
        # sympify using restricted locals
        sym_c = sp.sympify(c_expr, locals=SAFE_SYMBOLS)
        sym_r = sp.sympify(r_expr, locals=SAFE_SYMBOLS)
        
        diff = sp.simplify(sym_c - sym_r)
        if diff == 0:
            return True
            
        # Try trigonometric or exponential expansion
        expanded_diff = sp.trigsimp(sp.expand(diff))
        if expanded_diff == 0:
            return True
            
        return False
    except Exception:
        # Could not safely parse symbolics
        return None

def evaluate_final_answer(
    candidate_answer: str,
    reference_answer: str,
    acceptable_equivalents: List[str],
    tolerance: float = 0.005
) -> Tuple[int, str, bool]:
    """
    Main evaluation function for final-answer accuracy.
    Returns:
        score: 1 (correct), 0 (incorrect), -1 (unscorable/requires review)
        rationale: Explanatory note on the match
        requires_human_review: Boolean flag
    """
    if not candidate_answer:
        return 0, "No parseable answer found in response", False
        
    cand_norm = normalize_text(candidate_answer).lower()
    ref_norm = normalize_text(reference_answer).lower()
    
    # 1. Exact string match after normalization
    if cand_norm == ref_norm:
        return 1, "Exact normalized text match", False
        
    # 2. Check against acceptable equivalents list
    for eq in acceptable_equivalents:
        eq_norm = normalize_text(eq).lower()
        if cand_norm == eq_norm:
            return 1, f"Matched acceptable equivalent variant: '{eq}'", False
            
    # 3. Numeric equivalence check (fractions, decimals, percentages)
    if check_numeric_equivalence(candidate_answer, reference_answer, tolerance):
        return 1, f"Numerically equivalent within tolerance {tolerance}", False
        
    for eq in acceptable_equivalents:
        if check_numeric_equivalence(candidate_answer, eq, tolerance):
            return 1, f"Numerically matched acceptable equivalent: '{eq}'", False
            
    # 4. Symbolic equivalence check via SymPy
    sym_result = check_symbolic_equivalence(candidate_answer, reference_answer)
    if sym_result is True:
        return 1, "Symbolically equivalent by mathematical simplification", False
        
    for eq in acceptable_equivalents:
        if check_symbolic_equivalence(candidate_answer, eq) is True:
            return 1, f"Symbolically matched equivalent: '{eq}'", False
            
    # 5. Check if it's explicitly wrong (symbolic diff returned False or numeric diff > tolerance)
    if sym_result is False:
        return 0, f"Mathematically inequivalent to reference answer '{reference_answer}'", False
        
    # If candidate is a complex sentence or unparseable, mark for human review
    if len(candidate_answer) > 60 or sym_result is None:
        # Check if reference answer substring is present
        if reference_answer.lower() in candidate_answer.lower():
            return 1, f"Contained reference answer '{reference_answer}' in extracted text", True
        return -1, "Answer output format is complex or ambiguous; flagged for human review", True
        
    return 0, f"Incorrect: parsed '{candidate_answer}', expected '{reference_answer}'", False
