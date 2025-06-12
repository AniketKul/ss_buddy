#!/bin/bash

# Study Buddy Assistant Setup Script
echo "🎓 Setting up Study Buddy Assistant..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️ Creating .env file..."
    cp .env.example .env
    echo ""
    echo "🔑 IMPORTANT: Please edit .env file and add your NVIDIA API key:"
    echo "   1. Go to https://build.nvidia.com/explore/discover"
    echo "   2. Sign up/login and get your API key"
    echo "   3. Copy the key and paste it in .env file as NVIDIA_API_KEY=your-key-here"
    echo ""
    echo "📝 Edit .env file now? (y/n)"
    read -r edit_env
    if [ "$edit_env" = "y" ] || [ "$edit_env" = "Y" ]; then
        ${EDITOR:-nano} .env
    fi
else
    echo "✅ .env file already exists"
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p static/uploads

# Set permissions
chmod +x study_buddy_app.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To start the application:"
echo "   1. Activate virtual environment: source venv/bin/activate"
echo "   2. Make sure you've added your NVIDIA API key to .env"
echo "   3. Run: python study_buddy_app.py"
echo ""
echo "🌐 The app will be available at: http://localhost:5000"
echo ""
echo "📖 For deployment instructions, see DEPLOYMENT.md" 