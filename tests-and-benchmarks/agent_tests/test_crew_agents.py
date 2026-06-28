import pytest
import sys
from pathlib import Path
from unittest.mock import patch

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.agents.crew import run_compliance_check, _fallback_result

def test_fallback_result_violation():
    """Test the deterministic fallback logic catches basic keyword violations."""
    clause = "The vendor's liability is capped at 100 dollars."
    result = _fallback_result(clause, ["DPDP Act"], [])
    
    assert result["score"] == 70, "Liability cap should trigger a higher risk score"
    assert result["clauses"][0]["status"] == "Violation", "Should be flagged as a violation"

def test_fallback_result_compliant():
    """Test the deterministic fallback logic for a compliant-looking clause."""
    clause = "We will maintain the highest standards of security."
    result = _fallback_result(clause, ["DPDP Act"], [])
    
    assert result["score"] == 55, "Should have a moderate review score"
    assert result["clauses"][0]["status"] == "Review", "Should be flagged for review, not strict violation"

@patch("src.agents.crew.Crew")
@patch("src.agents.crew.get_llm")
def test_crew_pipeline_execution(mock_get_llm, mock_crew_class):
    """
    Test that the CrewAI pipeline assembles correctly and returns the expected structure.
    This mocks out the actual LLM calls to save money/time.
    """
    # Mock the LLM to just be an object, bypass actual API call
    mock_get_llm.return_value = "Mocked_LLM"
    
    # Mock the Crew execution
    mock_crew_instance = mock_crew_class.return_value
    mock_crew_instance.kickoff.return_value = "Mocked Final Report"
    
    result = run_compliance_check("Test clause", ["Test Regulation"])
    
    # Check if it returned a dictionary with our expected keys
    assert "score" in result
    assert "clauses" in result
    assert "email_draft" in result
    assert "context" in result
