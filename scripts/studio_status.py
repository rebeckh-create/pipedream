#!/usr/bin/env python3
"""
Script to check studio status and list recordings
Usage: python scripts/studio_status.py
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.studio_automation import StudioAutomation
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description='Check studio status and list recordings')
    parser.add_argument('--config', default='config/studio_config.yaml', help='Path to configuration file')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')
    
    args = parser.parse_args()
    
    try:
        studio = StudioAutomation(args.config)
        
        # Get status
        status = studio.get_status()
        recordings = studio.list_recordings()
        
        if args.json:
            output = {
                'status': status,
                'recordings': recordings
            }
            print(json.dumps(output, indent=2, default=str))
        else:
            print(f"Studio: {status['studio_name']}")
            print(f"Session Active: {status['session_active']}")
            
            if status['current_session']:
                session = status['current_session']
                print(f"Current Session: {session['id']}")
                print(f"Template: {session['template']}")
                print(f"Duration: {session['duration']} minutes")
                print(f"Started: {session['start_time']}")
            
            print(f"\nEquipment Status:")
            for equipment, connected in status['equipment_connected'].items():
                status_str = "Connected" if connected else "Disconnected"
                print(f"- {equipment.replace('_', ' ').title()}: {status_str}")
            
            print(f"\nRecent Recordings ({len(recordings)}):")
            for recording in recordings[:5]:  # Show last 5
                print(f"- {recording['name']} ({recording['size']} bytes) - {recording['modified']}")
            
            if len(recordings) > 5:
                print(f"... and {len(recordings) - 5} more")
            
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())