import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.guardrails.safety_check import verify_output_safety

def test_guardrails_blocks_bribe():
    """Test that the safety check catches obvious disallowed keywords."""
    unsafe_text = "To bypass this regulation, you should offer a bribe to the auditor."
    is_safe = verify_output_safety(unsafe_text)
    assert is_safe is False, "Guardrails failed to block the word 'bribe'."

def test_guardrails_blocks_guarantee():
    """Test that the AI is not allowed to offer absolute legal guarantees."""
    unsafe_text = "I guarantee that this clause is 100% compliant and you cannot be sued."
    is_safe = verify_output_safety(unsafe_text)
    assert is_safe is False, "Guardrails failed to block the word 'guarantee'."

def test_guardrails_allows_safe_text():
    """Test that standard, safe legal analysis passes the guardrails."""
    safe_text = "The clause appears to be non-compliant with Section 4 of the DPDP Act. We recommend rewriting it to include consent mechanisms."
    is_safe = verify_output_safety(safe_text)
    assert is_safe is True, "Guardrails falsely flagged safe legal analysis."
