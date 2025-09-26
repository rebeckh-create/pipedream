#!/usr/bin/env python3
"""
Twilio WhatsApp Integration for HiYoga
Handles WhatsApp messaging through Twilio API
"""

import os
import logging
from typing import Dict, Any, Optional
from twilio.rest import Client
from twilio.base.exceptions import TwilioException

class TwilioWhatsApp:
    """Twilio WhatsApp integration for HiYoga automation"""
    
    def __init__(self):
        """Initialize Twilio WhatsApp client"""
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.from_number = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')
        
        if not self.account_sid or not self.auth_token:
            logging.warning("Twilio credentials not configured")
            self.client = None
        else:
            self.client = Client(self.account_sid, self.auth_token)
            
        self.logger = logging.getLogger(__name__)
    
    def send_message(self, to_number: str, message: str, media_url: Optional[str] = None) -> bool:
        """Send WhatsApp message via Twilio
        
        Args:
            to_number: Recipient's phone number (format: +64XXXXXXXXX)
            message: Message text
            media_url: Optional media URL for images/videos
            
        Returns:
            bool: True if message sent successfully
        """
        if not self.client:
            self.logger.error("Twilio client not initialized")
            return False
        
        # Format phone number for WhatsApp
        if not to_number.startswith('whatsapp:'):
            to_number = f'whatsapp:{to_number}'
        
        try:
            message_data = {
                'from_': self.from_number,
                'body': message,
                'to': to_number
            }
            
            if media_url:
                message_data['media_url'] = [media_url]
            
            message = self.client.messages.create(**message_data)
            
            self.logger.info(f"WhatsApp message sent successfully. SID: {message.sid}")
            return True
            
        except TwilioException as e:
            self.logger.error(f"Failed to send WhatsApp message: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error sending WhatsApp message: {e}")
            return False
    
    def send_template_message(self, to_number: str, template_name: str, variables: Dict[str, str]) -> bool:
        """Send templated WhatsApp message
        
        Args:
            to_number: Recipient's phone number
            template_name: Name of the message template
            variables: Variables to substitute in template
            
        Returns:
            bool: True if message sent successfully
        """
        templates = {
            'welcome': """Kia ora {first_name}! 🧘‍♀️ 

Welcome to HiYoga! We're so excited to have you join our yoga and pilates community.

Your first class is always special - if you have any questions or need guidance, just reply to this message.

See you on the mat soon!

Namaste,
The HiYoga Team ✨""",

            'class_reminder_24h': """Hi {first_name}! 🧘‍♀️

Just a friendly reminder that you have {class_name} tomorrow at {class_time}.

We can't wait to see you on the mat!

If you need to cancel, please do so at least 12 hours in advance through Mindbody.

Namaste! ✨""",

            'class_reminder_2h': """Hi {first_name}! 

Your {class_name} class starts in 2 hours at {class_time}. 

See you soon! 🧘‍♀️""",

            'class_reminder_30min': """Hi {first_name}! 

Quick reminder - your {class_name} class starts in 30 minutes!

We're looking forward to seeing you! 🧘‍♀️""",

            'no_show_followup': """Hi {first_name} 💜

We missed you at {class_name} today! Life happens, and we totally understand.

Your wellness journey is important to us - we're here whenever you're ready to get back on the mat.

Your next class is always waiting for you! 🧘‍♀️

Namaste,
HiYoga Team""",

            'membership_renewal': """Hi {first_name}! 

Your {membership_type} membership expires in {days_until_expiry} days.

Don't let your practice pause - renew today to keep your spot on the mat! 

Reply 'RENEW' or visit hiyoga.nz to continue your journey.

Namaste! 🧘‍♀️""",

            'win_back': """Hi {first_name}, we miss you at HiYoga! 💜

It's been a while since we've seen you on the mat. Your wellness journey is important, and we're here to support you.

Come back and reconnect with your practice - we have some exciting new classes you'd love!

Special offer: Use code WELCOME-BACK for 20% off your next class package.

Hope to see you soon! 🧘‍♀️""",

            'birthday': """Happy Birthday {first_name}! 🎉🧘‍♀️

Wishing you a year full of peace, strength, and beautiful moments on the mat.

As a birthday gift, enjoy a complimentary class this month! Just mention this message when you book.

Celebrate your special day with some self-care - you deserve it! ✨

With love,
The HiYoga Team 💜""",

            'review_request': """Hi {first_name}! 

We hope you're loving your yoga journey with us! 🧘‍♀️

If you've enjoyed your classes, would you mind sharing a quick review on Google? It helps other yogis find us!

https://g.page/r/YOUR_GOOGLE_REVIEW_LINK/review

Thank you for being part of our community! 💜

Namaste,
HiYoga Team""",

            'booking_confirmation': """Hi {first_name}! ✨

Your booking is confirmed:

📅 {class_name}
🕐 {class_date} at {class_time}
📍 HiYoga Studio

We can't wait to see you on the mat! 

If you need to cancel, please do so at least 12 hours in advance.

Namaste! 🧘‍♀️""",

            'waitlist_spot_available': """Great news {first_name}! 🎉

A spot just opened up in {class_name} on {class_date} at {class_time}!

You have 15 minutes to claim your spot. Reply 'YES' to confirm or visit Mindbody to book.

See you on the mat! 🧘‍♀️"""
        }
        
        if template_name not in templates:
            self.logger.error(f"Template '{template_name}' not found")
            return False
        
        # Format message with variables
        message = templates[template_name].format(**variables)
        
        return self.send_message(to_number, message)
    
    def test_connection(self) -> bool:
        """Test Twilio connection"""
        if not self.client:
            return False
        
        try:
            # Test by fetching account info
            account = self.client.api.accounts(self.account_sid).fetch()
            self.logger.info(f"Twilio connection successful. Account: {account.friendly_name}")
            return True
        except Exception as e:
            self.logger.error(f"Twilio connection test failed: {e}")
            return False

def main():
    """Test the Twilio WhatsApp integration"""
    import logging
    logging.basicConfig(level=logging.INFO)
    
    twilio_wa = TwilioWhatsApp()
    
    print("🧘‍♀️ Testing HiYoga Twilio WhatsApp Integration")
    print("=" * 50)
    
    # Test connection
    if twilio_wa.test_connection():
        print("✅ Twilio connection: SUCCESS")
    else:
        print("❌ Twilio connection: FAILED")
        print("   Check your TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN")
        return 1
    
    # Test template message (to a test number - replace with actual)
    test_number = "+64XXXXXXXXX"  # Replace with your test number
    
    success = twilio_wa.send_template_message(
        to_number=test_number,
        template_name='welcome',
        variables={
            'first_name': 'Test User'
        }
    )
    
    if success:
        print("✅ Test message: SENT")
    else:
        print("❌ Test message: FAILED")
    
    return 0

if __name__ == "__main__":
    exit(main())