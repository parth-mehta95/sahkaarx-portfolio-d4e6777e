"""
Custom exception hierarchy for the AI-Enhanced Package.
"""


class AIError(Exception):
    """Base exception for all ai_enhanced_pkg runtime errors."""

    def __init__(self, message: str, error_code: str = "ERR_GENERAL"):
        super().__init__(message)
        self.message = message
        self.error_code = error_code

    def __str__(self) -> str:
        return f"[{self.error_code}] {self.message}"


class ConfigurationError(AIError):
    """Raised when an invalid configuration is supplied."""

    def __init__(self, message: str):
        super().__init__(message, error_code="ERR_CONFIG_INVALID")


class PromptValidationError(AIError):
    """Raised when prompt template validation fails."""

    def __init__(self, message: str, missing_keys: list = None):
        super().__init__(message, error_code="ERR_PROMPT_VALIDATION")
        self.missing_keys = missing_keys or []


class RateLimitExceededError(AIError):
    """Raised when request rate limits are breached."""

    def __init__(self, message: str = "Rate limit threshold exceeded."):
        super().__init__(message, error_code="ERR_RATE_LIMIT")


class ModelExecutionError(AIError):
    """Raised when model inference or response generation encounters an error."""

    def __init__(self, message: str):
        super().__init__(message, error_code="ERR_EXECUTION_FAILED")
