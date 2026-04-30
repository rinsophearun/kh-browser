# 🍎 macOS Build Quick Guide - KH Browser

## ✅ Verification Checklist

Before building, verify these files exist:

```
/Users/sophearun/Projects/KH browser/
├── main.py                        ✅ Entry point
├── khbrowser.spec                 ✅ PyInstaller config
├── build_macos.sh                 ✅ Build script
├── entitlements.plist             ✅ macOS permissions
├── requirements.txt               ✅ Python dependencies
├── assets/
│   ├── Logo.png                   ✅ App icon source
│   ├── icon.icns                  ✅ macOS icon (if generated)
│   └── icon.ico                   ✅ Windows icon (if generated)
└── runtime_hooks/
    └── hook_pyqt6_fix.py          ✅ Qt library path fix
```

## 🚀 Build Steps

### Step 1: Generate Icons (First Time Only)
```bash
cd "/Users/sophearun/Projects/KH browser"
python3 generate_icons_advanced.py
```

**Expected Output:**
```
🎨 KH Browser Icon Generator
✅ Loaded logo: (800, 275)
🍎 Generating macOS .icns...
   ✅ 16x16
   ✅ 32x32
   ✅ 64x64
   ...
✅ Created: assets/icon.icns (2.50 MB)
🪟 Generating Windows .ico...
   ✅ 16x16
   ...
✅ Created: assets/icon.ico (187 KB)
```

### Step 2: Build macOS Application
```bash
cd "/Users/sophearun/Projects/KH browser"
bash build_macos.sh
```

**Expected Output:**
```
╔══════════════════════════════════════════════════════╗
║   KH Browser — macOS Build                  ║
╚══════════════════════════════════════════════════════╝

▶ Cleaning previous build...
▶ Installing Python dependencies...
▶ Building .app bundle with PyInstaller...
✅  App built: dist/KHBrowser.app
▶ Creating .dmg installer...
created: dist/KHBrowser-1.0.0-macOS.dmg

╔══════════════════════════════════════════════════════╗
║   BUILD COMPLETE                                     ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║   .app size : 542M                                ║
║   .dmg size : 1.3G                                ║
║                                                      ║
║   Output: dist/KHBrowser-1.0.0-macOS.dmg
╚══════════════════════════════════════════════════════╝

📦 To install: open dist/KHBrowser-1.0.0-macOS.dmg
   Drag KHBrowser.app → Applications folder
```

### Step 3: Verify Build Output
```bash
cd "/Users/sophearun/Projects/KH browser"

# Check sizes
ls -lh dist/KHBrowser.app
ls -lh dist/KHBrowser-1.0.0-macOS.dmg

# Expected:
# 542M  KHBrowser.app
# 1.3G  KHBrowser-1.0.0-macOS.dmg
```

### Step 4: Test the Application
```bash
# Open the DMG
open "dist/KHBrowser-1.0.0-macOS.dmg"

# Or launch directly
open "dist/KHBrowser.app"
```

## 📊 Build Process Details

### What build_macos.sh Does:
1. **Clean**: Removes old build artifacts
2. **Dependencies**: Installs Python requirements
3. **Bundle**: Runs PyInstaller with khbrowser.spec
4. **DMG**: Creates compressed disk image
5. **Verify**: Checks output files

### Key Configuration Files:

**khbrowser.spec** - PyInstaller Configuration
- Specifies all hidden imports (PyQt6, cryptography, etc.)
- Configures icon paths
- Sets bundle identifier: `com.khbrowser.app`
- Runtime hook: `runtime_hooks/hook_pyqt6_fix.py`

**entitlements.plist** - macOS Permissions
- Disables sandboxing (required for browser)
- Enables file system access
- Enables network access

**runtime_hooks/hook_pyqt6_fix.py** - Qt Library Paths
- Fixes QtCore framework resolution
- Sets DYLD_FALLBACK_LIBRARY_PATH
- Sets QT_PLUGIN_PATH

## ⚠️ Troubleshooting

### Issue: "command not found: bash"
**Solution**: Try using full path:
```bash
/bin/bash "/Users/sophearun/Projects/KH browser/build_macos.sh"
```

### Issue: PyInstaller not installed
**Solution**: Install dependencies first:
```bash
pip3 install -r requirements.txt
```

### Issue: App crashes on launch
**Check**: 
1. Runtime hook is installed: `runtime_hooks/hook_pyqt6_fix.py`
2. Entitlements file exists: `entitlements.plist`
3. Rebuild with: `bash build_macos.sh`

### Issue: Icon not showing
**Solution**: Regenerate icons and rebuild:
```bash
python3 generate_icons_advanced.py
bash build_macos.sh
```

### Issue: Build takes too long
**Note**: First build is ~5-8 minutes (PyInstaller processes frameworks)
Subsequent builds are faster (cache used)

## 📦 Distribution

### For Personal Use
1. Open DMG: `dist/KHBrowser-1.0.0-macOS.dmg`
2. Drag to Applications folder
3. Run from Applications

### For App Store (Optional)
Requires:
- Apple Developer Account ($99/year)
- Code signing certificate
- Notarization

```bash
# Sign the app (optional)
codesign --deep --force --verify --verbose \
  --sign "Developer ID Application: Your Name" \
  dist/KHBrowser.app
```

## 🔍 Verification Commands

```bash
# Check app structure
ls -la "dist/KHBrowser.app/Contents/"

# Check icon
ls -lh "dist/KHBrowser.app/Contents/Resources/icon.icns"

# Check Python files
ls -la "dist/KHBrowser.app/Contents/Resources/__main__.py"

# Check bundle identifier
mdls -name kMDItemCFBundleIdentifier "dist/KHBrowser.app"
# Expected: com.khbrowser.app

# Launch from terminal (to see output)
"dist/KHBrowser.app/Contents/MacOS/KHBrowser"
```

## 🎯 Complete Build Workflow

```bash
#!/bin/bash
# Full build workflow

cd "/Users/sophearun/Projects/KH browser"

# 1. Generate icons
echo "📦 Generating icons..."
python3 generate_icons_advanced.py || exit 1

# 2. Build app
echo "🍎 Building macOS app..."
bash build_macos.sh || exit 1

# 3. Verify
echo "✅ Verifying build..."
ls -lh dist/KHBrowser.app
ls -lh dist/KHBrowser-1.0.0-macOS.dmg

# 4. Success
echo ""
echo "✅ BUILD COMPLETE"
echo "📦 DMG: dist/KHBrowser-1.0.0-macOS.dmg"
echo "🚀 To test: open dist/KHBrowser-1.0.0-macOS.dmg"
```

## 📝 Build Output Location

```
/Users/sophearun/Projects/KH browser/dist/
├── KHBrowser.app/
│   └── Contents/
│       ├── MacOS/
│       │   └── KHBrowser (executable)
│       ├── Resources/
│       │   ├── icon.icns
│       │   ├── __main__.py
│       │   ├── PyQt6/
│       │   └── ... (all dependencies)
│       └── Info.plist
└── KHBrowser-1.0.0-macOS.dmg (compressed installer)
```

## 🆘 Support

If build fails:
1. Check error messages in output
2. Verify all requirements installed: `pip3 install -r requirements.txt`
3. Clean and retry: `rm -rf build/ && bash build_macos.sh`
4. Check Python version: `python3 --version` (should be 3.9+)

---

**Last Updated**: 2026-04-30  
**Status**: Production Ready  
**Version**: 1.0.0
