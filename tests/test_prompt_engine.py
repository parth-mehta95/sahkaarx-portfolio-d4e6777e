"""
Unit tests for PromptTemplate, PromptEngine execution, streaming, and batching.
Verifies behaviors introduced by both feature branches.
"""

import pytest
from ai_enhanced_pkg.exceptions import PromptValidationError
from ai_enhanced_pkg.prompt_engine import PromptEngine, PromptTemplate


def test_template_rendering_success(sample_template):
    rendered = sample_template.render(role="junior developer", code="print('hello')")
    assert "junior developer" in rendered
    assert "print('hello')" in rendered


def test_template_missing_variable_raises(sample_template):
    with pytest.raises(PromptValidationError) as exc_info:
        sample_template.render(role="junior developer")
    assert "code" in exc_info.value.missing_keys


def test_single_prompt_execution(prompt_engine, sample_template):
    response = prompt_engine.execute_prompt(
        sample_template,
        variables={"role": "data scientist", "code": "import numpy as np"},
    )
    assert response.is_cached is False
    assert response.tokens_used > 0
    assert response.latency_ms >= 0.0
    assert "expert code reviewer" in response.text


def test_caching_behavior_and_hit_rate(prompt_engine, sample_template):
    vars_dict = {"role": "senior architect", "code": "class SystemArchitecture: pass"}

    # First call -> cache miss
    res1 = prompt_engine.execute_prompt(sample_template, vars_dict)
    assert res1.is_cached is False
    assert prompt_engine.cache_stats["hits"] == 0
    assert prompt_engine.cache_stats["misses"] == 1

    # Second call -> cache hit
    res2 = prompt_engine.execute_prompt(sample_template, vars_dict)
    assert res2.is_cached is True
    assert prompt_engine.cache_stats["hits"] == 1
    assert prompt_engine.cache_stats["hit_rate_pct"] == 50.0


def test_streaming_feature_branch_behavior(prompt_engine, sample_template):
    """Verifies functionality contributed by feature/streaming-response branch."""
    vars_dict = {"role": "qa engineer", "code": "assert True"}
    stream_gen = prompt_engine.stream_prompt(sample_template, vars_dict, chunk_size=10)

    chunks = []
    for chunk in stream_gen:
        assert isinstance(chunk, str)
        chunks.append(chunk)

    full_reconstructed = "".join(chunks)
    assert len(chunks) > 1
    assert "qa engineer" in full_reconstructed or "reviewer" in full_reconstructed


def test_batch_feature_branch_behavior(prompt_engine, sample_template):
    """Verifies functionality contributed by feature/batch-optimization branch."""
    batch_inputs = [
        {"role": "intern", "code": "x = 1"},
        {"role": "staff engineer", "code": "def optimize(): pass"},
        {"role": "intern", "code": "x = 1"},  # duplicate to hit cache
    ]

    results = prompt_engine.execute_batch(sample_template, batch_inputs)
    assert len(results) == 3
    assert results[0].is_cached is False
    assert results[1].is_cached is False
    assert results[2].is_cached is True
    assert prompt_engine.cache_stats["hits"] >= 1
