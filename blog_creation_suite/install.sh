#!/bin/bash
# Installation script for Blog Creation Suite

echo "🚀 Setting up End-to-End Blog Creation Suite..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.10"

if ! python3 -c "import sys; assert sys.version_info >= (3,10)" 2>/dev/null; then
    echo "❌ Python 3.10+ required. Current version: $python_version"
    exit 1
fi

echo "✅ Python version check passed"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create data directories
echo "📁 Creating data directories..."
mkdir -p data/uploads data/output data/logs

# Initialize database
echo "💾 Initializing database..."
python -c "from utils.database import init_db; init_db()"

# Create .env file from template
if [ ! -f .env ]; then
    echo "⚙️ Creating .env file from template..."
    cp .env.template .env
    echo "📝 Please edit .env file and add your Pexels API key"
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your Pexels API key"
echo "2. Run: streamlit run main.py"
echo "3. Open browser: http://localhost:8501"
echo ""
echo "To get a free Pexels API key:"
echo "- Visit: https://www.pexels.com/api/"
echo "- Sign up for free account"
echo "- Generate API key"
echo "- Add to .env file"
