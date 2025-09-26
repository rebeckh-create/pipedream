#!/bin/bash
# Studio Automation Quick Install Script

echo "🎬 Studio Automation System - Quick Install"
echo "==========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    echo "   Visit: https://python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Found Python $PYTHON_VERSION"

# Check Python version
if python3 -c 'import sys; exit(0 if sys.version_info >= (3, 8) else 1)'; then
    echo "✅ Python version is compatible"
else
    echo "❌ Python 3.8+ required. Current version: $PYTHON_VERSION"
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p recordings exports temp backups logs
echo "✅ Directories created"

# Test installation
echo "🧪 Testing installation..."
if python3 src/studio_automation.py > /dev/null 2>&1; then
    echo "✅ Installation test passed"
else
    echo "❌ Installation test failed"
    echo "   Try running: python3 src/studio_automation.py"
    exit 1
fi

echo ""
echo "🎉 Installation Complete!"
echo "========================"
echo ""
echo "Next steps:"
echo "1. Edit config/studio_config.yaml with your equipment"
echo "2. Test with: python3 scripts/studio_status.py"
echo "3. Start a session: python3 scripts/start_session.py yoga_class"
echo ""
echo "For detailed setup instructions, see DEPLOYMENT.md"
echo ""
echo "Quick commands:"
echo "  Status:  python3 scripts/studio_status.py"
echo "  Start:   python3 scripts/start_session.py [template]"
echo "  Stop:    python3 scripts/stop_session.py"
echo ""