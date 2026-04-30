@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM  build_windows_batch.bat
REM  Batch script for Windows 10/11
REM  Double-click to run (or: cmd.exe /k build_windows_batch.bat)
REM ═══════════════════════════════════════════════════════════════════════════

setlocal enabledelayedexpansion
color 0A

echo.
echo  ╔═══════════════════════════════════════════════════════════════╗
echo  ║   KH BROWSER — WINDOWS INSTALLER BUILDER                     ║
echo  ║   Version 1.0.0                                               ║
echo  ╚═══════════════════════════════════════════════════════════════╝
echo.

REM ── 1. Check Python ──────────────────────────────────────────────────────────
echo.
echo  [1/5] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo   ❌ Python not found!
    echo   Install from https://python.org
    echo   ☑ Check 'Add Python to PATH' during installation
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo   ✅  %PYVER% found

REM ── 2. Install Python deps ────────────────────────────────────────────────────
echo.
echo  [2/5] Installing Python dependencies...
pip install PyQt6 pyinstaller requests cryptography Pillow --quiet
if errorlevel 1 (
    echo   ❌ pip install failed
    pause
    exit /b 1
)
echo   ✅  Dependencies installed

REM ── 3. Generate icons ─────────────────────────────────────────────────────────
echo.
echo  [3/5] Generating application icons...
if not exist assets mkdir assets
python build_icons.py >nul 2>&1
echo   ✅  Icons ready

REM ── 4. PyInstaller build ──────────────────────────────────────────────────────
echo.
echo  [4/5] Building EXE with PyInstaller...
echo   (This may take 2-5 minutes)
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
pyinstaller khbrowser.spec --clean --noconfirm
if errorlevel 1 (
    echo   ❌ PyInstaller failed!
    pause
    exit /b 1
)
echo   ✅  EXE built: dist\KHBrowser\KHBrowser.exe

REM ── 5. Inno Setup Installer ───────────────────────────────────────────────────
echo.
echo  [5/5] Creating Windows Setup installer with Inno Setup...
set InnoPath=C:\Program Files (x86)\Inno Setup 6\ISCC.exe
if not exist "%InnoPath%" (
    echo   ⚠️   Inno Setup not found
    echo   Install from: https://jrsoftware.org/isdl.php
    echo.
    echo   ℹ️   Portable EXE is ready:
    echo   dist\KHBrowser\KHBrowser.exe
    pause
    exit /b 0
)
if not exist installer_output mkdir installer_output
"%InnoPath%" /Q installer.iss
if errorlevel 1 (
    echo   ❌ Inno Setup compilation failed
    pause
    exit /b 1
)
echo   ✅  Setup installer created in installer_output\

REM ── Done ─────────────────────────────────────────────────────────────────────
echo.
echo  ╔═══════════════════════════════════════════════════════════════╗
echo  ║   BUILD COMPLETE!                                             ║
echo  ╠═══════════════════════════════════════════════════════════════╣
echo  ║                                                               ║
echo  ║   Portable EXE:  dist\KHBrowser\KHBrowser.exe                ║
echo  ║   Setup Wizard:  installer_output\*.exe                      ║
echo  ║                                                               ║
echo  ║   🚀 Ready to distribute to users!                            ║
echo  ║                                                               ║
echo  ╚═══════════════════════════════════════════════════════════════╝
echo.

REM Open output folder
if exist installer_output start explorer.exe installer_output

pause
