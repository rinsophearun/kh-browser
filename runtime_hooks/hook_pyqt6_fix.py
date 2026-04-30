"""
PyQt6 library path fix for macOS bundled apps.
Ensures QtCore and other frameworks are found correctly.
"""
import sys
import os
from pathlib import Path

# Get app bundle path
if hasattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):
    # PyInstaller bundled app
    app_path = Path(sys._MEIPASS)
    
    # Add Qt plugins and frameworks to library search path
    qt_path = app_path / 'PyQt6' / 'Qt6'
    
    # Set environment variables for Qt
    if (qt_path / 'lib').exists():
        dyld_path = os.environ.get('DYLD_FALLBACK_LIBRARY_PATH', '')
        dyld_path = f"{qt_path / 'lib'}:{dyld_path}"
        os.environ['DYLD_FALLBACK_LIBRARY_PATH'] = dyld_path
    
    # Ensure Qt plugins are found
    if (qt_path / 'plugins').exists():
        qt_plugin_path = os.environ.get('QT_PLUGIN_PATH', '')
        qt_plugin_path = f"{qt_path / 'plugins'}:{qt_plugin_path}"
        os.environ['QT_PLUGIN_PATH'] = qt_plugin_path
