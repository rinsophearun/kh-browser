#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────
#  build_macos.sh  —  Build KHBrowser.app + .dmg for macOS
# ─────────────────────────────────────────────────────────────────
set -e

APP_NAME="KHBrowser"
VERSION="1.0.0"
DIST_DIR="dist"
DMG_NAME="${APP_NAME}-${VERSION}-macOS.dmg"

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║   KH Browser — macOS Build                  ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# 1. Clean previous build
echo "▶ Cleaning previous build..."
rm -rf build/ dist/ __pycache__/
find . -name "*.pyc" -delete 2>/dev/null || true

# 2. Check dependencies
echo "▶ Installing Python dependencies..."
pip3 install PyQt6 pyinstaller requests cryptography --break-system-packages -q

# 3. Build .app with PyInstaller
echo "▶ Building .app bundle with PyInstaller..."
pyinstaller khbrowser.spec \
    --clean \
    --noconfirm \
    --log-level WARN

echo ""
echo "✅  App built: dist/${APP_NAME}.app"

# 4. Create .dmg installer
echo "▶ Creating .dmg installer..."

DMG_STAGING="dist/dmg_staging"
rm -rf "$DMG_STAGING"
mkdir -p "$DMG_STAGING"
cp -r "dist/${APP_NAME}.app" "$DMG_STAGING/"

# Create DMG using hdiutil
hdiutil create \
    -volname "${APP_NAME} ${VERSION}" \
    -srcfolder "$DMG_STAGING" \
    -ov \
    -format UDZO \
    "dist/${DMG_NAME}" 2>/dev/null

rm -rf "$DMG_STAGING"

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║   BUILD COMPLETE                                     ║"
echo "╠══════════════════════════════════════════════════════╣"
echo "║                                                      ║"
APP_SIZE=$(du -sh "dist/${APP_NAME}.app" 2>/dev/null | cut -f1)
DMG_SIZE=$(du -sh "dist/${DMG_NAME}" 2>/dev/null | cut -f1)
echo "║   .app size : ${APP_SIZE:-???}                                ║"
echo "║   .dmg size : ${DMG_SIZE:-???}                                ║"
echo "║                                                      ║"
echo "║   Output: dist/${DMG_NAME}"
echo "╚══════════════════════════════════════════════════════╝"
echo ""
echo "📦 To install: open dist/${DMG_NAME}"
echo "   Drag KHBrowser.app → Applications folder"
echo ""
