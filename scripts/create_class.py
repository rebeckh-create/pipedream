#!/usr/bin/env python3
"""
Script to create a new class session
Usage: python scripts/create_class.py --name "Morning Yoga" --instructor "Sarah" --date 2025-09-26 --time 09:00
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.studio_admin import StudioAdmin
import argparse

def main():
    parser = argparse.ArgumentParser(description='Create a new class session')
    parser.add_argument('--name', required=True, help='Class name')
    parser.add_argument('--instructor', required=True, help='Instructor name')
    parser.add_argument('--date', required=True, help='Class date (YYYY-MM-DD)')
    parser.add_argument('--time', required=True, help='Class time (HH:MM)')
    parser.add_argument('--duration', type=int, default=60, help='Class duration in minutes')
    parser.add_argument('--capacity', type=int, default=20, help='Maximum capacity')
    parser.add_argument('--room', default='Main Studio', help='Room/location')
    parser.add_argument('--type', default='yoga', help='Class type')
    parser.add_argument('--price', type=float, default=20.0, help='Class price')
    
    args = parser.parse_args()
    
    try:
        admin = StudioAdmin()
        
        class_data = {
            'name': args.name,
            'instructor': args.instructor,
            'date': args.date,
            'time': args.time,
            'duration': args.duration,
            'capacity': args.capacity,
            'room': args.room,
            'class_type': args.type,
            'price': args.price
        }
        
        class_id = admin.create_class(class_data)
        print(f"✅ Class created successfully!")
        print(f"   Class: {args.name}")
        print(f"   Instructor: {args.instructor}")
        print(f"   Date/Time: {args.date} at {args.time}")
        print(f"   Duration: {args.duration} minutes")
        print(f"   Capacity: {args.capacity} students")
        print(f"   Price: ${args.price}")
        print(f"   ID: {class_id}")
        
    except Exception as e:
        print(f"❌ Error creating class: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())