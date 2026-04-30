╔═══════════════════════════════════════════════════════════════════════════╗
║         KH BROWSER v2.0.0 - WINDOWS INSTALLER BUILD PACKAGE              ║
║                                                                           ║
║  Complete, ready-to-build installer for Windows 10/11                   ║
║  No additional downloads needed (except Python 3.11+ & Inno Setup 6)    ║
╚═══════════════════════════════════════════════════════════════════════════╝

WHAT'S INCLUDED:
═════════════════════════════════════════════════════════════════════════════
✓ khbrowser.spec         (PyInstaller configuration)
✓ installer.iss          (Inno Setup installer configuration)
✓ build_windows.bat      (Automated build script)
✓ requirements.txt       (Python dependencies)
✓ All source code        (*.py files)
✓ All assets             (icons, QR codes)
✓ This README            (Instructions)


STEP-BY-STEP INSTALLATION & BUILD:
═════════════════════════════════════════════════════════════════════════════

STEP 1: COPY TO WINDOWS MACHINE
─────────────────────────────────
• Copy entire "KH browser" folder to Windows
  Example: C:\Users\YourName\Documents\KH browser


STEP 2: INSTALL PREREQUISITES ON WINDOWS
─────────────────────────────────────────

A) Install Python 3.11 or higher
   • Download: https://www.python.org/downloads/
   • Run installer
   • ⚠️  IMPORTANT: Check "Add Python to PATH"
   • Verify: Open CMD and type: python --version
   • Should show: Python 3.11.x or higher

B) Install Inno Setup 6 (FREE)
   • Download: https://jrsoftware.org/isdl.php
   • Click "Download" next to "inno-6.x.x.exe"
   • Run installer with default settings
   • Installation takes ~2 minutes


STEP 3: BUILD THE INSTALLER
────────────────────────────

Option A: Automatic Build (Recommended)
──────────────────────────────────────
1. Open Windows PowerShell as Administrator
   • Press Win+X → Select "Windows PowerShell (Admin)"

2. Navigate to project:
   PS> cd "C:\Users\YourName\Documents\KH browser"

3. Run this complete command:

   python -m venv venv; .\venv\Scripts\Activate; pip install -r requirements.txt; python build_windows_complete.py

4. Wait 10-15 minutes for build to complete


Option B: Manual Build Steps
──────────────────────────────
1. Create virtual environment:
   python -m venv venv

2. Activate virtual environment:
   .\venv\Scripts\Activate

3. Install dependencies:
   pip install -r requirements.txt

4. Run build:
   python build_windows_complete.py


STEP 4: VERIFY BUILD SUCCESS
─────────────────────────────

When build completes, check for:

✓ dist\KHBrowser\KHBrowser.exe
  └─ Size should be ~380 MB
  └─ This is the portable executable

✓ installer_output\KHBrowser-2.0.0-Setup-Windows.exe
  └─ Size should be ~95 MB
  └─ This is the setup installer


STEP 5: TEST BEFORE DISTRIBUTION
─────────────────────────────────

Test 1: Portable Version
• Double-click: dist\KHBrowser\KHBrowser.exe
• Wait for app to launch
• Verify main window appears with Profiles panel
• Click buttons: Open All, Close All, Update, Donate
• Check Settings tab
• Close app

Test 2: Setup Installer
• Double-click: installer_output\KHBrowser-2.0.0-Setup-Windows.exe
• Follow setup wizard
• Choose install location (default is fine)
• Click "Next" → "Install"
• Wait for installation to complete
• Check "Launch KH Browser" at end
• Verify app launches correctly
• Add to Start menu (select during install)

Test 3: Verify All Features
• Create a new profile
• Edit profile → Check Settings tab
• Open/close profile
• Check real-time updates (auto-refresh every 2 sec)
• Test Donate button (should show QR popup)
• Click Update button


BUILD OUTPUT FILES:
═════════════════════════════════════════════════════════════════════════════

After successful build, you'll have:

OPTION 1: PORTABLE (No installation required)
─────────────────────────────────────────────
File: dist\KHBrowser\KHBrowser.exe
Size: ~380 MB
Usage: Users double-click and run immediately
Best for: USB drives, portable installations
Share with: Users who want instant access

OPTION 2: INSTALLER (Traditional Windows setup)
────────────────────────────────────────────────
File: installer_output\KHBrowser-2.0.0-Setup-Windows.exe
Size: ~95 MB
Usage: Users run installer, adds Start menu shortcut
Best for: End users, standard distribution
Share with: General users, professional distribution


DISTRIBUTION GUIDE:
═════════════════════════════════════════════════════════════════════════════

To share with users:

