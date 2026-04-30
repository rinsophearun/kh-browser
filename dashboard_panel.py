"""Real-Time Dashboard — Premium Orange/Amber redesign with smooth animations."""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QScrollArea, QGridLayout, QProgressBar, QListWidget,
    QListWidgetItem, QSizePolicy, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QFont, QColor, QPainter, QLinearGradient, QBrush, QPen
import datetime
from assets import get_asset_path

# ── Palette ────────────────────────────────────────────────────────────────────
BG_DEEP   = "#080c12"
BG_CARD   = "#0e1420"
BG_CARD2  = "#111827"
BORDER    = "#1a2236"
ORANGE    = "#f97316"
ORANGE2   = "#fb923c"
ORANGE_DIM= "#7c2d12"
AMBER     = "#f59e0b"
AMBER_DIM = "#78350f"
GREEN     = "#22c55e"
GREEN_DIM = "#14532d"
BLUE      = "#38bdf8"
BLUE_DIM  = "#0c4a6e"
PURPLE    = "#a78bfa"
PURPLE_DIM= "#3b1d8a"
RED       = "#f87171"
RED_DIM   = "#450a0a"
TEXT_HI   = "#f1f5f9"
TEXT_MID  = "#94a3b8"
TEXT_LOW  = "#334155"


def _shadow(widget, blur=20, color="#f9731630"):
    eff = QGraphicsDropShadowEffect()
    eff.setBlurRadius(blur)
    eff.setOffset(0, 4)
    eff.setColor(QColor(color))
    widget.setGraphicsEffect(eff)


# ── Animated Number Label ──────────────────────────────────────────────────────
class AnimatedStat(QLabel):
    def __init__(self, parent=None):
        super().__init__("0", parent)
        self._target = 0
        self._current = 0.0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._step)

    def set_value(self, v: int):
        if v == self._target:
            return
        self._target = v
        self._timer.start(16)   # ~60 fps

    def _step(self):
        diff = self._target - self._current
        if abs(diff) < 0.5:
            self._current = self._target
            self._timer.stop()
        else:
            self._current += diff * 0.18
        self.setText(str(int(round(self._current))))


