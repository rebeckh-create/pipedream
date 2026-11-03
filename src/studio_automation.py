#!/usr/bin/env python3
"""
Studio Automation System
Main module for controlling studio equipment and recording sessions
"""

import os
import yaml
import json
import logging
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import subprocess
import time

class StudioAutomation:
    """Main class for studio automation control"""
    
    def __init__(self, config_path: str = "config/studio_config.yaml"):
        """Initialize the studio automation system"""
        self.config_path = config_path
        self.config = self._load_config()
        self.equipment_profiles = self._load_equipment_profiles()
        self.session_active = False
        self.current_session = None
        self._setup_logging()
        self._create_directories()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load studio configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing configuration file: {e}")
    
    def _load_equipment_profiles(self) -> Dict[str, Any]:
        """Load equipment profiles from JSON file"""
        try:
            with open("config/equipment_profiles.json", 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.warning("Equipment profiles file not found")
            return {}
    
    def _setup_logging(self):
        """Setup logging configuration"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f"logs/studio_{datetime.datetime.now().strftime('%Y%m%d')}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("Studio automation system initialized")
    
    def _create_directories(self):
        """Create necessary directories for recordings and exports"""
        directories = [
            self.config['files']['recording_path'],
            self.config['files']['export_path'], 
            self.config['files']['temp_path']
        ]
        
        if self.config['automation']['auto_backup']:
            directories.append(self.config['automation']['backup_location'])
            
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            
    def get_session_templates(self) -> List[Dict[str, Any]]:
        """Get available session templates"""
        return self.config['automation']['session_templates']
    
    def start_session(self, template_name: str, custom_duration: Optional[int] = None) -> bool:
        """Start a recording session with specified template"""
        if self.session_active:
            self.logger.error("Session already active. Stop current session first.")
            return False
            
        # Find the template
        template = None
        for t in self.config['automation']['session_templates']:
            if t['name'] == template_name:
                template = t
                break
                
        if not template:
            self.logger.error(f"Template '{template_name}' not found")
            return False
            
        self.logger.info(f"Starting session with template: {template_name}")
        
        # Create session object
        session_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        duration = custom_duration if custom_duration else template['duration']
        
        self.current_session = {
            'id': session_id,
            'template': template_name,
            'duration': duration,
            'start_time': datetime.datetime.now(),
            'audio_enabled': template['audio_enabled'],
            'video_enabled': template['video_enabled'],
            'lighting_preset': template['lighting_preset']
        }
        
        # Setup equipment based on template
        if template['lighting_preset']:
            self._set_lighting_preset(template['lighting_preset'])
            
        if template['audio_enabled']:
            self._setup_audio_recording()
            
        if template['video_enabled']:
            self._setup_video_recording()
            
        self.session_active = True
        self.logger.info(f"Session {session_id} started successfully")
        return True
    
    def stop_session(self) -> bool:
        """Stop the current recording session"""
        if not self.session_active:
            self.logger.warning("No active session to stop")
            return False
            
        self.logger.info(f"Stopping session {self.current_session['id']}")
        
        # Stop recording processes
        self._stop_audio_recording()
        self._stop_video_recording()
        
        # Calculate session duration
        end_time = datetime.datetime.now()
        actual_duration = (end_time - self.current_session['start_time']).total_seconds() / 60
        
        self.logger.info(f"Session completed. Planned: {self.current_session['duration']}min, Actual: {actual_duration:.1f}min")
        
        # Auto backup if enabled
        if self.config['automation']['auto_backup']:
            self._backup_session()
            
        self.session_active = False
        self.current_session = None
        return True
    
    def _set_lighting_preset(self, preset: str):
        """Set lighting based on preset"""
        self.logger.info(f"Setting lighting preset: {preset}")
        
        # This would integrate with actual lighting control hardware
        # For now, we'll just log the action
        lighting_settings = {
            'warm': {'brightness': 70, 'color_temp': 3200},
            'bright': {'brightness': 100, 'color_temp': 5600},
            'dim': {'brightness': 30, 'color_temp': 2700}
        }
        
        if preset in lighting_settings:
            settings = lighting_settings[preset]
            self.logger.info(f"Lighting set to {settings['brightness']}% brightness, {settings['color_temp']}K")
        else:
            self.logger.warning(f"Unknown lighting preset: {preset}")
    
    def _setup_audio_recording(self):
        """Setup audio recording"""
        self.logger.info("Setting up audio recording")
        
        audio_config = self.config['audio']
        interface = audio_config['interface']
        
        # This would integrate with actual audio interface
        # For demonstration, we'll create a placeholder script
        self.logger.info(f"Audio interface: {interface['brand']} {interface['model']}")
        self.logger.info(f"Sample rate: {interface['sample_rate']}Hz, Buffer: {interface['buffer_size']}")
    
    def _setup_video_recording(self):
        """Setup video recording"""
        self.logger.info("Setting up video recording")
        
        video_config = self.config['video']
        cameras = video_config['cameras']
        
        for camera in cameras:
            self.logger.info(f"Camera: {camera['name']} ({camera['resolution']}@{camera['fps']}fps)")
    
    def _stop_audio_recording(self):
        """Stop audio recording"""
        self.logger.info("Stopping audio recording")
        # Implementation would stop actual recording processes
    
    def _stop_video_recording(self):
        """Stop video recording"""  
        self.logger.info("Stopping video recording")
        # Implementation would stop actual recording processes
    
    def _backup_session(self):
        """Backup session files"""
        if not self.current_session:
            return
            
        backup_dir = Path(self.config['automation']['backup_location']) / self.current_session['id']
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.info(f"Backing up session to {backup_dir}")
        # Implementation would copy recording files to backup location
    
    def get_status(self) -> Dict[str, Any]:
        """Get current system status"""
        status = {
            'session_active': self.session_active,
            'current_session': self.current_session,
            'studio_name': self.config['studio']['name'],
            'equipment_connected': self._check_equipment_status()
        }
        return status
    
    def _check_equipment_status(self) -> Dict[str, bool]:
        """Check if equipment is connected and ready"""
        # This would check actual hardware connections
        return {
            'audio_interface': True,  # Placeholder
            'cameras': True,         # Placeholder  
            'lighting': True         # Placeholder
        }
    
    def list_recordings(self) -> List[Dict[str, Any]]:
        """List all recordings in the recording directory"""
        recording_path = Path(self.config['files']['recording_path'])
        recordings = []
        
        for file_path in recording_path.glob("*"):
            if file_path.is_file():
                stat = file_path.stat()
                recordings.append({
                    'name': file_path.name,
                    'size': stat.st_size,
                    'created': datetime.datetime.fromtimestamp(stat.st_ctime),
                    'modified': datetime.datetime.fromtimestamp(stat.st_mtime)
                })
                
        return sorted(recordings, key=lambda x: x['modified'], reverse=True)

def main():
    """Main entry point for the studio automation system"""
    try:
        studio = StudioAutomation()
        
        # Example usage
        print("Studio Automation System")
        print(f"Studio: {studio.config['studio']['name']}")
        print("\nAvailable session templates:")
        for template in studio.get_session_templates():
            print(f"- {template['name']}: {template['duration']}min")
            
        print(f"\nSystem Status: {studio.get_status()}")
        
    except Exception as e:
        print(f"Error initializing studio automation: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())