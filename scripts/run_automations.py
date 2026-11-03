#!/usr/bin/env python3
"""
Script to run HiYoga automation tasks
Usage: python scripts/run_automations.py [--daily|--hourly|--test]
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.hiyoga_automation import HiYogaAutomation
import argparse
import datetime

def main():
    parser = argparse.ArgumentParser(description='Run HiYoga automation tasks')
    parser.add_argument('--daily', action='store_true', help='Run daily automations')
    parser.add_argument('--hourly', action='store_true', help='Run hourly automations')
    parser.add_argument('--test', action='store_true', help='Run test automations')
    parser.add_argument('--trigger', help='Trigger specific automation (welcome, reminder, etc.)')
    parser.add_argument('--client-id', help='Client ID for specific automation')
    
    args = parser.parse_args()
    
    try:
        automation = HiYogaAutomation()
        
        print("🤖 HiYoga Automation Runner")
        print("=" * 30)
        print(f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        if args.daily:
            print("📅 Running daily automations...")
            automation.run_daily_automations()
            print("✅ Daily automations completed")
            
        elif args.hourly:
            print("⏰ Running hourly automations...")
            # Sync with Mindbody
            client_count = automation.sync_mindbody_clients()
            print(f"✅ Synced {client_count} clients from Mindbody")
            
        elif args.test:
            print("🧪 Running test automations...")
            # Create a test client
            test_client_data = {
                'first_name': 'Test',
                'last_name': 'User',
                'email': 'test@example.com',
                'phone': '+64 21 123 4567',
                'membership_type': 'drop-in'
            }
            
            client_id = automation._add_client(test_client_data)
            print(f"✅ Created test client: {client_id}")
            print("✅ Welcome automation triggered")
            
        elif args.trigger and args.client_id:
            print(f"🎯 Triggering {args.trigger} for client {args.client_id}")
            automation._trigger_automation(args.trigger, args.client_id)
            print("✅ Automation triggered")
            
        else:
            # Default: show status
            report = automation.get_automation_report(7)
            engagement = automation.get_client_engagement_report()
            
            print("📊 Automation Status (Last 7 Days)")
            print("-" * 35)
            print(f"Total automations run: {report['total_automations']}")
            print(f"New clients added: {report['new_clients']}")
            print(f"Total clients: {engagement['total_clients']}")
            print()
            
            print("📈 Automation Stats:")
            for stat in report['automation_stats']:
                print(f"  {stat['action_type']}: {stat['count']} ({stat['status']})")
            
        print("\n🎉 Automation run completed!")
        
    except Exception as e:
        print(f"❌ Error running automations: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())