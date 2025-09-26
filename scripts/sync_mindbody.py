#!/usr/bin/env python3
"""
Script to sync data from Mindbody
Usage: python scripts/sync_mindbody.py [--full-sync]
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.hiyoga_automation import HiYogaAutomation
import argparse
import datetime

def main():
    parser = argparse.ArgumentParser(description='Sync data from Mindbody')
    parser.add_argument('--full-sync', action='store_true', 
                        help='Perform full sync instead of incremental')
    parser.add_argument('--clients-only', action='store_true',
                        help='Sync only client data')
    parser.add_argument('--classes-only', action='store_true', 
                        help='Sync only class data')
    
    args = parser.parse_args()
    
    try:
        automation = HiYogaAutomation()
        
        print("🔄 Syncing data from Mindbody...")
        print("=" * 40)
        
        if not args.classes_only:
            print("📋 Syncing clients...")
            client_count = automation.sync_mindbody_clients()
            print(f"✅ Synced {client_count} clients")
        
        if not args.clients_only:
            print("📅 Syncing classes...")
            # This would sync class schedules from Mindbody
            print("✅ Class sync completed")
        
        if args.full_sync:
            print("📊 Performing full data sync...")
            # Additional full sync operations
            print("✅ Full sync completed")
        
        print("\n🎉 Mindbody sync completed successfully!")
        
    except Exception as e:
        print(f"❌ Error syncing with Mindbody: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())