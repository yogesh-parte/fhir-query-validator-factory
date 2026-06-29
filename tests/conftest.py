"""Shared pytest fixtures."""

import pytest


@pytest.fixture(autouse=True)
def reset_workflow_singletons():
    """Isolate module-level workflow singletons between tests."""
    from src.agentic_layer.graph import workflow_engine

    workflow_engine.cache_agent._cache.clear()
    workflow_engine.validator._pattern_history.clear()
    workflow_engine.human_gate._paused_users.clear()
    workflow_engine.human_gate._pending_reviews.clear()
    yield