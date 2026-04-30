#!/bin/bash
# Quick macOS build script for KH Browser
# Usage: bash build_quick.sh

set -e  # Exit on error

PROJECT_DIR="/Users/sophearun/Projects/KH browser"
cd "$PROJECT_DIR" || exit 1

echo "════════════════════════════════════════════════════════"
echo "  🍎 KH Browser - macOS Build Script"
echo "════════════════════════════════════════════════════════"
echo ""

# Step 1: Generate icons (if not already done)
if [ ! -f "assets/icon.icns" ]; then
    echo "📦 Step 1: Generating application icons..."
    echo ""
    if python3 generate_icons_advanced.py; then
        echo "✅ Icons generated successfully"
    else
        echo "⚠️  Icon generation had warnings (continuing...)"
    fi
    echo ""
else
    echo "✅ Step 1: Icons already exist (skipping generation)"
    echo ""
fi

# Step 2: Build macOS application
echo "🍎 Step 2: Building macOS application..."
echo ""
if bash build_macos.sh; then
    echo "✅ macOS build successful"
else
    echo "❌ macOS build failed"
    exit 1
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo "  ✅ BUILD COMPLETE"
echo "════════════════════════════════════════════════════════"
echo ""
echo "📦 Output:"
echo "   .app:  $(du -sh dist/KHBrowser.app 2>/dev/null | cut -f1)"
echo "   .dmg:  $(ls -lh dist/KHBrowser-1.0.0-macOS.dmg 2>/dev/null | awk '{print $5}')"
echo ""
echo "🚀 To test:"
echo "   open dist/KHBrowser-1.0.0-macOS.dmg"
echo ""
echo "Or launch directly:"
echo "   open dist/KHBrowser.app"
echo ""
