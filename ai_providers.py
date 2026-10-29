"""
AI Providers Module.
Integrates live AI APIs (ChatGPT, Gemini, Claude) with fallback to Local Reference Solver.
Strictly separates live API outputs from demo baseline data.
"""

import os
import time
import json
import requests
from typing import Dict, Any, Optional, List
from config import Config
from prompt_templates import format_prompt

class BaseAIProvider:
    def __init__(self, name: str, model_id: str, is_demo: bool = False):
        self.name = name
        self.model_id = model_id
        self.is_demo = is_demo

    def generate(self, problem: Dict[str, Any], prompt_condition: str) -> Dict[str, Any]:
        raise NotImplementedError("Subclasses must implement generate()")


class LocalDemoSolver(BaseAIProvider):
    """
    Local Reference Solver (Demo Baseline).
    Provides deterministic, mathematically transparent solutions for all 30 problems.
    Explicitly labeled as baseline/demo data, NOT a live commercial AI model.
    """
    def __init__(self):
        super().__init__(
            name="Local Reference Solver (Demo Baseline)",
            model_id="demo-baseline-v1.0",
            is_demo=True
        )

    def generate(self, problem: Dict[str, Any], prompt_condition: str) -> Dict[str, Any]:
        start_time = time.time()
        # Simulated fast local computation
        time.sleep(0.005)
        
        prob_id = problem["id"]
        topic = problem["topic"]
        statement = problem["statement"]
        ref_ans = problem["final_answer"]
        steps = problem["reference_steps"]
        formula = problem.get("formula", "Standard mathematical identity")
        
        # Build condition-specific realistic responses
        if prompt_condition == "plain":
            # Plain baseline: direct concise answer; occasional careless slip on a couple hard problems to simulate real baseline
            if prob_id == "ALG-06": # Logarithmic domain oversight slip in plain mode
                text = f"Solving {statement}\nWe get x^2 - 2x = 8, so (x-4)(x+2) = 0.\nTherefore, the answers are x = 4 and x = -2.\nFinal Answer: 4, -2"
            elif prob_id == "PROB-09": # Base rate fallacy slip in plain mode
                text = f"The test accuracy is 95%, so the probability is approximately 0.95.\nFinal Answer: 0.95"
            elif prob_id == "CALC-04": # Chain rule omitted inner derivative slip
                text = f"Differentiating sin(3x^2 + 1) with respect to x gives cos(3x^2 + 1).\nFinal Answer: cos(3x^2 + 1)"
            else:
                text = f"To solve this: {statement}\nFinal Answer: {ref_ans}"

        elif prompt_condition == "step_by_step":
            # Chain-of-thought: explicit formula, intermediate calculations, clear final answer
            step_lines = []
            step_lines.append(f"Problem: {statement}\n")
            step_lines.append(f"Relevant Formula/Theorem: {formula}\n")
            step_lines.append("Step-by-step Solution:")
            for s in steps:
                step_lines.append(f"Step {s['step_number']}: {s['description']}")
                step_lines.append(f"Calculation / Result: {s['intermediate_result']}")
                step_lines.append(f"Applied Rule: {s['formula_used']}\n")
            step_lines.append(f"Conclusion:\nFinal Answer: {ref_ans}")
            text = "\n".join(step_lines)

        elif prompt_condition == "self_verification":
            # Dual-phase: Initial solution derivation + explicit verification section
            step_lines = []
            step_lines.append(f"Initial Mathematical Derivation for: {statement}\n")
            step_lines.append(f"Formula: {formula}\n")
            
            # For ALG-06 and PROB-09, simulate an initial slip that the verification phase catches and fixes!
            if prob_id == "ALG-06":
                step_lines.append("Derivation:\nlog2(x(x - 2)) = 3 => x^2 - 2x - 8 = 0 => (x - 4)(x + 2) = 0.")
                step_lines.append("Initial candidate solutions: x = 4 and x = -2.")
                step_lines.append("The answer is 4, -2.")
                step_lines.append("\n--- VERIFICATION ---")
                step_lines.append("Independent Check:")
                step_lines.append("1. Test x = -2 in original log arguments: log2(-2) is undefined because logarithm domain requires x > 0.")
                step_lines.append("2. Error identified! x = -2 is an extraneous root and must be rejected.")
                step_lines.append("3. Test x = 4: log2(4) + log2(4 - 2) = 2 + 1 = 3. Validated.")
                step_lines.append(f"Verified Final Answer: {ref_ans}")
            elif prob_id == "PROB-09":
                step_lines.append("Initial calculation: Test sensitivity is 0.95.")
                step_lines.append("Initial Answer: 0.95")
                step_lines.append("\n--- VERIFICATION ---")
                step_lines.append("Independent Check using Bayes' Theorem:")
                step_lines.append("P(D|+) = P(+|D)P(D) / [P(+|D)P(D) + P(+|D')P(D')]")
                step_lines.append("Numerator: 0.95 * 0.01 = 0.0095")
                step_lines.append("Denominator: 0.0095 + (0.05 * 0.99) = 0.0590")
                step_lines.append("Quotient: 0.0095 / 0.0590 = 19/118 (approx 16.1%).")
                step_lines.append("Initial answer ignored false positives! Correction applied.")
                step_lines.append(f"Verified Final Answer: {ref_ans}")
            else:
                for s in steps:
                    step_lines.append(f"Step {s['step_number']}: {s['description']} => {s['intermediate_result']}")
                step_lines.append(f"Derived Answer: {ref_ans}")
                step_lines.append("\n--- VERIFICATION ---")
                step_lines.append("Independent Verification:")
                step_lines.append(f"Testing derived result {ref_ans} by direct substitution / alternative algebraic check:")
                step_lines.append(f"All constraints and intermediate equalities hold true without contradiction.")
                step_lines.append(f"Verified Final Answer: {ref_ans}")

            text = "\n".join(step_lines)
            
        else:
            text = f"Final Answer: {ref_ans}"

        latency = int((time.time() - start_time) * 1000)
        return {
            "provider": self.name,
            "model": self.model_id,
            "response_text": text,
            "latency_ms": latency,
            "is_demo": True,
            "status": "success",
            "error_message": None
        }