# ── Stat Card ──────────────────────────────────────────────────────────────────
class StatCard(QFrame):
    def __init__(self, icon, label, value=0, accent=ORANGE,
                 bg_dim=ORANGE_DIM, parent=None):
        super().__init__(parent)
        self.setFixedHeight(120)
        self.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                    stop:0 {BG_CARD}, stop:1 #0a0f1a);
                border: 1px solid {BORDER};
                border-radius: 16px;
            }}
            QFrame:hover {{
                border: 1px solid {accent};
            }}
        """)

        lay = QHBoxLayout(self)
        lay.setContentsMargins(20, 0, 20, 0)
        lay.setSpacing(0)

        # Left: icon bubble
        bubble = QFrame()
        bubble.setFixedSize(52, 52)
        bubble.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                    stop:0 {bg_dim}, stop:1 #0e1420);
                border-radius: 14px;
                border: 1px solid {accent}40;
            }}
        """)
        bl = QHBoxLayout(bubble)
        bl.setContentsMargins(0, 0, 0, 0)
        icon_lb = QLabel(icon)
        icon_lb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lb.setStyleSheet("font-size:22px; background:transparent; border:none;")
        bl.addWidget(icon_lb)

        # Right: value + label
        right = QVBoxLayout()
        right.setSpacing(2)
        right.setContentsMargins(16, 0, 0, 0)

        self._val = AnimatedStat()
        self._val.setStyleSheet(f"""
            color: {accent};
            font-size: 30px;
            font-weight: 800;
            background: transparent;
            border: none;
            letter-spacing: -1px;
        """)
        self._val.set_value(value)

        lbl = QLabel(label)
        lbl.setStyleSheet(f"""
            color: {TEXT_MID};
            font-size: 12px;
            font-weight: 500;
            background: transparent;
            border: none;
        """)

        right.addStretch()
        right.addWidget(self._val)
        right.addWidget(lbl)
        right.addStretch()

        # Accent bar (right edge)
        bar = QFrame()
        bar.setFixedWidth(3)
        bar.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                    stop:0 transparent, stop:0.3 {accent}, stop:0.7 {accent}, stop:1 transparent);
                border-radius: 2px;
                border: none;
            }}
        """)

        lay.addWidget(bubble)
        lay.addLayout(right, 1)
        lay.addWidget(bar)

    def set_value(self, v: int):
        self._val.set_value(v)


# ── Donut-style Percentage Ring (QPainter) ─────────────────────────────────────
class RingWidget(QWidget):
    def __init__(self, accent=ORANGE, parent=None):
        super().__init__(parent)
        self._pct  = 0
        self._accent = QColor(accent)
        self.setFixedSize(80, 80)

    def set_percent(self, p: float):
        self._pct = max(0.0, min(100.0, p))
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect().adjusted(6, 6, -6, -6)
        # Track
        pen = QPen(QColor(BORDER), 8, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        p.setPen(pen)
        p.drawArc(rect, 0, 360 * 16)
        # Fill
        pen2 = QPen(self._accent, 8, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        p.setPen(pen2)
        span = int(self._pct / 100 * 360 * 16)
        p.drawArc(rect, 90 * 16, -span)
        # Center text
        p.setPen(QPen(QColor(TEXT_HI)))
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        p.setFont(font)
        p.drawText(rect, Qt.AlignmentFlag.AlignCenter, f"{int(self._pct)}%")
        p.end()


# ── Bar Chart Row ──────────────────────────────────────────────────────────────
class BarRow(QWidget):
    COLORS = [ORANGE, AMBER, GREEN, BLUE, PURPLE, RED, "#06b6d4", "#ec4899"]

    def __init__(self, label, count, total, color_idx=0, parent=None):
        super().__init__(parent)
        color = self.COLORS[color_idx % len(self.COLORS)]
        pct = int(count / max(total, 1) * 100)

        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        lbl = QLabel(label)
        lbl.setFixedWidth(100)
        lbl.setStyleSheet(f"color:{TEXT_MID};font-size:12px;background:transparent;border:none;")

        bar_bg = QFrame()
        bar_bg.setFixedHeight(8)
        bar_bg.setStyleSheet(f"""
            QFrame {{
                background:{BG_CARD2};
                border-radius:4px;
                border:none;
            }}
        """)
        bar_fill = QFrame(bar_bg)
        bar_fill.setFixedHeight(8)
        bar_fill.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 {color}, stop:1 {color}80);
                border-radius:4px;
                border:none;
            }}
        """)
        # We'll resize fill in show/resize
        self._bar_bg   = bar_bg
        self._bar_fill = bar_fill
        self._pct      = pct

        cnt = QLabel(str(count))
        cnt.setFixedWidth(28)
        cnt.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        cnt.setStyleSheet(f"color:{color};font-size:12px;font-weight:700;background:transparent;border:none;")

        lay.addWidget(lbl)
        lay.addWidget(bar_bg, 1)
        lay.addWidget(cnt)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self._update_fill()

    def showEvent(self, e):
        super().showEvent(e)
        self._update_fill()

    def _update_fill(self):
        w = int(self._bar_bg.width() * self._pct / 100)
        self._bar_fill.setFixedWidth(max(w, 0))
        self._bar_fill.setFixedHeight(8)


