# 🪟 Windows Build Complete Guide

This guide explains how to build **KH Browser** for Windows after the `python BUILD.py all` command.

## ✅ What the BUILD.py all Command Does

```bash
python BUILD.py all
```

**On macOS (what you just did):**
- ✅ Builds `dist/KHBrowser.app` for macOS (254 MB)
- ✅ Generates complete build instructions for Windows
- ✅ Creates all necessary scripts and guides

**On Windows (if you run it):**
- ✅ Builds `dist\KHBrowser.exe` (standalone .exe file)
- ✅ Builds `KHBrowser-Setup.exe` (installer with wizard)
- ✅ Full production-ready Windows deployment

**On Linux:**
- ✅ Builds AppImage or standalone executable
- ✅ Complete Python bundle

---

## 🖥️ How to Build for Windows

### Prerequisites

You **MUST** use a **Windows computer** (Windows 7, 8, 10, or 11)

1. **Python 3.8+** → https://www.python.org/downloads/
   - ✅ Check "Add Python to PATH" during installation
   - ✅ Verify: Open Command Prompt and type `python --version`

2. **Git** (optional, for cloning) → https://git-scm.com/download/win

### Step 1: Get the Code

**Option A: Clone from GitHub**
```bash
git clone https://github.com/rinsophearun/kh-browser.git
cd kh-browser
```

**Option B: Download ZIP**
- Visit: https://github.com/rinsophearun/kh-browser
- Click "Code" → "Download ZIP"
- Extract to folder: `C:\Users\YourName\kh-browser`
- Open Command Prompt in that folder

### Step 2: Build Using One of These Methods

**Method A: Quick Batch File (Easiest) ✅ RECOMMENDED**
```batch
build_one_file.bat
```
- ✅ Works immediately
- ✅ Auto-installs dependencies
- ✅ Shows progress and completion
- ✅ Outputs: `dist\KHBrowser.exe`

**Method B: Python Script**
```bash
python build_one_file.py
```
- ✅ Same as batch file
- ✅ Better error messages
- ✅ Works on Python installed

**Method C: Master Builder (Complete)**
```bash
python BUILD.py windows
```
- ✅ Builds `dist\KHBrowser.exe` (one-file)
- ✅ Builds `KHBrowser-Setup.exe` (installer)
- ✅ Full verification
- ✅ Takes longer (5-10 minutes)

**Method D: Install Setup (For Distribution)**
```bash
python BUILD.py all
```
- ✅ Builds everything
- ✅ Creates both standalone and installer
- ✅ Complete production package

### Step 3: Find Your Output

**Quick Builds (Methods A, B):**
```
C:\path\to\kh-browser\dist\
  └── KHBrowser.exe         ← Standalone file (200-300 MB)
```

**Complete Build (Methods C, D):**
```
C:\path\to\kh-browser\dist\
  ├── KHBrowser.exe                    ← Standalone
  ├── KHBrowser-Setup.exe              ← Installer
  └── KHBrowser-2.0.26-Setup-Windows.exe
```

---

## 📊 Choosing Your Build Method

| Method | Output | Time | Best For |
|--------|--------|------|----------|
| `build_one_file.bat` | Single .exe | 5-10 min | Quick testing |
| `python build_one_file.py` | Single .exe | 5-10 min | Same as batch |
| `python BUILD.py windows` | .exe + Setup.exe | 10-15 min | Distribution |
| `python BUILD.py all` | Everything | 15-20 min | Complete package |

---

## 🚀 Using Your Built Executable

### For Testing

```bash
# Navigate to output folder
cd dist

# Run the executable
KHBrowser.exe
```

### For Distribution

**Option 1: Share Standalone .exe**
- Upload `KHBrowser.exe` to your website
- Send to users via email
- Users double-click to run (no installation!)

**Option 2: Share Setup Installer**
- Upload `KHBrowser-Setup.exe`
- Users run installer to install in Program Files
- Professional experience (Add/Remove Programs entry)

