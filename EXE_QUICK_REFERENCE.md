# 📦 dist\KHBrowser.exe - Quick Reference

## What Is It?

`dist\KHBrowser.exe` is a **single standalone Windows executable file** for KH Browser v2.0.26

- **Type:** Self-contained .exe (no installation needed)
- **Size:** ~200-300 MB
- **Version:** 2.0.26
- **Platform:** Windows 7, 8, 10, 11
- **Dependencies:** None (all bundled inside)

---

## 🔨 How to Build It

### ✅ You MUST Use Windows

This file can ONLY be built on a Windows computer (Windows 7+)

### Option 1: Quick Batch (Easiest) ⭐

On Windows, in Command Prompt:
```batch
build_one_file.bat
```

**What it does:**
1. Auto-installs PyInstaller
2. Builds the .exe
3. Shows completion with file size
4. Creates: `dist\KHBrowser.exe`

**Time:** 5-10 minutes

### Option 2: Python Script

```bash
python build_one_file.py
```

Same as batch file, more details shown.

### Option 3: Master Builder

```bash
python BUILD.py windows
```

Builds both:
- `dist\KHBrowser.exe` (standalone)
- `KHBrowser-Setup.exe` (installer)

**Time:** 10-15 minutes

---

## 📍 Location After Build

```
C:\Users\YourName\kh-browser\dist\
  └── KHBrowser.exe    ← The file you want!
```

---

## 🚀 How to Use It

### For Personal Use
1. Double-click `KHBrowser.exe`
2. Application launches
3. Done! (No installation needed)

### For Distribution to Users
1. Share `KHBrowser.exe` via:
   - Email
   - Website download
   - USB drive
   - Cloud storage (Google Drive, OneDrive, etc.)

2. Users double-click to run
3. May see Windows SmartScreen warning (click "Run anyway")
4. Application launches

### For Installation (Optional)
1. Use `KHBrowser-Setup.exe` instead (from `BUILD.py windows`)
2. Professional installer experience
3. Uninstall from Control Panel

---

## 📊 File Specifications

| Property | Value |
|----------|-------|
| **Filename** | `KHBrowser.exe` |
| **Size** | 200-300 MB |
| **Type** | Win32 Executable |
| **Requires** | Windows 7+ |
| **Architecture** | x86-64 (64-bit) |
| **Version** | 2.0.26 |
| **Installation** | None (portable) |
| **Dependencies** | None (all bundled) |

---

## 🔒 Windows SmartScreen

When users run `.exe` first time:

```
⚠️  Windows Defender SmartScreen
   "Windows protected your PC"
   
   This app couldn't be verified by an app store
```

**This is NORMAL** for unsigned executables.

**Users should click:**
1. "More info"
2. "Run anyway"
3. Application launches normally

**To remove this** (optional):
- Code-sign executable with SSL certificate ($200+/year)

---

## 🎯 What's Inside the .exe

```
KHBrowser.exe (300 MB) contains:
  ├── Python Runtime      (~100 MB)
  ├── PyQt6 Libraries     (~80 MB)
  ├── Dependencies        (~30 MB)
  │   ├── cryptography
  │   ├── requests
  │   ├── selenium (RPA)
  │   └── Others
  ├── Your Code           (~5 MB)
  │   ├── main.py
  │   ├── main_window.py
  │   ├── profile_dialog.py
  │   └── All modules
  ├── Assets              (~5 MB)
  │   ├── icons/
  │   ├── qr/qr.jpg
  │   └── Images
  └── Compression         (LZMA2 Ultra)
```

**Why so large?**
- Python runtime must be included
- No external dependencies required
- Works on any Windows computer

---

## ❌ Troubleshooting

| Problem | Solution |
|---------|----------|
| **"Python not found"** | Reinstall Python with "Add Python to PATH" |
| **Build takes 30+ min** | Normal for first build (caches after) |
| **"icon.ico not found"** | Make sure in project root directory |
| **.exe won't launch** | Try from Command Prompt: `cd dist && KHBrowser.exe` |
| **SmartScreen blocks it** | Click "More info" → "Run anyway" |

---

## 📋 Build Methods Comparison

| Method | Time | Output | Setup |
|--------|------|--------|-------|
| `build_one_file.bat` | 5-10 min | Single .exe | Easy |
| `python build_one_file.py` | 5-10 min | Single .exe | Medium |
| `python BUILD.py windows` | 10-15 min | .exe + Setup.exe | Complete |

---

## 💾 Distribution Options

### Option 1: Direct .exe Share
- Upload to website
- Email users
- USB drive
- Fastest, simplest

### Option 2: Installer (Setup.exe)
- Professional experience
- Add/Remove Programs entry
- Auto-updating setup
- Better for enterprises

### Option 3: GitHub Releases
1. Create release on GitHub
2. Attach `KHBrowser.exe`
3. Users download from releases page
4. Easy version management

### Option 4: Portable USB
- Copy `.exe` to USB drive
- Works on any Windows
- No installation
- Perfect for on-site demos

---

## 🔐 Security & Signing

### Current Status (Unsigned)
- ✅ Works perfectly
- ⚠️ Windows SmartScreen shows warning
- ✅ Users click "Run anyway" and it works

### To Remove Warning (Optional)
- Cost: $200-500/year for SSL certificate
- Time: ~2 hours to set up code signing
- Result: Professional signed executable

---

## 📞 Getting Help

### If Build Fails
1. Check: `python --version` (must be 3.8+)
2. Run: `pip install --upgrade pyinstaller PyQt6`
3. Try: `python -m PyInstaller --onefile main.py`

### If .exe Won't Run
1. Check Windows version (must be 7+)
2. Try running from Command Prompt to see error
3. Disable antivirus temporarily (test only)

### Report Issues
- GitHub: https://github.com/rinsophearun/kh-browser/issues
- Include: Windows version, build method, error message

---

## 📚 Related Files

- **BUILD_ONE_FILE_GUIDE.md** - Detailed one-file building guide
- **WINDOWS_BUILD_COMPLETE_GUIDE.md** - Complete Windows build guide
- **BUILD.py** - Master builder script
- **installer.iss** - Inno Setup configuration

---

## ✅ Checklist Before Distributing

- [ ] Build successful (no errors)
- [ ] File exists: `dist\KHBrowser.exe`
- [ ] File size: 200-300 MB (reasonable)
- [ ] Tested on Windows machine
- [ ] All features work (buttons, profiles, etc.)
- [ ] QR code popup works (Donate button)
- [ ] Settings tab works
- [ ] Real-time refresh works (2 second timer)

---

**Version:** 2.0.26  
**Last Updated:** 2026-04-30  
**Platform:** Windows 7+  
**Python:** 3.8+ (only for building)

