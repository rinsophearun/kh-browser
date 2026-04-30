"""Team Management — premium orange UI, clean rewrite."""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget,
    QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView,
    QAbstractItemView, QLineEdit, QComboBox, QGroupBox,
    QMessageBox, QFormLayout, QDialogButtonBox, QCheckBox, QFrame,
    QScrollArea, QSizePolicy,
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QColor, QFont
from models import TeamMember, SAMPLE_MEMBERS


# ── Shared helpers ──────────────────────────────────────────────────────────────

ROLE_COLORS = {
    "Owner":  ("#fbbf24", "#451a03"),
    "Admin":  ("#34d399", "#064e3b"),
    "Member": ("#94a3b8", "#1e2d45"),
    "Viewer": ("#64748b", "#0f172a"),
}
STATUS_COLORS = {
    "Active":    ("#22c55e", "#052e16"),
    "Invited":   ("#f59e0b", "#451a03"),
    "Suspended": ("#ef4444", "#450a0a"),
    "Inactive":  ("#64748b", "#0f172a"),
}


def _badge(text, fg, bg):
    lb = QLabel(text)
    lb.setAlignment(Qt.AlignmentFlag.AlignCenter)
    lb.setStyleSheet(f"""
        QLabel {{
            color: {fg}; background: {bg};
            border-radius: 6px; padding: 2px 10px;
            font-size: 11px; font-weight: 700;
        }}
    """)
    return lb


def _action_btn(label, fg="#94a3b8", bg="#111827", hover="#1e2d45", w=64, h=30):
    b = QPushButton(label)
    b.setFixedSize(w, h)
    b.setStyleSheet(f"""
        QPushButton {{
            background: {bg}; color: {fg};
            border: 1px solid #1e2d45; border-radius: 8px;
            font-size: 11px; font-weight: 600;
        }}
        QPushButton:hover {{ background: {hover}; border-color: {fg}; }}
    """)
    return b


def _section_header(title, subtitle=""):
    w = QWidget()
    w.setStyleSheet("background: transparent;")
    lay = QVBoxLayout(w)
    lay.setContentsMargins(0, 0, 0, 12)
    lay.setSpacing(2)
    t = QLabel(title)
    t.setStyleSheet("color:#f1f5f9; font-size:16px; font-weight:700;")
    lay.addWidget(t)
    if subtitle:
        s = QLabel(subtitle)
        s.setStyleSheet("color:#475569; font-size:12px;")
        lay.addWidget(s)
    sep = QFrame()
    sep.setFrameShape(QFrame.Shape.HLine)
    sep.setStyleSheet("background:#1a2236; border:none; min-height:1px; max-height:1px;")
    lay.addWidget(sep)
    return w


def _stat_chip(value, label, color="#f97316"):
    w = QWidget()
    w.setFixedSize(100, 58)
    w.setStyleSheet(f"""
        QWidget {{
            background: {color}18;
            border: 1px solid {color}40;
            border-radius: 10px;
        }}
    """)
    lay = QVBoxLayout(w)
    lay.setContentsMargins(10, 6, 10, 6)
    lay.setSpacing(0)
    v = QLabel(str(value))
    v.setAlignment(Qt.AlignmentFlag.AlignCenter)
    v.setStyleSheet(f"color:{color}; font-size:20px; font-weight:800;")
    l = QLabel(label)
    l.setAlignment(Qt.AlignmentFlag.AlignCenter)
    l.setStyleSheet("color:#475569; font-size:10px;")
    lay.addWidget(v)
    lay.addWidget(l)
    return w


