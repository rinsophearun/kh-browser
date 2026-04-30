"""Asset path utilities for cross-platform compatibility."""
from pathlib import Path
import os


def get_asset_path(filename: str) -> str:
    """Get cross-platform asset path.
    
    Works from any working directory by finding assets relative to this script.
    Args:
        filename: Asset filename (e.g., 'Logo.png', 'icon.png')
    
    Returns:
        Absolute path to asset file as string
    """
    # Try relative to this module first
    script_dir = Path(__file__).parent
    asset_path = script_dir / "assets" / filename
    
    if asset_path.exists():
        return str(asset_path)
    
    # Fallback: try relative to current working directory
    cwd_asset = Path.cwd() / "assets" / filename
    if cwd_asset.exists():
        return str(cwd_asset)
    
    # Return empty string if not found (graceful fallback)
    return ""
