from dataclasses import dataclass, field
from typing import List, Dict, Any
import uuid
import datetime


def _uid():
    return str(uuid.uuid4())[:8].upper()


def _now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def _today():
    return datetime.datetime.now().strftime("%Y-%m-%d")


@dataclass
class ProxyConfig:
    type: str = "None"
    host: str = ""
    port: int = 0
    username: str = ""
    password: str = ""
    rotation_url: str = ""
    check_ip: str = ""

    def to_dict(self):
        return self.__dict__.copy()

    @staticmethod
    def from_dict(d):
        return ProxyConfig(**{k: v for k, v in d.items() if k in ProxyConfig.__dataclass_fields__})


@dataclass
class Fingerprint:
    user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    screen_width: int = 1920
    screen_height: int = 1080
    color_depth: int = 24
    pixel_ratio: float = 1.0
    timezone: str = "America/New_York"
    timezone_offset: int = -300
    language: str = "en-US"
    languages: str = "en-US,en;q=0.9"
    webgl_vendor: str = "Google Inc. (Intel)"
    webgl_renderer: str = "ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0)"
    canvas_noise: bool = True
    audio_noise: bool = True
    webrtc_mode: str = "disabled"
    fonts: List[str] = field(default_factory=lambda: ["Arial", "Times New Roman", "Verdana", "Georgia"])
    hardware_concurrency: int = 8
    device_memory: int = 8
    platform: str = "Win32"
    do_not_track: bool = False
    webgl_noise: bool = True
    client_rects_noise: bool = True
    media_devices: int = 3
    battery_level: float = 0.85
    battery_charging: bool = True
    flash: bool = False
    ports_protection: bool = True
    geolocation_mode: str = "based_on_ip"
    latitude: float = 40.7128
    longitude: float = -74.0060


@dataclass
class PlatformAccount:
    id: str = field(default_factory=_uid)
    platform: str = ""
    username: str = ""
    password: str = ""
    notes: str = ""


@dataclass
class BrowserProfile:
    id: str = field(default_factory=_uid)
    name: str = ""
    group: str = "Default"
    browser_type: str = "Chrome"
    browser_version: str = "120.0"
    os_type: str = "Windows"
    os_version: str = "10"
    fingerprint: Fingerprint = field(default_factory=Fingerprint)
    proxy: ProxyConfig = field(default_factory=ProxyConfig)
    accounts: List[PlatformAccount] = field(default_factory=list)
    extensions: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    notes: str = ""
    status: str = "stopped"
    created_at: str = field(default_factory=_now)
    last_used: str = ""
    cloud_synced: bool = False
    startup_url: str = ""

    def validate(self) -> tuple[bool, str]:
        """Validate profile with rules. Returns (is_valid, error_message)"""
        # Rule 1: Name is required and 2-100 characters
        if not self.name or not self.name.strip():
            return False, "Profile name is required"
        if len(self.name) < 2:
            return False, "Profile name must be at least 2 characters"
        if len(self.name) > 100:
            return False, "Profile name must be less than 100 characters"
        
        # Rule 2: Group is required and 1-50 characters
        if not self.group or not self.group.strip():
            return False, "Group name is required"
        if len(self.group) > 50:
            return False, "Group name must be less than 50 characters"
        
        # Rule 3: Browser type must be valid
        valid_browsers = ["Chrome", "Firefox", "Edge", "Safari", "Brave", "Opera"]
        if self.browser_type not in valid_browsers:
            return False, f"Invalid browser type. Must be one of: {', '.join(valid_browsers)}"
        
        # Rule 4: OS type must be valid
        valid_os = ["Windows", "macOS", "Linux", "Android", "iOS"]
        if self.os_type not in valid_os:
            return False, f"Invalid OS type. Must be one of: {', '.join(valid_os)}"
        
        # Rule 5: Status must be valid
        valid_status = ["running", "stopped", "loading"]
        if self.status not in valid_status:
            return False, f"Invalid status. Must be one of: {', '.join(valid_status)}"
        
        # Rule 6: Tags limit (max 10 tags)
        if len(self.tags) > 10:
            return False, "Maximum 10 tags allowed per profile"
        
        # Rule 7: Tag length validation (each 1-30 characters)
        for tag in self.tags:
            if not tag or len(tag) > 30:
                return False, "Each tag must be 1-30 characters"
        
        # Rule 8: Notes length limit (max 1000 characters)
        if len(self.notes) > 1000:
            return False, "Notes must be less than 1000 characters"
        
        # Rule 9: Accounts limit (max 50)
        if len(self.accounts) > 50:
            return False, "Maximum 50 platform accounts per profile"
        
        # Rule 10: Extensions limit (max 30)
        if len(self.extensions) > 30:
            return False, "Maximum 30 extensions per profile"
        
        # Rule 11: Startup URL validation
        if self.startup_url:
            if not self.startup_url.startswith(("http://", "https://", "about:", "chrome:")):
                return False, "Invalid startup URL. Must start with http://, https://, about:, or chrome:"
        
        return True, ""


