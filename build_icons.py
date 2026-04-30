# -*- coding: utf-8 -*-
"""
build_icons.py  -  Auto-generate icon.icns (macOS) and icon.ico (Windows)
Run this once before building, or it's called automatically by the build scripts.
"""
import os, sys, io

# Force UTF-8 output on Windows (cp1252 can't print emoji)
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

os.makedirs("assets", exist_ok=True)

# ── Generate base 512x512 PNG via PyQt6 ──────────────────────────────────────
try:
    # On headless CI (Windows/Linux) set offscreen platform before QApplication
    if not os.environ.get("DISPLAY") and sys.platform != "darwin":
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

    from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont, QBrush, QRadialGradient
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtCore import Qt

    _app = QApplication.instance() or QApplication(sys.argv)

    pm = QPixmap(512, 512)
    pm.fill(QColor("#0d0d0d"))
    p = QPainter(pm)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)

    grad = QRadialGradient(256, 256, 256)
    grad.setColorAt(0, QColor("#ff8c00"))
    grad.setColorAt(1, QColor("#cc5500"))
    p.setBrush(QBrush(grad))
    p.setPen(Qt.PenStyle.NoPen)
    p.drawEllipse(20, 20, 472, 472)

    font = QFont(".AppleSystemUIFont", 160, QFont.Weight.Bold)
    p.setFont(font)
    p.setPen(QColor("white"))
    p.drawText(pm.rect(), Qt.AlignmentFlag.AlignCenter, "KH")
    p.end()

    pm.save("assets/icon.png")
    print("✅  assets/icon.png created (512×512)")

except Exception as e:
    print(f"⚠️  PyQt6 icon generation failed: {e}")
    sys.exit(1)

# ── macOS .icns ───────────────────────────────────────────────────────────────
if sys.platform == "darwin":
    import subprocess, shutil

    iconset = "assets/icon.iconset"
    os.makedirs(iconset, exist_ok=True)
    sizes = [16, 32, 64, 128, 256, 512]
    for s in sizes:
        subprocess.run(["sips", "-z", str(s), str(s), "assets/icon.png",
                        "--out", f"{iconset}/icon_{s}x{s}.png"], check=True,
                       capture_output=True)
    for s in [16, 32, 64, 128, 256]:
        subprocess.run(["sips", "-z", str(s*2), str(s*2), "assets/icon.png",
                        "--out", f"{iconset}/icon_{s}x{s}@2x.png"], check=True,
                       capture_output=True)
    subprocess.run(["iconutil", "-c", "icns", iconset, "-o", "assets/icon.icns"],
                   check=True, capture_output=True)
    shutil.rmtree(iconset)
    print("✅  assets/icon.icns created")

# ── Windows .ico ──────────────────────────────────────────────────────────────
try:
    from PIL import Image

    base = Image.open("assets/icon.png").convert("RGBA")
    ico_sizes = [16, 32, 48, 64, 128, 256]
    frames = [base.resize((s, s), Image.LANCZOS) for s in ico_sizes]
    frames[0].save(
        "assets/icon.ico",
        format="ICO",
        sizes=[(s, s) for s in ico_sizes],
        append_images=frames[1:],
    )
    print("✅  assets/icon.ico created")
except ImportError:
    print("⚠️  Pillow not installed — skipping icon.ico (pip install Pillow)")
except Exception as e:
    print(f"⚠️  icon.ico failed: {e}")

print("\n✅  All icons ready in assets/")
