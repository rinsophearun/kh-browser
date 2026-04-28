"""Real browser launcher — finds Chrome/Brave/Chromium and launches with isolated profile."""
import subprocess
import os
import platform
import shutil
from pathlib import Path
from models import BrowserProfile


# ── Locate browser executables ─────────────────────────────────────────────────

BROWSERS = {
    "Chrome": {
        "Darwin": [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        ],
        "Windows": [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        ],
        "Linux": [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            shutil.which("google-chrome") or "",
            shutil.which("google-chrome-stable") or "",
        ],
    },
    "Firefox": {
        "Darwin": [
            "/Applications/Firefox.app/Contents/MacOS/firefox",
        ],
        "Windows": [
            r"C:\Program Files\Mozilla Firefox\firefox.exe",
            r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
        ],
        "Linux": [
            "/usr/bin/firefox",
            shutil.which("firefox") or "",
        ],
    },
    "Edge": {
        "Darwin": [
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        ],
        "Windows": [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        ],
        "Linux": [
            "/usr/bin/microsoft-edge",
            shutil.which("microsoft-edge") or "",
        ],
    },
    "Brave": {
        "Darwin": [
            "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        ],
        "Windows": [
            os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe"),
        ],
        "Linux": [
            "/usr/bin/brave-browser",
            shutil.which("brave-browser") or "",
        ],
    },
    "Safari": {
        "Darwin": [
            "/Applications/Safari.app/Contents/MacOS/Safari",
        ],
        "Windows": [],
        "Linux": [],
    },
    "Opera": {
        "Darwin": [
            "/Applications/Opera.app/Contents/MacOS/Opera",
        ],
        "Windows": [
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\Opera\opera.exe"),
        ],
        "Linux": [
            "/usr/bin/opera",
            shutil.which("opera") or "",
        ],
    },
}

# Chromium fallback (works for Chrome, Edge, Brave profiles)
CHROMIUM_FALLBACK = {
    "Darwin": [
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ],
    "Windows": [],
    "Linux": [
        shutil.which("chromium-browser") or "",
        shutil.which("chromium") or "",
    ],
}


def find_browser(browser_type: str) -> str | None:
    """Find the executable path for the requested browser type."""
    system = platform.system()

    # Try exact match first
    candidates = BROWSERS.get(browser_type, {}).get(system, [])
    for path in candidates:
        if path and os.path.exists(path):
            return path

    # Safari on macOS — always available, use 'open' fallback
    if browser_type == "Safari" and system == "Darwin":
        return "/Applications/Safari.app/Contents/MacOS/Safari"

    # For Chromium-based browsers (Chrome, Edge, Brave, Opera) fall back to any Chromium
    chromium_types = {"Chrome", "Edge", "Brave", "Opera"}
    if browser_type in chromium_types:
        for path in CHROMIUM_FALLBACK.get(system, []):
            if path and os.path.exists(path):
                return path

    return None


def get_profile_dir(profile_id: str) -> Path:
    """Return (and create) an isolated user-data directory for this profile."""
    data_dir = Path.home() / ".khbrowser" / "profiles" / profile_id
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def build_chrome_args(exe: str, profile: BrowserProfile) -> list[str]:
    """Build Chromium command-line flags for the profile."""
    data_dir = get_profile_dir(profile.id)
    fp = profile.fingerprint

    args = [
        exe,
        f"--user-data-dir={data_dir}",
        # Window size matches fingerprint screen
        f"--window-size={fp.screen_width},{fp.screen_height}",
        # Locale / language
        f"--lang={fp.language}",
        f"--accept-lang={fp.language}",
        # Hide automation flags
        "--disable-blink-features=AutomationControlled",
        "--disable-infobars",
        # First-run suppression
        "--no-first-run",
        "--no-default-browser-check",
        "--no-service-autorun",
        # Background throttling disabled (keep active)
        "--disable-background-timer-throttling",
        "--disable-backgrounding-occluded-windows",
        "--disable-renderer-backgrounding",
        # Notifications off
        "--disable-notifications",
        "--disable-popup-blocking",
    ]

    # ── Proxy ────────────────────────────────────────────────────────────────
    if profile.proxy.type not in ("None", "") and profile.proxy.host:
        ptype = profile.proxy.type.lower()
        host  = profile.proxy.host
        port  = profile.proxy.port or 8080
        if ptype in ("socks4", "socks5"):
            args.append(f"--proxy-server={ptype}://{host}:{port}")
        else:
            args.append(f"--proxy-server={host}:{port}")

    # ── WebRTC ───────────────────────────────────────────────────────────────
    if fp.webrtc_mode == "disabled":
        args.append("--disable-webrtc")

    # ── Extensions ───────────────────────────────────────────────────────────
    if not profile.extensions:
        args.append("--disable-extensions")

    # ── Startup URL ──────────────────────────────────────────────────────────
    if profile.startup_url:
        args.append(profile.startup_url)
    else:
        args.append("about:blank")

    return args


def build_safari_args(exe: str, profile: BrowserProfile) -> list[str]:
    """
    Safari does not support Chrome-style --flags.
    We launch it via 'open -na Safari --args <url>' on macOS,
    or directly via the binary with just the URL.
    """
    # 'open' gives a clean launch and respects macOS sandboxing
    args = ["open", "-na", "Safari"]
    if profile.startup_url:
        args += ["--args", profile.startup_url]
    return args



    """Build Firefox command-line flags."""
    profile_dir = get_profile_dir(profile.id) / "firefox"
    profile_dir.mkdir(parents=True, exist_ok=True)
    args = [
        exe,
        "--profile", str(profile_dir),
        "--no-remote",
        "--new-instance",
    ]
    if profile.startup_url:
        args.append(profile.startup_url)
    return args


# ── Public API ─────────────────────────────────────────────────────────────────

def launch_profile(profile: BrowserProfile) -> tuple[bool, str, object]:
    """
    Launch a browser for this profile.
    Returns (success: bool, message: str, process: Popen | None)
    """
    exe = find_browser(profile.browser_type)

    if not exe:
        # Last-ditch: try open -a "Google Chrome" on macOS
        if platform.system() == "Darwin":
            app_map = {
                "Chrome":  "Google Chrome",
                "Firefox": "Firefox",
                "Edge":    "Microsoft Edge",
                "Brave":   "Brave Browser",
            }
            app_name = app_map.get(profile.browser_type)
            if app_name:
                try:
                    cmd = ["open", "-na", app_name, "--args",
                           "--no-first-run", "--no-default-browser-check",
                           f"--user-data-dir={get_profile_dir(profile.id)}"]
                    if profile.startup_url:
                        cmd.append(profile.startup_url)
                    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    return True, f"Launched {app_name} via macOS open (PID {proc.pid})", proc
                except Exception as e:
                    return False, f"macOS open failed: {e}", None

        return False, (
            f"{profile.browser_type} not found.\n\n"
            f"Please install it or check its path.\n"
            f"Supported: Chrome, Firefox, Edge, Brave, Safari, Opera"
        ), None

    try:
        btype = profile.browser_type
        if btype == "Safari":
            args = build_safari_args(exe, profile)
        elif btype == "Firefox":
            args = build_firefox_args(exe, profile)
        else:
            # Chromium-based: Chrome, Edge, Brave, Opera
            args = build_chrome_args(exe, profile)

        proc = subprocess.Popen(
            args,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            close_fds=True,
        )
        return True, f"Launched {btype} — PID {proc.pid}", proc

    except Exception as e:
        return False, f"Failed to launch {profile.browser_type}: {e}", None


def stop_profile(proc) -> bool:
    """Terminate a browser process."""
    if proc is None:
        return False
    if proc.poll() is None:       # still running
        proc.terminate()
        return True
    return False
