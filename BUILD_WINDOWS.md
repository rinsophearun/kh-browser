# 🪟 Build Windows 11 Installer — KH Browser

## Quick Start (Windows 10/11)

### Option A — Batch File (Easiest)
```batch
build_windows_installer.bat
```

### Option B — PowerShell
```powershell
# Right-click → Run with PowerShell
# OR in terminal:
powershell -ExecutionPolicy Bypass -File build_windows_installer.ps1
```

### Option C — GitHub Actions (Auto, no Windows needed)
Push a git tag and GitHub builds it automatically:
```bash
git tag v1.0.0 && git push origin v1.0.0
# Download installer from GitHub Actions → Artifacts
```

---

## What Gets Built

| File | Description |
|------|-------------|
| `dist\KHBrowser\KHBrowser.exe` | Portable EXE (no install needed) |
| `installer_output\KHBrowser-1.0.0-Setup-Windows.exe` | Setup wizard installer |

---

## Requirements (Windows)

| Tool | Download |
|------|----------|
| Python 3.10+ | https://python.org/downloads → ☑ Add to PATH |
| Inno Setup 6 | https://jrsoftware.org/isdl.php (auto-installed by script) |

> Python packages (PyQt6, PyInstaller, etc.) are installed **automatically** by the script.

---

## Manual Steps (if scripts fail)

```batch
REM 1. Install deps
pip install PyQt6 pyinstaller requests cryptography Pillow

REM 2. Generate icons
python build_icons.py

REM 3. Build EXE
pyinstaller --clean --noconfirm --name KHBrowser ^
  --icon assets\icon.ico --windowed --add-data "assets;assets" ^
  main.py

REM 4. Build installer (requires Inno Setup installed)
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

---

## Installer Features
- ✅ Install wizard with progress bar
- ✅ Choose install folder (default: `C:\Program Files\KH Browser`)
- ✅ Start Menu shortcut
- ✅ Optional Desktop shortcut
- ✅ Add/Remove Programs entry
- ✅ Professional uninstaller
- ✅ Launch app after install
