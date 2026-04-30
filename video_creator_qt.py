#!/usr/bin/env python3
"""
◆  VIDEO CREATOR v1.1.1  —  PyQt6 Desktop Application
Batch-converts images to MP4 videos with optional background music.

Requirements : pip install PyQt6 Pillow
System dep   : ffmpeg  (brew install ffmpeg)
"""

import os, sys, re, shutil, random, platform, subprocess
from pathlib import Path
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QSpinBox, QComboBox,
    QScrollArea, QFrame, QFileDialog, QTextEdit,
    QTableWidget, QTableWidgetItem,
    QHeaderView, QSizePolicy, QButtonGroup,
    QAbstractItemView, QLayout, QProgressBar,
)
from PyQt6.QtCore import (
    Qt, QThread, pyqtSignal, pyqtProperty,
    QSize, QRect, QPoint,
    QPropertyAnimation, QEasingCurve,
)
from PyQt6.QtGui import (
    QPixmap, QImage, QColor, QCursor,
    QPainter, QBrush, QPen, QLinearGradient,
)

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# ── Constants ─────────────────────────────────────────────────────────────────
VERSION  = "v1.1.1"
FPS      = 30
BITRATE  = "6M"
IMG_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".heic", ".avif"}
AUD_EXTS = {".mp3", ".wav", ".aac", ".m4a", ".flac", ".ogg", ".opus"}
QUALITIES = {
    "Full HD":  {"res": "1080x1920", "label": "1080 × 1920"},
    "4K Ultra": {"res": "2160x3840", "label": "2160 × 3840"},
}

# ── Theme / QSS ───────────────────────────────────────────────────────────────
APP_QSS = """
* {
    font-family: 'Inter', 'SF Pro Display', 'Segoe UI', system-ui, sans-serif;
}
QMainWindow, QWidget {
    background: #0F172A;
    color: #FFFFFF;
    font-size: 13px;
}

/* ── Top Bar ── */
QFrame#topbar {
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
        stop:0 #1E293B, stop:1 #192134);
    border-bottom: 1px solid rgba(255,255,255,0.08);
}

/* ── Cards ── */
QFrame#card {
    background: #192134;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
}
QFrame#leftPanel {
    background: #0F172A;
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* ── Labels ── */
QLabel#sectionLabel {
    color: #94A3B8;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2.5px;
    background: transparent;
}
QLabel#titleLabel {
    color: #2563EB;
    font-size: 15px;
    font-weight: 800;
    letter-spacing: 5px;
    background: transparent;
}
QLabel#versionLabel {
    color: #94A3B8;
    font-size: 9px;
    font-weight: 600;
    background: #1E293B;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 4px;
    padding: 2px 8px;
    letter-spacing: 1px;
}

/* ── Quality Buttons ── */
QPushButton#qualityBtn {
    background: #1E293B;
    color: #94A3B8;
    border: 1.5px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 10px 16px;
    font-size: 12px;
    font-weight: 600;
    text-align: left;
}
QPushButton#qualityBtn:hover {
    background: #334155;
    border-color: rgba(37,99,235,0.35);
    color: #CBD5E1;
}
QPushButton#qualityBtn[active="true"] {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
        stop:0 rgba(37,99,235,0.13), stop:1 rgba(37,99,235,0.06));
    border-color: rgba(37,99,235,0.65);
    color: #2563EB;
}

/* ── Source / Browse Buttons ── */
QPushButton#sourceBtn {
    background: #1E293B;
    color: #94A3B8;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 7px 10px;
    font-size: 11px;
    font-weight: 500;
}
QPushButton#sourceBtn:hover {
    background: #334155;
    color: #FFFFFF;
    border-color: rgba(37,99,235,0.3);
}
QPushButton#browseBtn {
    background: #1E293B;
    color: #94A3B8;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 7px;
    padding: 4px 12px;
    font-size: 11px;
    font-weight: 500;
}
QPushButton#browseBtn:hover {
    background: #334155;
    color: #FFFFFF;
    border-color: rgba(37,99,235,0.3);
}
QPushButton#labelActionBtn {
    background: transparent;
    color: #64748B;
    border: none;
    font-size: 11px;
    padding: 0 4px;
}
QPushButton#labelActionBtn:hover { color: #DC2626; }

/* ── Save / Stop Buttons ── */
QPushButton#btnSave {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #2563EB, stop:1 #1d4ed8);
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 800;
    letter-spacing: 1.5px;
    min-height: 48px;
    padding: 12px 20px;
}
QPushButton#btnSave:hover {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #3b82f6, stop:1 #2563EB);
    padding: 12px 24px;
}
QPushButton#btnSave:pressed {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #1e40af, stop:1 #1d4ed8);
}
QPushButton#btnSave:disabled {
    background: #1E293B;
    color: #64748B;
}
QPushButton#btnStop {
    background: transparent;
    color: #94A3B8;
    border: 2px solid #475569;
    border-radius: 10px;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 1.5px;
    min-height: 48px;
    padding: 12px 20px;
}
QPushButton#btnStop:hover:!disabled {
    background: rgba(220,38,38,0.1);
    color: #DC2626;
    border-color: rgba(220,38,38,0.6);
    padding: 12px 24px;
}
QPushButton#btnStop:pressed:!disabled {
    background: rgba(220,38,38,0.2);
    border-color: #DC2626;
}
QPushButton#btnStop:disabled {
    color: #475569;
    border-color: #1E293B;
}

/* ── Open Button in table ── */
QPushButton#tblBtn {
    background: rgba(37,99,235,0.1);
    color: #2563EB;
    border: 1px solid rgba(37,99,235,0.25);
    border-radius: 12px;
    font-size: 10px;
    font-weight: 600;
    padding: 3px 10px;
}
QPushButton#tblBtn:hover {
    background: rgba(37,99,235,0.2);
    border-color: rgba(37,99,235,0.5);
}

/* ── SpinBox ── */
QSpinBox {
    background: #1E293B;
    color: #FFFFFF;
    border: 1.5px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 6px 8px;
    min-width: 76px;
    font-size: 14px;
    font-weight: 600;
}
QSpinBox:focus { border-color: rgba(37,99,235,0.5); }
QSpinBox::up-button, QSpinBox::down-button {
    background: #334155;
    border: none;
    width: 20px;
    border-radius: 4px;
}
QSpinBox::up-button:hover, QSpinBox::down-button:hover { background: #475569; }

/* ── ScrollArea ── */
QScrollArea { border: none; background: transparent; }
QScrollBar:vertical {
    background: transparent;
    width: 4px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background: #2563EB;
    border-radius: 2px;
    min-height: 20px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal { height: 0; }

/* ── Table ── */
QTableWidget {
    background: #192134;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    gridline-color: rgba(255,255,255,0.05);
    outline: none;
}
QTableWidget::item { padding: 6px 10px; border: none; }
QTableWidget::item:selected { background: #334155; }
QHeaderView::section {
    background: #192134;
    color: #94A3B8;
    border: none;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    padding: 6px 10px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
}
QHeaderView { background: transparent; }

/* ── Console ── */
QTextEdit#console {
    background: #0F172A;
    color: #94A3B8;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 10px 12px;
    font-family: 'JetBrains Mono', 'Cascadia Code', 'Fira Code', 'Courier New', monospace;
    font-size: 11px;
    line-height: 1.5;
}

/* ── Status/Progress labels ── */
QLabel#thumbCount  { color: #64748B; font-size: 11px; background: transparent; }
QLabel#statusLabel { color: #94A3B8; font-size: 12px; background: transparent; }
QLabel#pctLabel    { color: #2563EB; font-size: 12px; font-weight: 700; min-width: 40px; background: transparent; }
QLabel#pathLabel   { color: #64748B; font-size: 12px; background: transparent; }
QLabel#pathLabel[set="true"] { color: #2563EB; }
QLabel#dotLabel    { font-size: 10px; color: #64748B; background: transparent; }
QLabel#dotLabel[active="true"] { color: #10b981; }
QLabel#srcCount    { color: #94A3B8; font-size: 12px; background: transparent; }

/* ── Export Mode Buttons ── */
QPushButton#modeBtn {
    background: #1E293B;
    color: #94A3B8;
    border: 1.5px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 8px 14px;
    font-size: 12px;
    font-weight: 600;
}
QPushButton#modeBtn:hover { border-color: rgba(37,99,235,0.35); color: #CBD5E1; }
QPushButton#modeBtn[active="true"] {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
        stop:0 rgba(37,99,235,0.13), stop:1 rgba(37,99,235,0.06));
    border-color: rgba(37,99,235,0.65);
    color: #2563EB;
}

/* ── Encoder Combo ── */
QComboBox {
    background: #1E293B;
    color: #FFFFFF;
    border: 1.5px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 5px 10px;
    font-size: 12px;
    font-weight: 600;
    min-width: 180px;
}
QComboBox:focus { border-color: rgba(37,99,235,0.5); }
QComboBox:hover { border-color: rgba(37,99,235,0.3); }
QComboBox::drop-down {
    border: none;
    width: 24px;
}
QComboBox::down-arrow {
    width: 10px;
    height: 10px;
}
QComboBox QAbstractItemView {
    background: #192134;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    color: #FFFFFF;
    selection-background-color: rgba(37,99,235,0.15);
    selection-color: #2563EB;
    padding: 4px;
    outline: none;
}

/* ── Progress Bar ── */
QProgressBar {
    background: #1E293B;
    border: none;
    border-radius: 4px;
    height: 8px;
}
QProgressBar::chunk {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #2563EB, stop:1 #1d4ed8);
    border-radius: 4px;
}
"""


