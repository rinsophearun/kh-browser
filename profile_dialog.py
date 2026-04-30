"""Profile creation/editing dialog with all tabs."""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QLabel, QLineEdit, QComboBox, QCheckBox, QSpinBox, QDoubleSpinBox,
    QPushButton, QTextEdit, QGroupBox, QGridLayout, QRadioButton,
    QButtonGroup, QListWidget, QListWidgetItem, QScrollArea, QFrame,
    QFormLayout, QSizePolicy, QMessageBox, QSlider, QDialogButtonBox,
    QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView,
    QPlainTextEdit
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor
from models import BrowserProfile, Fingerprint, ProxyConfig, PlatformAccount


# ── Helpers ────────────────────────────────────────────────────────────────────

def _label(text, style="fieldLabel"):
    lb = QLabel(text)
    lb.setObjectName(style)
    return lb


def _h_sep():
    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    return line


def _row(label, widget, tip=""):
    hl = QHBoxLayout()
    lb = _label(label)
    lb.setMinimumWidth(160)
    hl.addWidget(lb)
    hl.addWidget(widget, 1)
    if tip:
        widget.setToolTip(tip)
    return hl


def _section(title):
    lb = QLabel(f"  {title}")
    lb.setObjectName("sectionTitle")
    lb.setStyleSheet("font-size:14px;font-weight:700;color:#e2e8f0;padding:6px 0 2px 0;")
    return lb


# ── Sub-tabs ───────────────────────────────────────────────────────────────────

