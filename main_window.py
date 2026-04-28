"""Main window: sidebar + profile table panel."""
import datetime
import zipfile, json, shutil, os, tempfile
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QAbstractItemView, QLineEdit, QComboBox, QFrame, QStatusBar,
    QSplitter, QApplication, QMenu, QMessageBox, QDialog, QStackedWidget,
    QFileDialog, QProgressDialog
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QAction, QFont, QIcon, QColor, QPixmap

from models import (
    BrowserProfile, SAMPLE_PROFILES, SAMPLE_MEMBERS,
    TeamMember, RPATask, APIKey
)
import storage
from styles import DARK_THEME
from profile_dialog import ProfileDialog
from batch_dialog import BatchDialog
from team_dialog import TeamDialog, ShareProfileDialog, TransferDialog
from rpa_dialog import RPADialog
from settings_dialog import SettingsDialog
from api_dialog import APIDialog
from browser_launcher import launch_profile, stop_profile
from dashboard_panel import DashboardPanel
from groups_panel import GroupsPanel


# ── Badge widget ──────────────────────────────────────────────────────────────

def _badge(text, style):
    lb = QLabel(text)
    lb.setAlignment(Qt.AlignmentFlag.AlignCenter)
    lb.setStyleSheet(f"{style}border-radius:10px;padding:2px 8px;font-size:11px;font-weight:600;")
    lb.setFixedHeight(22)
    return lb


STATUS_STYLE = {
    "running": "background:#064e3b;color:#6ee7b7;",
    "stopped": "background:#1e2433;color:#64748b;",
    "loading": "background:#451a03;color:#fcd34d;",
}

BROWSER_ICON = {
    "Chrome": "🟡", "Firefox": "🦊", "Edge": "🔵", "Safari": "🧭", "Opera": "🔴",
}

OS_ICON = {
    "Windows": "🪟", "macOS": "🍎", "Linux": "🐧", "Android": "📱", "iOS": "📱",
}


# ── Sidebar ────────────────────────────────────────────────────────────────────

