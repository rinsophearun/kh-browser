#!/bin/bash
# Generate all app icons for macOS and Windows

set -e

cd "$(dirname "$0")" || exit 1

echo "🎨 Generating app icons for macOS and Windows..."
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found"
    exit 1
fi

# Check Pillow
python3 -c "import PIL" 2>/dev/null || {
    echo "📦 Installing Pillow..."
    pip3 install Pillow
}

# Run icon generator
python3 generate_icons.py

echo ""
echo "✅ Icons ready for build!"
