import pytest
from src.agentic_layer.agents.cache_agent import CacheAgent


def test_cache_hit_and_miss():
    agent = CacheAgent(ttl_seconds=10)
    
    # First call should fetch
    result1 = agent.get_capability_statement("hapi")
    assert result1["resourceType"] == "CapabilityStatement"
    
    # Second call should hit cache
    result2 = agent.get_capability_statement("hapi")
    assert result2 == result1
