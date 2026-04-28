"""Entry point for KH Browser."""
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon


def main():
    # Must set BEFORE QApplication is created
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("KH Browser")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("KHBrowser")

    from main_window import MainWindow
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
