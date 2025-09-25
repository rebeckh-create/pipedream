#!/usr/bin/env python3
"""
Test suite for Studio Automation System
"""

import pytest
import os
import sys
import tempfile
import shutil
from pathlib import Path
import yaml

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.studio_automation import StudioAutomation

class TestStudioAutomation:
    """Test cases for StudioAutomation class"""
    
    @pytest.fixture
    def temp_config_dir(self):
        """Create temporary configuration directory"""
        temp_dir = tempfile.mkdtemp()
        config_dir = Path(temp_dir) / "config"
        config_dir.mkdir()
        
        # Create test configuration
        test_config = {
            'studio': {'name': 'Test Studio', 'type': 'multi-purpose'},
            'audio': {
                'interface': {
                    'brand': 'test',
                    'model': 'test_interface',
                    'sample_rate': 48000,
                    'buffer_size': 256
                },
                'microphones': [],
                'monitors': []
            },
            'video': {'cameras': [], 'lighting': []},
            'automation': {
                'auto_start_recording': False,
                'auto_backup': False,
                'backup_location': f"{temp_dir}/backups",
                'session_templates': [
                    {
                        'name': 'test_session',
                        'duration': 30,
                        'audio_enabled': True,
                        'video_enabled': False,
                        'lighting_preset': 'bright'
                    }
                ]
            },
            'files': {
                'recording_path': f"{temp_dir}/recordings",
                'export_path': f"{temp_dir}/exports", 
                'temp_path': f"{temp_dir}/temp",
                'naming_convention': "{date}_{session_type}_{timestamp}",
                'formats': {'audio': ['wav'], 'video': ['mp4']}
            }
        }
        
        config_file = config_dir / "studio_config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(test_config, f)
            
        # Create equipment profiles
        equipment_file = config_dir / "equipment_profiles.json"
        with open(equipment_file, 'w') as f:
            f.write('{}')
        
        yield str(config_file)
        
        # Cleanup
        shutil.rmtree(temp_dir)
    
    def test_initialization(self, temp_config_dir):
        """Test studio automation initialization"""
        studio = StudioAutomation(temp_config_dir)
        
        assert studio.config is not None
        assert studio.config['studio']['name'] == 'Test Studio'
        assert not studio.session_active
        assert studio.current_session is None
    
    def test_get_session_templates(self, temp_config_dir):
        """Test getting session templates"""
        studio = StudioAutomation(temp_config_dir)
        templates = studio.get_session_templates()
        
        assert len(templates) == 1
        assert templates[0]['name'] == 'test_session'
        assert templates[0]['duration'] == 30
    
    def test_start_session_success(self, temp_config_dir):
        """Test successful session start"""
        studio = StudioAutomation(temp_config_dir)
        
        success = studio.start_session('test_session')
        
        assert success
        assert studio.session_active
        assert studio.current_session is not None
        assert studio.current_session['template'] == 'test_session'
        assert studio.current_session['duration'] == 30
    
    def test_start_session_invalid_template(self, temp_config_dir):
        """Test session start with invalid template"""
        studio = StudioAutomation(temp_config_dir)
        
        success = studio.start_session('nonexistent_template')
        
        assert not success
        assert not studio.session_active
        assert studio.current_session is None
    
    def test_start_session_already_active(self, temp_config_dir):
        """Test starting session when one is already active"""
        studio = StudioAutomation(temp_config_dir)
        
        # Start first session
        studio.start_session('test_session')
        
        # Try to start another
        success = studio.start_session('test_session')
        
        assert not success
        assert studio.session_active  # First session still active
    
    def test_stop_session_success(self, temp_config_dir):
        """Test successful session stop"""
        studio = StudioAutomation(temp_config_dir)
        
        # Start then stop session
        studio.start_session('test_session')
        success = studio.stop_session()
        
        assert success
        assert not studio.session_active
        assert studio.current_session is None
    
    def test_stop_session_no_active(self, temp_config_dir):
        """Test stopping session when none is active"""
        studio = StudioAutomation(temp_config_dir)
        
        success = studio.stop_session()
        
        assert not success  # Warning case, but not failure
        assert not studio.session_active
    
    def test_get_status(self, temp_config_dir):
        """Test getting system status"""
        studio = StudioAutomation(temp_config_dir)
        
        # Test status without active session
        status = studio.get_status()
        assert not status['session_active']
        assert status['current_session'] is None
        assert status['studio_name'] == 'Test Studio'
        assert 'equipment_connected' in status
        
        # Test status with active session
        studio.start_session('test_session')
        status = studio.get_status()
        assert status['session_active']
        assert status['current_session'] is not None
    
    def test_custom_duration(self, temp_config_dir):
        """Test session with custom duration"""
        studio = StudioAutomation(temp_config_dir)
        
        success = studio.start_session('test_session', custom_duration=60)
        
        assert success
        assert studio.current_session['duration'] == 60
    
    def test_list_recordings_empty(self, temp_config_dir):
        """Test listing recordings when directory is empty"""
        studio = StudioAutomation(temp_config_dir)
        
        recordings = studio.list_recordings()
        
        assert recordings == []
    
    def test_list_recordings_with_files(self, temp_config_dir):
        """Test listing recordings with files present"""
        studio = StudioAutomation(temp_config_dir)
        
        # Create a test recording file
        recording_path = Path(studio.config['files']['recording_path'])
        test_file = recording_path / "test_recording.wav"
        test_file.write_text("test content")
        
        recordings = studio.list_recordings()
        
        assert len(recordings) == 1
        assert recordings[0]['name'] == 'test_recording.wav'
        assert recordings[0]['size'] > 0

class TestConfigurationLoading:
    """Test configuration file loading"""
    
    def test_missing_config_file(self):
        """Test handling of missing configuration file"""
        with pytest.raises(FileNotFoundError):
            StudioAutomation("nonexistent_config.yaml")
    
    def test_invalid_yaml(self):
        """Test handling of invalid YAML configuration"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("invalid: yaml: content: [")
            temp_file = f.name
        
        try:
            with pytest.raises(ValueError):
                StudioAutomation(temp_file)
        finally:
            os.unlink(temp_file)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])