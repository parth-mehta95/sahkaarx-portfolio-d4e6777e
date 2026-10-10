"""
Unit tests for utility functions.
"""

from ai_enhanced_pkg.utils import (
    calculate_token_estimate,
    generate_cache_key,
    sanitize_prompt_text,
)


def test_calculate_token_estimate_empty():
    assert calculate_token_estimate("") == 0
    assert calculate_token_estimate("   ") == 0


def test_calculate_token_estimate_non_empty():
    text = "The quick brown fox jumps over the lazy dog."
    tokens = calculate_token_estimate(text)
    assert tokens > 0
    assert 5 <= tokens <= 15


def test_sanitize_prompt_text_excess_newlines():
    raw = "Line 1\n\n\n\n\nLine 2"
    sanitized = sanitize_prompt_text(raw, max_consecutive_newlines=2)
    assert "\n\n\n" not in sanitized
    assert "Line 1\n\nLine 2" == sanitized


def test_sanitize_prompt_text_null_bytes():
    raw = "Hello\x00World"
    assert sanitize_prompt_text(raw) == "HelloWorld"


def test_generate_cache_key_deterministic():
    key1 = generate_cache_key("test prompt", {"temp": 0.5, "model": "gpt-4"})
    key2 = generate_cache_key("test prompt", {"model": "gpt-4", "temp": 0.5})
    key3 = generate_cache_key("different prompt", {"temp": 0.5, "model": "gpt-4"})

    assert key1 == key2
    assert key1 != key3
    assert len(key1) == 64  # SHA-256 hex string length