# ── Chart Card ────────────────────────────────────────────────────────────────
class ChartCard(QFrame):
    def __init__(self, title, icon="📊", parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background: {BG_CARD};
                border: 1px solid {BORDER};
                border-radius: 16px;
            }}
        """)
        self._lay = QVBoxLayout(self)
        self._lay.setContentsMargins(20, 18, 20, 18)
        self._lay.setSpacing(14)

        # Header
        hdr = QHBoxLayout()
        dot = QLabel("●")
        dot.setStyleSheet(f"color:{ORANGE};font-size:8px;background:transparent;border:none;")
        t = QLabel(f"  {icon}  {title}")
        t.setStyleSheet(f"color:{TEXT_HI};font-size:13px;font-weight:700;background:transparent;border:none;")
        hdr.addWidget(dot)
        hdr.addWidget(t)
        hdr.addStretch()
        self._lay.addLayout(hdr)

        # Divider
        div = QFrame()
        div.setFixedHeight(1)
        div.setStyleSheet(f"background:{BORDER};border:none;")
        self._lay.addWidget(div)

        self._rows_container = QVBoxLayout()
        self._rows_container.setSpacing(10)
        self._lay.addLayout(self._rows_container)
        self._lay.addStretch()

    def update_data(self, data: dict):
        while self._rows_container.count():
            item = self._rows_container.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        total = max(sum(data.values()), 1)
        for i, (label, count) in enumerate(sorted(data.items(), key=lambda x: -x[1])):
            row = BarRow(label, count, total, i)
            self._rows_container.addWidget(row)


# ── Running Profile Row ────────────────────────────────────────────────────────
class RunningRow(QFrame):
    def __init__(self, profile, parent=None):
        super().__init__(parent)
        self.setFixedHeight(44)
        self.setStyleSheet(f"""
            QFrame {{
                background:{BG_CARD2};
                border-radius:10px;
                border:1px solid {BORDER};
            }}
            QFrame:hover {{
                border:1px solid {ORANGE}60;
                background:#111827;
            }}
        """)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(12, 0, 12, 0)
        lay.setSpacing(10)

        pulse = QLabel("●")
        pulse.setStyleSheet(f"color:{GREEN};font-size:10px;background:transparent;border:none;")

        name = QLabel(profile.name)
        name.setStyleSheet(f"color:{TEXT_HI};font-size:13px;font-weight:600;background:transparent;border:none;")

        grp = QLabel(profile.group)
        grp.setStyleSheet(f"color:{TEXT_LOW};font-size:11px;background:transparent;border:none;")

        brow = QLabel(profile.browser_type)
        brow.setStyleSheet(f"""
            color:{ORANGE};font-size:11px;font-weight:600;
            background:{ORANGE_DIM}60;border-radius:4px;
            padding:2px 6px;border:none;
        """)

        lay.addWidget(pulse)
        lay.addWidget(name, 1)
        lay.addWidget(grp)
        lay.addWidget(brow)


# ── Activity Feed Item ─────────────────────────────────────────────────────────
class ActivityItem(QListWidgetItem):
    def __init__(self, icon, text, ts, color):
        super().__init__()
        self.setText(f" {icon}  {text}")
        self.setToolTip(ts)
        self.setForeground(QColor(color))


# ── Activity Card ──────────────────────────────────────────────────────────────
class ActivityCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background:{BG_CARD};
                border:1px solid {BORDER};
                border-radius:16px;
            }}
        """)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 18, 20, 18)
        lay.setSpacing(12)

        # Header with live dot
        hdr = QHBoxLayout()
        self._dot = QLabel("●")
        self._dot.setStyleSheet(f"color:{GREEN};font-size:10px;background:transparent;border:none;")
        title = QLabel("  ⚡  Live Activity")
        title.setStyleSheet(f"color:{TEXT_HI};font-size:13px;font-weight:700;background:transparent;border:none;")
        self._ts = QLabel()
        self._ts.setStyleSheet(f"color:{TEXT_LOW};font-size:11px;background:transparent;border:none;")
        hdr.addWidget(self._dot)
        hdr.addWidget(title)
        hdr.addStretch()
        hdr.addWidget(self._ts)
        lay.addLayout(hdr)

        div = QFrame()
        div.setFixedHeight(1)
        div.setStyleSheet(f"background:{BORDER};border:none;")
        lay.addWidget(div)

        self.feed = QListWidget()
        self.feed.setStyleSheet(f"""
            QListWidget {{
                background:transparent;
                border:none;
                font-size:12px;
                color:{TEXT_MID};
                outline:none;
            }}
            QListWidget::item {{
                padding:7px 4px;
                border-bottom:1px solid {BORDER};
                border-radius:0px;
            }}
            QListWidget::item:hover {{
                background:{BG_CARD2};
                border-radius:8px;
            }}
        """)
        lay.addWidget(self.feed, 1)

        # Blink timer
        self._blink = True
        bt = QTimer(self)
        bt.timeout.connect(self._blink_tick)
        bt.start(700)

    def _blink_tick(self):
        self._blink = not self._blink
        self._dot.setStyleSheet(
            f"color:{'#22c55e' if self._blink else '#14532d'};font-size:10px;"
            f"background:transparent;border:none;"
        )
        self._ts.setText(datetime.datetime.now().strftime("%H:%M:%S"))

    def add(self, icon, text, color=TEXT_MID):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        item = ActivityItem(icon, text, ts, color)
        self.feed.insertItem(0, item)
        if self.feed.count() > 60:
            self.feed.takeItem(self.feed.count() - 1)


