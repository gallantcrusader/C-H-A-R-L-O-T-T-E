# core/__init__.py
# Initializes the core CHARLOTTE module
__version__ = "0.1.0"
import os
import sys

# ******************************************************************************************
# Utility Setup
# Ensure root project path is in sys.path for relative imports
# ******************************************************************************************
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

