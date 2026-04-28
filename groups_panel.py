"""Groups Panel — create, edit, delete groups with custom color & icon."""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QDialog, QLineEdit, QGridLayout,
    QMessageBox, QSizePolicy, QToolButton, QColorDialog,
    QFormLayout, QDialogButtonBox, QSpinBox, QComboBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont
import storage, json
from pathlib import Path

# ── Persistent group storage ───────────────────────────────────────────────────
GROUPS_FILE = Path.home() / ".khbrowser" / "groups.json"

DEFAULT_GROUPS = [
    {"name": "Default",      "icon": "📁", "color": "#6366f1", "description": "General profiles"},
    {"name": "Facebook",     "icon": "📘", "color": "#1877f2", "description": "Facebook accounts"},
    {"name": "Social Media", "icon": "📱", "color": "#e1306c", "description": "Social platforms"},
    {"name": "E-commerce",   "icon": "🛒", "color": "#f59e0b", "description": "Shop accounts"},
    {"name": "B2B",          "icon": "💼", "color": "#10b981", "description": "Business accounts"},
    {"name": "Content",      "icon": "🎬", "color": "#ef4444", "description": "Content creators"},
]

EMOJI_LIST = [
    "📁","📂","📘","📗","📕","📙","🗂️","💼","🛒","🎯","🎬","📱",
    "🌐","🔵","🟢","🟡","🔴","⚡","🚀","🤖","👤","🏆","💎","🔑",
    "🌟","🔥","💡","🎮","📊","📈","🛡️","⚙️","🧪","🎁","🏪","🏦",
]