class Sidebar(QWidget):
    nav_changed = pyqtSignal(str)

    NAV_ITEMS = [
        ("dashboard", "📊", "Dashboard"),
        ("profiles",  "📋", "Profiles"),
        ("groups",    "📁", "Groups"),
        ("team",      "👥", "Team"),
        ("rpa",       "🤖", "RPA Tasks"),
        ("api",       "🔌", "Open API"),
        ("settings",  "⚙️", "Settings"),
    ]

    NAV_SECTIONS = {
        "profiles": "WORKSPACE",
        "team":     "COLLABORATION",
        "settings": "SYSTEM",
    }

    def __init__(self):
        super().__init__()
        self.setObjectName("sidebar")
        self.setFixedWidth(220)
        self._active = "profiles"
        self._btns = {}
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        # ── Logo area ─────────────────────────────────────────────────────────
        logo_w = QWidget()
        logo_w.setFixedHeight(80)
        logo_w.setStyleSheet("""
            background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                stop:0 #0e1420, stop:1 #080b12);
            border-bottom: 1px solid #141a28;
        """)
        ll = QHBoxLayout(logo_w)
        ll.setContentsMargins(10, 8, 10, 8)
        ll.setSpacing(0)

        import os as _os
        _logo_path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "assets", "Logo.png")
        logo_lbl = QLabel()
        logo_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        _pm = QPixmap(_logo_path)
        if not _pm.isNull():
            logo_lbl.setPixmap(_pm.scaled(180, 60,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation))
        else:
            logo_lbl.setText("KH Browser")
            logo_lbl.setStyleSheet("color:#f97316; font-size:16px; font-weight:800;")

        ll.addWidget(logo_lbl, 1)
        lay.addWidget(logo_w)

        # ── Nav items ─────────────────────────────────────────────────────────
        scroll_w = QWidget()
        scroll_lay = QVBoxLayout(scroll_w)
        scroll_lay.setContentsMargins(12, 12, 12, 12)
        scroll_lay.setSpacing(2)

        _section_shown = set()
        for key, icon, label in self.NAV_ITEMS:
            # Section label
            if key in self.NAV_SECTIONS and key not in _section_shown:
                sec = self.NAV_SECTIONS[key]
                sec_lb = QLabel(sec)
                sec_lb.setStyleSheet("""
                    color: #253555;
                    font-size: 9px;
                    font-weight: 800;
                    letter-spacing: 2px;
                    padding: 10px 10px 4px 10px;
                """)
                scroll_lay.addWidget(sec_lb)
                _section_shown.add(key)

            btn = QPushButton()
            btn.setFixedHeight(44)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)

            # inner layout
            btn_lay = QHBoxLayout(btn)
            btn_lay.setContentsMargins(12, 0, 12, 0)
            btn_lay.setSpacing(10)

            icon_lb = QLabel(icon)
            icon_lb.setFixedSize(26, 26)
            icon_lb.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_lb.setStyleSheet("font-size: 15px; background:transparent; border:none;")

            lbl_lb = QLabel(label)
            lbl_lb.setStyleSheet("""
                font-size: 13px; font-weight: 500;
                background: transparent; border: none;
            """)

            # active indicator bar
            indicator = QFrame()
            indicator.setFixedSize(3, 20)
            indicator.setStyleSheet("background: transparent; border-radius: 2px;")
            indicator.setObjectName(f"ind_{key}")

            btn_lay.addWidget(icon_lb)
            btn_lay.addWidget(lbl_lb, 1)
            btn_lay.addWidget(indicator)

            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: none;
                    border-radius: 10px;
                    text-align: left;
                    color: #475569;
                }
                QPushButton:hover {
                    background: #0e1828;
                    color: #94a3b8;
                }
            """)
            btn.clicked.connect(lambda _, k=key: self._activate(k))

            # store refs for styling
            btn._icon_lb = icon_lb
            btn._lbl_lb  = lbl_lb
            btn._indicator = indicator

            self._btns[key] = btn
            scroll_lay.addWidget(btn)

        scroll_lay.addStretch()
        lay.addWidget(scroll_w, 1)

        # ── Bottom user card ──────────────────────────────────────────────────
        bottom = QWidget()
        bottom.setFixedHeight(70)
        bottom.setStyleSheet("""
            border-top: 1px solid #141a28;
            background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                stop:0 #0a0d16, stop:1 #080b12);
        """)
        bl = QHBoxLayout(bottom)
        bl.setContentsMargins(16, 0, 16, 0)
        bl.setSpacing(10)

        av = QLabel("JS")
        av.setFixedSize(36, 36)
        av.setAlignment(Qt.AlignmentFlag.AlignCenter)
        av.setStyleSheet("""
            background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                stop:0 #7c2d12, stop:1 #f97316);
            color: white; font-size: 12px; font-weight: 800;
            border-radius: 10px; border: none;
        """)

        uinfo = QVBoxLayout()
        uinfo.setSpacing(2)
        u1 = QLabel("John Smith")
        u1.setStyleSheet("color:#e2e8f0; font-size:12px; font-weight:700;")
        u2 = QLabel("Owner · Pro Plan")
        u2.setStyleSheet("color:#334155; font-size:10px;")
        uinfo.addWidget(u1)
        uinfo.addWidget(u2)

        online = QLabel("●")
        online.setStyleSheet("color:#22c55e; font-size:9px;")
        online.setToolTip("Online")

        bl.addWidget(av)
        bl.addLayout(uinfo, 1)
        bl.addWidget(online)
        lay.addWidget(bottom)

        # Apply initial active state
        self._apply_active(self._active)

    def _apply_active(self, key):
        for k, btn in self._btns.items():
            active = k == key
            if active:
                btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                            stop:0 #1e2d45, stop:1 #f9731608);
                        border: none;
                        border-radius: 10px;
                        border-left: 3px solid #f97316;
                        color: #f97316;
                    }
                    QPushButton:hover { background: #1e2d45; }
                """)
                btn._lbl_lb.setStyleSheet(
                    "color:#f97316; font-size:13px; font-weight:700; background:transparent; border:none;"
                )
                btn._indicator.setStyleSheet(
                    "background: #f97316; border-radius: 2px;"
                )
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background: transparent;
                        border: none;
                        border-radius: 10px;
                        color: #475569;
                    }
                    QPushButton:hover { background: #0e1828; }
                """)
                btn._lbl_lb.setStyleSheet(
                    "color:#475569; font-size:13px; font-weight:500; background:transparent; border:none;"
                )
                btn._indicator.setStyleSheet("background:transparent; border-radius:2px;")

    def _activate(self, key):
        self._active = key
        self._apply_active(key)
        self.nav_changed.emit(key)


# ── Profile Panel ──────────────────────────────────────────────────────────────

class ProfilePanel(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.mw = main_window
        # Load saved profiles; fall back to sample data on first run
        saved = storage.load_profiles()
        self.profiles = saved if saved else list(SAMPLE_PROFILES)
        if not saved:                          # first ever run → persist sample data
            storage.save_profiles(self.profiles)
        self._processes = {}   # profile.id → subprocess.Popen
        self._build()
        self._populate()

    # ── Column indices ────────────────────────────────────────────────────────
    COL_CHK     = 0
    COL_IDX     = 1
    COL_PROFILE = 2   # avatar + name + id
    COL_GROUP   = 3
    COL_BROWSER = 4
    COL_OS      = 5
    COL_PROXY   = 6
    COL_FP      = 7   # fingerprint summary
    COL_STATUS  = 8
    COL_USED    = 9
    COL_ACTIONS = 10

    # Avatar colour palette (cycles by profile index)
    AVATAR_COLORS = [
        ("#7c3aed","#4c1d95"), ("#f97316","#7c2d12"), ("#10b981","#064e3b"),
        ("#3b82f6","#1e3a8a"), ("#ec4899","#831843"), ("#f59e0b","#78350f"),
        ("#06b6d4","#0c4a6e"), ("#84cc16","#365314"),
    ]

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        # ── Top bar ───────────────────────────────────────────────────────────
        top = QWidget()
        top.setFixedHeight(64)
        top.setStyleSheet("""
            background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                stop:0 #0d1117, stop:1 #080c12);
            border-bottom: 1px solid #1a2236;
        """)
        tl = QHBoxLayout(top)
        tl.setContentsMargins(20, 0, 20, 0)
        tl.setSpacing(10)

        # Search
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍  Search by name, group, browser, proxy…")
        self.search_box.setFixedHeight(38)
        self.search_box.setMinimumWidth(300)
        self.search_box.setStyleSheet("""
            QLineEdit {
                background:#111827; color:#e2e8f0;
                border:1px solid #1e2d45; border-radius:10px;
                padding:0 14px; font-size:13px;
            }
            QLineEdit:focus { border:1px solid #f97316; }
        """)
        self.search_box.textChanged.connect(self._filter)

        # Filters
        filter_style = """
            QComboBox {
                background:#111827; color:#94a3b8;
                border:1px solid #1e2d45; border-radius:10px;
                padding:0 12px; height:38px; font-size:12px;
            }
            QComboBox:hover { border:1px solid #f97316; }
            QComboBox::drop-down { border:none; width:24px; }
            QComboBox QAbstractItemView {
                background:#111827; color:#e2e8f0;
                border:1px solid #1e2d45; selection-background-color:#1e3a5f;
            }
        """
        self.group_filter = QComboBox()
        self.group_filter.setFixedHeight(38)
        self.group_filter.setMinimumWidth(130)
        self.group_filter.setStyleSheet(filter_style)
        self.group_filter.addItem("📁  All Groups")
        for g in sorted(set(p.group for p in self.profiles)):
            self.group_filter.addItem(g)
        self.group_filter.currentTextChanged.connect(self._filter)

        self.status_filter = QComboBox()
        self.status_filter.setFixedHeight(38)
        self.status_filter.setMinimumWidth(120)
        self.status_filter.setStyleSheet(filter_style)
        for s in ["⚡  All Status", "🟢  Running", "⬜  Stopped"]:
            self.status_filter.addItem(s)
        self.status_filter.currentTextChanged.connect(self._filter)

        tl.addWidget(self.search_box, 2)
        tl.addWidget(self.group_filter)
        tl.addWidget(self.status_filter)
        tl.addStretch()

        # Action buttons
        btn_configs = [
            ("✨  New Profile", "#f97316", "#c2410c", self._new_profile),
            ("⚡  Batch",       "#1e2d45", "#253555", self._batch),
            ("☁️  Sync",        "#1e2d45", "#253555", self._sync),
        ]
        for label, bg, hover, handler in btn_configs:
            b = QPushButton(label)
            b.setFixedHeight(38)
            b.setStyleSheet(f"""
                QPushButton {{
                    background:{bg}; color:#f1f5f9;
                    border:none; border-radius:10px;
                    padding:0 18px; font-size:13px; font-weight:600;
                }}
                QPushButton:hover {{ background:{hover}; }}
            """)
            b.clicked.connect(handler)
            tl.addWidget(b)
        lay.addWidget(top)

        # ── Sub-toolbar ───────────────────────────────────────────────────────
        sub = QWidget()
        sub.setFixedHeight(46)
        sub.setStyleSheet("background:#080c12; border-bottom:1px solid #1a2236;")
        sl = QHBoxLayout(sub)
        sl.setContentsMargins(20, 0, 20, 0)
        sl.setSpacing(8)

        def _sub_btn(label, color="#94a3b8", bg="#111827", hover="#1e2d45"):
            b = QPushButton(label)
            b.setFixedHeight(30)
            b.setStyleSheet(f"""
                QPushButton {{
                    background:{bg}; color:{color};
                    border:1px solid #1e2d45; border-radius:8px;
                    padding:0 12px; font-size:12px; font-weight:500;
                }}
                QPushButton:hover {{ background:{hover}; border-color:#f97316; }}
            """)
            return b

        self.sel_all_btn = _sub_btn("☐  Select All")
        self.sel_all_btn.clicked.connect(self._select_all)

        self.profile_count_lb = QLabel()
        self.profile_count_lb.setStyleSheet("color:#334155; font-size:12px; padding:0 8px;")

        self.open_btn   = _sub_btn("▶  Open",    "#22c55e", "#0a1f13", "#14532d")
        self.share_btn  = _sub_btn("🔗  Share",   "#94a3b8")
        self.transfer_btn = _sub_btn("🔄  Transfer","#94a3b8")
        self.delete_btn = _sub_btn("🗑  Delete",  "#f87171", "#1a0a0a", "#450a0a")

        self.open_btn.clicked.connect(self._open_selected)
        self.share_btn.clicked.connect(self._share_selected)
        self.transfer_btn.clicked.connect(self._transfer_selected)
        self.delete_btn.clicked.connect(self._delete_selected)

        sl.addWidget(self.sel_all_btn)
        sl.addWidget(self.profile_count_lb)
        sl.addStretch()
        sl.addWidget(self.open_btn)
        sl.addWidget(self.share_btn)
        sl.addWidget(self.transfer_btn)
        sl.addWidget(self.delete_btn)
        lay.addWidget(sub)

        # ── Table ─────────────────────────────────────────────────────────────
        COLS = ["", "#", "Profile", "Group", "Browser", "OS",
                "Proxy", "Fingerprint", "Status", "Last Used", "Actions"]
        self.table = QTableWidget(0, len(COLS))
        self.table.setHorizontalHeaderLabels(COLS)
        hh = self.table.horizontalHeader()
        hh.setVisible(True)
        hh.setMinimumSectionSize(30)
        hh.setDefaultSectionSize(100)
        hh.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        hh.setSectionResizeMode(self.COL_PROFILE, QHeaderView.ResizeMode.Stretch)
        hh.setSectionResizeMode(self.COL_ACTIONS, QHeaderView.ResizeMode.Fixed)
        # Total fixed = 1000px; Profile (Stretch) fills the remaining ~220px
        self.table.setColumnWidth(self.COL_CHK,     38)
        self.table.setColumnWidth(self.COL_IDX,     42)
        self.table.setColumnWidth(self.COL_GROUP,   112)
        self.table.setColumnWidth(self.COL_BROWSER, 105)
        self.table.setColumnWidth(self.COL_OS,       95)
        self.table.setColumnWidth(self.COL_PROXY,   118)
        self.table.setColumnWidth(self.COL_FP,      128)
        self.table.setColumnWidth(self.COL_STATUS,   98)
        self.table.setColumnWidth(self.COL_USED,    108)
        self.table.setColumnWidth(self.COL_ACTIONS, 156)

        self.table.setStyleSheet("""
            QTableWidget {
                background: #080c12;
                alternate-background-color: #0a0f18;
                border: none;
                gridline-color: transparent;
                font-size: 13px;
                color: #e2e8f0;
                outline: none;
            }
            QTableWidget::item { padding: 0px; border: none; }
            QTableWidget::item:selected {
                background: #1e2d45;
                color: #f1f5f9;
            }
            QHeaderView::section {
                background: #0d1117;
                color: #475569;
                font-size: 11px;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 1px;
                padding: 10px 8px;
                border: none;
                border-bottom: 2px solid #1a2236;
                border-right: 1px solid #1a2236;
            }
            QHeaderView::section:hover { color: #f97316; background: #0d1421; }
            QScrollBar:vertical {
                background: #0d1117; width: 6px; border-radius: 3px;
            }
            QScrollBar::handle:vertical {
                background: #f97316; border-radius: 3px; min-height: 30px;
            }
            QScrollBar:horizontal {
                background: #0d1117; height: 6px; border-radius: 3px;
            }
            QScrollBar::handle:horizontal {
                background: #f97316; border-radius: 3px;
            }
        """)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(False)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._context_menu)
        lay.addWidget(self.table, 1)

    # ── Helpers ───────────────────────────────────────────────────────────────
    @staticmethod
    def _time_ago(dt_str):
        if not dt_str:
            return "—"
        try:
            dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
            diff = datetime.datetime.now() - dt
            s = int(diff.total_seconds())
            if s < 60:       return "just now"
            if s < 3600:     return f"{s//60}m ago"
            if s < 86400:    return f"{s//3600}h ago"
            return f"{s//86400}d ago"
        except Exception:
            return dt_str

    @staticmethod
    def _make_badge(text, fg, bg, border="transparent"):
        lb = QLabel(text)
        lb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lb.setStyleSheet(f"""
            QLabel {{
                color:{fg}; background:{bg};
                border:1px solid {border};
                border-radius:6px;
                padding:2px 8px;
                font-size:11px;
                font-weight:600;
            }}
        """)
        return lb

    @staticmethod
    def _cell(widget, align=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft):
        w = QWidget()
        w.setStyleSheet("background:transparent;")
        l = QHBoxLayout(w)
        l.setContentsMargins(6, 0, 6, 0)
        l.setSpacing(6)
        l.setAlignment(align)
        l.addWidget(widget)
        l.addStretch()
        return w

    def _populate(self, filter_text="", group="All Groups", status="All Status"):
        import datetime
        self.table.setRowCount(0)
        shown = 0

        # Normalize filter strings (strip emojis/spaces from combo labels)
        grp_filter  = group.replace("📁  ","").replace("All Groups","All Groups")
        stat_filter = (status.replace("⚡  ","").replace("🟢  ","")
                             .replace("⬜  ","").strip())

        for i, p in enumerate(self.profiles):
            if filter_text:
                q = filter_text.lower()
                haystack = f"{p.name} {p.group} {p.browser_type} {p.os_type} {p.proxy.host} {p.id}".lower()
                if q not in haystack:
                    continue
            if grp_filter not in ("All Groups", "") and p.group != grp_filter:
                continue
            if stat_filter not in ("All Status", "") and p.status.lower() != stat_filter.lower():
                continue

            r = self.table.rowCount()
            self.table.insertRow(r)
            self.table.setRowHeight(r, 58)

            # ── COL 0: Checkbox ───────────────────────────────────────────────
            from PyQt6.QtWidgets import QCheckBox
            cb_w = QWidget()
            cb_w.setStyleSheet("background:transparent;")
            cb_l = QHBoxLayout(cb_w)
            cb_l.setContentsMargins(10, 0, 0, 0)
            cb = QCheckBox()
            cb.setStyleSheet("""
                QCheckBox::indicator { width:16px; height:16px; border-radius:4px;
                    border:2px solid #334155; background:#111827; }
                QCheckBox::indicator:checked { background:#f97316; border-color:#f97316; }
                QCheckBox::indicator:hover { border-color:#f97316; }
            """)
            cb_l.addWidget(cb)
            self.table.setCellWidget(r, self.COL_CHK, cb_w)

            # ── COL 1: Index ──────────────────────────────────────────────────
            idx_item = QTableWidgetItem(str(i + 1))
            idx_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            idx_item.setForeground(QColor("#334155"))
            self.table.setItem(r, self.COL_IDX, idx_item)

            # ── COL 2: Profile (Avatar + Name + ID) ───────────────────────────
            ac, ac_bg = self.AVATAR_COLORS[i % len(self.AVATAR_COLORS)]
            avatar = QLabel(p.name[0].upper() if p.name else "?")
            avatar.setFixedSize(36, 36)
            avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
            avatar.setStyleSheet(f"""
                QLabel {{
                    background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                        stop:0 {ac}, stop:1 {ac_bg});
                    color: white;
                    border-radius: 10px;
                    font-size: 15px;
                    font-weight: 800;
                    border: none;
                }}
            """)

            name_col = QVBoxLayout()
            name_col.setSpacing(2)
            name_col.setContentsMargins(0, 0, 0, 0)

            name_lb = QLabel(p.name)
            name_lb.setStyleSheet("color:#f1f5f9; font-size:13px; font-weight:700;"
                                  "background:transparent; border:none;")

            id_row = QHBoxLayout()
            id_row.setSpacing(6)
            id_row.setContentsMargins(0, 0, 0, 0)
            id_lb = QLabel(f"#{p.id}")
            id_lb.setStyleSheet("color:#334155; font-size:10px; background:transparent; border:none;")
            id_row.addWidget(id_lb)
            if p.cloud_synced:
                sync_lb = QLabel("☁️")
                sync_lb.setStyleSheet("font-size:10px; background:transparent; border:none;")
                sync_lb.setToolTip("Cloud synced")
                id_row.addWidget(sync_lb)
            id_row.addStretch()

            name_col.addStretch()
            name_col.addWidget(name_lb)
            id_row_w = QWidget()
            id_row_w.setStyleSheet("background:transparent;")
            id_row_w.setLayout(id_row)
            name_col.addWidget(id_row_w)
            name_col.addStretch()

            prof_w = QWidget()
            prof_w.setStyleSheet("background:transparent;")
            prof_l = QHBoxLayout(prof_w)
            prof_l.setContentsMargins(8, 0, 8, 0)
            prof_l.setSpacing(10)
            prof_l.addWidget(avatar)
            prof_l.addLayout(name_col, 1)
            self.table.setCellWidget(r, self.COL_PROFILE, prof_w)

            # ── COL 3: Group ──────────────────────────────────────────────────
            grp_w = QWidget()
            grp_w.setStyleSheet("background:transparent;")
            gl = QHBoxLayout(grp_w)
            gl.setContentsMargins(8, 0, 8, 0)
            gl.setSpacing(6)
            grp_dot = QLabel("●")
            grp_dot.setStyleSheet("color:#f97316; font-size:8px; background:transparent; border:none;")
            grp_lb = QLabel(p.group)
            grp_lb.setStyleSheet("color:#94a3b8; font-size:12px; background:transparent; border:none;")
            gl.addWidget(grp_dot)
            gl.addWidget(grp_lb)
            gl.addStretch()
            self.table.setCellWidget(r, self.COL_GROUP, grp_w)

            # ── COL 4: Browser ────────────────────────────────────────────────
            BROWSER_COLORS = {
                "Chrome":  ("#fbbf24","#78350f","#fef3c7"),
                "Firefox": ("#f97316","#7c2d12","#ffedd5"),
                "Edge":    ("#38bdf8","#0c4a6e","#e0f2fe"),
                "Safari":  ("#34d399","#064e3b","#d1fae5"),
                "Brave":   ("#fb7185","#881337","#ffe4e6"),
                "Opera":   ("#f87171","#450a0a","#fee2e2"),
            }
            bc = BROWSER_COLORS.get(p.browser_type, ("#94a3b8","#1e293b","#f8fafc"))
            brow_w = QWidget()
            brow_w.setStyleSheet("background:transparent;")
            bwl = QHBoxLayout(brow_w)
            bwl.setContentsMargins(8, 0, 8, 0)
            bwl.setSpacing(0)
            brow_badge = QLabel(f"  {BROWSER_ICON.get(p.browser_type,'🌐')} {p.browser_type}  ")
            brow_badge.setStyleSheet(f"""
                QLabel {{
                    color:{bc[0]}; background:{bc[1]}40;
                    border:1px solid {bc[0]}40;
                    border-radius:8px; font-size:11px; font-weight:600;
                }}
            """)
            bwl.addWidget(brow_badge)
            bwl.addStretch()
            self.table.setCellWidget(r, self.COL_BROWSER, brow_w)

            # ── COL 5: OS ─────────────────────────────────────────────────────
            OS_COLORS = {
                "Windows": ("#60a5fa","#1e3a8a"),
                "macOS":   ("#a78bfa","#3b0764"),
                "Linux":   ("#4ade80","#14532d"),
                "Android": ("#34d399","#064e3b"),
                "iOS":     ("#c084fc","#4a044e"),
            }
            oc = OS_COLORS.get(p.os_type, ("#94a3b8","#1e293b"))
            os_w = QWidget()
            os_w.setStyleSheet("background:transparent;")
            owl = QHBoxLayout(os_w)
            owl.setContentsMargins(8, 0, 8, 0)
            os_badge = QLabel(f"  {OS_ICON.get(p.os_type,'💻')} {p.os_type}  ")
            os_badge.setStyleSheet(f"""
                QLabel {{
                    color:{oc[0]}; background:{oc[1]}40;
                    border:1px solid {oc[0]}40;
                    border-radius:8px; font-size:11px; font-weight:600;
                }}
            """)
            owl.addWidget(os_badge)
            owl.addStretch()
            self.table.setCellWidget(r, self.COL_OS, os_w)

            # ── COL 6: Proxy ──────────────────────────────────────────────────
            prx_w = QWidget()
            prx_w.setStyleSheet("background:transparent;")
            pxl = QHBoxLayout(prx_w)
            pxl.setContentsMargins(8, 0, 8, 0)
            pxl.setSpacing(4)
            if p.proxy.host:
                proxy_icon = QLabel("🌐")
                proxy_icon.setStyleSheet("font-size:11px; background:transparent; border:none;")
                proxy_type = QLabel(p.proxy.type)
                proxy_type.setStyleSheet("""
                    color:#38bdf8; background:#0c4a6e40;
                    border:1px solid #38bdf840; border-radius:5px;
                    padding:1px 6px; font-size:10px; font-weight:600;
                """)
                proxy_host = QLabel(f"{p.proxy.host}:{p.proxy.port}" if p.proxy.port else p.proxy.host)
                proxy_host.setStyleSheet("color:#64748b; font-size:10px; background:transparent; border:none;")
                pxl.addWidget(proxy_icon)
                pxl.addWidget(proxy_type)
                pxl.addWidget(proxy_host)
            else:
                no_prx = QLabel("  —  No Proxy  ")
                no_prx.setStyleSheet("color:#334155; font-size:11px; background:transparent; border:none;")
                pxl.addWidget(no_prx)
            pxl.addStretch()
            self.table.setCellWidget(r, self.COL_PROXY, prx_w)

            # ── COL 7: Fingerprint ────────────────────────────────────────────
            fp = p.fingerprint
            fp_w = QWidget()
            fp_w.setStyleSheet("background:transparent;")
            fpl = QVBoxLayout(fp_w)
            fpl.setContentsMargins(8, 6, 8, 6)
            fpl.setSpacing(2)
            fp_screen = QLabel(f"🖥  {fp.screen_width}×{fp.screen_height}")
            fp_screen.setStyleSheet("color:#64748b; font-size:11px; background:transparent; border:none;")
            fp_ua = QLabel(f"🌐  {fp.language}")
            fp_ua.setStyleSheet("color:#475569; font-size:10px; background:transparent; border:none;")
            fpl.addWidget(fp_screen)
            fpl.addWidget(fp_ua)
            self.table.setCellWidget(r, self.COL_FP, fp_w)

            # ── COL 8: Status ─────────────────────────────────────────────────
            st_w = QWidget()
            st_w.setStyleSheet("background:transparent;")
            stl = QHBoxLayout(st_w)
            stl.setContentsMargins(8, 0, 8, 0)
            if p.status == "running":
                pulse = QLabel("●")
                pulse.setStyleSheet("color:#22c55e; font-size:9px; background:transparent; border:none;")
                st_badge = QLabel("  Running  ")
                st_badge.setStyleSheet("""
                    color:#22c55e; background:#14532d40;
                    border:1px solid #22c55e50; border-radius:8px;
                    font-size:11px; font-weight:700; padding:2px 4px;
                """)
                stl.addWidget(pulse)
                stl.addWidget(st_badge)
            else:
                st_badge = QLabel("  Stopped  ")
                st_badge.setStyleSheet("""
                    color:#475569; background:#0f172a;
                    border:1px solid #1e2d4550; border-radius:8px;
                    font-size:11px; font-weight:600; padding:2px 4px;
                """)
                stl.addWidget(st_badge)
            stl.addStretch()
            self.table.setCellWidget(r, self.COL_STATUS, st_w)

            # ── COL 9: Last Used ──────────────────────────────────────────────
            ago = self._time_ago(p.last_used)
            lu_w = QWidget()
            lu_w.setStyleSheet("background:transparent;")
            lul = QVBoxLayout(lu_w)
            lul.setContentsMargins(8, 6, 8, 6)
            lul.setSpacing(2)
            ago_lb = QLabel(ago)
            ago_lb.setStyleSheet("color:#94a3b8; font-size:12px; font-weight:600;"
                                 "background:transparent; border:none;")
            date_lb = QLabel(p.last_used or "Never")
            date_lb.setStyleSheet("color:#334155; font-size:10px; background:transparent; border:none;")
            lul.addWidget(ago_lb)
            lul.addWidget(date_lb)
            self.table.setCellWidget(r, self.COL_USED, lu_w)

            # ── COL 10: Actions ───────────────────────────────────────────────
            acts = QWidget()
            acts.setStyleSheet("background:transparent;")
            al = QHBoxLayout(acts)
            al.setContentsMargins(6, 0, 6, 0)
            al.setSpacing(4)

            def _act_btn(icon, tip, fg, bg, hover_bg):
                b = QPushButton(icon)
                b.setFixedSize(32, 32)
                b.setToolTip(tip)
                b.setStyleSheet(f"""
                    QPushButton {{
                        background:{bg}; color:{fg};
                        border:1px solid {bg}; border-radius:8px;
                        font-size:13px;
                    }}
                    QPushButton:hover {{
                        background:{hover_bg};
                        border-color:{fg};
                    }}
                """)
                return b

            is_running = p.status == "running"
            launch_btn = _act_btn(
                "⏹" if is_running else "▶",
                "Stop" if is_running else "Launch",
                "#f87171" if is_running else "#22c55e",
                "#450a0a30" if is_running else "#14532d30",
                "#450a0a" if is_running else "#14532d",
            )
            launch_btn.clicked.connect(lambda _, pr=p: self._toggle_profile(pr))

            edit_btn = _act_btn("✏️", "Edit",  "#94a3b8", "#111827", "#1e2d45")
            edit_btn.clicked.connect(lambda _, pr=p: self._edit_profile(pr))

            clone_btn = _act_btn("📋", "Clone", "#94a3b8", "#111827", "#1e2d45")
            clone_btn.clicked.connect(lambda _, pr=p: self._clone_profile(pr))

            more_btn = _act_btn("⋯", "More",  "#94a3b8", "#111827", "#1e2d45")
            more_btn.clicked.connect(lambda _, pr=p, btn=more_btn: self._more_menu(pr, btn))

            for b in [launch_btn, edit_btn, clone_btn, more_btn]:
                al.addWidget(b)
            self.table.setCellWidget(r, self.COL_ACTIONS, acts)
            shown += 1

        running = sum(1 for p in self.profiles if p.status == "running")
        self.profile_count_lb.setText(
            f"  {shown} shown  ·  {running} running  ·  {len(self.profiles)} total"
        )

    def _filter(self):
        self._populate(
            self.search_box.text(),
            self.group_filter.currentText(),
            self.status_filter.currentText(),
        )

    def _toggle_profile(self, profile: BrowserProfile):
        if profile.status == "running":
            # ── Stop ──────────────────────────────────────────────────────────
            proc = self._processes.pop(profile.id, None)
            stop_profile(proc)
            profile.status = "stopped"
            self._filter()
            self.mw.statusBar().showMessage(f"Stopped: {profile.name}", 3000)
            if hasattr(self.mw, 'dashboard_panel'):
                self.mw.dashboard_panel.log_event("⏹️", f"Stopped: {profile.name}", "#ef4444")
        else:
            # ── Launch ────────────────────────────────────────────────────────
            self.mw.statusBar().showMessage(f"⏳  Launching {profile.name}…")
            QApplication.processEvents()

            ok, msg, proc = launch_profile(profile)

            if ok:
                profile.status = "running"
                import datetime
                profile.last_used = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                self._processes[profile.id] = proc
                self._save()
                self.mw.statusBar().showMessage(f"✅  {msg}", 5000)
                # Log to dashboard activity feed
                if hasattr(self.mw, 'dashboard_panel'):
                    self.mw.dashboard_panel.log_event(
                        "▶️", f"Launched: {profile.name}", "#10b981"
                    )
                # Poll process — auto-mark stopped when browser closes
                self._watch_process(profile, proc)
            else:
                QMessageBox.critical(self, "Launch Failed", msg)
                self.mw.statusBar().showMessage(f"❌  Launch failed: {profile.name}", 5000)

            self._filter()

    def _watch_process(self, profile: BrowserProfile, proc):
        """Poll every 2 s; mark profile stopped when browser closes."""
        if proc is None:
            return
        timer = QTimer(self)
        def _check():
            if proc.poll() is not None:          # process ended
                timer.stop()
                self._processes.pop(profile.id, None)
                profile.status = "stopped"
                self._filter()
                self.mw.statusBar().showMessage(
                    f"Browser closed: {profile.name}", 4000
                )
        timer.timeout.connect(_check)
        timer.start(2000)

    def _new_profile(self):
        dlg = ProfileDialog(self)
        dlg.profile_saved.connect(self._on_profile_saved)
        dlg.exec()

    def _edit_profile(self, profile: BrowserProfile):
        dlg = ProfileDialog(self, profile)
        dlg.profile_saved.connect(lambda _: (self._save(), self._filter()))
        dlg.exec()

    def _clone_profile(self, profile: BrowserProfile):
        import copy, uuid
        clone = copy.deepcopy(profile)
        clone.id = str(uuid.uuid4())[:8].upper()
        clone.name = f"{profile.name} (Copy)"
        clone.status = "stopped"
        self.profiles.append(clone)
        self._save()
        self._filter()
        self.mw.statusBar().showMessage(f"Cloned: {clone.name}", 3000)

    def _save(self):
        """Persist all profiles to disk immediately."""
        storage.save_profiles(self.profiles)

    def _on_profile_saved(self, profile: BrowserProfile):
        if profile not in self.profiles:
            self.profiles.append(profile)
        self._save()
        self._filter()
        self.mw.statusBar().showMessage(f"✅  Saved: {profile.name}", 3000)

    def _select_all(self):
        for r in range(self.table.rowCount()):
            cb_w = self.table.cellWidget(r, 0)
            if cb_w:
                for cb in cb_w.findChildren(type(cb_w)):
                    pass
                from PyQt6.QtWidgets import QCheckBox
                for cb in cb_w.findChildren(QCheckBox):
                    cb.setChecked(True)

    def _get_selected(self):
        from PyQt6.QtWidgets import QCheckBox
        selected = []
        for r in range(self.table.rowCount()):
            cb_w = self.table.cellWidget(r, 0)
            if cb_w:
                for cb in cb_w.findChildren(QCheckBox):
                    if cb.isChecked() and r < len(self.profiles):
                        selected.append(self.profiles[r])
        return selected

    def _open_selected(self):
        sel = self._get_selected()
        if not sel:
            rows = set(i.row() for i in self.table.selectedItems())
            if rows:
                r = min(rows)
                if r < len(self.profiles):
                    self._toggle_profile(self.profiles[r])
            return
        for p in sel:
            self._toggle_profile(p)

    def _share_selected(self):
        sel = self._get_selected()
        dlg = ShareProfileDialog(self, sel, SAMPLE_MEMBERS)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            QMessageBox.information(self, "Share", f"✅  Profiles shared successfully.")

    def _transfer_selected(self):
        sel = self._get_selected()
        dlg = TransferDialog(self, sel, SAMPLE_MEMBERS)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            QMessageBox.information(self, "Transfer", "✅  Profiles transferred.")

    def _delete_selected(self):
        sel = self._get_selected()
        if not sel:
            rows = set(i.row() for i in self.table.selectedItems())
            if rows:
                sel = [self.profiles[r] for r in rows if r < len(self.profiles)]
        if not sel:
            return
        reply = QMessageBox.question(
            self, "Delete",
            f"Delete {len(sel)} profile(s)? This cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            for p in sel:
                if p in self.profiles:
                    storage.delete_profile_data(p.id)
                    self.profiles.remove(p)
            self._save()
            self._filter()

    def _more_menu(self, profile: BrowserProfile, btn):
        menu = QMenu(self)
        actions = [
            ("📋  Clone Profile",   lambda: self._clone_profile(profile)),
            ("🔗  Share Profile",   lambda: ShareProfileDialog(self, [profile], SAMPLE_MEMBERS).exec()),
            ("🔄  Transfer Profile",lambda: TransferDialog(self, [profile], SAMPLE_MEMBERS).exec()),
            ("💾  Export Profile",  lambda pr=profile: self._export_profile(pr)),
            ("♻️  Restore Profile", lambda: QMessageBox.information(self, "Restore", "Profile restored.")),
            (None, None),
            ("🗑  Delete Profile",  lambda: self._delete_profile(profile)),
        ]
        for label, handler in actions:
            if label is None:
                menu.addSeparator()
            else:
                act = QAction(label, self)
                act.triggered.connect(handler)
                menu.addAction(act)
        btn_pos = btn.mapToGlobal(btn.rect().bottomLeft())
        menu.exec(btn_pos)

    # ── Export profile as ZIP ─────────────────────────────────────────────────
    def _export_profile(self, profile):
        """Export a single profile to a .zip file the user chooses."""
        from storage import STORAGE_DIR

        default_name = f"{profile.name.replace(' ', '_')}_{profile.id[:8]}.zip"
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Export Profile — KH Browser",
            os.path.join(os.path.expanduser("~"), "Desktop", default_name),
            "KH Browser Profile (*.zip)"
        )
        if not save_path:
            return  # user cancelled

        # Show progress
        prog = QProgressDialog("Exporting profile…", None, 0, 4, self)
        prog.setWindowTitle("Export Profile")
        prog.setWindowModality(Qt.WindowModality.WindowModal)
        prog.setMinimumWidth(360)
        prog.setStyleSheet("""
            QProgressDialog { background:#0f172a; color:#f1f5f9; border:1px solid #1e293b; border-radius:12px; }
            QLabel { color:#f1f5f9; font-size:13px; padding:8px; }
            QProgressBar {
                background:#1e293b; border:none; border-radius:6px;
                height:10px; text-align:center; color:#f1f5f9;
            }
            QProgressBar::chunk { background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                stop:0 #f97316, stop:1 #fb923c); border-radius:6px; }
        """)
        prog.show()
        QApplication.processEvents()

        try:
            with tempfile.TemporaryDirectory() as tmp:
                export_dir = os.path.join(tmp, f"kh_profile_{profile.id[:8]}")
                os.makedirs(export_dir)

                # ── Step 1: Write profile metadata JSON ──────────────────────
                prog.setValue(1)
                prog.setLabelText("📋  Writing profile metadata…")
                QApplication.processEvents()

                meta = {
                    "export_version": "1.0",
                    "app": "KH Browser",
                    "exported_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "profile": {
                        "id":             profile.id,
                        "name":           profile.name,
                        "browser_type":   profile.browser_type,
                        "browser_version":profile.browser_version,
                        "os_type":        profile.os_type,
                        "os_version":     profile.os_version,
                        "group":          profile.group,
                        "status":         profile.status,
                        "created_at":     profile.created_at,
                        "last_used":      profile.last_used,
                        "notes":          profile.notes,
                        "startup_url":    profile.startup_url,
                        "tags":           profile.tags,
                        "fingerprint": {
                            "ua":         profile.fingerprint.user_agent   if hasattr(profile.fingerprint,"user_agent")   else getattr(profile.fingerprint,"ua",""),
                            "platform":   profile.fingerprint.platform     if hasattr(profile.fingerprint,"platform")     else "",
                            "language":   profile.fingerprint.language     if hasattr(profile.fingerprint,"language")     else "",
                            "timezone":   profile.fingerprint.timezone     if hasattr(profile.fingerprint,"timezone")     else "",
                            "resolution": profile.fingerprint.resolution   if hasattr(profile.fingerprint,"resolution")   else "",
                            "webgl":      profile.fingerprint.webgl_vendor if hasattr(profile.fingerprint,"webgl_vendor") else "",
                            "canvas":     profile.fingerprint.canvas_noise if hasattr(profile.fingerprint,"canvas_noise") else "",
                        } if profile.fingerprint else {},
                        "proxy": {
                            "type":     profile.proxy.proxy_type if hasattr(profile.proxy,"proxy_type") else getattr(profile.proxy,"type",""),
                            "host":     profile.proxy.host,
                            "port":     profile.proxy.port,
                            "username": profile.proxy.username,
                            "password": profile.proxy.password,
                        } if profile.proxy else None,
                    }
                }
                with open(os.path.join(export_dir, "profile.json"), "w", encoding="utf-8") as f:
                    json.dump(meta, f, indent=2, ensure_ascii=False)

                # ── Step 2: Copy browser profile data folder (if exists) ──────
                prog.setValue(2)
                prog.setLabelText("📁  Copying browser data…")
                QApplication.processEvents()

                profile_data_dir = STORAGE_DIR / "profiles" / profile.id
                if profile_data_dir.exists():
                    dest = os.path.join(export_dir, "browser_data")
                    shutil.copytree(str(profile_data_dir), dest,
                                   ignore=shutil.ignore_patterns(
                                       "Cache", "Code Cache", "GPU Cache",
                                       "logs", "*.log", "CrashPad"
                                   ))

                # ── Step 3: Write README inside ZIP ──────────────────────────
                prog.setValue(3)
                prog.setLabelText("📝  Writing README…")
                QApplication.processEvents()

                readme = (
                    f"KH Browser — Profile Export\n"
                    f"============================\n\n"
                    f"Profile Name : {profile.name}\n"
                    f"Profile ID   : {profile.id}\n"
                    f"Browser      : {profile.browser_type} {profile.browser_version}\n"
                    f"OS           : {profile.os_type} {profile.os_version}\n"
                    f"Exported At  : {meta['exported_at']}\n\n"
                    f"How to import:\n"
                    f"  1. Open KH Browser\n"
                    f"  2. Go to Profiles → ⋯ More → Import Profile\n"
                    f"  3. Select this .zip file\n"
                )
                with open(os.path.join(export_dir, "README.txt"), "w") as f:
                    f.write(readme)

                # ── Step 4: Pack everything into ZIP ─────────────────────────
                prog.setValue(4)
                prog.setLabelText("🗜️  Packing ZIP archive…")
                QApplication.processEvents()

                with zipfile.ZipFile(save_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
                    for root, dirs, files in os.walk(export_dir):
                        for fname in files:
                            full = os.path.join(root, fname)
                            arcname = os.path.relpath(full, tmp)
                            zf.write(full, arcname)

            prog.close()

            # ── Success dialog ────────────────────────────────────────────────
            size_mb = os.path.getsize(save_path) / (1024 * 1024)
            msg = QMessageBox(self)
            msg.setWindowTitle("Export Complete")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText(
                f"<b style='color:#f97316; font-size:15px;'>✅  Profile Exported!</b>"
            )
            msg.setInformativeText(
                f"<b>{profile.name}</b> has been exported successfully.<br><br>"
                f"📦 &nbsp;<b>File:</b> {os.path.basename(save_path)}<br>"
                f"📁 &nbsp;<b>Size:</b> {size_mb:.2f} MB<br>"
                f"📍 &nbsp;<b>Saved to:</b><br>"
                f"<span style='color:#94a3b8; font-size:11px;'>{save_path}</span>"
            )
            msg.setStyleSheet("""
                QMessageBox { background:#0f172a; }
                QLabel { color:#f1f5f9; font-size:13px; }
                QPushButton {
                    background:#f97316; color:white; border:none;
                    border-radius:8px; padding:8px 20px; font-weight:700;
                }
                QPushButton:hover { background:#fb923c; }
            """)
            open_btn = msg.addButton("📂  Show in Folder", QMessageBox.ButtonRole.ActionRole)
            msg.addButton("OK", QMessageBox.ButtonRole.AcceptRole)
            msg.exec()

            if msg.clickedButton() == open_btn:
                folder = os.path.dirname(save_path)
                import subprocess as _sp
                if os.sys.platform == "darwin":
                    _sp.run(["open", "-R", save_path])
                elif os.sys.platform == "win32":
                    _sp.run(["explorer", "/select,", save_path])
                else:
                    _sp.run(["xdg-open", folder])

        except Exception as e:
            prog.close()
            QMessageBox.critical(self, "Export Failed", f"Could not export profile:\n{e}")

    def _delete_profile(self, profile):
        reply = QMessageBox.question(
            self, "Delete", f"Delete '{profile.name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            if profile in self.profiles:
                self.profiles.remove(profile)
            self._filter()

    def _batch(self):
        dlg = BatchDialog(self, self.profiles)
        dlg.exec()

    def _sync(self):
        self.mw.statusBar().showMessage("☁️  Syncing profiles to cloud…", 2000)
        QTimer.singleShot(2500, lambda: self.mw.statusBar().showMessage("✅  Cloud sync complete", 3000))

    def _context_menu(self, pos):
        idx = self.table.indexAt(pos)
        if not idx.isValid() or idx.row() >= len(self.profiles):
            return
        profile = self.profiles[idx.row()]
        menu = QMenu(self)
        for label, handler in [
            ("▶  Launch" if profile.status == "stopped" else "⏹  Stop",
             lambda: self._toggle_profile(profile)),
            ("✏️  Edit Profile",   lambda: self._edit_profile(profile)),
            ("📋  Clone Profile",  lambda: self._clone_profile(profile)),
            ("🔗  Share Profile",  lambda: ShareProfileDialog(self, [profile], SAMPLE_MEMBERS).exec()),
            (None, None),
            ("🗑  Delete",         lambda: self._delete_profile(profile)),
        ]:
            if label is None:
                menu.addSeparator()
            else:
                act = QAction(label, self)
                act.triggered.connect(handler)
                menu.addAction(act)
        menu.exec(self.table.mapToGlobal(pos))


# ── Placeholder panels ─────────────────────────────────────────────────────────

def _placeholder(icon, title, subtitle=""):
    w = QWidget()
    lay = QVBoxLayout(w)
    lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
    ib = QLabel(icon)
    ib.setAlignment(Qt.AlignmentFlag.AlignCenter)
    ib.setStyleSheet("font-size:48px;margin-bottom:10px;")
    tb = QLabel(title)
    tb.setAlignment(Qt.AlignmentFlag.AlignCenter)
    tb.setStyleSheet("font-size:20px;font-weight:700;color:#e2e8f0;")
    lay.addWidget(ib)
    lay.addWidget(tb)
    if subtitle:
        sb = QLabel(subtitle)
        sb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sb.setStyleSheet("color:#64748b;font-size:13px;")
        lay.addWidget(sb)
    return w


# ── Main Window ────────────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KH Browser")
        self.setMinimumSize(1440, 820)
        self.setStyleSheet(DARK_THEME)
        self._build()

    def _build(self):
        central = QWidget()
        central.setObjectName("centralWidget")
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.nav_changed.connect(self._nav)
        root.addWidget(self.sidebar)

        # Thin separator line
        sep = QFrame()
        sep.setFixedWidth(1)
        sep.setStyleSheet("background:#141a28;")
        root.addWidget(sep)

        # Stacked content
        self.stack = QStackedWidget()
        self.stack.setObjectName("mainContent")
        root.addWidget(self.stack, 1)

        self.profile_panel   = ProfilePanel(self)
        self.dashboard_panel = DashboardPanel(self.profile_panel)
        self.groups_panel    = GroupsPanel(self.profile_panel)

        self.stack.addWidget(self.dashboard_panel)   # 0
        self.stack.addWidget(self.profile_panel)     # 1
        self.stack.addWidget(self.groups_panel)      # 2

        self.stack.setCurrentIndex(1)
        self.sidebar._activate("profiles")

        # Premium status bar
        sb = QStatusBar()
        self.setStatusBar(sb)
        self._update_status()

        timer = QTimer(self)
        timer.timeout.connect(self._update_status)
        timer.start(5000)

    def _nav(self, key):
        if key == "dashboard":
            self.stack.setCurrentIndex(0)
            self.dashboard_panel.refresh()
        elif key == "profiles":
            self.stack.setCurrentIndex(1)
        elif key == "groups":
            self.stack.setCurrentIndex(2)
            self.groups_panel.refresh()
        elif key == "team":
            TeamDialog(self).exec()
            self.sidebar._activate("profiles")
        elif key == "rpa":
            RPADialog(self).exec()
            self.sidebar._activate("profiles")
        elif key == "api":
            APIDialog(self).exec()
            self.sidebar._activate("profiles")
        elif key == "settings":
            SettingsDialog(self).exec()
            self.sidebar._activate("profiles")

    def _update_status(self):
        running = sum(1 for p in self.profile_panel.profiles if p.status == "running")
        total = len(self.profile_panel.profiles)
        self.statusBar().showMessage(
            f"  🛡️  AntiDetect Browser Manager  |  {total} profiles  |  {running} running  "
            f"|  Cloud: Connected  |  v2.0.0"
        )
