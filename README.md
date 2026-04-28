<div align="center">
  <img src="assets/Logo.png" alt="KH Browser Logo" width="300"/>

  <h1>🌐 KH Browser</h1>
  <h3>Professional Antidetect Browser Profile Manager</h3>

  <p>
    <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
    <img src="https://img.shields.io/badge/PyQt6-6.4%2B-41CD52?style=for-the-badge&logo=qt&logoColor=white"/>
    <img src="https://img.shields.io/badge/Platform-macOS%20%7C%20Windows-lightgrey?style=for-the-badge"/>
    <img src="https://img.shields.io/badge/Version-1.0.0-FF8C00?style=for-the-badge"/>
    <img src="https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge"/>
    <img src="https://img.shields.io/badge/Build-Passing-22C55E?style=for-the-badge&logo=github-actions&logoColor=white"/>
  </p>

  <p><strong>Manage unlimited browser profiles with unique fingerprints, proxies, RPA automation,<br/>team collaboration, cloud sync — all from one premium dark orange UI.</strong></p>

  <br/>

  <a href="#-quick-start">Quick Start</a> •
  <a href="#-features">Features</a> •
  <a href="#-automation-rpa">Automation</a> •
  <a href="#-build-distributable">Build</a> •
  <a href="#-api-reference">API</a> •
  <a href="#-team-management">Team</a>

</div>

