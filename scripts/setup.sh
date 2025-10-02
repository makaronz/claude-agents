#!/bin/bash

# Setup script for Claude Agents repository using Claude Agent SDK

set -e

echo "🤖 Claude Agents Setup (Claude Agent SDK)"
echo "=========================================="

# Check Python version
echo "Checking Python version..."
python3 -c "import sys; assert sys.version_info >= (3, 10), 'Python 3.10+ required'" || {
    echo "❌ Python 3.10 or higher is required for Claude Agent SDK"
    exit 1
}
echo "✅ Python version OK"

# Check Node.js for Claude Code CLI
echo "Checking Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -ge 18 ]; then
        echo "✅ Node.js version OK: $(node --version)"
    else
        echo "⚠️  Node.js version $(node --version) detected. Node.js 18+ recommended."
    fi
else
    echo "⚠️  Node.js not found. Please install Node.js to use Claude Code CLI."
    echo "   Visit: https://nodejs.org/"
fi

# Check/Install Claude Code CLI
echo "Checking Claude Code CLI..."
if command -v claude-code &> /dev/null; then
    echo "✅ Claude Code CLI already installed: $(claude-code --version)"
else
    echo "Installing Claude Code CLI..."
    if command -v npm &> /dev/null; then
        npm install -g @anthropic-ai/claude-code
        echo "✅ Claude Code CLI installed"
    else
        echo "⚠️  npm not found. Please install Node.js and npm, then run:"
        echo "   npm install -g @anthropic-ai/claude-code"
    fi
fi

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
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Python dependencies installed"

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
echo "1. Edit .env and add your ANTHROPIC_API_KEY"
echo "2. Try the example agent:"
echo "   cd agents/example-agent && python agent.py"
echo "3. Create your first custom agent:"
echo "   cp -r agents/agent-template agents/my-first-agent"
echo "   cd agents/my-first-agent && python agent.py"
echo ""
echo "📚 Documentation:"
echo "• Getting Started: docs/getting-started.md"
echo "• Agent Development: docs/agent-guide.md"
echo "• Claude Agent SDK: https://docs.anthropic.com/en/docs/claude-code/sdk/sdk-python"