# ── Running Profiles Card ──────────────────────────────────────────────────────
class RunningCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background:{BG_CARD};
                border:1px solid {BORDER};
                border-radius:16px;
            }}
        """)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 18, 20, 18)
        lay.setSpacing(12)

        hdr = QHBoxLayout()
        dot = QLabel("●")
        dot.setStyleSheet(f"color:{GREEN};font-size:8px;background:transparent;border:none;")
        title = QLabel("  🟢  Running Profiles")
        title.setStyleSheet(f"color:{TEXT_HI};font-size:13px;font-weight:700;background:transparent;border:none;")
        self._count = QLabel("0")
        self._count.setStyleSheet(f"""
            color:{GREEN};font-size:11px;font-weight:700;
            background:{GREEN_DIM}80;border-radius:8px;
            padding:2px 8px;border:none;
        """)
        hdr.addWidget(dot)
        hdr.addWidget(title)
        hdr.addStretch()
        hdr.addWidget(self._count)
        lay.addLayout(hdr)

        div = QFrame()
        div.setFixedHeight(1)
        div.setStyleSheet(f"background:{BORDER};border:none;")
        lay.addWidget(div)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea{background:transparent;border:none;}")
        scroll.setMaximumHeight(220)

        self._inner = QWidget()
        self._inner.setStyleSheet("background:transparent;")
        self._vlay = QVBoxLayout(self._inner)
        self._vlay.setContentsMargins(0, 0, 0, 0)
        self._vlay.setSpacing(6)
        scroll.setWidget(self._inner)
        lay.addWidget(scroll)

    def update(self, profiles):
        while self._vlay.count():
            item = self._vlay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        running = [p for p in profiles if p.status == "running"]
        self._count.setText(str(len(running)))

        if not running:
            empty = QLabel("  No profiles running right now")
            empty.setStyleSheet(f"color:{TEXT_LOW};font-size:12px;padding:12px 0;background:transparent;border:none;")
            self._vlay.addWidget(empty)
        else:
            for p in running:
                self._vlay.addWidget(RunningRow(p))
        self._vlay.addStretch()


# ── Uptime / Quick-Info Strip ──────────────────────────────────────────────────
class QuickInfoStrip(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(54)
        self.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 {ORANGE_DIM}80, stop:0.5 #0e1420, stop:1 {AMBER_DIM}80);
                border: 1px solid {ORANGE}30;
                border-radius: 12px;
            }}
        """)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(20, 0, 20, 0)
        lay.setSpacing(0)

        self._items = {}
        for key, icon, default in [
            ("time",    "🕐", "00:00:00"),
            ("uptime",  "⏱️", "Uptime: 0s"),
            ("date",    "📅", ""),
            ("version", "🛡️", "v2.0.2.6"),
        ]:
            lbl = QLabel(f" {icon} {default} ")
            lbl.setStyleSheet(f"color:{TEXT_MID};font-size:12px;background:transparent;border:none;")
            lay.addWidget(lbl)
            if key != "version":
                sep = QLabel("  |  ")
                sep.setStyleSheet(f"color:{TEXT_LOW};background:transparent;border:none;")
                lay.addWidget(sep)
            self._items[key] = lbl
        lay.addStretch()

        self._start = datetime.datetime.now()
        t = QTimer(self)
        t.timeout.connect(self._tick)
        t.start(1000)
        self._tick()

    def _tick(self):
        now = datetime.datetime.now()
        delta = now - self._start
        secs = int(delta.total_seconds())
        h, r = divmod(secs, 3600)
        m, s = divmod(r, 60)
        self._items["time"].setText(f" 🕐 {now.strftime('%H:%M:%S')} ")
        self._items["uptime"].setText(f" ⏱️ Uptime: {h:02d}:{m:02d}:{s:02d} ")
        self._items["date"].setText(f" 📅 {now.strftime('%a %d %b %Y')} ")


