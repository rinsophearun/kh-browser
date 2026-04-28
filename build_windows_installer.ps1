# ═══════════════════════════════════════════════════════════════════════════
#  build_windows_installer.ps1
#  PowerShell build script for Windows 10/11
#  Run: Right-click → "Run with PowerShell"  (or: pwsh build_windows_installer.ps1)
# ═══════════════════════════════════════════════════════════════════════════

$AppName  = "KHBrowser"
$Version  = "1.0.0"
$InnoPath = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

function Write-Step($n, $msg) {
    Write-Host ""
    Write-Host "  [$n/5] $msg" -ForegroundColor Cyan
}

function Write-OK($msg)  { Write-Host "   ✅  $msg" -ForegroundColor Green }
function Write-ERR($msg) { Write-Host "   ❌  $msg" -ForegroundColor Red }
function Write-WARN($msg){ Write-Host "   ⚠️   $msg" -ForegroundColor Yellow }

Write-Host ""
Write-Host "  ╔═══════════════════════════════════════════════════════════╗" -ForegroundColor DarkOrange
Write-Host "  ║   ANTIDETECT BROWSER — Windows 11 Installer Builder      ║" -ForegroundColor DarkOrange
Write-Host "  ╚═══════════════════════════════════════════════════════════╝" -ForegroundColor DarkOrange

# ── 1. Check Python ──────────────────────────────────────────────────────────
Write-Step 1 "Checking Python..."
try {
    $pyver = python --version 2>&1
    Write-OK "$pyver found"
} catch {
    Write-ERR "Python not found! Install from https://python.org"
    exit 1
}

# ── 2. Install Python deps ────────────────────────────────────────────────────
Write-Step 2 "Installing Python dependencies..."
pip install PyQt6 pyinstaller requests cryptography Pillow --quiet
if ($LASTEXITCODE -ne 0) { Write-ERR "pip install failed"; exit 1 }
Write-OK "Dependencies installed"

# ── 3. Generate icons ─────────────────────────────────────────────────────────
Write-Step 3 "Generating icons..."
if (!(Test-Path "assets")) { New-Item -ItemType Directory -Path "assets" | Out-Null }
python build_icons.py
Write-OK "Icons ready"

# ── 4. PyInstaller build ──────────────────────────────────────────────────────
Write-Step 4 "Building EXE with PyInstaller (2-5 minutes)..."
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist")  { Remove-Item -Recurse -Force "dist" }

$pyiArgs = @(
    "--clean", "--noconfirm",
    "--name", $AppName,
    "--icon", "assets\icon.ico",
    "--windowed",
    "--add-data", "assets;assets",
    "--hidden-import", "PyQt6.QtCore",
    "--hidden-import", "PyQt6.QtGui",
    "--hidden-import", "PyQt6.QtWidgets",
    "--hidden-import", "PyQt6.QtNetwork",
    "--hidden-import", "cryptography",
    "--hidden-import", "requests",
    "--hidden-import", "main_window",
    "--hidden-import", "dashboard_panel",
    "--hidden-import", "groups_panel",
    "--hidden-import", "profile_dialog",
    "--hidden-import", "team_dialog",
    "--hidden-import", "browser_launcher",
    "--hidden-import", "storage",
    "--hidden-import", "models",
    "--hidden-import", "styles",
    "--hidden-import", "rpa_dialog",
    "--hidden-import", "batch_dialog",
    "--hidden-import", "settings_dialog",
    "--hidden-import", "api_dialog",
    "--exclude-module", "tkinter",
    "--exclude-module", "matplotlib",
    "--log-level", "WARN",
    "main.py"
)

pyinstaller @pyiArgs
if ($LASTEXITCODE -ne 0) { Write-ERR "PyInstaller failed!"; exit 1 }
Write-OK "EXE built: dist\$AppName\$AppName.exe"

# ── 5. Inno Setup Installer ───────────────────────────────────────────────────
Write-Step 5 "Creating Windows Setup installer with Inno Setup..."

# Auto-install Inno Setup if missing
if (!(Test-Path $InnoPath)) {
    Write-WARN "Inno Setup not found. Installing via winget..."
    try {
        winget install JRSoftware.InnoSetup --silent --accept-package-agreements
        Start-Sleep -Seconds 8
    } catch {
        Write-WARN "winget failed. Trying Chocolatey..."
        try { choco install innosetup --no-progress -y }
        catch { Write-WARN "Chocolatey not available either." }
    }
}

if (Test-Path $InnoPath) {
    if (!(Test-Path "installer_output")) { New-Item -ItemType Directory -Path "installer_output" | Out-Null }
    & $InnoPath /Q installer.iss
    if ($LASTEXITCODE -eq 0) {
        Write-OK "Installer created in installer_output\"
        $setupFile = Get-ChildItem "installer_output\*.exe" | Select-Object -First 1
        if ($setupFile) {
            $sizeMB = [math]::Round($setupFile.Length / 1MB, 1)
            Write-OK "Setup file: $($setupFile.Name) ($sizeMB MB)"
        }
    } else {
        Write-ERR "Inno Setup compilation failed"
    }
} else {
    Write-WARN "Inno Setup not found. Install from: https://jrsoftware.org/isdl.php"
    Write-WARN "Portable EXE available at: dist\$AppName\$AppName.exe"
}

# ── Done ─────────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "  ╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "  ║   BUILD COMPLETE!                                         ║" -ForegroundColor Green
Write-Host "  ╠═══════════════════════════════════════════════════════════╣" -ForegroundColor Green
Write-Host "  ║                                                           ║" -ForegroundColor Green
Write-Host "  ║   Portable EXE  →  dist\$AppName\$AppName.exe" -ForegroundColor Green
Write-Host "  ║   Setup Wizard  →  installer_output\*.exe                ║" -ForegroundColor Green
Write-Host "  ║                                                           ║" -ForegroundColor Green
Write-Host "  ╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

# Open output folder
if (Test-Path "installer_output") { explorer.exe installer_output }
