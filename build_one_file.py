#!/usr/bin/env python3
"""
Build KH Browser as a single .exe file (one-file)
Cross-platform build script that works on Windows

Usage:
  python build_one_file.py

Result:
  - Builds: dist/KHBrowser.exe (single standalone file)
  - No installation needed
  - Ready to distribute to users
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    width = 80
    print(f"\n{'='*width}")
    print(f"  {text}")
    print(f"{'='*width}\n")

def run_command(cmd, description=""):
    """Execute command and handle errors"""
    if description:
        print(f"✅ {description}")
    print(f"   Command: {cmd}\n")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"\n❌ Error: {description}")
        return False
    return True

def check_python():
    """Check Python installation"""
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"✅ Python found: {py_version}")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    return True

def check_files():
    """Check required files exist"""
    required = ['main.py', 'assets/icon.ico', 'qr/qr.jpg']
    missing = [f for f in required if not Path(f).exists()]
    
    if missing:
        print(f"❌ Missing files: {', '.join(missing)}")
        return False
    print("✅ All required files found:")
    for f in required:
        print(f"   • {f}")
    return True

def install_pyinstaller():
    """Install PyInstaller"""
    print("\n📦 Installing PyInstaller...")
    if not run_command(
        f"{sys.executable} -m pip install --upgrade pip pyinstaller",
        "Installing PyInstaller"
    ):
        return False
    return True

def clean_builds():
    """Clean previous builds"""
    print("\n🧹 Cleaning previous builds...")
    for folder in ['build', 'dist', '__pycache__']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"   Removed: {folder}/")
    return True

def build_one_file():
    """Build one-file executable"""
    print("\n🏗️  Building KHBrowser.exe (one-file, windowed)...\n")
    
    cmd = (
        f'{sys.executable} -m PyInstaller '
        '--onefile '
        '--windowed '
        '--icon=assets/icon.ico '
        '--name=KHBrowser '
        '--add-data="assets:assets" '
        '--add-data="qr:qr" '
        '--hidden-import=PyQt6 '
        '--hidden-import=PyQt6.QtCore '
        '--hidden-import=PyQt6.QtGui '
        '--hidden-import=PyQt6.QtWidgets '
        '--hidden-import=PyQt6.QtNetwork '
        '--hidden-import=cryptography '
        '--hidden-import=requests '
        '--hidden-import=json '
        '--hidden-import=subprocess '
        '--hidden-import=threading '
        '--hidden-import=uuid '
        '--hidden-import=datetime '
        '--hidden-import=main_window '
        '--hidden-import=dashboard_panel '
        '--hidden-import=groups_panel '
        '--hidden-import=profile_dialog '
        '--hidden-import=team_dialog '
        '--hidden-import=browser_launcher '
        '--hidden-import=storage '
        '--hidden-import=models '
        '--hidden-import=styles '
        '--hidden-import=rpa_dialog '
        '--hidden-import=batch_dialog '
        '--hidden-import=settings_dialog '
        '--hidden-import=api_dialog '
        '--hidden-import=assets '
        '--hidden-import=video_creator_qt '
        '--hidden-import=video_creator_panel '
        'main.py'
    )
    
    return run_command(cmd, "Building executable")

def verify_build():
    """Verify build output"""
    exe_path = Path('dist') / 'KHBrowser.exe'
    
    if exe_path.exists():
        size_bytes = exe_path.stat().st_size
        size_mb = size_bytes / (1024 * 1024)
        
        print_header("✅ BUILD SUCCESSFUL!")
        print(f"📄 Output file: {exe_path}")
        print(f"📊 File size: {size_mb:.1f} MB ({size_bytes:,} bytes)")
        print("\n🚀 Ready to distribute!")
        print("   • Share dist/KHBrowser.exe with users")
        print("   • No installation needed")
        print("   • Double-click to launch")
        print(f"\n📋 Project: KH Browser v2.0.26")
        print(f"📦 Platform: Windows")
        print(f"📝 Build Type: One-File Standalone Executable")
        return True
    else:
        print("\n❌ BUILD FAILED - dist/KHBrowser.exe not found")
        return False

def main():
    """Main build process"""
    print_header("🔨 KH Browser - Build One-File .exe")
    
    # Check platform
    system = platform.system()
    print(f"System: {system}")
    if system != "Windows":
        print("\n⚠️  WARNING: This build is optimized for Windows!")
        print("   To build .exe files, run this script on Windows.")
        print("   On macOS/Linux, use: python BUILD.py macos")
    print()
    
    # Step 1: Check Python
    if not check_python():
        return 1
    
    # Step 2: Check files
    print()
    if not check_files():
        return 1
    
    # Step 3: Install PyInstaller
    if not install_pyinstaller():
        return 1
    
    # Step 4: Clean previous builds
    clean_builds()
    
    # Step 5: Build
    if not build_one_file():
        return 1
    
    # Step 6: Verify
    if not verify_build():
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
