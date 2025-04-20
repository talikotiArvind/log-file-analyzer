import pytest
from unittest.mock import patch, MagicMock
from src.log_analyzer import process_logs

@patch('src.log_analyzer.read_log_file')
@patch('src.log_analyzer.parse_log_line')
def test_process_logs_all_successful(mock_parse_log_line, mock_read_log_file):
    # Mock the log file lines
    mock_read_log_file.return_value = ["log line 1", "log line 2"]
    # Mock the parse_log_line function to return dictionaries
    mock_parse_log_line.side_effect = [{"key": "value1"}, {"key": "value2"}]

    # Call the function
    results = process_logs("dummy_path")

    # Assertions
    assert len(results) == 2
    assert all(isinstance(result, dict) for result in results)
    mock_read_log_file.assert_called_once_with("dummy_path")
    assert mock_parse_log_line.call_count == 2

@patch('src.log_analyzer.read_log_file')
@patch('src.log_analyzer.parse_log_line')
def test_process_logs_some_failures(mock_parse_log_line, mock_read_log_file):
    # Mock the log file lines
    mock_read_log_file.return_value = ["log line 1", "log line 2"]
    # Mock the parse_log_line function to return mixed results
    mock_parse_log_line.side_effect = [{"key": "value1"}, "error"]

    # Call the function
    results = process_logs("dummy_path")

    # Assertions
    assert len(results) == 2
    assert isinstance(results[0], dict)
    assert results[1] == "error"
    mock_read_log_file.assert_called_once_with("dummy_path")
    assert mock_parse_log_line.call_count == 2