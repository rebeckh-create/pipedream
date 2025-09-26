#!/usr/bin/env python3
"""
HiYoga.nz Studio Automation System
Complete business automation for yoga and pilates studio operations
"""

import os
import json
import sqlite3
import logging
import datetime
import requests
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import uuid
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart

@dataclass
class HiYogaClient:
    """HiYoga client data structure"""
    id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    mindbody_id: str = ""
    membership_type: str = "drop-in"
    membership_status: str = "active"
    join_date: str = ""
    last_class_date: str = ""
    total_classes: int = 0
    preferred_class_types: List[str] = None
    communication_preferences: Dict[str, bool] = None
    emergency_contact: str = ""
    medical_notes: str = ""
    created_at: str = ""
    updated_at: str = ""

@dataclass
class AutomationTrigger:
    """Automation trigger configuration"""
    id: str
    name: str
    trigger_type: str  # new_booking, missed_class, membership_expiry, etc.
    conditions: Dict[str, Any]
    actions: List[Dict[str, Any]]
    active: bool = True
    created_at: str = ""

class HiYogaAutomation:
    """Main automation system for HiYoga.nz"""
    
    def __init__(self, config_path: str = "config/hiyoga_config.yaml"):
        """Initialize the HiYoga automation system"""
        self.config_path = config_path
        self.config = self._load_config()
        self._setup_logging()
        self._create_directories()
        self._setup_database()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration"""
        # Default configuration for HiYoga
        return {
            "studio": {
                "name": "HiYoga",
                "website": "hiyoga.nz",
                "location": "Auckland, New Zealand",
                "email": "info@hiyoga.nz",
                "phone": "+64 9 XXX XXXX"
            },
            "integrations": {
                "mindbody": {
                    "api_key": "",
                    "site_id": "",
                    "enabled": True
                },
                "whatsapp": {
                    "api_token": "",
                    "phone_number": "",
                    "enabled": True
                },
                "metasuite": {
                    "api_key": "",
                    "enabled": True
                },
                "manychat": {
                    "api_token": "",
                    "enabled": True
                },
                "google": {
                    "analytics_id": "",
                    "business_id": "",
                    "enabled": True
                }
            },
            "automation_rules": {
                "new_client_welcome": True,
                "class_reminders": True,
                "no_show_followup": True,
                "membership_renewal": True,
                "win_back_campaigns": True,
                "birthday_messages": True,
                "review_requests": True
            }
        }
    
    def _setup_logging(self):
        """Setup logging"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f"logs/hiyoga_{datetime.datetime.now().strftime('%Y%m%d')}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("HiYoga automation system initialized")
    
    def _create_directories(self):
        """Create necessary directories"""
        directories = ["data", "exports", "reports", "templates", "campaigns"]
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def _setup_database(self):
        """Setup database with HiYoga-specific tables"""
        db_path = "data/hiyoga.db"
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(db_path) as conn:
            # Clients table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS clients (
                    id TEXT PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT,
                    mindbody_id TEXT,
                    membership_type TEXT,
                    membership_status TEXT,
                    join_date TEXT,
                    last_class_date TEXT,
                    total_classes INTEGER DEFAULT 0,
                    preferred_class_types TEXT,
                    communication_preferences TEXT,
                    emergency_contact TEXT,
                    medical_notes TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
            ''')
            
            # Automation triggers table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS automation_triggers (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    trigger_type TEXT,
                    conditions TEXT,
                    actions TEXT,
                    active BOOLEAN DEFAULT 1,
                    created_at TEXT
                )
            ''')
            
            # Automation logs table
            conn.execute('''
                CREATE TABLE IF NOT EXISTS automation_logs (
                    id TEXT PRIMARY KEY,
                    trigger_id TEXT,
                    client_id TEXT,
                    action_type TEXT,
                    status TEXT,
                    message TEXT,
                    executed_at TEXT
                )
            ''')
            
            conn.commit()
            self.logger.info("HiYoga database initialized")
    
    # MINDBODY INTEGRATION
    def sync_mindbody_clients(self) -> int:
        """Sync clients from Mindbody"""
        if not self.config["integrations"]["mindbody"]["enabled"]:
            self.logger.info("Mindbody integration disabled")
            return 0
        
        # This would integrate with actual Mindbody API
        # For now, we'll simulate the sync
        self.logger.info("Syncing clients from Mindbody...")
        
        # Simulated client data that would come from Mindbody API
        mindbody_clients = [
            {
                "id": "mb_001",
                "first_name": "Sarah",
                "last_name": "Wilson",
                "email": "sarah@example.com",
                "phone": "+64 21 123 4567",
                "membership_type": "unlimited",
                "last_visit": "2025-09-20"
            },
            {
                "id": "mb_002", 
                "first_name": "Mike",
                "last_name": "Johnson",
                "email": "mike@example.com",
                "phone": "+64 21 234 5678",
                "membership_type": "monthly",
                "last_visit": "2025-09-18"
            }
        ]
        
        synced_count = 0
        for mb_client in mindbody_clients:
            client_data = {
                "first_name": mb_client["first_name"],
                "last_name": mb_client["last_name"],
                "email": mb_client["email"],
                "phone": mb_client["phone"],
                "mindbody_id": mb_client["id"],
                "membership_type": mb_client["membership_type"],
                "last_class_date": mb_client.get("last_visit", "")
            }
            
            # Check if client exists, update or create
            existing_client = self._get_client_by_email(mb_client["email"])
            if existing_client:
                self._update_client(existing_client.id, client_data)
            else:
                self._add_client(client_data)
            
            synced_count += 1
        
        self.logger.info(f"Synced {synced_count} clients from Mindbody")
        return synced_count
    
    def _get_client_by_email(self, email: str) -> Optional[HiYogaClient]:
        """Get client by email"""
        with sqlite3.connect("data/hiyoga.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('SELECT * FROM clients WHERE email = ?', (email,))
            row = cursor.fetchone()
            
            if row:
                client_dict = dict(row)
                # Parse JSON fields
                client_dict['preferred_class_types'] = json.loads(client_dict.get('preferred_class_types', '[]'))
                client_dict['communication_preferences'] = json.loads(client_dict.get('communication_preferences', '{}'))
                return HiYogaClient(**client_dict)
            return None
    
    def _add_client(self, client_data: Dict[str, Any]) -> str:
        """Add new client"""
        client_id = str(uuid.uuid4())
        now = datetime.datetime.now().isoformat()
        
        client = HiYogaClient(
            id=client_id,
            first_name=client_data['first_name'],
            last_name=client_data['last_name'],
            email=client_data['email'],
            phone=client_data.get('phone', ''),
            mindbody_id=client_data.get('mindbody_id', ''),
            membership_type=client_data.get('membership_type', 'drop-in'),
            membership_status=client_data.get('membership_status', 'active'),
            join_date=client_data.get('join_date', now.split('T')[0]),
            last_class_date=client_data.get('last_class_date', ''),
            total_classes=client_data.get('total_classes', 0),
            preferred_class_types=client_data.get('preferred_class_types', []),
            communication_preferences=client_data.get('communication_preferences', {
                'email': True, 'whatsapp': True, 'sms': False
            }),
            emergency_contact=client_data.get('emergency_contact', ''),
            medical_notes=client_data.get('medical_notes', ''),
            created_at=now,
            updated_at=now
        )
        
        with sqlite3.connect("data/hiyoga.db") as conn:
            conn.execute('''
                INSERT INTO clients VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''', (
                client.id, client.first_name, client.last_name, client.email,
                client.phone, client.mindbody_id, client.membership_type,
                client.membership_status, client.join_date, client.last_class_date,
                client.total_classes, json.dumps(client.preferred_class_types),
                json.dumps(client.communication_preferences), client.emergency_contact,
                client.medical_notes, client.created_at, client.updated_at
            ))
            conn.commit()
        
        # Trigger new client welcome automation
        self._trigger_automation('new_client_welcome', client_id)
        
        self.logger.info(f"Added new client: {client.first_name} {client.last_name}")
        return client_id
    
    def _update_client(self, client_id: str, updates: Dict[str, Any]) -> bool:
        """Update client information"""
        updates['updated_at'] = datetime.datetime.now().isoformat()
        
        # Convert lists/dicts to JSON strings for storage
        if 'preferred_class_types' in updates:
            updates['preferred_class_types'] = json.dumps(updates['preferred_class_types'])
        if 'communication_preferences' in updates:
            updates['communication_preferences'] = json.dumps(updates['communication_preferences'])
        
        set_clause = ', '.join([f'{key} = ?' for key in updates.keys()])
        values = list(updates.values()) + [client_id]
        
        with sqlite3.connect("data/hiyoga.db") as conn:
            cursor = conn.execute(f'UPDATE clients SET {set_clause} WHERE id = ?', values)
            conn.commit()
            
        return cursor.rowcount > 0
    
    # AUTOMATION TRIGGERS
    def _trigger_automation(self, trigger_type: str, client_id: str, context: Dict[str, Any] = None):
        """Trigger automation based on event"""
        if not self.config["automation_rules"].get(trigger_type, False):
            return
        
        client = self._get_client_by_id(client_id)
        if not client:
            return
        
        context = context or {}
        
        if trigger_type == 'new_client_welcome':
            self._send_welcome_sequence(client)
        elif trigger_type == 'class_reminder':
            self._send_class_reminder(client, context)
        elif trigger_type == 'no_show_followup':
            self._send_no_show_followup(client, context)
        elif trigger_type == 'membership_renewal':
            self._send_renewal_reminder(client)
        elif trigger_type == 'win_back_campaign':
            self._send_win_back_message(client)
        elif trigger_type == 'birthday_message':
            self._send_birthday_message(client)
        elif trigger_type == 'review_request':
            self._send_review_request(client)
        
        # Log automation execution
        self._log_automation(trigger_type, client_id, "executed", f"Triggered {trigger_type}")
    
    def _get_client_by_id(self, client_id: str) -> Optional[HiYogaClient]:
        """Get client by ID"""
        with sqlite3.connect("data/hiyoga.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('SELECT * FROM clients WHERE id = ?', (client_id,))
            row = cursor.fetchone()
            
            if row:
                client_dict = dict(row)
                client_dict['preferred_class_types'] = json.loads(client_dict.get('preferred_class_types', '[]'))
                client_dict['communication_preferences'] = json.loads(client_dict.get('communication_preferences', '{}'))
                return HiYogaClient(**client_dict)
            return None
    
    # COMMUNICATION METHODS
    def _send_welcome_sequence(self, client: HiYogaClient):
        """Send welcome sequence to new client"""
        self.logger.info(f"Sending welcome sequence to {client.email}")
        
        # Email welcome
        if client.communication_preferences.get('email', True):
            self._send_email(
                to_email=client.email,
                subject=f"Welcome to HiYoga, {client.first_name}! 🧘‍♀️",
                template="welcome_email",
                variables={
                    "first_name": client.first_name,
                    "studio_name": "HiYoga",
                    "website": "hiyoga.nz"
                }
            )
        
        # WhatsApp welcome (if enabled and phone provided)
        if client.communication_preferences.get('whatsapp', True) and client.phone:
            self._send_whatsapp_message(
                phone=client.phone,
                message=f"Kia ora {client.first_name}! Welcome to HiYoga 🧘‍♀️ We're excited to have you join our community. Your first class is always special - let us know if you need any guidance!"
            )
    
    def _send_class_reminder(self, client: HiYogaClient, context: Dict[str, Any]):
        """Send class reminder"""
        class_name = context.get('class_name', 'your class')
        class_time = context.get('class_time', '')
        
        # WhatsApp reminder
        if client.communication_preferences.get('whatsapp', True) and client.phone:
            message = f"Hi {client.first_name}! Reminder: You have {class_name} tomorrow at {class_time}. See you on the mat! 🧘‍♀️"
            self._send_whatsapp_message(client.phone, message)
    
    def _send_no_show_followup(self, client: HiYogaClient, context: Dict[str, Any]):
        """Send follow-up message for missed class"""
        class_name = context.get('class_name', 'your class')
        
        message = f"Hi {client.first_name}, we missed you at {class_name} today! Life happens - hope to see you soon. Your next class is always waiting for you 💜"
        
        if client.communication_preferences.get('whatsapp', True) and client.phone:
            self._send_whatsapp_message(client.phone, message)
    
    def _send_renewal_reminder(self, client: HiYogaClient):
        """Send membership renewal reminder"""
        if client.communication_preferences.get('email', True):
            self._send_email(
                to_email=client.email,
                subject=f"Time to Renew Your HiYoga Membership, {client.first_name}",
                template="renewal_reminder",
                variables={
                    "first_name": client.first_name,
                    "membership_type": client.membership_type
                }
            )
    
    def _send_win_back_message(self, client: HiYogaClient):
        """Send win-back campaign message"""
        message = f"Hi {client.first_name}, we miss you at HiYoga! 💜 Come back and reconnect with your practice. We have some exciting new classes you'd love!"
        
        if client.communication_preferences.get('whatsapp', True) and client.phone:
            self._send_whatsapp_message(client.phone, message)
    
    def _send_birthday_message(self, client: HiYogaClient):
        """Send birthday message"""
        message = f"Happy Birthday {client.first_name}! 🎉 Wishing you a year full of peace, strength, and beautiful moments on the mat. Enjoy your special day!"
        
        if client.communication_preferences.get('whatsapp', True) and client.phone:
            self._send_whatsapp_message(client.phone, message)
    
    def _send_review_request(self, client: HiYogaClient):
        """Send review request"""
        if client.communication_preferences.get('email', True):
            self._send_email(
                to_email=client.email,
                subject=f"How was your experience at HiYoga, {client.first_name}?",
                template="review_request",
                variables={
                    "first_name": client.first_name,
                    "google_review_link": "https://g.page/r/YOUR_GOOGLE_BUSINESS_ID/review"
                }
            )
    
    # COMMUNICATION INTEGRATIONS
    def _send_email(self, to_email: str, subject: str, template: str, variables: Dict[str, Any]):
        """Send email using template"""
        # This would integrate with your email service (Gmail, SendGrid, etc.)
        self.logger.info(f"Sending email to {to_email}: {subject}")
        
        # Load email template
        template_content = self._load_email_template(template, variables)
        
        # For now, just log the email (in production, integrate with actual email service)
        self._log_automation("email", to_email, "sent", f"Email sent: {subject}")
    
    def _send_whatsapp_message(self, phone: str, message: str):
        """Send WhatsApp message via Twilio"""
        if not self.config["integrations"]["whatsapp"]["enabled"]:
            return
        
        try:
            from .twilio_whatsapp import TwilioWhatsApp
            twilio_wa = TwilioWhatsApp()
            
            success = twilio_wa.send_message(phone, message)
            
            if success:
                self.logger.info(f"WhatsApp sent to {phone}: {message[:50]}...")
                self._log_automation("whatsapp", phone, "sent", f"WhatsApp sent: {message[:100]}")
            else:
                self.logger.error(f"Failed to send WhatsApp to {phone}")
                self._log_automation("whatsapp", phone, "failed", f"WhatsApp failed: {message[:100]}")
                
        except ImportError:
            self.logger.error("Twilio not installed. Install with: pip install twilio")
            self._log_automation("whatsapp", phone, "failed", "Twilio not installed")
    
    def _load_email_template(self, template_name: str, variables: Dict[str, Any]) -> str:
        """Load and process email template"""
        template_path = f"templates/{template_name}.html"
        
        # Create template if it doesn't exist
        if not Path(template_path).exists():
            self._create_default_templates()
        
        try:
            with open(template_path, 'r') as f:
                template_content = f.read()
                
            # Simple variable substitution
            for key, value in variables.items():
                template_content = template_content.replace(f"{{{key}}}", str(value))
                
            return template_content
        except FileNotFoundError:
            return f"Template {template_name} not found"
    
    def _create_default_templates(self):
        """Create default email templates"""
        templates = {
            "welcome_email": """
            <h2>Welcome to {studio_name}, {first_name}! 🧘‍♀️</h2>
            <p>We're thrilled to have you join our yoga and pilates community!</p>
            <p>Here's what you can expect:</p>
            <ul>
                <li>Expert instruction in a welcoming environment</li>
                <li>Classes for all levels and abilities</li>
                <li>A supportive community of practitioners</li>
            </ul>
            <p>Visit us at <a href="https://{website}">{website}</a> to book your next class.</p>
            <p>Namaste,<br>The HiYoga Team</p>
            """,
            
            "renewal_reminder": """
            <h2>Time to Renew, {first_name}!</h2>
            <p>Your {membership_type} membership is coming up for renewal.</p>
            <p>Don't miss out on your yoga practice - renew today to keep your spot on the mat!</p>
            <p><a href="https://hiyoga.nz/renew">Renew Now</a></p>
            """,
            
            "review_request": """
            <h2>How was your HiYoga experience, {first_name}?</h2>
            <p>We'd love to hear about your experience at HiYoga!</p>
            <p>If you enjoyed your time with us, would you mind sharing a quick review?</p>
            <p><a href="{google_review_link}">Leave a Google Review</a></p>
            <p>Your feedback helps us improve and helps others find us!</p>
            """
        }
        
        Path("templates").mkdir(exist_ok=True)
        for template_name, content in templates.items():
            with open(f"templates/{template_name}.html", 'w') as f:
                f.write(content)
    
    def _log_automation(self, action_type: str, target: str, status: str, message: str):
        """Log automation execution"""
        log_id = str(uuid.uuid4())
        now = datetime.datetime.now().isoformat()
        
        with sqlite3.connect("data/hiyoga.db") as conn:
            conn.execute('''
                INSERT INTO automation_logs VALUES (?,?,?,?,?,?,?)
            ''', (log_id, "", target, action_type, status, message, now))
            conn.commit()
    
    # REPORTING AND ANALYTICS
    def get_automation_report(self, days: int = 30) -> Dict[str, Any]:
        """Generate automation performance report"""
        start_date = (datetime.datetime.now() - datetime.timedelta(days=days)).isoformat()
        
        with sqlite3.connect("data/hiyoga.db") as conn:
            conn.row_factory = sqlite3.Row
            
            # Get automation stats
            stats = conn.execute('''
                SELECT action_type, status, COUNT(*) as count
                FROM automation_logs
                WHERE executed_at >= ?
                GROUP BY action_type, status
            ''', (start_date,)).fetchall()
            
            # Get client growth
            new_clients = conn.execute('''
                SELECT COUNT(*) as count
                FROM clients
                WHERE created_at >= ?
            ''', (start_date,)).fetchone()
            
            return {
                'period_days': days,
                'automation_stats': [dict(row) for row in stats],
                'new_clients': new_clients['count'],
                'total_automations': sum(row['count'] for row in stats)
            }
    
    def get_client_engagement_report(self) -> Dict[str, Any]:
        """Generate client engagement report"""
        with sqlite3.connect("data/hiyoga.db") as conn:
            conn.row_factory = sqlite3.Row
            
            # Membership distribution
            membership_stats = conn.execute('''
                SELECT membership_type, COUNT(*) as count
                FROM clients
                GROUP BY membership_type
            ''').fetchall()
            
            # Communication preferences
            comm_prefs = conn.execute('''
                SELECT communication_preferences, COUNT(*) as count
                FROM clients
                GROUP BY communication_preferences
            ''').fetchall()
            
            return {
                'total_clients': conn.execute('SELECT COUNT(*) FROM clients').fetchone()[0],
                'membership_distribution': [dict(row) for row in membership_stats],
                'communication_preferences': [dict(row) for row in comm_prefs]
            }
    
    # MAIN AUTOMATION RUNNER
    def run_daily_automations(self):
        """Run daily automation tasks"""
        self.logger.info("Running daily automations...")
        
        # Sync with Mindbody
        self.sync_mindbody_clients()
        
        # Check for membership renewals (30 days out)
        self._check_renewal_reminders()
        
        # Check for win-back campaigns (clients who haven't been in 14 days)
        self._check_win_back_campaigns()
        
        # Send birthday messages
        self._check_birthday_messages()
        
        self.logger.info("Daily automations completed")
    
    def _check_renewal_reminders(self):
        """Check for clients needing renewal reminders"""
        # This would check Mindbody for expiring memberships
        # For now, we'll simulate
        self.logger.info("Checking renewal reminders...")
    
    def _check_win_back_campaigns(self):
        """Check for clients to target with win-back campaigns"""
        cutoff_date = (datetime.datetime.now() - datetime.timedelta(days=14)).isoformat()
        
        with sqlite3.connect("data/hiyoga.db") as conn:
            cursor = conn.execute('''
                SELECT id FROM clients 
                WHERE last_class_date < ? AND last_class_date != ''
            ''', (cutoff_date,))
            
            inactive_clients = cursor.fetchall()
            
        for client_row in inactive_clients:
            self._trigger_automation('win_back_campaign', client_row[0])
    
    def _check_birthday_messages(self):
        """Check for client birthdays today"""
        # This would check client birthdays and send messages
        # Implementation would depend on having birthday data
        self.logger.info("Checking birthday messages...")

def main():
    """Main entry point"""
    try:
        automation = HiYogaAutomation()
        
        print("🧘‍♀️ HiYoga.nz Automation System")
        print("=================================")
        
        # Show current stats
        report = automation.get_automation_report(7)
        print(f"Automations (last 7 days): {report['total_automations']}")
        print(f"New clients (last 7 days): {report['new_clients']}")
        
        engagement = automation.get_client_engagement_report()
        print(f"Total clients: {engagement['total_clients']}")
        
        return 0
        
    except Exception as e:
        print(f"Error initializing HiYoga automation: {e}")
        return 1

if __name__ == "__main__":
    exit(main())