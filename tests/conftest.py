#!/usr/bin/env python

import sys
import yaml
import time
import pytest
import random
import psutil
from pathlib import Path
from unittest.mock import MagicMock

sys.path.append(str(Path(__file__).resolve().parent.parent))
from logger import logger_main

logger = logger_main.get_logger(__name__)

def get_cfg_file():
    """Find the first configuration file in the 'configs' directory, read it, and return its contents."""
    cfg_files = list(Path(__file__).resolve().parent.parent.glob('configs/*.yml'))
    if not cfg_files:
        logger.warning("No configuration file found in 'configs/' directory.")
        raise FileNotFoundError("No configuration file found in 'configs/' directory.")
    
    config_path = cfg_files[0]
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config

def generate_random_create_time():
    """Generate a random timestamp for the last 30 days."""
    current_time = time.time()
    random_past_time = current_time - random.randint(0, 30 * 24 * 60 * 60)  # Random time in the last 30 days
    return random_past_time


@pytest.fixture(scope="session")
def process_name_feeder():
    """Fixture to feed ps apps names from process_names.yml"""
    if "apps" not in get_cfg_file():
        raise KeyError("Key 'processes' not found in the configuration file.")
    return get_cfg_file()["apps"]

@pytest.fixture
def mock_process_iter(process_name_feeder):
    """Fixture to mock psutil.process_iter with realistic data."""
    mock_processes = []
    for name in process_name_feeder:
        mock_proc = MagicMock()
        mock_proc.info = {
            "name": name,
            "pid": random.randint(1000, 9999),
            "create_time": time.time() - random.randint(0, 10000),
        }
        mock_processes.append(mock_proc)
    return mock_processes

@pytest.fixture
def mock_psutil_process():
    """Fixture to mock psutil.Process with randomized CPU and memory usage."""
    mock_process = MagicMock()
    mock_process.cpu_percent.return_value = random.uniform(0.0, 100.0)  # Random CPU percentage
    mock_process.memory_info.return_value = MagicMock(
        rss=random.randint(50 * 1024 * 1024, 500 * 1024 * 1024)  # Random RSS between 50 MB and 500 MB
    )
    return mock_process


@pytest.fixture
def mock_disk_usage():
    """Fixture to mock psutil.disk_usage with randomized data."""
    mock_disk = MagicMock()
    mock_disk.percent = random.uniform(0.0, 100.0)  # Random disk usage percentage
    return mock_disk

@pytest.fixture(params=get_cfg_file().get("apps", []), ids=lambda app: f"App: {app}")
def tag_id(request):
    """Fixture to parameterize tests with app names."""
    return request.param


###################### debug help ############################
def test_empty_config_handling(monkeypatch):
    def mock_get_cfg_file_empty():
        return {}
    monkeypatch.setattr("conftest.get_cfg_file", mock_get_cfg_file_empty)
    with pytest.raises(KeyError, match="Key 'apps' not found"):
        _ = process_name_feeder()

def debug_running_processes():
    for proc in psutil.process_iter(attrs=['name', 'pid']):
        try:
            print(f"Process Name: {proc.info['name']}, PID: {proc.info['pid']}")
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass


if __name__ == "__main__":
    pass
    # test_empty_config_handling(monkeypatch)
    # print(get_cfg_file())
    # print(process_name_feeder())
    # print(type(get_cfg_file()), f'actual --> {get_cfg_file()}')
    # debug_running_processes()