def load_groups():
    if not GROUPS_FILE.exists():
        save_groups(DEFAULT_GROUPS)
        return [dict(g) for g in DEFAULT_GROUPS]
    try:
        with open(GROUPS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return [dict(g) for g in DEFAULT_GROUPS]


def save_groups(groups):
    GROUPS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(GROUPS_FILE, "w", encoding="utf-8") as f:
        json.dump(groups, f, indent=2, ensure_ascii=False)


# ── Group Edit Dialog ──────────────────────────────────────────────────────────

class GroupEditDialog(QDialog):
    def __init__(self, parent, group: dict = None):
        super().__init__(parent)
        self.setWindowTitle("Edit Group" if group else "New Group")
        self.setMinimumWidth(420)
        self.setStyleSheet(parent.styleSheet() if parent else "")
        self._group = dict(group) if group else {
            "name": "", "icon": "📁", "color": "#6366f1", "description": ""
        }
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 24, 24, 24)
        lay.setSpacing(16)

        title = QLabel("Edit Group" if self._group.get("name") else "New Group")
        title.setStyleSheet("font-size:16px;font-weight:700;color:#e2e8f0;")
        lay.addWidget(title)

        # Preview card
        self._preview = QFrame()
        self._preview.setFixedHeight(70)
        self._preview.setStyleSheet(f"""
            QFrame {{
                background:#131720;
                border:2px solid {self._group['color']};
                border-radius:12px;
            }}
        """)
        pl = QHBoxLayout(self._preview)
        pl.setContentsMargins(16, 0, 16, 0)
        self._prev_icon = QLabel(self._group["icon"])
        self._prev_icon.setStyleSheet("font-size:28px;")
        self._prev_name = QLabel(self._group["name"] or "Group Name")
        self._prev_name.setStyleSheet("color:#e2e8f0;font-size:16px;font-weight:700;")
        pl.addWidget(self._prev_icon)
        pl.addWidget(self._prev_name, 1)
        lay.addWidget(self._preview)

        # Form
        form = QFormLayout()
        form.setSpacing(12)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.name_edit = QLineEdit(self._group["name"])
        self.name_edit.setPlaceholderText("Group name…")
        self.name_edit.setStyleSheet("background:#1a2035;color:#e2e8f0;border:1px solid #2d3a50;border-radius:6px;padding:6px 10px;")
        self.name_edit.textChanged.connect(self._update_preview)

        self.desc_edit = QLineEdit(self._group.get("description", ""))
        self.desc_edit.setPlaceholderText("Short description…")
        self.desc_edit.setStyleSheet("background:#1a2035;color:#e2e8f0;border:1px solid #2d3a50;border-radius:6px;padding:6px 10px;")

        form.addRow(QLabel("Name"), self.name_edit)
        form.addRow(QLabel("Description"), self.desc_edit)
        lay.addLayout(form)

        # Icon picker
        icon_lbl = QLabel("Icon")
        icon_lbl.setStyleSheet("color:#94a3b8;font-size:12px;font-weight:600;")
        lay.addWidget(icon_lbl)

        grid = QGridLayout()
        grid.setSpacing(6)
        self._icon_btns = []
        for i, em in enumerate(EMOJI_LIST):
            btn = QPushButton(em)
            btn.setFixedSize(38, 38)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {'#1e2d4a' if em == self._group['icon'] else '#1a2035'};
                    border: 2px solid {'#6366f1' if em == self._group['icon'] else '#2d3a50'};
                    border-radius: 8px;
                    font-size: 18px;
                }}
                QPushButton:hover {{ background:#1e2d4a; border-color:#6366f1; }}
            """)
            btn.clicked.connect(lambda _, e=em: self._pick_icon(e))
            self._icon_btns.append((em, btn))
            grid.addWidget(btn, i // 8, i % 8)
        lay.addLayout(grid)

        # Color picker
        color_row = QHBoxLayout()
        color_lbl = QLabel("Accent Color")
        color_lbl.setStyleSheet("color:#94a3b8;font-size:12px;font-weight:600;")
        self._color_btn = QPushButton()
        self._color_btn.setFixedSize(100, 32)
        self._color_btn.clicked.connect(self._pick_color)
        self._refresh_color_btn()
        color_row.addWidget(color_lbl)
        color_row.addStretch()
        color_row.addWidget(self._color_btn)
        lay.addLayout(color_row)

        # Preset colors
        preset_row = QHBoxLayout()
        preset_row.setSpacing(8)
        for c in ["#6366f1","#10b981","#f59e0b","#ef4444","#06b6d4","#a78bfa","#ec4899","#1877f2"]:
            cb = QPushButton()
            cb.setFixedSize(28, 28)
            cb.setStyleSheet(f"""
                QPushButton {{
                    background:{c};
                    border-radius:14px;
                    border: 2px solid {'#ffffff' if c == self._group['color'] else 'transparent'};
                }}
                QPushButton:hover {{ border:2px solid #ffffff; }}
            """)
            cb.clicked.connect(lambda _, col=c: self._pick_color_direct(col))
            preset_row.addWidget(cb)
        preset_row.addStretch()
        lay.addLayout(preset_row)

        # Buttons
        btns = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        btns.accepted.connect(self._accept)
        btns.rejected.connect(self.reject)
        btns.button(QDialogButtonBox.StandardButton.Save).setStyleSheet(
            "background:#6366f1;color:white;font-weight:700;border-radius:8px;padding:8px 20px;"
        )
        lay.addWidget(btns)

    def _update_preview(self):
        self._prev_name.setText(self.name_edit.text() or "Group Name")

    def _pick_icon(self, em):
        self._group["icon"] = em
        self._prev_icon.setText(em)
        for emoji, btn in self._icon_btns:
            sel = emoji == em
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: {'#1e2d4a' if sel else '#1a2035'};
                    border: 2px solid {'#6366f1' if sel else '#2d3a50'};
                    border-radius: 8px;
                    font-size: 18px;
                }}
                QPushButton:hover {{ background:#1e2d4a; border-color:#6366f1; }}
            """)

    def _pick_color(self):
        c = QColorDialog.getColor(QColor(self._group["color"]), self, "Pick accent color")
        if c.isValid():
            self._pick_color_direct(c.name())

    def _pick_color_direct(self, color):
        self._group["color"] = color
        self._refresh_color_btn()
        self._preview.setStyleSheet(f"""
            QFrame {{
                background:#131720;
                border:2px solid {color};
                border-radius:12px;
            }}
        """)

    def _refresh_color_btn(self):
        c = self._group["color"]
        self._color_btn.setStyleSheet(f"""
            QPushButton {{
                background:{c};
                border-radius:8px;
                border:none;
                color:white;
                font-size:11px;
                font-weight:600;
            }}
        """)
        self._color_btn.setText(c)

    def _accept(self):
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Validation", "Group name cannot be empty.")
            return
        self._group["name"] = name
        self._group["description"] = self.desc_edit.text().strip()
        self.accept()

    def get_group(self):
        return self._group


# ── Group Card ─────────────────────────────────────────────────────────────────

class GroupCard(QFrame):
    edit_requested   = pyqtSignal(dict)
    delete_requested = pyqtSignal(dict)

    def __init__(self, group: dict, profile_count=0, running_count=0, parent=None):
        super().__init__(parent)
        self.group = group
        self.setObjectName("groupCard")
        self.setFixedHeight(140)
        color = group.get("color", "#6366f1")
        self.setStyleSheet(f"""
            QFrame#groupCard {{
                background:#131720;
                border:1px solid #1e2433;
                border-top:3px solid {color};
                border-radius:12px;
            }}
            QFrame#groupCard:hover {{
                border:1px solid {color};
                border-top:3px solid {color};
            }}
        """)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 14, 16, 14)
        lay.setSpacing(8)

        # Top row: icon + name + action buttons
        top = QHBoxLayout()
        icon_lb = QLabel(group.get("icon", "📁"))
        icon_lb.setStyleSheet("font-size:24px;")
        name_lb = QLabel(group.get("name", ""))
        name_lb.setStyleSheet(f"color:{color};font-size:15px;font-weight:700;")
        top.addWidget(icon_lb)
        top.addWidget(name_lb)
        top.addStretch()

        edit_btn = QToolButton()
        edit_btn.setText("✏️")
        edit_btn.setFixedSize(28, 28)
        edit_btn.setStyleSheet("QToolButton{background:#1a2035;border:none;border-radius:6px;font-size:14px;}"
                               "QToolButton:hover{background:#1e2d4a;}")
        edit_btn.clicked.connect(lambda: self.edit_requested.emit(self.group))

        del_btn = QToolButton()
        del_btn.setText("🗑")
        del_btn.setFixedSize(28, 28)
        del_btn.setStyleSheet("QToolButton{background:#1a2035;border:none;border-radius:6px;font-size:14px;}"
                              "QToolButton:hover{background:#3d1515;}")
        del_btn.clicked.connect(lambda: self.delete_requested.emit(self.group))

        top.addWidget(edit_btn)
        top.addWidget(del_btn)
        lay.addLayout(top)

        # Description
        desc = group.get("description", "")
        if desc:
            desc_lb = QLabel(desc)
            desc_lb.setStyleSheet("color:#4b5568;font-size:12px;")
            desc_lb.setWordWrap(True)
            lay.addWidget(desc_lb)

        # Stats row
        stats = QHBoxLayout()
        stats.setSpacing(16)
        for icon, val, label in [
            ("🗂️", str(profile_count), "profiles"),
            ("▶️", str(running_count), "running"),
        ]:
            sw = QWidget()
            sl = QHBoxLayout(sw)
            sl.setContentsMargins(0, 0, 0, 0)
            sl.setSpacing(4)
            iv = QLabel(icon)
            iv.setStyleSheet("font-size:12px;")
            vl = QLabel(f"{val} {label}")
            vl.setStyleSheet("color:#94a3b8;font-size:12px;")
            sl.addWidget(iv)
            sl.addWidget(vl)
            stats.addWidget(sw)
        stats.addStretch()
        lay.addLayout(stats)


# ── Groups Panel ───────────────────────────────────────────────────────────────

class GroupsPanel(QWidget):
    group_filter_changed = pyqtSignal(str)   # emitted when user clicks a group

    def __init__(self, profile_panel, parent=None):
        super().__init__(parent)
        self.pp = profile_panel
        self.groups = load_groups()
        self._build()
        self._populate()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Header ─────────────────────────────────────────────────────────
        hdr = QWidget()
        hdr.setFixedHeight(60)
        hdr.setStyleSheet("background:#0d1117;border-bottom:1px solid #1e2433;")
        hl = QHBoxLayout(hdr)
        hl.setContentsMargins(24, 0, 24, 0)

        title = QLabel("📁  Groups")
        title.setStyleSheet("color:#e2e8f0;font-size:18px;font-weight:700;")

        self.count_lb = QLabel()
        self.count_lb.setStyleSheet("color:#4b5568;font-size:13px;")

        new_btn = QPushButton("✨  New Group")
        new_btn.setFixedHeight(36)
        new_btn.setStyleSheet("""
            QPushButton {
                background:#6366f1;color:white;font-weight:700;
                border-radius:8px;padding:0 16px;border:none;
            }
            QPushButton:hover { background:#4f46e5; }
        """)
        new_btn.clicked.connect(self._new_group)

        hl.addWidget(title)
        hl.addWidget(self.count_lb)
        hl.addStretch()
        hl.addWidget(new_btn)
        root.addWidget(hdr)

        # ── Scroll body ────────────────────────────────────────────────────
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { background: #0d1117; border: none; }")

        self._body = QWidget()
        self._body.setStyleSheet("background:#0d1117;")
        self._grid = QGridLayout(self._body)
        self._grid.setContentsMargins(24, 20, 24, 24)
        self._grid.setSpacing(16)
        scroll.setWidget(self._body)
        root.addWidget(scroll, 1)

    def _populate(self):
        # Clear grid
        while self._grid.count():
            item = self._grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        profiles = self.pp.profiles
        cols = 3
        for i, g in enumerate(self.groups):
            name = g["name"]
            pcount  = sum(1 for p in profiles if p.group == name)
            rcount  = sum(1 for p in profiles if p.group == name and p.status == "running")
            card = GroupCard(g, pcount, rcount)
            card.edit_requested.connect(self._edit_group)
            card.delete_requested.connect(self._delete_group)
            self._grid.addWidget(card, i // cols, i % cols)

        # Fill empty slots for alignment
        remainder = len(self.groups) % cols
        if remainder:
            for j in range(cols - remainder):
                spacer = QWidget()
                spacer.setFixedHeight(140)
                self._grid.addWidget(spacer, len(self.groups) // cols, remainder + j)

        self._grid.setRowStretch(self._grid.rowCount(), 1)
        self.count_lb.setText(f"  {len(self.groups)} groups")

    def _new_group(self):
        dlg = GroupEditDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            g = dlg.get_group()
            # Check duplicate
            if any(x["name"] == g["name"] for x in self.groups):
                QMessageBox.warning(self, "Duplicate", f"Group '{g['name']}' already exists.")
                return
            self.groups.append(g)
            save_groups(self.groups)
            self._populate()

    def _edit_group(self, group: dict):
        dlg = GroupEditDialog(self, group)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            updated = dlg.get_group()
            old_name = group["name"]
            new_name = updated["name"]
            # Update profiles that belong to this group
            if old_name != new_name:
                for p in self.pp.profiles:
                    if p.group == old_name:
                        p.group = new_name
                storage.save_profiles(self.pp.profiles)
            # Update group in list
            for i, g in enumerate(self.groups):
                if g["name"] == old_name:
                    self.groups[i] = updated
                    break
            save_groups(self.groups)
            self._populate()

    def _delete_group(self, group: dict):
        name = group["name"]
        pcount = sum(1 for p in self.pp.profiles if p.group == name)
        msg = f"Delete group '{name}'?"
        if pcount:
            msg += f"\n\n{pcount} profile(s) will be moved to 'Default'."
        reply = QMessageBox.question(
            self, "Delete Group", msg,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            if pcount:
                for p in self.pp.profiles:
                    if p.group == name:
                        p.group = "Default"
                storage.save_profiles(self.pp.profiles)
            self.groups = [g for g in self.groups if g["name"] != name]
            save_groups(self.groups)
            self._populate()

    def refresh(self):
        """Call this after profile list changes."""
        self._populate()
