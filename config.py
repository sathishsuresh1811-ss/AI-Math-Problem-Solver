"""
Configuration settings for AI Math Problem Explainer and Error Checker.
Loads environment variables safely without hardcoded API keys.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Load .env file if it exists
load_dotenv(BASE_DIR / ".env")

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "capstone-math-checker-secret-key-2026")
    DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "data" / "math_checker.db"))
    EXPORTS_PATH = os.getenv("EXPORTS_PATH", str(BASE_DIR / "exports"))
    PORT = int(os.getenv("PORT", "5050"))
    
    # API Keys (Loaded from environment variables, never hardcoded)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Model defaults for providers
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-5-haiku-20241022")
    
    # Numerical tolerance for floating-point answers
    NUMERIC_TOLERANCE = float(os.getenv("NUMERIC_TOLERANCE", "0.005"))
    
    # Provider availability checks
    @classmethod
    def get_provider_status(cls):
        return {
            "demo": {
                "name": "Local Reference Solver (Demo Baseline)",
                "available": True,
                "model": "demo-baseline-v1.0",
                "notes": "Always available, deterministic reference benchmark"
            },
            "openai": {
                "name": "ChatGPT (OpenAI)",
                "available": bool(cls.OPENAI_API_KEY),
                "model": cls.OPENAI_MODEL,
                "notes": "Configured via OPENAI_API_KEY" if cls.OPENAI_API_KEY else "Requires OPENAI_API_KEY in .env"
            },
            "gemini": {
                "name": "Google Gemini",
                "available": bool(cls.GEMINI_API_KEY),
                "model": cls.GEMINI_MODEL,
                "notes": "Configured via GEMINI_API_KEY" if cls.GEMINI_API_KEY else "Requires GEMINI_API_KEY in .env"
            },
            "anthropic": {
                "name": "Claude (Anthropic)",
                "available": bool(cls.ANTHROPIC_API_KEY),
                "model": cls.ANTHROPIC_MODEL,
                "notes": "Configured via ANTHROPIC_API_KEY" if cls.ANTHROPIC_API_KEY else "Requires ANTHROPIC_API_KEY in .env"
            }
        }
