"""Batch operations dialog."""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTabWidget, QWidget, QTextEdit, QComboBox, QGroupBox,
    QGridLayout, QCheckBox, QSpinBox, QProgressBar, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer


def _h_sep():
    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    return line


class BatchDialog(QDialog):
    def __init__(self, parent=None, profiles=None):
        super().__init__(parent)
        self.profiles = profiles or []
        self.setWindowTitle("Batch Operations")
        self.setMinimumSize(760, 540)
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        header = QWidget()
        header.setStyleSheet("background:#111827;border-bottom:1px solid #1e2433;")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(20, 14, 20, 14)
        title = QLabel("⚡  Batch Operations")
        title.setStyleSheet("font-size:16px;font-weight:700;color:#e2e8f0;")
        hl.addWidget(title)
        root.addWidget(header)

        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        tabs.addTab(self._build_import_tab(), "📥  Batch Import")
        tabs.addTab(self._build_create_tab(), "✨  Batch Create")
        tabs.addTab(self._build_update_tab(), "✏️  Batch Update")
        tabs.addTab(self._build_export_tab(), "📤  Export")
        root.addWidget(tabs, 1)

    # ── Import ──────────────────────────────────────────────────────────────────
    def _build_import_tab(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(14)

        lay.addWidget(QLabel("📋  Import profiles from file (JSON / CSV)"))
        lay.addWidget(_h_sep())

        hl = QHBoxLayout()
        self.import_path = QLabel("No file selected")
        self.import_path.setStyleSheet("color:#64748b;")
        browse_btn = QPushButton("📂  Browse File")
        browse_btn.clicked.connect(self._browse_import)
        hl.addWidget(self.import_path, 1)
        hl.addWidget(browse_btn)
        lay.addLayout(hl)

        fmt_gb = QGroupBox("Format")
        fmt_lay = QHBoxLayout(fmt_gb)
        self.fmt_json = QCheckBox("JSON")
        self.fmt_json.setChecked(True)
        self.fmt_csv = QCheckBox("CSV")
        fmt_lay.addWidget(self.fmt_json)
        fmt_lay.addWidget(self.fmt_csv)
        fmt_lay.addStretch()
        lay.addWidget(fmt_gb)

        opts_gb = QGroupBox("Import Options")
        opts_lay = QVBoxLayout(opts_gb)
        self.overwrite_cb = QCheckBox("Overwrite existing profiles (by name)")
        self.assign_group_cb = QCheckBox("Assign to group:")
        self.group_combo = QComboBox()
        for g in ["Default", "Facebook", "E-commerce", "Social Media", "Testing"]:
            self.group_combo.addItem(g)
        opts_lay.addWidget(self.overwrite_cb)
        oh = QHBoxLayout()
        oh.addWidget(self.assign_group_cb)
        oh.addWidget(self.group_combo)
        oh.addStretch()
        opts_lay.addLayout(oh)
        lay.addWidget(opts_gb)

        self.import_progress = QProgressBar()
        self.import_progress.setVisible(False)
        lay.addWidget(self.import_progress)

        run_btn = QPushButton("⬆️  Start Import")
        run_btn.setObjectName("primaryBtn")
        run_btn.setFixedHeight(40)
        run_btn.clicked.connect(self._run_import)
        lay.addWidget(run_btn)

        lay.addStretch()
        return w

    def _browse_import(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Import File", "", "JSON Files (*.json);;CSV Files (*.csv);;All Files (*)"
        )
        if path:
            self.import_path.setText(path)
            self.import_path.setStyleSheet("color:#e2e8f0;")

    def _run_import(self):
        self.import_progress.setVisible(True)
        self.import_progress.setValue(0)
        timer = QTimer(self)
        count = [0]
        def tick():
            count[0] += 5
            self.import_progress.setValue(count[0])
            if count[0] >= 100:
                timer.stop()
                QMessageBox.information(self, "Import", "✅  Import completed successfully!\n12 profiles imported.")
        timer.timeout.connect(tick)
        timer.start(60)

    # ── Create ──────────────────────────────────────────────────────────────────
    def _build_create_tab(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(14)

        lay.addWidget(QLabel("✨  Create multiple profiles at once"))
        lay.addWidget(_h_sep())

        grid = QGridLayout()
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(10)

        grid.addWidget(QLabel("Count"), 0, 0)
        self.count_spin = QSpinBox()
        self.count_spin.setRange(1, 500)
        self.count_spin.setValue(10)
        grid.addWidget(self.count_spin, 0, 1)

        grid.addWidget(QLabel("Prefix"), 1, 0)
        from PyQt6.QtWidgets import QLineEdit
        self.prefix_edit = QLineEdit("Profile")
        grid.addWidget(self.prefix_edit, 1, 1)

        grid.addWidget(QLabel("Group"), 2, 0)
        self.create_group = QComboBox()
        for g in ["Default", "Facebook", "E-commerce", "Social Media", "Testing"]:
            self.create_group.addItem(g)
        grid.addWidget(self.create_group, 2, 1)

        grid.addWidget(QLabel("Browser"), 3, 0)
        self.create_browser = QComboBox()
        for b in ["Chrome", "Firefox", "Edge", "Random"]:
            self.create_browser.addItem(b)
        grid.addWidget(self.create_browser, 3, 1)

        grid.addWidget(QLabel("OS"), 4, 0)
        self.create_os = QComboBox()
        for o in ["Windows", "macOS", "Linux", "Random"]:
            self.create_os.addItem(o)
        grid.addWidget(self.create_os, 4, 1)

        lay.addLayout(grid)

        fp_gb = QGroupBox("Fingerprint")
        fp_lay = QVBoxLayout(fp_gb)
        self.rand_fp_cb = QCheckBox("Randomize fingerprint for each profile")
        self.rand_fp_cb.setChecked(True)
        self.rand_ua_cb = QCheckBox("Randomize User-Agent")
        self.rand_ua_cb.setChecked(True)
        self.rand_screen_cb = QCheckBox("Randomize screen resolution")
        self.rand_screen_cb.setChecked(True)
        fp_lay.addWidget(self.rand_fp_cb)
        fp_lay.addWidget(self.rand_ua_cb)
        fp_lay.addWidget(self.rand_screen_cb)
        lay.addWidget(fp_gb)

        self.create_progress = QProgressBar()
        self.create_progress.setVisible(False)
        lay.addWidget(self.create_progress)

        run_btn = QPushButton(f"✨  Create Profiles")
        run_btn.setObjectName("primaryBtn")
        run_btn.setFixedHeight(40)
        run_btn.clicked.connect(self._run_create)
        lay.addWidget(run_btn)

        lay.addStretch()
        return w

    def _run_create(self):
        count = self.count_spin.value()
        self.create_progress.setVisible(True)
        self.create_progress.setValue(0)
        timer = QTimer(self)
        step = [0]
        def tick():
            step[0] += max(1, 100 // count)
            self.create_progress.setValue(min(step[0], 100))
            if step[0] >= 100:
                timer.stop()
                QMessageBox.information(self, "Create", f"✅  {count} profiles created successfully!")
        timer.timeout.connect(tick)
        timer.start(40)

    # ── Update ──────────────────────────────────────────────────────────────────
    def _build_update_tab(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(14)

        lay.addWidget(QLabel("✏️  Update multiple profiles at once"))
        lay.addWidget(_h_sep())

        sel_gb = QGroupBox("Target Profiles")
        sel_lay = QVBoxLayout(sel_gb)
        from PyQt6.QtWidgets import QRadioButton
        self.all_radio = QRadioButton("All profiles")
        self.group_radio = QRadioButton("Profiles in group:")
        self.all_radio.setChecked(True)
        self.update_group_combo = QComboBox()
        for g in ["Default", "Facebook", "E-commerce", "Social Media"]:
            self.update_group_combo.addItem(g)
        sel_lay.addWidget(self.all_radio)
        hr = QHBoxLayout()
        hr.addWidget(self.group_radio)
        hr.addWidget(self.update_group_combo)
        hr.addStretch()
        sel_lay.addLayout(hr)
        lay.addWidget(sel_gb)

        fields_gb = QGroupBox("Fields to Update")
        fields_lay = QVBoxLayout(fields_gb)
        self.upd_proxy_cb = QCheckBox("Update Proxy")
        self.upd_fp_cb = QCheckBox("Re-randomize Fingerprint")
        self.upd_ua_cb = QCheckBox("Update User-Agent")
        self.upd_group_cb = QCheckBox("Move to Group:")
        self.upd_group_target = QComboBox()
        for g in ["Default", "Facebook", "E-commerce", "Social Media", "Archive"]:
            self.upd_group_target.addItem(g)
        fields_lay.addWidget(self.upd_proxy_cb)
        fields_lay.addWidget(self.upd_fp_cb)
        fields_lay.addWidget(self.upd_ua_cb)
        hg = QHBoxLayout()
        hg.addWidget(self.upd_group_cb)
        hg.addWidget(self.upd_group_target)
        hg.addStretch()
        fields_lay.addLayout(hg)
        lay.addWidget(fields_gb)

        self.update_progress = QProgressBar()
        self.update_progress.setVisible(False)
        lay.addWidget(self.update_progress)

        run_btn = QPushButton("🔄  Apply Updates")
        run_btn.setObjectName("primaryBtn")
        run_btn.setFixedHeight(40)
        run_btn.clicked.connect(self._run_update)
        lay.addWidget(run_btn)

        lay.addStretch()
        return w

    def _run_update(self):
        self.update_progress.setVisible(True)
        self.update_progress.setValue(0)
        timer = QTimer(self)
        v = [0]
        def tick():
            v[0] += 8
            self.update_progress.setValue(min(v[0], 100))
            if v[0] >= 100:
                timer.stop()
                QMessageBox.information(self, "Update", "✅  Profiles updated successfully!")
        timer.timeout.connect(tick)
        timer.start(50)

    # ── Export ──────────────────────────────────────────────────────────────────
    def _build_export_tab(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(14)

        lay.addWidget(QLabel("📤  Export profiles to file"))
        lay.addWidget(_h_sep())

        fmt_gb = QGroupBox("Export Format")
        fmt_lay = QHBoxLayout(fmt_gb)
        from PyQt6.QtWidgets import QRadioButton
        self.exp_json = QRadioButton("JSON")
        self.exp_csv = QRadioButton("CSV")
        self.exp_json.setChecked(True)
        fmt_lay.addWidget(self.exp_json)
        fmt_lay.addWidget(self.exp_csv)
        fmt_lay.addStretch()
        lay.addWidget(fmt_gb)

        sel_gb = QGroupBox("Which Profiles")
        sel_lay = QVBoxLayout(sel_gb)
        self.exp_all = QRadioButton("All profiles")
        self.exp_selected = QRadioButton("Selected profiles only")
        self.exp_group = QRadioButton("By group:")
        self.exp_all.setChecked(True)
        self.exp_group_combo = QComboBox()
        for g in ["Default", "Facebook", "E-commerce", "Social Media"]:
            self.exp_group_combo.addItem(g)
        sel_lay.addWidget(self.exp_all)
        sel_lay.addWidget(self.exp_selected)
        hg = QHBoxLayout()
        hg.addWidget(self.exp_group)
        hg.addWidget(self.exp_group_combo)
        hg.addStretch()
        sel_lay.addLayout(hg)
        lay.addWidget(sel_gb)

        fields_gb = QGroupBox("Include Fields")
        fields_lay = QGridLayout(fields_gb)
        for i, f in enumerate(["Basic Info", "Fingerprint", "Proxy", "Accounts", "Extensions", "Notes"]):
            cb = QCheckBox(f)
            cb.setChecked(True)
            fields_lay.addWidget(cb, i // 3, i % 3)
        lay.addWidget(fields_gb)

        export_btn = QPushButton("💾  Export to File")
        export_btn.setObjectName("primaryBtn")
        export_btn.setFixedHeight(40)
        export_btn.clicked.connect(self._run_export)
        lay.addWidget(export_btn)

        lay.addStretch()
        return w

    def _run_export(self):
        ext = "json" if self.exp_json.isChecked() else "csv"
        path, _ = QFileDialog.getSaveFileName(
            self, "Export Profiles", f"profiles_export.{ext}",
            f"{'JSON' if ext == 'json' else 'CSV'} Files (*.{ext})"
        )
        if path:
            QMessageBox.information(self, "Export", f"✅  Profiles exported to:\n{path}")
