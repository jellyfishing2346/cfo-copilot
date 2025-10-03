#!/bin/bash
# CFO Copilot Setup Script

echo "🏦 Setting up CFO Copilot..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "⬇️  Installing dependencies..."
pip install -r requirements.txt

# Run tests
echo "🧪 Running tests..."
python run_tests.py

if [ $? -eq 0 ]; then
    echo "✅ Setup completed successfully!"
    echo ""
    echo "🚀 To start the CFO Copilot:"
    echo "   source venv/bin/activate"
    echo "   streamlit run app.py"
    echo ""
    echo "📊 For a quick demo:"
    echo "   python simple_demo.py"
else
    echo "❌ Setup failed. Please check the errors above."
    exit 1
fi