# ── Dashboard Panel ────────────────────────────────────────────────────────────
class DashboardPanel(QWidget):
    def __init__(self, profile_panel, parent=None):
        super().__init__(parent)
        self.pp = profile_panel
        self._build()
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.refresh)
        self._timer.start(3000)
        self.refresh()

    def _build(self):
        self.setStyleSheet(f"background:{BG_DEEP};")
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Top header bar ────────────────────────────────────────────────────
        hdr = QWidget()
        hdr.setFixedHeight(64)
        hdr.setStyleSheet(f"""
            background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                stop:0 {BG_DEEP}, stop:0.5 #0d1422, stop:1 {BG_DEEP});
            border-bottom: 1px solid {BORDER};
        """)
        hl = QHBoxLayout(hdr)
        hl.setContentsMargins(28, 0, 28, 0)

        logo = QLabel("📊")
        logo_img = QLabel()
        from PyQt6.QtGui import QPixmap
        logo_path = get_asset_path("Logo.png")
        logo_pixmap = QPixmap(logo_path) if logo_path else QPixmap()
        if not logo_pixmap.isNull():
            scaled_logo = logo_pixmap.scaledToHeight(56)
            logo_img.setPixmap(scaled_logo)
            logo_img.setStyleSheet("background:transparent;border:none;padding:0;margin:0;")
            hl.addWidget(logo_img)
        else:
            logo.setStyleSheet(f"""
                font-size:24px;
                background:{ORANGE_DIM}80;
                border-radius:10px;
                padding:4px 8px;
                border:1px solid {ORANGE}40;
            """)
            hl.addWidget(logo)

        title_col = QVBoxLayout()
        title_col.setSpacing(1)
        t1 = QLabel("Real-Time Dashboard")
        t1.setStyleSheet(f"color:{TEXT_HI};font-size:16px;font-weight:800;background:transparent;border:none;")
        t2 = QLabel("Live monitoring · Auto-refresh every 3s")
        t2.setStyleSheet(f"color:{TEXT_LOW};font-size:11px;background:transparent;border:none;")
        title_col.addWidget(t1)
        title_col.addWidget(t2)

        self._refresh_lb = QLabel()
        self._refresh_lb.setStyleSheet(f"""
            color:{ORANGE};font-size:11px;font-weight:600;
            background:{ORANGE_DIM}40;
            border-radius:8px;padding:4px 12px;
            border:1px solid {ORANGE}30;
        """)

        hl.addSpacing(12)
        hl.addLayout(title_col)
        hl.addStretch()
        hl.addWidget(self._refresh_lb)
        root.addWidget(hdr)

        # ── Scrollable body ───────────────────────────────────────────────────
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet(f"""
            QScrollArea {{ background:{BG_DEEP}; border:none; }}
            QScrollBar:vertical {{
                background:{BG_CARD}; width:6px; border-radius:3px;
            }}
            QScrollBar::handle:vertical {{
                background:{ORANGE}60; border-radius:3px;
            }}
        """)

        body = QWidget()
        body.setStyleSheet(f"background:{BG_DEEP};")
        bl = QVBoxLayout(body)
        bl.setContentsMargins(28, 20, 28, 28)
        bl.setSpacing(18)

        # ── Quick info strip ──────────────────────────────────────────────────
        self._strip = QuickInfoStrip()
        bl.addWidget(self._strip)

        # ── Stat cards row ────────────────────────────────────────────────────
        stat_row = QHBoxLayout()
        stat_row.setSpacing(14)

        self.c_total   = StatCard("🗂️", "Total Profiles",  0, ORANGE,  ORANGE_DIM)
        self.c_running = StatCard("▶️", "Running",          0, GREEN,   GREEN_DIM)
        self.c_stopped = StatCard("⏹️", "Stopped",          0, BLUE,    BLUE_DIM)
        self.c_groups  = StatCard("📁", "Groups",           0, AMBER,   AMBER_DIM)
        self.c_proxy   = StatCard("🌐", "With Proxy",       0, PURPLE,  PURPLE_DIM)
        self.c_synced  = StatCard("☁️", "Cloud Synced",     0, RED,     RED_DIM)

        for c in [self.c_total, self.c_running, self.c_stopped,
                  self.c_groups, self.c_proxy, self.c_synced]:
            stat_row.addWidget(c)
        bl.addLayout(stat_row)

        # ── Middle row: 3 charts ──────────────────────────────────────────────
        charts_row = QHBoxLayout()
        charts_row.setSpacing(14)

        self.ch_browser = ChartCard("Browser Split",  "🌐")
        self.ch_os      = ChartCard("OS Distribution","💻")
        self.ch_group   = ChartCard("Profiles / Group","📁")

        for ch in [self.ch_browser, self.ch_os, self.ch_group]:
            ch.setMinimumHeight(220)
            charts_row.addWidget(ch)
        bl.addLayout(charts_row)

        # ── Bottom row: running + activity ────────────────────────────────────
        bot_row = QHBoxLayout()
        bot_row.setSpacing(14)

        self._running_card = RunningCard()
        self._running_card.setMinimumHeight(280)

        self._activity = ActivityCard()
        self._activity.setMinimumHeight(280)

        bot_row.addWidget(self._running_card, 2)
        bot_row.addWidget(self._activity, 3)
        bl.addLayout(bot_row)

        bl.addStretch()
        scroll.setWidget(body)
        root.addWidget(scroll, 1)

        # Seed events
        self._activity.add("🚀", "Dashboard loaded — monitoring active", ORANGE)

    # ── Refresh ───────────────────────────────────────────────────────────────
    def refresh(self):
        profiles = self.pp.profiles
        total   = len(profiles)
        running = sum(1 for p in profiles if p.status == "running")
        stopped = total - running
        groups  = len(set(p.group for p in profiles))
        proxied = sum(1 for p in profiles if p.proxy.host)
        synced  = sum(1 for p in profiles if p.cloud_synced)

        self.c_total.set_value(total)
        self.c_running.set_value(running)
        self.c_stopped.set_value(stopped)
        self.c_groups.set_value(groups)
        self.c_proxy.set_value(proxied)
        self.c_synced.set_value(synced)

        b = {}
        o = {}
        g = {}
        for p in profiles:
            b[p.browser_type] = b.get(p.browser_type, 0) + 1
            o[p.os_type]      = o.get(p.os_type, 0) + 1
            g[p.group]        = g.get(p.group, 0) + 1

        self.ch_browser.update_data(b)
        self.ch_os.update_data(o)
        self.ch_group.update_data(g)
        self._running_card.update(profiles)

        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self._refresh_lb.setText(f"● LIVE  {ts}")

    def log_event(self, icon, text, color=TEXT_MID):
        self._activity.add(icon, text, color)
