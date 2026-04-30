#!/usr/bin/env python3
"""
Build KH Browser .exe to custom output directory
Outputs to: /Users/sophearun/Desktop/build/

Usage:
  python build_to_desktop.py
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_header(text):
    width = 80
    print(f"\n{'='*width}")
    print(f"  {text}")
    print(f"{'='*width}\n")

def main():
    print_header("🔨 Build KH Browser .exe to Desktop")
    
    # Setup paths
    output_dir = Path.home() / "Desktop" / "build"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Output directory: {output_dir}")
    print(f"✅ Directory ready\n")
    
    # Step 1: Install PyInstaller
    print("📦 Installing PyInstaller...")
    result = subprocess.run(
        f"{sys.executable} -m pip install --upgrade pyinstaller",
        shell=True,
        capture_output=True
    )
    if result.returncode != 0:
        print("❌ Failed to install PyInstaller")
        print(result.stderr.decode())
        return 1
    print("✅ PyInstaller installed\n")
    
    # Step 2: Clean previous builds
    print("🧹 Cleaning previous builds...")
    for folder in ['build', 'dist', '__pycache__']:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"   Removed: {folder}/")
    print("✅ Cleanup complete\n")
    
    # Step 3: Build one-file .exe
    print("🏗️  Building KHBrowser.exe (one-file)...\n")
    
    cmd = (
        f'{sys.executable} -m PyInstaller '
        '--onefile '
        '--windowed '
        '--icon=assets/icon.ico '
        '--name=KHBrowser '
        '--add-data="assets:assets" '
        '--add-data="qr:qr" '
        '--distpath="{output_dir}/dist" '
        '--buildpath="{output_dir}/build" '
        '--specpath="{output_dir}" '
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
    
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print("\n❌ Build failed")
        return 1
    
    # Step 4: Verify output
    print("\n" + "="*80)
    exe_path = output_dir / "dist" / "KHBrowser.exe"
    
    if exe_path.exists():
        size_bytes = exe_path.stat().st_size
        size_mb = size_bytes / (1024 * 1024)
        
        print_header("✅ BUILD SUCCESSFUL!")
        print(f"📄 Output file: {exe_path}")
        print(f"📊 File size: {size_mb:.1f} MB ({size_bytes:,} bytes)")
        print(f"\n🎯 Location: ~/Desktop/build/dist/KHBrowser.exe")
        print(f"\n🚀 Ready to use!")
        print(f"   • Open in Finder: {output_dir}")
        print(f"   • Share dist/KHBrowser.exe with users")
        print(f"   • No installation needed")
        print(f"   • Double-click to run")
        print(f"\n📋 Project: KH Browser v2.0.26")
        print(f"�� Platform: Windows Standalone")
        print(f"📝 Build Type: One-File Executable\n")
        return 0
    else:
        print(f"❌ BUILD FAILED - {exe_path} not found")
        return 1

if __name__ == "__main__":
    sys.exit(main())
