"""
Core client and configuration structures for the AI-Enhanced Package.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import os

from .exceptions import ConfigurationError
from .utils import calculate_token_estimate


@dataclass
class AIEngineConfig:
    """
    Configuration dataclass for AI engine parameters.
    """
    model_name: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 1024
    api_key: Optional[str] = field(default_factory=lambda: os.environ.get("AI_API_KEY"))
    timeout_seconds: float = 30.0
    enable_caching: bool = True
    enable_streaming: bool = False

    def validate(self) -> None:
        """Validate configuration constraints."""
        if not self.model_name or not self.model_name.strip():
            raise ConfigurationError("model_name cannot be empty.")
        if not (0.0 <= self.temperature <= 2.0):
            raise ConfigurationError(
                f"temperature must be between 0.0 and 2.0, got {self.temperature}"
            )
        if self.max_tokens <= 0:
            raise ConfigurationError(
                f"max_tokens must be a positive integer, got {self.max_tokens}"
            )
        if self.timeout_seconds <= 0:
            raise ConfigurationError(
                f"timeout_seconds must be positive, got {self.timeout_seconds}"
            )


class AIEnhancedClient:
    """
    High-level orchestrator for AI model execution, tracking usage metrics,
    and managing active session history.
    """

    def __init__(self, config: Optional[AIEngineConfig] = None):
        self.config = config or AIEngineConfig()
        self.config.validate()
        self._execution_history: List[Dict[str, Any]] = []
        self._total_tokens_used: int = 0

    @property
    def total_tokens(self) -> int:
        """Returns cumulative estimated tokens consumed by this client instance."""
        return self._total_tokens_used

    @property
    def history(self) -> List[Dict[str, Any]]:
        """Returns an immutable copy of execution history."""
        return list(self._execution_history)

    def record_interaction(
        self,
        prompt: str,
        response_text: str,
        latency_ms: float,
        cached: bool = False,
    ) -> Dict[str, Any]:
        """
        Record an interaction log entry and update cumulative token totals.
        """
        prompt_tokens = calculate_token_estimate(prompt)
        response_tokens = calculate_token_estimate(response_text)
        interaction_tokens = prompt_tokens + response_tokens

        if not cached:
            self._total_tokens_used += interaction_tokens

        entry = {
            "model": self.config.model_name,
            "prompt_tokens": prompt_tokens,
            "response_tokens": response_tokens,
            "total_tokens": interaction_tokens,
            "latency_ms": latency_ms,
            "cached": cached,
        }
        self._execution_history.append(entry)
        return entry

    def reset_history(self) -> None:
        """Clears execution logs and token counters."""
        self._execution_history.clear()
        self._total_tokens_used = 0