class OpenAIProvider(BaseAIProvider):
    """OpenAI ChatGPT provider integration."""
    def __init__(self):
        super().__init__(
            name="ChatGPT (OpenAI)",
            model_id=Config.OPENAI_MODEL,
            is_demo=False
        )

    def generate(self, problem: Dict[str, Any], prompt_condition: str) -> Dict[str, Any]:
        api_key = Config.OPENAI_API_KEY
        if not api_key:
            return {
                "provider": self.name,
                "model": self.model_id,
                "response_text": "",
                "latency_ms": 0,
                "is_demo": False,
                "status": "error",
                "error_message": "OpenAI API key missing. Please set OPENAI_API_KEY in your .env file."
            }

        prompt = format_prompt(prompt_condition, problem["statement"])
        start_time = time.time()
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": self.model_id,
                "messages": [
                    {"role": "system", "content": "You are an expert mathematician and solver. Provide mathematically rigorous answers."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1
            }
            res = requests.post(url, headers=headers, json=payload, timeout=30)
            latency = int((time.time() - start_time) * 1000)
            if res.status_code == 200:
                data = res.json()
                text = data["choices"][0]["message"]["content"]
                return {
                    "provider": self.name,
                    "model": data.get("model", self.model_id),
                    "response_text": text,
                    "latency_ms": latency,
                    "is_demo": False,
                    "status": "success",
                    "error_message": None
                }
            else:
                return {
                    "provider": self.name,
                    "model": self.model_id,
                    "response_text": "",
                    "latency_ms": latency,
                    "is_demo": False,
                    "status": "error",
                    "error_message": f"OpenAI API Error {res.status_code}: {res.text}"
                }
        except Exception as e:
            latency = int((time.time() - start_time) * 1000)
            return {
                "provider": self.name,
                "model": self.model_id,
                "response_text": "",
                "latency_ms": latency,
                "is_demo": False,
                "status": "error",
                "error_message": f"Network/Request Exception: {str(e)}"
            }


class GeminiProvider(BaseAIProvider):
    """Google Gemini provider integration."""
    def __init__(self):
        super().__init__(
            name="Google Gemini",
            model_id=Config.GEMINI_MODEL,
            is_demo=False
        )

    def generate(self, problem: Dict[str, Any], prompt_condition: str) -> Dict[str, Any]:
        api_key = Config.GEMINI_API_KEY
        if not api_key:
            return {
                "provider": self.name,
                "model": self.model_id,
                "response_text": "",
                "latency_ms": 0,
                "is_demo": False,
                "status": "error",
                "error_message": "Gemini API key missing. Please set GEMINI_API_KEY in your .env file."
            }

        prompt = format_prompt(prompt_condition, problem["statement"])
        start_time = time.time()
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_id}:generateContent?key={api_key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [
                    {"parts": [{"text": prompt}]}
                ],
                "generationConfig": {"temperature": 0.1}
            }
            res = requests.post(url, headers=headers, json=payload, timeout=30)
            latency = int((time.time() - start_time) * 1000)
            if res.status_code == 200:
                data = res.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return {
                    "provider": self.name,
                    "model": self.model_id,
                    "response_text": text,
                    "latency_ms": latency,
                    "is_demo": False,
                    "status": "success",
                    "error_message": None
                }
            else:
                return {
                    "provider": self.name,
                    "model": self.model_id,
                    "response_text": "",
                    "latency_ms": latency,
                    "is_demo": False,
                    "status": "error",
                    "error_message": f"Gemini API Error {res.status_code}: {res.text}"
                }
        except Exception as e:
            latency = int((time.time() - start_time) * 1000)
            return {
                "provider": self.name,
                "model": self.model_id,
                "response_text": "",
                "latency_ms": latency,
                "is_demo": False,
                "status": "error",
                "error_message": f"Network/Request Exception: {str(e)}"
            }


