#!/usr/bin/env python3
"""
🍎 KH Browser - Complete macOS Build Automation
Orchestrates the entire build process in one go.
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime

# Configuration
PROJECT_DIR = Path("/Users/sophearun/Projects/KH browser")
BUILD_LOG = PROJECT_DIR / "build.log"

# Color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Print section header."""
    print(f"\n{Colors.BLUE}{'='*70}{Colors.ENDC}")
    print(f"{Colors.BLUE}{text:^70}{Colors.ENDC}")
    print(f"{Colors.BLUE}{'='*70}{Colors.ENDC}\n")

def print_step(text):
    """Print step."""
    print(f"{Colors.YELLOW}▶ {text}{Colors.ENDC}")

def print_success(text):
    """Print success message."""
    print(f"{Colors.GREEN}✅ {text}{Colors.ENDC}")

def print_error(text):
    """Print error message."""
    print(f"{Colors.RED}❌ {text}{Colors.ENDC}")

def print_info(text):
    """Print info message."""
    print(f"{Colors.CYAN}ℹ️  {text}{Colors.ENDC}")

def run_command(cmd, description="", show_output=False):
    """Run shell command and return success status."""
    try:
        if show_output:
            print_step(description if description else "Running command...")
            result = subprocess.run(cmd, cwd=str(PROJECT_DIR), shell=True, check=True)
            return result.returncode == 0
        else:
            result = subprocess.run(
                cmd,
                cwd=str(PROJECT_DIR),
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
            return True
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed: {description}")
        if e.stderr:
            print(f"Error: {e.stderr[:500]}")
        return False

def main():
    """Main build orchestration."""
    
    os.chdir(PROJECT_DIR)
    
    print_header("🍎 KH Browser - Complete macOS Build")
    
    # ────────────────────────────────────────────────────────────────────────
    # Phase 1: Verification
    # ────────────────────────────────────────────────────────────────────────
    
    print_header("📋 Phase 1: Verify Project Structure")
    
    required_files = [
        "main.py",
        "khbrowser.spec",
        "build_macos.sh",
        "entitlements.plist",
        "requirements.txt",
        "assets/Logo.png",
        "runtime_hooks/hook_pyqt6_fix.py",
    ]
    
    missing = []
    for file in required_files:
        path = PROJECT_DIR / file
        if path.exists():
            print_success(f"Found: {file}")
        else:
            print_error(f"Missing: {file}")
            missing.append(file)
    
    if missing:
        print_error(f"Cannot proceed - missing {len(missing)} files")
        return False
    
    print_success("All required files present")
    
    # ────────────────────────────────────────────────────────────────────────
    # Phase 2: Generate Icons
    # ────────────────────────────────────────────────────────────────────────
    
    print_header("📦 Phase 2: Generate Application Icons")
    
    icns_path = PROJECT_DIR / "assets/icon.icns"
    ico_path = PROJECT_DIR / "assets/icon.ico"
    
    if icns_path.exists() and ico_path.exists():
        print_success("Icons already exist")
        icns_size = icns_path.stat().st_size / (1024*1024)
        ico_size = ico_path.stat().st_size / 1024
        print_success(f"macOS icon: icon.icns ({icns_size:.1f} MB)")
        print_success(f"Windows icon: icon.ico ({ico_size:.1f} KB)")
    else:
        print_step("Generating icons...")
        if run_command(
            "python3 generate_icons_advanced.py",
            "Icon generation",
            show_output=True
        ):
            print_success("Icons generated")
        else:
            print_error("Icon generation failed")
            return False
    
    # ────────────────────────────────────────────────────────────────────────
    # Phase 3: Install Dependencies
    # ────────────────────────────────────────────────────────────────────────
    
    print_header("📚 Phase 3: Install Dependencies")
    
    print_step("Installing Python packages...")
    if run_command(
        "pip3 install -q -r requirements.txt",
        "Dependency installation"
    ):
        print_success("Dependencies installed")
    else:
        print_error("Failed to install dependencies")
        return False
    
    # Verify key packages
    packages = ["PyQt6", "pyinstaller", "cryptography", "requests"]
    for pkg in packages:
        try:
            __import__(pkg.replace("-", "_"))
            print_success(f"Package: {pkg}")
        except ImportError:
            print_error(f"Missing package: {pkg}")
            return False
    
    # ────────────────────────────────────────────────────────────────────────
    # Phase 4: Clean Previous Builds
    # ────────────────────────────────────────────────────────────────────────
    
    print_header("🧹 Phase 4: Clean Previous Builds")
    
    print_step("Removing old build artifacts...")
    for dirpath in ["build", "dist"]:
        path = PROJECT_DIR / dirpath
        if path.exists():
            print_info(f"Removing {dirpath}/...")
            import shutil
            shutil.rmtree(path, ignore_errors=True)
    
    print_success("Clean complete")
    
    # ────────────────────────────────────────────────────────────────────────
    # Phase 5: Build macOS Application
    # ────────────────────────────────────────────────────────────────────────
    
    print_header("🏗️  Phase 5: Build macOS Application")
    
    print_step("Running PyInstaller...")
    print_info("This may take 5-10 minutes on first build...")
    
    start = time.time()
    if run_command(
        "pyinstaller khbrowser.spec",
        "PyInstaller build",
        show_output=True
    ):
        build_time = int(time.time() - start)
        print_success(f"Build completed in {build_time}s")
    else:
        print_error("PyInstaller failed")
        return False
    
    # Verify app bundle
    app_path = PROJECT_DIR / "dist/KHBrowser.app"
    if not app_path.exists():
        print_error(".app bundle not created")
        return False
    
    app_size = sum(p.stat().st_size for p in app_path.rglob('*')) / (1024*1024)
    print_success(f"App bundle created: dist/KHBrowser.app ({app_size:.0f} MB)")
    
    # ────────────────────────────────────────────────────────────────────────
    # Phase 6: Create DMG Installer
    # ────────────────────────────────────────────────────────────────────────
    
    print_header("📦 Phase 6: Create DMG Installer")
    
    dmg_file = "dist/KHBrowser-1.0.0-macOS.dmg"
    
    print_step("Creating DMG with LZMA2 compression...")
    print_info("This may take 2-3 minutes...")
    
    if run_command(
        f'hdiutil create -volname "KHBrowser 1.0.0" -srcfolder dist/KHBrowser.app -ov -format ULMO {dmg_file}',
        "DMG creation",
        show_output=True
    ):
        dmg_path = PROJECT_DIR / dmg_file
        dmg_size = dmg_path.stat().st_size / (1024*1024*1024)
        print_success(f"DMG created: {dmg_file} ({dmg_size:.1f} GB)")
    else:
        print_error("DMG creation failed")
        return False
    
    # ────────────────────────────────────────────────────────────────────────
    # Phase 7: Final Verification
    # ────────────────────────────────────────────────────────────────────────
    
    print_header("✅ Phase 7: Final Verification")
    
    checks = {
        "dist/KHBrowser.app/Contents/MacOS/KHBrowser": ".app executable",
        "dist/KHBrowser-1.0.0-macOS.dmg": ".dmg installer",
        "dist/KHBrowser.app/Contents/Resources/icon.icns": "App icon",
    }
    
    passed = 0
    for file, desc in checks.items():
        path = PROJECT_DIR / file
        if path.exists():
            print_success(desc)
            passed += 1
        else:
            print_error(f"{desc} NOT found")
    
    # ────────────────────────────────────────────────────────────────────────
    # Final Report
    # ────────────────────────────────────────────────────────────────────────
    
    print_header("📊 BUILD COMPLETE - FINAL REPORT")
    
    if passed == len(checks):
        print(f"{Colors.GREEN}{Colors.BOLD}✅ BUILD SUCCESSFUL{Colors.ENDC}\n")
        
        print(f"{Colors.BLUE}📦 Output Files:{Colors.ENDC}")
        print(f"  .app bundle:    dist/KHBrowser.app ({app_size:.0f} MB)")
        dmg_path = PROJECT_DIR / "dist/KHBrowser-1.0.0-macOS.dmg"
        dmg_mb = dmg_path.stat().st_size / (1024*1024)
        print(f"  .dmg installer: dist/KHBrowser-1.0.0-macOS.dmg ({dmg_mb:.0f} MB)\n")
        
        print(f"{Colors.BLUE}🚀 Next Steps:{Colors.ENDC}")
        print(f"  1. Open the DMG:")
        print(f"     open 'dist/KHBrowser-1.0.0-macOS.dmg'\n")
        print(f"  2. Drag KHBrowser.app to Applications folder\n")
        print(f"  3. Run from Applications or Spotlight: KH Browser\n")
        
        print(f"{Colors.BLUE}Or launch directly:{Colors.ENDC}")
        print(f"  open 'dist/KHBrowser.app'\n")
        
        print(f"{Colors.GREEN}{'='*70}{Colors.ENDC}")
        print(f"{Colors.GREEN}🍎 macOS Build Complete - Ready to Install!{Colors.ENDC}")
        print(f"{Colors.GREEN}{'='*70}{Colors.ENDC}\n")
        
        return True
    else:
        print_error("Some verification checks failed")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print_error("\n\nBuild cancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
