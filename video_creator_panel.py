"""
Video Creator Panel - Wraps video_creator_qt.py MainWindow as a QWidget panel
for embedding in KH Browser sidebar.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt


class VideoCreatorPanel(QWidget):
    """Wrapper to embed VideoCreatorApp MainWindow as a panel."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background: #07070e;")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        
        try:
            from video_creator_qt import MainWindow as VideoCreatorApp
            
            # Create the video creator app and extract its central widget
            self.video_app = VideoCreatorApp()
            
            # Get the central widget from MainWindow
            central = self.video_app.centralWidget()
            
            # Reparent it to this panel
            central.setParent(self)
            lay.addWidget(central)
            
            # Hide the window but keep the widget active
            self.video_app.hide()
            
        except ImportError as e:
            # Fallback if PIL or ffmpeg missing
            from PyQt6.QtWidgets import QLabel
            lbl = QLabel(f"⚠️  Video Creator requires:\n• pip install Pillow\n• brew install ffmpeg\n\nError: {e}")
            lbl.setStyleSheet("color: #CBD5E1; padding: 20px;")
            lay.addWidget(lbl)
            self.video_app = None
        except Exception as e:
            from PyQt6.QtWidgets import QLabel
            lbl = QLabel(f"❌ Failed to load Video Creator:\n{str(e)}")
            lbl.setStyleSheet("color: #e05555; padding: 20px;")
            lay.addWidget(lbl)
            self.video_app = None
    
    def closeEvent(self, event):
        """Clean up video app on close."""
        try:
            if self.video_app:
                self.video_app.close()
        except Exception:
            pass
        super().closeEvent(event)