@dataclass
class TeamMember:
    id: str = field(default_factory=_uid)
    name: str = ""
    email: str = ""
    role: str = "Member"
    status: str = "Active"
    max_profiles: int = 100
    max_devices: int = 3
    joined_at: str = field(default_factory=_today)
    last_login: str = ""
    shared_profiles: int = 0


@dataclass
class RPATask:
    id: str = field(default_factory=_uid)
    name: str = ""
    description: str = ""
    script: str = "// Write your automation script here\n\nawait page.goto('https://example.com');\n"
    profile_ids: List[str] = field(default_factory=list)
    schedule: str = ""
    repeat: str = "once"
    status: str = "idle"
    created_at: str = field(default_factory=_now)
    last_run: str = ""
    run_count: int = 0


@dataclass
class APIKey:
    id: str = field(default_factory=_uid)
    name: str = ""
    key: str = field(default_factory=lambda: "ak_live_" + str(uuid.uuid4()).replace("-", "")[:32])
    permissions: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=_today)
    last_used: str = ""
    active: bool = True
    request_count: int = 0


# ── Sample Data ────────────────────────────────────────────────────────────────

SAMPLE_PROFILES = [
]

SAMPLE_MEMBERS = [
    TeamMember(name="SOPHEARUN", email="sophearun@khbrowser.com", role="Creator",
               status="Active", max_profiles=1000, max_devices=10, joined_at="2023-06-01",
               last_login="2024-01-15 09:00", shared_profiles=120),
    TeamMember(name="Sarah Lee", email="sarah@company.com", role="Admin",
               status="Active", max_profiles=500, max_devices=5, joined_at="2023-07-15",
               last_login="2024-01-15 08:45", shared_profiles=85),
    TeamMember(name="Mike Chen", email="mike@company.com", role="Member",
               status="Active", max_profiles=100, max_devices=3, joined_at="2023-09-01",
               last_login="2024-01-14 17:20", shared_profiles=30),
    TeamMember(name="Emily Wang", email="emily@company.com", role="Member",
               status="Invited", max_profiles=100, max_devices=3, joined_at="2024-01-10"),
    TeamMember(name="Tom Davis", email="tom@company.com", role="Viewer",
               status="Active", max_profiles=50, max_devices=2, joined_at="2023-11-20",
               last_login="2024-01-13 10:00", shared_profiles=10),
]

SAMPLE_TASKS = [
    RPATask(name="Auto Login FB", description="Auto login to Facebook accounts", status="idle", run_count=5),
    RPATask(name="Post Scheduler", description="Schedule posts across platforms", status="scheduled", run_count=12),
    RPATask(name="Data Scraper", description="Scrape product data from Amazon", status="completed", run_count=3),
    RPATask(name="Account Warmer", description="Warm up new accounts with activity", status="running", run_count=1),
]

SAMPLE_API_KEYS = [
    APIKey(name="Production API", permissions=["read", "write", "delete"],
           request_count=1523, last_used="2024-01-15"),
    APIKey(name="Read-Only Key", permissions=["read"],
           request_count=89, last_used="2024-01-14"),
    APIKey(name="Dev Testing", permissions=["read", "write"],
           active=False, request_count=0),
]
