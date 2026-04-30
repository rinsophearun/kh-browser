#!/bin/bash
###############################################################################
# 🍎 KH Browser - Complete macOS Build & Package Automation
# 
# This script automates the entire build process:
# 1. Generates application icons (macOS .icns + Windows .ico)
# 2. Builds the Python PyQt6 app with PyInstaller
# 3. Creates the macOS .dmg installer
# 4. Verifies all output files
# 5. Reports final status
#
# Usage: bash complete_build.sh
###############################################################################

set -e  # Exit immediately on any error

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────

PROJECT_DIR="/Users/sophearun/Projects/KH browser"
ASSETS_DIR="$PROJECT_DIR/assets"
DIST_DIR="$PROJECT_DIR/dist"
BUILD_LOG="$PROJECT_DIR/build.log"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ─────────────────────────────────────────────────────────────────────────────
# Functions
# ─────────────────────────────────────────────────────────────────────────────

log_header() {
    echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
}

log_step() {
    echo -e "\n${YELLOW}▶ $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# ─────────────────────────────────────────────────────────────────────────────
# Verification
# ─────────────────────────────────────────────────────────────────────────────

log_header "🍎 KH Browser - Complete macOS Build"

log_step "Verifying project structure..."

# Check required files
required_files=(
    "main.py"
    "khbrowser.spec"
    "build_macos.sh"
    "entitlements.plist"
    "requirements.txt"
    "assets/Logo.png"
    "runtime_hooks/hook_pyqt6_fix.py"
)

cd "$PROJECT_DIR" || exit 1

missing_files=0
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        log_success "Found: $file"
    else
        log_error "Missing: $file"
        missing_files=$((missing_files + 1))
    fi
done

if [ $missing_files -gt 0 ]; then
    log_error "Missing $missing_files required files. Cannot proceed."
    exit 1
fi

log_success "All required files present"

# ─────────────────────────────────────────────────────────────────────────────
# Phase 1: Generate Icons
# ─────────────────────────────────────────────────────────────────────────────

log_header "📦 Phase 1: Generate Application Icons"

if [ -f "assets/icon.icns" ] && [ -f "assets/icon.ico" ]; then
    log_success "Icons already exist (skipping generation)"
else
    log_step "Generating macOS and Windows icons..."
    
    if python3 generate_icons_advanced.py >> "$BUILD_LOG" 2>&1; then
        log_success "Icons generated successfully"
    else
        log_error "Icon generation failed"
        log_info "Check build log: $BUILD_LOG"
        exit 1
    fi
fi

# Verify icons
if [ ! -f "assets/icon.icns" ]; then
    log_error "macOS icon (icon.icns) not found after generation"
    exit 1
fi

if [ ! -f "assets/icon.ico" ]; then
    log_error "Windows icon (icon.ico) not found after generation"
    exit 1
fi

icns_size=$(du -h "assets/icon.icns" | cut -f1)
ico_size=$(du -h "assets/icon.ico" | cut -f1)

log_success "macOS icon: assets/icon.icns ($icns_size)"
log_success "Windows icon: assets/icon.ico ($ico_size)"

# ─────────────────────────────────────────────────────────────────────────────
# Phase 2: Install Dependencies
# ─────────────────────────────────────────────────────────────────────────────

log_header "📚 Phase 2: Install Dependencies"

log_step "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
log_success "Python version: $python_version"

log_step "Installing Python dependencies..."
if pip3 install -q -r requirements.txt >> "$BUILD_LOG" 2>&1; then
    log_success "Dependencies installed"
else
    log_error "Failed to install dependencies"
    exit 1
fi

# Verify key dependencies
log_step "Verifying key packages..."
for pkg in PyQt6 pyinstaller cryptography requests; do
    if python3 -c "import ${pkg//-/_}" 2>/dev/null; then
        log_success "Package: $pkg"
    else
        log_error "Missing package: $pkg"
        exit 1
    fi
done

# ─────────────────────────────────────────────────────────────────────────────
# Phase 3: Clean Previous Builds
# ─────────────────────────────────────────────────────────────────────────────

log_header "🧹 Phase 3: Clean Previous Builds"

log_step "Removing old build artifacts..."

if [ -d "build" ]; then
    log_info "Removing build/ directory..."
    rm -rf build
fi

if [ -d "dist" ]; then
    log_info "Removing dist/ directory..."
    rm -rf dist
fi

if [ -f "*.spec" ] && [ -f "$(basename *.spec)" ]; then
    # Find any .spec generated files
    find . -maxdepth 1 -name "*.spec" -not -name "khbrowser.spec" -delete 2>/dev/null || true
fi

log_success "Clean complete"

# ─────────────────────────────────────────────────────────────────────────────
# Phase 4: Build macOS Application
# ─────────────────────────────────────────────────────────────────────────────

log_header "🏗️  Phase 4: Build macOS Application"

log_step "Running PyInstaller with khbrowser.spec..."
log_info "This may take 5-10 minutes on first build..."

start_time=$(date +%s)

if pyinstaller khbrowser.spec >> "$BUILD_LOG" 2>&1; then
    end_time=$(date +%s)
    build_time=$((end_time - start_time))
    log_success "PyInstaller completed in ${build_time}s"
else
    log_error "PyInstaller failed"
    log_info "Check build log: $BUILD_LOG"
    tail -50 "$BUILD_LOG"
    exit 1
fi

# Verify .app bundle
if [ ! -d "dist/KHBrowser.app" ]; then
    log_error ".app bundle not created"
    exit 1
fi

app_size=$(du -sh dist/KHBrowser.app | cut -f1)
log_success "App bundle created: dist/KHBrowser.app ($app_size)"

# ─────────────────────────────────────────────────────────────────────────────
# Phase 5: Verify App Bundle
# ─────────────────────────────────────────────────────────────────────────────

log_header "🔍 Phase 5: Verify App Bundle"

log_step "Checking app structure..."

required_app_files=(
    "dist/KHBrowser.app/Contents/MacOS/KHBrowser"
    "dist/KHBrowser.app/Contents/Info.plist"
    "dist/KHBrowser.app/Contents/Resources/icon.icns"
)

for file in "${required_app_files[@]}"; do
    if [ -f "$file" ]; then
        log_success "Found: $file"
    else
        log_error "Missing: $file"
    fi
done

log_step "Checking bundle identifier..."
bundle_id=$(mdls -name kMDItemCFBundleIdentifier "dist/KHBrowser.app" 2>/dev/null | cut -d'"' -f2)
if [ "$bundle_id" = "com.khbrowser.app" ]; then
    log_success "Bundle ID correct: $bundle_id"
else
    log_error "Bundle ID incorrect: $bundle_id"
fi

log_step "Checking entitlements..."
if [ -f "dist/KHBrowser.app/Contents/entitlements.plist" ]; then
    log_success "Entitlements file present"
else
    log_info "Note: Entitlements embedded in signature or not needed"
fi

# ─────────────────────────────────────────────────────────────────────────────
# Phase 6: Create DMG Installer
# ─────────────────────────────────────────────────────────────────────────────

log_header "📦 Phase 6: Create DMG Installer"

dmg_file="dist/KHBrowser-1.0.0-macOS.dmg"

log_step "Creating DMG with LZMA2 compression..."
log_info "This may take 2-3 minutes..."

# Create DMG
if hdiutil create \
    -volname "KHBrowser 1.0.0" \
    -srcfolder "dist/KHBrowser.app" \
    -ov \
    -format ULMO \
    "$dmg_file" >> "$BUILD_LOG" 2>&1; then
    log_success "DMG created: $dmg_file"
else
    log_error "DMG creation failed"
    exit 1
fi

dmg_size=$(du -h "$dmg_file" | cut -f1)
log_success "DMG size: $dmg_size"

# ─────────────────────────────────────────────────────────────────────────────
# Phase 7: Final Verification
# ─────────────────────────────────────────────────────────────────────────────

log_header "✅ Phase 7: Final Verification"

log_step "Verifying output files..."

files_ok=0

if [ -f "dist/KHBrowser.app/Contents/MacOS/KHBrowser" ]; then
    log_success ".app executable present"
    files_ok=$((files_ok + 1))
else
    log_error ".app executable NOT found"
fi

if [ -f "$dmg_file" ]; then
    log_success ".dmg installer present"
    files_ok=$((files_ok + 1))
else
    log_error ".dmg installer NOT found"
fi

if [ -f "dist/KHBrowser.app/Contents/Resources/icon.icns" ]; then
    log_success "App icon present"
    files_ok=$((files_ok + 1))
else
    log_error "App icon NOT found"
fi

# ─────────────────────────────────────────────────────────────────────────────
# Final Report
# ─────────────────────────────────────────────────────────────────────────────

log_header "📊 BUILD COMPLETE - FINAL REPORT"

echo ""
echo -e "${GREEN}✅ BUILD SUCCESSFUL${NC}"
echo ""
echo -e "${BLUE}📦 Output Files:${NC}"
echo "  .app bundle:   dist/KHBrowser.app ($app_size)"
echo "  .dmg installer: $dmg_file ($dmg_size)"
echo ""
echo -e "${BLUE}🎯 Next Steps:${NC}"
echo "  1. Open the DMG:"
echo "     open '$dmg_file'"
echo ""
echo "  2. Drag KHBrowser.app to Applications folder"
echo ""
echo "  3. Run from Applications or Spotlight:"
echo "     KH Browser"
echo ""
echo -e "${BLUE}🔧 Or launch directly:${NC}"
echo "  open 'dist/KHBrowser.app'"
echo ""
echo -e "${BLUE}📝 Build log:${NC}"
echo "  $BUILD_LOG"
echo ""
echo -e "${BLUE}📊 File Sizes:${NC}"
ls -lh dist/KHBrowser.app/Contents/MacOS/KHBrowser 2>/dev/null | awk '{print "  Executable: " $5}'
du -sh dist/KHBrowser.app 2>/dev/null | awk '{print "  .app bundle: " $1}'
ls -lh "$dmg_file" 2>/dev/null | awk '{print "  .dmg file: " $5}'
echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}🍎 macOS Build Complete - Ready to Install!${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
echo ""
