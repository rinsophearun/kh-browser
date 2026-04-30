@echo off
REM ═══════════════════════════════════════════════════════════════════════════
REM  KH BROWSER v2.0.0 - WINDOWS INSTALLER BUILD
REM  
REM  One-click build script for Windows
REM  This script will:
REM    1. Create virtual environment
REM    2. Install dependencies
REM    3. Build portable EXE with PyInstaller
REM    4. Create installer with Inno Setup
REM ═══════════════════════════════════════════════════════════════════════════

setlocal enabledelayedexpansion

echo.
echo ╔═══════════════════════════════════════════════════════════════════════════╗
echo ║            KH BROWSER v2.0.0 - WINDOWS BUILD STARTING                     ║
echo ╚═══════════════════════════════════════════════════════════════════════════╝
echo.

REM Check Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Python not found!
    echo.
    echo Please install Python 3.11+ from: https://www.python.org/downloads/
    echo ⚠️  Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Check Inno Setup is installed
echo Checking Inno Setup installation...
if not exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    echo.
    echo ⚠️  WARNING: Inno Setup 6 not found
    echo.
    echo Inno Setup is required to create the installer.
    echo Download from: https://jrsoftware.org/isdl.php
    echo.
    echo For now, we can still create the portable EXE.
    echo Continue anyway? (Y/N)
    set /p choice=
    if /i not "!choice!"=="Y" exit /b 1
)

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install dependencies
echo.
echo Installing Python dependencies...
echo This may take 3-5 minutes...
echo.
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

REM Run build script
echo.
echo Starting build process...
echo This will take 10-15 minutes...
echo.
python build_windows_complete.py

if errorlevel 1 (
    echo.
    echo ❌ Build failed!
    echo.
    pause
    exit /b 1
)

echo.
echo ╔═══════════════════════════════════════════════════════════════════════════╗
echo ║                    ✅ BUILD COMPLETED SUCCESSFULLY!                        ║
echo ╚═══════════════════════════════════════════════════════════════════════════╝
echo.
echo Your installers are ready:
echo.
echo 📦 PORTABLE (no installation required):
echo    dist\KHBrowser\KHBrowser.exe  (~380 MB)
echo.
echo 📦 INSTALLER (setup wizard):
echo    installer_output\KHBrowser-2.0.0-Setup-Windows.exe  (~95 MB)
echo.
echo Next steps:
echo   1. Test the portable EXE by double-clicking it
echo   2. Test the installer by double-clicking it
echo   3. Share the files with users
echo.
pause
