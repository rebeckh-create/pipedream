#!/usr/bin/env python3
"""
HiYoga Simple Control Hub
Your one-stop dashboard for managing studio automations
No extra software needed - uses your existing tools
"""

import os
import json
import sqlite3
import logging
import datetime
import requests
from pathlib import Path
from typing import Dict, List, Optional, Any

class HiYogaHub:
    """Simple control hub for HiYoga studio automation"""
    
    def __init__(self):
        """Initialize HiYoga Hub"""
        self.setup_logging()
        self.setup_database()
        self.load_config()
        
        print("🧘‍♀️ HiYoga Control Hub Initialized")
        print("=" * 40)
    
    def setup_logging(self):
        """Setup simple logging"""
        Path("logs").mkdir(exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            handlers=[
                logging.FileHandler(f"logs/hiyoga_{datetime.datetime.now().strftime('%Y%m%d')}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_database(self):
        """Setup simple SQLite database"""
        Path("data").mkdir(exist_ok=True)
        self.db_path = "data/hiyoga_hub.db"
        
        with sqlite3.connect(self.db_path) as conn:
            # Simple clients table
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
            
            # Automation log
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
    
    def load_config(self):
        """Load simple configuration"""
        self.config = {
            'studio_name': 'HiYoga',
            'studio_phone': '+64 21 199 9642',
            'studio_email': 'info@hiyoga.nz',
            'mindbody_site_id': '32353',
            'enable_whatsapp': True,
            'enable_email': True,
            'enable_reviews': True
        }
    
    # ===== MINDBODY SCRAPING =====
    def scrape_mindbody_data(self):
        """Scrape client data from Mindbody"""
        print("📋 Scraping Mindbody data...")
        
        # Simulated data scraping (in real version, this would connect to Mindbody API)
        new_clients = [
            {
                'id': 'mb_001',
                'first_name': 'Sarah',
                'last_name': 'Wilson',
                'email': 'sarah@example.com',
                'phone': '+64 21 123 4567',
                'last_class_date': '2025-09-24',
                'total_classes': 1,
                'membership_status': 'active'
            },
            {
                'id': 'mb_002',
                'first_name': 'Mike',
                'last_name': 'Johnson', 
                'email': 'mike@example.com',
                'phone': '+64 21 234 5678',
                'last_class_date': '2025-09-20',
                'total_classes': 8,
                'membership_status': 'active'
            }
        ]
        
        # Update database with new/changed clients
        updated_count = 0
        for client in new_clients:
            if self.update_client(client):
                updated_count += 1
        
        print(f"✅ Updated {updated_count} clients from Mindbody")
        return updated_count
    
    def update_client(self, client_data: Dict[str, Any]) -> bool:
        """Update or insert client data"""
        with sqlite3.connect(self.db_path) as conn:
            # Check if client exists
            existing = conn.execute(
                'SELECT id FROM clients WHERE email = ?', 
                (client_data['email'],)
            ).fetchone()
            
            now = datetime.datetime.now().isoformat()
            
            if existing:
                # Update existing client
                conn.execute('''
                    UPDATE clients SET 
                    first_name=?, last_name=?, phone=?, last_class_date=?, 
                    total_classes=?, membership_status=?
                    WHERE email=?
                ''', (
                    client_data['first_name'], client_data['last_name'],
                    client_data['phone'], client_data['last_class_date'],
                    client_data['total_classes'], client_data['membership_status'],
                    client_data['email']
                ))
            else:
                # Insert new client
                conn.execute('''
                    INSERT INTO clients VALUES (?,?,?,?,?,?,?,?,?)
                ''', (
                    client_data['id'], client_data['first_name'], client_data['last_name'],
                    client_data['email'], client_data['phone'], client_data['last_class_date'],
                    client_data['total_classes'], client_data['membership_status'], now
                ))
                
                # Trigger welcome automation for new clients
                self.trigger_welcome_automation(client_data)
                
            conn.commit()
            return True
    
    # ===== AUTOMATION TRIGGERS =====
    def trigger_welcome_automation(self, client_data: Dict[str, Any]):
        """Send welcome messages to new clients"""
        print(f"🌟 Triggering welcome for {client_data['first_name']}")
        
        # Send welcome WhatsApp
        if self.config['enable_whatsapp'] and client_data.get('phone'):
            self.send_whatsapp_message(
                phone=client_data['phone'],
                template='welcome',
                variables={'first_name': client_data['first_name']}
            )
        
        # Send welcome email
        if self.config['enable_email']:
            self.send_email(
                to_email=client_data['email'],
                template='welcome',
                variables={'first_name': client_data['first_name']}
            )
        
        self.log_automation(client_data['email'], 'welcome', 'Welcome sequence sent', 'success')
    
    def check_class_reminders(self):
        """Check for classes that need reminders"""
        print("⏰ Checking class reminders...")
        
        # This would check Mindbody for upcoming classes
        # For now, simulate finding clients who need reminders
        tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            clients = conn.execute('''
                SELECT * FROM clients WHERE membership_status = 'active'
            ''').fetchall()
        
        # Simulate reminder logic
        reminder_count = 0
        for client in clients[:2]:  # Just first 2 for demo
            self.send_class_reminder({
                'first_name': client[1],
                'email': client[3],
                'phone': client[4]
            })
            reminder_count += 1
        
        print(f"✅ Sent {reminder_count} class reminders")
        return reminder_count
    
    def send_class_reminder(self, client_data: Dict[str, Any]):
        """Send class reminder to client"""
        if self.config['enable_whatsapp'] and client_data.get('phone'):
            self.send_whatsapp_message(
                phone=client_data['phone'],
                template='class_reminder_24h',
                variables={
                    'first_name': client_data['first_name'],
                    'class_name': 'Vinyasa Flow',
                    'class_time': '6:00 PM'
                }
            )
        
        self.log_automation(client_data['email'], 'class_reminder', 'Class reminder sent', 'success')
    
    def check_no_shows(self):
        """Check for no-shows and send follow-up"""
        print("💜 Checking no-shows...")
        
        # This would check Mindbody for missed classes
        # Simulate finding no-shows
        no_show_count = 0
        
        with sqlite3.connect(self.db_path) as conn:
            clients = conn.execute('''
                SELECT * FROM clients WHERE membership_status = 'active' LIMIT 1
            ''').fetchall()
        
        for client in clients:
            self.send_no_show_followup({
                'first_name': client[1],
                'email': client[3],
                'phone': client[4]
            })
            no_show_count += 1
        
        print(f"✅ Sent {no_show_count} no-show follow-ups")
        return no_show_count
    
    def send_no_show_followup(self, client_data: Dict[str, Any]):
        """Send caring no-show follow-up"""
        if self.config['enable_whatsapp'] and client_data.get('phone'):
            self.send_whatsapp_message(
                phone=client_data['phone'],
                template='no_show_followup',
                variables={
                    'first_name': client_data['first_name'],
                    'class_name': 'Morning Yoga'
                }
            )
        
        self.log_automation(client_data['email'], 'no_show_followup', 'No-show follow-up sent', 'success')
    
    def check_review_requests(self):
        """Check for clients ready for review requests"""
        print("⭐ Checking review requests...")
        
        with sqlite3.connect(self.db_path) as conn:
            # Find clients with 5+ classes who haven't been asked for review recently
            clients = conn.execute('''
                SELECT * FROM clients WHERE total_classes >= 5 LIMIT 1
            ''').fetchall()
        
        review_count = 0
        for client in clients:
            self.send_review_request({
                'first_name': client[1],
                'email': client[3]
            })
            review_count += 1
        
        print(f"✅ Sent {review_count} review requests")
        return review_count
    
    def send_review_request(self, client_data: Dict[str, Any]):
        """Send Google review request"""
        if self.config['enable_email']:
            self.send_email(
                to_email=client_data['email'],
                template='review_request',
                variables={'first_name': client_data['first_name']}
            )
        
        self.log_automation(client_data['email'], 'review_request', 'Review request sent', 'success')
    
    # ===== MESSAGING =====
    def send_whatsapp_message(self, phone: str, template: str, variables: Dict[str, str]):
        """Send WhatsApp message using templates"""
        templates = {
            'welcome': f"""Kia ora {variables['first_name']}! 🧘‍♀️ 

Welcome to HiYoga! We're so excited to have you join our yoga and pilates community.

Your first class is always special - if you have any questions or need guidance, just reply to this message.

See you on the mat soon!

Namaste,
The HiYoga Team ✨""",

            'class_reminder_24h': f"""Hi {variables['first_name']}! 🧘‍♀️

Just a friendly reminder that you have {variables['class_name']} tomorrow at {variables['class_time']}.

We can't wait to see you on the mat!

If you need to cancel, please do so at least 12 hours in advance through Mindbody.

Namaste! ✨""",

            'no_show_followup': f"""Hi {variables['first_name']} 💜

We missed you at {variables['class_name']} today! Life happens, and we totally understand.

Your wellness journey is important to us - we're here whenever you're ready to get back on the mat.

Your next class is always waiting for you! 🧘‍♀️

Namaste,
HiYoga Team"""
        }
        
        message = templates.get(template, f"Hi {variables['first_name']}, message from HiYoga!")
        
        # In real implementation, this would send via Twilio
        print(f"📱 WhatsApp to {phone}: {message[:50]}...")
        
        # Log the message
        self.logger.info(f"WhatsApp sent to {phone}")
    
    def send_email(self, to_email: str, template: str, variables: Dict[str, str]):
        """Send email using templates"""
        templates = {
            'welcome': {
                'subject': f"Welcome to HiYoga, {variables['first_name']}! 🧘‍♀️",
                'body': f"""Hi {variables['first_name']},

Welcome to HiYoga! We're thrilled to have you join our yoga and pilates community.

Here's what you can expect:
• Expert instruction in a welcoming environment
• Classes for all levels and abilities  
• A supportive community of practitioners

Visit hiyoga.nz to book your next class or manage your membership.

Namaste,
The HiYoga Team"""
            },
            'review_request': {
                'subject': f"How was your HiYoga experience, {variables['first_name']}?",
                'body': f"""Hi {variables['first_name']},

We hope you're loving your yoga journey with us! 🧘‍♀️

If you've enjoyed your classes, would you mind sharing a quick review on Google? It helps other yogis find us!

https://www.google.com/search?q=HIYOGA

Thank you for being part of our community! 💜

Namaste,
HiYoga Team"""
            }
        }
        
        template_data = templates.get(template, {
            'subject': f"Message from HiYoga, {variables['first_name']}",
            'body': f"Hi {variables['first_name']}, thank you for being part of HiYoga!"
        })
        
        # In real implementation, this would send via Gmail/SMTP
        print(f"📧 Email to {to_email}: {template_data['subject']}")
        
        # Log the email
        self.logger.info(f"Email sent to {to_email}")
    
    def log_automation(self, client_email: str, action_type: str, message: str, status: str):
        """Log automation actions"""
        log_id = f"log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        now = datetime.datetime.now().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO automation_log VALUES (?,?,?,?,?,?)
            ''', (log_id, client_email, action_type, message, status, now))
            conn.commit()
    
    # ===== DASHBOARD =====
    def show_dashboard(self):
        """Show simple dashboard"""
        print("\n🧘‍♀️ HiYoga Control Hub Dashboard")
        print("=" * 40)
        
        with sqlite3.connect(self.db_path) as conn:
            # Client stats
            total_clients = conn.execute('SELECT COUNT(*) FROM clients').fetchone()[0]
            active_clients = conn.execute(
                "SELECT COUNT(*) FROM clients WHERE membership_status = 'active'"
            ).fetchone()[0]
            
            # Recent automations
            recent_automations = conn.execute('''
                SELECT action_type, COUNT(*) 
                FROM automation_log 
                WHERE date(created_at) = date('now') 
                GROUP BY action_type
            ''').fetchall()
        
        print(f"📊 Studio Stats:")
        print(f"   Total Clients: {total_clients}")
        print(f"   Active Members: {active_clients}")
        
        print(f"\n🤖 Today's Automations:")
        if recent_automations:
            for action_type, count in recent_automations:
                print(f"   {action_type}: {count}")
        else:
            print("   No automations run today")
        
        print(f"\n⚙️  Available Commands:")
        print(f"   1. Sync Mindbody data")
        print(f"   2. Send class reminders") 
        print(f"   3. Check no-shows")
        print(f"   4. Send review requests")
        print(f"   5. Run all automations")
        print(f"   6. Show logs")
    
    def show_logs(self):
        """Show recent automation logs"""
        print("\n📋 Recent Automation Logs")
        print("-" * 30)
        
        with sqlite3.connect(self.db_path) as conn:
            logs = conn.execute('''
                SELECT action_type, client_email, message, status, created_at
                FROM automation_log 
                ORDER BY created_at DESC 
                LIMIT 10
            ''').fetchall()
        
        for log in logs:
            action_type, email, message, status, created_at = log
            time_str = created_at.split('T')[1][:5]  # Just show time
            status_icon = "✅" if status == "success" else "❌"
            print(f"{time_str} {status_icon} {action_type}: {email} - {message}")
    
    def run_all_automations(self):
        """Run all daily automations"""
        print("\n🚀 Running All Automations")
        print("=" * 30)
        
        # 1. Sync Mindbody data
        self.scrape_mindbody_data()
        
        # 2. Send class reminders
        self.check_class_reminders()
        
        # 3. Check no-shows
        self.check_no_shows()
        
        # 4. Send review requests
        self.check_review_requests()
        
        print("\n🎉 All automations completed!")

def main():
    """Main control hub interface"""
    hub = HiYogaHub()
    
    while True:
        hub.show_dashboard()
        
        try:
            choice = input("\nEnter command (1-6) or 'quit': ").strip()
            
            if choice.lower() in ['quit', 'q', 'exit']:
                print("👋 Goodbye!")
                break
            elif choice == '1':
                hub.scrape_mindbody_data()
            elif choice == '2':
                hub.check_class_reminders()
            elif choice == '3':
                hub.check_no_shows()
            elif choice == '4':
                hub.check_review_requests()
            elif choice == '5':
                hub.run_all_automations()
            elif choice == '6':
                hub.show_logs()
            else:
                print("❌ Invalid choice. Please enter 1-6.")
            
            input("\nPress Enter to continue...")
            print("\n" * 2)  # Clear screen
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()