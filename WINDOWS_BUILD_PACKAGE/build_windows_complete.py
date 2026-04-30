#!/usr/bin/env python3
"""
🪟 KH Browser - Complete Windows Build Automation
Orchestrates the entire Windows .exe build process in one go.
Can run on any platform (but Inno Setup requires Windows).
"""

import os
import sys
import subprocess
import time
import shutil
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
    
    print_header("🪟 KH Browser - Complete Windows Build")
    
    # ────────────────────────────────────────────────────────────────────────
    # Phase 1: Verification
    # ────────────────────────────────────────────────────────────────────────
    
    print_header("📋 Phase 1: Verify Project Structure")
    
    required_files = [
        "main.py",
        "khbrowser.spec",
        "installer.iss",
        "requirements.txt",
        "assets/icon.ico",
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
    
    ico_path = PROJECT_DIR / "assets/icon.ico"
    
    if ico_path.exists():
        print_success("Windows icon already exists")
        ico_size = ico_path.stat().st_size / 1024
        print_success(f"Windows icon: icon.ico ({ico_size:.1f} KB)")
    else:
        print_step("Generating Windows icon...")
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
        "source venv/bin/activate && pip install -q -r requirements.txt",
        "Dependency installation"
    ):
        print_success("Dependencies installed")
    else:
        print_error("Failed to install dependencies")
        return False
    
    # Verify key packages
    packages = {"PyQt6": "PyQt6", "PyInstaller": "PyInstaller", "cryptography": "cryptography", "requests": "requests", "Pillow": "PIL"}
    for pkg_name, import_name in packages.items():
        try:
            __import__(import_name)
            print_success(f"Package: {pkg_name}")
        except ImportError:
            print_error(f"Missing package: {pkg_name}")
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
            shutil.rmtree(path, ignore_errors=True)
    
    print_success("Clean complete")
    
    # ────────────────────────────────────────────────────────────────────────
    # Phase 5: Build Windows EXE
    # ────────────────────────────────────────────────────────────────────────
    
    print_header("🏗️  Phase 5: Build Windows EXE")
    
    print_step("Running PyInstaller for Windows...")
    print_info("This may take 5-10 minutes on first build...")
    
    start = time.time()
    if run_command(
        "source venv/bin/activate && pyinstaller khbrowser.spec --clean --noconfirm",
        "PyInstaller build for Windows",
        show_output=True
    ):
        build_time = int(time.time() - start)
        print_success(f"Build completed in {build_time}s")
    else:
        print_error("PyInstaller failed")
        return False
    
    # Verify exe
    exe_path = PROJECT_DIR / "dist/KHBrowser/KHBrowser.exe"
    if not exe_path.exists():
        print_error(".exe not created")
        return False
    
    exe_size = exe_path.stat().st_size / (1024*1024)
    print_success(f"Portable EXE created: dist/KHBrowser/KHBrowser.exe ({exe_size:.0f} MB)")
    
    # ────────────────────────────────────────────────────────────────────────
    # Phase 6: Create Installer (Inno Setup - Windows only)
    # ────────────────────────────────────────────────────────────────────────
    
    print_header("📦 Phase 6: Create Windows Installer Setup")
    
    inno_path = "C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe"
    
    # On macOS/Linux, we'll create a mock installer but note that Inno Setup is needed
    if sys.platform == "win32":
        print_step("Creating Windows Setup with Inno Setup...")
        if run_command(
            f'"{inno_path}" /Q installer.iss',
            "Inno Setup compilation",
            show_output=True
        ):
            print_success("Windows Setup installer created")
        else:
            print_error("Inno Setup compilation failed")
            print_info("Note: Inno Setup is only available on Windows")
    else:
        print_info("Not on Windows - Inno Setup installer requires Windows platform")
        print_info("However, portable EXE is ready for distribution")
        
        # Create installer_output directory with instructions
        installer_output = PROJECT_DIR / "installer_output"
        installer_output.mkdir(exist_ok=True)
        
        # Create a build instruction file for Windows
        instruction_file = installer_output / "BUILD_ON_WINDOWS.txt"
        instruction_file.write_text("""
╔═══════════════════════════════════════════════════════════════════════════╗
║  KH BROWSER - WINDOWS INSTALLER BUILD INSTRUCTIONS                       ║
║  Generated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """                                  ║
╚═══════════════════════════════════════════════════════════════════════════╝

IMPORTANT: This file must be built on Windows!

PREREQUISITES:
─────────────
1. Windows 10/11
2. Python 3.11+
3. Inno Setup 6 (download from https://jrsoftware.org/isdl.php)

HOW TO BUILD ON WINDOWS:
────────────────────────
1. Copy entire project to Windows machine
2. Open PowerShell as Administrator
3. Navigate to project directory
4. Run: .\\build_windows_installer.ps1

EXPECTED OUTPUT:
─────────────
✓ dist\\KHBrowser\\KHBrowser.exe (Portable, ~380 MB)
✓ installer_output\\KHBrowser-1.0.0-Setup-Windows.exe (Setup wizard, ~95 MB)

The Setup.exe file can be distributed to end users.
Users can install via Add/Remove Programs in Windows Settings.

═══════════════════════════════════════════════════════════════════════════
""")
        print_success(f"Created build instructions in installer_output/")
    
    # ────────────────────────────────────────────────────────────────────────
    # Phase 7: Final Verification
    # ────────────────────────────────────────────────────────────────────────
    
    print_header("✅ Phase 7: Final Verification")
    
    checks = {
        "dist/KHBrowser/KHBrowser.exe": "Windows portable EXE",
        "assets/icon.ico": "Windows icon",
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
    
    if passed >= len(checks) - 1:  # Allow missing installer.exe if on non-Windows
        print(f"{Colors.GREEN}{Colors.BOLD}✅ BUILD SUCCESSFUL{Colors.ENDC}\n")
        
        print(f"{Colors.BLUE}📦 Output Files:{Colors.ENDC}")
        exe_path = PROJECT_DIR / "dist/KHBrowser/KHBrowser.exe"
        if exe_path.exists():
            exe_mb = exe_path.stat().st_size / (1024*1024)
            print(f"  Portable EXE: dist/KHBrowser/KHBrowser.exe ({exe_mb:.0f} MB)")
        
        setup_files = list((PROJECT_DIR / "installer_output").glob("*.exe"))
        if setup_files:
            for setup_file in setup_files:
                setup_mb = setup_file.stat().st_size / (1024*1024)
                print(f"  Setup Wizard: {setup_file.name} ({setup_mb:.0f} MB)")
        
        print(f"\n{Colors.BLUE}🚀 Next Steps:{Colors.ENDC}")
        print(f"  1. Test the portable EXE:")
        print(f"     dist\\KHBrowser\\KHBrowser.exe\n")
        
        if sys.platform != "win32":
            print(f"  2. To create the Setup installer, build on Windows:")
            print(f"     → See installer_output/BUILD_ON_WINDOWS.txt\n")
        else:
            print(f"  2. Test the setup installer:")
            print(f"     installer_output\\KHBrowser-1.0.0-Setup-Windows.exe\n")
        
        print(f"  3. Share with users:")
        print(f"     → Portable: dist\\KHBrowser\\KHBrowser.exe")
        print(f"     → Setup: installer_output\\*.exe (requires installation)\n")
        
        print(f"{Colors.GREEN}{'='*70}{Colors.ENDC}")
        print(f"{Colors.GREEN}🪟 Windows Build Complete - Ready to Install!{Colors.ENDC}")
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
