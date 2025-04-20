from unittest.mock import patch, MagicMock
import pytest
from .log_analyzer import process_logs

@pytest.fixture
def mock_read_log_file():
    with patch('log_analyzer.log_analyzer.read_log_file') as mock:
        yield mock

@pytest.fixture
def mock_parse_log_line():
    with patch('log_analyzer.log_analyzer.parse_log_line') as mock:
        yield mock

@pytest.fixture
def mock_log_results_decorator():
    with patch('log_analyzer.log_analyzer.log_results_decorator', lambda x: x):
        yield

def test_process_logs_success(mock_read_log_file, mock_parse_log_line, mock_log_results_decorator):
    # Mock the behavior of read_log_file
    mock_read_log_file.return_value = ["log line 1", "log line 2"]

    # Mock the behavior of parse_log_line
    mock_parse_log_line.side_effect = [{"key": "value1"}, {"key": "value2"}]

    # Call the function
    result = process_logs("dummy_path")

    # Assertions
    assert len(result) == 2
    assert all(isinstance(item, dict) for item in result)
    mock_read_log_file.assert_called_once_with("dummy_path")
    assert mock_parse_log_line.call_count == 2

def test_process_logs_partial_failure(mock_read_log_file, mock_parse_log_line, mock_log_results_decorator):
    # Mock the behavior of read_log_file
    mock_read_log_file.return_value = ["log line 1", "log line 2"]

    # Mock the behavior of parse_log_line
    mock_parse_log_line.side_effect = [{"key": "value1"}, None]

    # Call the function
    result = process_logs("dummy_path")

    # Assertions
    assert len(result) == 2
    assert isinstance(result[0], dict)
    assert result[1] is None
    mock_read_log_file.assert_called_once_with("dummy_path")
    assert mock_parse_log_line.call_count == 2

def test_process_logs_empty_file(mock_read_log_file, mock_parse_log_line, mock_log_results_decorator):
    # Mock the behavior of read_log_file
    mock_read_log_file.return_value = []

    # Call the function
    result = process_logs("dummy_path")

    # Assertions
    assert result == []
    mock_read_log_file.assert_called_once_with("dummy_path")
    mock_parse_log_line.assert_not_called()