import pytest
import sys
from pathlib import Path
from unittest.mock import patch

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.retrieval.hybrid_search import hybrid_search

@patch("src.retrieval.hybrid_search.load_and_chunk")
def test_hybrid_search_fallback_when_db_missing(mock_load):
    """Test that the system falls back gracefully when ChromaDB is unavailable."""
    # Force the data loader to raise an Exception (simulating DB failure)
    mock_load.side_effect = Exception("ChromaDB not found")
    
    results = hybrid_search("data breach")
    
    assert len(results) == 1, "Should return exactly one fallback result"
    assert "offline-fallback" in results[0]["source"], "Should mark source as fallback"
    assert results[0]["score"] == 0.0, "Fallback score should be 0.0"

def test_hybrid_search_structure():
    """Test that the hybrid search returns the correct dictionary structure."""
    results = hybrid_search("liability cap", top_k=2)
    
    assert isinstance(results, list), "Search must return a list"
    
    if len(results) > 0:
        first_result = results[0]
        assert "text" in first_result, "Result missing 'text' key"
        assert "score" in first_result, "Result missing 'score' key"
        assert "source" in first_result, "Result missing 'source' key"