def _styled_table(col_labels, stretch_col=None):
    t = QTableWidget(0, len(col_labels))
    t.setHorizontalHeaderLabels(col_labels)
    t.verticalHeader().setVisible(False)
    t.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    t.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    t.setAlternatingRowColors(True)
    t.setShowGrid(False)
    hh = t.horizontalHeader()
    hh.setVisible(True)
    hh.setMinimumSectionSize(30)
    if stretch_col is not None:
        hh.setSectionResizeMode(stretch_col, QHeaderView.ResizeMode.Stretch)
    t.setStyleSheet("""
        QTableWidget {
            background: #080c12;
            alternate-background-color: #0a1018;
            border: none; gridline-color: transparent;
            font-size: 13px; color: #e2e8f0;
        }
        QTableWidget::item { padding: 4px 8px; border: none; }
        QTableWidget::item:selected { background: #1e2d45; color: #f1f5f9; }
        QHeaderView::section {
            background: #0d1117; color: #475569;
            font-size: 10px; font-weight: 700;
            padding: 10px 8px; border: none;
            border-bottom: 1px solid #1a2236;
            border-right: 1px solid #1a2236;
        }
        QHeaderView::section:hover { color: #f97316; }
        QScrollBar:vertical {
            background: #0d1117; width: 5px; border-radius: 3px;
        }
        QScrollBar::handle:vertical { background: #f97316; border-radius: 3px; }
    """)
    return t


# ── Invite Dialog ───────────────────────────────────────────────────────────────

class InviteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Invite Team Member")
        self.setFixedSize(460, 320)
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 28, 28, 28)
        lay.setSpacing(16)

        # Header
        hdr = QLabel("📧  Invite New Member")
        hdr.setStyleSheet("font-size:16px; font-weight:700; color:#f1f5f9;")
        lay.addWidget(hdr)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background:#1a2236; border:none; min-height:1px;")
        lay.addWidget(sep)

        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("name@company.com")
        self.email_edit.setFixedHeight(38)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Full name")
        self.name_edit.setFixedHeight(38)

        self.role_combo = QComboBox()
        self.role_combo.setFixedHeight(38)
        for r in ["Admin", "Member", "Viewer"]:
            self.role_combo.addItem(r)
        self.role_combo.setCurrentText("Member")

        self.limit_combo = QComboBox()
        self.limit_combo.setFixedHeight(38)
        for v in ["50", "100", "200", "500", "Unlimited"]:
            self.limit_combo.addItem(v)
        self.limit_combo.setCurrentText("100")

        form.addRow("Email *", self.email_edit)
        form.addRow("Name", self.name_edit)
        form.addRow("Role", self.role_combo)
        form.addRow("Max Profiles", self.limit_combo)
        lay.addLayout(form)

        btns = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        btns.accepted.connect(self._validate)
        btns.rejected.connect(self.reject)
        ok = btns.button(QDialogButtonBox.StandardButton.Ok)
        ok.setText("Send Invitation")
        ok.setStyleSheet("""
            QPushButton {
                background: #f97316; color: white;
                border: none; border-radius: 10px;
                padding: 8px 24px; font-weight: 700;
            }
            QPushButton:hover { background: #ea6c10; }
        """)
        lay.addStretch()
        lay.addWidget(btns)

    def _validate(self):
        if not self.email_edit.text().strip():
            QMessageBox.warning(self, "Validation", "Email is required.")
            return
        self.accept()


# ── Share Profile Dialog ────────────────────────────────────────────────────────

