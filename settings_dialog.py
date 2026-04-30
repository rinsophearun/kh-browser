"""Settings dialog (Global, Personal, Window Sync, Cloud Sync) - Professional UI Redesign."""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget,
    QTabWidget, QGroupBox, QComboBox, QCheckBox, QSpinBox, QLineEdit,
    QFrame, QSlider, QRadioButton, QProgressBar, QMessageBox,
    QDialogButtonBox, QSizePolicy, QFormLayout, QScrollArea
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon, QColor
from assets import get_asset_path


def _h_sep():
    f = QFrame()
    f.setFrameShape(QFrame.Shape.HLine)
    f.setStyleSheet("color:#1e2d45;")
    return f


def _row(label, widget):
    hl = QHBoxLayout()
    lb = QLabel(label)
    lb.setMinimumWidth(240)
    lb.setStyleSheet("""
        color:#cbd5e1;
        font-size:13px;
        font-weight:500;
        letter-spacing:0.3px;
    """)
    hl.addWidget(lb)
    hl.addWidget(widget, 1)
    hl.setSpacing(16)
    return hl


def _section(text, icon=""):
    lb = QLabel(f"{icon}  {text}" if icon else text)
    lb.setStyleSheet("""
        font-size:14px;
        font-weight:700;
        color:#f1f5f9;
        padding:12px 0 6px 0;
        letter-spacing:0.5px;
    """)
    return lb


