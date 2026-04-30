@echo off
REM ════════════════════════════════════════════════════════════════════════════
REM  KH Browser - Build One-File .exe on Windows
REM  Usage: build_one_file.bat
REM  ✅ Installs PyInstaller
REM  ✅ Builds single KHBrowser.exe file
REM  ✅ No dependencies needed
REM ════════════════════════════════════════════════════════════════════════════

setlocal enabledelayedexpansion

echo.
echo ════════════════════════════════════════════════════════════════════════════
echo  🔨 KH Browser - Build One-File .exe
echo ════════════════════════════════════════════════════════════════════════════
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo    Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo ✅ Python found:
python --version

REM Step 1: Install PyInstaller
echo.
echo 📦 Installing PyInstaller...
pip install --upgrade pip >nul 2>&1
pip install pyinstaller
if errorlevel 1 (
    echo ❌ Failed to install PyInstaller
    pause
    exit /b 1
)

REM Step 2: Clean previous builds
echo.
echo 🧹 Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist KHBrowser.spec del KHBrowser.spec
echo    Cleanup complete

REM Step 3: Build one-file .exe
echo.
echo 🏗️  Building KHBrowser.exe (one-file, windowed, with icon and assets)...
echo.

pyinstaller ^
  --onefile ^
  --windowed ^
  --icon=assets\icon.ico ^
  --name=KHBrowser ^
  --add-data="assets;assets" ^
  --add-data="qr;qr" ^
  --hidden-import=PyQt6 ^
  --hidden-import=PyQt6.QtCore ^
  --hidden-import=PyQt6.QtGui ^
  --hidden-import=PyQt6.QtWidgets ^
  --hidden-import=PyQt6.QtNetwork ^
  --hidden-import=cryptography ^
  --hidden-import=requests ^
  --hidden-import=json ^
  --hidden-import=subprocess ^
  --hidden-import=threading ^
  --hidden-import=uuid ^
  --hidden-import=datetime ^
  --hidden-import=main_window ^
  --hidden-import=dashboard_panel ^
  --hidden-import=groups_panel ^
  --hidden-import=profile_dialog ^
  --hidden-import=team_dialog ^
  --hidden-import=browser_launcher ^
  --hidden-import=storage ^
  --hidden-import=models ^
  --hidden-import=styles ^
  --hidden-import=rpa_dialog ^
  --hidden-import=batch_dialog ^
  --hidden-import=settings_dialog ^
  --hidden-import=api_dialog ^
  --hidden-import=assets ^
  --hidden-import=video_creator_qt ^
  --hidden-import=video_creator_panel ^
  main.py

if errorlevel 1 (
    echo.
    echo ❌ Build failed
    pause
    exit /b 1
)

REM Step 4: Verify output
echo.
if exist "dist\KHBrowser.exe" (
    echo ════════════════════════════════════════════════════════════════════════════
    echo ✅ BUILD SUCCESSFUL!
    echo ════════════════════════════════════════════════════════════════════════════
    echo.
    echo 📄 Output file: dist\KHBrowser.exe
    echo 📊 File size: 
    for %%A in (dist\KHBrowser.exe) do echo    %%~zA bytes (%%~sA)
    echo.
    echo 🚀 Ready to distribute! You can:
    echo    • Share dist\KHBrowser.exe with users
    echo    • No installation needed - it runs standalone
    echo    • Double-click to launch
    echo.
    echo 📋 Project: KH Browser v2.0.26
    echo 📦 Platform: Windows
    echo 📝 Build Type: One-File Standalone Executable
    echo.
    pause
) else (
    echo ❌ BUILD FAILED - dist\KHBrowser.exe not found
    pause
    exit /b 1
)

endlocal
