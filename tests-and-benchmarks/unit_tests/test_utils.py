import pytest
from unittest.mock import MagicMock
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.ui.utils import extract_text_from_upload

def test_extract_text_from_txt():
    """Test extracting text from a simple text file."""
    # Create a mock Streamlit UploadedFile object
    mock_file = MagicMock()
    mock_file.name = "contract.txt"
    mock_file.getvalue.return_value = b"This is a test contract clause."
    
    result = extract_text_from_upload(mock_file)
    assert result == "This is a test contract clause.", "Failed to read standard text file."

def test_extract_text_empty_file():
    """Test that an empty file returns an empty string without crashing."""
    mock_file = MagicMock()
    mock_file.name = "empty.txt"
    mock_file.getvalue.return_value = b""
    
    result = extract_text_from_upload(mock_file)
    assert result == "", "Empty file should return an empty string."