def _card_wrapper(layout):
    """Wrap a layout in a styled card widget."""
    card = QWidget()
    card.setLayout(layout)
    card.setStyleSheet("""
        QWidget {
            background:#0e1420;
            border:1px solid #1e2d45;
            border-radius:14px;
            padding:24px;
        }
    """)
    return card


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumSize(1000, 750)
        self.resize(1100, 820)
        self.setStyleSheet("""
            QDialog {
                background:#07090f;
                border-radius:16px;
            }
        """)
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        header = QWidget()
        header.setFixedHeight(90)
        header.setStyleSheet("""
            background: qlineargradient(x1:0,y1:0,x2:1,y2:1,
                stop:0 #0a0d16, stop:1 #080b12);
            border-bottom:2px solid #1e2d45;
        """)
        hl = QHBoxLayout(header)
        hl.setContentsMargins(40, 24, 40, 24)
        hl.setSpacing(16)
        
        icon_lb = QLabel("⚙️")
        icon_lb.setStyleSheet("font-size:40px;")
        icon_lb.setFixedWidth(50)
        title = QLabel("Settings")
        title.setStyleSheet("""
            font-size:26px;
            font-weight:900;
            color:#f1f5f9;
            letter-spacing:0.8px;
        """)
        subtitle = QLabel("Manage application preferences and configurations")
        subtitle.setStyleSheet("""
            font-size:13px;
            color:#64748b;
            font-weight:500;
            letter-spacing:0.2px;
        """)
        
        vl = QVBoxLayout()
        vl.setContentsMargins(0, 0, 0, 0)
        vl.setSpacing(6)
        vl.addWidget(title)
        vl.addWidget(subtitle)
        
        hl.addWidget(icon_lb)
        hl.addLayout(vl, 1)
        root.addWidget(header)

        tabs = QTabWidget()
        tabs.setDocumentMode(False)
        tabs.setContentsMargins(0, 0, 0, 0)
        tabs.setStyleSheet("""
            QTabWidget::pane {
                background:#07090f;
                border:none;
                border-top:2px solid #1e2d45;
            }
            QTabBar {
                background:#0a0d16;
                border-bottom:1px solid #1e2d45;
            }
            QTabBar::tab {
                background:#0a0d16;
                color:#64748b;
                padding:16px 28px;
                border:none;
                font-size:13px;
                font-weight:600;
                letter-spacing:0.5px;
                margin-right:2px;
            }
            QTabBar::tab:selected {
                background:#0e1420;
                color:#f97316;
                border-bottom:3px solid #f97316;
            }
            QTabBar::tab:hover:!selected {
                color:#cbd5e1;
                background:#0d1319;
            }
        """)
        tabs.addTab(self._global_tab(), "🌐  Global")
        tabs.addTab(self._personal_tab(), "👤  Personal")
        tabs.addTab(self._window_sync_tab(), "🪟  Window Sync")
        tabs.addTab(self._cloud_tab(), "☁️  Cloud Sync")
        tabs.addTab(self._about_tab(), "ℹ️  About")
        root.addWidget(tabs, 1)

        footer = QWidget()
        footer.setFixedHeight(80)
        footer.setStyleSheet("""
            background:#0a0d16;
            border-top:2px solid #1e2d45;
        """)
        fl = QHBoxLayout(footer)
        fl.setContentsMargins(40, 18, 40, 18)
        fl.setSpacing(14)
        
        reset_btn = QPushButton("↺  Reset to Defaults")
        reset_btn.setFixedHeight(48)
        reset_btn.setMinimumWidth(160)
        reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        reset_btn.setStyleSheet("""
            QPushButton {
                background:#1e2d45;
                color:#cbd5e1;
                border:1px solid #253555;
                border-radius:11px;
                padding:0 28px;
                font-size:13px;
                font-weight:600;
                letter-spacing:0.3px;
            }
            QPushButton:hover {
                background:#253555;
                color:#f1f5f9;
                border-color:#f9731660;
            }
            QPushButton:pressed {
                background:#1a2236;
            }
        """)
        reset_btn.clicked.connect(self._reset)
        
        save_btn = QPushButton("💾  Save Settings")
        save_btn.setFixedHeight(48)
        save_btn.setFixedWidth(220)
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.setStyleSheet("""
            QPushButton {
                background:#f97316;
                color:#ffffff;
                border:none;
                border-radius:11px;
                font-size:13px;
                font-weight:700;
                letter-spacing:0.5px;
            }
            QPushButton:hover {
                background:#fb923c;
            }
            QPushButton:pressed {
                background:#c2410c;
            }
        """)
        save_btn.clicked.connect(self._save)
        
        fl.addWidget(reset_btn)
        fl.addStretch()
        fl.addWidget(save_btn)
        root.addWidget(footer)

    # ── Global ──────────────────────────────────────────────────────────────────
    def _global_tab(self):
        w = QWidget()
        w.setStyleSheet("background:#07090f;")
        main_lay = QVBoxLayout(w)
        main_lay.setContentsMargins(24, 24, 24, 24)
        main_lay.setSpacing(20)

        # Application Section
        app_lay = QVBoxLayout()
        app_lay.setSpacing(14)
        app_lay.addWidget(_section("🖥️  Application"))
        app_lay.addWidget(_h_sep())

        self.lang_combo = QComboBox()
        self.lang_combo.setMinimumHeight(38)
        self.lang_combo.setStyleSheet(self._combo_style())
        for l in ["English", "Chinese (Simplified)", "Chinese (Traditional)", "Japanese",
                  "Korean", "Russian", "Spanish", "Portuguese", "Vietnamese"]:
            self.lang_combo.addItem(l)
        app_lay.addLayout(_row("Interface Language", self.lang_combo))

        self.theme_combo = QComboBox()
        self.theme_combo.setMinimumHeight(38)
        self.theme_combo.setStyleSheet(self._combo_style())
        for t in ["Dark (Default)", "Light", "System Auto"]:
            self.theme_combo.addItem(t)
        app_lay.addLayout(_row("UI Theme", self.theme_combo))

        self.start_min_cb = QCheckBox("Start minimized to system tray")
        self.start_min_cb.setStyleSheet(self._checkbox_style())
        app_lay.addWidget(self.start_min_cb)

        self.autostart_cb = QCheckBox("Launch at system startup")
        self.autostart_cb.setStyleSheet(self._checkbox_style())
        app_lay.addWidget(self.autostart_cb)

        self.update_cb = QCheckBox("Check for updates automatically")
        self.update_cb.setChecked(True)
        self.update_cb.setStyleSheet(self._checkbox_style())
        app_lay.addWidget(self.update_cb)

        main_lay.addWidget(_card_wrapper(app_lay))

        # Browser Engine Section
        engine_lay = QVBoxLayout()
        engine_lay.setSpacing(14)
        engine_lay.addWidget(_section("🔧  Browser Engine"))
        engine_lay.addWidget(_h_sep())

        self.engine_combo = QComboBox()
        self.engine_combo.setMinimumHeight(38)
        self.engine_combo.setStyleSheet(self._combo_style())
        for e in ["Chromium 120", "Chromium 119", "Firefox 120", "Firefox 118"]:
            self.engine_combo.addItem(e)
        engine_lay.addLayout(_row("Default Browser Engine", self.engine_combo))

        self.cache_combo = QComboBox()
        self.cache_combo.setMinimumHeight(38)
        self.cache_combo.setStyleSheet(self._combo_style())
        for c in ["Per Profile (Isolated)", "Shared Cache", "No Cache"]:
            self.cache_combo.addItem(c)
        engine_lay.addLayout(_row("Cache Mode", self.cache_combo))

        self.max_open_spin = QSpinBox()
        self.max_open_spin.setRange(1, 200)
        self.max_open_spin.setValue(20)
        self.max_open_spin.setMinimumHeight(38)
        self.max_open_spin.setStyleSheet(self._spinbox_style())
        engine_lay.addLayout(_row("Max Open Profiles", self.max_open_spin))

        main_lay.addWidget(_card_wrapper(engine_lay))

        # Security Section
        sec_lay = QVBoxLayout()
        sec_lay.setSpacing(14)
        sec_lay.addWidget(_section("🔒  Security"))
        sec_lay.addWidget(_h_sep())

        self.encrypt_cb = QCheckBox("Encrypt profile data at rest")
        self.encrypt_cb.setChecked(True)
        self.encrypt_cb.setStyleSheet(self._checkbox_style())
        sec_lay.addWidget(self.encrypt_cb)

        self.lock_timeout_spin = QSpinBox()
        self.lock_timeout_spin.setRange(0, 120)
        self.lock_timeout_spin.setValue(30)
        self.lock_timeout_spin.setSuffix(" min")
        self.lock_timeout_spin.setMinimumHeight(38)
        self.lock_timeout_spin.setStyleSheet(self._spinbox_style())
        sec_lay.addLayout(_row("Auto-lock timeout (0 = disabled)", self.lock_timeout_spin))

        self.master_pw_cb = QCheckBox("Require master password on startup")
        self.master_pw_cb.setStyleSheet(self._checkbox_style())
        sec_lay.addWidget(self.master_pw_cb)

        main_lay.addWidget(_card_wrapper(sec_lay))
        main_lay.addStretch()
        return w

    # ── Personal ────────────────────────────────────────────────────────────────
    def _personal_tab(self):
        w = QWidget()
        w.setStyleSheet("background:#07090f;")
        main_lay = QVBoxLayout(w)
        main_lay.setContentsMargins(24, 24, 24, 24)
        main_lay.setSpacing(20)

        # Profile Section
        prof_lay = QVBoxLayout()
        prof_lay.setSpacing(14)
        prof_lay.addWidget(_section("👤  Profile"))
        prof_lay.addWidget(_h_sep())

        self.display_name = QLineEdit("SOPHEARUN")
        self.display_name.setMinimumHeight(38)
        self.display_name.setStyleSheet(self._lineedit_style())
        prof_lay.addLayout(_row("Display Name", self.display_name))

        self.email_edit = QLineEdit("sophearun@khbrowser.com")
        self.email_edit.setReadOnly(True)
        self.email_edit.setMinimumHeight(38)
        self.email_edit.setStyleSheet(self._lineedit_style())
        prof_lay.addLayout(_row("Email (read-only)", self.email_edit))

        ch_pw = QPushButton("🔐  Change Password")
        ch_pw.setFixedHeight(38)
        ch_pw.setFixedWidth(180)
        ch_pw.setCursor(Qt.CursorShape.PointingHandCursor)
        ch_pw.setStyleSheet(self._secondary_btn_style())
        ch_pw.clicked.connect(lambda: QMessageBox.information(self, "Password", "✅  Password change email sent."))
        pw_lay = QHBoxLayout()
        pw_lb = QLabel("Password")
        pw_lb.setMinimumWidth(240)
        pw_lb.setStyleSheet("color:#cbd5e1;font-size:13px;font-weight:500;")
        pw_lay.addWidget(pw_lb)
        pw_lay.addWidget(ch_pw)
        pw_lay.addStretch()
        prof_lay.addLayout(pw_lay)

        main_lay.addWidget(_card_wrapper(prof_lay))

        # Notifications Section
        notif_lay = QVBoxLayout()
        notif_lay.setSpacing(12)
        notif_lay.addWidget(_section("🔔  Notifications"))
        notif_lay.addWidget(_h_sep())

        for label in ["Task completed", "Task failed", "Profile sync error",
                      "Team member joined", "Profile shared with me", "API quota warning"]:
            cb = QCheckBox(label)
            cb.setChecked(True)
            cb.setStyleSheet(self._checkbox_style())
            notif_lay.addWidget(cb)

        main_lay.addWidget(_card_wrapper(notif_lay))

        # Display Preferences Section
        display_lay = QVBoxLayout()
        display_lay.setSpacing(14)
        display_lay.addWidget(_section("🎨  Display Preferences"))
        display_lay.addWidget(_h_sep())

        self.table_density = QComboBox()
        self.table_density.setMinimumHeight(38)
        self.table_density.setStyleSheet(self._combo_style())
        for d in ["Compact", "Normal", "Comfortable"]:
            self.table_density.addItem(d)
        self.table_density.setCurrentText("Normal")
        display_lay.addLayout(_row("Table Density", self.table_density))

        self.date_format = QComboBox()
        self.date_format.setMinimumHeight(38)
        self.date_format.setStyleSheet(self._combo_style())
        for f in ["YYYY-MM-DD", "MM/DD/YYYY", "DD/MM/YYYY"]:
            self.date_format.addItem(f)
        display_lay.addLayout(_row("Date Format", self.date_format))

        self.default_group = QComboBox()
        self.default_group.setMinimumHeight(38)
        self.default_group.setStyleSheet(self._combo_style())
        for g in ["Default", "Facebook", "E-commerce", "Social Media"]:
            self.default_group.addItem(g)
        display_lay.addLayout(_row("Default Group for New Profiles", self.default_group))

        main_lay.addWidget(_card_wrapper(display_lay))
        main_lay.addStretch()
        return w

    # ── Window Sync ─────────────────────────────────────────────────────────────
    def _window_sync_tab(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(24, 20, 24, 20)
        lay.setSpacing(12)

        lay.addWidget(_section("Window Synchronization"))
        lay.addWidget(_h_sep())

        info = QLabel(
            "Window Sync allows you to synchronize actions across multiple open browser "
            "profiles simultaneously — useful for managing many accounts at once."
        )
        info.setWordWrap(True)
        info.setStyleSheet("color:#64748b;font-size:12px;background:#111827;border-radius:6px;padding:10px;")
        lay.addWidget(info)

        self.sync_enable_cb = QCheckBox("Enable Window Synchronization")
        self.sync_enable_cb.setChecked(True)
        lay.addWidget(self.sync_enable_cb)

        lay.addSpacing(8)
        lay.addWidget(_section("Sync Settings"))
        lay.addWidget(_h_sep())

        self.sync_mouse_cb = QCheckBox("Sync mouse movements")
        self.sync_keyboard_cb = QCheckBox("Sync keyboard input")
        self.sync_scroll_cb = QCheckBox("Sync scroll actions")
        self.sync_click_cb = QCheckBox("Sync clicks")
        self.sync_nav_cb = QCheckBox("Sync navigation (URL changes)")
        for cb in [self.sync_mouse_cb, self.sync_keyboard_cb, self.sync_scroll_cb,
                   self.sync_click_cb, self.sync_nav_cb]:
            cb.setChecked(True)
            lay.addWidget(cb)

        lay.addSpacing(8)
        lay.addWidget(_section("Window Layout"))
        lay.addWidget(_h_sep())

        self.layout_combo = QComboBox()
        for l in ["Grid (auto)", "2×2", "3×2", "4×2", "Custom"]:
            self.layout_combo.addItem(l)
        lay.addLayout(_row("Layout Mode", self.layout_combo))

        self.leader_combo = QComboBox()
        self.leader_combo.addItem("First opened profile (default)")
        lay.addLayout(_row("Leader Profile (source)", self.leader_combo))

        self.delay_spin = QSpinBox()
        self.delay_spin.setRange(0, 5000)
        self.delay_spin.setValue(50)
        self.delay_spin.setSuffix(" ms")
        lay.addLayout(_row("Action broadcast delay", self.delay_spin))

        lay.addStretch()
        return w

    # ── Cloud ───────────────────────────────────────────────────────────────────
    def _cloud_tab(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(24, 20, 24, 20)
        lay.setSpacing(12)

        lay.addWidget(_section("Cloud Sync"))
        lay.addWidget(_h_sep())

        self.cloud_enable_cb = QCheckBox("Enable Cloud Sync")
        self.cloud_enable_cb.setChecked(True)
        lay.addWidget(self.cloud_enable_cb)

        # Usage bar
        usage_lay = QHBoxLayout()
        usage_lb = QLabel("Storage:")
        usage_lb.setMinimumWidth(100)
        self.usage_bar = QProgressBar()
        self.usage_bar.setRange(0, 100)
        self.usage_bar.setValue(34)
        self.usage_bar.setFixedHeight(8)
        self.usage_bar.setFormat("")
        used_lb = QLabel("3.4 GB / 10 GB")
        used_lb.setStyleSheet("color:#64748b;font-size:12px;")
        usage_lay.addWidget(usage_lb)
        usage_lay.addWidget(self.usage_bar, 1)
        usage_lay.addWidget(used_lb)
        lay.addLayout(usage_lay)

        lay.addSpacing(8)
        lay.addWidget(_section("Sync Options"))
        lay.addWidget(_h_sep())

        self.sync_auto_cb = QCheckBox("Auto-sync every:")
        interval_lay = QHBoxLayout()
        self.sync_interval = QSpinBox()
        self.sync_interval.setRange(1, 60)
        self.sync_interval.setValue(5)
        self.sync_interval.setSuffix(" min")
        interval_lay.addWidget(self.sync_auto_cb)
        interval_lay.addWidget(self.sync_interval)
        interval_lay.addStretch()
        lay.addLayout(interval_lay)

        for label, checked in [
            ("Sync profile settings", True),
            ("Sync fingerprint configurations", True),
            ("Sync proxy settings", False),
            ("Sync platform accounts", False),
            ("Sync extensions list", True),
            ("Sync RPA tasks", True),
        ]:
            cb = QCheckBox(label)
            cb.setChecked(checked)
            lay.addWidget(cb)

        lay.addSpacing(8)
        sync_now_btn = QPushButton("☁️  Sync Now")
        sync_now_btn.setObjectName("primaryBtn")
        sync_now_btn.setFixedHeight(40)
        sync_now_btn.clicked.connect(self._sync_now)
        lay.addWidget(sync_now_btn)

        self.sync_status_lb = QLabel("Last synced: 2024-01-15 09:00:00")
        self.sync_status_lb.setStyleSheet("color:#64748b;font-size:12px;")
        lay.addWidget(self.sync_status_lb)

        lay.addStretch()
        return w

    def _sync_now(self):
        self.sync_status_lb.setText("⏳  Syncing…")
        QTimer.singleShot(2000, lambda: self.sync_status_lb.setText(
            "✅  Last synced: just now"
        ))

    def _save(self):
        QMessageBox.information(self, "Settings", "✅  Settings saved successfully.")
        self.accept()

    def _reset(self):
        reply = QMessageBox.question(
            self, "Reset", "Reset all settings to default values?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "Reset", "✅  Settings reset to defaults.")

    # ── Window Sync ─────────────────────────────────────────────────────────────
    def _window_sync_tab(self):
        w = QWidget()
        w.setStyleSheet("background:#07090f;")
        main_lay = QVBoxLayout(w)
        main_lay.setContentsMargins(24, 24, 24, 24)
        main_lay.setSpacing(20)

        # Info Card
        info_lay = QVBoxLayout()
        info = QLabel(
            "Window Sync allows you to synchronize actions across multiple open browser "
            "profiles simultaneously — useful for managing many accounts at once."
        )
        info.setWordWrap(True)
        info.setStyleSheet("""
            color:#cbd5e1;
            font-size:12px;
            background:#0e1420;
            border:1px solid #1e2d45;
            border-radius:10px;
            padding:14px;
            line-height:1.6;
        """)
        info_lay.addWidget(info)
        main_lay.addWidget(_card_wrapper(info_lay))

        # Enable Section
        enable_lay = QVBoxLayout()
        enable_lay.setSpacing(14)
        enable_lay.addWidget(_section("✨  Enable"))
        enable_lay.addWidget(_h_sep())

        self.sync_enable_cb = QCheckBox("Enable Window Synchronization")
        self.sync_enable_cb.setChecked(True)
        self.sync_enable_cb.setStyleSheet(self._checkbox_style())
        enable_lay.addWidget(self.sync_enable_cb)

        main_lay.addWidget(_card_wrapper(enable_lay))

        # Sync Settings Section
        sync_lay = QVBoxLayout()
        sync_lay.setSpacing(12)
        sync_lay.addWidget(_section("⚙️  Sync Settings"))
        sync_lay.addWidget(_h_sep())

        self.sync_mouse_cb = QCheckBox("Sync mouse movements")
        self.sync_mouse_cb.setStyleSheet(self._checkbox_style())
        sync_lay.addWidget(self.sync_mouse_cb)
        
        self.sync_keyboard_cb = QCheckBox("Sync keyboard input")
        self.sync_keyboard_cb.setStyleSheet(self._checkbox_style())
        sync_lay.addWidget(self.sync_keyboard_cb)
        
        self.sync_scroll_cb = QCheckBox("Sync scroll actions")
        self.sync_scroll_cb.setStyleSheet(self._checkbox_style())
        sync_lay.addWidget(self.sync_scroll_cb)
        
        self.sync_click_cb = QCheckBox("Sync clicks")
        self.sync_click_cb.setStyleSheet(self._checkbox_style())
        sync_lay.addWidget(self.sync_click_cb)
        
        self.sync_nav_cb = QCheckBox("Sync navigation (URL changes)")
        self.sync_nav_cb.setStyleSheet(self._checkbox_style())
        sync_lay.addWidget(self.sync_nav_cb)
        
        for cb in [self.sync_mouse_cb, self.sync_keyboard_cb, self.sync_scroll_cb,
                   self.sync_click_cb, self.sync_nav_cb]:
            cb.setChecked(True)

        main_lay.addWidget(_card_wrapper(sync_lay))

        # Layout & Performance Section
        perf_lay = QVBoxLayout()
        perf_lay.setSpacing(14)
        perf_lay.addWidget(_section("📐  Layout & Performance"))
        perf_lay.addWidget(_h_sep())

        self.layout_combo = QComboBox()
        self.layout_combo.setMinimumHeight(38)
        self.layout_combo.setStyleSheet(self._combo_style())
        for l in ["Grid (auto)", "2×2", "3×2", "4×2", "Custom"]:
            self.layout_combo.addItem(l)
        perf_lay.addLayout(_row("Layout Mode", self.layout_combo))

        self.leader_combo = QComboBox()
        self.leader_combo.setMinimumHeight(38)
        self.leader_combo.setStyleSheet(self._combo_style())
        self.leader_combo.addItem("First opened profile (default)")
        perf_lay.addLayout(_row("Leader Profile (source)", self.leader_combo))

        self.delay_spin = QSpinBox()
        self.delay_spin.setRange(0, 5000)
        self.delay_spin.setValue(50)
        self.delay_spin.setSuffix(" ms")
        self.delay_spin.setMinimumHeight(38)
        self.delay_spin.setStyleSheet(self._spinbox_style())
        perf_lay.addLayout(_row("Action broadcast delay", self.delay_spin))

        main_lay.addWidget(_card_wrapper(perf_lay))
        main_lay.addStretch()
        return w

    # ── Cloud ───────────────────────────────────────────────────────────────────
    def _cloud_tab(self):
        w = QWidget()
        w.setStyleSheet("background:#07090f;")
        main_lay = QVBoxLayout(w)
        main_lay.setContentsMargins(24, 24, 24, 24)
        main_lay.setSpacing(20)

        # Cloud Sync Status
        cloud_lay = QVBoxLayout()
        cloud_lay.setSpacing(14)
        cloud_lay.addWidget(_section("☁️  Cloud Sync Status"))
        cloud_lay.addWidget(_h_sep())

        self.cloud_enable_cb = QCheckBox("Enable Cloud Sync")
        self.cloud_enable_cb.setChecked(True)
        self.cloud_enable_cb.setStyleSheet(self._checkbox_style())
        cloud_lay.addWidget(self.cloud_enable_cb)

        # Usage bar
        usage_lay = QHBoxLayout()
        usage_lb = QLabel("Storage:")
        usage_lb.setMinimumWidth(100)
        usage_lb.setStyleSheet("color:#cbd5e1;font-size:13px;font-weight:500;")
        self.usage_bar = QProgressBar()
        self.usage_bar.setRange(0, 100)
        self.usage_bar.setValue(34)
        self.usage_bar.setFixedHeight(10)
        self.usage_bar.setFormat("")
        self.usage_bar.setStyleSheet("""
            QProgressBar {
                background:#1e2d45;
                border:none;
                border-radius:5px;
                text-align:center;
            }
            QProgressBar::chunk {
                background:qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #f97316, stop:1 #fb923c);
                border-radius:5px;
            }
        """)
        used_lb = QLabel("3.4 GB / 10 GB")
        used_lb.setStyleSheet("color:#64748b;font-size:12px;font-weight:500;")
        usage_lay.addWidget(usage_lb)
        usage_lay.addWidget(self.usage_bar, 1)
        usage_lay.addWidget(used_lb)
        cloud_lay.addLayout(usage_lay)

        main_lay.addWidget(_card_wrapper(cloud_lay))

        # Sync Options
        options_lay = QVBoxLayout()
        options_lay.setSpacing(14)
        options_lay.addWidget(_section("⚡  Sync Options"))
        options_lay.addWidget(_h_sep())

        self.sync_auto_cb = QCheckBox("Auto-sync every:")
        self.sync_auto_cb.setStyleSheet(self._checkbox_style())
        interval_lay = QHBoxLayout()
        self.sync_interval = QSpinBox()
        self.sync_interval.setRange(1, 60)
        self.sync_interval.setValue(5)
        self.sync_interval.setSuffix(" min")
        self.sync_interval.setMinimumHeight(38)
        self.sync_interval.setStyleSheet(self._spinbox_style())
        interval_lay.addWidget(self.sync_auto_cb)
        interval_lay.addWidget(self.sync_interval)
        interval_lay.addStretch()
        options_lay.addLayout(interval_lay)

        # Sync items
        items_lay = QVBoxLayout()
        items_lay.setSpacing(10)
        for label, checked in [
            ("Sync profile settings", True),
            ("Sync fingerprint configurations", True),
            ("Sync proxy settings", False),
            ("Sync platform accounts", False),
            ("Sync extensions list", True),
            ("Sync RPA tasks", True),
        ]:
            cb = QCheckBox(label)
            cb.setChecked(checked)
            cb.setStyleSheet(self._checkbox_style())
            items_lay.addWidget(cb)

        options_lay.addLayout(items_lay)
        main_lay.addWidget(_card_wrapper(options_lay))

        # Sync Now
        sync_now_btn = QPushButton("☁️  Sync Now")
        sync_now_btn.setFixedHeight(44)
        sync_now_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        sync_now_btn.setStyleSheet("""
            QPushButton {
                background:#f97316;
                color:#ffffff;
                border:none;
                border-radius:10px;
                font-size:13px;
                font-weight:700;
                letter-spacing:0.5px;
            }
            QPushButton:hover {
                background:#fb923c;
            }
            QPushButton:pressed {
                background:#c2410c;
            }
        """)
        sync_now_btn.clicked.connect(self._sync_now)
        main_lay.addWidget(sync_now_btn)

        self.sync_status_lb = QLabel("Last synced: 2024-01-15 09:00:00")
        self.sync_status_lb.setStyleSheet("color:#64748b;font-size:12px;text-align:center;padding:8px;")
        main_lay.addWidget(self.sync_status_lb)

        main_lay.addStretch()
        return w

    def _about_tab(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(14)

        # Large Logo
        from PyQt6.QtGui import QPixmap
        logo_lbl = QLabel()
        logo_path = get_asset_path("Logo.png")
        logo_pixmap = QPixmap(logo_path) if logo_path else QPixmap()
        if not logo_pixmap.isNull():
            scaled_logo = logo_pixmap.scaledToWidth(200)
            logo_lbl.setPixmap(scaled_logo)
            logo_lbl.setAlignment(0x0004 | 0x0020)  # Center | AlignHCenter
        logo_lbl.setStyleSheet("background:transparent;")
        lay.addWidget(logo_lbl)

        # Title
        title = QLabel("KH Browser Manager")
        title.setStyleSheet("font-size:20px;font-weight:700;color:#f97316;text-align:center;")
        title.setAlignment(0x0004 | 0x0020)  # Center
        lay.addWidget(title)

        # Subtitle
        subtitle = QLabel("Advanced Anti-Detection Browser")
        subtitle.setStyleSheet("font-size:13px;color:#94a3b8;text-align:center;")
        subtitle.setAlignment(0x0004 | 0x0020)  # Center
        lay.addWidget(subtitle)

        lay.addSpacing(10)

        # Version info
        version_gb = QGroupBox("Version Information")
        version_lay = QVBoxLayout(version_gb)
        version_lay.addWidget(QLabel("📦  Version: v2.0.2.6"))
        version_lay.addWidget(QLabel("📅  Last Updated: April 29, 2026"))
        lay.addWidget(version_gb)

        # Author info with Profile Image
        author_gb = QGroupBox("Creator Profile")
        author_lay = QVBoxLayout(author_gb)
        
        # Profile image
        from PyQt6.QtGui import QPixmap
        profile_img = QLabel()
        profile_path = get_asset_path("SOPHEARUNpng.png")
        profile_pixmap = QPixmap(profile_path) if profile_path else QPixmap()
        if not profile_pixmap.isNull():
            scaled_profile = profile_pixmap.scaledToHeight(120)
            profile_img.setPixmap(scaled_profile)
            profile_img.setAlignment(0x0004 | 0x0020)  # Center
        author_lay.addWidget(profile_img)
        
        # Name
        name_lbl = QLabel("SOPHEARUN")
        name_lbl.setStyleSheet("font-size:16px;font-weight:700;color:#f97316;text-align:center;")
        name_lbl.setAlignment(0x0004 | 0x0020)
        author_lay.addWidget(name_lbl)
        
        # Title
        title_lbl = QLabel("Creator & Developer")
        title_lbl.setStyleSheet("font-size:12px;color:#94a3b8;text-align:center;")
        title_lbl.setAlignment(0x0004 | 0x0020)
        author_lay.addWidget(title_lbl)
        
        # Facebook link
        fb_link = QLabel('<a href="https://web.facebook.com/Mr.SOPHEARUN" style="color:#f97316;text-decoration:none;font-weight:600;">🔗  Mr.SOPHEARUN on Facebook</a>')
        fb_link.setOpenExternalLinks(True)
        fb_link.setAlignment(0x0004 | 0x0020)
        author_lay.addWidget(fb_link)
        
        lay.addWidget(author_gb)

        # Features
        features_gb = QGroupBox("Features")
        features_lay = QVBoxLayout(features_gb)
        features = [
            "✅ Multi-profile Browser Management",
            "✅ Advanced Fingerprinting",
            "✅ Proxy Configuration",
            "✅ Batch Profile Creation",
            "✅ Cloud Sync Support",
            "✅ Real-time Dashboard",
        ]
        for feature in features:
            features_lay.addWidget(QLabel(feature))
        lay.addWidget(features_gb)

        lay.addStretch()
        return w

    # ── Styling Methods ────────────────────────────────────────────────────────
    def _combo_style(self):
        return """
            QComboBox {
                background:#0e1420; color:#cbd5e1;
                border:1px solid #1e2d45; border-radius:10px;
                padding:0 12px; font-size:12px; font-weight:500;
            }
            QComboBox:hover { border:1px solid #f9731660; }
            QComboBox:focus { border:2px solid #f97316; background:#0f1520; }
            QComboBox::drop-down { border:none; width:24px; }
            QComboBox QAbstractItemView {
                background:#0e1420; color:#e2e8f0;
                border:1px solid #1e2d45; border-radius:8px; padding:4px;
                selection-background-color:#1a2840;
            }
            QComboBox QAbstractItemView::item { padding:8px 12px; border-radius:6px; }
        """

    def _lineedit_style(self):
        return """
            QLineEdit {
                background:#0e1420; color:#e2e8f0;
                border:1px solid #1e2d45; border-radius:10px;
                padding:0 12px; font-size:13px;
            }
            QLineEdit:focus { border:2px solid #f97316; background:#0f1520; }
            QLineEdit:hover { border:1px solid #f9731660; }
            QLineEdit::placeholder { color:#334155; }
        """

    def _spinbox_style(self):
        return """
            QSpinBox {
                background:#0e1420; color:#cbd5e1;
                border:1px solid #1e2d45; border-radius:10px;
                padding:0 12px; font-size:12px;
            }
            QSpinBox:focus { border:2px solid #f97316; background:#0f1520; }
            QSpinBox::up-button, QSpinBox::down-button {
                background:#1e2d45; border:none; border-radius:4px; width:16px;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover { background:#f97316; }
        """

    def _checkbox_style(self):
        return """
            QCheckBox {
                spacing:10px; color:#cbd5e1; font-size:13px; font-weight:500;
            }
            QCheckBox::indicator {
                width:18px; height:18px; border-radius:6px;
                border:2px solid #1e2d45; background:#0e1420;
            }
            QCheckBox::indicator:checked {
                background:#f97316; border-color:#f97316;
            }
            QCheckBox::indicator:hover {
                border-color:#f9731660;
            }
        """

    def _secondary_btn_style(self):
        return """
            QPushButton {
                background:#1e2d45; color:#cbd5e1;
                border:1px solid #253555; border-radius:10px;
                padding:0 20px; font-size:13px; font-weight:600;
            }
            QPushButton:hover {
                background:#253555; color:#f1f5f9;
                border-color:#f9731660;
            }
            QPushButton:pressed {
                background:#1a2236;
            }
        """

    def _sync_now(self):
        self.sync_status_lb.setText("⏳  Syncing…")
        QTimer.singleShot(2000, lambda: self.sync_status_lb.setText(
            "✅  Last synced: just now"
        ))

    def _save(self):
        QMessageBox.information(self, "Settings", "✅  Settings saved successfully.")
        self.accept()

    def _reset(self):
        reply = QMessageBox.question(
            self, "Reset", "Reset all settings to default values?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "Reset", "✅  Settings reset to defaults.")
