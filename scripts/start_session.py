#!/usr/bin/env python3
"""
Script to start a studio session
Usage: python scripts/start_session.py [template_name] [duration_minutes]
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.studio_automation import StudioAutomation
import argparse

def main():
    parser = argparse.ArgumentParser(description='Start a studio recording session')
    parser.add_argument('template', help='Session template name (yoga_class, meditation, workshop)')
    parser.add_argument('--duration', type=int, help='Custom session duration in minutes')
    parser.add_argument('--config', default='config/studio_config.yaml', help='Path to configuration file')
    
    args = parser.parse_args()
    
    try:
        studio = StudioAutomation(args.config)
        
        # Check if template exists
        templates = [t['name'] for t in studio.get_session_templates()]
        if args.template not in templates:
            print(f"Error: Template '{args.template}' not found.")
            print(f"Available templates: {', '.join(templates)}")
            return 1
        
        # Start the session
        success = studio.start_session(args.template, args.duration)
        if success:
            print(f"Session started successfully with template: {args.template}")
            if args.duration:
                print(f"Custom duration: {args.duration} minutes")
            print("Use 'python scripts/stop_session.py' to stop the session")
        else:
            print("Failed to start session")
            return 1
            
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())