"""
Utility helpers for AI-Enhanced Package.
Includes token estimation, string sanitization, cache key hashing, and retry logic.
"""

import functools
import hashlib
import re
import time
from typing import Any, Callable, Dict


def calculate_token_estimate(text: str) -> int:
    """
    Estimate token count for a given text snippet.
    Approximates ~4 characters per token for standard English LLM tokenizers.

    Args:
        text: Input string.

    Returns:
        Estimated integer token count (minimum 1 for non-empty text).
    """
    if not text:
        return 0
    clean_text = text.strip()
    if not clean_text:
        return 0
    # Average 4 characters per token heuristic with a base floor of word count
    char_estimate = len(clean_text) / 4.0
    word_estimate = len(clean_text.split()) * 1.3
    return max(1, int(round((char_estimate + word_estimate) / 2.0)))


def sanitize_prompt_text(text: str, max_consecutive_newlines: int = 2) -> str:
    """
    Cleans prompt input text by removing null bytes, stripping trailing whitespace,
    and collapsing excessive consecutive newlines.

    Args:
        text: Raw input string.
        max_consecutive_newlines: Maximum permitted consecutive newlines.

    Returns:
        Sanitized string.
    """
    if not text:
        return ""
    # Strip null characters
    sanitized = text.replace("\x00", "")
    # Normalize Windows line endings to Unix style
    sanitized = sanitized.replace("\r\n", "\n").replace("\r", "\n")
    # Collapse excess newlines
    pattern = r"\n{" + str(max_consecutive_newlines + 1) + r",}"
    sanitized = re.sub(pattern, "\n" * max_consecutive_newlines, sanitized)
    return sanitized.strip()


def generate_cache_key(prompt: str, params: Dict[str, Any]) -> str:
    """
    Generate a deterministic SHA-256 cache key based on prompt and parameters.

    Args:
        prompt: Prompt string.
        params: Dictionary of parameters (temperature, max_tokens, etc.).

    Returns:
        Hexadecimal hash string.
    """
    sorted_params = sorted([(k, str(v)) for k, v in params.items()])
    raw_payload = f"{prompt}|{sorted_params}"
    return hashlib.sha256(raw_payload.encode("utf-8")).hexdigest()


def exponential_backoff(max_retries: int = 3, base_delay: float = 0.5):
    """
    Decorator for retrying transient operations with exponential backoff delay.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = base_delay
            last_exception = None
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    last_exception = exc
                    if attempt == max_retries:
                        break
                    time.sleep(delay)
                    delay *= 2.0
            raise last_exception
        return wrapper
    return decorator
