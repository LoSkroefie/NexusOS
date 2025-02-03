#!/usr/bin/env python3
"""
NexusOS - AI-Powered Operating System
Main entry point for the NexusOS system.
"""

import sys
import os

# Add src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from nexus_terminal.terminal_gui import main as terminal_main

def setup_logging():
    """Configure system-wide logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='nexus.log'
    )

def check_dependencies():
    """Verify all required dependencies are installed."""
    try:
        import PyQt6
        import psutil
        import pyttsx3
        import requests
        return True
    except ImportError as e:
        print(f"Missing dependency: {str(e)}")
        print("Please install all required dependencies using:")
        print("pip install -r requirements.txt")
        return False

def main():
    """Main entry point for NexusOS."""
    # Setup logging
    setup_logging()
    logger = logging.getLogger('NexusOS')
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    try:
        # Start the NexusOS Terminal
        terminal_main()
    except Exception as e:
        logger.error(f"Error starting NexusOS: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
