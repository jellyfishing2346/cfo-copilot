#!/usr/bin/env python3
"""
🤗 Hugging Face Spaces Entry Point for CFO Copilot
AI-Powered Financial Analysis Assistant

This file serves as the entry point for Hugging Face Spaces deployment.
It imports and runs the main Streamlit application.
"""

import sys
import os

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import and run the main application
if __name__ == "__main__":
    # Import the main app module
    import app
    
    # The app will be automatically served by Hugging Face Spaces
    # when this file is executed
