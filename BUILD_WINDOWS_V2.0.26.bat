@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM  BUILD_WINDOWS_V2.0.26.bat
REM  KH Browser v2.0.26 Windows Installer Builder
REM  Windows 10/11 - Double-click to run
REM ═══════════════════════════════════════════════════════════════════════════

setlocal enabledelayedexpansion
color 0A
cls

echo.
echo  ╔═══════════════════════════════════════════════════════════════╗
echo  ║   KH BROWSER v2.0.26 — WINDOWS INSTALLER BUILDER             ║
echo  ║   Automated Build Process                                     ║
echo  ╚═══════════════════════════════════════════════════════════════╝
echo.

REM ── 1. Check Python ──────────────────────────────────────────────────────────
echo.
echo  [1/6] ▶ Checking Python Installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo   ❌ Python NOT FOUND!
    echo   Install from: https://www.python.org/downloads/
    echo   ☑ Check "Add Python to PATH"
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo   ✅ %PYVER% detected

REM ── 2. Verify Project Files ──────────────────────────────────────────────────
echo.
echo  [2/6] ▶ Verifying Project Files...
if not exist "main.py" (
    echo   ❌ main.py not found
    pause
    exit /b 1
)
if not exist "khbrowser.spec" (
    echo   ❌ khbrowser.spec not found
    pause
    exit /b 1
)
if not exist "installer.iss" (
    echo   ❌ installer.iss not found
    pause
    exit /b 1
)
echo   ✅ All project files found

REM ── 3. Install Dependencies ──────────────────────────────────────────────────
echo.
echo  [3/6] ▶ Installing Python Dependencies...
pip install --quiet PyQt6 pyinstaller requests cryptography Pillow
if errorlevel 1 (
    echo   ❌ pip install failed
    pause
    exit /b 1
)
echo   ✅ Dependencies installed (PyQt6, PyInstaller, etc.)

REM ── 4. Clean and Prepare ─────────────────────────────────────────────────────
echo.
echo  [4/6] ▶ Cleaning Previous Builds...
if exist "build" rmdir /s /q "build" >nul 2>&1
if exist "dist" rmdir /s /q "dist" >nul 2>&1
if exist "__pycache__" rmdir /s /q "__pycache__" >nul 2>&1
echo   ✅ Previous builds cleaned

REM ── 5. Build EXE with PyInstaller ────────────────────────────────────────────
echo.
echo  [5/6] ▶ Building Windows EXE (PyInstaller)...
echo   ⏳ This may take 3-8 minutes. Please wait...
echo.

pyinstaller khbrowser.spec --clean --noconfirm
if errorlevel 1 (
    echo.
    echo   ❌ PyInstaller build FAILED!
    echo   Check error messages above
    pause
    exit /b 1
)
echo.
echo   ✅ EXE built successfully

REM Verify EXE
if not exist "dist\KHBrowser\KHBrowser.exe" (
    echo   ❌ KHBrowser.exe not created
    pause
    exit /b 1
)

for /f %%A in ('powershell -Command "(Get-Item 'dist\KHBrowser\KHBrowser.exe').length / 1MB"') do set EXESIZE=%%A
echo   ✅ Portable EXE: dist\KHBrowser\KHBrowser.exe (%EXESIZE% MB)

REM ── 6. Create Installer with Inno Setup ──────────────────────────────────────
echo.
echo  [6/6] ▶ Creating Windows Setup Installer (Inno Setup)...
set InnoPath=C:\Program Files (x86)\Inno Setup 6\ISCC.exe

if not exist "%InnoPath%" (
    echo.
    echo   ⚠️  Inno Setup NOT found!
    echo   Install from: https://jrsoftware.org/isdl.php
    echo.
    echo   ℹ️  But your Portable EXE is ready:
    echo   → dist\KHBrowser\KHBrowser.exe (%EXESIZE% MB)
    echo.
    echo   You can distribute the portable EXE to users.
    pause
    exit /b 0
)

if not exist "installer_output" mkdir "installer_output"
"%InnoPath%" /Q installer.iss

if errorlevel 1 (
    echo   ❌ Inno Setup compilation FAILED
    echo   Check installer.iss configuration
    pause
    exit /b 1
)

REM Verify Setup installer
if not exist "installer_output\KHBrowser-2.0.26-Setup-Windows.exe" (
    echo   ❌ Setup installer not created
    pause
    exit /b 1
)

for /f %%A in ('powershell -Command "(Get-Item 'installer_output\KHBrowser-2.0.26-Setup-Windows.exe').length / 1MB"') do set SETUPSIZE=%%A
echo   ✅ Setup installer created: installer_output\KHBrowser-2.0.26-Setup-Windows.exe (%SETUPSIZE% MB)

REM ── SUCCESS ──────────────────────────────────────────────────────────────────
echo.
echo  ╔═══════════════════════════════════════════════════════════════╗
echo  ║   ✅ BUILD SUCCESSFUL - KH BROWSER v2.0.26                    ║
echo  ╠═══════════════════════════════════════════════════════════════╣
echo  ║                                                               ║
echo  ║  📦 OUTPUT FILES:                                             ║
echo  ║                                                               ║
echo  ║  1. PORTABLE EXE (No installation needed):                    ║
echo  ║     → dist\KHBrowser\KHBrowser.exe                            ║
echo  ║     Size: ~%EXESIZE% MB                                            ║
echo  ║     Use: Run directly on any Windows machine                 ║
echo  ║                                                               ║
echo  ║  2. SETUP INSTALLER (Professional installer):                ║
echo  ║     → installer_output\KHBrowser-2.0.26-Setup-Windows.exe    ║
echo  ║     Size: ~%SETUPSIZE% MB                                            ║
echo  ║     Use: Distribute to users (recommended)                   ║
echo  ║                                                               ║
echo  ║  🧪 NEXT STEPS:                                               ║
echo  ║                                                               ║
echo  ║  1. Test the portable EXE:                                    ║
echo  ║     Double-click: dist\KHBrowser\KHBrowser.exe               ║
echo  ║                                                               ║
echo  ║  2. Test the setup installer:                                ║
echo  ║     Double-click: installer_output\*.exe                     ║
echo  ║     Verify: Install completes, app runs, Add/Remove works   ║
echo  ║                                                               ║
echo  ║  3. Share with users:                                         ║
echo  ║     Portable: dist\KHBrowser\KHBrowser.exe                   ║
echo  ║     Installer: installer_output\KHBrowser-2.0.26-*.exe       ║
echo  ║                                                               ║
echo  ║  🎉 Ready for distribution!                                   ║
echo  ║                                                               ║
echo  ╚═══════════════════════════════════════════════════════════════╝
echo.

REM Open output folder
if exist "installer_output" (
    echo  Opening installer_output folder...
    start explorer.exe installer_output
)

echo.
echo  Build completed successfully!
echo.
pause
