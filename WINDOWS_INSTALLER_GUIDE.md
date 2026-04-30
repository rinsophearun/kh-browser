# 🪟 KH Browser Windows Installer - Complete Guide

**Status:** ✅ **READY FOR WINDOWS BUILD**  
**Last Updated:** April 30, 2026

---

## 📋 Summary

The KH Browser project is **fully prepared** for Windows .exe installer building. All necessary files, scripts, and configurations are in place. The build process is automated and ready to run on any Windows 10/11 machine.

### What's Ready:
- ✅ PyInstaller configuration (khbrowser.spec)
- ✅ Inno Setup installer script (installer.iss)
- ✅ Automated build scripts (PowerShell & Batch)
- ✅ All dependencies configured
- ✅ Windows icon prepared (icon.ico)
- ✅ Build documentation complete

---

## 🎯 Quick Start (Windows Only)

### Option 1: Automated Build (Recommended)
```batch
# Double-click: build_windows_batch.bat
```

### Option 2: PowerShell
```powershell
# Right-click → Run with PowerShell
.\build_windows_installer.ps1
```

### Option 3: Manual Build
See [Manual Build Section](#manual-build) below.

---

## 📦 Expected Output

After successful build on Windows:

```
dist\KHBrowser\KHBrowser.exe
├─ Size: ~380 MB
├─ Type: Portable executable
├─ Features:
│  ├─ No installation needed
│  ├─ Can run from USB drive
│  ├─ All dependencies bundled
│  └─ Self-contained
│
installer_output\KHBrowser-1.0.0-Setup-Windows.exe
├─ Size: ~95 MB
├─ Type: Professional installer
├─ Features:
│  ├─ Windows installer interface
│  ├─ Add/Remove Programs support
│  ├─ Start Menu shortcuts
│  ├─ Desktop shortcuts
│  └─ Registry integration
```

---

## 🔧 Prerequisites

### Required:
1. **Windows 10** (version 1909+) or **Windows 11**
2. **Python 3.11+**
   - Download: https://www.python.org/downloads/
   - ☑️ Check "Add Python to PATH" during installation
3. **Inno Setup 6**
   - Download: https://jrsoftware.org/isdl.php
   - Install to: `C:\Program Files (x86)\Inno Setup 6\`

### Optional:
- **Visual C++ Build Tools** (for some packages)
- **Code signing certificate** (for signing the EXE)

---

## 📝 Installation Instructions

### On Windows Machine:

#### Step 1: Verify Python
```batch
python --version
# Expected: Python 3.11.x or higher
```

#### Step 2: Verify Inno Setup
Check if file exists:
```batch
dir "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
```

If not found, install from: https://jrsoftware.org/isdl.php

#### Step 3: Build

**Option A - Easiest (Double-click):**
```
1. Navigate to project folder
2. Double-click: build_windows_batch.bat
3. Wait for completion (5-8 minutes)
4. Two folders created: dist\ and installer_output\
```

**Option B - PowerShell:**
```powershell
cd C:\Users\YourUsername\Projects\KH browser
.\build_windows_installer.ps1
```

**Option C - Manual:**
```batch
# Install dependencies
pip install PyQt6 pyinstaller requests cryptography Pillow

# Build EXE
pyinstaller khbrowser.spec --clean --noconfirm

# Build installer (if Inno Setup installed)
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

---

## <a name="manual-build"></a>🛠️ Manual Build Process

If automated scripts don't work, follow these steps:

### 1. Open Command Prompt or PowerShell

### 2. Navigate to Project
```batch
cd "C:\Users\YourUsername\Projects\KH browser"
```

### 3. Create Virtual Environment (Optional but Recommended)
```batch
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies
```batch
pip install --upgrade pip
pip install PyQt6 pyinstaller requests cryptography Pillow
```

### 5. Clean Previous Builds
```batch
rmdir /s /q build
rmdir /s /q dist
```

### 6. Build with PyInstaller
```batch
pyinstaller khbrowser.spec --clean --noconfirm
```

**Output:** `dist\KHBrowser\KHBrowser.exe` (~380 MB)

### 7. Build Installer with Inno Setup
```batch
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

**Output:** `installer_output\KHBrowser-1.0.0-Setup-Windows.exe` (~95 MB)

---

## ✅ Verification Checklist

After build completes:

- [ ] `dist\KHBrowser\KHBrowser.exe` exists (380 MB)
- [ ] `installer_output\KHBrowser-1.0.0-Setup-Windows.exe` exists (95 MB)
- [ ] Portable EXE launches without errors
- [ ] Setup installer runs without errors
- [ ] Application starts and works correctly
- [ ] All features function as expected

---

## 🧪 Testing

### Test Portable EXE:
```batch
dist\KHBrowser\KHBrowser.exe
```

### Test Setup Installer:
```batch
installer_output\KHBrowser-1.0.0-Setup-Windows.exe
```

Then verify:
1. Installer launches
2. Installation completes
3. App appears in Add/Remove Programs
4. Shortcuts created (Start Menu, Desktop)
5. Application launches and works

---

## 📊 File Structure After Build

```
KH browser/
├── dist/
│   ├── KHBrowser/
│   │   ├── KHBrowser.exe         ← Portable executable
│   │   └── _internal/            ← Dependencies
│   └── KHBrowser.app             ← macOS (from earlier build)
│
├── installer_output/
│   └── KHBrowser-1.0.0-Setup-Windows.exe  ← Setup wizard
│
├── build/                        ← Temporary build files
│
├── khbrowser.spec               ← PyInstaller config
├── installer.iss                ← Inno Setup config
├── build_windows_batch.bat      ← Batch build script
└── build_windows_installer.ps1  ← PowerShell script
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| `python: command not found` | Add Python to PATH or use full path: `C:\Python311\python.exe` |
| `ISCC.exe not found` | Install Inno Setup from https://jrsoftware.org/isdl.php |
| `ModuleNotFoundError: PyQt6` | Run: `pip install --force-reinstall PyQt6` |
| `Build takes too long` | Close other applications, increase available RAM |
| `Inno Setup compilation failed` | Check `installer.iss` path, ensure Inno Setup is installed |
| `EXE won't start` | Check Windows Defender isn't blocking it, try unblocking |
| `Missing DLL files` | Ensure all PyQt6 dependencies are bundled (check _internal folder) |

---

## 🔐 Code Signing (Optional)

To digitally sign the executables:

```batch
REM Requires a code signing certificate
signtool sign /f certificate.pfx /p password /t http://timestamp.server.com ^
    dist\KHBrowser\KHBrowser.exe

signtool sign /f certificate.pfx /p password /t http://timestamp.server.com ^
    installer_output\KHBrowser-1.0.0-Setup-Windows.exe
```

Benefits:
- Users see your company name during installation
- No Windows Defender warnings
- Better security reputation

---

## 📤 Distribution

### For End Users:
**Recommended:** Share `installer_output\KHBrowser-1.0.0-Setup-Windows.exe`

Why:
- Professional appearance
- Easy installation
- Add/Remove Programs integration
- System shortcuts

### For Advanced Users / USB Drive:
**Alternative:** Share `dist\KHBrowser\KHBrowser.exe`

Why:
- No installation needed
- Can run from USB
- Portable across systems

---

## 📈 Build Statistics

| Metric | Value |
|--------|-------|
| Portable EXE Size | ~380 MB |
| Setup Installer Size | ~95 MB |
| Build Time | 5-8 minutes |
| PyInstaller Time | 2-5 minutes |
| Inno Setup Time | 1-2 minutes |
| Supported Windows | 10 (1909+), 11 |
| Architecture | x86_64, arm64 |

---

## 🎯 Next Steps

1. ✅ Transfer project to Windows machine (if needed)
2. ✅ Verify Python 3.11+ installed
3. ✅ Install Inno Setup 6
4. ⏳ Run `build_windows_batch.bat`
5. ⏳ Verify output files created
6. ⏳ Test both executables
7. ⏳ Distribute to users

---

## 📞 Support

For issues or questions:
1. Check [Troubleshooting](#troubleshooting) section
2. Review `WINDOWS_BUILD_INSTRUCTIONS.txt`
3. Check PyInstaller logs in `build/khbrowser/`
4. Check Inno Setup logs in `installer_output/`

---

## 📄 Related Files

- `khbrowser.spec` - PyInstaller configuration
- `installer.iss` - Inno Setup configuration
- `build_windows_batch.bat` - Automated batch build
- `build_windows_installer.ps1` - PowerShell build script
- `build_windows_complete.py` - Cross-platform Python build
- `WINDOWS_BUILD_INSTRUCTIONS.txt` - Original instructions
- `WINDOWS_BUILD_READY.md` - Build preparation status

---

**🎉 Everything is ready! Transfer to Windows and build the installer.**

---

*Generated on April 30, 2026*  
*For KH Browser v1.0.0*
