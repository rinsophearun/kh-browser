"""RPA Tasks dialog."""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget,
    QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView,
    QAbstractItemView, QFrame, QLineEdit, QComboBox, QGroupBox,
    QPlainTextEdit, QTextEdit, QSplitter, QListWidget, QListWidgetItem,
    QMessageBox, QProgressBar, QDialogButtonBox, QCheckBox, QSpinBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor
from models import RPATask, SAMPLE_TASKS, SAMPLE_PROFILES


def _badge_label(text, color_style):
    lb = QLabel(text)
    lb.setAlignment(Qt.AlignmentFlag.AlignCenter)
    lb.setStyleSheet(
        f"{color_style}border-radius:10px;padding:2px 8px;font-size:11px;font-weight:600;"
    )
    return lb


STATUS_STYLES = {
    "idle":      "background:#1e2433;color:#64748b;",
    "running":   "background:#064e3b;color:#6ee7b7;",
    "completed": "background:#1e3a5f;color:#93c5fd;",
    "failed":    "background:#7f1d1d;color:#fca5a5;",
    "scheduled": "background:#451a03;color:#fcd34d;",
}


class TaskEditorDialog(QDialog):
    def __init__(self, parent=None, task: RPATask = None):
        super().__init__(parent)
        self.task = task or RPATask()
        self.is_new = task is None
        self.setWindowTitle("New RPA Task" if self.is_new else f"Edit: {self.task.name}")
        self.setMinimumSize(820, 600)
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        header = QWidget()
        header.setStyleSheet("background:#111827;border-bottom:1px solid #1e2433;")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(20, 14, 20, 14)
        title = QLabel("🤖  " + ("New RPA Task" if self.is_new else f"Edit Task"))
        title.setStyleSheet("font-size:16px;font-weight:700;color:#e2e8f0;")
        hl.addWidget(title)
        root.addWidget(header)

        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        tabs.addTab(self._build_script_tab(), "📝  Script")
        tabs.addTab(self._build_profiles_tab(), "📋  Target Profiles")
        tabs.addTab(self._build_schedule_tab(), "⏰  Schedule")
        root.addWidget(tabs, 1)

        footer = QWidget()
        footer.setStyleSheet("background:#111827;border-top:1px solid #1e2433;")
        fl = QHBoxLayout(footer)
        fl.setContentsMargins(20, 12, 20, 12)
        run_btn = QPushButton("▶️  Run Now")
        run_btn.setObjectName("successBtn")
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        save_btn = QPushButton("💾  Save Task")
        save_btn.setObjectName("primaryBtn")
        save_btn.setFixedHeight(38)
        save_btn.clicked.connect(self.accept)
        fl.addWidget(run_btn)
        fl.addStretch()
        fl.addWidget(cancel_btn)
        fl.addSpacing(8)
        fl.addWidget(save_btn)
        root.addWidget(footer)

    def _build_script_tab(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(20, 16, 20, 16)
        lay.setSpacing(12)

        hl = QHBoxLayout()
        hl.addWidget(QLabel("Task Name:"))
        self.name_edit = QLineEdit(self.task.name)
        self.name_edit.setPlaceholderText("e.g. Auto Login Facebook")
        hl.addWidget(self.name_edit, 1)
        lay.addLayout(hl)

        hl2 = QHBoxLayout()
        hl2.addWidget(QLabel("Description:"))
        self.desc_edit = QLineEdit(self.task.description)
        self.desc_edit.setPlaceholderText("Brief description of what this task does")
        hl2.addWidget(self.desc_edit, 1)
        lay.addLayout(hl2)

        lay.addWidget(QLabel("Automation Script (JavaScript / Playwright):"))

        toolbar = QHBoxLayout()
        for label, snippet in [
            ("goto(url)", "await page.goto('https://example.com');"),
            ("click", "await page.click('#selector');"),
            ("fill", "await page.fill('#input', 'value');"),
            ("wait", "await page.waitForSelector('#element');"),
            ("screenshot", "await page.screenshot({path: 'screenshot.png'});"),
        ]:
            btn = QPushButton(label)
            btn.setObjectName("iconBtn")
            btn.setFixedHeight(26)
            btn.setStyleSheet("font-size:11px;border:1px solid #2d3748;")
            btn.clicked.connect(lambda _, s=snippet: self._insert_snippet(s))
            toolbar.addWidget(btn)
        toolbar.addStretch()
        lay.addLayout(toolbar)

        self.script_edit = QPlainTextEdit(self.task.script)
        self.script_edit.setObjectName("codeEditor")
        self.script_edit.setMinimumHeight(280)
        lay.addWidget(self.script_edit, 1)
        return w

    def _insert_snippet(self, snippet):
        self.script_edit.insertPlainText("\n" + snippet)

    def _build_profiles_tab(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(20, 16, 20, 16)
        lay.setSpacing(10)
        lay.addWidget(QLabel("Select profiles to run this task on:"))

        hl = QHBoxLayout()
        search = QLineEdit()
        search.setPlaceholderText("🔍  Search profiles…")
        search.setObjectName("searchBox")
        sel_all = QPushButton("Select All")
        sel_none = QPushButton("Clear")
        hl.addWidget(search, 1)
        hl.addWidget(sel_all)
        hl.addWidget(sel_none)
        lay.addLayout(hl)

        self.profile_list = QListWidget()
        for p in SAMPLE_PROFILES:
            item = QListWidgetItem(f"  {p.name}  [{p.group}]  •  {p.browser_type}/{p.os_type}")
            item.setData(Qt.ItemDataRole.UserRole, p.id)
            item.setCheckState(
                Qt.CheckState.Checked if p.id in self.task.profile_ids
                else Qt.CheckState.Unchecked
            )
            self.profile_list.addItem(item)
        lay.addWidget(self.profile_list, 1)

        sel_all.clicked.connect(lambda: [
            self.profile_list.item(i).setCheckState(Qt.CheckState.Checked)
            for i in range(self.profile_list.count())
        ])
        sel_none.clicked.connect(lambda: [
            self.profile_list.item(i).setCheckState(Qt.CheckState.Unchecked)
            for i in range(self.profile_list.count())
        ])
        return w

    def _build_schedule_tab(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(14)

        self.schedule_cb = QCheckBox("Enable Scheduling")
        self.schedule_cb.setChecked(bool(self.task.schedule))
        lay.addWidget(self.schedule_cb)

        from PyQt6.QtWidgets import QRadioButton, QDateTimeEdit
        from PyQt6.QtCore import QDateTime
        self.once_radio = QRadioButton("Run once")
        self.daily_radio = QRadioButton("Daily")
        self.weekly_radio = QRadioButton("Weekly")
        self.once_radio.setChecked(True)
        for r in [self.once_radio, self.daily_radio, self.weekly_radio]:
            lay.addWidget(r)

        dt_lay = QHBoxLayout()
        dt_lay.addWidget(QLabel("Start at:"))
        self.dt_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.dt_edit.setCalendarPopup(True)
        dt_lay.addWidget(self.dt_edit)
        dt_lay.addStretch()
        lay.addLayout(dt_lay)

        cc_lay = QHBoxLayout()
        cc_lay.addWidget(QLabel("Concurrent profiles:"))
        self.concurrent_spin = QSpinBox()
        self.concurrent_spin.setRange(1, 50)
        self.concurrent_spin.setValue(1)
        cc_lay.addWidget(self.concurrent_spin)
        cc_lay.addStretch()
        lay.addLayout(cc_lay)

        lay.addStretch()
        return w


class RPADialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tasks = list(SAMPLE_TASKS)
        self.setWindowTitle("RPA Tasks")
        self.setMinimumSize(960, 620)
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        header = QWidget()
        header.setStyleSheet("background:#111827;border-bottom:1px solid #1e2433;")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(20, 14, 20, 14)
        title = QLabel("🤖  RPA Task Manager")
        title.setStyleSheet("font-size:16px;font-weight:700;color:#e2e8f0;")
        new_btn = QPushButton("➕  New Task")
        new_btn.setObjectName("primaryBtn")
        new_btn.clicked.connect(self._new_task)
        hl.addWidget(title)
        hl.addStretch()
        hl.addWidget(new_btn)
        root.addWidget(header)

        # Main content
        content = QWidget()
        cl = QHBoxLayout(content)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(0)

        # Task list
        left = QWidget()
        left.setFixedWidth(320)
        left.setStyleSheet("border-right:1px solid #1e2433;")
        ll = QVBoxLayout(left)
        ll.setContentsMargins(0, 0, 0, 0)
        ll.setSpacing(0)

        search_bar = QWidget()
        search_bar.setStyleSheet("background:#111827;border-bottom:1px solid #1e2433;padding:8px;")
        sl = QHBoxLayout(search_bar)
        sl.setContentsMargins(10, 6, 10, 6)
        search = QLineEdit()
        search.setPlaceholderText("🔍  Search tasks…")
        search.setObjectName("searchBox")
        sl.addWidget(search)
        ll.addWidget(search_bar)

        self.task_list = QListWidget()
        self.task_list.setStyleSheet(
            "QListWidget{border:none;background:#0b0e14;}"
            "QListWidget::item{padding:12px 14px;border-bottom:1px solid #1a2035;}"
            "QListWidget::item:selected{background:#1a2a4a;}"
        )
        self.task_list.currentRowChanged.connect(self._show_task)
        ll.addWidget(self.task_list, 1)

        for t in self.tasks:
            self._add_task_item(t)

        cl.addWidget(left)

        # Detail panel
        self.detail_panel = QWidget()
        self.detail_panel.setStyleSheet("background:#0f1117;")
        dl = QVBoxLayout(self.detail_panel)
        dl.setContentsMargins(24, 24, 24, 24)
        dl.setSpacing(16)

        self.detail_title = QLabel("Select a task")
        self.detail_title.setStyleSheet("font-size:18px;font-weight:700;color:#e2e8f0;")
        self.detail_desc = QLabel()
        self.detail_desc.setStyleSheet("color:#64748b;")
        self.detail_status = QLabel()
        self.detail_runs = QLabel()
        self.detail_runs.setStyleSheet("color:#64748b;font-size:12px;")

        top_row = QHBoxLayout()
        top_row.addWidget(self.detail_title, 1)
        top_row.addWidget(self.detail_status)

        dl.addLayout(top_row)
        dl.addWidget(self.detail_desc)
        dl.addWidget(self.detail_runs)
        dl.addWidget(self._make_separator())

        # Script preview
        script_label = QLabel("Script Preview:")
        script_label.setStyleSheet("font-weight:600;color:#94a3b8;font-size:12px;text-transform:uppercase;")
        dl.addWidget(script_label)
        self.script_preview = QPlainTextEdit()
        self.script_preview.setObjectName("codeEditor")
        self.script_preview.setReadOnly(True)
        dl.addWidget(self.script_preview, 1)

        # Progress
        self.task_progress = QProgressBar()
        self.task_progress.setVisible(False)
        dl.addWidget(self.task_progress)

        # Action buttons
        btn_row = QHBoxLayout()
        self.run_btn = QPushButton("▶️  Run Task")
        self.run_btn.setObjectName("successBtn")
        self.run_btn.setFixedHeight(38)
        self.run_btn.clicked.connect(self._run_task)
        self.stop_btn = QPushButton("⏹  Stop")
        self.stop_btn.setObjectName("dangerBtn")
        self.stop_btn.setFixedHeight(38)
        self.stop_btn.setVisible(False)
        self.edit_btn = QPushButton("✏️  Edit")
        self.edit_btn.setFixedHeight(38)
        self.edit_btn.clicked.connect(self._edit_task)
        self.clone_btn = QPushButton("📋  Clone")
        self.clone_btn.setFixedHeight(38)
        self.delete_btn = QPushButton("🗑  Delete")
        self.delete_btn.setObjectName("dangerBtn")
        self.delete_btn.setFixedHeight(38)
        for b in [self.run_btn, self.stop_btn, self.edit_btn, self.clone_btn, self.delete_btn]:
            btn_row.addWidget(b)
        btn_row.addStretch()
        dl.addLayout(btn_row)

        cl.addWidget(self.detail_panel, 1)
        root.addWidget(content, 1)

        if self.tasks:
            self.task_list.setCurrentRow(0)

    def _make_separator(self):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        return line

    def _add_task_item(self, task: RPATask):
        item = QListWidgetItem()
        item.setData(Qt.ItemDataRole.UserRole, task)
        item.setSizeHint(item.sizeHint().__class__(320, 72))
        self.task_list.addItem(item)
        # Custom widget for item
        w = QWidget()
        wl = QVBoxLayout(w)
        wl.setContentsMargins(14, 10, 14, 10)
        wl.setSpacing(4)
        hl = QHBoxLayout()
        name_lb = QLabel(f"🤖  {task.name}")
        name_lb.setStyleSheet("font-weight:600;color:#e2e8f0;font-size:13px;")
        status_lb = _badge_label(task.status.upper(), STATUS_STYLES.get(task.status, ""))
        hl.addWidget(name_lb, 1)
        hl.addWidget(status_lb)
        desc_lb = QLabel(task.description[:50] + ("…" if len(task.description) > 50 else ""))
        desc_lb.setStyleSheet("color:#64748b;font-size:12px;")
        wl.addLayout(hl)
        wl.addWidget(desc_lb)
        w.setStyleSheet("background:transparent;")
        self.task_list.setItemWidget(item, w)

    def _show_task(self, row):
        if row < 0 or row >= len(self.tasks):
            return
        task = self.tasks[row]
        self.detail_title.setText(f"🤖  {task.name}")
        self.detail_desc.setText(task.description)
        self.detail_status.setParent(None)
        self.detail_status = _badge_label(task.status.upper(), STATUS_STYLES.get(task.status, ""))
        self.script_preview.setPlainText(task.script)
        self.detail_runs.setText(
            f"  Run count: {task.run_count}  •  Last run: {task.last_run or 'Never'}"
            f"  •  Created: {task.created_at}"
        )

    def _run_task(self):
        self.task_progress.setVisible(True)
        self.task_progress.setValue(0)
        self.run_btn.setVisible(False)
        self.stop_btn.setVisible(True)
        timer = QTimer(self)
        v = [0]
        def tick():
            v[0] += 3
            self.task_progress.setValue(min(v[0], 100))
            if v[0] >= 100:
                timer.stop()
                self.task_progress.setVisible(False)
                self.run_btn.setVisible(True)
                self.stop_btn.setVisible(False)
                QMessageBox.information(self, "Task Complete", "✅  RPA task completed successfully!")
        timer.timeout.connect(tick)
        timer.start(80)

    def _new_task(self):
        dlg = TaskEditorDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            task = RPATask(name=dlg.name_edit.text(), description=dlg.desc_edit.text(),
                          script=dlg.script_edit.toPlainText())
            self.tasks.append(task)
            self._add_task_item(task)

    def _edit_task(self):
        row = self.task_list.currentRow()
        if 0 <= row < len(self.tasks):
            dlg = TaskEditorDialog(self, self.tasks[row])
            dlg.exec()