Method 1: GitHub Releases (Recommended)
• Visit: https://github.com/rinsophearun/kh-browser/releases
• Click "Draft a new release"
• Tag version: v2.0.0
• Title: "KH Browser v2.0.0 - Full Release"
• Upload both .exe files
• Add release notes
• Publish release

Method 2: Direct download
• Host both .exe files on your website
• Provide links for users

Method 3: Cloud storage
• Upload to Google Drive, OneDrive, Dropbox
• Share links with users


SYSTEM REQUIREMENTS FOR END USERS:
═════════════════════════════════════════════════════════════════════════════

Windows:
  ✓ Windows 10 (version 1909 or later)
  ✓ Windows 11
  ✓ 64-bit recommended (32-bit may work)

Hardware:
  ✓ Processor: Intel/AMD (any modern processor)
  ✓ RAM: Minimum 4 GB (8 GB recommended)
  ✓ Disk space: 500 MB free
  ✓ Graphics: Modern GPU with OpenGL support

Internet:
  ✓ Required for browser profile management features


WHAT'S NEW IN v2.0.0:
═════════════════════════════════════════════════════════════════════════════

✨ New Features:
  • Open All / Close All buttons for batch operations
  • Donate button with QR code popup
  • Update button for manual profile refresh
  • Settings tab with 7 per-profile configuration options
  • Real-time profile sync (auto-refresh every 2 seconds)

🎨 UI Improvements:
  • Enhanced spacing and layout
  • Better visual hierarchy
  • Improved button styling with gradients
  • Optimized table row heights and padding

🔧 Technical:
  • Updated to version 2.0.0
  • Cleaned up sample profiles
  • Added QR code asset for donations
  • Improved code structure


TROUBLESHOOTING:
═════════════════════════════════════════════════════════════════════════════

Problem: "Python not found" or "python is not recognized"
Solution:
  1. Reinstall Python from https://www.python.org/downloads/
  2. ✓ Check "Add Python to PATH" during installation
  3. Restart computer
  4. Verify: python --version

Problem: "pip: command not found"
Solution:
  1. Verify Python PATH: python -m pip --version
  2. Use: python -m pip install -r requirements.txt

Problem: "Inno Setup not found" (C:\Program Files (x86)\Inno Setup 6\ISCC.exe)
Solution:
  1. Download from: https://jrsoftware.org/isdl.php
  2. Run installer
  3. Use default installation path
  4. Restart PowerShell after installing
  5. Retry build

Problem: "Not enough space" or "Permission denied"
Solution:
  1. Ensure 3+ GB free disk space
  2. Run PowerShell as Administrator
  3. Close any open KH Browser windows
  4. Try build again

Problem: Build hangs or takes too long
Solution:
  1. First build is slow (10-15 minutes is normal)
  2. Wait at least 15 minutes before canceling
  3. Check Task Manager for pyinstaller.exe
  4. If truly stuck: Press Ctrl+C and retry


BUILD COMPLETE CHECKLIST:
═════════════════════════════════════════════════════════════════════════════

After successful build, verify:

✓ Both .exe files exist:
  [ ] dist\KHBrowser\KHBrowser.exe (portable)
  [ ] installer_output\*.exe (setup)

✓ File sizes are correct:
  [ ] Portable: ~380 MB
  [ ] Installer: ~95 MB

✓ Icons are embedded:
  [ ] Both .exe files have KH Browser icon
  [ ] No generic icon shown

✓ No error messages:
  [ ] Build completed without errors
  [ ] No "failed", "error", or "missing" messages
  [ ] Final report shows "✅ BUILD SUCCESSFUL"

✓ Both versions tested:
  [ ] Portable .exe launches and runs
  [ ] Setup wizard completes
  [ ] All features work correctly
  [ ] No crashes or warnings


NEXT STEPS AFTER BUILD:
═════════════════════════════════════════════════════════════════════════════

1. ✅ Verify build completed successfully

2. 🧪 Test both .exe files thoroughly

3. 📤 Upload to GitHub Releases or hosting

4. 📢 Announce to users

5. 📝 Create installation guide for end users (if needed)

6. 🔄 For future builds:
   • Just run: python build_windows_complete.py
   • Previous builds are cleaned automatically
   • Takes 10-15 minutes each time


CONTACT & SUPPORT:
═════════════════════════════════════════════════════════════════════════════

GitHub: https://github.com/rinsophearun/kh-browser
Issues: https://github.com/rinsophearun/kh-browser/issues
Version: 2.0.0
Built: 2026-04-30
Python: 3.11+
PyQt6: Latest


═══════════════════════════════════════════════════════════════════════════
Ready to build! Follow the steps above to create your installer.
═══════════════════════════════════════════════════════════════════════════
