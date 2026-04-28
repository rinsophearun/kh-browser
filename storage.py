"""Persistent storage — saves/loads all profiles to ~/.khbrowser/profiles.json"""
import json
import os
import dataclasses
from pathlib import Path
from typing import List

from models import BrowserProfile, Fingerprint, ProxyConfig, PlatformAccount

STORAGE_DIR = Path.home() / ".khbrowser"
PROFILES_FILE = STORAGE_DIR / "profiles.json"


def _ensure_dir():
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)


# ── Serialisation helpers ──────────────────────────────────────────────────────

def _profile_to_dict(p: BrowserProfile) -> dict:
    d = dataclasses.asdict(p)
    return d


def _profile_from_dict(d: dict) -> BrowserProfile:
    # Nested objects
    fp_data = d.pop("fingerprint", {})
    proxy_data = d.pop("proxy", {})
    accounts_data = d.pop("accounts", [])

    fp = Fingerprint(**{k: v for k, v in fp_data.items()
                        if k in Fingerprint.__dataclass_fields__})
    proxy = ProxyConfig(**{k: v for k, v in proxy_data.items()
                           if k in ProxyConfig.__dataclass_fields__})
    accounts = [
        PlatformAccount(**{k: v for k, v in a.items()
                           if k in PlatformAccount.__dataclass_fields__})
        for a in accounts_data
    ]

    # Only pass known fields to BrowserProfile
    known = {k for k in BrowserProfile.__dataclass_fields__}
    safe = {k: v for k, v in d.items() if k in known}

    return BrowserProfile(fingerprint=fp, proxy=proxy, accounts=accounts, **safe)


# ── Public API ─────────────────────────────────────────────────────────────────

def load_profiles() -> List[BrowserProfile]:
    """Load saved profiles. Returns empty list if none saved yet."""
    _ensure_dir()
    if not PROFILES_FILE.exists():
        return []
    try:
        with open(PROFILES_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return [_profile_from_dict(d) for d in raw]
    except Exception as e:
        print(f"[storage] Failed to load profiles: {e}")
        return []


def save_profiles(profiles: List[BrowserProfile]):
    """Save all profiles to disk immediately."""
    _ensure_dir()
    try:
        data = [_profile_to_dict(p) for p in profiles]
        tmp = PROFILES_FILE.with_suffix(".json.tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        tmp.replace(PROFILES_FILE)          # atomic write
    except Exception as e:
        print(f"[storage] Failed to save profiles: {e}")


def delete_profile_data(profile_id: str):
    """Remove the browser user-data directory for a deleted profile."""
    import shutil
    profile_dir = STORAGE_DIR / "profiles" / profile_id
    if profile_dir.exists():
        shutil.rmtree(profile_dir, ignore_errors=True)
