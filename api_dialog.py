"""Open API management dialog."""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QFrame, QLineEdit, QCheckBox, QGroupBox, QTextEdit, QComboBox,
    QMessageBox, QPlainTextEdit, QTabWidget, QScrollArea, QGridLayout
)
from PyQt6.QtCore import Qt
from models import APIKey, SAMPLE_API_KEYS
import uuid


def _badge(text, color_style):
    lb = QLabel(text)
    lb.setAlignment(Qt.AlignmentFlag.AlignCenter)
    lb.setStyleSheet(f"{color_style}border-radius:10px;padding:2px 8px;font-size:11px;font-weight:600;")
    return lb


class NewKeyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create API Key")
        self.setFixedSize(460, 320)
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 24, 24, 24)
        lay.setSpacing(14)
        lay.addWidget(QLabel("🔑  Create New API Key"))

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("e.g. Production Key")
        lay.addWidget(QLabel("Key Name *"))
        lay.addWidget(self.name_edit)

        lay.addWidget(QLabel("Permissions"))
        perm_gb = QGroupBox()
        pg = QGridLayout(perm_gb)
        self.perms = {}
        for i, (p, checked) in enumerate([
            ("read", True), ("write", True), ("delete", False),
            ("team:read", False), ("team:write", False), ("api:manage", False)
        ]):
            cb = QCheckBox(p)
            cb.setChecked(checked)
            self.perms[p] = cb
            pg.addWidget(cb, i // 3, i % 3)
        lay.addWidget(perm_gb)

        self.expiry_combo = QComboBox()
        for e in ["Never", "30 days", "90 days", "1 year"]:
            self.expiry_combo.addItem(e)
        hl = QHBoxLayout()
        hl.addWidget(QLabel("Expiry:"))
        hl.addWidget(self.expiry_combo)
        hl.addStretch()
        lay.addLayout(hl)

        from PyQt6.QtWidgets import QDialogButtonBox
        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(self._validate)
        btns.rejected.connect(self.reject)
        btns.button(QDialogButtonBox.StandardButton.Ok).setText("Create Key")
        btns.button(QDialogButtonBox.StandardButton.Ok).setObjectName("primaryBtn")
        lay.addWidget(btns)

    def _validate(self):
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "Validation", "Key name is required.")
            return
        self.accept()

    def get_permissions(self):
        return [p for p, cb in self.perms.items() if cb.isChecked()]


class APIDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.keys = list(SAMPLE_API_KEYS)
        self.setWindowTitle("Open API")
        self.setMinimumSize(980, 660)
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        header = QWidget()
        header.setStyleSheet("background:#111827;border-bottom:1px solid #1e2433;")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(20, 14, 20, 14)
        title = QLabel("🔌  Open API")
        title.setStyleSheet("font-size:16px;font-weight:700;color:#e2e8f0;")
        new_btn = QPushButton("➕  Create API Key")
        new_btn.setObjectName("primaryBtn")
        new_btn.clicked.connect(self._create_key)
        hl.addWidget(title)
        hl.addStretch()
        hl.addWidget(new_btn)
        root.addWidget(header)

        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        tabs.addTab(self._build_keys_tab(), "🔑  API Keys")
        tabs.addTab(self._build_docs_tab(), "📖  Documentation")
        tabs.addTab(self._build_logs_tab(), "📊  Request Logs")
        root.addWidget(tabs, 1)

    # ── Keys tab ────────────────────────────────────────────────────────────────
    def _build_keys_tab(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(20, 16, 20, 16)

        info = QLabel(
            "Use API keys to integrate with external tools and automate profile management. "
            "Keep your keys secure — treat them like passwords."
        )
        info.setWordWrap(True)
        info.setStyleSheet("color:#64748b;font-size:12px;background:#111827;border-radius:6px;padding:10px;")
        lay.addWidget(info)

        cols = ["Name", "API Key", "Permissions", "Requests", "Last Used", "Status", "Actions"]
        self.key_table = QTableWidget(0, len(cols))
        self.key_table.setHorizontalHeaderLabels(cols)
        self.key_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.key_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.key_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.key_table.verticalHeader().setVisible(False)
        self.key_table.setAlternatingRowColors(True)
        lay.addWidget(self.key_table)

        self._populate_keys()
        return w

    def _populate_keys(self):
        self.key_table.setRowCount(0)
        for key in self.keys:
            r = self.key_table.rowCount()
            self.key_table.insertRow(r)
            self.key_table.setRowHeight(r, 48)

            self.key_table.setItem(r, 0, QTableWidgetItem(f"  {key.name}"))

            # masked key with reveal btn
            key_w = QWidget()
            kl = QHBoxLayout(key_w)
            kl.setContentsMargins(4, 4, 4, 4)
            masked = key.key[:12] + "••••••••••••••••••"
            key_lb = QLabel(masked)
            key_lb.setStyleSheet("font-family:monospace;font-size:12px;color:#64748b;")
            copy_btn = QPushButton("📋")
            copy_btn.setObjectName("iconBtn")
            copy_btn.setFixedSize(26, 26)
            copy_btn.setToolTip("Copy to clipboard")
            copy_btn.clicked.connect(lambda _, k=key.key: self._copy_key(k))
            kl.addWidget(key_lb, 1)
            kl.addWidget(copy_btn)
            self.key_table.setCellWidget(r, 1, key_w)

            perms_text = ", ".join(key.permissions)
            self.key_table.setItem(r, 2, QTableWidgetItem(perms_text))
            self.key_table.setItem(r, 3, QTableWidgetItem(f"{key.request_count:,}"))
            self.key_table.setItem(r, 4, QTableWidgetItem(key.last_used or "Never"))

            st_w = QWidget()
            sl = QHBoxLayout(st_w)
            sl.setContentsMargins(4, 4, 4, 4)
            status_badge = _badge(
                "Active" if key.active else "Inactive",
                "background:#064e3b;color:#6ee7b7;" if key.active else "background:#1e2433;color:#64748b;"
            )
            sl.addWidget(status_badge)
            sl.addStretch()
            self.key_table.setCellWidget(r, 5, st_w)

            acts = QWidget()
            al = QHBoxLayout(acts)
            al.setContentsMargins(4, 4, 4, 4)
            al.setSpacing(4)
            toggle_btn = QPushButton("Disable" if key.active else "Enable")
            toggle_btn.setObjectName("iconBtn")
            toggle_btn.setFixedSize(60, 28)
            del_btn = QPushButton("Delete")
            del_btn.setObjectName("iconBtn")
            del_btn.setFixedSize(55, 28)
            del_btn.setStyleSheet("color:#fca5a5;")
            del_btn.clicked.connect(lambda _, k=key: self._delete_key(k))
            al.addWidget(toggle_btn)
            al.addWidget(del_btn)
            al.addStretch()
            self.key_table.setCellWidget(r, 6, acts)

    def _copy_key(self, key_text):
        from PyQt6.QtWidgets import QApplication
        QApplication.clipboard().setText(key_text)
        QMessageBox.information(self, "Copied", "✅  API key copied to clipboard.")

    def _create_key(self):
        dlg = NewKeyDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            key = APIKey(
                name=dlg.name_edit.text(),
                permissions=dlg.get_permissions()
            )
            # Show new key
            QMessageBox.information(
                self, "Key Created",
                f"✅  API Key created!\n\nKey:\n{key.key}\n\n"
                "⚠️  Copy this key now. It will not be shown again."
            )
            self.keys.append(key)
            self._populate_keys()

    def _delete_key(self, key):
        reply = QMessageBox.question(
            self, "Delete Key",
            f"Delete API key '{key.name}'?\nThis will immediately invalidate the key.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.keys.remove(key)
            self._populate_keys()

    # ── Documentation tab ───────────────────────────────────────────────────────
    def _build_docs_tab(self):
        w = QWidget()
        lay = QHBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)

        # Endpoint list
        sidebar = QWidget()
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet("background:#0b0e14;border-right:1px solid #1e2433;")
        sl = QVBoxLayout(sidebar)
        sl.setContentsMargins(0, 0, 0, 0)

        from PyQt6.QtWidgets import QListWidget, QListWidgetItem
        endpoint_list = QListWidget()
        endpoint_list.setStyleSheet(
            "QListWidget{border:none;background:#0b0e14;}"
            "QListWidget::item{padding:10px 14px;border-bottom:1px solid #1a2035;}"
            "QListWidget::item:selected{background:#1a2a4a;color:#3b82f6;}"
        )
        endpoints = [
            "GET  /profiles",
            "POST  /profiles",
            "GET  /profiles/{id}",
            "PUT  /profiles/{id}",
            "DELETE  /profiles/{id}",
            "POST  /profiles/{id}/start",
            "POST  /profiles/{id}/stop",
            "GET  /profiles/{id}/status",
            "POST  /profiles/batch",
            "GET  /groups",
            "GET  /team/members",
        ]
        for e in endpoints:
            item = QListWidgetItem(f"  {e}")
            endpoint_list.addItem(item)
        sl.addWidget(endpoint_list, 1)
        lay.addWidget(sidebar)

        # Doc content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        content = QWidget()
        cl = QVBoxLayout(content)
        cl.setContentsMargins(24, 20, 24, 20)
        cl.setSpacing(16)

        cl.addWidget(self._doc_title("API Documentation"))

        base_gb = QGroupBox("Base URL")
        bl = QVBoxLayout(base_gb)
        base_url = QLineEdit("https://api.khbrowser.io/v1")
        base_url.setReadOnly(True)
        bl.addWidget(base_url)
        cl.addWidget(base_gb)

        auth_gb = QGroupBox("Authentication")
        al = QVBoxLayout(auth_gb)
        auth_info = QLabel(
            "All API requests must include your API key in the Authorization header:\n\n"
            "  Authorization: Bearer ak_live_your_api_key_here"
        )
        auth_info.setStyleSheet("font-family:monospace;color:#a5f3fc;")
        al.addWidget(auth_info)
        cl.addWidget(auth_gb)

        # Sample endpoints
        for method, endpoint, desc, example in [
            ("GET", "/profiles", "List all profiles",
             '{"profiles": [...], "total": 8, "page": 1}'),
            ("POST", "/profiles/{id}/start", "Launch a browser profile",
             '{"status": "running", "debug_port": 9222, "ws_url": "ws://..."}'),
            ("POST", "/profiles", "Create a new profile",
             '{"id": "A1B2C3D4", "name": "My Profile", "status": "stopped"}'),
        ]:
            self._add_endpoint_doc(cl, method, endpoint, desc, example)

        cl.addStretch()
        scroll.setWidget(content)
        lay.addWidget(scroll, 1)
        return w

    def _doc_title(self, text):
        lb = QLabel(text)
        lb.setStyleSheet("font-size:20px;font-weight:700;color:#e2e8f0;")
        return lb

    def _add_endpoint_doc(self, lay, method, endpoint, desc, example):
        gb = QGroupBox()
        gb.setStyleSheet("QGroupBox{border:1px solid #1e2433;border-radius:8px;padding:12px;margin-top:4px;}")
        gl = QVBoxLayout(gb)

        hl = QHBoxLayout()
        colors = {"GET": ("background:#064e3b;color:#6ee7b7;"),
                  "POST": ("background:#1e3a5f;color:#93c5fd;"),
                  "DELETE": ("background:#7f1d1d;color:#fca5a5;")}
        method_lb = _badge(method, colors.get(method, ""))
        ep_lb = QLabel(endpoint)
        ep_lb.setStyleSheet("font-family:monospace;font-size:14px;color:#e2e8f0;font-weight:600;")
        hl.addWidget(method_lb)
        hl.addWidget(ep_lb, 1)
        gl.addLayout(hl)

        desc_lb = QLabel(desc)
        desc_lb.setStyleSheet("color:#64748b;margin:4px 0;")
        gl.addWidget(desc_lb)

        resp_lb = QLabel("Response example:")
        resp_lb.setStyleSheet("color:#94a3b8;font-size:11px;font-weight:600;text-transform:uppercase;")
        gl.addWidget(resp_lb)
        code = QPlainTextEdit(example)
        code.setReadOnly(True)
        code.setObjectName("codeEditor")
        code.setMaximumHeight(70)
        gl.addWidget(code)
        lay.addWidget(gb)

    # ── Logs tab ────────────────────────────────────────────────────────────────
    def _build_logs_tab(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(20, 16, 20, 16)

        hl = QHBoxLayout()
        filter_combo = QComboBox()
        for f in ["All Requests", "2xx Success", "4xx Client Error", "5xx Server Error"]:
            filter_combo.addItem(f)
        key_filter = QComboBox()
        key_filter.addItem("All API Keys")
        for k in self.keys:
            key_filter.addItem(k.name)
        hl.addWidget(QLabel("Filter:"))
        hl.addWidget(filter_combo)
        hl.addWidget(key_filter)
        hl.addStretch()
        lay.addLayout(hl)

        cols = ["Timestamp", "Method", "Endpoint", "Status", "Duration", "API Key"]
        tbl = QTableWidget(0, len(cols))
        tbl.setHorizontalHeaderLabels(cols)
        tbl.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        tbl.verticalHeader().setVisible(False)
        tbl.setAlternatingRowColors(True)

        import random
        methods = ["GET", "POST", "DELETE"]
        endpoints = ["/profiles", "/profiles/{id}/start", "/profiles/{id}/stop", "/profiles/{id}"]
        for _ in range(20):
            r = tbl.rowCount()
            tbl.insertRow(r)
            tbl.setRowHeight(r, 36)
            import datetime
            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            m = random.choice(methods)
            ep = random.choice(endpoints)
            status = random.choice(["200", "201", "400", "404"])
            dur = f"{random.randint(20, 500)}ms"
            tbl.setItem(r, 0, QTableWidgetItem(f"  {ts}"))
            colors = {"GET": "background:#064e3b;color:#6ee7b7;",
                      "POST": "background:#1e3a5f;color:#93c5fd;",
                      "DELETE": "background:#7f1d1d;color:#fca5a5;"}
            mw = QWidget()
            ml = QHBoxLayout(mw)
            ml.setContentsMargins(4, 4, 4, 4)
            ml.addWidget(_badge(m, colors.get(m, "")))
            ml.addStretch()
            tbl.setCellWidget(r, 1, mw)
            tbl.setItem(r, 2, QTableWidgetItem(ep))
            sc = QWidget()
            scl = QHBoxLayout(sc)
            scl.setContentsMargins(4, 4, 4, 4)
            color = "background:#064e3b;color:#6ee7b7;" if status.startswith("2") else "background:#7f1d1d;color:#fca5a5;"
            scl.addWidget(_badge(status, color))
            scl.addStretch()
            tbl.setCellWidget(r, 3, sc)
            tbl.setItem(r, 4, QTableWidgetItem(dur))
            tbl.setItem(r, 5, QTableWidgetItem(self.keys[0].name if self.keys else "—"))
        lay.addWidget(tbl, 1)
        return w
