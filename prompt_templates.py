"""
Prompt Templates Module for AI Math Problem Explainer and Error Checker.
Defines three standardized experimental conditions:
1. Plain Prompt
2. Step-by-Step Prompt
3. Self-Verification Prompt
"""

from typing import Dict, Any

PROMPT_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "plain": {
        "id": "plain",
        "name": "Plain Prompt",
        "condition_code": "COND-A",
        "description": "Minimal baseline prompt asking directly for the solution and answer without guidance on reasoning or structure.",
        "template": "Solve this mathematics problem: {problem}. Give your answer.",
        "intended_behavior": "Tests raw zero-shot capability, response conciseness, and baseline mathematical intuition.",
        "common_issues": "Omission of intermediate derivations, higher rate of careless arithmetic slips, difficulty in parsing unstructured text."
    },
    "step_by_step": {
        "id": "step_by_step",
        "name": "Step-by-Step Reasoning Prompt",
        "condition_code": "COND-B",
        "description": "Chain-of-thought prompt prompting explicit formula declaration, intermediate calculations, and deductive coherence.",
        "template": "Solve this mathematics problem step by step. State the relevant formula, explain each calculation, show intermediate steps, and provide the final answer. Check that the reasoning follows mathematically.\n\nProblem:\n{problem}",
        "intended_behavior": "Encourages decomposition of complex problems, structured derivations, and explicit formula referencing.",
        "common_issues": "Verbosity, hallucination of unnecessary lemmas, failure in error-checking despite detailed steps."
    },
    "self_verification": {
        "id": "self_verification",
        "name": "Self-Verification Prompt",
        "condition_code": "COND-C",
        "description": "Metacognitive dual-phase prompt requiring the solver to derive the solution, then independently verify or critique the answer using an alternative technique or substitution.",
        "template": "Solve this mathematics problem step by step. State the relevant formula, show the calculations, provide the final answer, independently verify the result using substitution, an alternative method, or another appropriate mathematical check, and correct any errors you identify. Explain the verification.\n\nProblem:\n{problem}",
        "intended_behavior": "Simulates metacognitive reflection, allowing the model to detect arithmetic slips or flawed assumptions before finalizing.",
        "common_issues": "Verification bias (confirming an incorrect answer through circular logic), or rarely, introducing a new error into an initially correct answer."
    }
}

def format_prompt(template_key: str, problem_statement: str) -> str:
    """Format prompt with the given problem statement."""
    template_info = PROMPT_TEMPLATES.get(template_key)
    if not template_info:
        template_info = PROMPT_TEMPLATES["plain"]
    return template_info["template"].format(problem=problem_statement.strip())

def get_all_templates() -> Dict[str, Dict[str, Any]]:
    """Return all prompt templates."""
    return PROMPT_TEMPLATES