class BasicTab(QWidget):
    def __init__(self, profile: BrowserProfile):
        super().__init__()
        self.profile = profile
        self._build()

    def _build(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        inner = QWidget()
        lay = QVBoxLayout(inner)
        lay.setSpacing(14)
        lay.setContentsMargins(20, 20, 20, 20)

        # Identity
        lay.addWidget(_section("Profile Identity"))
        lay.addWidget(_h_sep())

        self.name_edit = QLineEdit(self.profile.name)
        self.name_edit.setPlaceholderText("e.g. Facebook Account 1")
        lay.addLayout(_row("Profile Name *", self.name_edit))

        self.group_combo = QComboBox()
        self.group_combo.setEditable(True)
        for g in ["Default", "Facebook", "Social Media", "E-commerce", "B2B", "Content", "Testing"]:
            self.group_combo.addItem(g)
        self.group_combo.setCurrentText(self.profile.group)
        lay.addLayout(_row("Group", self.group_combo))

        self.tags_edit = QLineEdit(", ".join(self.profile.tags))
        self.tags_edit.setPlaceholderText("e.g. work, main, warmup  (comma separated)")
        lay.addLayout(_row("Tags", self.tags_edit))

        lay.addSpacing(10)
        lay.addWidget(_section("Browser & OS"))
        lay.addWidget(_h_sep())

        self.browser_combo = QComboBox()
        for b in ["Chrome", "Firefox", "Edge", "Safari", "Opera"]:
            self.browser_combo.addItem(b)
        self.browser_combo.setCurrentText(self.profile.browser_type)
        lay.addLayout(_row("Browser", self.browser_combo))

        self.version_edit = QLineEdit(self.profile.browser_version)
        self.version_edit.setPlaceholderText("120.0")
        lay.addLayout(_row("Browser Version", self.version_edit))

        self.os_combo = QComboBox()
        for o in ["Windows", "macOS", "Linux", "Android", "iOS"]:
            self.os_combo.addItem(o)
        self.os_combo.setCurrentText(self.profile.os_type)
        lay.addLayout(_row("Operating System", self.os_combo))

        self.os_ver_edit = QLineEdit(self.profile.os_version)
        self.os_ver_edit.setPlaceholderText("10 / 11 / 14.0")
        lay.addLayout(_row("OS Version", self.os_ver_edit))

        lay.addSpacing(10)
        lay.addWidget(_section("Startup"))
        lay.addWidget(_h_sep())

        self.url_edit = QLineEdit(self.profile.startup_url)
        self.url_edit.setPlaceholderText("https://example.com  (leave blank for new tab)")
        lay.addLayout(_row("Startup URL", self.url_edit))

        self.notes_edit = QTextEdit(self.profile.notes)
        self.notes_edit.setPlaceholderText("Notes…")
        self.notes_edit.setMaximumHeight(90)
        lay.addLayout(_row("Notes", self.notes_edit))

        lay.addStretch()
        scroll.setWidget(inner)
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.addWidget(scroll)

    def get_data(self):
        tags = [t.strip() for t in self.tags_edit.text().split(",") if t.strip()]
        return dict(
            name=self.name_edit.text().strip(),
            group=self.group_combo.currentText(),
            tags=tags,
            browser_type=self.browser_combo.currentText(),
            browser_version=self.version_edit.text().strip(),
            os_type=self.os_combo.currentText(),
            os_version=self.os_ver_edit.text().strip(),
            startup_url=self.url_edit.text().strip(),
            notes=self.notes_edit.toPlainText(),
        )


class FingerprintTab(QWidget):
    def __init__(self, profile: BrowserProfile):
        super().__init__()
        self.fp = profile.fingerprint
        self._build()

    def _build(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        inner = QWidget()
        lay = QVBoxLayout(inner)
        lay.setSpacing(12)
        lay.setContentsMargins(20, 20, 20, 20)

        # Random button
        rand_btn = QPushButton("⚡  Randomize All Fingerprints")
        rand_btn.setObjectName("primaryBtn")
        rand_btn.setFixedHeight(38)
        rand_btn.clicked.connect(self._randomize)
        lay.addWidget(rand_btn)

        lay.addWidget(_section("User Agent"))
        lay.addWidget(_h_sep())
        self.ua_edit = QLineEdit(self.fp.user_agent)
        lay.addLayout(_row("User Agent", self.ua_edit))

        lay.addSpacing(6)
        lay.addWidget(_section("Screen & Display"))
        lay.addWidget(_h_sep())

        self.sw_spin = QSpinBox()
        self.sw_spin.setRange(800, 7680)
        self.sw_spin.setValue(self.fp.screen_width)
        lay.addLayout(_row("Screen Width", self.sw_spin))

        self.sh_spin = QSpinBox()
        self.sh_spin.setRange(600, 4320)
        self.sh_spin.setValue(self.fp.screen_height)
        lay.addLayout(_row("Screen Height", self.sh_spin))

        self.cd_spin = QSpinBox()
        self.cd_spin.setRange(16, 32)
        self.cd_spin.setValue(self.fp.color_depth)
        lay.addLayout(_row("Color Depth", self.cd_spin))

        self.dpr_spin = QDoubleSpinBox()
        self.dpr_spin.setRange(1.0, 4.0)
        self.dpr_spin.setSingleStep(0.25)
        self.dpr_spin.setValue(self.fp.pixel_ratio)
        lay.addLayout(_row("Pixel Ratio (DPR)", self.dpr_spin))

        lay.addSpacing(6)
        lay.addWidget(_section("Hardware"))
        lay.addWidget(_h_sep())

        self.cpu_spin = QSpinBox()
        self.cpu_spin.setRange(1, 64)
        self.cpu_spin.setValue(self.fp.hardware_concurrency)
        lay.addLayout(_row("CPU Cores", self.cpu_spin))

        self.mem_combo = QComboBox()
        for m in ["1", "2", "4", "8", "16", "32", "64"]:
            self.mem_combo.addItem(m + " GB")
        self.mem_combo.setCurrentText(f"{self.fp.device_memory} GB")
        lay.addLayout(_row("Device Memory", self.mem_combo))

        self.platform_combo = QComboBox()
        for p in ["Win32", "Win64", "MacIntel", "Linux x86_64", "Linux armv8l"]:
            self.platform_combo.addItem(p)
        self.platform_combo.setCurrentText(self.fp.platform)
        lay.addLayout(_row("Platform", self.platform_combo))

        lay.addSpacing(6)
        lay.addWidget(_section("WebGL"))
        lay.addWidget(_h_sep())

        self.webgl_vendor_edit = QLineEdit(self.fp.webgl_vendor)
        lay.addLayout(_row("WebGL Vendor", self.webgl_vendor_edit))

        self.webgl_renderer_edit = QLineEdit(self.fp.webgl_renderer)
        lay.addLayout(_row("WebGL Renderer", self.webgl_renderer_edit))

        self.webgl_noise_cb = QCheckBox("Enable WebGL Noise")
        self.webgl_noise_cb.setChecked(self.fp.webgl_noise)
        lay.addWidget(self.webgl_noise_cb)

        lay.addSpacing(6)
        lay.addWidget(_section("Noise & Protection"))
        lay.addWidget(_h_sep())

        for attr, label in [
            ("canvas_noise_cb", "Canvas 2D Noise"),
            ("audio_noise_cb", "Audio Context Noise"),
            ("rect_noise_cb", "Client Rects Noise"),
            ("ports_cb", "Port Scan Protection"),
            ("dnt_cb", "Do Not Track"),
        ]:
            cb = QCheckBox(label)
            cb.setChecked(getattr(self.fp, {
                "canvas_noise_cb": "canvas_noise",
                "audio_noise_cb": "audio_noise",
                "rect_noise_cb": "client_rects_noise",
                "ports_cb": "ports_protection",
                "dnt_cb": "do_not_track",
            }[attr]))
            setattr(self, attr, cb)
            lay.addWidget(cb)

        lay.addSpacing(6)
        lay.addWidget(_section("WebRTC"))
        lay.addWidget(_h_sep())

        self.webrtc_combo = QComboBox()
        for m in ["disabled", "replaced", "real"]:
            self.webrtc_combo.addItem(m.capitalize())
        self.webrtc_combo.setCurrentText(self.fp.webrtc_mode.capitalize())
        lay.addLayout(_row("WebRTC Mode", self.webrtc_combo))

        lay.addStretch()
        scroll.setWidget(inner)
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.addWidget(scroll)

    def _randomize(self):
        import random
        screen_presets = [(1920, 1080), (2560, 1440), (1366, 768), (1440, 900), (1280, 800)]
        w, h = random.choice(screen_presets)
        self.sw_spin.setValue(w)
        self.sh_spin.setValue(h)
        self.cpu_spin.setValue(random.choice([2, 4, 6, 8, 12, 16]))
        self.dpr_spin.setValue(random.choice([1.0, 1.25, 1.5, 2.0]))

    def get_data(self):
        return dict(
            user_agent=self.ua_edit.text(),
            screen_width=self.sw_spin.value(),
            screen_height=self.sh_spin.value(),
            color_depth=self.cd_spin.value(),
            pixel_ratio=self.dpr_spin.value(),
            hardware_concurrency=self.cpu_spin.value(),
            webgl_vendor=self.webgl_vendor_edit.text(),
            webgl_renderer=self.webgl_renderer_edit.text(),
            webgl_noise=self.webgl_noise_cb.isChecked(),
            canvas_noise=self.canvas_noise_cb.isChecked(),
            audio_noise=self.audio_noise_cb.isChecked(),
            client_rects_noise=self.rect_noise_cb.isChecked(),
            ports_protection=self.ports_cb.isChecked(),
            do_not_track=self.dnt_cb.isChecked(),
            webrtc_mode=self.webrtc_combo.currentText().lower(),
        )


class ProxyTab(QWidget):
    def __init__(self, profile: BrowserProfile):
        super().__init__()
        self.proxy = profile.proxy
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(14)

        lay.addWidget(_section("Proxy Configuration"))
        lay.addWidget(_h_sep())

        self.type_combo = QComboBox()
        for t in ["None", "HTTP", "HTTPS", "SOCKS4", "SOCKS5"]:
            self.type_combo.addItem(t)
        self.type_combo.setCurrentText(self.proxy.type)
        self.type_combo.currentTextChanged.connect(self._toggle)
        lay.addLayout(_row("Proxy Type", self.type_combo))

        self.host_edit = QLineEdit(self.proxy.host)
        self.host_edit.setPlaceholderText("proxy.example.com  or  127.0.0.1")
        lay.addLayout(_row("Host / IP", self.host_edit))

        self.port_spin = QSpinBox()
        self.port_spin.setRange(0, 65535)
        self.port_spin.setValue(self.proxy.port or 8080)
        lay.addLayout(_row("Port", self.port_spin))

        self.user_edit = QLineEdit(self.proxy.username)
        self.user_edit.setPlaceholderText("Username (optional)")
        lay.addLayout(_row("Username", self.user_edit))

        self.pass_edit = QLineEdit(self.proxy.password)
        self.pass_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_edit.setPlaceholderText("Password (optional)")
        lay.addLayout(_row("Password", self.pass_edit))

        lay.addSpacing(8)
        lay.addWidget(_section("Rotation"))
        lay.addWidget(_h_sep())

        self.rot_edit = QLineEdit(self.proxy.rotation_url)
        self.rot_edit.setPlaceholderText("https://api.provider.com/rotate?token=xxx")
        lay.addLayout(_row("IP Rotation URL", self.rot_edit))

        # test btn
        hl = QHBoxLayout()
        self.test_btn = QPushButton("🔍  Test Proxy")
        self.test_btn.setObjectName("successBtn")
        self.test_btn.clicked.connect(self._test)
        self.result_label = QLabel()
        hl.addWidget(self.test_btn)
        hl.addWidget(self.result_label, 1)
        lay.addLayout(hl)

        lay.addStretch()
        self._toggle(self.type_combo.currentText())

    def _toggle(self, t):
        enabled = t != "None"
        for w in [self.host_edit, self.port_spin, self.user_edit, self.pass_edit, self.rot_edit]:
            w.setEnabled(enabled)

    def _test(self):
        self.result_label.setText("⏳  Testing…")
        self.result_label.setStyleSheet("color:#fcd34d")
        import random
        # Mock test result
        if self.host_edit.text():
            ip = f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
            country = random.choice(["US", "UK", "DE", "SG", "JP"])
            self.result_label.setText(f"✅  {ip}  |  {country}")
            self.result_label.setStyleSheet("color:#6ee7b7")
        else:
            self.result_label.setText("❌  No proxy configured")
            self.result_label.setStyleSheet("color:#fca5a5")

    def get_data(self):
        return ProxyConfig(
            type=self.type_combo.currentText(),
            host=self.host_edit.text(),
            port=self.port_spin.value(),
            username=self.user_edit.text(),
            password=self.pass_edit.text(),
            rotation_url=self.rot_edit.text(),
        )


class TimezoneTab(QWidget):
    def __init__(self, profile: BrowserProfile):
        super().__init__()
        self.fp = profile.fingerprint
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(14)

        lay.addWidget(_section("Timezone & Locale"))
        lay.addWidget(_h_sep())

        self.tz_combo = QComboBox()
        tzs = ["America/New_York", "America/Los_Angeles", "America/Chicago", "America/Denver",
               "Europe/London", "Europe/Paris", "Europe/Berlin", "Europe/Moscow",
               "Asia/Tokyo", "Asia/Shanghai", "Asia/Singapore", "Asia/Dubai",
               "Australia/Sydney", "Pacific/Auckland", "UTC"]
        for t in tzs:
            self.tz_combo.addItem(t)
        self.tz_combo.setCurrentText(self.fp.timezone)
        lay.addLayout(_row("Timezone", self.tz_combo))

        self.lang_combo = QComboBox()
        for l in ["en-US", "en-GB", "zh-CN", "ja-JP", "ko-KR", "fr-FR", "de-DE", "es-ES", "pt-BR", "ru-RU"]:
            self.lang_combo.addItem(l)
        self.lang_combo.setCurrentText(self.fp.language)
        lay.addLayout(_row("Language", self.lang_combo))

        self.langs_edit = QLineEdit(self.fp.languages)
        self.langs_edit.setPlaceholderText("en-US,en;q=0.9")
        lay.addLayout(_row("Accept-Language", self.langs_edit))

        lay.addSpacing(8)
        lay.addWidget(_section("Geolocation"))
        lay.addWidget(_h_sep())

        self.geo_combo = QComboBox()
        for m in ["based_on_ip", "custom", "disabled"]:
            self.geo_combo.addItem(m.replace("_", " ").title())
        lay.addLayout(_row("Geolocation Mode", self.geo_combo))

        self.lat_spin = QDoubleSpinBox()
        self.lat_spin.setRange(-90, 90)
        self.lat_spin.setDecimals(6)
        self.lat_spin.setValue(self.fp.latitude)
        lay.addLayout(_row("Latitude", self.lat_spin))

        self.lon_spin = QDoubleSpinBox()
        self.lon_spin.setRange(-180, 180)
        self.lon_spin.setDecimals(6)
        self.lon_spin.setValue(self.fp.longitude)
        lay.addLayout(_row("Longitude", self.lon_spin))

        lay.addStretch()

    def get_data(self):
        return dict(
            timezone=self.tz_combo.currentText(),
            language=self.lang_combo.currentText(),
            languages=self.langs_edit.text(),
            geolocation_mode=self.geo_combo.currentText().lower().replace(" ", "_"),
            latitude=self.lat_spin.value(),
            longitude=self.lon_spin.value(),
        )


class AccountsTab(QWidget):
    def __init__(self, profile: BrowserProfile):
        super().__init__()
        self.profile = profile
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(10)

        hl = QHBoxLayout()
        hl.addWidget(_label("Platform Accounts"))
        hl.addStretch()
        add_btn = QPushButton("+ Add Account")
        add_btn.setObjectName("primaryBtn")
        add_btn.setFixedHeight(32)
        add_btn.clicked.connect(self._add)
        hl.addWidget(add_btn)
        lay.addLayout(hl)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Platform", "Username", "Password", "Notes", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
        self.table.verticalHeader().setVisible(False)
        lay.addWidget(self.table)

        for acc in self.profile.accounts:
            self._add_row(acc)

    def _add_row(self, acc: PlatformAccount = None):
        r = self.table.rowCount()
        self.table.insertRow(r)
        plat = QComboBox()
        for p in ["Facebook", "Instagram", "Twitter", "TikTok", "YouTube", "LinkedIn",
                  "Amazon", "Shopify", "eBay", "Reddit", "Pinterest", "Custom"]:
            plat.addItem(p)
        if acc and acc.platform:
            plat.setCurrentText(acc.platform)
        self.table.setCellWidget(r, 0, plat)
        self.table.setItem(r, 1, QTableWidgetItem(acc.username if acc else ""))
        pw_item = QTableWidgetItem(acc.password if acc else "")
        self.table.setItem(r, 2, pw_item)
        self.table.setItem(r, 3, QTableWidgetItem(acc.notes if acc else ""))
        del_btn = QPushButton("🗑")
        del_btn.setObjectName("iconBtn")
        del_btn.clicked.connect(lambda _, row=r: self.table.removeRow(row))
        self.table.setCellWidget(r, 4, del_btn)

    def _add(self):
        self._add_row()

    def get_data(self):
        accs = []
        for r in range(self.table.rowCount()):
            plat_w = self.table.cellWidget(r, 0)
            accs.append(PlatformAccount(
                platform=plat_w.currentText() if plat_w else "",
                username=self.table.item(r, 1).text() if self.table.item(r, 1) else "",
                password=self.table.item(r, 2).text() if self.table.item(r, 2) else "",
                notes=self.table.item(r, 3).text() if self.table.item(r, 3) else "",
            ))
        return accs


class ExtensionsTab(QWidget):
    def __init__(self, profile: BrowserProfile):
        super().__init__()
        self.profile = profile
        self._build()

    COMMON_EXT = [
        ("uBlock Origin", "uBlock0@raymondhill.net"),
        ("Privacy Badger", "jid1-MnnxcxisBPnSXQ@jetpack"),
        ("Grammarly", "87677a2c52b84ad3a151a4a72f5bd3c4@jetpack"),
        ("LastPass", "support@lastpass.com"),
        ("NordVPN", "nordvpn@example.com"),
        ("AdGuard", "adguard@adguard.com"),
        ("Dark Reader", "addon@darkreader.org"),
        ("Honey", "id@joinhoney.com"),
        ("Tampermonkey", "tampermonkey@gmail.com"),
        ("EditThisCookie", "edit-this-cookie@edit-this-cookie.com"),
    ]

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(12)

        lay.addWidget(_label("Enabled Extensions"))

        self.list_widget = QListWidget()
        for name, ext_id in self.COMMON_EXT:
            item = QListWidgetItem(f"  {name}")
            item.setData(Qt.ItemDataRole.UserRole, ext_id)
            item.setCheckState(
                Qt.CheckState.Checked if ext_id in self.profile.extensions
                else Qt.CheckState.Unchecked
            )
            self.list_widget.addItem(item)
        lay.addWidget(self.list_widget)

        lay.addWidget(_section("Custom Extension"))
        lay.addWidget(_h_sep())
        hl = QHBoxLayout()
        self.custom_edit = QLineEdit()
        self.custom_edit.setPlaceholderText("Extension ID or path")
        add_btn = QPushButton("Add")
        add_btn.setObjectName("primaryBtn")
        add_btn.clicked.connect(self._add_custom)
        hl.addWidget(self.custom_edit, 1)
        hl.addWidget(add_btn)
        lay.addLayout(hl)

        lay.addStretch()

    def _add_custom(self):
        text = self.custom_edit.text().strip()
        if text:
            item = QListWidgetItem(f"  {text}")
            item.setData(Qt.ItemDataRole.UserRole, text)
            item.setCheckState(Qt.CheckState.Checked)
            self.list_widget.addItem(item)
            self.custom_edit.clear()

    def get_data(self):
        result = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                result.append(item.data(Qt.ItemDataRole.UserRole))
        return result


class SettingsTab(QWidget):
    """Profile-specific layout and sidebar settings."""
    def __init__(self, profile: BrowserProfile):
        super().__init__()
        self.profile = profile
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(16)

        lay.addWidget(_label("Sidebar Settings"))
        lay.addWidget(_h_sep())
        
        self.sidebar_visible = QCheckBox("Show sidebar by default")
        self.sidebar_visible.setChecked(getattr(self.profile, 'sidebar_visible', True))
        lay.addWidget(self.sidebar_visible)

        sb_width_lay = QHBoxLayout()
        sb_width_lay.addWidget(QLabel("Sidebar width (px):"))
        self.sidebar_width = QSpinBox()
        self.sidebar_width.setMinimum(150)
        self.sidebar_width.setMaximum(500)
        self.sidebar_width.setValue(getattr(self.profile, 'sidebar_width', 220))
        sb_width_lay.addWidget(self.sidebar_width)
        sb_width_lay.addStretch()
        lay.addLayout(sb_width_lay)

        lay.addWidget(_h_sep())
        lay.addWidget(_label("Layout Settings"))
        lay.addWidget(_h_sep())

        self.compact_mode = QCheckBox("Compact mode (smaller spacing)")
        self.compact_mode.setChecked(getattr(self.profile, 'compact_mode', False))
        lay.addWidget(self.compact_mode)

        self.dark_mode = QCheckBox("Dark theme")
        self.dark_mode.setChecked(getattr(self.profile, 'dark_mode', True))
        lay.addWidget(self.dark_mode)

        font_size_lay = QHBoxLayout()
        font_size_lay.addWidget(QLabel("Default font size:"))
        self.font_size = QSpinBox()
        self.font_size.setMinimum(10)
        self.font_size.setMaximum(20)
        self.font_size.setValue(getattr(self.profile, 'font_size', 13))
        font_size_lay.addWidget(self.font_size)
        font_size_lay.addStretch()
        lay.addLayout(font_size_lay)

        lay.addWidget(_h_sep())
        lay.addWidget(_label("Real-time Settings"))
        lay.addWidget(_h_sep())

        self.realtime_sync = QCheckBox("Enable real-time settings sync")
        self.realtime_sync.setChecked(getattr(self.profile, 'realtime_sync', True))
        lay.addWidget(self.realtime_sync)

        self.auto_refresh = QCheckBox("Auto-refresh profile list")
        self.auto_refresh.setChecked(getattr(self.profile, 'auto_refresh', True))
        lay.addWidget(self.auto_refresh)

        lay.addStretch()

    def get_data(self):
        """Return settings as dict."""
        return {
            'sidebar_visible': self.sidebar_visible.isChecked(),
            'sidebar_width': self.sidebar_width.value(),
            'compact_mode': self.compact_mode.isChecked(),
            'dark_mode': self.dark_mode.isChecked(),
            'font_size': self.font_size.value(),
            'realtime_sync': self.realtime_sync.isChecked(),
            'auto_refresh': self.auto_refresh.isChecked(),
        }


# ── Main Dialog ────────────────────────────────────────────────────────────────

class ProfileDialog(QDialog):
    profile_saved = pyqtSignal(object)

    def __init__(self, parent=None, profile: BrowserProfile = None):
        super().__init__(parent)
        self.profile = profile or BrowserProfile()
        self.is_new = profile is None
        self._build()
        self.setMinimumSize(780, 640)
        self.setWindowTitle("New Profile" if self.is_new else f"Edit: {self.profile.name}")

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Header
        header = QWidget()
        header.setStyleSheet("background:#111827;border-bottom:1px solid #1e2433;")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(20, 14, 20, 14)
        title = QLabel("✨  New Profile" if self.is_new else f"✏️  Edit Profile")
        title.setStyleSheet("font-size:16px;font-weight:700;color:#e2e8f0;")
        pid = QLabel(f"ID: {self.profile.id}")
        pid.setStyleSheet("color:#4b5568;font-size:12px;")
        hl.addWidget(title)
        hl.addStretch()
        hl.addWidget(pid)
        root.addWidget(header)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        self.basic_tab = BasicTab(self.profile)
        self.fp_tab = FingerprintTab(self.profile)
        self.proxy_tab = ProxyTab(self.profile)
        self.tz_tab = TimezoneTab(self.profile)
        self.accts_tab = AccountsTab(self.profile)
        self.ext_tab = ExtensionsTab(self.profile)
        self.settings_tab = SettingsTab(self.profile)

        self.tabs.addTab(self.basic_tab, "📋  Basic")
        self.tabs.addTab(self.fp_tab, "🔬  Fingerprint")
        self.tabs.addTab(self.proxy_tab, "🌐  Proxy")
        self.tabs.addTab(self.tz_tab, "🕒  Timezone")
        self.tabs.addTab(self.accts_tab, "👤  Accounts")
        self.tabs.addTab(self.ext_tab, "🧩  Extensions")
        self.tabs.addTab(self.settings_tab, "⚙️  Settings")

        root.addWidget(self.tabs, 1)

        # Footer
        footer = QWidget()
        footer.setStyleSheet("background:#111827;border-top:1px solid #1e2433;")
        fl = QHBoxLayout(footer)
        fl.setContentsMargins(20, 12, 20, 12)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        save_btn = QPushButton("💾  Save Profile")
        save_btn.setObjectName("primaryBtn")
        save_btn.setFixedHeight(38)
        save_btn.clicked.connect(self._save)
        fl.addStretch()
        fl.addWidget(cancel_btn)
        fl.addSpacing(8)
        fl.addWidget(save_btn)
        root.addWidget(footer)

    def _save(self):
        basic = self.basic_tab.get_data()
        if not basic["name"]:
            QMessageBox.warning(self, "Validation Error", "❌  Profile name is required.")
            return

        # Create temporary profile with collected data for validation
        temp_profile = BrowserProfile(**basic)
        temp_profile.fingerprint = Fingerprint(**self.fp_tab.get_data())
        
        tz_data = self.tz_tab.get_data()
        for k, v in tz_data.items():
            setattr(temp_profile.fingerprint, k, v)
        
        temp_profile.proxy = self.proxy_tab.get_data()
        temp_profile.accounts = self.accts_tab.get_data()
        temp_profile.extensions = self.ext_tab.get_data()

        # Validate profile against all rules
        is_valid, error_msg = temp_profile.validate()
        if not is_valid:
            QMessageBox.warning(self, "Validation Error", f"❌  {error_msg}")
            return

        # Apply validated data to actual profile
        for k, v in basic.items():
            setattr(self.profile, k, v)

        fp_data = self.fp_tab.get_data()
        for k, v in fp_data.items():
            setattr(self.profile.fingerprint, k, v)

        tz_data = self.tz_tab.get_data()
        for k, v in tz_data.items():
            setattr(self.profile.fingerprint, k, v)

        self.profile.proxy = self.proxy_tab.get_data()
        self.profile.accounts = self.accts_tab.get_data()
        self.profile.extensions = self.ext_tab.get_data()

        settings_data = self.settings_tab.get_data()
        for k, v in settings_data.items():
            setattr(self.profile, k, v)

        QMessageBox.information(self, "Success", "✅  Profile saved successfully with all validation rules passed.")
        self.profile_saved.emit(self.profile)
        self.accept()
