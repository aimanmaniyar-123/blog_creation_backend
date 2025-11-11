@echo off
echo 🚀 Setting up End-to-End Blog Creation Suite...

REM Check Python version
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.10+
    exit /b 1
)

echo ✅ Python found

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📚 Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

REM Create data directories
echo 📁 Creating data directories...
mkdir data\uploads data\output data\logs 2>nul

REM Initialize database
echo 💾 Initializing database...
python -c "from utils.database import init_db; init_db()"

REM Create .env file from template
if not exist .env (
    echo ⚙️ Creating .env file from template...
    copy .env.template .env
    echo 📝 Please edit .env file and add your Pexels API key
)

echo.
echo 🎉 Installation complete!
echo.
echo Next steps:
echo 1. Edit .env file and add your Pexels API key
echo 2. Run: streamlit run main.py
echo 3. Open browser: http://localhost:8501
echo.
echo To get a free Pexels API key:
echo - Visit: https://www.pexels.com/api/
echo - Sign up for free account
echo - Generate API key
echo - Add to .env file
