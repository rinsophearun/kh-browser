"""Settings dialog (Global, Personal, Window Sync, Cloud Sync)."""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget,
    QTabWidget, QGroupBox, QComboBox, QCheckBox, QSpinBox, QLineEdit,
    QFrame, QSlider, QRadioButton, QProgressBar, QMessageBox,
    QDialogButtonBox, QSizePolicy, QFormLayout
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont


def _h_sep():
    f = QFrame()
    f.setFrameShape(QFrame.Shape.HLine)
    return f


def _row(label, widget):
    hl = QHBoxLayout()
    lb = QLabel(label)
    lb.setMinimumWidth(220)
    lb.setStyleSheet("color:#94a3b8;font-size:12px;font-weight:600;")
    hl.addWidget(lb)
    hl.addWidget(widget, 1)
    return hl


def _section(text):
    lb = QLabel(text)
    lb.setStyleSheet("font-size:13px;font-weight:700;color:#e2e8f0;padding:6px 0 2px 0;")
    return lb


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setMinimumSize(740, 580)
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        header = QWidget()
        header.setStyleSheet("background:#111827;border-bottom:1px solid #1e2433;")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(20, 14, 20, 14)
        title = QLabel("⚙️  Settings")
        title.setStyleSheet("font-size:16px;font-weight:700;color:#e2e8f0;")
        hl.addWidget(title)
        root.addWidget(header)

        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        tabs.addTab(self._global_tab(), "🌐  Global")
        tabs.addTab(self._personal_tab(), "👤  Personal")
        tabs.addTab(self._window_sync_tab(), "🪟  Window Sync")
        tabs.addTab(self._cloud_tab(), "☁️  Cloud Sync")
        root.addWidget(tabs, 1)

        footer = QWidget()
        footer.setStyleSheet("background:#111827;border-top:1px solid #1e2433;")
        fl = QHBoxLayout(footer)
        fl.setContentsMargins(20, 12, 20, 12)
        reset_btn = QPushButton("Reset to Defaults")
        reset_btn.clicked.connect(self._reset)
        save_btn = QPushButton("💾  Save Settings")
        save_btn.setObjectName("primaryBtn")
        save_btn.setFixedHeight(38)
        save_btn.clicked.connect(self._save)
        fl.addWidget(reset_btn)
        fl.addStretch()
        fl.addWidget(save_btn)
        root.addWidget(footer)

    # ── Global ──────────────────────────────────────────────────────────────────
    def _global_tab(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(24, 20, 24, 20)
        lay.setSpacing(12)

        lay.addWidget(_section("Application"))
        lay.addWidget(_h_sep())

        self.lang_combo = QComboBox()
        for l in ["English", "Chinese (Simplified)", "Chinese (Traditional)", "Japanese",
                  "Korean", "Russian", "Spanish", "Portuguese", "Vietnamese"]:
            self.lang_combo.addItem(l)
        lay.addLayout(_row("Interface Language", self.lang_combo))

        self.theme_combo = QComboBox()
        for t in ["Dark (Default)", "Light", "System Auto"]:
            self.theme_combo.addItem(t)
        lay.addLayout(_row("UI Theme", self.theme_combo))

        self.start_min_cb = QCheckBox("Start minimized to system tray")
        lay.addWidget(self.start_min_cb)

        self.autostart_cb = QCheckBox("Launch at system startup")
        lay.addWidget(self.autostart_cb)

        self.update_cb = QCheckBox("Check for updates automatically")
        self.update_cb.setChecked(True)
        lay.addWidget(self.update_cb)

        lay.addSpacing(10)
        lay.addWidget(_section("Browser Engine"))
        lay.addWidget(_h_sep())

        self.engine_combo = QComboBox()
        for e in ["Chromium 120", "Chromium 119", "Firefox 120", "Firefox 118"]:
            self.engine_combo.addItem(e)
        lay.addLayout(_row("Default Browser Engine", self.engine_combo))

        self.cache_combo = QComboBox()
        for c in ["Per Profile (Isolated)", "Shared Cache", "No Cache"]:
            self.cache_combo.addItem(c)
        lay.addLayout(_row("Cache Mode", self.cache_combo))

        self.max_open_spin = QSpinBox()
        self.max_open_spin.setRange(1, 200)
        self.max_open_spin.setValue(20)
        lay.addLayout(_row("Max Open Profiles", self.max_open_spin))

        lay.addSpacing(10)
        lay.addWidget(_section("Security"))
        lay.addWidget(_h_sep())

        self.encrypt_cb = QCheckBox("Encrypt profile data at rest")
        self.encrypt_cb.setChecked(True)
        lay.addWidget(self.encrypt_cb)

        self.lock_timeout_spin = QSpinBox()
        self.lock_timeout_spin.setRange(0, 120)
        self.lock_timeout_spin.setValue(30)
        self.lock_timeout_spin.setSuffix(" min")
        lay.addLayout(_row("Auto-lock timeout (0 = disabled)", self.lock_timeout_spin))

        self.master_pw_cb = QCheckBox("Require master password on startup")
        lay.addWidget(self.master_pw_cb)

        lay.addStretch()
        return w

    # ── Personal ────────────────────────────────────────────────────────────────
    def _personal_tab(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(24, 20, 24, 20)
        lay.setSpacing(12)

        lay.addWidget(_section("Profile"))
        lay.addWidget(_h_sep())

        self.display_name = QLineEdit("John Smith")
        lay.addLayout(_row("Display Name", self.display_name))

        self.email_edit = QLineEdit("john@company.com")
        self.email_edit.setReadOnly(True)
        lay.addLayout(_row("Email (read-only)", self.email_edit))

        ch_pw = QPushButton("Change Password")
        ch_pw.setFixedWidth(160)
        ch_pw.clicked.connect(lambda: QMessageBox.information(self, "Password", "Password change email sent."))
        lay.addLayout(_row("Password", ch_pw))

        lay.addSpacing(10)
        lay.addWidget(_section("Notifications"))
        lay.addWidget(_h_sep())

        for label in ["Task completed", "Task failed", "Profile sync error",
                      "Team member joined", "Profile shared with me", "API quota warning"]:
            cb = QCheckBox(label)
            cb.setChecked(True)
            lay.addWidget(cb)

        lay.addSpacing(10)
        lay.addWidget(_section("Display Preferences"))
        lay.addWidget(_h_sep())

        self.table_density = QComboBox()
        for d in ["Compact", "Normal", "Comfortable"]:
            self.table_density.addItem(d)
        self.table_density.setCurrentText("Normal")
        lay.addLayout(_row("Table Density", self.table_density))

        self.date_format = QComboBox()
        for f in ["YYYY-MM-DD", "MM/DD/YYYY", "DD/MM/YYYY"]:
            self.date_format.addItem(f)
        lay.addLayout(_row("Date Format", self.date_format))

        self.default_group = QComboBox()
        for g in ["Default", "Facebook", "E-commerce", "Social Media"]:
            self.default_group.addItem(g)
        lay.addLayout(_row("Default Group for New Profiles", self.default_group))

        lay.addStretch()
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
