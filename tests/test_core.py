"""
Unit tests for core configuration and AIEnhancedClient.
"""

import pytest
from ai_enhanced_pkg.core import AIEngineConfig, AIEnhancedClient
from ai_enhanced_pkg.exceptions import ConfigurationError


def test_config_defaults():
    config = AIEngineConfig()
    assert config.model_name == "gpt-4o-mini"
    assert config.temperature == 0.7
    assert config.max_tokens == 1024
    assert config.enable_caching is True


def test_config_validation_invalid_temperature():
    config = AIEngineConfig(temperature=2.5)
    with pytest.raises(ConfigurationError) as exc_info:
        config.validate()
    assert "temperature" in str(exc_info.value)


def test_config_validation_empty_model():
    config = AIEngineConfig(model_name="   ")
    with pytest.raises(ConfigurationError):
        config.validate()


def test_config_validation_negative_max_tokens():
    config = AIEngineConfig(max_tokens=-10)
    with pytest.raises(ConfigurationError):
        config.validate()


def test_client_interaction_recording(mock_client):
    assert mock_client.total_tokens == 0
    assert len(mock_client.history) == 0

    entry = mock_client.record_interaction(
        prompt="Explain recursion",
        response_text="Recursion is when a function calls itself.",
        latency_ms=120.5,
        cached=False,
    )

    assert entry["cached"] is False
    assert mock_client.total_tokens > 0
    assert len(mock_client.history) == 1

    # Cached entry should not increment token tally
    current_tokens = mock_client.total_tokens
    mock_client.record_interaction(
        prompt="Explain recursion",
        response_text="Recursion is when a function calls itself.",
        latency_ms=1.0,
        cached=True,
    )
    assert mock_client.total_tokens == current_tokens
    assert len(mock_client.history) == 2


def test_client_reset_history(mock_client):
    mock_client.record_interaction("Prompt", "Response", 50.0)
    assert len(mock_client.history) == 1
    mock_client.reset_history()
    assert len(mock_client.history) == 0
    assert mock_client.total_tokens == 0
