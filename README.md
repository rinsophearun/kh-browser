<div align="center">
  <img src="assets/Logo.png" alt="KH Browser Logo" width="320"/>

  <h1>KH Browser</h1>
  <p><strong>Professional Antidetect Browser Profile Manager</strong></p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python"/>
    <img src="https://img.shields.io/badge/PyQt6-6.4%2B-41CD52?style=flat-square&logo=qt"/>
    <img src="https://img.shields.io/badge/Platform-macOS%20%7C%20Windows-lightgrey?style=flat-square"/>
    <img src="https://img.shields.io/badge/Version-1.0.0-orange?style=flat-square"/>
    <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square"/>
  </p>

  <p>Manage unlimited browser profiles with unique fingerprints, proxies, RPA automation, team collaboration, and cloud sync — all from one premium dark UI.</p>
</div>

---

## ✨ Features

| Category | Features |
|----------|----------|
| 🛡️ **Fingerprint** | Custom UA, Canvas, WebGL, Fonts, Timezone, Resolution per profile |
| 🌐 **Proxy** | HTTP/HTTPS/SOCKS5 — per-profile proxy configuration |
| 👥 **Team** | Members, Roles & Permissions, Devices, Transfer Boss |
| 🤖 **RPA** | Automated browser tasks per profile |
| 📊 **Dashboard** | Real-time stats, live activity feed, animated charts |
| 📁 **Groups** | Organize profiles into custom color-coded groups |
| 📦 **Export** | Export profiles as ZIP (settings + browser data) |
| 🔁 **Batch** | Batch import / create / update / clone profiles |
| ☁️ **Cloud Sync** | Sync profiles across devices |
| 🔌 **Open API** | REST API for external integrations |
| 🪟 **Window Sync** | Sync windows across sessions |

---

## 📸 Screenshots

> Open `mockup.html` in your browser for a full interactive preview of all 6 screens.

```bash
open mockup.html
```

| Screen | Description |
|--------|-------------|
| Profiles | 11-column table with avatar, fingerprint, proxy, status, actions |
| Dashboard | Live stat cards, bar charts, donut ring, activity feed |
| Groups | Color-coded group cards |
| Team | Members, roles, devices, transfer boss |
| New Profile | Tabbed dialog: Basic Info, Fingerprint, Proxy |
| Transfer BOSS | Admin transfer with confirmation |

---

## 🚀 Quick Start

### Requirements
- Python 3.10 or higher
- macOS 10.15+ or Windows 10/11

### Install & Run

```bash
# 1. Clone the repository
git clone https://github.com/your-org/kh-browser.git
cd kh-browser

# 2. Install dependencies
pip install PyQt6 requests cryptography

# 3. Launch
python main.py
```

---

## 📁 Project Structure

```
kh-browser/
│
├── main.py                  # App entry point
├── main_window.py           # Sidebar + Profile table + Main window
├── models.py                # Data models (BrowserProfile, Fingerprint, Proxy…)
├── storage.py               # JSON persistence (~/.khbrowser/)
├── styles.py                # Global dark orange QSS design system
│
├── dashboard_panel.py       # Real-time dashboard with animated stats
├── groups_panel.py          # Groups manager
│
├── profile_dialog.py        # New / Edit profile dialog
├── team_dialog.py           # Team management (Members, Roles, Devices, Transfer)
├── batch_dialog.py          # Batch import / create / update
├── rpa_dialog.py            # RPA task builder
├── settings_dialog.py       # Global & personal settings
├── api_dialog.py            # Open API configuration
├── browser_launcher.py      # Launch Chrome / Firefox / Edge / Brave / Safari
│
├── assets/
│   ├── Logo.png             # KH Browser logo (source)
│   ├── icon.icns            # macOS app icon
│   └── icon.ico             # Windows app icon
│
├── mockup.html              # Interactive HTML mockup (6 screens)
│
├── build_macos.sh           # Build macOS .app + .dmg
├── build_windows_installer.bat   # Build Windows .exe + Setup installer
├── build_windows_installer.ps1   # PowerShell version
├── build_icons.py           # Generate icons from Logo.png
├── khbrowser.spec           # PyInstaller spec
├── installer.iss            # Inno Setup Windows installer script
│
└── .github/
    └── workflows/
        └── build.yml        # GitHub Actions: auto-build macOS + Windows
```

---

## 🛠 Build Distributable

### macOS (.app + .dmg)

```bash
bash build_macos.sh
# Output: dist/KHBrowser-1.0.0-macOS.dmg
```

**Install:** Open the `.dmg` → drag `KHBrowser.app` to **Applications**

---

### Windows 11 (.exe Setup Installer)

Run on a Windows 10/11 machine:

```batch
build_windows_installer.bat
```

Or with PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File build_windows_installer.ps1
```

**Output:**
| File | Description |
|------|-------------|
| `dist\KHBrowser\KHBrowser.exe` | Portable — no install needed |
| `installer_output\KHBrowser-1.0.0-Setup-Windows.exe` | Full setup wizard |

> Inno Setup 6 is auto-installed if not found (`winget install JRSoftware.InnoSetup`).

---

### Auto-Build via GitHub Actions

Push a version tag → GitHub builds both platforms automatically:

```bash
git tag v1.0.0
git push origin v1.0.0
# Download from GitHub → Actions → Artifacts
```

---

## 📦 Profile Export

1. Open **Profiles** table
2. Click **⋯ More** on any profile
3. Click **💾 Export Profile**
4. Choose save location → `.zip` file is created

**ZIP contents:**
```
kh_<profile_id>/
├── profile.json     ← Settings, fingerprint, proxy config
├── README.txt       ← Import instructions
└── browser_data/    ← Browser session data (cache excluded)
```

---

## 🗂 Data Storage

All data is stored locally at `~/.khbrowser/`:

```
~/.khbrowser/
├── profiles.json        ← All browser profiles
├── groups.json          ← Profile groups
└── profiles/
    └── <profile_id>/    ← Browser user data directory
        ├── Default/
        └── ...
```

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | New Profile |
| `Ctrl+F` | Search profiles |
| `Ctrl+R` | Refresh list |
| `Ctrl+,` | Settings |

---

## 🧩 Supported Browsers

| Browser | Windows | macOS | Profile Isolation |
|---------|---------|-------|------------------|
| Chrome | ✅ | ✅ | ✅ |
| Firefox | ✅ | ✅ | ✅ |
| Edge | ✅ | ✅ | ✅ |
| Brave | ✅ | ✅ | ✅ |
| Safari | ❌ | ✅ | ⚠️ Limited |
| Opera | ✅ | ✅ | ✅ |

---

## 🏗 Tech Stack

| Layer | Technology |
|-------|-----------|
| UI Framework | **PyQt6** (Qt 6.4+) |
| Language | **Python 3.10+** |
| Storage | **JSON** (`~/.khbrowser/`) |
| Packaging | **PyInstaller 6** |
| Windows Installer | **Inno Setup 6** |
| CI/CD | **GitHub Actions** |

---

## 🔐 Security Notes

- All profile data is stored **locally only** (no telemetry)
- Proxy passwords are stored in plain JSON — use OS keychain for production
- Browser profile isolation uses `--user-data-dir` per profile

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">
  <img src="assets/Logo.png" width="80"/>
  <br/>
  <sub>Built with ❤️ · KH Browser © 2025</sub>
</div>
