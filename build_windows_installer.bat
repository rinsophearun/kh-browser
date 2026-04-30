@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM  build_windows_installer.bat
REM  KH Browser v2.0.0 - One-click Windows Installer Builder
REM  Python deps → PyInstaller EXE → Inno Setup installer
REM  Run this on Windows 10/11 with Python 3.11+ installed
REM ═══════════════════════════════════════════════════════════════════════════

setlocal EnableDelayedExpansion
set APP_NAME=KHBrowser
set VERSION=2.0.0
set INNO_DEFAULT=C:\Program Files (x86)\Inno Setup 6\ISCC.exe

echo.
echo  ╔═══════════════════════════════════════════════════════════════╗
echo  ║   KH BROWSER v%VERSION% — Windows Installer Builder             ║
echo  ║   Portable EXE + Setup Wizard                                 ║
echo  ╚═══════════════════════════════════════════════════════════════╝
echo.

REM ── Step 1: Check Python ─────────────────────────────────────────────────
echo [1/5] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  ERROR: Python not found in PATH!
    echo  Download Python 3.12+ from https://www.python.org/downloads/
    echo  Make sure to check "Add Python to PATH" during install.
    echo.
    pause & exit /b 1
)
for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PY_VER=%%v
echo  ✓ Python %PY_VER% found

REM ── Step 2: Install dependencies ─────────────────────────────────────────
echo.
echo [2/5] Installing Python dependencies...
pip install PyQt6 PyInstaller requests cryptography Pillow --quiet
if errorlevel 1 (
    echo  ERROR: pip install failed!
    pause & exit /b 1
)
echo  ✓ Dependencies installed

REM ── Step 3: Generate icons ────────────────────────────────────────────────
echo.
echo [3/5] Verifying icons and assets...
if not exist "assets\icon.ico" (
    echo  WARNING: assets\icon.ico not found
)
if not exist "qr\qr.jpg" (
    echo  WARNING: qr\qr.jpg not found
)
echo  ✓ Assets verified

REM ── Step 4: Build .exe with PyInstaller ──────────────────────────────────
echo.
echo [4/5] Building .exe with PyInstaller (this takes 2-5 minutes)...
if exist build\ rmdir /s /q build
if exist dist\ rmdir /s /q dist

pyinstaller ^
    --clean ^
    --noconfirm ^
    --name "%APP_NAME%" ^
    --icon "assets\icon.ico" ^
    --windowed ^
    --add-data "assets;assets" ^
    --hidden-import PyQt6.QtCore ^
    --hidden-import PyQt6.QtGui ^
    --hidden-import PyQt6.QtWidgets ^
    --hidden-import PyQt6.QtNetwork ^
    --hidden-import cryptography ^
    --hidden-import requests ^
    --hidden-import main_window ^
    --hidden-import dashboard_panel ^
    --hidden-import groups_panel ^
    --hidden-import profile_dialog ^
    --hidden-import team_dialog ^
    --hidden-import browser_launcher ^
    --hidden-import storage ^
    --hidden-import models ^
    --hidden-import styles ^
    --hidden-import rpa_dialog ^
    --hidden-import batch_dialog ^
    --hidden-import settings_dialog ^
    --hidden-import api_dialog ^
    --exclude-module tkinter ^
    --exclude-module matplotlib ^
    --exclude-module numpy ^
    --log-level WARN ^
    main.py

if errorlevel 1 (
    echo.
    echo  ERROR: PyInstaller build failed!
    pause & exit /b 1
)
echo  ✓ EXE built: dist\%APP_NAME%.exe

REM ── Step 5: Create Setup Installer with Inno Setup ───────────────────────
echo.
echo [5/5] Creating Windows Setup installer...

REM Auto-detect Inno Setup location
set ISCC=""
if exist "%INNO_DEFAULT%" set ISCC="%INNO_DEFAULT%"
if exist "C:\Program Files\Inno Setup 6\ISCC.exe" set ISCC="C:\Program Files\Inno Setup 6\ISCC.exe"

REM Try to download Inno Setup if not found
if %ISCC%=="" (
    echo  Inno Setup not found. Attempting to install via winget...
    winget install JRSoftware.InnoSetup --silent 2>nul
    timeout /t 5 /nobreak >nul
    if exist "%INNO_DEFAULT%" set ISCC="%INNO_DEFAULT%"
)

if %ISCC%=="" (
    echo.
    echo  ⚠  Inno Setup not found!
    echo     Download from: https://jrsoftware.org/isdl.php
    echo     Install it, then re-run this script.
    echo.
    echo  OR: Your EXE is already at dist\%APP_NAME%.exe
    echo      You can distribute that file directly.
    echo.
    pause & exit /b 0
)

if not exist "installer_output\" mkdir installer_output
%ISCC% /Q installer.iss
if errorlevel 1 (
    echo  ERROR: Inno Setup compilation failed!
    pause & exit /b 1
)

REM ── Done ─────────────────────────────────────────────────────────────────
echo.
echo  ╔═══════════════════════════════════════════════════════════════╗
echo  ║   BUILD COMPLETE — KH Browser v%VERSION%                        ║
echo  ╠═══════════════════════════════════════════════════════════════╣
echo  ║                                                               ║
echo  ║   📦 Portable EXE (~380 MB):                                 ║
echo  ║      dist\%APP_NAME%\%APP_NAME%.exe                          ║
echo  ║      (No installation required - run directly)               ║
echo  ║                                                               ║
echo  ║   🪟 Windows Installer (~95 MB):                             ║
echo  ║      installer_output\%APP_NAME%-%VERSION%-Setup.exe         ║
echo  ║      (Setup wizard for traditional installation)             ║
echo  ║                                                               ║
echo  ║   ✨ Features Included:                                       ║
echo  ║      • Open All / Close All buttons                          ║
echo  ║      • Donate button with QR code                            ║
echo  ║      • Update button                                         ║
echo  ║      • Settings tab (7 options)                              ║
echo  ║      • Real-time auto-refresh                                ║
echo  ║                                                               ║
echo  ║   ✅ Both files ready for distribution to users!             ║
echo  ╚═══════════════════════════════════════════════════════════════╝
echo.

REM Open output folder
explorer installer_output
pause
