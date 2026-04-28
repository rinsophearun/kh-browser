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
    BrowserProfile(id="A1B2C3D4", name="FB Account 1", group="Facebook",
                   browser_type="Chrome", os_type="Windows", status="stopped",
                   last_used="2024-01-15 10:30", cloud_synced=True),
    BrowserProfile(id="E5F6G7H8", name="Instagram Pro", group="Social Media",
                   browser_type="Firefox", os_type="macOS", status="running",
                   last_used="2024-01-15 09:15", cloud_synced=True),
    BrowserProfile(id="I9J0K1L2", name="Shopify Store", group="E-commerce",
                   browser_type="Chrome", os_type="Windows", status="stopped",
                   last_used="2024-01-14 18:22"),
    BrowserProfile(id="M3N4O5P6", name="Twitter Bot", group="Social Media",
                   browser_type="Edge", os_type="Windows", status="stopped",
                   last_used="2024-01-14 15:45"),
    BrowserProfile(id="Q7R8S9T0", name="Amazon Seller", group="E-commerce",
                   browser_type="Chrome", os_type="Windows", status="running",
                   last_used="2024-01-15 08:00", cloud_synced=True),
    BrowserProfile(id="U1V2W3X4", name="TikTok Creator", group="Content",
                   browser_type="Chrome", os_type="macOS", status="stopped",
                   last_used="2024-01-13 20:10"),
    BrowserProfile(id="Y5Z6A7B8", name="LinkedIn Outreach", group="B2B",
                   browser_type="Chrome", os_type="Windows", status="stopped",
                   last_used="2024-01-12 11:00"),
    BrowserProfile(id="C9D0E1F2", name="Reddit Account", group="Social Media",
                   browser_type="Firefox", os_type="Linux", status="stopped",
                   last_used="2024-01-11 14:30"),
]

SAMPLE_MEMBERS = [
    TeamMember(name="John Smith", email="john@company.com", role="Owner",
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
