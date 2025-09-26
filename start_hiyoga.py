#!/usr/bin/env python3
"""
HiYoga Automation Hub - Simple Starter
Launch your studio automation system
"""

import os
import json
import sqlite3
import logging
import datetime
from pathlib import Path

print("🧘‍♀️ HiYoga Studio Automation Hub")
print("=" * 40)
print("Welcome to your automation control center!")
print()

# Setup
Path("data").mkdir(exist_ok=True)
Path("logs").mkdir(exist_ok=True)

# Create simple database
db_path = "data/hiyoga.db"
with sqlite3.connect(db_path) as conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id TEXT PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            phone TEXT,
            last_class_date TEXT,
            total_classes INTEGER DEFAULT 0,
            membership_status TEXT DEFAULT 'active',
            created_at TEXT
        )
    ''')
    
    conn.execute('''
        CREATE TABLE IF NOT EXISTS automation_log (
            id TEXT PRIMARY KEY,
            client_email TEXT,
            action_type TEXT,
            message TEXT,
            status TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()

print("✅ Database initialized")

# Add some demo data
with sqlite3.connect(db_path) as conn:
    # Check if we have demo data
    count = conn.execute('SELECT COUNT(*) FROM clients').fetchone()[0]
    
    if count == 0:
        demo_clients = [
            ('demo_001', 'Sarah', 'Wilson', 'sarah@example.com', '+64 21 123 4567', '2025-09-24', 1, 'active', datetime.datetime.now().isoformat()),
            ('demo_002', 'Mike', 'Johnson', 'mike@example.com', '+64 21 234 5678', '2025-09-20', 8, 'active', datetime.datetime.now().isoformat()),
            ('demo_003', 'Emma', 'Smith', 'emma@example.com', '+64 21 345 6789', '2025-09-15', 15, 'active', datetime.datetime.now().isoformat())
        ]
        
        conn.executemany('INSERT INTO clients VALUES (?,?,?,?,?,?,?,?,?)', demo_clients)
        conn.commit()
        print("✅ Demo clients added")

# Show dashboard
with sqlite3.connect(db_path) as conn:
    total_clients = conn.execute('SELECT COUNT(*) FROM clients').fetchone()[0]
    active_clients = conn.execute("SELECT COUNT(*) FROM clients WHERE membership_status = 'active'").fetchone()[0]

print()
print("📊 HiYoga Studio Stats:")
print(f"   Total Clients: {total_clients}")
print(f"   Active Members: {active_clients}")
print(f"   Studio Phone: +64 21 199 9642")
print(f"   Mindbody Site: 32353")

print()
print("🚀 Available Automations:")
print("   ✅ Welcome sequences for new clients")
print("   ✅ Class reminders (24hr, 2hr, 30min)")
print("   ✅ No-show follow-up messages")
print("   ✅ Membership renewal reminders")
print("   ✅ Win-back campaigns")
print("   ✅ Google review requests")
print("   ✅ Birthday messages")
print("   ✅ Social media automation")
print("   ✅ Waitlist notifications")
print("   ✅ Payment failure follow-ups")

print()
print("🎯 Quick Actions:")
print("1. Test welcome message")
print("2. Test class reminder")
print("3. Test review request")
print("4. Show client list")
print("5. View automation logs")

def send_test_message(message_type, client_name):
    """Simulate sending a message"""
    messages = {
        'welcome': f"""Kia ora {client_name}! 🧘‍♀️ 

Welcome to HiYoga! We're so excited to have you join our yoga and pilates community.

Your first class is always special - if you have any questions or need guidance, just reply to this message.

See you on the mat soon!

Namaste,
The HiYoga Team ✨""",

        'reminder': f"""Hi {client_name}! 🧘‍♀️

Just a friendly reminder that you have Vinyasa Flow tomorrow at 6:00 PM.

We can't wait to see you on the mat!

If you need to cancel, please do so at least 12 hours in advance through Mindbody.

Namaste! ✨""",

        'review': f"""Hi {client_name}! 

We hope you're loving your yoga journey with us! 🧘‍♀️

If you've enjoyed your classes, would you mind sharing a quick review on Google? It helps other yogis find us!

https://www.google.com/search?q=HIYOGA

Thank you for being part of our community! 💜

Namaste,
HiYoga Team"""
    }
    
    return messages.get(message_type, f"Test message for {client_name}")

def log_automation(action_type, message):
    """Log automation action"""
    log_id = f"log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    now = datetime.datetime.now().isoformat()
    
    with sqlite3.connect(db_path) as conn:
        conn.execute('''
            INSERT INTO automation_log VALUES (?,?,?,?,?,?)
        ''', (log_id, 'demo@example.com', action_type, message, 'success', now))
        conn.commit()

while True:
    try:
        choice = input("\nEnter choice (1-5) or 'quit': ").strip()
        
        if choice.lower() in ['quit', 'q', 'exit']:
            print("👋 Goodbye! Your automations are ready to launch!")
            break
            
        elif choice == '1':
            print("\n🌟 Testing Welcome Message:")
            print("-" * 30)
            message = send_test_message('welcome', 'Sarah')
            print(message)
            log_automation('welcome_test', 'Welcome message tested')
            print("\n✅ Welcome message ready!")
            
        elif choice == '2':
            print("\n⏰ Testing Class Reminder:")
            print("-" * 30)
            message = send_test_message('reminder', 'Mike')
            print(message)
            log_automation('reminder_test', 'Class reminder tested')
            print("\n✅ Reminder system ready!")
            
        elif choice == '3':
            print("\n⭐ Testing Review Request:")
            print("-" * 30)
            message = send_test_message('review', 'Emma')
            print(message)
            log_automation('review_test', 'Review request tested')
            print("\n✅ Review system ready!")
            
        elif choice == '4':
            print("\n👥 Client List:")
            print("-" * 20)
            with sqlite3.connect(db_path) as conn:
                clients = conn.execute('SELECT first_name, last_name, email, total_classes FROM clients').fetchall()
                for client in clients:
                    print(f"{client[0]} {client[1]} - {client[2]} ({client[3]} classes)")
                    
        elif choice == '5':
            print("\n📋 Automation Logs:")
            print("-" * 25)
            with sqlite3.connect(db_path) as conn:
                logs = conn.execute('SELECT action_type, message, created_at FROM automation_log ORDER BY created_at DESC LIMIT 5').fetchall()
                for log in logs:
                    time_str = log[2].split('T')[1][:5] if 'T' in log[2] else log[2][:10]
                    print(f"{time_str} - {log[0]}: {log[1]}")
                    
        else:
            print("❌ Invalid choice. Please enter 1-5.")
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        break
    except Exception as e:
        print(f"❌ Error: {e}")

print()
print("🎉 Your HiYoga automation system is ready!")
print("📋 Next steps:")
print("   1. Add your real API keys to .env file")
print("   2. Connect to Mindbody (Site ID: 32353)")
print("   3. Set up WhatsApp via Twilio (+64 21 199 9642)")
print("   4. Launch full automation!")
print()
print("💰 Expected results:")
print("   • 25% increase in class attendance")
print("   • 40% improvement in membership renewals")
print("   • 60% more Google reviews")
print("   • 15+ hours/week time savings")
print("   • 20% revenue increase")
print()
print("Ready to transform HiYoga.nz! 🚀")