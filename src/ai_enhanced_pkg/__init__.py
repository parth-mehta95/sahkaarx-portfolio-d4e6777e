"""
AI-Enhanced Python Package (ai_enhanced_pkg)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A modular Python package providing prompt engineering, token optimization,
response streaming, and batch inference pipelines with unified conflict-resolved features.
"""

from .core import AIEngineConfig, AIEnhancedClient
from .exceptions import (
    AIError,
    ConfigurationError,
    ModelExecutionError,
    PromptValidationError,
    RateLimitExceededError,
)
from .prompt_engine import PromptTemplate, ProcessedResponse, PromptEngine
from .utils import (
    calculate_token_estimate,
    sanitize_prompt_text,
    exponential_backoff,
)

__version__ = "1.0.0"
__author__ = "Parth Mehta"
__email__ = "parth.mehta@ttpl.ind.in"
__license__ = "MIT"

__all__ = [
    "AIEngineConfig",
    "AIEnhancedClient",
    "PromptTemplate",
    "ProcessedResponse",
    "PromptEngine",
    "calculate_token_estimate",
    "sanitize_prompt_text",
    "exponential_backoff",
    "AIError",
    "PromptValidationError",
    "ConfigurationError",
    "RateLimitExceededError",
    "ModelExecutionError",
]
