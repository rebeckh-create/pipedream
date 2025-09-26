@echo off
REM Studio Automation Quick Install Script for Windows

echo 🎬 Studio Automation System - Quick Install
echo ===========================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    echo    Visit: https://python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Found Python %PYTHON_VERSION%

REM Create virtual environment
echo 📦 Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)
echo ✅ Dependencies installed successfully

REM Create necessary directories
echo 📁 Creating directories...
mkdir recordings 2>nul
mkdir exports 2>nul
mkdir temp 2>nul
mkdir backups 2>nul
mkdir logs 2>nul
echo ✅ Directories created

REM Test installation
echo 🧪 Testing installation...
python src\studio_automation.py >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Installation test failed
    echo    Try running: python src\studio_automation.py
    pause
    exit /b 1
)
echo ✅ Installation test passed

echo.
echo 🎉 Installation Complete!
echo ========================
echo.
echo Next steps:
echo 1. Edit config\studio_config.yaml with your equipment
echo 2. Test with: python scripts\studio_status.py
echo 3. Start a session: python scripts\start_session.py yoga_class
echo.
echo For detailed setup instructions, see DEPLOYMENT.md
echo.
echo Quick commands:
echo   Status:  python scripts\studio_status.py
echo   Start:   python scripts\start_session.py [template]
echo   Stop:    python scripts\stop_session.py
echo.
pause