class ShareProfileDialog(QDialog):
    def __init__(self, parent=None, profiles=None, members=None):
        super().__init__(parent)
        self.profiles = profiles or []
        self.members  = members  or []
        self.setWindowTitle("Share Profile")
        self.setMinimumSize(520, 400)
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 28, 28, 28)
        lay.setSpacing(14)

        hdr = QLabel("🔗  Share Profile with Team Members")
        hdr.setStyleSheet("font-size:15px; font-weight:700; color:#f1f5f9;")
        lay.addWidget(hdr)

        if self.profiles:
            names = ", ".join(p.name for p in self.profiles[:3])
            if len(self.profiles) > 3:
                names += f"  +{len(self.profiles) - 3} more"
            info = QLabel(f"Sharing:  {names}")
            info.setStyleSheet(
                "color:#f97316; font-size:12px; background:#1e140800;"
                "border:1px solid #f9731640; border-radius:6px; padding:6px 12px;"
            )
            lay.addWidget(info)

        sub = QLabel("Select members to share with:")
        sub.setStyleSheet("color:#64748b; font-size:12px;")
        lay.addWidget(sub)

        tbl = _styled_table(["", "Member", "Role"], stretch_col=1)
        tbl.setColumnWidth(0, 40)
        tbl.setColumnWidth(2, 100)
        self._share_checks = []
        for i, m in enumerate(self.members):
            tbl.insertRow(i)
            tbl.setRowHeight(i, 42)
            cb_w = QWidget()
            cb_w.setStyleSheet("background:transparent;")
            cb_l = QHBoxLayout(cb_w)
            cb_l.setContentsMargins(8, 0, 0, 0)
            cb = QCheckBox()
            self._share_checks.append(cb)
            cb_l.addWidget(cb)
            tbl.setCellWidget(i, 0, cb_w)
            tbl.setItem(i, 1, QTableWidgetItem(f"{m.name}  ({m.email})"))
            fg, bg = ROLE_COLORS.get(m.role, ("#94a3b8", "#1e2d45"))
            role_w = QWidget()
            role_w.setStyleSheet("background:transparent;")
            rl = QHBoxLayout(role_w)
            rl.setContentsMargins(4, 4, 4, 4)
            rl.addWidget(_badge(m.role, fg, bg))
            rl.addStretch()
            tbl.setCellWidget(i, 2, role_w)
        lay.addWidget(tbl)

        # Permissions
        perm_gb = QGroupBox("Permissions")
        pl = QHBoxLayout(perm_gb)
        pl.setSpacing(16)
        self.perm_view  = QCheckBox("View")
        self.perm_open  = QCheckBox("Open / Launch")
        self.perm_edit  = QCheckBox("Edit")
        for cb in [self.perm_view, self.perm_open, self.perm_edit]:
            cb.setChecked(True)
            pl.addWidget(cb)
        pl.addStretch()
        lay.addWidget(perm_gb)

        btns = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        btns.button(QDialogButtonBox.StandardButton.Ok).setText("Share")
        btns.button(QDialogButtonBox.StandardButton.Ok).setStyleSheet("""
            QPushButton {
                background: #f97316; color: white; border: none;
                border-radius: 10px; padding: 8px 24px; font-weight: 700;
            }
            QPushButton:hover { background: #ea6c10; }
        """)
        lay.addWidget(btns)


# ── Transfer Profile Dialog ─────────────────────────────────────────────────────

class TransferDialog(QDialog):
    def __init__(self, parent=None, profiles=None, members=None):
        super().__init__(parent)
        self.profiles = profiles or []
        self.members  = members  or []
        self.setWindowTitle("Transfer Profile")
        self.setFixedSize(460, 300)
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 28, 28, 28)
        lay.setSpacing(14)

        hdr = QLabel("🔄  Transfer Profile Ownership")
        hdr.setStyleSheet("font-size:15px; font-weight:700; color:#f1f5f9;")
        lay.addWidget(hdr)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background:#1a2236; border:none; min-height:1px;")
        lay.addWidget(sep)

        sub = QLabel("Transfer to:")
        sub.setStyleSheet("color:#94a3b8; font-size:12px;")
        lay.addWidget(sub)

        self.target_combo = QComboBox()
        self.target_combo.setFixedHeight(40)
        for m in self.members:
            self.target_combo.addItem(f"{m.name}  ·  {m.role}  ({m.email})")
        lay.addWidget(self.target_combo)

        warn = QLabel(
            "⚠️  The recipient becomes the new owner of the selected profiles.\n"
            "This action cannot be undone."
        )
        warn.setStyleSheet(
            "color:#fcd34d; font-size:12px; background:#451a0380;"
            "border:1px solid #f59e0b40; border-radius:8px; padding:12px 16px;"
        )
        warn.setWordWrap(True)
        lay.addWidget(warn)

        lay.addStretch()

        btns = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        btns.button(QDialogButtonBox.StandardButton.Ok).setText("Transfer Now")
        btns.button(QDialogButtonBox.StandardButton.Ok).setStyleSheet("""
            QPushButton {
                background: #ef4444; color: white; border: none;
                border-radius: 10px; padding: 8px 24px; font-weight: 700;
            }
            QPushButton:hover { background: #dc2626; }
        """)
        lay.addWidget(btns)


