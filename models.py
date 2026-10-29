"""
Data models and helper representations for AI Math Problem Explainer and Error Checker.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class ProblemModel:
    id: str
    topic: str
    subtopic: str
    difficulty: str
    statement: str
    final_answer: str
    acceptable_equivalents: List[str]
    formula: str
    reference_steps: List[Dict[str, Any]]
    common_mistakes: List[str]
    verification_status: str

@dataclass
class ExperimentResultModel:
    id: str
    experiment_id: str
    problem_id: str
    provider: str
    model: str
    prompt_condition: str
    exact_prompt: str
    ai_response: str
    parsed_answer: str
    is_demo: bool
    is_correct: int
    step_accuracy: float
    latency_ms: int
    timestamp: str
    status: str
    verification_initial_answer: Optional[str] = None
    verification_fixed_error: int = 0
    requires_human_review: bool = False
