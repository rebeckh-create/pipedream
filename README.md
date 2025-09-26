# HiYoga Studio Automation System

A comprehensive automation system for managing studio recording sessions, equipment control, and workflow optimization.

## Features

- **Session Templates**: Pre-configured session types (yoga classes, meditation, workshops)
- **Equipment Control**: Automated audio, video, and lighting setup
- **Recording Management**: Automated recording start/stop with file organization
- **Backup System**: Automatic session backup to specified locations
- **Status Monitoring**: Real-time equipment and session status
- **Flexible Configuration**: YAML-based configuration for easy customization

## Project Structure

```
/workspace/
├── src/                    # Main source code
│   └── studio_automation.py
├── config/                 # Configuration files
│   ├── studio_config.yaml
│   └── equipment_profiles.json
├── scripts/                # Utility scripts
│   ├── start_session.py
│   ├── stop_session.py
│   └── studio_status.py
├── tests/                  # Test files
├── logs/                   # Log files
├── recordings/             # Recording output
├── exports/                # Exported files
├── temp/                   # Temporary files
└── backups/                # Backup location
```

## Installation

1. **Clone and Setup**:
   ```bash
   cd /workspace
   pip install -r requirements.txt
   ```

2. **Install Optional Dependencies** (based on your equipment):
   ```bash
   # For audio processing
   pip install pyaudio soundfile numpy
   
   # For video processing
   pip install opencv-python ffmpeg-python
   
   # For hardware control
   pip install pyserial requests websockets
   ```

3. **Configure Your Studio**:
   - Edit `config/studio_config.yaml` with your equipment details
   - Update `config/equipment_profiles.json` if using different hardware

## Configuration

### Studio Configuration (`config/studio_config.yaml`)

The main configuration file contains:

- **Studio Info**: Name and type
- **Audio Setup**: Interface, microphones, monitors
- **Video Setup**: Cameras, lighting equipment  
- **Automation**: Session templates, backup settings
- **File Management**: Recording paths, naming conventions

### Equipment Profiles (`config/equipment_profiles.json`)

Defines supported equipment with technical specifications for:
- Audio interfaces (sample rates, bit depths, latency)
- Cameras (resolutions, frame rates, connection types)
- Lighting (power, color temperature, control options)

## Usage

### Starting a Session

```bash
# Start with a template
python scripts/start_session.py yoga_class

# Start with custom duration
python scripts/start_session.py meditation --duration 45

# Using different config file
python scripts/start_session.py workshop --config /path/to/config.yaml
```

### Checking Status

```bash
# Human-readable status
python scripts/studio_status.py

# JSON output for integration
python scripts/studio_status.py --json
```

### Stopping a Session

```bash
python scripts/stop_session.py
```

### Programmatic Usage

```python
from src.studio_automation import StudioAutomation

# Initialize
studio = StudioAutomation()

# Start a session
studio.start_session('yoga_class', custom_duration=75)

# Check status
status = studio.get_status()
print(f"Active: {status['session_active']}")

# Stop session
studio.stop_session()

# List recordings
recordings = studio.list_recordings()
```

## Session Templates

### Built-in Templates

1. **yoga_class**: 60-minute sessions with audio/video, warm lighting
2. **meditation**: 30-minute audio-only sessions with dim lighting  
3. **workshop**: 120-minute sessions with full recording and bright lighting

### Custom Templates

Add new templates to `config/studio_config.yaml`:

```yaml
automation:
  session_templates:
    - name: "custom_session"
      duration: 90
      audio_enabled: true
      video_enabled: true
      lighting_preset: "bright"
```

## Equipment Integration

### Audio Interfaces
- Focusrite Scarlett series
- Behringer UMC series
- Custom ASIO drivers supported

### Cameras
- DSLR cameras (Canon, Nikon, Sony)
- USB webcams (Logitech, etc.)
- HDMI capture devices

### Lighting
- LED panels with DMX control
- Smart bulbs with API control
- Manual lighting with presets

## Automation Features

### Auto-Start Recording
Set `auto_start_recording: true` to begin recording immediately when a session starts.

### Auto-Backup
Enable `auto_backup: true` to automatically copy recordings to backup location after each session.

### File Naming
Customize file naming with variables:
- `{date}`: Current date (YYYYMMDD)
- `{session_type}`: Template name
- `{timestamp}`: Time (HHMMSS)

Example: `20250925_yoga_class_143022.wav`

## Troubleshooting

### Common Issues

1. **Configuration File Not Found**:
   ```
   FileNotFoundError: Configuration file not found
   ```
   - Ensure `config/studio_config.yaml` exists
   - Check file path and permissions

2. **Equipment Not Detected**:
   ```
   Equipment connection failed
   ```
   - Verify hardware connections
   - Check driver installation
   - Review equipment profiles

3. **Permission Errors**:
   ```
   PermissionError: Cannot create directory
   ```
   - Check directory permissions
   - Ensure write access to recording paths

### Logs

Check log files in the `logs/` directory:
```bash
tail -f logs/studio_$(date +%Y%m%d).log
```

### Testing Setup

```bash
# Test basic functionality
python -m pytest tests/

# Test with your configuration
python src/studio_automation.py
```

## Development

### Adding New Equipment

1. Add equipment profile to `config/equipment_profiles.json`
2. Implement control methods in `StudioAutomation` class
3. Update configuration schema in `config/studio_config.yaml`

### Custom Session Logic

Override session methods in `StudioAutomation`:

```python
class CustomStudioAutomation(StudioAutomation):
    def _setup_custom_equipment(self):
        # Your custom setup logic
        pass
```

### Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review log files in `logs/`
3. Verify configuration files
4. Test with minimal setup first

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request