**Option 3: Create Portable USB**
- Copy `KHBrowser.exe` to USB drive
- Users plug in USB and double-click to run
- Works on any Windows computer

---

## ❌ Troubleshooting

### Problem: "Python not found"
**Solution:** Reinstall Python with "Add Python to PATH" checked

### Problem: Build takes 30+ minutes
**Solution:** Normal for first build (builds cache), subsequent builds faster

### Problem: "icon.ico not found"
**Solution:** Make sure you're in project root directory with `assets/` folder

### Problem: .exe won't run
**Solution 1:** Open Command Prompt and run manually:
```bash
cd dist
KHBrowser.exe
```
Check the error message.

**Solution 2:** Windows Defender might block it
- Click "More info" → "Run anyway"
- Normal for unsigned executables

### Problem: .exe is 250+ MB
**Solution:** That's normal!
- Python runtime: ~100 MB
- PyQt6 libraries: ~80 MB
- Dependencies: ~30 MB
- Your code: ~5 MB

---

## 📝 Batch File Details

`build_one_file.bat` does this automatically:

1. Checks Python installation
2. Installs PyInstaller (if needed)
3. Cleans previous builds
4. Builds `dist\KHBrowser.exe`
5. Shows completion with file size
6. Pauses to show results

**Manual equivalent:**
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=assets\icon.ico --name=KHBrowser ^
  --add-data "assets;assets" --add-data "qr;qr" main.py
```

---

## 🔒 Windows SmartScreen Warning

When users run your .exe for first time, Windows might show:

```
⚠️  Windows Defender SmartScreen
   "Windows protected your PC"
```

**This is NORMAL** for unsigned executables.

**Users should:**
1. Click "More info"
2. Click "Run anyway"
3. Application launches normally

**To remove warning** (optional):
- Code sign the executable with SSL certificate ($200+/year)
- Or use Installer (Setup.exe) which is trusted better

---

## 📦 All Available Build Scripts

**In Project Root:**

| File | Purpose |
|------|---------|
| `BUILD.py` | Master builder (Windows, macOS, Linux) |
| `build_one_file.bat` | Windows quick build (batch) |
| `build_one_file.py` | Windows quick build (Python) |
| `build_to_desktop.py` | Builds to custom output directory |
| `khbrowser.spec` | PyInstaller configuration |
| `installer.iss` | Inno Setup installer config |

---

## 🆘 Getting Help

### If Build Fails

1. **Check Python:**
   ```bash
   python --version
   ```
   Should be 3.8 or higher

2. **Install Dependencies:**
   ```bash
   pip install --upgrade pip pyinstaller PyQt6
   ```

3. **Try Manual Build:**
   ```bash
   python -m PyInstaller --onefile main.py
   ```

4. **Check Logs:**
   - Look in `build/` folder for detailed logs
   - Look in project root for `KHBrowser.spec`

### Report Issues

- GitHub: https://github.com/rinsophearun/kh-browser/issues
- Include: Windows version, Python version, error message

---

## 📚 Additional Resources

- **BUILD_GUIDE.md** - Complete build system documentation
- **BUILD_ONE_FILE_GUIDE.md** - Single .exe specific guide
- **WINDOWS_BUILD_PACKAGE/** - Pre-configured build tools
- **GitHub:** https://github.com/rinsophearun/kh-browser

---

## ✅ Summary

### macOS (You Are Here)
- ✅ Run `python BUILD.py all`
- ✅ Get `dist/KHBrowser.app` (ready to use)
- ✅ Get instructions for Windows (this guide)

### Windows (Next Step)
1. Use a Windows computer
2. Clone repository
3. Run `build_one_file.bat`
4. Get `dist\KHBrowser.exe`
5. Share with users!

---

**Version:** 2.0.26  
**Last Updated:** 2026-04-30  
**Platform:** Windows 7+  
**Python:** 3.8+