# ── Utility ───────────────────────────────────────────────────────────────────
def find_ffmpeg() -> str | None:
    ff = shutil.which("ffmpeg")
    if ff:
        return ff
    for p in ["/opt/homebrew/bin/ffmpeg", "/usr/local/bin/ffmpeg",
              "/usr/bin/ffmpeg", "/snap/bin/ffmpeg"]:
        if os.path.isfile(p):
            return p
    return None


def detect_hw_encoders(ffmpeg_bin: str) -> list[tuple[str, str]]:
    """
    Return all available hardware H.264 encoders as list of (encoder_id, display_label).
    Order: NVENC → VideoToolbox → VAAPI
    """
    candidates = [
        ("h264_nvenc",         "NVIDIA NVENC"),
        ("h264_videotoolbox",  "Apple VideoToolbox"),
        ("h264_vaapi",         "VAAPI  (Intel / AMD)"),
    ]
    found = []
    try:
        r = subprocess.run(
            [ffmpeg_bin, "-hide_banner", "-encoders"],
            capture_output=True, text=True, timeout=5,
        )
        for enc_id, label in candidates:
            if enc_id in r.stdout:
                found.append((enc_id, label))
    except Exception:
        pass
    return found

def detect_hw_encoder(ffmpeg_bin: str) -> tuple[str | None, str | None]:
    """Return (encoder_id, label) for best available HW encoder, or (None, None)."""
    found = detect_hw_encoders(ffmpeg_bin)
    return found[0] if found else (None, None)



# ── Toggle Switch ─────────────────────────────────────────────────────────────
class ToggleSwitch(QWidget):
    """Animated iOS-style toggle that replaces QCheckBox for binary settings."""
    toggled = pyqtSignal(bool)

    def __init__(self, parent=None, checked=False, enabled=True):
        super().__init__(parent)
        self.setFixedSize(48, 26)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._checked  = checked
        self._enabled  = enabled
        self._handle_x = 22 if checked else 2

        self._anim = QPropertyAnimation(self, b"handle_pos", self)
        self._anim.setDuration(160)
        self._anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

    @pyqtProperty(float)
    def handle_pos(self):
        return self._handle_x

    @handle_pos.setter
    def handle_pos(self, v):
        self._handle_x = v
        self.update()

    def isChecked(self) -> bool:
        return self._checked

    def setChecked(self, v: bool):
        self._checked = v
        self._handle_x = 22 if v else 2
        self.update()

    def setEnabled(self, v: bool):
        self._enabled = v
        self.update()

    def mousePressEvent(self, event):
        if self._enabled:
            self._checked = not self._checked
            target = 22 if self._checked else 2
            self._anim.setStartValue(self._handle_x)
            self._anim.setEndValue(float(target))
            self._anim.start()
            self.toggled.emit(self._checked)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Track
        if not self._enabled:
            track_color = QColor("#13142a")
        elif self._checked:
            track_color = QColor("#f0a800")
        else:
            track_color = QColor("#1a1b30")
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QBrush(track_color))
        p.drawRoundedRect(0, 3, 48, 20, 10, 10)

        # Handle
        handle_color = QColor("#888899") if not self._enabled else QColor("#ffffff")
        p.setBrush(QBrush(handle_color))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(int(self._handle_x), 5, 16, 16)
        p.end()


