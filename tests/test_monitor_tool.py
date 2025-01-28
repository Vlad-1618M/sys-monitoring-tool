#!/usr/bin/env python

import sys
import pytest
from pathlib import Path
from unittest.mock import patch

sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.get_process_momitor import(
    get_running_processes_by_name,
    measure_cpu_usage,
    measure_memory_usage,
    measure_disk_usage,
    ProcessNotFoundError,
)

@patch("psutil.process_iter")
def test_get_running_processes_by_name(mock_process_iter_func, mock_process_iter, tag_id):
    """Test fetching processes by name with randomized PIDs and create times."""
    mock_process_iter_func.return_value = mock_process_iter
    result = get_running_processes_by_name(tag_id)

    if not result:
        pytest.skip(f"Skipping test: {tag_id} process not found.")

    assert len(result) > 0, f"No processes were returned for {tag_id}."
    assert result[0][0].lower() == tag_id.lower(), (
        f"Expected process name {tag_id}, got {result[0][0]}"
    )
    assert isinstance(result[0][1], int), "PID is not an integer."
    assert isinstance(result[0][2], str), "Create time is not a formatted string."


@patch("psutil.process_iter")
@patch("psutil.Process")
def test_measure_cpu_usage(mock_psutil_process_func, mock_process_iter_func, mock_psutil_process, mock_process_iter, tag_id):
    """Test CPU usage for all apps in the config."""
    mock_process_iter_func.return_value = mock_process_iter
    mock_psutil_process_func.return_value = mock_psutil_process

    result = measure_cpu_usage(tag_id)
    if result is None:
        pytest.skip(f"Skipping test: {tag_id} process not found.")
    assert 0.0 <= result <= 100.0, f"CPU usage for {tag_id} should be between 0 and 100, got {result}."


@patch("psutil.process_iter")
@patch("psutil.Process")
def test_measure_memory_usage(mock_psutil_process_func, mock_process_iter_func, mock_psutil_process, mock_process_iter, tag_id):
    """Test memory usage for all apps in the config."""
    mock_process_iter_func.return_value = mock_process_iter
    mock_psutil_process_func.return_value = mock_psutil_process

    result = measure_memory_usage(tag_id)
    if result is None:
        pytest.skip(f"Skipping test: {tag_id} process not found.")
    assert result > 0, f"Memory usage for {tag_id} should be greater than 0, got {result}."


@patch("psutil.disk_usage")
def test_measure_disk_usage(mock_disk_usage_func, mock_disk_usage):
    """Test disk usage."""
    mock_disk_usage_func.return_value = mock_disk_usage

    result = measure_disk_usage()
    assert result is not None, "Disk usage should not be None."
    assert 0.0 <= result <= 100.0, f"Disk usage should be between 0 and 100, got {result}."


################ REAL TEST No FAKE Stuff :0)) #############

def test_real_running_processes(tag_id):
    """Test to verify if the real process is running on the system using the existing module."""
    try:
        result = get_running_processes_by_name(tag_id)
        assert result, f"Process '{tag_id}' is not currently running on the system."
        
        for process in result:
            name, pid, runtime = process
            assert isinstance(name, str), "Process name should be a string."
            assert isinstance(pid, int), "PID should be an integer."
            assert isinstance(runtime, str), "Runtime should be a formatted string."

    except ProcessNotFoundError as e:
        pytest.fail(f"{e.name} process not found: {e}")

