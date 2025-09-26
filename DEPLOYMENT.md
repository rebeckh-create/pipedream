# 🚀 Studio Automation Deployment Guide

## System Requirements

### **Minimum Requirements**
- **Operating System**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: Python 3.8 or higher (3.9+ recommended)
- **RAM**: 4GB minimum (8GB+ recommended for video processing)
- **Storage**: 10GB free space (more for recordings)
- **Network**: Internet connection for streaming features (optional)

### **Hardware Requirements**
- **Audio Interface**: USB audio interface (Focusrite, Behringer, etc.)
- **Cameras**: USB webcams or DSLR cameras with USB/capture cards
- **Lighting**: Smart lights with API control (optional) or manual lighting

## Installation Methods

### **Method 1: Local Installation (Recommended)**

#### **Step 1: Clone Repository**
```bash
git clone https://github.com/rebeckh-create/pipedream.git
cd pipedream
git checkout cursor/fix-automated-studio-setup-issues-ae02
```

#### **Step 2: Set Up Python Environment**

**On Windows:**
```cmd
# Install Python from python.org if not installed
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**On Mac/Linux:**
```bash
# Install Python 3 if not installed
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### **Step 3: Test Installation**
```bash
python src/studio_automation.py
```

### **Method 2: Docker Installation**

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "src/studio_automation.py"]
```

Run with Docker:
```bash
docker build -t studio-automation .
docker run -p 8000:8000 -v $(pwd)/recordings:/app/recordings studio-automation
```

## Configuration

### **Step 1: Edit Studio Configuration**
Edit `config/studio_config.yaml`:

```yaml
studio:
  name: "Your Studio Name"  # Change this
  type: "multi-purpose"

audio:
  interface:
    brand: "your_brand"      # e.g., "focusrite", "behringer"
    model: "your_model"      # e.g., "scarlett_2i2", "umc202hd"
    sample_rate: 48000
    buffer_size: 256
```

### **Step 2: Configure Your Equipment**
Update the following sections with your actual equipment:
- **Audio**: Your audio interface, microphones, monitors
- **Video**: Your cameras and specifications
- **Lighting**: Your lighting setup and control methods

### **Step 3: Set File Paths**
Update file paths in the config:
```yaml
files:
  recording_path: "/path/to/your/recordings"  # Change these paths
  export_path: "/path/to/your/exports"
  temp_path: "/path/to/temp"
```

## Running the System

### **Basic Commands**
```bash
# Check system status
python scripts/studio_status.py

# Start a yoga class session
python scripts/start_session.py yoga_class

# Start meditation with custom duration
python scripts/start_session.py meditation --duration 45

# Stop current session
python scripts/stop_session.py
```

### **Advanced Usage**
```bash
# Use custom config file
python scripts/start_session.py yoga_class --config /path/to/custom_config.yaml

# Get JSON output for integrations
python scripts/studio_status.py --json
```

## Hardware Integration

### **Audio Equipment**
For real audio control, install additional packages:
```bash
pip install pyaudio soundfile numpy
```

Common audio interfaces supported:
- Focusrite Scarlett series
- Behringer UMC series  
- PreSonus AudioBox series
- Any ASIO-compatible interface

### **Video Equipment**
For camera control:
```bash
pip install opencv-python ffmpeg-python
```

Supported cameras:
- USB webcams (Logitech, etc.)
- DSLR cameras with USB tethering
- HDMI capture devices
- IP cameras with RTSP streams

### **Lighting Control**
For smart lighting:
```bash
pip install requests websockets pyserial
```

Supported lighting systems:
- Philips Hue
- LIFX
- DMX-controlled lights
- Serial-controlled LED panels

## Automation Features

### **Session Templates**
Built-in templates:
- **yoga_class**: 60min, audio+video, warm lighting
- **meditation**: 30min, audio-only, dim lighting  
- **workshop**: 120min, full recording, bright lighting

### **Custom Templates**
Add to `config/studio_config.yaml`:
```yaml
automation:
  session_templates:
    - name: "my_custom_session"
      duration: 90
      audio_enabled: true
      video_enabled: true
      lighting_preset: "custom"
```

## Production Setup

### **Running as a Service (Linux)**
Create `/etc/systemd/system/studio-automation.service`:
```ini
[Unit]
Description=Studio Automation Service
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/studio-automation
ExecStart=/path/to/venv/bin/python src/studio_automation.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable the service:
```bash
sudo systemctl enable studio-automation
sudo systemctl start studio-automation
```

### **Running as Windows Service**
Use `nssm` (Non-Sucking Service Manager):
```cmd
nssm install StudioAutomation
nssm set StudioAutomation Application C:\path\to\python.exe
nssm set StudioAutomation AppParameters C:\path\to\src\studio_automation.py
nssm start StudioAutomation
```

## Troubleshooting

### **Common Issues**

#### **"Configuration file not found"**
```bash
# Ensure you're in the correct directory
pwd
ls config/studio_config.yaml
```

#### **"Python module not found"**
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### **"Permission denied" errors**
```bash
# Fix directory permissions
chmod -R 755 recordings/ exports/ temp/ logs/
```

#### **Audio interface not detected**
- Check USB connections
- Install manufacturer drivers
- Verify device in system audio settings
- Check `config/equipment_profiles.json` for your device

### **Logging**
Check logs for detailed error information:
```bash
tail -f logs/studio_$(date +%Y%m%d).log
```

### **Testing Hardware**
Test individual components:
```bash
# Test audio
python -c "import pyaudio; print('Audio OK')"

# Test video  
python -c "import cv2; print('Video OK')"

# Test configuration
python -c "from src.studio_automation import StudioAutomation; s=StudioAutomation(); print('Config OK')"
```

## Performance Optimization

### **For Better Performance**
- Use SSD storage for recordings
- Increase buffer sizes for audio
- Close unnecessary applications during recording
- Use wired network connections for streaming

### **Resource Monitoring**
```bash
# Monitor system resources
htop  # Linux/Mac
# or use Task Manager on Windows
```

## Security Considerations

### **Network Security**
- Use firewall rules to restrict access
- Change default passwords on network devices
- Use VPN for remote access

### **File Security**
- Set appropriate file permissions
- Use encrypted storage for sensitive recordings
- Regular backups to secure locations

## Backup Strategy

### **Automated Backups**
The system includes auto-backup features. Configure in `studio_config.yaml`:
```yaml
automation:
  auto_backup: true
  backup_location: "/path/to/backup/drive"
```

### **Manual Backups**
```bash
# Backup recordings
rsync -av recordings/ /backup/location/recordings/

# Backup configuration
cp -r config/ /backup/location/config/
```

## Integration with Other Systems

### **Streaming Platforms**
Configure streaming in `studio_config.yaml`:
```yaml
streaming:
  enabled: true
  platforms:
    - name: "youtube"
      stream_key: "your_stream_key"
    - name: "twitch"
      stream_key: "your_stream_key"
```

### **Calendar Integration**
The system can be extended to integrate with calendar systems for automated session scheduling.

### **Web Interface**
Consider adding a web interface using Flask or FastAPI for remote control.

## Support and Maintenance

### **Regular Maintenance**
- Update dependencies monthly
- Clean old log files
- Check disk space for recordings
- Test backup systems

### **Updates**
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade
```

## Getting Help

1. Check the logs first: `logs/studio_YYYYMMDD.log`
2. Verify configuration: `python src/studio_automation.py`
3. Test individual components
4. Check GitHub issues for similar problems
5. Create detailed bug reports with logs and system info