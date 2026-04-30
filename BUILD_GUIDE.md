# 🚀 KH Browser v2.0.0 - Universal Build Guide

Complete build system for Windows and macOS with full installation packages, icons, images, and everything included.

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [System Requirements](#system-requirements)
3. [Installation](#installation)
4. [Building](#building)
5. [Output Files](#output-files)
6. [Distribution](#distribution)
7. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### For macOS:
```bash
python BUILD.py macos        # Build macOS .app and DMG
# or
python BUILD.py all          # Build for both platforms
```

### For Windows:
```cmd
python BUILD.py windows      # Build Windows .exe and installer
REM or
python BUILD.py all          # Build for both platforms
```

---

## 💻 System Requirements

### macOS:
- **OS**: macOS 10.13 or later
- **Python**: 3.11+
- **Tools**: Xcode Command Line Tools (for hdiutil)
- **Disk Space**: 5+ GB free

### Windows:
- **OS**: Windows 10/11 (64-bit)
- **Python**: 3.11+
- **Tools**: Inno Setup 6 (for installer creation)
- **Disk Space**: 5+ GB free

---

## 📦 Installation

### 1. Install Python 3.11+

**macOS:**
```bash
brew install python@3.11
```

**Windows:**
- Download from https://www.python.org/downloads/
- ⚠️ Check "Add Python to PATH"

### 2. Install Inno Setup (Windows Only)

- Download from https://jrsoftware.org/isdl.php
- Run installer with default settings

### 3. Create Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows:**
```cmd
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🏗️ Building

### Build Script Features:

✅ Verifies all required files
✅ Cleans previous builds
✅ Installs all dependencies
✅ Builds application for target platform
✅ Creates native installers
✅ Embeds all icons and images
✅ Verifies all outputs
✅ Shows detailed progress

### Usage:

```bash
# Build for current platform only
python BUILD.py

# Build for specific platform
python BUILD.py macos                 # macOS only
python BUILD.py windows               # Windows only

# Build for both platforms
python BUILD.py all
```

### Build Phases:

1. **Verification** (< 1 min)
   - Checks all required files exist
   - Verifies icons and assets

2. **Clean** (< 1 min)
   - Removes previous build artifacts
   - Clears cache directories

3. **Install Dependencies** (3-5 min)
   - Installs PyQt6
   - Installs PyInstaller
   - Installs other required packages

4. **Build Application** (5-10 min per platform)
   - PyInstaller bundles Python + dependencies
   - Creates standalone application
   - Embeds icons and resources

5. **Create Installer** (2-5 min, platform-specific)
   - macOS: Creates DMG disk image
   - Windows: Creates Setup.exe with Inno Setup

6. **Verification** (< 1 min)
   - Confirms all outputs created
   - Checks file sizes and integrity

**Total Time:** 15-25 minutes first build, 10-15 minutes subsequent

---

## 📦 Output Files

### macOS:

```
dist/
├── KHBrowser.app                      (Complete macOS application)
│   └── Contents/
│       ├── MacOS/KHBrowser           (Executable)
│       ├── Resources/                (Icons, images)
│       └── Frameworks/               (PyQt6, Python libraries)
│
└── KHBrowser-2.0.0.dmg               (Installer - optional)
```

**Sizes:**
- `KHBrowser.app`: ~500 MB
- `KHBrowser-2.0.0.dmg`: ~200 MB (compressed)

### Windows:

```
dist/KHBrowser/
└── KHBrowser.exe                      (~380 MB portable executable)

installer_output/
└── KHBrowser-2.0.0-Setup-Windows.exe (~95 MB installer)
```

---

## 🎯 What's Included

### Features:
- ✨ Open All / Close All buttons
- 💝 Donate button with QR code
- 🔄 Update button for manual refresh
- ⚙️ Settings tab (7 options per profile)
- ⏱️ Real-time auto-refresh (2 seconds)

### Assets Bundled:
- Application icon (all formats)
- QR code image for donations
- All UI assets and styling
- All Python source code

### Dependencies:
- PyQt6 (GUI framework)
- cryptography (SSL/TLS)
- requests (HTTP)
- Pillow (images)
- All required libraries

---

## 📤 Distribution

### macOS Distribution:

**Option 1: Direct App**
```
dist/KHBrowser.app → Share directly
Users can run immediately
Requires ~500 MB disk space
```

**Option 2: DMG Installer**
```
dist/KHBrowser-2.0.0.dmg → Traditional macOS installer
Users double-click to install
Compressed to ~200 MB
Adds to Applications folder
```

### Windows Distribution:

**Option 1: Portable EXE**
```
dist/KHBrowser/KHBrowser.exe → No installation
Share directly (~380 MB)
Users can run from USB drive
No registry modifications
```

**Option 2: Setup Installer**
```
installer_output/KHBrowser-2.0.0-Setup-Windows.exe → Traditional installer
Users run setup wizard (~95 MB)
Adds to Start menu
More professional appearance
Standard Windows installation
```

### Upload to GitHub:

1. Go to: https://github.com/rinsophearun/kh-browser/releases
2. Click "Draft a new release"
3. Tag: `v2.0.0`
4. Upload all built files
5. Add release notes with features
6. Publish release

### Share Links:
- GitHub Releases (recommended)
- Website download page
- Cloud storage (Google Drive, Dropbox)
- Direct email/messaging

---

## 🐛 Troubleshooting

### "Python not found"
**Solution:**
1. Verify Python installed: `python --version`
2. On Windows, reinstall with "Add Python to PATH"
3. Restart terminal/command prompt

### "Module not found" (PyQt6, PyInstaller, etc)
**Solution:**
1. Activate virtual environment
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Verify: `pip list | grep PyQt6`

### "Inno Setup not found" (Windows)
**Solution:**
1. Download: https://jrsoftware.org/isdl.php
2. Install with default settings
3. Restart Command Prompt
4. Retry build

### "Permission denied" / "Access denied"
**Solution:**
1. Close any running KH Browser windows
2. Run as Administrator (Windows)
3. Clear `~/.khbrowser/` cache directory
4. Retry build

### "Not enough disk space"
**Solution:**
1. Free up 5+ GB disk space
2. Delete `dist/`, `build/` directories
3. Clean temp files
4. Retry build

### Build hangs or takes too long
**Solution:**
1. First build takes 10-15 minutes (normal)
2. Check Task Manager for `python.exe` / `pyinstaller`
3. Wait at least 15 minutes before canceling
4. If stuck: Press Ctrl+C and retry

### DMG Creation Fails (macOS)
**Solution:**
1. Ensure `KHBrowser.app` exists in `dist/`
2. Check disk space (needs ~2 GB free)
3. Try: `hdiutil create -help` to verify tool exists
4. Build will continue even if DMG fails

---

## ✅ Verification Checklist

After build completes:

### Files Created:
- [ ] macOS: `dist/KHBrowser.app` exists (~500 MB)
- [ ] macOS: `dist/KHBrowser-2.0.0.dmg` exists (~200 MB)
- [ ] Windows: `dist/KHBrowser/KHBrowser.exe` exists (~380 MB)
- [ ] Windows: `installer_output/*.exe` exists (~95 MB)

### Icons & Assets:
- [ ] macOS app shows KH Browser icon
- [ ] Windows .exe files show colored icon
- [ ] QR code image bundled
- [ ] All UI assets present

### Test macOS App:
- [ ] Double-click `dist/KHBrowser.app`
- [ ] Window opens without errors
- [ ] All buttons visible
- [ ] Donate button shows QR code
- [ ] Settings tab opens
- [ ] Real-time refresh working

### Test macOS DMG (Optional):
- [ ] Double-click `.dmg` file
- [ ] Mounts as virtual volume
- [ ] Shows installer window
- [ ] Can drag app to Applications

### Test Windows Portable:
- [ ] Double-click `KHBrowser.exe`
- [ ] Window opens without errors
- [ ] All buttons visible
- [ ] All features working
- [ ] No missing DLLs errors

### Test Windows Installer:
- [ ] Double-click `Setup.exe`
- [ ] Setup wizard launches
- [ ] Installation completes
- [ ] Shortcut created in Start menu
- [ ] Shortcut launches app
- [ ] All features working

---

## 📝 Release Notes

### v2.0.0 - Major Release

**New Features:**
- ✨ Open All / Close All buttons for batch operations
- 💝 Donate button with QR code popup
- 🔄 Update button for manual refresh
- ⚙️ Settings tab (7 per-profile options)
- ⏱️ Real-time auto-refresh (2 second interval)

**Improvements:**
- Better UI spacing and layout
- Enhanced button styling with gradients
- Optimized table rendering
- Improved code architecture

**System Requirements:**
- Windows 10 (version 1909+) or Windows 11
- macOS 10.13 or later
- 64-bit system
- 500+ MB disk space
- Modern GPU with OpenGL support

---

## 🔗 Links

- **Repository:** https://github.com/rinsophearun/kh-browser
- **Issues:** https://github.com/rinsophearun/kh-browser/issues
- **Releases:** https://github.com/rinsophearun/kh-browser/releases

---

## 📞 Support

For issues or questions:
1. Check Troubleshooting section above
2. Review BUILD.py output messages
3. Check GitHub Issues
4. Provide: Platform, Python version, error message

---

## 📄 License

See LICENSE file in repository.

---

**Ready to build KH Browser for Windows and macOS!** 🚀
