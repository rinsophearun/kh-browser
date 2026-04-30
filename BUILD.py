#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════╗
║  KH BROWSER v2.0.0 - UNIVERSAL BUILD SCRIPT                              ║
║  Builds for both Windows and macOS with full installation packages       ║
║  Usage: python BUILD.py [windows|macos|all]                             ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
import platform
import json

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

PROJECT_DIR = Path(__file__).parent
APP_NAME = "KH Browser"
APP_VERSION = "2.0.0"
CURRENT_PLATFORM = platform.system()

# Color codes for terminal output
class Color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Print colored header."""
    print(f"\n{Color.BLUE}{'='*75}{Color.ENDC}")
    print(f"{Color.BLUE}{text:^75}{Color.ENDC}")
    print(f"{Color.BLUE}{'='*75}{Color.ENDC}\n")

def print_step(text):
    """Print step."""
    print(f"{Color.YELLOW}▶ {text}{Color.ENDC}")

def print_success(text):
    """Print success message."""
    print(f"{Color.GREEN}✅ {text}{Color.ENDC}")

def print_error(text):
    """Print error message."""
    print(f"{Color.RED}❌ {text}{Color.ENDC}")

def print_info(text):
    """Print info message."""
    print(f"{Color.CYAN}ℹ️  {text}{Color.ENDC}")

def run_cmd(cmd, description="", show_output=True):
    """Run shell command."""
    try:
        if show_output:
            print_step(description if description else "Running...")
            subprocess.run(cmd, cwd=str(PROJECT_DIR), shell=True, check=True)
            return True
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

# ═══════════════════════════════════════════════════════════════════════════
# STEP 1: VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════

def verify_project():
    """Verify all required files exist."""
    print_header("📋 STEP 1: Verify Project Structure")
    
    required = [
        "main.py",
        "main_window.py",
        "models.py",
        "khbrowser.spec",
        "installer.iss",
        "requirements.txt",
        "assets/icon.ico",
        "qr/qr.jpg",
    ]
    
    missing = []
    for file in required:
        path = PROJECT_DIR / file
        if path.exists():
            print_success(f"Found: {file}")
        else:
            print_error(f"Missing: {file}")
            missing.append(file)
    
    if missing:
        print_error(f"Cannot proceed - missing {len(missing)} files")
        return False
    
    print_success("All required files verified")
    return True

# ═══════════════════════════════════════════════════════════════════════════
# STEP 2: CLEAN PREVIOUS BUILDS
# ═══════════════════════════════════════════════════════════════════════════

def clean_builds():
    """Clean previous build artifacts."""
    print_header("🧹 STEP 2: Clean Previous Builds")
    
    dirs_to_clean = ["build", "dist", "installer_output", ".pytest_cache", "__pycache__"]
    
    for dir_name in dirs_to_clean:
        path = PROJECT_DIR / dir_name
        if path.exists():
            print_info(f"Removing {dir_name}/...")
            shutil.rmtree(path, ignore_errors=True)
    
    print_success("Clean complete")
    return True

# ═══════════════════════════════════════════════════════════════════════════
# STEP 3: INSTALL DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════════════

def install_dependencies():
    """Install Python dependencies."""
    print_header("📚 STEP 3: Install Dependencies")
    
    print_step("Installing Python packages...")
    if CURRENT_PLATFORM == "Darwin":
        cmd = "source venv/bin/activate && pip install -q -r requirements.txt"
    else:
        cmd = ".\\venv\\Scripts\\pip install -q -r requirements.txt"
    
    if not run_cmd(cmd, "Installing dependencies", show_output=False):
        print_error("Failed to install dependencies")
        return False
    
    print_success("Dependencies installed")
    return True

# ═══════════════════════════════════════════════════════════════════════════
# STEP 4: BUILD FOR MACOS
# ═══════════════════════════════════════════════════════════════════════════

def build_macos():
    """Build for macOS."""
    print_header("🍎 STEP 4: Build for macOS")
    
    if CURRENT_PLATFORM != "Darwin":
        print_info("Not on macOS - skipping macOS build")
        print_info("macOS builds can only be created on macOS")
        return True
    
    print_step("Building macOS application...")
    cmd = "source venv/bin/activate && pyinstaller khbrowser.spec --clean --noconfirm"
    
    if not run_cmd(cmd, "PyInstaller macOS build", show_output=True):
        print_error("PyInstaller build failed")
        return False
    
    # Verify app
    app_path = PROJECT_DIR / "dist/KHBrowser.app"
    if not app_path.exists():
        print_error("macOS .app not created")
        return False
    
    app_size = sum(f.stat().st_size for f in app_path.rglob('*')) / (1024*1024)
    print_success(f"macOS app created: dist/KHBrowser.app ({app_size:.0f} MB)")
    
    return True

# ═══════════════════════════════════════════════════════════════════════════
# STEP 5: BUILD FOR WINDOWS
# ═══════════════════════════════════════════════════════════════════════════

def build_windows():
    """Build for Windows."""
    print_header("🪟 STEP 5: Build for Windows")
    
    if CURRENT_PLATFORM != "Windows":
        print_info("Not on Windows - portable EXE will be created for testing")
        print_info("Full Windows installer requires Windows + Inno Setup")
    
    print_step("Building Windows executable...")
    if CURRENT_PLATFORM == "Darwin":
        cmd = "source venv/bin/activate && pyinstaller khbrowser.spec --clean --noconfirm"
    else:
        cmd = ".\\venv\\Scripts\\pyinstaller khbrowser.spec --clean --noconfirm"
    
    if not run_cmd(cmd, "PyInstaller Windows build", show_output=True):
        print_error("PyInstaller build failed")
        return False
    
    # Verify exe
    exe_path = PROJECT_DIR / "dist/KHBrowser/KHBrowser.exe"
    if exe_path.exists():
        exe_size = exe_path.stat().st_size / (1024*1024)
        print_success(f"Windows portable EXE created: dist/KHBrowser/KHBrowser.exe ({exe_size:.0f} MB)")
        return True
    else:
        exe_path = PROJECT_DIR / "dist/KHBrowser"
        if exe_path.exists():
            print_success(f"Windows build output created: dist/KHBrowser/")
            return True
        
        print_error("Windows executable not created")
        return False

# ═══════════════════════════════════════════════════════════════════════════
# STEP 6: CREATE INSTALLER (WINDOWS)
# ═══════════════════════════════════════════════════════════════════════════

def create_windows_installer():
    """Create Windows installer with Inno Setup."""
    print_header("📦 STEP 6: Create Windows Installer")
    
    if CURRENT_PLATFORM != "Windows":
        print_info("Not on Windows - Inno Setup installer requires Windows")
        print_info("Portable EXE is ready for distribution")
        return True
    
    inno_path = "C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe"
    
    if not Path(inno_path).exists():
        print_error("Inno Setup not found")
        print_info("Download from: https://jrsoftware.org/isdl.php")
        return False
    
    print_step("Creating Windows Setup installer...")
    cmd = f'"{inno_path}" /Q installer.iss'
    
    if not run_cmd(cmd, "Inno Setup compilation", show_output=True):
        print_error("Inno Setup failed")
        return False
    
    setup_files = list((PROJECT_DIR / "installer_output").glob("*.exe"))
    if setup_files:
        setup_size = setup_files[0].stat().st_size / (1024*1024)
        print_success(f"Installer created: {setup_files[0].name} ({setup_size:.0f} MB)")
        return True
    else:
        print_error("Installer not created")
        return False

# ═══════════════════════════════════════════════════════════════════════════
# STEP 7: CREATE DMG (MACOS)
# ═══════════════════════════════════════════════════════════════════════════

def create_macos_dmg():
    """Create macOS DMG installer."""
    print_header("💿 STEP 7: Create macOS DMG Installer")
    
    if CURRENT_PLATFORM != "Darwin":
        print_info("Not on macOS - skipping DMG creation")
        return True
    
    app_path = PROJECT_DIR / "dist/KHBrowser.app"
    if not app_path.exists():
        print_error("KHBrowser.app not found")
        return False
    
    dmg_path = PROJECT_DIR / f"dist/KHBrowser-{APP_VERSION}.dmg"
    
    print_step("Creating macOS DMG...")
    
    # Create DMG using hdiutil
    cmd = f"hdiutil create -volname 'KH Browser' -srcfolder {app_path.parent}/KHBrowser.app -ov -format UDZO {dmg_path}"
    
    if run_cmd(cmd, "Creating DMG", show_output=True):
        dmg_size = dmg_path.stat().st_size / (1024*1024)
        print_success(f"macOS DMG created: dist/KHBrowser-{APP_VERSION}.dmg ({dmg_size:.0f} MB)")
        return True
    else:
        print_info("DMG creation skipped (optional)")
        return True

# ═══════════════════════════════════════════════════════════════════════════
# STEP 8: FINAL VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════

def final_verification():
    """Verify all outputs."""
    print_header("✅ STEP 8: Final Verification")
    
    outputs = []
    
    # Check macOS app
    app_path = PROJECT_DIR / "dist/KHBrowser.app"
    if app_path.exists():
        app_size = sum(f.stat().st_size for f in app_path.rglob('*')) / (1024*1024)
        print_success(f"macOS App: dist/KHBrowser.app ({app_size:.0f} MB)")
        outputs.append(("macOS App", "dist/KHBrowser.app", f"{app_size:.0f} MB"))
    
    # Check macOS DMG
    dmg_path = PROJECT_DIR / f"dist/KHBrowser-{APP_VERSION}.dmg"
    if dmg_path.exists():
        dmg_size = dmg_path.stat().st_size / (1024*1024)
        print_success(f"macOS DMG: dist/KHBrowser-{APP_VERSION}.dmg ({dmg_size:.0f} MB)")
        outputs.append(("macOS DMG", f"dist/KHBrowser-{APP_VERSION}.dmg", f"{dmg_size:.0f} MB"))
    
    # Check Windows EXE
    exe_path = PROJECT_DIR / "dist/KHBrowser/KHBrowser.exe"
    if exe_path.exists():
        exe_size = exe_path.stat().st_size / (1024*1024)
        print_success(f"Windows Portable: dist/KHBrowser/KHBrowser.exe ({exe_size:.0f} MB)")
        outputs.append(("Windows Portable", "dist/KHBrowser/KHBrowser.exe", f"{exe_size:.0f} MB"))
    
    # Check Windows Installer
    setup_files = list((PROJECT_DIR / "installer_output").glob("*.exe"))
    for setup_file in setup_files:
        setup_size = setup_file.stat().st_size / (1024*1024)
        print_success(f"Windows Installer: {setup_file.name} ({setup_size:.0f} MB)")
        outputs.append(("Windows Installer", setup_file.name, f"{setup_size:.0f} MB"))
    
    return outputs

# ═══════════════════════════════════════════════════════════════════════════
# MAIN BUILD ORCHESTRATION
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Main build orchestration."""
    os.chdir(PROJECT_DIR)
    
    print_header(f"🚀 {APP_NAME} v{APP_VERSION} - UNIVERSAL BUILD")
    print_info(f"Platform: {CURRENT_PLATFORM}")
    print_info(f"Python: {sys.version.split()[0]}")
    
    # Determine build targets
    if len(sys.argv) > 1:
        target = sys.argv[1].lower()
    else:
        target = "all"
    
    if target not in ["windows", "macos", "all"]:
        print_error(f"Invalid target: {target}")
        print_info("Usage: python BUILD.py [windows|macos|all]")
        return False
    
    # Execute build steps
    steps = [
        ("Verification", verify_project),
        ("Clean", clean_builds),
        ("Dependencies", install_dependencies),
    ]
    
    if target in ["macos", "all"]:
        steps.append(("macOS App", build_macos))
        steps.append(("macOS DMG", create_macos_dmg))
    
    if target in ["windows", "all"]:
        steps.append(("Windows EXE", build_windows))
        steps.append(("Windows Installer", create_windows_installer))
    
    steps.append(("Final Verification", final_verification))
    
    for step_name, step_func in steps:
        try:
            result = step_func()
            if isinstance(result, list):  # final_verification returns list
                continue
            if not result:
                print_error(f"Build failed at: {step_name}")
                return False
        except Exception as e:
            print_error(f"Unexpected error in {step_name}: {e}")
            return False
    
    # Final report
    print_header(f"✅ BUILD COMPLETE - {APP_NAME} v{APP_VERSION}")
    
    print(f"{Color.GREEN}{Color.BOLD}All builds completed successfully!{Color.ENDC}\n")
    
    print(f"{Color.BLUE}Output files ready for distribution:{Color.ENDC}\n")
    
    if (PROJECT_DIR / "dist/KHBrowser.app").exists():
        print(f"  {Color.GREEN}macOS:{Color.ENDC}")
        print(f"    • dist/KHBrowser.app (full application)")
        print(f"    • dist/KHBrowser-{APP_VERSION}.dmg (installer)\n")
    
    exe_path = PROJECT_DIR / "dist/KHBrowser/KHBrowser.exe"
    setup_files = list((PROJECT_DIR / "installer_output").glob("*.exe"))
    
    if exe_path.exists() or setup_files:
        print(f"  {Color.GREEN}Windows:{Color.ENDC}")
        if exe_path.exists():
            print(f"    • dist/KHBrowser/KHBrowser.exe (portable)")
        if setup_files:
            for f in setup_files:
                print(f"    • installer_output/{f.name} (setup)")
        print()
    
    print(f"{Color.CYAN}Next steps:{Color.ENDC}")
    print(f"  1. Test all built applications")
    print(f"  2. Upload to GitHub Releases")
    print(f"  3. Share with users")
    print(f"  4. Include system requirements with download\n")
    
    return True

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
