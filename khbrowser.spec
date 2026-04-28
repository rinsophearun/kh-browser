# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for KH Browser
# Builds for macOS (.app / .dmg) and Windows (.exe)

import sys
from PyInstaller.utils.hooks import collect_all

block_cipher = None

# Collect all PyQt6 data / binaries
datas_qt, binaries_qt, hiddenimports_qt = collect_all('PyQt6')

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=binaries_qt,
    datas=datas_qt + [
        # Include any local resource files here if you add icons/images later
        # ('assets/*', 'assets'),
    ],
    hiddenimports=hiddenimports_qt + [
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.QtNetwork',
        'cryptography',
        'requests',
        'json',
        'subprocess',
        'threading',
        'uuid',
        'datetime',
        # App modules
        'main_window',
        'dashboard_panel',
        'groups_panel',
        'profile_dialog',
        'team_dialog',
        'browser_launcher',
        'storage',
        'models',
        'styles',
        'rpa_dialog',
        'batch_dialog',
        'settings_dialog',
        'api_dialog',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'cv2',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# ─── macOS / Linux: single directory bundle ───────────────────────────────────
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='KHBrowser',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,              # No terminal window
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.icns' if sys.platform == 'darwin' else 'assets/icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='KHBrowser',
)

# ─── macOS .app bundle ────────────────────────────────────────────────────────
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='KHBrowser.app',
        icon='assets/icon.icns',
        bundle_identifier='com.khbrowser.app',
        info_plist={
            'NSPrincipalClass': 'NSApplication',
            'NSHighResolutionCapable': True,
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleVersion': '1.0.0',
            'CFBundleName': 'KH Browser',
            'CFBundleDisplayName': 'KH Browser',
            'LSMinimumSystemVersion': '10.15',
            'NSRequiresAquaSystemAppearance': False,
        },
    )
