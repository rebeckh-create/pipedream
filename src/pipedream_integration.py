#!/usr/bin/env python3
"""
Pipedream Integration for HiYoga Automation
Uses Pipedream workflows and OAuth for seamless API integrations
"""

import os
import json
import requests
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

class PipedreamIntegration:
    """Pipedream integration for HiYoga automation workflows"""
    
    def __init__(self):
        """Initialize Pipedream integration"""
        self.pipedream_api_key = os.getenv('PIPEDREAM_API_KEY')
        self.pipedream_base_url = "https://api.pipedream.com/v1"
        self.webhook_base_url = "https://webhook.pipedream.com"
        
        # HiYoga specific workflow endpoints (you'll get these from Pipedream)
        self.workflows = {
            'mindbody_sync': os.getenv('PIPEDREAM_MINDBODY_WORKFLOW_ID'),
            'whatsapp_send': os.getenv('PIPEDREAM_WHATSAPP_WORKFLOW_ID'),
            'email_send': os.getenv('PIPEDREAM_EMAIL_WORKFLOW_ID'),
            'facebook_post': os.getenv('PIPEDREAM_FACEBOOK_WORKFLOW_ID'),
            'google_review': os.getenv('PIPEDREAM_GOOGLE_WORKFLOW_ID')
        }
        
        self.logger = logging.getLogger(__name__)
        
        if not self.pipedream_api_key:
            self.logger.warning("Pipedream API key not configured")
    
    def trigger_workflow(self, workflow_name: str, data: Dict[str, Any]) -> bool:
        """Trigger a Pipedream workflow with data
        
        Args:
            workflow_name: Name of the workflow (e.g., 'whatsapp_send')
            data: Data to send to the workflow
            
        Returns:
            bool: True if workflow triggered successfully
        """
        if workflow_name not in self.workflows:
            self.logger.error(f"Workflow '{workflow_name}' not configured")
            return False
        
        workflow_id = self.workflows[workflow_name]
        if not workflow_id:
            self.logger.error(f"Workflow ID for '{workflow_name}' not set")
            return False
        
        try:
            # Trigger workflow via webhook
            webhook_url = f"{self.webhook_base_url}/{workflow_id}"
            
            response = requests.post(
                webhook_url,
                json=data,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                self.logger.info(f"Successfully triggered workflow: {workflow_name}")
                return True
            else:
                self.logger.error(f"Failed to trigger workflow {workflow_name}: {response.status_code}")
                return False
                
        except requests.RequestException as e:
            self.logger.error(f"Error triggering workflow {workflow_name}: {e}")
            return False
    
    # MINDBODY INTEGRATION
    def sync_mindbody_clients(self) -> Dict[str, Any]:
        """Sync clients from Mindbody using Pipedream workflow"""
        data = {
            'action': 'sync_clients',
            'site_id': '32353',
            'timestamp': datetime.now().isoformat()
        }
        
        success = self.trigger_workflow('mindbody_sync', data)
        
        return {
            'success': success,
            'action': 'sync_clients',
            'timestamp': datetime.now().isoformat()
        }
    
    def get_mindbody_classes(self, date_from: str, date_to: str) -> Dict[str, Any]:
        """Get class schedule from Mindbody"""
        data = {
            'action': 'get_classes',
            'site_id': '32353',
            'date_from': date_from,
            'date_to': date_to,
            'timestamp': datetime.now().isoformat()
        }
        
        success = self.trigger_workflow('mindbody_sync', data)
        
        return {
            'success': success,
            'action': 'get_classes',
            'date_range': f"{date_from} to {date_to}"
        }
    
    # WHATSAPP INTEGRATION
    def send_whatsapp_message(self, phone: str, message: str, template: Optional[str] = None) -> bool:
        """Send WhatsApp message via Pipedream workflow"""
        data = {
            'to': phone,
            'message': message,
            'from': '+640211999642',  # HiYoga studio number
            'timestamp': datetime.now().isoformat()
        }
        
        if template:
            data['template'] = template
        
        return self.trigger_workflow('whatsapp_send', data)
    
    def send_whatsapp_template(self, phone: str, template_name: str, variables: Dict[str, str]) -> bool:
        """Send templated WhatsApp message"""
        data = {
            'to': phone,
            'template_name': template_name,
            'variables': variables,
            'from': '+640211999642',
            'timestamp': datetime.now().isoformat()
        }
        
        return self.trigger_workflow('whatsapp_send', data)
    
    # EMAIL INTEGRATION
    def send_email(self, to_email: str, subject: str, template: str, variables: Dict[str, str]) -> bool:
        """Send email via Pipedream workflow"""
        data = {
            'to': to_email,
            'subject': subject,
            'template': template,
            'variables': variables,
            'from_email': 'info@hiyoga.nz',
            'from_name': 'HiYoga Team',
            'timestamp': datetime.now().isoformat()
        }
        
        return self.trigger_workflow('email_send', data)
    
    # FACEBOOK/INSTAGRAM INTEGRATION
    def post_to_social_media(self, message: str, image_url: Optional[str] = None, platforms: List[str] = None) -> bool:
        """Post to Facebook/Instagram via Pipedream"""
        if platforms is None:
            platforms = ['facebook', 'instagram']
        
        data = {
            'message': message,
            'platforms': platforms,
            'timestamp': datetime.now().isoformat()
        }
        
        if image_url:
            data['image_url'] = image_url
        
        return self.trigger_workflow('facebook_post', data)
    
    # GOOGLE INTEGRATION
    def request_google_review(self, client_email: str, client_name: str) -> bool:
        """Send Google review request via Pipedream"""
        data = {
            'client_email': client_email,
            'client_name': client_name,
            'business_name': 'HIYOGA',
            'review_url': 'https://www.google.com/search?q=HIYOGA&stick=H4sIAAAAAAAA_-NgU1I1qDBLMUgxMU9LSk01TDY3TEqzMqgwtLA0MTdIMzQxNTMEsi0XsbJ5eEb6uzsCAGAb6W4yAAAA&hl=en',
            'timestamp': datetime.now().isoformat()
        }
        
        return self.trigger_workflow('google_review', data)
    
    # AUTOMATION WORKFLOWS
    def trigger_welcome_sequence(self, client_data: Dict[str, Any]) -> bool:
        """Trigger welcome sequence for new client"""
        # Send welcome email
        email_success = self.send_email(
            to_email=client_data['email'],
            subject=f"Welcome to HiYoga, {client_data['first_name']}! 🧘‍♀️",
            template='welcome_email',
            variables={
                'first_name': client_data['first_name'],
                'studio_name': 'HiYoga'
            }
        )
        
        # Send welcome WhatsApp
        whatsapp_success = self.send_whatsapp_template(
            phone=client_data.get('phone', ''),
            template_name='welcome',
            variables={
                'first_name': client_data['first_name']
            }
        )
        
        return email_success and whatsapp_success
    
    def trigger_class_reminder(self, client_data: Dict[str, Any], class_data: Dict[str, Any], hours_before: int) -> bool:
        """Trigger class reminder"""
        template_name = f'class_reminder_{hours_before}h'
        
        return self.send_whatsapp_template(
            phone=client_data.get('phone', ''),
            template_name=template_name,
            variables={
                'first_name': client_data['first_name'],
                'class_name': class_data['name'],
                'class_time': class_data['time'],
                'class_date': class_data['date']
            }
        )
    
    def trigger_no_show_followup(self, client_data: Dict[str, Any], class_data: Dict[str, Any]) -> bool:
        """Trigger no-show follow-up"""
        return self.send_whatsapp_template(
            phone=client_data.get('phone', ''),
            template_name='no_show_followup',
            variables={
                'first_name': client_data['first_name'],
                'class_name': class_data['name']
            }
        )
    
    def trigger_membership_renewal(self, client_data: Dict[str, Any], days_until_expiry: int) -> bool:
        """Trigger membership renewal reminder"""
        # Send email
        email_success = self.send_email(
            to_email=client_data['email'],
            subject=f"Time to Renew Your HiYoga Membership, {client_data['first_name']}",
            template='membership_renewal',
            variables={
                'first_name': client_data['first_name'],
                'membership_type': client_data.get('membership_type', 'membership'),
                'days_until_expiry': str(days_until_expiry)
            }
        )
        
        # Send WhatsApp
        whatsapp_success = self.send_whatsapp_template(
            phone=client_data.get('phone', ''),
            template_name='membership_renewal',
            variables={
                'first_name': client_data['first_name'],
                'membership_type': client_data.get('membership_type', 'membership'),
                'days_until_expiry': str(days_until_expiry)
            }
        )
        
        return email_success or whatsapp_success
    
    def trigger_win_back_campaign(self, client_data: Dict[str, Any]) -> bool:
        """Trigger win-back campaign"""
        return self.send_whatsapp_template(
            phone=client_data.get('phone', ''),
            template_name='win_back',
            variables={
                'first_name': client_data['first_name']
            }
        )
    
    def trigger_birthday_message(self, client_data: Dict[str, Any]) -> bool:
        """Trigger birthday message"""
        return self.send_whatsapp_template(
            phone=client_data.get('phone', ''),
            template_name='birthday',
            variables={
                'first_name': client_data['first_name']
            }
        )
    
    def trigger_review_request(self, client_data: Dict[str, Any]) -> bool:
        """Trigger review request"""
        return self.request_google_review(
            client_email=client_data['email'],
            client_name=f"{client_data['first_name']} {client_data.get('last_name', '')}"
        )
    
    def test_all_workflows(self) -> Dict[str, bool]:
        """Test all configured workflows"""
        results = {}
        
        for workflow_name, workflow_id in self.workflows.items():
            if workflow_id:
                test_data = {
                    'test': True,
                    'workflow': workflow_name,
                    'timestamp': datetime.now().isoformat()
                }
                
                results[workflow_name] = self.trigger_workflow(workflow_name, test_data)
            else:
                results[workflow_name] = False
        
        return results

def main():
    """Test the Pipedream integration"""
    import logging
    logging.basicConfig(level=logging.INFO)
    
    pipedream = PipedreamIntegration()
    
    print("🧘‍♀️ Testing HiYoga Pipedream Integration")
    print("=" * 45)
    
    # Test all workflows
    results = pipedream.test_all_workflows()
    
    print("Workflow Test Results:")
    print("-" * 25)
    
    for workflow, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{workflow:<20} {status}")
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"\nOverall: {passed}/{total} workflows configured")
    
    if passed == total:
        print("🎉 All Pipedream workflows ready!")
    else:
        print("⚠️  Some workflows need configuration")
        print("   Set up the missing workflow IDs in your .env file")
    
    return 0 if passed > 0 else 1

if __name__ == "__main__":
    exit(main())