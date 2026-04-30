# 📦 Build One-File .exe Guide

This guide helps you build **KH Browser** as a single standalone `.exe` file.

## ✅ What You Get

- **Single file:** `KHBrowser.exe` (no installation needed)
- **Portable:** Works on any Windows computer
- **Complete:** Includes all icons, images, and features
- **Standalone:** No dependencies required
- **Professional:** Version 2.0.26 with modern UI

## 🖥️ System Requirements

**Windows Only:**
- Windows 7, 8, 10, or 11
- Python 3.8+ (if building from source)
- ~500MB disk space for build

## 🚀 Quick Start (Windows)

### Option 1: Batch File (Easiest)

```bash
# Double-click or run in Command Prompt:
build_one_file.bat
```

This automatically:
1. Installs PyInstaller
2. Builds the executable
3. Shows completion message

### Option 2: Python Script

```bash
# In Command Prompt or PowerShell:
python build_one_file.py
```

Same result, more control for troubleshooting.

## 📋 Build Output

```
dist/
  └── KHBrowser.exe    ← Single file (200-300 MB)
```

## 🎯 Using the Built Executable

### For Users (No Setup Required)
1. Download `KHBrowser.exe`
2. Double-click to run
3. No installation needed!

### For Distribution
- Share `dist/KHBrowser.exe` directly
- Host on your website
- Include in USB drives
- Upload to app stores

## 🔧 Build Process Details

### What PyInstaller Does:
```
your code (main.py + modules)
    ↓
    ├─ Analyzes dependencies
    ├─ Bundles Python runtime
    ├─ Includes all libraries
    ├─ Adds icon & assets
    └─ Compiles to single .exe
```

### Build Size Explanation:
- Python runtime: ~100 MB
- PyQt6 libraries: ~80 MB
- Dependencies: ~30 MB
- Your code & assets: ~5 MB
- **Total: ~200-300 MB**

## ❌ Troubleshooting

### Build Fails - Module Not Found
```bash
# Solution: Check hidden imports in build_one_file.py
# Add missing module name to --hidden-import=module_name
```

### Build Too Slow
- First build is slowest (caches after)
- Normal: 3-10 minutes
- Depends on computer speed

### .exe Won't Run
1. Check `dist/KHBrowser.exe` exists
2. Try from Command Prompt to see error:
   ```bash
   cd dist
   KHBrowser.exe
   ```
3. Check Windows Defender isn't blocking it

### File Size Too Large
- PyInstaller bundles entire Python runtime
- Unavoidable with PyQt6
- Normal for desktop apps (200-300 MB)

## 📚 Command-Line Options

If you want to customize the build:

```bash
# Build with console window (for debugging):
pyinstaller --onefile --console main.py

# Build without icon:
pyinstaller --onefile --windowed main.py

# Build with custom icon:
pyinstaller --onefile --icon=custom_icon.ico main.py

# Build in one directory (instead of single file):
pyinstaller --onedir --windowed main.py
```

## 🔐 Security Notes

- Windows SmartScreen may warn on first run
  - Click "More info" → "Run anyway"
  - This is normal for unsigned executables
  
- To remove warning, code-sign the executable
  - Requires SSL certificate ($200+/year)
  - Optional for internal use

## 📊 File Comparison

| Feature | build_one_file.bat | build_one_file.py |
|---------|-------------------|------------------|
| Platform | Windows | Windows, macOS, Linux |
| Setup | None (runs .bat) | Python 3.8+ |
| Speed | Same | Same |
| Output | Same .exe | Same .exe |

## 🆘 When to Use Each Build Method

| Use Case | Method |
|----------|--------|
| Quick build on Windows | `build_one_file.bat` |
| Cross-platform building | `python BUILD.py windows` |
| Installer (Setup.exe) | `python BUILD.py windows` |
| macOS .app distribution | `python BUILD.py macos` |

## 📞 Support

See detailed help:
- `BUILD_GUIDE.md` - Complete build system
- `BUILD.py --help` - Universal builder
- GitHub Issues - Report problems

---

**Version:** 2.0.26  
**Last Updated:** 2026-04-30  
**Platform:** Windows (Python 3.8+)
