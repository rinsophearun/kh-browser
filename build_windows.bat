@echo off
REM ─────────────────────────────────────────────────────────────────
REM  build_windows.bat  —  Build KHBrowser.exe for Windows
REM ─────────────────────────────────────────────────────────────────

set APP_NAME=KHBrowser
set VERSION=1.0.0

echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║   KH Browser — Windows Build                ║
echo ╚══════════════════════════════════════════════════════╝
echo.

REM 1. Clean previous build
echo ^> Cleaning previous build...
if exist build\ rmdir /s /q build
if exist dist\ rmdir /s /q dist
del /s /q *.pyc 2>nul

REM 2. Install dependencies
echo ^> Installing Python dependencies...
pip install PyQt6 pyinstaller requests cryptography -q
if errorlevel 1 (
    echo ERROR: pip install failed. Is Python in PATH?
    pause
    exit /b 1
)

REM 3. Build with PyInstaller (Windows: one-file EXE)
echo ^> Building single-file .exe with PyInstaller...
pyinstaller ^
    --clean ^
    --noconfirm ^
    --onefile ^
    --windowed ^
    --name "%APP_NAME%" ^
    --icon "assets\icon.ico" ^
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
    echo ERROR: PyInstaller build failed!
    pause
    exit /b 1
)

echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║   BUILD COMPLETE                                     ║
echo ╠══════════════════════════════════════════════════════╣
echo ║                                                      ║
echo ║   Output: dist\%APP_NAME%.exe                        ║
echo ╚══════════════════════════════════════════════════════╝
echo.
echo Double-click dist\%APP_NAME%.exe to run
echo.
pause