# ── Main Team Dialog ────────────────────────────────────────────────────────────

class TeamDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.members = list(SAMPLE_MEMBERS)
        self.setWindowTitle("Team Management")
        self.setMinimumSize(960, 640)
        self._build()

    # ── Shell ───────────────────────────────────────────────────────────────────
    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._make_header())

        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        tabs.addTab(self._tab_members(),     "👤  Members")
        tabs.addTab(self._tab_roles(),       "🔑  Roles & Permissions")
        tabs.addTab(self._tab_devices(),     "💻  Devices")
        tabs.addTab(self._tab_transfer(),    "👑  Transfer BOSS")
        root.addWidget(tabs, 1)

    def _make_header(self):
        hdr = QWidget()
        hdr.setFixedHeight(66)
        hdr.setStyleSheet("""
            background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
                stop:0 #0d1117, stop:1 #080c12);
            border-bottom: 1px solid #1a2236;
        """)
        hl = QHBoxLayout(hdr)
        hl.setContentsMargins(24, 0, 24, 0)
        hl.setSpacing(12)

        icon = QLabel("👥")
        icon.setStyleSheet("font-size:22px;")

        info = QVBoxLayout()
        info.setSpacing(1)
        t = QLabel("Team Management")
        t.setStyleSheet("font-size:16px; font-weight:800; color:#f1f5f9;")
        s = QLabel(f"{len(self.members)} members  ·  Pro Plan")
        s.setStyleSheet("font-size:11px; color:#475569;")
        info.addWidget(t)
        info.addWidget(s)

        invite_btn = QPushButton("＋  Invite Member")
        invite_btn.setFixedHeight(38)
        invite_btn.setStyleSheet("""
            QPushButton {
                background: #f97316; color: white;
                border: none; border-radius: 10px;
                padding: 0 20px; font-size: 13px; font-weight: 700;
            }
            QPushButton:hover { background: #ea6c10; }
        """)
        invite_btn.clicked.connect(self._invite)

        hl.addWidget(icon)
        hl.addLayout(info)
        hl.addStretch()
        hl.addWidget(invite_btn)
        return hdr

    # ── Members tab ─────────────────────────────────────────────────────────────
    def _tab_members(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(20, 16, 20, 16)
        lay.setSpacing(12)

        # Stat chips
        total    = len(self.members)
        active   = sum(1 for m in self.members if m.status == "Active")
        admins   = sum(1 for m in self.members if m.role in ("Owner","Admin"))
        invited  = sum(1 for m in self.members if m.status == "Invited")

        chips_row = QHBoxLayout()
        chips_row.setSpacing(10)
        chips_row.addWidget(_stat_chip(total,   "Total",   "#f97316"))
        chips_row.addWidget(_stat_chip(active,  "Active",  "#22c55e"))
        chips_row.addWidget(_stat_chip(admins,  "Admins",  "#3b82f6"))
        chips_row.addWidget(_stat_chip(invited, "Invited", "#f59e0b"))
        chips_row.addStretch()
        lay.addLayout(chips_row)

        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.setSpacing(8)

        self.member_search = QLineEdit()
        self.member_search.setPlaceholderText("🔍  Search members…")
        self.member_search.setFixedHeight(36)
        self.member_search.textChanged.connect(self._filter_members)

        self.role_filter = QComboBox()
        self.role_filter.setFixedHeight(36)
        for r in ["All Roles", "Owner", "Admin", "Member", "Viewer"]:
            self.role_filter.addItem(r)
        self.role_filter.currentTextChanged.connect(self._filter_members)

        self.status_filter_m = QComboBox()
        self.status_filter_m.setFixedHeight(36)
        for s in ["All Status", "Active", "Invited", "Suspended"]:
            self.status_filter_m.addItem(s)
        self.status_filter_m.currentTextChanged.connect(self._filter_members)

        toolbar.addWidget(self.member_search, 2)
        toolbar.addWidget(self.role_filter)
        toolbar.addWidget(self.status_filter_m)
        lay.addLayout(toolbar)

        # Table
        COLS = ["Member", "Email", "Role", "Status", "Profiles", "Devices", "Last Login", "Actions"]
        self.member_table = _styled_table(COLS, stretch_col=1)
        self.member_table.setColumnWidth(0, 160)
        self.member_table.setColumnWidth(2, 90)
        self.member_table.setColumnWidth(3, 100)
        self.member_table.setColumnWidth(4, 70)
        self.member_table.setColumnWidth(5, 70)
        self.member_table.setColumnWidth(6, 130)
        self.member_table.setColumnWidth(7, 130)
        lay.addWidget(self.member_table, 1)

        self._populate_members(self.members)
        return w

    def _populate_members(self, members):
        self.member_table.setRowCount(0)
        for m in members:
            r = self.member_table.rowCount()
            self.member_table.insertRow(r)
            self.member_table.setRowHeight(r, 50)

            # Name with avatar initial
            name_w = QWidget()
            name_w.setStyleSheet("background:transparent;")
            nl = QHBoxLayout(name_w)
            nl.setContentsMargins(8, 4, 8, 4)
            nl.setSpacing(10)

            av = QLabel(m.name[0].upper())
            av.setFixedSize(32, 32)
            av.setAlignment(Qt.AlignmentFlag.AlignCenter)
            fg_r, bg_r = ROLE_COLORS.get(m.role, ("#94a3b8", "#1e2d45"))
            av.setStyleSheet(f"""
                background: {bg_r}; color: {fg_r};
                border-radius: 8px; font-size:13px; font-weight:800; border:none;
            """)

            nm = QLabel(m.name)
            nm.setStyleSheet("color:#f1f5f9; font-size:13px; font-weight:600;"
                             "background:transparent; border:none;")
            nl.addWidget(av)
            nl.addWidget(nm)
            nl.addStretch()
            self.member_table.setCellWidget(r, 0, name_w)

            email_item = QTableWidgetItem(m.email)
            email_item.setForeground(QColor("#64748b"))
            self.member_table.setItem(r, 1, email_item)

            # Role badge
            fg_r, bg_r = ROLE_COLORS.get(m.role, ("#94a3b8", "#1e2d45"))
            role_w = QWidget()
            role_w.setStyleSheet("background:transparent;")
            rl = QHBoxLayout(role_w)
            rl.setContentsMargins(6, 0, 6, 0)
            rl.addWidget(_badge(m.role, fg_r, bg_r))
            rl.addStretch()
            self.member_table.setCellWidget(r, 2, role_w)

            # Status badge
            fg_s, bg_s = STATUS_COLORS.get(m.status, ("#64748b", "#0f172a"))
            st_w = QWidget()
            st_w.setStyleSheet("background:transparent;")
            sl = QHBoxLayout(st_w)
            sl.setContentsMargins(6, 0, 6, 0)
            sl.addWidget(_badge(m.status, fg_s, bg_s))
            sl.addStretch()
            self.member_table.setCellWidget(r, 3, st_w)

            # Numbers
            for col, val in [(4, m.shared_profiles), (5, m.max_devices)]:
                it = QTableWidgetItem(str(val))
                it.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                it.setForeground(QColor("#94a3b8"))
                self.member_table.setItem(r, col, it)

            self.member_table.setItem(r, 6, QTableWidgetItem(m.last_login or "—"))

            # Action buttons
            acts = QWidget()
            acts.setStyleSheet("background:transparent;")
            al = QHBoxLayout(acts)
            al.setContentsMargins(6, 0, 6, 0)
            al.setSpacing(6)

            edit_b = _action_btn("✏️ Edit",  "#94a3b8", "#111827", "#1e2d45", 72, 30)
            del_b  = _action_btn("🗑 Remove", "#f87171", "#1a0a0a", "#450a0a", 80, 30)
            del_b.clicked.connect(lambda _, name=m.name: self._remove_member(name))

            al.addWidget(edit_b)
            al.addWidget(del_b)
            al.addStretch()
            self.member_table.setCellWidget(r, 7, acts)

    def _filter_members(self):
        q     = self.member_search.text().lower()
        role  = self.role_filter.currentText()
        stat  = self.status_filter_m.currentText()
        result = [
            m for m in self.members
            if (not q or q in m.name.lower() or q in m.email.lower())
            and (role  == "All Roles"   or m.role   == role)
            and (stat  == "All Status"  or m.status  == stat)
        ]
        self._populate_members(result)

    def _invite(self):
        dlg = InviteDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            QMessageBox.information(
                self, "Invited",
                f"✅  Invitation sent to {dlg.email_edit.text()}"
            )

    def _remove_member(self, name):
        reply = QMessageBox.question(
            self, "Remove Member",
            f"Remove '{name}' from the team?\nThis cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.members = [m for m in self.members if m.name != name]
            self._populate_members(self.members)

    # ── Roles & Permissions tab ─────────────────────────────────────────────────
    def _tab_roles(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border:none; background:transparent; }")

        inner = QWidget()
        inner.setStyleSheet("background:transparent;")
        lay = QVBoxLayout(inner)
        lay.setContentsMargins(24, 20, 24, 20)
        lay.setSpacing(14)

        lay.addWidget(_section_header(
            "Roles & Permissions",
            "Define what each role can do across the platform"
        ))

        PERMS = [
            ("View Profiles",    "See all profiles in the workspace"),
            ("Launch Profiles",  "Open and run browser profiles"),
            ("Edit Profiles",    "Modify profile settings and fingerprints"),
            ("Delete Profiles",  "Permanently remove profiles"),
            ("Manage Team",      "Invite, edit, and remove team members"),
            ("Manage Settings",  "Change global workspace settings"),
            ("API Access",       "Use the Open API with API keys"),
            ("Cloud Sync",       "Sync profiles to and from the cloud"),
        ]
        ROLE_PERMS = {
            "Owner":  {p[0] for p in PERMS},
            "Admin":  {"View Profiles","Launch Profiles","Edit Profiles","Delete Profiles","API Access","Cloud Sync"},
            "Member": {"View Profiles","Launch Profiles","Edit Profiles"},
            "Viewer": {"View Profiles"},
        }
        ROLE_META = [
            ("Owner",  "👑", "#fbbf24", "#451a03", "Full control — can transfer ownership"),
            ("Admin",  "🛡️",  "#34d399", "#064e3b", "Manages profiles and members; cannot transfer ownership"),
            ("Member", "👤", "#94a3b8", "#1e2d45", "Works with assigned profiles; no team management"),
            ("Viewer", "👁️",  "#64748b", "#0f172a", "Read-only access; cannot edit or launch"),
        ]

        for role, icon, fg, bg, desc in ROLE_META:
            card = QFrame()
            card.setStyleSheet(f"""
                QFrame {{
                    background: {bg}30;
                    border: 1px solid {fg}30;
                    border-radius: 12px;
                    padding: 4px;
                }}
            """)
            cl = QVBoxLayout(card)
            cl.setContentsMargins(16, 14, 16, 14)
            cl.setSpacing(10)

            # Role title row
            title_row = QHBoxLayout()
            title_row.setSpacing(10)
            ic = QLabel(icon)
            ic.setStyleSheet("font-size:18px;")
            name_lb = QLabel(role)
            name_lb.setStyleSheet(f"color:{fg}; font-size:14px; font-weight:800;")
            desc_lb = QLabel(desc)
            desc_lb.setStyleSheet("color:#475569; font-size:12px;")
            title_row.addWidget(ic)
            title_row.addWidget(name_lb)
            title_row.addWidget(desc_lb)
            title_row.addStretch()
            cl.addLayout(title_row)

            # Permission checkboxes grid (4 per row)
            grid_w = QWidget()
            grid_w.setStyleSheet("background:transparent;")
            grid_l = QHBoxLayout(grid_w)
            grid_l.setContentsMargins(0, 0, 0, 0)
            grid_l.setSpacing(0)

            col1 = QVBoxLayout(); col1.setSpacing(4)
            col2 = QVBoxLayout(); col2.setSpacing(4)
            for i, (pname, _ptip) in enumerate(PERMS):
                cb = QCheckBox(pname)
                cb.setChecked(pname in ROLE_PERMS[role])
                cb.setEnabled(False)
                cb.setStyleSheet(f"""
                    QCheckBox {{ color: {'#e2e8f0' if pname in ROLE_PERMS[role] else '#334155'};
                                 font-size:12px; spacing:6px; }}
                    QCheckBox::indicator {{
                        width:14px; height:14px; border-radius:4px;
                        border:1px solid {'#'+fg[1:] if pname in ROLE_PERMS[role] else '334155'};
                        background: {''+bg if pname in ROLE_PERMS[role] else '#0a0d16'};
                    }}
                    QCheckBox::indicator:checked {{ background:{fg}; border-color:{fg}; }}
                """)
                (col1 if i < 4 else col2).addWidget(cb)

            grid_l.addLayout(col1, 1)
            grid_l.addLayout(col2, 1)
            cl.addWidget(grid_w)
            lay.addWidget(card)

        lay.addStretch()
        scroll.setWidget(inner)
        return scroll

    # ── Devices tab ─────────────────────────────────────────────────────────────
    def _tab_devices(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(20, 16, 20, 16)
        lay.setSpacing(12)

        lay.addWidget(_section_header(
            "💻  Multi-Device Login",
            "Track and manage all active device sessions for your team"
        ))

        COLS = ["Member", "Device", "OS", "Last Active", "Status", "Action"]
        tbl = _styled_table(COLS, stretch_col=0)
        tbl.setColumnWidth(1, 170)
        tbl.setColumnWidth(2, 110)
        tbl.setColumnWidth(3, 140)
        tbl.setColumnWidth(4, 100)
        tbl.setColumnWidth(5, 90)

        DEVICES = [
            ("SOPHEARUN",   "MacBook Pro M2",  "macOS 14",   "Today 09:00",      "Active"),
            ("SOPHEARUN",   "Windows Desktop", "Windows 11", "Yesterday 18:00",  "Active"),
            ("Sarah Lee",   "Dell XPS 15",     "Windows 10", "Today 08:45",      "Active"),
            ("Mike Chen",   "MacBook Air M1",  "macOS 13",   "Yesterday 17:20",  "Active"),
            ("Tom Davis",   "HP EliteBook",    "Windows 11", "3 days ago",       "Inactive"),
            ("Anna Kim",    "iPad Pro",        "iPadOS 17",  "Today 07:30",      "Active"),
        ]

        for name, device, os_, last, status in DEVICES:
            r = tbl.rowCount()
            tbl.insertRow(r)
            tbl.setRowHeight(r, 46)

            for col, val in [(0, name), (1, device), (2, os_), (3, last)]:
                it = QTableWidgetItem(val)
                it.setForeground(QColor("#94a3b8" if col > 0 else "#e2e8f0"))
                tbl.setItem(r, col, it)

            fg_s, bg_s = STATUS_COLORS.get(status, ("#64748b", "#0f172a"))
            st_w = QWidget()
            st_w.setStyleSheet("background:transparent;")
            sl = QHBoxLayout(st_w)
            sl.setContentsMargins(6, 0, 6, 0)
            sl.addWidget(_badge(status, fg_s, bg_s))
            sl.addStretch()
            tbl.setCellWidget(r, 4, st_w)

            revoke = _action_btn("Revoke", "#f87171", "#1a0a0a", "#450a0a", 70, 28)
            act_w = QWidget()
            act_w.setStyleSheet("background:transparent;")
            al = QHBoxLayout(act_w)
            al.setContentsMargins(6, 0, 6, 0)
            al.addWidget(revoke)
            al.addStretch()
            tbl.setCellWidget(r, 5, act_w)

        lay.addWidget(tbl, 1)
        return w

    # ── Transfer BOSS tab ────────────────────────────────────────────────────────
    def _tab_transfer(self):
        w = QWidget()
        outer = QVBoxLayout(w)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setFixedWidth(540)
        card.setStyleSheet("""
            QFrame {
                background: #0d1117;
                border: 1px solid #1a2236;
                border-radius: 16px;
            }
        """)
        lay = QVBoxLayout(card)
        lay.setContentsMargins(40, 36, 40, 36)
        lay.setSpacing(18)

        # Crown icon
        crown = QLabel("👑")
        crown.setAlignment(Qt.AlignmentFlag.AlignCenter)
        crown.setStyleSheet("font-size:52px; background:transparent;")
        lay.addWidget(crown)

        title = QLabel("Transfer Team Ownership")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:20px; font-weight:800; color:#f1f5f9; background:transparent;")
        lay.addWidget(title)

        desc = QLabel(
            "Transfer your BOSS (Owner) role to an Admin member.\n"
            "After transfer you will become an Admin. This is irreversible."
        )
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setWordWrap(True)
        desc.setStyleSheet("color:#475569; font-size:13px; background:transparent;")
        lay.addWidget(desc)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background:#1a2236; border:none; min-height:1px; max-height:1px;")
        lay.addWidget(sep)

        target_lb = QLabel("Transfer ownership to:")
        target_lb.setStyleSheet("color:#94a3b8; font-size:12px; font-weight:600; background:transparent;")
        lay.addWidget(target_lb)

        self.boss_target = QComboBox()
        self.boss_target.setFixedHeight(42)
        admins = [m for m in self.members if m.role == "Admin"]
        if admins:
            for m in admins:
                self.boss_target.addItem(f"🛡️  {m.name}  ({m.email})")
        else:
            self.boss_target.addItem("No Admin members available")
        lay.addWidget(self.boss_target)

        warn = QLabel(
            "⚠️  This action is permanent and cannot be undone.\n"
            "Make sure you trust the selected member."
        )
        warn.setWordWrap(True)
        warn.setStyleSheet(
            "color:#fcd34d; font-size:12px; background:#451a0360;"
            "border:1px solid #f59e0b40; border-radius:10px; padding:14px 16px;"
        )
        lay.addWidget(warn)

        transfer_btn = QPushButton("👑  Transfer Ownership Now")
        transfer_btn.setFixedHeight(46)
        transfer_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #7f1d1d, stop:1 #ef4444);
                color: white; border: none; border-radius: 12px;
                font-size: 14px; font-weight: 800;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                    stop:0 #991b1b, stop:1 #dc2626);
            }
        """)
        transfer_btn.clicked.connect(self._confirm_transfer)
        transfer_btn.setEnabled(bool(admins))
        lay.addWidget(transfer_btn)

        outer.addStretch()
        outer.addWidget(card, 0, Qt.AlignmentFlag.AlignHCenter)
        outer.addStretch()
        return w

    def _confirm_transfer(self):
        target = self.boss_target.currentText()
        reply = QMessageBox.question(
            self, "Confirm Transfer",
            f"Transfer ownership to:\n{target}\n\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(
                self, "Transferred",
                f"✅  Ownership has been transferred to\n{target}"
            )
