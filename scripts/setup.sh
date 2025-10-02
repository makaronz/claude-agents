#!/bin/bash

# Setup script for Claude Agents repository

set -e

echo "🤖 Claude Agents Setup"
echo "====================="

# Check Python version
echo "Checking Python version..."
python3 -c "import sys; assert sys.version_info >= (3, 8), 'Python 3.8+ required'" || {
    echo "❌ Python 3.8 or higher is required"
    exit 1
}
echo "✅ Python version OK"

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created from template"
    echo "⚠️  Please edit .env and add your Anthropic API key"
else
    echo "✅ .env file already exists"
fi

# Create logs directory
mkdir -p logs
echo "✅ Logs directory created"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your Anthropic API key"
echo "2. Create your first agent:"
echo "   cp -r agents/agent-template agents/my-first-agent"
echo "3. Run your agent:"
echo "   cd agents/my-first-agent && python agent.py"
echo ""
echo "For more information, see docs/getting-started.md"