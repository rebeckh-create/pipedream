#!/usr/bin/env python3
"""
Script to add a new client to the studio
Usage: python scripts/add_client.py
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.studio_admin import StudioAdmin
import argparse

def main():
    parser = argparse.ArgumentParser(description='Add a new client to the studio')
    parser.add_argument('--first-name', required=True, help='Client first name')
    parser.add_argument('--last-name', required=True, help='Client last name')
    parser.add_argument('--email', required=True, help='Client email address')
    parser.add_argument('--phone', help='Client phone number')
    parser.add_argument('--membership-type', default='drop-in', 
                        choices=['drop-in', 'monthly', 'annual', 'unlimited'],
                        help='Membership type')
    parser.add_argument('--emergency-contact', help='Emergency contact information')
    
    args = parser.parse_args()
    
    try:
        admin = StudioAdmin()
        
        client_data = {
            'first_name': args.first_name,
            'last_name': args.last_name,
            'email': args.email,
            'phone': args.phone or '',
            'membership_type': args.membership_type,
            'emergency_contact': args.emergency_contact or ''
        }
        
        client_id = admin.add_client(client_data)
        print(f"✅ Client added successfully!")
        print(f"   Name: {args.first_name} {args.last_name}")
        print(f"   Email: {args.email}")
        print(f"   ID: {client_id}")
        print(f"   Membership: {args.membership_type}")
        
    except Exception as e:
        print(f"❌ Error adding client: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())