class ClaudeProvider(BaseAIProvider):
    """Anthropic Claude provider integration."""
    def __init__(self):
        super().__init__(
            name="Claude (Anthropic)",
            model_id=Config.ANTHROPIC_MODEL,
            is_demo=False
        )

    def generate(self, problem: Dict[str, Any], prompt_condition: str) -> Dict[str, Any]:
        api_key = Config.ANTHROPIC_API_KEY
        if not api_key:
            return {
                "provider": self.name,
                "model": self.model_id,
                "response_text": "",
                "latency_ms": 0,
                "is_demo": False,
                "status": "error",
                "error_message": "Anthropic API key missing. Please set ANTHROPIC_API_KEY in your .env file."
            }

        prompt = format_prompt(prompt_condition, problem["statement"])
        start_time = time.time()
        try:
            url = "https://api.anthropic.com/v1/messages"
            headers = {
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json"
            }
            payload = {
                "model": self.model_id,
                "max_tokens": 1024,
                "temperature": 0.1,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
            res = requests.post(url, headers=headers, json=payload, timeout=30)
            latency = int((time.time() - start_time) * 1000)
            if res.status_code == 200:
                data = res.json()
                text = data["content"][0]["text"]
                return {
                    "provider": self.name,
                    "model": data.get("model", self.model_id),
                    "response_text": text,
                    "latency_ms": latency,
                    "is_demo": False,
                    "status": "success",
                    "error_message": None
                }
            else:
                return {
                    "provider": self.name,
                    "model": self.model_id,
                    "response_text": "",
                    "latency_ms": latency,
                    "is_demo": False,
                    "status": "error",
                    "error_message": f"Claude API Error {res.status_code}: {res.text}"
                }
        except Exception as e:
            latency = int((time.time() - start_time) * 1000)
            return {
                "provider": self.name,
                "model": self.model_id,
                "response_text": "",
                "latency_ms": latency,
                "is_demo": False,
                "status": "error",
                "error_message": f"Network/Request Exception: {str(e)}"
            }


PROVIDERS: Dict[str, BaseAIProvider] = {
    "demo": LocalDemoSolver(),
    "openai": OpenAIProvider(),
    "gemini": GeminiProvider(),
    "anthropic": ClaudeProvider()
}

def get_provider(provider_key: str) -> Optional[BaseAIProvider]:
    """Retrieve provider instance by key."""
    return PROVIDERS.get(provider_key.lower())

def list_providers_status() -> List[Dict[str, Any]]:
    """List all available providers with configuration status."""
    status_dict = Config.get_provider_status()
    result = []
    for key, info in status_dict.items():
        result.append({
            "key": key,
            "name": info["name"],
            "model": info["model"],
            "available": info["available"],
            "notes": info["notes"],
            "is_demo": (key == "demo")
        })
    return result
