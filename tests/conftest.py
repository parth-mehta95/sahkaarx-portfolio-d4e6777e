"""
Pytest configuration and reusable fixtures.
"""

import pytest
from ai_enhanced_pkg.core import AIEngineConfig, AIEnhancedClient
from ai_enhanced_pkg.prompt_engine import PromptEngine, PromptTemplate


@pytest.fixture
def default_config() -> AIEngineConfig:
    return AIEngineConfig(
        model_name="gpt-4o-mini",
        temperature=0.5,
        max_tokens=500,
        enable_caching=True,
    )


@pytest.fixture
def mock_client(default_config) -> AIEnhancedClient:
    return AIEnhancedClient(config=default_config)


@pytest.fixture
def prompt_engine(mock_client) -> PromptEngine:
    return PromptEngine(client=mock_client)


@pytest.fixture
def sample_template() -> PromptTemplate:
    return PromptTemplate(
        template="Summarize the following code snippet for a {role}: {code}",
        system_role="expert code reviewer",
    )
