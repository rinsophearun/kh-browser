# 🎨 KH Browser Icon Generation Guide

## Overview
This guide explains how to generate properly sized application icons for both macOS (.icns) and Windows (.ico) from the Logo.png source image.

## Prerequisites

### Required
- Python 3.7+
- Pillow (PIL): `pip3 install Pillow`

### Optional but Recommended
- **macOS only**: Xcode Command Line Tools (for native .icns generation)
  ```bash
  xcode-select --install
  ```

## Quick Start

### Option 1: Automated (Recommended)
```bash
cd "/Users/sophearun/Projects/KH browser"
bash generate_icons.sh
```

### Option 2: Direct Python
```bash
cd "/Users/sophearun/Projects/KH browser"
python3 generate_icons_advanced.py
```

## Icon Specifications

### macOS (.icns)
- **Format**: Apple Icon Image Format
- **Sizes**: 16, 32, 64, 128, 256, 512, 1024 pixels
- **Features**:
  - Used in Finder, Dock, App Store
  - Supports High DPI (@2x variants)
  - Generated using native macOS `iconutil` when available

### Windows (.ico)
- **Format**: Windows Icon Format
- **Sizes**: 16, 32, 48, 64, 128, 256 pixels
- **Features**:
  - Used in taskbar, file explorer, shortcuts
  - All sizes embedded in single .ico file
  - Standard Windows application icon

## File Locations

```
/Users/sophearun/Projects/KH browser/
├── assets/
│   ├── Logo.png          ← Source image (must exist)
│   ├── icon.icns         ← macOS icon (generated)
│   ├── icon.ico          ← Windows icon (generated)
│   └── KHBrowser.iconset/
│       ├── icon_16x16.png
│       ├── icon_32x32.png
│       ├── ...
│       └── icon_1024x1024.png
```

## Step-by-Step Guide

### 1. Prepare Source Image
The `Logo.png` file should be:
- **Minimum size**: 1024×1024 pixels (or higher for best quality)
- **Format**: PNG with transparency (RGBA)
- **Content**: Logo centered on transparent background
- **Location**: `/Users/sophearun/Projects/KH browser/assets/Logo.png`

### 2. Generate Icons (macOS)
```bash
bash generate_icons.sh
```

**Output:**
- Generates 16 PNG files in `assets/KHBrowser.iconset/`
- Converts to `assets/icon.icns` using `iconutil`
- Generates `assets/icon.ico` for Windows

### 3. Verify Icons
```bash
ls -lh "/Users/sophearun/Projects/KH browser/assets/icon.*"
```

**Expected output:**
```
-rw-r--r--  1 user  staff  2.5M  Apr 29 10:00 icon.icns
-rw-r--r--  1 user  staff  187K  Apr 29 10:00 icon.ico
```

### 4. Build Applications

**macOS:**
```bash
cd "/Users/sophearun/Projects/KH browser"
bash build_macos.sh
```

**Windows (on Windows machine):**
```cmd
cd "C:\path\to\KH browser"
build_windows_installer.bat
```

## Troubleshooting

### Issue: "iconutil not found"
**Symptom**: Warning about `iconutil` not available

**Solution**:
1. Install Xcode Command Line Tools:
   ```bash
   xcode-select --install
   ```
2. Re-run generation:
   ```bash
   python3 generate_icons_advanced.py
   ```

### Issue: "Pillow not installed"
**Symptom**: ImportError when running script

**Solution**:
```bash
pip3 install Pillow
```

### Issue: Logo.png not found
**Symptom**: FileNotFoundError

**Solution**:
1. Verify file exists:
   ```bash
   ls -la "/Users/sophearun/Projects/KH browser/assets/Logo.png"
   ```
2. Ensure it's in correct location and has read permissions

### Issue: Icons look pixelated in macOS
**Symptom**: Blurry icons in Dock or Finder

**Cause**: Source image is too small
**Solution**:
1. Use a larger source image (minimum 1024×1024)
2. Re-generate icons
3. Rebuild macOS app with `bash build_macos.sh`

## Build Configuration Reference

### khbrowser.spec
The PyInstaller spec file references:
```python
icon='assets/icon.icns' if sys.platform == 'darwin' else 'assets/icon.ico'
```

This automatically selects the correct icon for each platform.

### entitlements.plist
macOS app bundle uses entitlements for permissions:
```xml
<key>com.apple.security.app-sandbox</key>
<false/>  <!-- Required for browser functionality -->
```

### installer.iss (Windows)
Windows installer includes icon in shortcuts and Add/Remove Programs.

## Icon Design Best Practices

1. **Square Format**: Ensure logo fits in square canvas
2. **Centered**: Logo should be centered for consistency
3. **Transparency**: Use transparent background (RGBA)
4. **Safe Zone**: Keep important content in center 70% of canvas
5. **Simple Shapes**: Avoid thin lines (may be lost at small sizes)
6. **Contrast**: Ensure visibility on both light and dark backgrounds

## Development vs Production

### Development
- Use simplified icons or placeholder
- Quick regeneration for testing

### Production
- Use high-quality 1024×1024+ source image
- Test on actual hardware (Mac, Windows)
- Consider code signing (optional but recommended)

## macOS Code Signing (Optional)

If you plan to distribute on Mac App Store:
```bash
# Sign the .app
codesign --deep --force --verify --verbose \
  --sign "Developer ID Application: Your Name" \
  dist/KHBrowser.app

# Notarize (optional, for App Store distribution)
xcrun notarytool submit dist/KHBrowser-1.0.0-macOS.dmg \
  --apple-id your-apple-id@example.com \
  --password your-app-password \
  --team-id YOUR_TEAM_ID
```

## Windows Code Signing (Optional)

For professional distribution:
```batch
# Sign the .exe (requires Windows code signing certificate)
signtool.exe sign /f certificate.pfx /p password /t http://timestamp.server /d "KH Browser" dist\KHBrowser-1.0.0-Setup.exe
```

## Testing Icons

### macOS
1. Drag `dist/KHBrowser.app` to Applications folder
2. Check Finder icon
3. Check Dock icon
4. Check App Store (if applicable)

### Windows
1. Run installer: `dist/KHBrowser-1.0.0-Setup.exe`
2. Check taskbar icon
3. Check Start Menu shortcut icon
4. Check desktop shortcut icon

## References

- [Apple macOS Icon Guidelines](https://developer.apple.com/design/human-interface-guidelines/macos/icons-and-images/app-icon/)
- [Windows Icon Guidelines](https://learn.microsoft.com/en-us/windows/uwp/design/style/app-icons-and-logos/)
- [PIL/Pillow Documentation](https://pillow.readthedocs.io/)
- [PyInstaller Icon Documentation](https://pyinstaller.org/en/stable/spec-file.html#icon)

## Automation

To regenerate icons automatically before each build:

### macOS (add to build_macos.sh)
```bash
echo "▶ Generating app icons..."
python3 generate_icons_advanced.py || exit 1
```

### Windows (add to build_windows_installer.bat)
```batch
echo Generating app icons...
python generate_icons_advanced.py || exit /b 1
```

---

**Last Updated**: 2026-04-29  
**Version**: 1.0.0  
**Author**: KH Browser Build System
