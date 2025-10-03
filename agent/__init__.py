"""
CFO Copilot Agent Package

This package contains the AI agent components for financial analysis:
- planner.py: Natural language query planning and intent classification
- tools.py: Financial analysis tools and data processing
"""

__version__ = "1.0.0"
__author__ = "CFO Copilot Team"

# Make key components easily importable
from .planner import get_planner
from .tools import get_analyzer

__all__ = ['get_planner', 'get_analyzer']
