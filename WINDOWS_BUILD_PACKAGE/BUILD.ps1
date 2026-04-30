<#
═══════════════════════════════════════════════════════════════════════════
  KH BROWSER v2.0.0 - WINDOWS INSTALLER BUILD (PowerShell)
  
  One-command build script for Windows PowerShell
  Run with: powershell -ExecutionPolicy Bypass -File BUILD.ps1
═══════════════════════════════════════════════════════════════════════════
#>

Write-Host "`n╔═══════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Blue
Write-Host "║            KH BROWSER v2.0.0 - WINDOWS BUILD STARTING                     ║" -ForegroundColor Blue
Write-Host "╚═══════════════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Blue

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    python --version | Out-Null
    Write-Host "✓ Python found" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found!" -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "⚠️  Check 'Add Python to PATH' during installation`n" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check Inno Setup
Write-Host "Checking Inno Setup installation..." -ForegroundColor Yellow
if (-not (Test-Path "C:\Program Files (x86)\Inno Setup 6\ISCC.exe")) {
    Write-Host "⚠️  Inno Setup not found" -ForegroundColor Yellow
    Write-Host "Download from: https://jrsoftware.org/isdl.php`n" -ForegroundColor Yellow
}

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv
if ($?) {
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
if ($?) {
    Write-Host "✓ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to activate virtual environment" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Install dependencies
Write-Host "`nInstalling Python dependencies..." -ForegroundColor Yellow
Write-Host "This may take 3-5 minutes...`n" -ForegroundColor Cyan
pip install -q -r requirements.txt
if ($?) {
    Write-Host "✓ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Run build
Write-Host "`nStarting build process..." -ForegroundColor Yellow
Write-Host "This will take 10-15 minutes...`n" -ForegroundColor Cyan
python build_windows_complete.py
if ($?) {
    Write-Host "`n╔═══════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║                    ✅ BUILD COMPLETED SUCCESSFULLY!                        ║" -ForegroundColor Green
    Write-Host "╚═══════════════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Green
    
    Write-Host "Your installers are ready:" -ForegroundColor Green
    Write-Host "`n📦 PORTABLE (no installation required):" -ForegroundColor Cyan
    Write-Host "   dist\KHBrowser\KHBrowser.exe  (~380 MB)`n" -ForegroundColor White
    
    Write-Host "📦 INSTALLER (setup wizard):" -ForegroundColor Cyan
    Write-Host "   installer_output\KHBrowser-2.0.0-Setup-Windows.exe  (~95 MB)`n" -ForegroundColor White
    
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "  1. Test the portable EXE by double-clicking it" -ForegroundColor White
    Write-Host "  2. Test the installer by double-clicking it" -ForegroundColor White
    Write-Host "  3. Share the files with users`n" -ForegroundColor White
} else {
    Write-Host "`n❌ Build failed!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Read-Host "Press Enter to close"