class FlowLayout(QLayout):
    """Wrapping flow layout — items left-to-right, wraps to next row."""

    def __init__(self, parent=None, h_spacing=8, v_spacing=8):
        super().__init__(parent)
        self._items      = []
        self._h_spacing  = h_spacing
        self._v_spacing  = v_spacing

    def addItem(self, item):
        self._items.append(item)

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        return self._items[index] if 0 <= index < len(self._items) else None

    def takeAt(self, index):
        return self._items.pop(index) if 0 <= index < len(self._items) else None

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self._layout(QRect(0, 0, width, 0), dry_run=True)

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self._layout(rect, dry_run=False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        m = self.contentsMargins()
        return size + QSize(m.left() + m.right(), m.top() + m.bottom())

    def _layout(self, rect, dry_run):
        m  = self.contentsMargins()
        r  = rect.adjusted(m.left(), m.top(), -m.right(), -m.bottom())
        x, y, row_h = r.x(), r.y(), 0

        for item in self._items:
            w = item.widget()
            if w and not w.isVisible():
                continue
            sz    = item.sizeHint()
            next_x = x + sz.width()
            if next_x > r.right() and row_h > 0:
                x, y, row_h = r.x(), y + row_h + self._v_spacing, 0
                next_x = x + sz.width()
            if not dry_run:
                item.setGeometry(QRect(QPoint(x, y), sz))
            x      = next_x + self._h_spacing
            row_h  = max(row_h, sz.height())

        return y + row_h - rect.y() + m.bottom()


# ── Encoder Worker ────────────────────────────────────────────────────────────
class EncoderWorker(QThread):
    progress   = pyqtSignal(int)
    status     = pyqtSignal(str)
    log        = pyqtSignal(str, str)        # message, level
    active_idx = pyqtSignal(int)
    file_done  = pyqtSignal(str, str, str)   # path, display, quality_res
    all_done   = pyqtSignal(int, bool)       # count, was_cancelled

    def __init__(self, image_files, music_files, quality_key,
                 duration, output_dir, use_gpu, ffmpeg_bin,
                 hw_encoder=None, export_mp3=False):
        super().__init__()
        self.image_files = image_files
        self.music_files = music_files
        self.quality_key = quality_key
        self.duration    = duration
        self.output_dir  = output_dir
        self.use_gpu     = use_gpu
        self.hw_encoder  = hw_encoder
        self.export_mp3  = export_mp3
        self.ffmpeg      = ffmpeg_bin
        self._cancel     = False
        self._proc       = None

    def stop(self):
        self._cancel = True
        if self._proc:
            try:
                self._proc.terminate()
            except Exception:
                pass

    def run(self):
        if self.export_mp3:
            self._run_mp3_export()
        else:
            self._run_video_export()

    def _run_mp3_export(self):
        import subprocess
        music  = list(self.music_files)
        total  = len(music)
        out_base = Path(self.output_dir) if self.output_dir else Path.home() / "Downloads"
        out_base.mkdir(exist_ok=True)

        self.log.emit("─" * 44, "")
        self.log.emit(f"MP3 EXPORT  —  {total} track(s)", "warn")
        self.log.emit(f"Output : {out_base}", "")
        self.log.emit("─" * 44, "")

        count = 0
        for idx, src in enumerate(music):
            if self._cancel:
                break
            out_name = Path(src).stem + ".mp3"
            out_path = str(out_base / out_name)
            self.status.emit(f"MP3 {idx+1}/{total} — {Path(src).name}")
            self.log.emit(f"▶ {idx+1}/{total}  {Path(src).name}  →  {out_name}", "")

            cmd = [
                self.ffmpeg, "-y", "-i", src,
                "-vn",
                "-c:a", "libmp3lame", "-q:a", "0",  # VBR highest quality
                "-ar", "44100", "-ac", "2",
                out_path,
            ]
            try:
                self._proc = subprocess.Popen(
                    cmd, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL,
                    text=True, errors="replace",
                )
                stderr_lines = []
                for line in self._proc.stderr:
                    stderr_lines.append(line.rstrip())
                    if self._cancel:
                        self._proc.terminate()
                        break
                self._proc.wait()
                ok = self._proc.returncode == 0

                if ok and not self._cancel:
                    display = str(out_base.name) + "/" + out_name
                    self.file_done.emit(out_path, display, "MP3")
                    self.log.emit(f"✓ Saved: {display}", "ok")
                    count += 1
                elif not self._cancel:
                    errors = [l for l in stderr_lines if any(
                        k in l for k in ("Error", "error", "Invalid", "No such")
                    )]
                    for e in errors[-3:]:
                        self.log.emit(f"  ffmpeg: {e}", "err")
            except Exception as ex:
                self.log.emit(f"✗ Failed: {ex}", "err")

            self.progress.emit(int((idx + 1) / total * 100))

        self.all_done.emit(count, self._cancel)

    def _run_video_export(self):
        import subprocess

        images   = self.image_files
        music    = list(self.music_files)
        quality  = QUALITIES[self.quality_key]
        w, h     = quality["res"].split("x")
        dur      = self.duration
        total    = len(images)
        shuffled = sorted(music, key=lambda _: random.random())

        self.log.emit("─" * 44, "")
        self.log.emit(f"MP4 EXPORT  —  {total} image(s) → {total} video(s)", "warn")
        self.log.emit(f"Size     : {w} × {h}", "")
        self.log.emit(f"Duration : {dur}s / video", "")
        self.log.emit(f"Music    : {'random (' + str(len(music)) + ' track(s))' if music else 'none'}", "")
        self.log.emit(f"Output   : {self.output_dir or '~/Downloads'}", "")
        self.log.emit("─" * 44, "")

        count = 0
        for idx, img_path in enumerate(images):
            if self._cancel:
                break

            music_path = shuffled[idx % len(shuffled)] if shuffled else None
            self.active_idx.emit(idx)
            self.log.emit(
                f"▶ Video {idx+1}/{total}  img: {Path(img_path).name}"
                + (f"  🎵 {Path(music_path).name}" if music_path else "  (no audio)"),
                ""
            )

            out_name = Path(img_path).stem + ".mp4"
            # When no output dir chosen, save directly to ~/Downloads
            if self.output_dir:
                out_path = str(Path(self.output_dir) / out_name)
            else:
                downloads = Path.home() / "Downloads"
                downloads.mkdir(exist_ok=True)
                out_path  = str(downloads / out_name)

            ok = self._encode_one(img_path, music_path, out_path,
                                  w, h, dur, idx, total)
            if ok and not self._cancel:
                display = (
                    Path(self.output_dir).name + "/" + out_name
                    if self.output_dir
                    else "~/Downloads/" + out_name
                )
                self.file_done.emit(out_path, display, quality["res"])
                self.log.emit(f"✓ Saved: {display}", "ok")
                count += 1

        self.active_idx.emit(-1)
        self.all_done.emit(count, self._cancel)

    def _encode_one(self, img, audio, out, w, h, dur, idx, total):
        import subprocess

        vf = (f"scale={w}:{h}:force_original_aspect_ratio=increase,"
              f"crop={w}:{h}")

        def build_cmd(use_gpu):
            if use_gpu and self.hw_encoder:
                enc = self.hw_encoder
                if enc == "h264_videotoolbox":
                    vcodec = ["-c:v", enc, "-b:v", BITRATE]
                elif enc == "h264_nvenc":
                    vcodec = ["-c:v", enc, "-preset", "p4", "-b:v", BITRATE]
                else:
                    vcodec = ["-c:v", enc, "-b:v", BITRATE]
            else:
                vcodec = ["-c:v", "libx264", "-preset", "fast",
                          "-b:v", BITRATE, "-pix_fmt", "yuv420p"]

            cmd = [self.ffmpeg, "-y",
                   "-loop", "1", "-framerate", str(FPS), "-i", img]
            if audio:
                cmd += ["-stream_loop", "-1", "-i", audio]
            cmd += ["-vf", vf] + vcodec
            if audio:
                cmd += ["-c:a", "aac", "-b:a", "192k",
                        "-ac", "2", "-ar", "44100",
                        "-map", "0:v", "-map", "1:a"]
            cmd += ["-t", str(dur), out]
            return cmd

        def run_cmd(cmd):
            self._proc = subprocess.Popen(
                cmd,
                stderr=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                text=True, errors="replace",
            )
            total_frames = dur * FPS
            frame_re = re.compile(r"frame=\s*(\d+)")
            stderr_lines = []

            for line in self._proc.stderr:
                stderr_lines.append(line.rstrip())
                if self._cancel:
                    self._proc.terminate()
                    return False, stderr_lines
                m = frame_re.search(line)
                if m:
                    frame   = int(m.group(1))
                    overall = (idx / total + min(frame / total_frames, 1.0) / total) * 100
                    self.progress.emit(int(overall))
                    self.status.emit(
                        f"Video {idx+1}/{total} — frame {frame}/{total_frames}"
                    )

            self._proc.wait()
            return self._proc.returncode == 0, stderr_lines

        try:
            ok, stderr_lines = run_cmd(build_cmd(self.use_gpu))

            # Auto-fallback: if GPU failed, retry with libx264
            if not ok and self.use_gpu and self.hw_encoder and not self._cancel:
                self.log.emit(f"⚠  {self.hw_encoder} failed — retrying with libx264", "warn")
                ok, stderr_lines = run_cmd(build_cmd(False))

            if not ok and not self._cancel:
                # Show the last relevant FFmpeg error lines
                errors = [l for l in stderr_lines if "Error" in l or "error" in l
                          or "Invalid" in l or "No such" in l or "Unknown" in l]
                for line in (errors or stderr_lines[-4:]):
                    if line.strip():
                        self.log.emit(f"  ffmpeg: {line.strip()}", "err")

            return ok

        except Exception as e:
            self.log.emit(f"ERROR: {e}", "err")
            return False
        finally:
            self._proc = None


# ── Quality Button ────────────────────────────────────────────────────────────
class QualityButton(QPushButton):
    def __init__(self, name: str, resolution: str, parent=None):
        super().__init__(parent)
        self.setObjectName("qualityBtn")
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setCheckable(True)
        self.setFixedHeight(60)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(14, 10, 14, 10)
        lay.setSpacing(3)

        self._name_lbl = QLabel(name)
        self._name_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self._res_lbl  = QLabel(resolution)
        self._res_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        lay.addWidget(self._name_lbl)
        lay.addWidget(self._res_lbl)

        self.toggled.connect(self._refresh_style)
        self._refresh_style(False)

    def _refresh_style(self, _=None):
        checked = self.isChecked()
        self.setProperty("active", "true" if checked else "false")
        self.style().unpolish(self)
        self.style().polish(self)
        self._name_lbl.setStyleSheet(
            f"color: {'#f0a800' if checked else '#7070a0'};"
            " font-size: 13px; font-weight: 700; background: transparent;"
        )
        self._res_lbl.setStyleSheet(
            f"color: {'#c08000' if checked else '#38384a'};"
            " font-size: 11px; background: transparent;"
        )


# ── Thumbnail Item ────────────────────────────────────────────────────────────
class ThumbnailItem(QFrame):
    def __init__(self, path: str, index: int, parent=None):
        super().__init__(parent)
        self.index = index
        self.setFixedSize(96, 120)
        self._is_active = False
        self.setStyleSheet(self._style(False))

        lay = QVBoxLayout(self)
        lay.setContentsMargins(4, 4, 4, 4)
        lay.setSpacing(3)

        self.img_lbl = QLabel()
        self.img_lbl.setFixedSize(88, 94)
        self.img_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.img_lbl.setStyleSheet(
            "background:#0a0a16; border-radius:6px; border:none;"
        )

        name = Path(path).name
        short = name[:11] + "…" if len(name) > 12 else name
        name_lbl = QLabel(short)
        name_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_lbl.setStyleSheet(
            "color:#5a5a7a; font-size:9px; background:transparent; border:none;"
        )

        lay.addWidget(self.img_lbl)
        lay.addWidget(name_lbl)

        self._load_thumb(path)

    @staticmethod
    def _style(active: bool) -> str:
        if active:
            return (
                "QFrame { background: rgba(240,168,0,0.1);"
                " border: 1.5px solid rgba(240,168,0,0.7); border-radius:9px; }"
            )
        return "QFrame { background:#0d0e1c; border:1.5px solid #1a1b30; border-radius:9px; }"

    def _load_thumb(self, path: str):
        try:
            if HAS_PIL:
                with Image.open(path) as im:
                    im.thumbnail((88, 94))
                    im   = im.convert("RGBA")
                    data = im.tobytes("raw", "RGBA")
                    qimg = QImage(data, im.width, im.height,
                                  QImage.Format.Format_RGBA8888)
            else:
                qimg = QImage(path)
                qimg = qimg.scaled(
                    88, 94,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            self.img_lbl.setPixmap(QPixmap.fromImage(qimg))
        except Exception:
            self.img_lbl.setText("🖼")

    def set_active(self, active: bool):
        self._is_active = active
        self.setStyleSheet(self._style(active))

    def enterEvent(self, event):
        if not self._is_active:
            self.setStyleSheet(
                "QFrame { background:#13142a; border:1.5px solid rgba(240,168,0,0.3);"
                " border-radius:9px; }"
            )

    def leaveEvent(self, event):
        if not self._is_active:
            self.setStyleSheet(self._style(False))


# ── Main Window ───────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"VIDEO CREATOR  {VERSION}")
        self.setMinimumSize(1060, 700)
        self.resize(1260, 800)

        self._image_files  = []
        self._music_files  = []
        self._quality_key  = "Full HD"
        self._output_dir   = ""
        self._worker       = None
        self._thumb_items  = []
        self._output_rows  = 0
        self._ffmpeg        = find_ffmpeg()
        self._hw_encoders   = detect_hw_encoders(self._ffmpeg) if self._ffmpeg else []
        self._hw_encoder, self._hw_label = (
            self._hw_encoders[0] if self._hw_encoders else (None, None)
        )
        self._has_hw = bool(self._hw_encoders)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        root.addWidget(self._build_topbar())

        body_w = QWidget()
        body   = QHBoxLayout(body_w)
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)
        body.addWidget(self._build_left_panel(), 0)
        body.addWidget(self._build_right_panel(), 1)
        root.addWidget(body_w, 1)

        if not self._ffmpeg:
            self._log("⚠  ffmpeg not found — install: brew install ffmpeg", "err")
        else:
            hw_msg = f"HW encoder: {self._hw_label} ✓" if self._has_hw else "No HW encoder — using libx264"
            self._log(f"ffmpeg: {self._ffmpeg}  |  {hw_msg}", "ok" if self._has_hw else "warn")

        self.setAcceptDrops(True)

    # ── Drag & Drop ───────────────────────────────────────────────────────────
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        added = []
        for url in event.mimeData().urls():
            p = url.toLocalFile()
            if os.path.isdir(p):
                for root, _, fnames in os.walk(p):
                    for f in sorted(fnames):
                        if Path(f).suffix.lower() in IMG_EXTS:
                            added.append(os.path.join(root, f))
            elif Path(p).suffix.lower() in IMG_EXTS:
                added.append(p)
            elif Path(p).suffix.lower() in AUD_EXTS:
                self._music_files.append(p)
        if added:
            self._image_files += added
            self._update_source_status()
            self._rebuild_thumbnails()
            self._log(f"Dropped {len(added)} image(s). Total: {len(self._image_files)}", "")

    # ── Top Bar ───────────────────────────────────────────────────────────────
    def _build_topbar(self) -> QFrame:
        bar = QFrame()
        bar.setObjectName("topbar")
        bar.setFixedHeight(58)
        lay = QHBoxLayout(bar)
        lay.setContentsMargins(28, 0, 28, 0)
        lay.setSpacing(10)

        diamond = QLabel("◆")
        diamond.setStyleSheet(
            "color:#f0a800; font-size:18px; background:transparent;"
        )
        title = QLabel("VIDEO CREATOR")
        title.setObjectName("titleLabel")
        ver = QLabel(VERSION)
        ver.setObjectName("versionLabel")

        # Separator dot
        sep = QLabel("·")
        sep.setStyleSheet("color:#1a1b30; font-size:20px; background:transparent;")

        ffmpeg_tag = QLabel(f"FFmpeg {'✓' if self._ffmpeg else '✗'}")
        ffmpeg_tag.setStyleSheet(
            f"color: {'#4ec87a' if self._ffmpeg else '#e05555'};"
            " font-size:11px; font-weight:600; background:transparent;"
        )

        lay.addWidget(diamond)
        lay.addSpacing(2)
        lay.addWidget(title)
        lay.addSpacing(2)
        lay.addWidget(ver)
        lay.addStretch()
        lay.addWidget(sep)
        lay.addWidget(ffmpeg_tag)
        return bar

    # ── Left Panel ────────────────────────────────────────────────────────────
    def _build_left_panel(self) -> QScrollArea:
        inner = QWidget()
        inner.setObjectName("leftPanel")
        lay = QVBoxLayout(inner)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(12)

        lay.addWidget(self._card_export_mode())
        lay.addWidget(self._card_quality())
        lay.addWidget(self._card_duration())
        lay.addWidget(self._card_encoding())
        lay.addWidget(self._card_output_folder())
        lay.addWidget(self._card_sources())
        lay.addWidget(self._card_actions())
        lay.addStretch()

        scroll = QScrollArea()
        scroll.setObjectName("leftPanel")
        scroll.setWidget(inner)
        scroll.setWidgetResizable(True)
        scroll.setFixedWidth(430)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        return scroll

    # helpers
    def _make_card(self) -> tuple[QFrame, QVBoxLayout]:
        card = QFrame()
        card.setObjectName("card")
        lay  = QVBoxLayout(card)
        lay.setContentsMargins(16, 14, 16, 16)
        lay.setSpacing(12)
        return card, lay

    def _hdr_row(self, text: str, action: QPushButton = None) -> QHBoxLayout:
        row = QHBoxLayout()
        lbl = QLabel(text.upper())
        lbl.setObjectName("sectionLabel")
        row.addWidget(lbl)
        row.addStretch()
        if action:
            row.addWidget(action)
        return row

    # ── Cards ─────────────────────────────────────────────────────────────────
    def _card_export_mode(self) -> QFrame:
        card, lay = self._make_card()
        lay.addLayout(self._hdr_row("Export Mode"))

        self._mode_mp4 = QPushButton("🎬  MP4 Video")
        self._mode_mp3 = QPushButton("🎵  MP3 Audio")
        for btn in (self._mode_mp4, self._mode_mp3):
            btn.setObjectName("modeBtn")
            btn.setCheckable(True)
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self._mode_grp = QButtonGroup(self)
        self._mode_grp.addButton(self._mode_mp4)
        self._mode_grp.addButton(self._mode_mp3)
        self._mode_grp.setExclusive(True)
        self._mode_mp4.setChecked(True)
        self._mode_mp4.setProperty("active", "true")

        def _refresh_mode_btn(btn, checked):
            btn.setProperty("active", "true" if checked else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        self._mode_mp4.toggled.connect(lambda c: (
            _refresh_mode_btn(self._mode_mp4, c),
            self._on_export_mode_changed()
        ))
        self._mode_mp3.toggled.connect(lambda c: (
            _refresh_mode_btn(self._mode_mp3, c),
            self._on_export_mode_changed()
        ))

        row = QHBoxLayout()
        row.setSpacing(8)
        row.addWidget(self._mode_mp4)
        row.addWidget(self._mode_mp3)
        lay.addLayout(row)

        self._mode_desc = QLabel("One MP4 video per image, with optional music track")
        self._mode_desc.setStyleSheet(
            "color:#38384a; font-size:11px; background:transparent;"
        )
        self._mode_desc.setWordWrap(True)
        lay.addWidget(self._mode_desc)
        return card

    def _on_export_mode_changed(self):
        is_mp3 = self._mode_mp3.isChecked()
        if is_mp3:
            self._mode_desc.setText(
                "One MP3 audio file per music track — image files are not required"
            )
            self._btn_save.setText("🎵  EXPORT MP3")
            # Disable quality/encoding card (not relevant for audio)
            self._btn_hd.setEnabled(False)
            self._btn_4k.setEnabled(False)
            self._encoder_combo.setEnabled(False)
            self._gpu_toggle.setEnabled(False)
        else:
            self._mode_desc.setText(
                "One MP4 video per image, with optional music track"
            )
            self._btn_save.setText("💾  SAVE VIDEO")
            self._btn_hd.setEnabled(True)
            self._btn_4k.setEnabled(True)
            self._encoder_combo.setEnabled(self._has_hw)
            self._gpu_toggle.setEnabled(self._has_hw)

    def _card_quality(self) -> QFrame:
        card, lay = self._make_card()
        lay.addLayout(self._hdr_row("Output Quality"))

        self._btn_hd = QualityButton("Full HD",   "1080 × 1920")
        self._btn_4k = QualityButton("4K Ultra",  "2160 × 3840")
        self._btn_hd.setChecked(True)

        grp = QButtonGroup(self)
        grp.addButton(self._btn_hd)
        grp.addButton(self._btn_4k)
        grp.setExclusive(True)

        self._btn_hd.toggled.connect(lambda c: c and self._set_quality("Full HD"))
        self._btn_4k.toggled.connect(lambda c: c and self._set_quality("4K Ultra"))

        row = QHBoxLayout()
        row.setSpacing(8)
        row.addWidget(self._btn_hd)
        row.addWidget(self._btn_4k)
        lay.addLayout(row)
        return card

    def _card_duration(self) -> QFrame:
        card, lay = self._make_card()
        lay.addLayout(self._hdr_row("Duration"))

        row = QHBoxLayout()
        lbl = QLabel("Length")
        lbl.setStyleSheet("color:#9090a8; background:transparent;")

        self._duration_spin = QSpinBox()
        self._duration_spin.setRange(1, 3600)
        self._duration_spin.setValue(10)

        sec = QLabel("sec")
        sec.setStyleSheet("color:#48485a; background:transparent;")

        row.addWidget(lbl)
        row.addStretch()
        row.addWidget(self._duration_spin)
        row.addWidget(sec)
        lay.addLayout(row)
        return card

    def _card_encoding(self) -> QFrame:
        card, lay = self._make_card()
        lay.addLayout(self._hdr_row("Encoding"))

        # ── GPU toggle row ──
        toggle_row = QHBoxLayout()
        lbl = QLabel("Hardware GPU Encoding")
        lbl.setStyleSheet(
            f"color: {'#ddddf0' if self._has_hw else '#38384a'};"
            " background:transparent;"
        )
        self._gpu_toggle = ToggleSwitch(
            checked=self._has_hw, enabled=self._has_hw
        )
        toggle_row.addWidget(lbl)
        toggle_row.addStretch()
        toggle_row.addWidget(self._gpu_toggle)
        lay.addLayout(toggle_row)

        # ── Encoder selector row ──
        self._encoder_combo = QComboBox()
        self._encoder_combo.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        if self._hw_encoders:
            for enc_id, enc_label in self._hw_encoders:
                self._encoder_combo.addItem(enc_label, userData=enc_id)
            self._encoder_combo.addItem("Software  (libx264)", userData="libx264")
            self._encoder_combo.currentIndexChanged.connect(self._on_encoder_changed)
        else:
            self._encoder_combo.addItem("Software  (libx264)", userData="libx264")
            self._encoder_combo.setEnabled(False)
            self._gpu_toggle.setToolTip("No hardware H.264 encoder found")
            lbl.setToolTip("No hardware H.264 encoder found")

        # Keep toggle & combo in sync
        self._gpu_toggle.toggled.connect(self._on_gpu_toggled)

        combo_row = QHBoxLayout()
        enc_lbl = QLabel("Encoder")
        enc_lbl.setStyleSheet("color:#5a5a7a; font-size:11px; background:transparent;")
        combo_row.addWidget(enc_lbl)
        combo_row.addStretch()
        combo_row.addWidget(self._encoder_combo)
        lay.addLayout(combo_row)
        return card

    def _on_gpu_toggled(self, checked: bool):
        """When toggle flips, switch combo to first HW encoder or libx264."""
        if not self._hw_encoders:
            return
        if checked:
            self._encoder_combo.setCurrentIndex(0)
        else:
            # Select the libx264 entry (last item)
            self._encoder_combo.setCurrentIndex(self._encoder_combo.count() - 1)

    def _on_encoder_changed(self, idx: int):
        """Keep toggle in sync when combo changes."""
        enc_id = self._encoder_combo.itemData(idx)
        if enc_id and enc_id != "libx264":
            if not self._gpu_toggle.isChecked():
                self._gpu_toggle.setChecked(True)
        else:
            if self._gpu_toggle.isChecked():
                self._gpu_toggle.setChecked(False)

    def _selected_encoder(self) -> str | None:
        """Return selected hw encoder id, or None if software."""
        if not self._gpu_toggle.isChecked():
            return None
        enc_id = self._encoder_combo.currentData()
        return enc_id if enc_id and enc_id != "libx264" else None

    def _card_output_folder(self) -> QFrame:
        card, lay = self._make_card()

        self._folder_clear_btn = QPushButton("✕ Reset")
        self._folder_clear_btn.setObjectName("labelActionBtn")
        self._folder_clear_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._folder_clear_btn.clicked.connect(self._clear_output_folder)
        self._folder_clear_btn.setVisible(False)

        lay.addLayout(self._hdr_row("Output Folder", self._folder_clear_btn))

        row = QHBoxLayout()
        icon = QLabel("📁")
        icon.setStyleSheet("background:transparent; font-size:14px;")

        self._folder_path_lbl = QLabel("~/Downloads (default)")
        self._folder_path_lbl.setObjectName("pathLabel")
        self._folder_path_lbl.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )

        browse = QPushButton("Browse")
        browse.setObjectName("browseBtn")
        browse.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        browse.clicked.connect(self._browse_output_folder)

        row.addWidget(icon)
        row.addWidget(self._folder_path_lbl)
        row.addWidget(browse)
        lay.addLayout(row)
        return card

    def _card_sources(self) -> QFrame:
        card, lay = self._make_card()
        lay.addLayout(self._hdr_row("Source Files"))

        def make_status_row(label):
            row  = QHBoxLayout()
            dot  = QLabel("●")
            dot.setObjectName("dotLabel")
            dot.setFixedWidth(14)
            lbl  = QLabel(label)
            lbl.setStyleSheet("color:#9090a8; font-size:12px; background:transparent;")
            cnt  = QLabel("0 files")
            cnt.setObjectName("srcCount")
            row.addWidget(dot)
            row.addWidget(lbl)
            row.addStretch()
            row.addWidget(cnt)
            return row, dot, cnt

        img_row, self._img_dot, self._img_count_lbl = make_status_row("Images")
        mus_row, self._mus_dot, self._mus_count_lbl = make_status_row("Music")
        lay.addLayout(img_row)
        lay.addLayout(mus_row)

        btns = QHBoxLayout()
        btns.setSpacing(6)
        for text, slot in [
            ("📂 Folder", self._pick_image_folder),
            ("🖼 Images",  self._pick_images),
            ("🎵 Music",   self._pick_music),
            ("↻ Refresh",  self._refresh_files),
        ]:
            b = QPushButton(text)
            b.setObjectName("sourceBtn")
            b.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            b.clicked.connect(slot)
            btns.addWidget(b)
        lay.addLayout(btns)
        return card

    def _card_actions(self) -> QFrame:
        card = QFrame()
        card.setObjectName("card")
        lay  = QVBoxLayout(card)
        lay.setContentsMargins(16, 14, 16, 14)
        lay.setSpacing(12)

        # Header
        hdr = QHBoxLayout()
        lbl = QLabel("ACTIONS")
        lbl.setObjectName("sectionLabel")
        hdr.addWidget(lbl)
        hdr.addStretch()
        lay.addLayout(hdr)

        # Buttons
        btns = QHBoxLayout()
        btns.setSpacing(8)

        self._btn_stop = QPushButton("⏸️  STOP")
        self._btn_stop.setObjectName("btnStop")
        self._btn_stop.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._btn_stop.setEnabled(False)
        self._btn_stop.setMinimumHeight(48)
        self._btn_stop.clicked.connect(self._stop_encoding)

        self._btn_save = QPushButton("▶️  START")
        self._btn_save.setObjectName("btnSave")
        self._btn_save.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self._btn_save.setMinimumHeight(48)
        self._btn_save.clicked.connect(self._start_encoding)

        btns.addWidget(self._btn_stop, 1)
        btns.addWidget(self._btn_save, 2)
        lay.addLayout(btns)
        return card

    # ── Right Panel ───────────────────────────────────────────────────────────
    def _build_right_panel(self) -> QWidget:
        panel = QWidget()
        lay   = QVBoxLayout(panel)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(14)

        lay.addWidget(self._wrap_card("Images",       self._build_thumb_section(),    thumb_count=True), 2)
        lay.addWidget(self._wrap_card("Progress",     self._build_progress_section()))
        lay.addWidget(self._wrap_card("Output Files", self._build_output_table(),     has_clear=True), 2)
        lay.addWidget(self._wrap_card("Console",      self._build_console()), 2)
        return panel

    def _wrap_card(self, title: str, body: QWidget,
                   thumb_count=False, has_clear=False) -> QFrame:
        card = QFrame()
        card.setObjectName("card")
        lay  = QVBoxLayout(card)
        lay.setContentsMargins(16, 14, 16, 14)
        lay.setSpacing(10)

        hdr = QHBoxLayout()
        lbl = QLabel(title.upper())
        lbl.setObjectName("sectionLabel")
        hdr.addWidget(lbl)
        hdr.addStretch()

        if thumb_count:
            self._thumb_count_lbl = QLabel("(0)")
            self._thumb_count_lbl.setObjectName("thumbCount")
            hdr.addWidget(self._thumb_count_lbl)

        if has_clear:
            cb = QPushButton("✕ Clear")
            cb.setObjectName("labelActionBtn")
            cb.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            cb.clicked.connect(self._clear_output_table)
            hdr.addWidget(cb)

        lay.addLayout(hdr)
        lay.addWidget(body, 1)
        return card

    def _build_thumb_section(self) -> QScrollArea:
        self._thumb_scroll = QScrollArea()
        self._thumb_scroll.setWidgetResizable(True)
        self._thumb_scroll.setMinimumHeight(130)
        self._rebuild_thumbnails()
        return self._thumb_scroll

    def _build_progress_section(self) -> QWidget:
        w = QWidget()
        w.setStyleSheet("background:transparent;")
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(6)

        self._status_lbl = QLabel("Idle — ready to render")
        self._status_lbl.setObjectName("statusLabel")

        bar_row = QHBoxLayout()
        self._progress_bar = QProgressBar()
        self._progress_bar.setRange(0, 100)
        self._progress_bar.setValue(0)
        self._progress_bar.setTextVisible(False)
        self._progress_bar.setFixedHeight(6)

        self._pct_lbl = QLabel("0%")
        self._pct_lbl.setObjectName("pctLabel")
        self._pct_lbl.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        bar_row.addWidget(self._progress_bar, 1)
        bar_row.addWidget(self._pct_lbl)

        lay.addWidget(self._status_lbl)
        lay.addLayout(bar_row)
        return w

    def _build_output_table(self) -> QTableWidget:
        tbl = QTableWidget(0, 5)
        tbl.setHorizontalHeaderLabels(["#", "Path", "Quality", "Time", ""])
        tbl.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        tbl.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        tbl.setColumnWidth(0, 36)
        tbl.setColumnWidth(2, 100)
        tbl.setColumnWidth(3, 72)
        tbl.setColumnWidth(4, 60)
        tbl.verticalHeader().setVisible(False)
        tbl.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        tbl.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        tbl.setShowGrid(False)
        self._output_table = tbl
        return tbl

    def _build_console(self) -> QTextEdit:
        log = QTextEdit()
        log.setObjectName("console")
        log.setReadOnly(True)
        log.setMinimumHeight(80)
        self._console = log
        return log

    # ── Slots: quality / folder / sources ─────────────────────────────────────
    def _set_quality(self, key: str):
        self._quality_key = key
        self._log(f"Quality set to {QUALITIES[key]['res']}", "warn")

    def _browse_output_folder(self):
        start = self._output_dir or str(Path.home())
        dlg   = QFileDialog(self, "Select Output Folder", start)
        dlg.setFileMode(QFileDialog.FileMode.Directory)
        dlg.setOption(QFileDialog.Option.ShowDirsOnly, True)
        dlg.setOption(QFileDialog.Option.DontUseNativeDialog, True)

        if dlg.exec():
            selected = dlg.selectedFiles()
            if selected:
                path = selected[0]
                self._output_dir = path
                # Show truncated path in label (max 40 chars from the right)
                display = path if len(path) <= 40 else "…" + path[-38:]
                self._folder_path_lbl.setText(display)
                self._folder_path_lbl.setToolTip(path)
                self._folder_path_lbl.setProperty("set", "true")
                self._folder_path_lbl.style().unpolish(self._folder_path_lbl)
                self._folder_path_lbl.style().polish(self._folder_path_lbl)
                self._folder_clear_btn.setVisible(True)
                self._log(f"Output folder: {path}", "ok")

    def _clear_output_folder(self):
        self._output_dir = ""
        self._folder_path_lbl.setText("~/Downloads (default)")
        self._folder_path_lbl.setProperty("set", "false")
        self._folder_path_lbl.style().unpolish(self._folder_path_lbl)
        self._folder_path_lbl.style().polish(self._folder_path_lbl)
        self._folder_clear_btn.setVisible(False)

    def _pick_images(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Images", "",
            "Images (*.jpg *.jpeg *.png *.webp *.bmp *.tiff *.heic *.avif)"
        )
        if files:
            self._image_files += files
            self._update_source_status()
            self._rebuild_thumbnails()
            self._log(f"Added {len(files)} image(s). Total: {len(self._image_files)}", "")

    def _pick_image_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Select Image Folder")
        if path:
            found = []
            for root, _, fnames in os.walk(path):
                for f in sorted(fnames):
                    if Path(f).suffix.lower() in IMG_EXTS:
                        found.append(os.path.join(root, f))
            if found:
                self._image_files += found
                self._update_source_status()
                self._rebuild_thumbnails()
                self._log(
                    f"Loaded {len(found)} image(s) from folder. "
                    f"Total: {len(self._image_files)}", "ok"
                )
            else:
                self._log("No images found in that folder.", "warn")

    def _pick_music(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Music", "",
            "Audio (*.mp3 *.wav *.aac *.m4a *.flac *.ogg *.opus)"
        )
        if files:
            self._music_files += files
            self._update_source_status()
            self._log(
                f"Added {len(files)} music track(s). Total: {len(self._music_files)}", ""
            )

    def _refresh_files(self):
        self._image_files.clear()
        self._music_files.clear()
        self._update_source_status()
        self._rebuild_thumbnails()
        self._log("File list cleared.", "warn")

    def _update_source_status(self):
        n_img = len(self._image_files)
        n_mus = len(self._music_files)
        self._img_count_lbl.setText(f"{n_img} file{'s' if n_img != 1 else ''}")
        self._mus_count_lbl.setText(f"{n_mus} file{'s' if n_mus != 1 else ''}")
        self._thumb_count_lbl.setText(f"({n_img})")

        for dot, active in [
            (self._img_dot, n_img > 0),
            (self._mus_dot, n_mus > 0),
        ]:
            dot.setProperty("active", "true" if active else "false")
            dot.style().unpolish(dot)
            dot.style().polish(dot)

    def _rebuild_thumbnails(self):
        old = self._thumb_scroll.takeWidget()
        if old:
            old.deleteLater()
        self._thumb_items.clear()

        container = QWidget()
        container.setStyleSheet("background:transparent;")
        flow = FlowLayout(container, h_spacing=8, v_spacing=8)

        if not self._image_files:
            lbl = QLabel("Drop images here\nor use the buttons below")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet(
                "color:#38384a; font-size:13px; line-height:1.6;"
                " border: 1.5px dashed #1a1b30; border-radius:10px;"
                " padding:24px; margin:8px;"
            )
            flow.addWidget(lbl)
        else:
            for i, path in enumerate(self._image_files):
                item = ThumbnailItem(path, i)
                flow.addWidget(item)
                self._thumb_items.append(item)

        self._thumb_scroll.setWidget(container)

    def _set_active_thumbnail(self, idx: int):
        for i, item in enumerate(self._thumb_items):
            item.set_active(i == idx)

    # ── Encoding ──────────────────────────────────────────────────────────────
    def _start_encoding(self):
        is_mp3_mode = self._mode_mp3.isChecked()

        if is_mp3_mode:
            if not self._music_files:
                self._log("⚠  No music files loaded for MP3 export.", "err")
                return
        else:
            if not self._image_files:
                self._log("⚠  No images loaded.", "err")
                return

        if not self._ffmpeg:
            self._log("⚠  ffmpeg not found. Install: brew install ffmpeg", "err")
            return

        self._btn_save.setEnabled(False)
        self._btn_save.setText("⏳  Exporting…")
        self._btn_stop.setEnabled(True)
        self._progress_bar.setValue(0)
        self._pct_lbl.setText("0%")

        self._worker = EncoderWorker(
            image_files = self._image_files,
            music_files = self._music_files,
            quality_key = self._quality_key,
            duration    = self._duration_spin.value(),
            output_dir  = self._output_dir,
            use_gpu     = self._gpu_toggle.isChecked(),
            ffmpeg_bin  = self._ffmpeg,
            hw_encoder  = self._selected_encoder(),
            export_mp3  = is_mp3_mode,
        )
        self._worker.progress.connect(self._on_progress)
        self._worker.status.connect(self._on_status)
        self._worker.log.connect(self._log)
        self._worker.active_idx.connect(self._set_active_thumbnail)
        self._worker.file_done.connect(self._on_file_done)
        self._worker.all_done.connect(self._on_all_done)
        self._worker.start()

    def _stop_encoding(self):
        if self._worker:
            self._worker.stop()
        self._btn_stop.setEnabled(False)

    def _on_progress(self, pct: int):
        self._progress_bar.setValue(pct)
        self._pct_lbl.setText(f"{pct}%")

    def _on_status(self, msg: str):
        self._status_lbl.setText(msg)

    def _on_file_done(self, path: str, display: str, quality: str):
        self._output_rows += 1
        row = self._output_table.rowCount()
        self._output_table.insertRow(row)
        self._output_table.setRowHeight(row, 34)

        items = [
            QTableWidgetItem(str(self._output_rows)),
            QTableWidgetItem(display),
            QTableWidgetItem(quality),
            QTableWidgetItem(datetime.now().strftime("%H:%M:%S")),
        ]
        for i, it in enumerate(items):
            it.setForeground(QColor(
                "#ddddf0" if i < 2 else "#7070a0"
            ))
            self._output_table.setItem(row, i, it)
        items[0].setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        open_btn = QPushButton("Open")
        open_btn.setObjectName("tblBtn")
        open_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        open_btn.clicked.connect(lambda _, p=path: self._open_file(p))
        self._output_table.setCellWidget(row, 4, open_btn)
        self._output_table.scrollToBottom()

    def _on_all_done(self, count: int, cancelled: bool):
        is_mp3 = self._mode_mp3.isChecked()
        self._btn_stop.setEnabled(False)
        self._btn_save.setEnabled(True)
        self._btn_save.setText("🎵  EXPORT MP3" if is_mp3 else "💾  SAVE VIDEO")
        self._set_active_thumbnail(-1)

        fmt = "MP3" if is_mp3 else "MP4"
        if cancelled:
            self._log("Export cancelled.", "err")
            self._on_status("Cancelled")
            self._on_progress(0)
        else:
            self._on_progress(100)
            self._on_status(f"All {count} {fmt} file(s) saved ✓")
            self._log(f"Done — {count} {fmt} file(s) saved.", "ok")

    def _clear_output_table(self):
        self._output_table.setRowCount(0)
        self._output_rows = 0

    def _open_file(self, path: str):
        import subprocess as sp
        sys_name = platform.system()
        try:
            if sys_name == "Darwin":
                sp.run(["open", "-R", path])
            elif sys_name == "Windows":
                os.startfile(path)
            else:
                sp.run(["xdg-open", str(Path(path).parent)])
        except Exception as e:
            self._log(f"Could not open file: {e}", "warn")

    # ── Console ───────────────────────────────────────────────────────────────
    def _log(self, msg: str, level: str = ""):
        COLORS = {"ok": "#4ec87a", "warn": "#e8a200", "err": "#e05555", "": "#9090a8"}
        color  = COLORS.get(level, "#9090a8")
        ts     = datetime.now().strftime("%H:%M:%S")
        html   = (
            f'<span style="color:#48485a">[{ts}]</span> '
            f'<span style="color:{color}">{msg}</span>'
        )
        self._console.append(html)
        sb = self._console.verticalScrollBar()
        sb.setValue(sb.maximum())


# ── Entry Point ───────────────────────────────────────────────────────────────
def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Video Creator")
    app.setStyleSheet(APP_QSS)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
