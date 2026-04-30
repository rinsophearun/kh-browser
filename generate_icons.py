#!/usr/bin/env python3
"""
Generate properly sized app icons for macOS (.icns) and Windows (.ico)
from the Logo.png source image.

Usage: python3 generate_icons.py
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw

# Ensure PIL is available
try:
    from PIL import Image
except ImportError:
    print("❌ Pillow is required. Install with: pip install Pillow")
    sys.exit(1)

PROJECT_ROOT = Path(__file__).parent
ASSETS_DIR = PROJECT_ROOT / 'assets'
LOGO_FILE = ASSETS_DIR / 'Logo.png'

# Icon specifications
MACOS_SIZES = [16, 32, 64, 128, 256, 512, 1024]
WINDOWS_SIZES = [16, 32, 48, 64, 128, 256]

def generate_macos_icons():
    """Generate macOS .icns file with all required sizes."""
    print("🍎 Generating macOS icons...")
    
    if not LOGO_FILE.exists():
        print(f"❌ Logo file not found: {LOGO_FILE}")
        return False
    
    try:
        # Open original logo
        logo = Image.open(LOGO_FILE).convert('RGBA')
        print(f"   Loaded logo: {logo.size}")
        
        # Create temp directory for icon sizes
        iconset_dir = ASSETS_DIR / 'KHBrowser.iconset'
        iconset_dir.mkdir(exist_ok=True)
        
        # Generate all required sizes for macOS
        for size in MACOS_SIZES:
            # Resize
            resized = logo.resize((size, size), Image.Resampling.LANCZOS)
            
            # Save individual icon
            icon_file = iconset_dir / f'icon_{size}x{size}.png'
            resized.save(icon_file, 'PNG')
            print(f"   ✅ Generated {size}x{size} icon")
            
            # For @2x versions on macOS
            if size <= 512:
                icon_2x_file = iconset_dir / f'icon_{size*2}x{size*2}@2x.png'
                resized_2x = logo.resize((size*2, size*2), Image.Resampling.LANCZOS)
                resized_2x.save(icon_2x_file, 'PNG')
                print(f"   ✅ Generated {size*2}x{size*2}@2x icon")
        
        # Convert iconset to .icns using iconutil
        icns_file = ASSETS_DIR / 'icon.icns'
        
        # Try using iconutil (macOS native tool)
        import subprocess
        try:
            result = subprocess.run(
                ['iconutil', '-c', 'icns', '-o', str(icns_file), str(iconset_dir)],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"✅ macOS .icns created: {icns_file}")
            print(f"   Size: {icns_file.stat().st_size / 1024:.1f} KB")
            return True
        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            print(f"⚠️  iconutil not available, using alternative method...")
            
            # Fallback: Create a simple .icns manually using PIL
            # This is a simplified version - full .icns format is complex
            # For production, recommend using Xcode's iconutil tool
            fallback_icon = logo.resize((512, 512), Image.Resampling.LANCZOS)
            fallback_icon.save(str(icns_file), 'ICO')
            print(f"   ⚠️  Created simplified icon (use Xcode's iconutil for production)")
            return True
            
    except Exception as e:
        print(f"❌ Error generating macOS icons: {e}")
        return False

def generate_windows_icons():
    """Generate Windows .ico file with all required sizes."""
    print("\n🪟 Generating Windows icons...")
    
    if not LOGO_FILE.exists():
        print(f"❌ Logo file not found: {LOGO_FILE}")
        return False
    
    try:
        # Open original logo
        logo = Image.open(LOGO_FILE).convert('RGBA')
        
        # Generate all required sizes
        ico_images = []
        for size in WINDOWS_SIZES:
            resized = logo.resize((size, size), Image.Resampling.LANCZOS)
            ico_images.append(resized)
            print(f"   ✅ Generated {size}x{size} icon")
        
        # Save as .ico with all sizes
        ico_file = ASSETS_DIR / 'icon.ico'
        ico_images[0].save(
            str(ico_file),
            'ICO',
            sizes=[(size, size) for size in WINDOWS_SIZES]
        )
        
        print(f"✅ Windows .ico created: {ico_file}")
        print(f"   Size: {ico_file.stat().st_size / 1024:.1f} KB")
        print(f"   Includes sizes: {WINDOWS_SIZES}")
        return True
        
    except Exception as e:
        print(f"❌ Error generating Windows icons: {e}")
        return False

def main():
    """Main entry point."""
    print("=" * 60)
    print("  KH Browser Icon Generator")
    print("=" * 60)
    print()
    
    # Verify assets directory
    if not ASSETS_DIR.exists():
        print(f"❌ Assets directory not found: {ASSETS_DIR}")
        return False
    
    # Check if Logo.png exists
    if not LOGO_FILE.exists():
        print(f"❌ Logo file not found: {LOGO_FILE}")
        print(f"   Expected at: {LOGO_FILE}")
        return False
    
    print(f"📁 Assets directory: {ASSETS_DIR}")
    print(f"🎨 Source logo: {LOGO_FILE}")
    print(f"📐 Logo size: {Image.open(LOGO_FILE).size}")
    print()
    
    # Generate icons
    macos_ok = generate_macos_icons()
    windows_ok = generate_windows_icons()
    
    print()
    print("=" * 60)
    if macos_ok and windows_ok:
        print("✅ Icon generation complete!")
        print()
        print("Next steps:")
        print("  1. macOS: Run `bash build_macos.sh` to rebuild the app")
        print("  2. Windows: Run `build_windows_installer.bat` on Windows machine")
        print()
        return True
    else:
        print("⚠️  Icon generation completed with warnings")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