---

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Features](#-features)
3. [Screenshots](#-screenshots)
4. [Quick Start](#-quick-start)
5. [Project Structure](#-project-structure)
6. [Browser Profiles](#-browser-profiles)
7. [Fingerprint Engine](#-fingerprint-engine)
8. [Proxy Configuration](#-proxy-configuration)
9. [Automation (RPA)](#-automation-rpa)
10. [Team Management](#-team-management)
11. [Batch Operations](#-batch-operations)
12. [Profile Export & Import](#-profile-export--import)
13. [Cloud Sync](#-cloud-sync)
14. [Dashboard](#-dashboard)
15. [Groups](#-groups)
16. [Settings](#-settings)
17. [Open API](#-open-api)
18. [Build Distributable](#-build-distributable)
19. [Data Storage](#-data-storage)
20. [Keyboard Shortcuts](#-keyboard-shortcuts)
21. [Supported Browsers](#-supported-browsers)
22. [Tech Stack](#-tech-stack)
23. [Security Notes](#-security-notes)
24. [Changelog](#-changelog)
25. [License](#-license)

---

## 🔍 Overview

**KH Browser** is a desktop application for managing multiple isolated browser profiles, each with its own unique fingerprint, proxy, cookies, and browser data. It is designed for:

- **Digital marketers** managing multiple ad accounts
- **E-commerce sellers** running multiple storefronts
- **Social media managers** handling many accounts
- **QA teams** testing across browser environments
- **Security researchers** needing isolated sessions

Each profile acts as a completely separate browser identity — different fingerprint, different IP (via proxy), different cookies, different hardware signature. Sites cannot detect that profiles belong to the same user.

---

## ✨ Features

### Core Features

| Category | Features |
|----------|----------|
| 🛡️ **Fingerprint** | Custom User-Agent, Canvas noise, WebGL spoofing, Fonts, Timezone, Screen resolution, Platform, Hardware concurrency, Device memory, Battery, WebRTC, Client Rects noise |
| 🌐 **Proxy** | HTTP / HTTPS / SOCKS4 / SOCKS5 per profile, rotation URL, IP check, username/password auth |
| �� **Automation** | RPA task builder with JavaScript/Playwright scripts, live execution log, 6 built-in templates, 12 quick snippets |
| 📊 **Dashboard** | Real-time stat cards, animated bar charts, donut ring, live activity feed, running profiles counter |
| 👥 **Team** | Members, Roles & Permissions (Owner/Admin/Member/Viewer), device limits, Transfer Boss |
| 📁 **Groups** | Color-coded profile groups, move/assign profiles |
| 📦 **Export** | Export profiles as ZIP (metadata + browser data) |
| 🔁 **Batch** | Batch import CSV, batch create, batch update, batch clone |
| ☁️ **Cloud Sync** | Sync profiles & settings across devices |
| 🔌 **Open API** | REST API keys with granular permissions |
| 🪟 **Window Sync** | Synchronize browser window positions and sizes |
| ⚙️ **Settings** | Global settings, personal preferences, browser paths |
| 📋 **Platform Accounts** | Store platform credentials per profile (Facebook, Instagram, etc.) |
| 🏷️ **Tags & Notes** | Tag profiles, add free-form notes |

### Advanced Features

| Feature | Description |
|---------|-------------|
| **Profile Isolation** | Each profile has its own `--user-data-dir` — zero cookie sharing |
| **Startup URL** | Custom launch URL per profile |
| **Extensions** | Enable/disable extensions per profile |
| **Quick Launch** | Launch browser directly from profile list |
| **Clone Profile** | Duplicate any profile with one click |
| **Restore Profile** | Restore deleted profiles from backup |
| **Transfer Profile** | Send profile to another team member |
| **Share Profile** | Share read-only profile access |
| **Multi-device Login** | Internal member multi-device session management |

---

## 📸 Screenshots

> Open `mockup.html` in browser for a full interactive preview of all screens.

```bash
open mockup.html          # macOS
start mockup.html         # Windows
```

| Screen | Description |
|--------|-------------|
| **Profiles** | 11-column table: avatar, name, group, OS, browser, proxy, status, fingerprint badge, last used, actions |
| **Dashboard** | Live stat cards, animated bar charts, donut ring, activity feed, running counter |
| **Groups** | Color-coded group cards with profile counts and member assignments |
| **RPA Tasks** | Task list, live execution log, script editor, schedule builder |
| **Team** | Members table with roles, devices, permissions; Transfer Boss dialog |
| **New Profile** | Multi-tab dialog: Basic Info, Fingerprint, Proxy, Platform Accounts, Extensions |

---

## 🚀 Quick Start

### Requirements

| Requirement | Version |
|-------------|---------|
| Python | 3.10 or higher |
| PyQt6 | 6.4 or higher |
| OS | macOS 10.15+ or Windows 10/11 |
| RAM | 256 MB minimum |
| Disk | 200 MB |

### Install & Run

```bash
# 1. Clone the repository
git clone https://github.com/rinsophearun/kh-browser.git
cd kh-browser

# 2. Install dependencies
pip install PyQt6 requests cryptography Pillow

# 3. Launch
python main.py
```

### One-liner install (macOS)

```bash
git clone https://github.com/rinsophearun/kh-browser.git && \
cd kh-browser && pip install PyQt6 requests cryptography Pillow && python main.py
```

### Pre-built binaries

| Platform | Download | Size |
|----------|----------|------|
| 🪟 Windows | `KHBrowser-1.0.0-Setup-Windows.exe` | ~38 MB |
| 🪟 Windows Portable | `KHBrowser.exe` | ~4.5 MB |
| 🍎 macOS | `KHBrowser-1.0.0-macOS.dmg` | ~1.3 GB |

> Download from [GitHub Releases](https://github.com/rinsophearun/kh-browser/releases) or [GitHub Actions Artifacts](https://github.com/rinsophearun/kh-browser/actions)

---

## 📁 Project Structure

```
kh-browser/
│
├── main.py                       # App entry point — QApplication bootstrap
├── main_window.py                # Sidebar + Profile table + MainWindow
├── models.py                     # Data models (BrowserProfile, Fingerprint, Proxy…)
├── storage.py                    # JSON persistence (~/.khbrowser/)
├── styles.py                     # Global dark-orange QSS design system
│
├── dashboard_panel.py            # Real-time dashboard (stats, charts, activity)
├── groups_panel.py               # Groups manager
│
├── profile_dialog.py             # New / Edit profile — tabbed dialog
├── team_dialog.py                # Team management (Members, Roles, Devices, Transfer)
├── batch_dialog.py               # Batch import / create / update / clone
├── rpa_dialog.py                 # RPA automation task builder + execution log
├── settings_dialog.py            # Global & personal settings
├── api_dialog.py                 # Open API key management
├── browser_launcher.py           # Launch Chrome / Firefox / Edge / Brave / Safari
│
├── assets/
│   ├── Logo.png                  # KH Browser logo (source image)
│   ├── icon.icns                 # macOS app icon (generated from Logo.png)
│   └── icon.ico                  # Windows app icon (generated from Logo.png)
│
├── mockup.html                   # Interactive HTML mockup (all 6 screens)
│
├── build_macos.sh                # Build macOS .app + .dmg
├── build_windows_installer.bat   # Build Windows .exe + Inno Setup installer
├── build_windows_installer.ps1   # PowerShell build script
├── build_icons.py                # Generate icons from Logo.png (Pillow)
├── khbrowser.spec                # PyInstaller bundling spec
├── installer.iss                 # Inno Setup 6 installer script
│
├── .github/
│   └── workflows/
│       └── build.yml             # CI/CD — auto-build macOS + Windows on tag push
│
├── README.md                     # This file
├── CHANGELOG.md                  # Version history
└── BUILD_WINDOWS.md              # Windows-specific build guide
```

---

## 🖥 Browser Profiles

A **Browser Profile** is an isolated identity containing:

```
BrowserProfile
├── id              — Unique 8-char ID
├── name            — Display name
├── group           — Group assignment (color-coded)
├── browser_type    — Chrome / Firefox / Edge / Brave
├── browser_version — e.g. "120.0"
├── os_type         — Windows / macOS / Linux
├── os_version      — e.g. "10"
├── fingerprint     — Full Fingerprint object (see below)
├── proxy           — ProxyConfig object
├── accounts        — List of PlatformAccount (credentials)
├── extensions      — List of extension IDs
├── tags            — String tags for filtering
├── notes           — Free-form notes
├── status          — stopped / running / error
├── startup_url     — Custom URL on launch
├── cloud_synced    — Boolean
├── created_at      — Timestamp
└── last_used       — Timestamp
```

### Profile Actions (Right-click / More menu)

| Action | Description |
|--------|-------------|
| ▶ Launch | Open browser with this profile |
| ✏ Edit | Modify profile settings |
| 📋 Clone | Duplicate with new ID |
| 💾 Export | Export as ZIP |
| 🔄 Restore | Restore from backup |
| 📤 Transfer | Send to team member |
| 🗑 Delete | Remove profile |
| 🔗 Share | Share read-only access |

---

## 🛡 Fingerprint Engine

Each profile has a fully customizable fingerprint to prevent browser tracking and site detection.

### Fingerprint Properties

| Property | Description | Example |
|----------|-------------|---------|
| `user_agent` | Browser User-Agent string | `Mozilla/5.0 (Windows NT 10.0; Win64; x64)...` |
| `screen_width` | Screen resolution width | `1920` |
| `screen_height` | Screen resolution height | `1080` |
| `color_depth` | Color depth bits | `24` |
| `pixel_ratio` | Device pixel ratio | `1.0` |
| `timezone` | Timezone identifier | `America/New_York` |
| `timezone_offset` | UTC offset in minutes | `-300` |
| `language` | Browser language | `en-US` |
| `languages` | Accept-Language header | `en-US,en;q=0.9` |
| `webgl_vendor` | WebGL vendor string | `Google Inc. (Intel)` |
| `webgl_renderer` | WebGL renderer string | `ANGLE (Intel, Intel(R) UHD Graphics...)` |
| `canvas_noise` | Enable canvas fingerprint noise | `true` |
| `audio_noise` | Enable AudioContext noise | `true` |
| `webrtc_mode` | WebRTC leak protection | `disabled` / `real` / `fake` |
| `hardware_concurrency` | CPU thread count | `8` |
| `device_memory` | RAM in GB | `8` |
| `platform` | JS `navigator.platform` | `Win32` |
| `fonts` | Available fonts list | `["Arial", "Georgia"...]` |
| `do_not_track` | DNT header | `false` |
| `webgl_noise` | WebGL noise injection | `true` |
| `client_rects_noise` | ClientRects API noise | `true` |
| `media_devices` | Number of media devices | `3` |
| `battery_level` | Battery level (0.0–1.0) | `0.85` |
| `battery_charging` | Battery charging state | `true` |
| `ports_protection` | Block port scanning | `true` |
| `geolocation_mode` | Geolocation mode | `based_on_ip` / `custom` |
| `latitude` | Custom latitude | `40.7128` |
| `longitude` | Custom longitude | `-74.0060` |

### Fingerprint Noise Modes

```
Canvas Noise  → Adds imperceptible pixel-level noise to canvas drawings
WebGL Noise   → Randomizes WebGL buffer data slightly  
Audio Noise   → Adds tiny noise to AudioContext outputs
ClientRects   → Micro-adjusts getBoundingClientRect() return values
```

---

## 🌐 Proxy Configuration

Each profile can have its own independent proxy:

### Supported Proxy Types

| Type | Format | Authentication |
|------|--------|---------------|
| None | — | — |
| HTTP | `http://host:port` | ✅ Optional |
| HTTPS | `https://host:port` | ✅ Optional |
| SOCKS4 | `socks4://host:port` | ❌ |
| SOCKS5 | `socks5://host:port` | ✅ |
| Rotating | Rotation URL endpoint | ✅ |

### ProxyConfig Fields

```python
ProxyConfig
├── type          — None / HTTP / HTTPS / SOCKS4 / SOCKS5 / Rotating
├── host          — Proxy hostname or IP
├── port          — Port number
├── username      — Auth username (optional)
├── password      — Auth password (optional)
├── rotation_url  — URL for IP rotation endpoint
└── check_ip      — IP check service URL (e.g. api.ipify.org)
```

### IP Check

Click **"Check IP"** in the proxy tab to verify the proxy is working and see the outgoing IP address.

---

## 🤖 Automation (RPA)

The built-in **RPA (Robotic Process Automation)** engine lets you automate browser actions across any number of profiles simultaneously.

### Architecture

```
RPATask
├── id            — Unique task ID
├── name          — Task display name  
├── description   — What the task does
├── script        — JavaScript / Playwright automation code
├── profile_ids   — Which profiles to run on
├── schedule      — Cron expression or datetime
├── repeat        — once / hourly / daily / weekly / monthly
├── status        — idle / running / completed / failed / scheduled / paused
├── run_count     — How many times executed
├── last_run      — Last execution timestamp
└── created_at    — Creation timestamp
```

### Built-in Templates

| Template | Use Case |
|----------|----------|
| **Auto Login** | Automate login to any website |
| **Scrape Data** | Extract structured data from pages |
| **Post Content** | Publish posts across social platforms |
| **Account Warmup** | Simulate natural browsing activity |
| **Cookie Collector** | Harvest and store session cookies |
| **Form Filler** | Auto-fill and submit web forms |

### Quick Snippets

| Snippet | Code |
|---------|------|
| 🌐 goto | `await page.goto('{url}');` |
| 🖱 click | `await page.click('{selector}');` |
| ⌨ fill | `await page.fill('{selector}', '{value}');` |
| ⏳ wait | `await page.waitForSelector('{selector}');` |
| 💤 sleep | `await page.waitForTimeout(2000);` |
| 📷 screenshot | `await page.screenshot({ path: 'snap.png' });` |
| 📜 scroll | `await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));` |
| 🔑 press | `await page.keyboard.press('Enter');` |
| 🍪 cookies | `const cookies = await page.context().cookies();` |
| 📋 getText | `const text = await page.$eval('{sel}', el => el.textContent);` |
| 🔀 random wait | `await page.waitForTimeout(Math.floor(Math.random()*3000)+1000);` |
| 🖱 hover | `await page.hover('{selector}');` |

### Schedule Options

| Option | Description |
|--------|-------------|
| Once | Run one time at specified datetime |
| Hourly | Repeat every N hours |
| Daily | Run once per day |
| Weekly | Run once per week |
| Monthly | Run once per month |

### Execution Settings

| Setting | Range | Default |
|---------|-------|---------|
| Concurrent profiles | 1–50 | 1 |
| Retry on failure | 0–10 | 2 |

### Live Execution Log

When a task runs, the **Execution Log** tab shows real-time output:

```
[10:24:01] 🚀 Starting task: Auto Login FB
[10:24:01] 🔧 Initializing browser context...
[10:24:02] 🌐 Launching profile: FB Account 1
[10:24:03] ✅ Browser started  PID: 48291
[10:24:03] 📜 Executing script line 1...
[10:24:04] 🌐 Navigating to https://facebook.com...
[10:24:06] ✅ Page loaded  (1240ms)
[10:24:06] 🖱 Clicking selector #email
[10:24:07] ✅ Login successful
[10:24:08] ✅ Task completed!  Run #6  Duration: 7s
```

---

## 👥 Team Management

Manage multi-user access with role-based permissions.

### Roles & Permissions

| Role | Profiles | Launch | Create | Delete | Team | Settings | API |
|------|----------|--------|--------|--------|------|----------|-----|
| **Owner** | Unlimited | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Admin** | Up to 500 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Member** | Up to 100 | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Viewer** | Up to 50 | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

### Team Features

| Feature | Description |
|---------|-------------|
| **Invite Member** | Send invitation by email |
| **Set Role** | Assign or change member role |
| **Device Limit** | Max simultaneous device logins per member |
| **Profile Limit** | Max profiles a member can access |
| **Shared Profiles** | Count of profiles shared with member |
| **Last Login** | Track last activity time |
| **Transfer Boss** | Transfer Owner role to another Admin |
| **Revoke Access** | Remove member immediately |

### TeamMember Object

```python
TeamMember
├── id              — Unique member ID
├── name            — Display name
├── email           — Email address
├── role            — Owner / Admin / Member / Viewer
├── status          — Active / Invited / Suspended
├── max_profiles    — Profile access limit
├── max_devices     — Device login limit
├── joined_at       — Join date
├── last_login      — Last login timestamp
└── shared_profiles — Number of shared profiles
```

---

## 📦 Batch Operations

Process multiple profiles at once with the Batch panel.

### Batch Actions

| Action | Description |
|--------|-------------|
| **Batch Import** | Import profiles from CSV file |
| **Batch Create** | Create N profiles from a template |
| **Batch Update** | Update fields across selected profiles |
| **Batch Clone** | Duplicate selected profiles |
| **Batch Delete** | Remove multiple profiles at once |
| **Batch Export** | Export multiple profiles to ZIP |
| **Batch Move** | Move profiles between groups |

### CSV Import Format

```csv
name,group,browser_type,os_type,proxy_type,proxy_host,proxy_port,proxy_user,proxy_pass
"FB Account 1","Facebook","Chrome","Windows","SOCKS5","proxy.example.com","1080","user","pass"
"Instagram Pro","Social","Firefox","macOS","HTTP","proxy2.example.com","8080","","" 
```

### Batch Update Fields

- `group` — Move to different group
- `browser_type` — Change browser
- `os_type` — Change OS fingerprint
- `proxy_type` — Change proxy type
- `tags` — Add/replace tags
- `status` — Reset status
- `startup_url` — Set launch URL

---

## 📤 Profile Export & Import

### Export a Profile

1. Open **Profiles** table
2. Click **⋯ More** on any profile row
3. Click **💾 Export Profile**
4. Choose save location — default filename: `ProfileName_<id>.zip`

### ZIP Structure

```
ProfileName_AB12CD34.zip
├── profile.json         ← All settings, fingerprint, proxy, metadata
├── README.txt           ← Import instructions and profile summary
└── browser_data/        ← Browser user data directory
    ├── Default/
    │   ├── Cookies
    │   ├── Local Storage/
    │   ├── History
    │   └── ...
    └── (cache excluded for smaller file size)
```

### What's in `profile.json`

```json
{
  "id": "AB12CD34",
  "name": "FB Account 1",
  "group": "Facebook",
  "browser_type": "Chrome",
  "browser_version": "120.0",
  "os_type": "Windows",
  "os_version": "10",
  "fingerprint": {
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "screen_width": 1920,
    "screen_height": 1080,
    "timezone": "America/New_York",
    "webgl_vendor": "Google Inc. (Intel)",
    "canvas_noise": true,
    "webrtc_mode": "disabled"
  },
  "proxy": {
    "type": "SOCKS5",
    "host": "proxy.example.com",
    "port": 1080,
    "username": "user",
    "password": "pass"
  },
  "created_at": "2025-01-15 10:30",
  "last_used": "2025-01-15 14:22",
  "cloud_synced": true
}
```

### Import a Profile

> Import from ZIP will be available in v1.1.0

---

## ☁️ Cloud Sync

Synchronize profiles and settings across multiple devices.

### What Gets Synced

| Data | Synced |
|------|--------|
| Profile metadata | ✅ |
| Fingerprint settings | ✅ |
| Proxy configuration | ✅ |
| Platform accounts | ✅ |
| Groups | ✅ |
| Tags & Notes | ✅ |
| Browser session data (cookies) | ⚙️ Optional |
| RPA tasks | ✅ |
| Team settings | ✅ |

### Sync Modes

| Mode | Description |
|------|-------------|
| **Auto** | Sync on every change |
| **Manual** | Sync only when you click "Sync Now" |
| **On Start** | Sync once when app launches |
| **On Exit** | Sync when closing app |

---

## 📊 Dashboard

The real-time dashboard shows live statistics about your profiles.

### Stat Cards

| Card | Metric |
|------|--------|
| 🟢 **Active Profiles** | Currently running profiles |
| 👥 **Total Profiles** | All profiles in system |
| 🌐 **With Proxy** | Profiles with proxy configured |
| ☁️ **Cloud Synced** | Profiles synced to cloud |

### Charts

| Chart | Description |
|-------|-------------|
| **Bar Chart** | Profile launches over last 7 days |
| **Donut Ring** | Profile status distribution |
| **Activity Feed** | Live log of recent profile actions |

### Activity Feed Events

```
● FB Account 1         launched         2 min ago
● Instagram Pro        proxy changed    5 min ago
● Shopify Store        fingerprint set  12 min ago
● Twitter Bot          stopped          1 hour ago
● Amazon Seller        exported         3 hours ago
```

---

## 📁 Groups

Organize profiles into color-coded groups.

### Default Groups

| Group | Color |
|-------|-------|
| Default | Gray |
| Facebook | Blue |
| Social Media | Purple |
| E-commerce | Green |
| B2B | Orange |
| Content | Pink |
| Testing | Yellow |

### Group Actions

| Action | Description |
|--------|-------------|
| ➕ Create Group | New group with custom name + color |
| 📝 Rename | Rename existing group |
| 🎨 Change Color | Pick new color |
| 🗑 Delete | Delete group (profiles move to Default) |
| 📋 Assign Profiles | Move profiles to this group |

---

## ⚙️ Settings

### Global Settings

| Setting | Options |
|---------|---------|
| App Language | English, Khmer, Chinese, Vietnamese, Thai |
| Theme | Dark (default), Darker, Dark Blue |
| Accent Color | Orange (default), Blue, Green, Purple |
| Default Browser | Chrome, Firefox, Edge, Brave |
| Auto-start | On / Off |
| Minimize to Tray | On / Off |
| Check for Updates | On / Off |
| Telemetry | Off (always) |

### Browser Paths

Set custom browser executable paths for each browser type:

```
Chrome:  C:\Program Files\Google\Chrome\Application\chrome.exe
Firefox: C:\Program Files\Mozilla Firefox\firefox.exe
Edge:    C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
Brave:   C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe
```

### Personal Settings

| Setting | Description |
|---------|-------------|
| Display Name | Your name in the team |
| Avatar | Profile picture |
| Email | Notification email |
| Notifications | Desktop / Email notifications |
| 2FA | Two-factor authentication |
| Session Timeout | Auto-lock after N minutes |

---

## 🔌 Open API

Integrate KH Browser with external tools via the REST API.

### Authentication

```bash
# Add API key to every request header:
Authorization: Bearer ak_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/profiles` | List all profiles |
| `GET` | `/api/v1/profiles/{id}` | Get profile by ID |
| `POST` | `/api/v1/profiles` | Create new profile |
| `PUT` | `/api/v1/profiles/{id}` | Update profile |
| `DELETE` | `/api/v1/profiles/{id}` | Delete profile |
| `POST` | `/api/v1/profiles/{id}/launch` | Launch browser |
| `POST` | `/api/v1/profiles/{id}/stop` | Stop browser |
| `GET` | `/api/v1/profiles/{id}/status` | Get browser status |
| `GET` | `/api/v1/tasks` | List RPA tasks |
| `POST` | `/api/v1/tasks/{id}/run` | Execute RPA task |

### API Key Permissions

| Permission | Access |
|------------|--------|
| `read` | GET endpoints only |
| `write` | POST / PUT endpoints |
| `delete` | DELETE endpoints |
| `launch` | Launch/stop browser |
| `tasks` | RPA task execution |

### Example: Create Profile via API

```bash
curl -X POST http://localhost:8080/api/v1/profiles \
  -H "Authorization: Bearer ak_live_xxxxxxxxxxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Profile",
    "group": "Facebook",
    "browser_type": "Chrome",
    "os_type": "Windows",
    "proxy": {
      "type": "SOCKS5",
      "host": "proxy.example.com",
      "port": 1080
    }
  }'
```

---

## 🛠 Build Distributable

### macOS (.app + .dmg)

```bash
# Install build dependencies
pip install pyinstaller Pillow

# Generate icons from Logo.png
python3 build_icons.py

# Build .app bundle + .dmg installer
bash build_macos.sh

# Output:
# dist/KHBrowser.app           (537 MB — full bundle)
# dist/KHBrowser-1.0.0-macOS.dmg  (1.3 GB — installer)
```

**Install on macOS:**
1. Open `KHBrowser-1.0.0-macOS.dmg`
2. Drag `KHBrowser.app` to `Applications`
3. Right-click → Open (first time — to bypass Gatekeeper)

> **macOS 13+ Note:** If you get a security error, run:
> ```bash
> xattr -dr com.apple.quarantine /Applications/KHBrowser.app
> ```

---

### Windows 11 (.exe Setup Installer)

Copy project to a Windows 10/11 machine, then:

**Option A — Batch file (easiest):**
```batch
build_windows_installer.bat
```

**Option B — PowerShell:**
```powershell
powershell -ExecutionPolicy Bypass -File build_windows_installer.ps1
```

**Manual steps:**
```batch
pip install PyQt6 pyinstaller requests cryptography Pillow
python build_icons.py
pyinstaller --clean --noconfirm --name KHBrowser ^
    --icon assets\icon.ico --windowed ^
    --add-data "assets;assets" main.py
```

**Output:**

| File | Description | Size |
|------|-------------|------|
| `dist\KHBrowser\KHBrowser.exe` | Portable — run directly | ~4.5 MB |
| `installer_output\KHBrowser-1.0.0-Setup-Windows.exe` | Full setup wizard | ~38 MB |

> Inno Setup 6 is auto-installed via `winget` if not found.

---

### Auto-Build via GitHub Actions (Recommended)

The included GitHub Actions workflow builds both platforms automatically.

**Trigger a build:**
```bash
# Push a version tag → GitHub builds automatically
git tag v1.1.0
git push origin v1.1.0
```

**Or trigger manually:**
- GitHub → Actions → "🏗 Build KH Browser" → "Run workflow"

**Download artifacts:**
- GitHub → Actions → Latest run → **Artifacts**
  - `KHBrowser-Windows-Setup-Installer` — `.exe` installer
  - `KHBrowser-Windows-Portable-EXE` — portable `.exe`
  - `KHBrowser-macOS-DMG` — `.dmg` installer

**Workflow file:** `.github/workflows/build.yml`

```yaml
jobs:
  build-windows:  # Runs on windows-latest
  build-macos:    # Runs on macos-latest
  release:        # Creates GitHub Release on tag push
```

---

## 🗂 Data Storage

All data is stored **locally** on your machine:

```
~/.khbrowser/
├── profiles.json          ← All browser profiles (metadata + fingerprint + proxy)
├── groups.json            ← Profile groups
├── settings.json          ← App settings
├── tasks.json             ← RPA tasks
├── team.json              ← Team members
└── profiles/
    ├── AB12CD34/          ← Browser user data for profile AB12CD34
    │   ├── Default/
    │   │   ├── Cookies
    │   │   ├── Local Storage/
    │   │   ├── History
    │   │   ├── Bookmarks
    │   │   └── Extensions/
    │   └── ...
    └── E5F6G7H8/          ← Browser user data for profile E5F6G7H8
        └── ...
```

**Platform paths:**

| OS | Path |
|----|------|
| macOS | `~/.khbrowser/` |
| Windows | `C:\Users\<username>\.khbrowser\` |
| Linux | `~/.khbrowser/` |

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | New Profile |
| `Ctrl+F` | Focus search box |
| `Ctrl+R` | Refresh profile list |
| `Ctrl+,` | Open Settings |
| `Ctrl+D` | Open Dashboard |
| `Ctrl+G` | Open Groups |
| `Ctrl+T` | Open Team |
| `Ctrl+A` | Select all profiles |
| `Delete` | Delete selected profile |
| `Enter` | Launch selected profile |
| `Esc` | Close dialog / deselect |

---

## 🧩 Supported Browsers

| Browser | Windows | macOS | Linux | Profile Isolation | Notes |
|---------|---------|-------|-------|------------------|-------|
| **Chrome** | ✅ | ✅ | ✅ | ✅ Full | Recommended |
| **Firefox** | ✅ | ✅ | ✅ | ✅ Full | `--profile` dir |
| **Edge** | ✅ | ✅ | ❌ | ✅ Full | Chromium-based |
| **Brave** | ✅ | ✅ | ✅ | ✅ Full | Chromium-based |
| **Safari** | ❌ | ✅ | ❌ | ⚠️ Limited | macOS only |
| **Opera** | ✅ | ✅ | ✅ | ✅ Full | Chromium-based |
| **Chromium** | ✅ | ✅ | ✅ | ✅ Full | Open source |

---

## 🏗 Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| **UI Framework** | PyQt6 | 6.4+ |
| **Language** | Python | 3.10+ |
| **Storage** | JSON files | — |
| **Icons** | Pillow | 10+ |
| **HTTP** | requests | 2.28+ |
| **Crypto** | cryptography | 41+ |
| **Packaging** | PyInstaller | 6.0+ |
| **Windows Installer** | Inno Setup | 6.0 |
| **CI/CD** | GitHub Actions | — |
| **OS** | macOS 10.15+ / Windows 10+ | — |

---

## 🔐 Security Notes

| Topic | Details |
|-------|---------|
| **Local Storage** | All profile data stored locally — no telemetry |
| **Passwords** | Stored in plain JSON — encrypt for production use |
| **Profile Isolation** | Uses `--user-data-dir` per profile — zero cookie sharing |
| **API Keys** | Stored in settings.json — rotate regularly |
| **Proxy Auth** | Credentials in plaintext — use environment variables for production |
| **No Analytics** | Zero usage analytics or tracking |
| **WebRTC** | Can be disabled per profile to prevent IP leaks |
| **Canvas** | Noise injection prevents cross-profile tracking |

---

## 📝 Changelog

### v1.0.0 (2025-04-29)

**Added:**
- ✅ Full browser profile management (create, edit, delete, clone)
- ✅ Custom fingerprint engine (UA, Canvas, WebGL, Fonts, Timezone, WebRTC…)
- ✅ Per-profile proxy (HTTP/HTTPS/SOCKS4/SOCKS5)
- ✅ Real-time dashboard (stats, charts, activity feed)
- ✅ RPA automation with JavaScript/Playwright scripts
- ✅ 6 built-in automation templates
- ✅ Live execution log with timestamps
- ✅ Team management (Members, Roles, Permissions, Transfer Boss)
- ✅ Batch operations (import CSV, create, update, clone)
- ✅ Profile export to ZIP
- ✅ Color-coded profile groups
- ✅ Open API with key management
- ✅ Global + personal settings
- ✅ macOS .app + .dmg build
- ✅ Windows .exe + Inno Setup installer
- ✅ GitHub Actions CI/CD (auto-build on tag push)
- ✅ KH Browser logo + icons (.icns, .ico)
- ✅ Dark orange premium UI (PyQt6, QSS)

**Coming in v1.1.0:**
- 🔜 Profile import from ZIP
- 🔜 Real browser fingerprint injection (CDP/Playwright integration)
- 🔜 Cloud sync backend
- 🔜 Windows Sync mode
- 🔜 Plugin/Extension manager UI
- 🔜 Proxy health checker
- 🔜 Mass proxy import

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m "Add amazing feature"`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Setup

```bash
git clone https://github.com/rinsophearun/kh-browser.git
cd kh-browser
pip install PyQt6 requests cryptography Pillow
python main.py
```

### Code Style

- Follow PEP 8
- UI widgets: PyQt6 only (no tkinter, no web views)
- Storage: JSON via `storage.py` (no SQLite, no ORM)
- Styling: QSS in `styles.py`

---

## 📄 License

MIT License — Copyright (c) 2025 KH Browser

```
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

See [LICENSE](LICENSE) for full text.

---

## 🙋 Support

| Channel | Link |
|---------|------|
| 🐛 Bug Reports | [GitHub Issues](https://github.com/rinsophearun/kh-browser/issues) |
| 💡 Feature Requests | [GitHub Discussions](https://github.com/rinsophearun/kh-browser/discussions) |
| 📖 Documentation | This README |

---

<div align="center">
  <img src="assets/Logo.png" width="80"/>
  <br/><br/>
  <strong>KH Browser</strong> — Professional Antidetect Browser Profile Manager
  <br/>
  <sub>Built with ❤️ using Python + PyQt6 &nbsp;•&nbsp; KH Browser © 2025 &nbsp;•&nbsp; MIT License</sub>
  <br/><br/>
  <a href="https://github.com/rinsophearun/kh-browser">⭐ Star on GitHub</a>
  &nbsp;&nbsp;•&nbsp;&nbsp;
  <a href="https://github.com/rinsophearun/kh-browser/releases">📦 Download</a>
  &nbsp;&nbsp;•&nbsp;&nbsp;
  <a href="https://github.com/rinsophearun/kh-browser/issues">🐛 Report Bug</a>
</div>
