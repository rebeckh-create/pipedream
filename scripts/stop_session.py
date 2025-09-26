#!/usr/bin/env python3
"""
Script to stop the current studio session
Usage: python scripts/stop_session.py
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.studio_automation import StudioAutomation
import argparse

def main():
    parser = argparse.ArgumentParser(description='Stop the current studio recording session')
    parser.add_argument('--config', default='config/studio_config.yaml', help='Path to configuration file')
    
    args = parser.parse_args()
    
    try:
        studio = StudioAutomation(args.config)
        
        # Check if there's an active session
        status = studio.get_status()
        if not status['session_active']:
            print("No active session to stop")
            return 0
            
        # Stop the session
        success = studio.stop_session()
        if success:
            print("Session stopped successfully")
        else:
            print("Failed to stop session")
            return 1
            
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())