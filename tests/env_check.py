#!/usr/bin/env python

import sys
import platform
import subprocess
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from logger import logger_main
logger = logger_main.get_logger(__name__)

def check_python_and_pip():
    try:
        # ... get Python path:
        logger.info(f"Python Path: {sys.executable}")
        
        # ... get Python version
        logger.info(f"Python Version: {platform.python_version()}")
        pip_version = subprocess.check_output([sys.executable, "-m", "pip", "--version"], text=True).strip()
        logger.info(f"Pip Version: {pip_version}")
        
        # ... check if pip is installed:
        if not pip_version:
            logger.error("Error: pip is not installed.")
        else:
            logger.info("pip is installed and functional.")
            
    except FileNotFoundError:
        logger.error("Error: Python or pip could not be found.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    check_python_and_pip()