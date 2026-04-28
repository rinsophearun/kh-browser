# -*- coding: utf-8 -*-
"""RPA / Automation Tasks — full-featured dialog."""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget,
    QTabWidget, QFrame, QLineEdit, QComboBox, QListWidget, QListWidgetItem,
    QMessageBox, QProgressBar, QCheckBox, QSpinBox, QPlainTextEdit,
    QRadioButton, QDateTimeEdit, QScrollArea, QGridLayout, QSizePolicy,
    QToolButton, QMenu, QApplication, QSplitter,
)
from PyQt6.QtCore import Qt, QTimer, QDateTime, QSize, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QIcon, QTextCursor
from models import RPATask, SAMPLE_TASKS, SAMPLE_PROFILES
import datetime, random


# ─── helpers ──────────────────────────────────────────────────────────────────

STATUS_STYLE = {
    "idle":      ("●", "#64748b", "#1e2433"),
    "running":   ("●", "#6ee7b7", "#064e3b"),
    "completed": ("●", "#93c5fd", "#1e3a5f"),
    "failed":    ("●", "#fca5a5", "#7f1d1d"),
    "scheduled": ("●", "#fcd34d", "#451a03"),
    "paused":    ("●", "#fb923c", "#431407"),
}

TEMPLATES = {
    "Auto Login": """\
// ── Auto Login Template ──────────────────────────────────────────────
await page.goto('{url}');
await page.waitForSelector('#email', { timeout: 10000 });
await page.fill('#email', '{username}');
await page.fill('#password', '{password}');
await page.click('[type="submit"]');
await page.waitForNavigation({ waitUntil: 'networkidle' });
console.log('Login success:', page.url());
""",
    "Scrape Data": """\
// ── Data Scraper Template ─────────────────────────────────────────────
await page.goto('{url}');
await page.waitForSelector('.item-list', { timeout: 15000 });

const items = await page.$$eval('.item', nodes =>
  nodes.map(n => ({
    title: n.querySelector('.title')?.innerText,
    price: n.querySelector('.price')?.innerText,
    url:   n.querySelector('a')?.href,
  }))
);

console.log(`Scraped ${items.length} items`);
// Items stored in task results
""",
    "Post Content": """\
// ── Post / Publish Template ──────────────────────────────────────────
await page.goto('{platform_url}');
await page.waitForSelector('[data-testid="compose"]');
await page.click('[data-testid="compose"]');
await page.fill('[role="textbox"]', '{content}');
await page.waitForTimeout(1000);
await page.click('[data-testid="post-btn"]');
await page.waitForSelector('[data-testid="success"]');
console.log('Posted successfully!');
""",
    "Account Warmup": """\
// ── Account Warmup Template ──────────────────────────────────────────
const urls = [
  'https://google.com',
  'https://youtube.com',
  'https://reddit.com',
  'https://twitter.com',
];

for (const url of urls) {
  await page.goto(url);
  await page.waitForTimeout(Math.random() * 3000 + 2000);
  await page.mouse.move(
    Math.random() * 800 + 100,
    Math.random() * 600 + 100
  );
  await page.waitForTimeout(1500);
  console.log('Visited:', url);
}
""",
    "Cookie Collector": """\
// ── Cookie Collector Template ─────────────────────────────────────────
await page.goto('{url}');
await page.waitForTimeout(3000);

const cookies = await page.context().cookies();
console.log(`Collected ${cookies.length} cookies`);

// Save important cookies
const session = cookies.filter(c =>
  ['session', 'auth', 'token'].some(k => c.name.toLowerCase().includes(k))
);
console.log('Session cookies:', session.map(c => c.name));
""",
    "Form Filler": """\
// ── Form Filler Template ──────────────────────────────────────────────
await page.goto('{form_url}');
await page.waitForSelector('form');

// Fill all text inputs with profile data
const fields = {
  '[name="firstName"]': '{first_name}',
  '[name="lastName"]':  '{last_name}',
  '[name="email"]':     '{email}',
  '[name="phone"]':     '{phone}',
};

for (const [selector, value] of Object.entries(fields)) {
  const el = await page.$(selector);
  if (el) await page.fill(selector, value);
}

await page.click('[type="submit"]');
console.log('Form submitted!');
""",
}

SNIPPET_LIBRARY = [
    ("🌐 goto",       "await page.goto('{url}');"),
    ("🖱 click",      "await page.click('{selector}');"),
    ("⌨ fill",       "await page.fill('{selector}', '{value}');"),
    ("⏳ wait",       "await page.waitForSelector('{selector}');"),
    ("💤 sleep",      "await page.waitForTimeout(2000);"),
    ("📷 screenshot", "await page.screenshot({ path: 'snap.png' });"),
    ("📜 scroll",     "await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));"),
    ("🔑 press",      "await page.keyboard.press('Enter');"),
    ("🍪 cookies",    "const cookies = await page.context().cookies();"),
    ("📋 getText",    "const text = await page.$eval('{sel}', el => el.textContent);"),
    ("🔀 random wait","await page.waitForTimeout(Math.floor(Math.random()*3000)+1000);"),
    ("🖱 hover",      "await page.hover('{selector}');"),
]


def _badge(text, dot_color, bg_color):
    lb = QLabel(f"  ● {text}  ")
    lb.setAlignment(Qt.AlignmentFlag.AlignCenter)
    lb.setStyleSheet(
        f"background:{bg_color};color:{dot_color};"
        "border-radius:10px;padding:2px 6px;font-size:11px;font-weight:700;"
        "letter-spacing:0.5px;"
    )
    return lb


def _sep():
    f = QFrame()
    f.setFrameShape(QFrame.Shape.HLine)
    f.setStyleSheet("color:#1e2433;")
    return f


# ─── Task Editor ──────────────────────────────────────────────────────────────

class TaskEditorDialog(QDialog):
    def __init__(self, parent=None, task: RPATask = None):
        super().__init__(parent)
        self.task = task or RPATask()
        self.is_new = task is None
        self.setWindowTitle("New Automation Task" if self.is_new else f"Edit: {self.task.name}")
        self.setMinimumSize(900, 650)
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Header
        hdr = QWidget()
        hdr.setStyleSheet("background:#111827;border-bottom:2px solid #ff8c00;")
        hl = QHBoxLayout(hdr)
        hl.setContentsMargins(20, 14, 20, 14)
        title = QLabel("🤖  " + ("New Automation Task" if self.is_new else "Edit Task"))
        title.setStyleSheet("font-size:16px;font-weight:700;color:#ff8c00;")
        hl.addWidget(title)
        hl.addStretch()
        # Template picker
        tmp_lbl = QLabel("Template:")
        tmp_lbl.setStyleSheet("color:#94a3b8;")
        self.tmp_combo = QComboBox()
        self.tmp_combo.addItem("— Load Template —")
        self.tmp_combo.addItems(list(TEMPLATES.keys()))
        self.tmp_combo.setFixedWidth(180)
        self.tmp_combo.currentTextChanged.connect(self._load_template)
        hl.addWidget(tmp_lbl)
        hl.addWidget(self.tmp_combo)
        root.addWidget(hdr)

        # Tabs
        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        tabs.setStyleSheet(
            "QTabWidget::pane{border:none;background:#0f1117;}"
            "QTabBar::tab{background:#111827;color:#64748b;padding:10px 20px;border:none;}"
            "QTabBar::tab:selected{background:#0f1117;color:#ff8c00;border-bottom:2px solid #ff8c00;}"
        )
        tabs.addTab(self._build_script_tab(), "  📝 Script  ")
        tabs.addTab(self._build_profiles_tab(), "  📋 Profiles  ")
        tabs.addTab(self._build_schedule_tab(), "  ⏰ Schedule  ")
        root.addWidget(tabs, 1)

        # Footer
        ftr = QWidget()
        ftr.setStyleSheet("background:#111827;border-top:1px solid #1e2433;")
        fl = QHBoxLayout(ftr)
        fl.setContentsMargins(20, 12, 20, 12)
        run_btn = QPushButton("  ▶  Run Now")
        run_btn.setStyleSheet(
            "background:#16a34a;color:#fff;font-weight:700;padding:8px 20px;"
            "border-radius:6px;border:none;font-size:13px;"
        )
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("color:#94a3b8;background:transparent;border:1px solid #2d3748;padding:8px 16px;border-radius:6px;")
        cancel_btn.clicked.connect(self.reject)
        save_btn = QPushButton("  💾  Save Task")
        save_btn.setStyleSheet(
            "background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #ff8c00,stop:1 #ea580c);"
            "color:#fff;font-weight:700;padding:8px 24px;border-radius:6px;border:none;font-size:13px;"
        )
        save_btn.clicked.connect(self.accept)
        fl.addWidget(run_btn)
        fl.addStretch()
        fl.addWidget(cancel_btn)
        fl.addSpacing(8)
        fl.addWidget(save_btn)
        root.addWidget(ftr)

    def _build_script_tab(self):
        w = QWidget()
        w.setStyleSheet("background:#0f1117;")
        lay = QVBoxLayout(w)
        lay.setContentsMargins(20, 16, 20, 16)
        lay.setSpacing(10)

        # Name + description row
        g = QGridLayout()
        g.setSpacing(8)
        name_lbl = QLabel("Task Name")
        name_lbl.setStyleSheet("color:#94a3b8;font-size:12px;font-weight:600;")
        self.name_edit = QLineEdit(self.task.name)
        self.name_edit.setPlaceholderText("e.g.  Auto Login Facebook")
        self.name_edit.setStyleSheet(
            "background:#111827;color:#e2e8f0;border:1px solid #2d3748;"
            "border-radius:6px;padding:8px 12px;font-size:13px;"
        )
        desc_lbl = QLabel("Description")
        desc_lbl.setStyleSheet("color:#94a3b8;font-size:12px;font-weight:600;")
        self.desc_edit = QLineEdit(self.task.description)
        self.desc_edit.setPlaceholderText("Brief description of what this task does")
        self.desc_edit.setStyleSheet(self.name_edit.styleSheet())
        g.addWidget(name_lbl, 0, 0)
        g.addWidget(self.name_edit, 1, 0)
        g.addWidget(desc_lbl, 0, 1)
        g.addWidget(self.desc_edit, 1, 1)
        lay.addLayout(g)

        # Snippet toolbar
        snip_lbl = QLabel("Quick Snippets")
        snip_lbl.setStyleSheet("color:#94a3b8;font-size:12px;font-weight:600;")
        lay.addWidget(snip_lbl)

        snip_scroll = QScrollArea()
        snip_scroll.setFixedHeight(44)
        snip_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        snip_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        snip_scroll.setStyleSheet("border:none;background:transparent;")
        snip_w = QWidget()
        snip_l = QHBoxLayout(snip_w)
        snip_l.setContentsMargins(0, 0, 0, 0)
        snip_l.setSpacing(6)
        for label, snippet in SNIPPET_LIBRARY:
            b = QPushButton(label)
            b.setFixedHeight(30)
            b.setStyleSheet(
                "background:#1e2433;color:#94a3b8;border:1px solid #2d3748;"
                "border-radius:5px;padding:2px 10px;font-size:11px;"
                "hover{background:#ff8c00;color:#fff;}"
            )
            b.clicked.connect(lambda _, s=snippet: self._insert(s))
            snip_l.addWidget(b)
        snip_l.addStretch()
        snip_scroll.setWidget(snip_w)
        snip_scroll.setWidgetResizable(True)
        lay.addWidget(snip_scroll)

        # Code editor
        code_lbl = QLabel("Automation Script  (JavaScript / Playwright)")
        code_lbl.setStyleSheet("color:#94a3b8;font-size:12px;font-weight:600;")
        lay.addWidget(code_lbl)
        self.script_edit = QPlainTextEdit(self.task.script)
        self.script_edit.setStyleSheet(
            "background:#0a0d13;color:#e2e8f0;font-family:monospace;font-size:13px;"
            "border:1px solid #2d3748;border-radius:6px;padding:8px;"
        )
        self.script_edit.setMinimumHeight(260)
        lay.addWidget(self.script_edit, 1)
        return w

    def _insert(self, snippet):
        self.script_edit.insertPlainText("\n" + snippet)

    def _load_template(self, name):
        if name in TEMPLATES:
            self.script_edit.setPlainText(TEMPLATES[name])

    def _build_profiles_tab(self):
        w = QWidget()
        w.setStyleSheet("background:#0f1117;")
        lay = QVBoxLayout(w)
        lay.setContentsMargins(20, 16, 20, 16)
        lay.setSpacing(10)

        top = QHBoxLayout()
        lbl = QLabel("Select profiles to run this task on:")
        lbl.setStyleSheet("color:#e2e8f0;font-size:13px;font-weight:600;")
        search = QLineEdit()
        search.setPlaceholderText("🔍  Search profiles…")
        search.setFixedWidth(220)
        search.setStyleSheet(
            "background:#111827;color:#e2e8f0;border:1px solid #2d3748;"
            "border-radius:6px;padding:6px 10px;"
        )
        sel_all = QPushButton("Select All")
        sel_none = QPushButton("Clear")
        for b in [sel_all, sel_none]:
            b.setStyleSheet(
                "background:#1e2433;color:#94a3b8;border:1px solid #2d3748;"
                "border-radius:5px;padding:6px 14px;"
            )
        top.addWidget(lbl, 1)
        top.addWidget(search)
        top.addWidget(sel_all)
        top.addWidget(sel_none)
        lay.addLayout(top)

        self.profile_list = QListWidget()
        self.profile_list.setStyleSheet(
            "QListWidget{background:#111827;border:1px solid #2d3748;border-radius:6px;}"
            "QListWidget::item{padding:10px 14px;border-bottom:1px solid #1a2035;color:#e2e8f0;}"
            "QListWidget::item:hover{background:#1e2433;}"
            "QListWidget::item:selected{background:#1a2a4a;}"
        )
        for p in SAMPLE_PROFILES:
            dot, _ = ("🟢", "#6ee7b7") if p.status == "running" else ("⚪", "#64748b")
            item = QListWidgetItem(
                f"  {dot}  {p.name}    [{p.group}]  •  {p.browser_type} / {p.os_type}"
            )
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

        # Filter
        def _filter(text):
            for i in range(self.profile_list.count()):
                it = self.profile_list.item(i)
                it.setHidden(text.lower() not in it.text().lower())
        search.textChanged.connect(_filter)
        return w

    def _build_schedule_tab(self):
        w = QWidget()
        w.setStyleSheet("background:#0f1117;")
        lay = QVBoxLayout(w)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(16)

        self.sched_cb = QCheckBox("  Enable Automatic Scheduling")
        self.sched_cb.setChecked(bool(self.task.schedule))
        self.sched_cb.setStyleSheet(
            "color:#e2e8f0;font-size:14px;font-weight:600;"
            "QCheckBox::indicator:checked{background:#ff8c00;border:2px solid #ff8c00;border-radius:3px;}"
        )
        lay.addWidget(self.sched_cb)
        lay.addWidget(_sep())

        freq_lbl = QLabel("Frequency")
        freq_lbl.setStyleSheet("color:#94a3b8;font-size:12px;font-weight:600;")
        lay.addWidget(freq_lbl)

        freq_row = QHBoxLayout()
        self.freq_btns = {}
        for label in ["Once", "Hourly", "Daily", "Weekly", "Monthly"]:
            b = QPushButton(label)
            b.setCheckable(True)
            b.setChecked(label == "Once")
            b.setFixedHeight(36)
            b.setStyleSheet(
                "QPushButton{background:#1e2433;color:#94a3b8;border:1px solid #2d3748;"
                "border-radius:6px;padding:4px 16px;}"
                "QPushButton:checked{background:#ff8c00;color:#fff;border:none;font-weight:700;}"
            )
            freq_row.addWidget(b)
            self.freq_btns[label] = b
        freq_row.addStretch()
        lay.addLayout(freq_row)

        dt_lbl = QLabel("Start at")
        dt_lbl.setStyleSheet("color:#94a3b8;font-size:12px;font-weight:600;")
        lay.addWidget(dt_lbl)
        dt_row = QHBoxLayout()
        self.dt_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.dt_edit.setCalendarPopup(True)
        self.dt_edit.setStyleSheet(
            "background:#111827;color:#e2e8f0;border:1px solid #2d3748;"
            "border-radius:6px;padding:6px 10px;font-size:13px;"
        )
        self.dt_edit.setFixedWidth(220)
        dt_row.addWidget(self.dt_edit)
        dt_row.addStretch()
        lay.addLayout(dt_row)

        conc_lbl = QLabel("Concurrent profiles  (run how many profiles at once)")
        conc_lbl.setStyleSheet("color:#94a3b8;font-size:12px;font-weight:600;")
        lay.addWidget(conc_lbl)
        conc_row = QHBoxLayout()
        self.conc_spin = QSpinBox()
        self.conc_spin.setRange(1, 50)
        self.conc_spin.setValue(1)
        self.conc_spin.setFixedWidth(100)
        self.conc_spin.setStyleSheet(
            "background:#111827;color:#e2e8f0;border:1px solid #2d3748;"
            "border-radius:6px;padding:6px;font-size:13px;"
        )
        conc_row.addWidget(self.conc_spin)
        conc_row.addStretch()
        lay.addLayout(conc_row)

        retry_lbl = QLabel("Retry on failure")
        retry_lbl.setStyleSheet("color:#94a3b8;font-size:12px;font-weight:600;")
        lay.addWidget(retry_lbl)
        retry_row = QHBoxLayout()
        self.retry_spin = QSpinBox()
        self.retry_spin.setRange(0, 10)
        self.retry_spin.setValue(2)
        self.retry_spin.setFixedWidth(100)
        self.retry_spin.setStyleSheet(self.conc_spin.styleSheet())
        retry_lbl2 = QLabel("times")
        retry_lbl2.setStyleSheet("color:#64748b;")
        retry_row.addWidget(self.retry_spin)
        retry_row.addWidget(retry_lbl2)
        retry_row.addStretch()
        lay.addLayout(retry_row)

        lay.addStretch()
        return w


# ─── Main RPA Dialog ──────────────────────────────────────────────────────────

class RPADialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tasks = list(SAMPLE_TASKS)
        self._current_row = -1
        self._running = False
        self._timer = None
        self._log_lines = []
        self.setWindowTitle("Automation  —  KH Browser")
        self.setMinimumSize(1100, 680)
        self.setStyleSheet("background:#0b0e14;color:#e2e8f0;")
        self._build()

    # ── Layout ────────────────────────────────────────────────────────

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_header())

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setStyleSheet("QSplitter::handle{background:#1e2433;width:1px;}")
        splitter.addWidget(self._build_left())
        splitter.addWidget(self._build_right())
        splitter.setSizes([320, 780])
        root.addWidget(splitter, 1)

        root.addWidget(self._build_status_bar())

    def _build_header(self):
        hdr = QWidget()
        hdr.setFixedHeight(60)
        hdr.setStyleSheet("background:#111827;border-bottom:2px solid #ff8c00;")
        hl = QHBoxLayout(hdr)
        hl.setContentsMargins(20, 0, 20, 0)

        title = QLabel("🤖  Automation Tasks")
        title.setStyleSheet("font-size:17px;font-weight:700;color:#ff8c00;")

        # Stats pills
        self.stat_total = self._stat_pill("Total", str(len(self.tasks)), "#64748b")
        self.stat_running = self._stat_pill("Running",
            str(sum(1 for t in self.tasks if t.status == "running")), "#6ee7b7")
        self.stat_scheduled = self._stat_pill("Scheduled",
            str(sum(1 for t in self.tasks if t.status == "scheduled")), "#fcd34d")

        new_btn = QPushButton("  ➕  New Task")
        new_btn.setFixedHeight(38)
        new_btn.setStyleSheet(
            "background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #ff8c00,stop:1 #ea580c);"
            "color:#fff;font-weight:700;border-radius:8px;border:none;font-size:13px;padding:0 18px;"
        )
        new_btn.clicked.connect(self._new_task)

        import_btn = QPushButton("  📥  Import")
        import_btn.setFixedHeight(38)
        import_btn.setStyleSheet(
            "background:#1e2433;color:#94a3b8;border:1px solid #2d3748;"
            "border-radius:8px;font-size:13px;padding:0 14px;"
        )

        hl.addWidget(title)
        hl.addSpacing(24)
        hl.addWidget(self.stat_total)
        hl.addWidget(self.stat_running)
        hl.addWidget(self.stat_scheduled)
        hl.addStretch()
        hl.addWidget(import_btn)
        hl.addSpacing(8)
        hl.addWidget(new_btn)
        return hdr

    def _stat_pill(self, label, val, color):
        w = QWidget()
        l = QHBoxLayout(w)
        l.setContentsMargins(10, 4, 10, 4)
        l.setSpacing(6)
        v = QLabel(val)
        v.setStyleSheet(f"color:{color};font-size:15px;font-weight:800;")
        lb = QLabel(label)
        lb.setStyleSheet("color:#475569;font-size:11px;")
        l.addWidget(v)
        l.addWidget(lb)
        w.setStyleSheet("background:#1a1f2e;border-radius:8px;")
        return w

    def _build_left(self):
        left = QWidget()
        left.setFixedWidth(310)
        left.setStyleSheet("background:#0b0e14;")
        ll = QVBoxLayout(left)
        ll.setContentsMargins(0, 0, 0, 0)
        ll.setSpacing(0)

        # Search + filter
        top = QWidget()
        top.setStyleSheet("background:#111827;border-bottom:1px solid #1e2433;")
        tl = QVBoxLayout(top)
        tl.setContentsMargins(10, 10, 10, 10)
        tl.setSpacing(8)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍  Search tasks…")
        self.search_box.setStyleSheet(
            "background:#1e2433;color:#e2e8f0;border:1px solid #2d3748;"
            "border-radius:6px;padding:7px 12px;font-size:12px;"
        )
        self.search_box.textChanged.connect(self._filter_tasks)
        tl.addWidget(self.search_box)

        filter_row = QHBoxLayout()
        filter_row.setSpacing(4)
        self.filter_btns = {}
        for status in ["All", "Running", "Scheduled", "Idle", "Completed"]:
            b = QPushButton(status)
            b.setCheckable(True)
            b.setChecked(status == "All")
            b.setFixedHeight(26)
            b.setStyleSheet(
                "QPushButton{background:transparent;color:#64748b;border:1px solid #2d3748;"
                "border-radius:5px;font-size:10px;padding:2px 8px;}"
                "QPushButton:checked{background:#ff8c00;color:#fff;border:none;font-weight:700;}"
            )
            b.clicked.connect(lambda _, s=status: self._set_filter(s))
            filter_row.addWidget(b)
            self.filter_btns[status] = b
        tl.addLayout(filter_row)
        ll.addWidget(top)

        self.task_list = QListWidget()
        self.task_list.setStyleSheet(
            "QListWidget{border:none;background:#0b0e14;outline:none;}"
            "QListWidget::item{padding:0px;border-bottom:1px solid #131720;}"
            "QListWidget::item:selected{background:transparent;}"
            "QListWidget::item:hover{background:transparent;}"
        )
        self.task_list.currentRowChanged.connect(self._show_task)
        ll.addWidget(self.task_list, 1)

        for t in self.tasks:
            self._add_task_item(t)

        return left

    def _build_right(self):
        right = QWidget()
        right.setStyleSheet("background:#0f1117;")
        rl = QVBoxLayout(right)
        rl.setContentsMargins(0, 0, 0, 0)
        rl.setSpacing(0)

        # Action toolbar
        toolbar = QWidget()
        toolbar.setFixedHeight(52)
        toolbar.setStyleSheet("background:#111827;border-bottom:1px solid #1e2433;")
        tl = QHBoxLayout(toolbar)
        tl.setContentsMargins(16, 0, 16, 0)
        tl.setSpacing(8)

        self.run_btn = QPushButton("  ▶  Run Task")
        self.run_btn.setFixedHeight(36)
        self.run_btn.setStyleSheet(
            "background:#16a34a;color:#fff;font-weight:700;border-radius:7px;"
            "border:none;font-size:13px;padding:0 18px;"
        )
        self.run_btn.clicked.connect(self._run_task)

        self.stop_btn = QPushButton("  ⏹  Stop")
        self.stop_btn.setFixedHeight(36)
        self.stop_btn.setVisible(False)
        self.stop_btn.setStyleSheet(
            "background:#dc2626;color:#fff;font-weight:700;border-radius:7px;"
            "border:none;font-size:13px;padding:0 18px;"
        )
        self.stop_btn.clicked.connect(self._stop_task)

        self.pause_btn = QPushButton("  ⏸  Pause")
        self.pause_btn.setFixedHeight(36)
        self.pause_btn.setVisible(False)
        self.pause_btn.setStyleSheet(
            "background:#d97706;color:#fff;font-weight:700;border-radius:7px;"
            "border:none;font-size:13px;padding:0 14px;"
        )

        self.edit_btn = QPushButton("  ✏  Edit")
        self.edit_btn.setFixedHeight(36)
        self.edit_btn.setStyleSheet(
            "background:#1e2433;color:#94a3b8;border:1px solid #2d3748;"
            "border-radius:7px;font-size:13px;padding:0 14px;"
        )
        self.edit_btn.clicked.connect(self._edit_task)

        self.clone_btn = QPushButton("  📋  Clone")
        self.clone_btn.setFixedHeight(36)
        self.clone_btn.setStyleSheet(self.edit_btn.styleSheet())
        self.clone_btn.clicked.connect(self._clone_task)

        self.delete_btn = QPushButton("  🗑  Delete")
        self.delete_btn.setFixedHeight(36)
        self.delete_btn.setStyleSheet(
            "background:transparent;color:#ef4444;border:1px solid #7f1d1d;"
            "border-radius:7px;font-size:13px;padding:0 14px;"
        )
        self.delete_btn.clicked.connect(self._delete_task)

        tl.addWidget(self.run_btn)
        tl.addWidget(self.stop_btn)
        tl.addWidget(self.pause_btn)
        tl.addWidget(_sep() if False else QFrame())  # spacer trick
        tl.addSpacing(8)
        tl.addWidget(self.edit_btn)
        tl.addWidget(self.clone_btn)
        tl.addWidget(self.delete_btn)
        tl.addStretch()

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setFixedHeight(3)
        self.progress.setTextVisible(False)
        self.progress.setVisible(False)
        self.progress.setStyleSheet(
            "QProgressBar{background:#1e2433;border:none;}"
            "QProgressBar::chunk{background:qlineargradient(x1:0,y1:0,x2:1,y2:0,"
            "stop:0 #ff8c00,stop:1 #ea580c);}"
        )

        rl.addWidget(toolbar)
        rl.addWidget(self.progress)

        # Tabs: Details / Script / Log
        self.detail_tabs = QTabWidget()
        self.detail_tabs.setDocumentMode(True)
        self.detail_tabs.setStyleSheet(
            "QTabWidget::pane{border:none;background:#0f1117;}"
            "QTabBar::tab{background:#111827;color:#64748b;padding:10px 22px;border:none;}"
            "QTabBar::tab:selected{background:#0f1117;color:#ff8c00;border-bottom:2px solid #ff8c00;}"
        )
        self.detail_tabs.addTab(self._build_overview_tab(), "  📊 Overview  ")
        self.detail_tabs.addTab(self._build_script_tab_r(), "  📝 Script  ")
        self.detail_tabs.addTab(self._build_log_tab(), "  📋 Execution Log  ")

        rl.addWidget(self.detail_tabs, 1)
        return right

    def _build_overview_tab(self):
        w = QWidget()
        w.setStyleSheet("background:#0f1117;")
        lay = QVBoxLayout(w)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(16)

        # Task title row
        title_row = QHBoxLayout()
        self.ov_title = QLabel("Select a task")
        self.ov_title.setStyleSheet("font-size:20px;font-weight:700;color:#e2e8f0;")
        self.ov_badge = QLabel()
        title_row.addWidget(self.ov_title, 1)
        title_row.addWidget(self.ov_badge)
        lay.addLayout(title_row)

        self.ov_desc = QLabel()
        self.ov_desc.setStyleSheet("color:#64748b;font-size:13px;")
        self.ov_desc.setWordWrap(True)
        lay.addWidget(self.ov_desc)
        lay.addWidget(_sep())

        # Stats row
        stats_row = QHBoxLayout()
        stats_row.setSpacing(12)
        self.stat_widgets = {}
        for key, label, color in [
            ("run_count", "Total Runs", "#93c5fd"),
            ("last_run",  "Last Run",   "#6ee7b7"),
            ("created",   "Created",    "#fcd34d"),
            ("profiles",  "Profiles",   "#fb923c"),
        ]:
            card = QWidget()
            card.setStyleSheet(
                "background:#111827;border-radius:10px;border:1px solid #1e2433;"
            )
            cl = QVBoxLayout(card)
            cl.setContentsMargins(16, 12, 16, 12)
            cl.setSpacing(4)
            val = QLabel("—")
            val.setStyleSheet(f"color:{color};font-size:22px;font-weight:800;")
            lbl = QLabel(label)
            lbl.setStyleSheet("color:#475569;font-size:11px;")
            cl.addWidget(val)
            cl.addWidget(lbl)
            stats_row.addWidget(card, 1)
            self.stat_widgets[key] = val
        lay.addLayout(stats_row)

        # Profile tags
        prof_lbl = QLabel("Assigned Profiles")
        prof_lbl.setStyleSheet("color:#94a3b8;font-size:12px;font-weight:600;")
        lay.addWidget(prof_lbl)
        self.profile_tags_w = QWidget()
        self.profile_tags_l = QHBoxLayout(self.profile_tags_w)
        self.profile_tags_l.setContentsMargins(0, 0, 0, 0)
        self.profile_tags_l.setSpacing(6)
        lay.addWidget(self.profile_tags_w)
        lay.addStretch()
        return w

    def _build_script_tab_r(self):
        w = QWidget()
        w.setStyleSheet("background:#0f1117;")
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)

        self.script_view = QPlainTextEdit()
        self.script_view.setReadOnly(True)
        self.script_view.setStyleSheet(
            "background:#0a0d13;color:#a3e635;font-family:monospace;font-size:13px;"
            "border:none;padding:20px;"
        )
        lay.addWidget(self.script_view)
        return w

    def _build_log_tab(self):
        w = QWidget()
        w.setStyleSheet("background:#0a0d13;")
        lay = QVBoxLayout(w)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        # Log toolbar
        log_toolbar = QWidget()
        log_toolbar.setStyleSheet("background:#111827;border-bottom:1px solid #1e2433;")
        ltl = QHBoxLayout(log_toolbar)
        ltl.setContentsMargins(12, 8, 12, 8)
        log_lbl = QLabel("Execution Log")
        log_lbl.setStyleSheet("color:#94a3b8;font-size:12px;font-weight:600;")
        clear_log_btn = QPushButton("Clear")
        clear_log_btn.setFixedHeight(26)
        clear_log_btn.setStyleSheet(
            "background:#1e2433;color:#64748b;border:1px solid #2d3748;"
            "border-radius:4px;font-size:11px;padding:2px 10px;"
        )
        clear_log_btn.clicked.connect(lambda: self.log_view.setPlainText(""))
        copy_btn = QPushButton("Copy")
        copy_btn.setFixedHeight(26)
        copy_btn.setStyleSheet(clear_log_btn.styleSheet())
        copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(self.log_view.toPlainText()))
        ltl.addWidget(log_lbl, 1)
        ltl.addWidget(clear_log_btn)
        ltl.addWidget(copy_btn)
        lay.addWidget(log_toolbar)

        self.log_view = QPlainTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setStyleSheet(
            "background:#0a0d13;color:#a3e635;font-family:monospace;font-size:12px;"
            "border:none;padding:12px;"
        )
        self.log_view.setPlaceholderText("  Run a task to see execution log here…")
        lay.addWidget(self.log_view, 1)
        return w

    def _build_status_bar(self):
        bar = QWidget()
        bar.setFixedHeight(28)
        bar.setStyleSheet("background:#0b0e14;border-top:1px solid #1e2433;")
        bl = QHBoxLayout(bar)
        bl.setContentsMargins(16, 0, 16, 0)
        self.status_lbl = QLabel("  Ready")
        self.status_lbl.setStyleSheet("color:#475569;font-size:11px;")
        self.time_lbl = QLabel()
        self.time_lbl.setStyleSheet("color:#2d3748;font-size:11px;")
        bl.addWidget(self.status_lbl, 1)
        bl.addWidget(self.time_lbl)
        # Update clock
        def _tick():
            self.time_lbl.setText(datetime.datetime.now().strftime("  %Y-%m-%d  %H:%M:%S  "))
        t = QTimer(self)
        t.timeout.connect(_tick)
        t.start(1000)
        _tick()
        return bar

    # ── Task list helpers ─────────────────────────────────────────────

    def _add_task_item(self, task: RPATask):
        item = QListWidgetItem()
        item.setData(Qt.ItemDataRole.UserRole, task)
        item.setSizeHint(QSize(300, 80))
        self.task_list.addItem(item)

        dot, dot_color, bg = STATUS_STYLE.get(task.status, ("●", "#64748b", "#1e2433"))
        w = QWidget()
        w.setObjectName("taskCard")
        w.setStyleSheet(
            "#taskCard{background:#111827;border-radius:0;}"
            "#taskCard:hover{background:#141b2b;}"
        )
        wl = QVBoxLayout(w)
        wl.setContentsMargins(14, 12, 14, 12)
        wl.setSpacing(6)

        top_row = QHBoxLayout()
        name = QLabel(f"🤖  {task.name}")
        name.setStyleSheet("font-weight:700;color:#e2e8f0;font-size:13px;")
        badge = QLabel(f"  {dot} {task.status.upper()}  ")
        badge.setStyleSheet(
            f"background:{bg};color:{dot_color};border-radius:8px;"
            "padding:1px 8px;font-size:10px;font-weight:700;"
        )
        top_row.addWidget(name, 1)
        top_row.addWidget(badge)

        bot_row = QHBoxLayout()
        desc = QLabel(task.description[:46] + "…" if len(task.description) > 46 else task.description)
        desc.setStyleSheet("color:#475569;font-size:11px;")
        runs = QLabel(f"🔄 {task.run_count} runs")
        runs.setStyleSheet("color:#374151;font-size:10px;")
        bot_row.addWidget(desc, 1)
        bot_row.addWidget(runs)

        wl.addLayout(top_row)
        wl.addLayout(bot_row)
        self.task_list.setItemWidget(item, w)

    def _filter_tasks(self, text=""):
        for i in range(self.task_list.count()):
            item = self.task_list.item(i)
            task = item.data(Qt.ItemDataRole.UserRole)
            if task:
                match = text.lower() in task.name.lower() or text.lower() in task.description.lower()
                item.setHidden(not match)

    def _set_filter(self, status):
        for k, b in self.filter_btns.items():
            b.setChecked(k == status)
        for i in range(self.task_list.count()):
            item = self.task_list.item(i)
            task = item.data(Qt.ItemDataRole.UserRole)
            if task:
                if status == "All":
                    item.setHidden(False)
                else:
                    item.setHidden(task.status.lower() != status.lower())

    # ── Task detail ───────────────────────────────────────────────────

    def _show_task(self, row):
        if row < 0 or row >= len(self.tasks):
            return
        self._current_row = row
        task = self.tasks[row]

        # Overview
        self.ov_title.setText(task.name)
        dot, dot_color, bg = STATUS_STYLE.get(task.status, ("●", "#64748b", "#1e2433"))
        self.ov_badge.setText(f"  {dot} {task.status.upper()}  ")
        self.ov_badge.setStyleSheet(
            f"background:{bg};color:{dot_color};border-radius:10px;"
            "padding:3px 12px;font-size:11px;font-weight:700;"
        )
        self.ov_desc.setText(task.description)
        self.stat_widgets["run_count"].setText(str(task.run_count))
        self.stat_widgets["last_run"].setText(task.last_run or "Never")
        self.stat_widgets["created"].setText(task.created_at[:10] if task.created_at else "—")
        self.stat_widgets["profiles"].setText(str(len(task.profile_ids)))

        # Profile tags
        for i in reversed(range(self.profile_tags_l.count())):
            self.profile_tags_l.itemAt(i).widget().deleteLater()
        for pid in task.profile_ids[:6]:
            tag = QLabel(f"  {pid}  ")
            tag.setStyleSheet(
                "background:#1e3a5f;color:#93c5fd;border-radius:5px;"
                "padding:2px 8px;font-size:11px;"
            )
            self.profile_tags_l.addWidget(tag)
        if not task.profile_ids:
            none_tag = QLabel("  No profiles assigned  ")
            none_tag.setStyleSheet("color:#374151;font-size:11px;")
            self.profile_tags_l.addWidget(none_tag)
        self.profile_tags_l.addStretch()

        # Script
        self.script_view.setPlainText(task.script)
        self.status_lbl.setText(f"  Task: {task.name}  •  Status: {task.status}")

    # ── Task actions ──────────────────────────────────────────────────

    def _run_task(self):
        row = self._current_row
        if row < 0:
            return
        task = self.tasks[row]
        self._running = True

        self.run_btn.setVisible(False)
        self.stop_btn.setVisible(True)
        self.pause_btn.setVisible(True)
        self.progress.setVisible(True)
        self.progress.setValue(0)
        self.detail_tabs.setCurrentIndex(2)  # Switch to Log tab

        self.log_view.setPlainText("")
        task.status = "running"
        self._refresh_item(row)

        log_steps = [
            f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 🚀 Starting task: {task.name}",
            f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 🔧 Initializing browser context...",
            f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 🌐 Launching profile: FB Account 1",
            f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ✅ Browser started  PID: {random.randint(10000,99999)}",
            f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 📜 Executing script line 1...",
            f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 🌐 Navigating to target URL...",
            f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ⏳ Waiting for page load...",
            f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ✅ Page loaded  (1240ms)",
            f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 🖱 Clicking selector #submit",
            f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ✅ Click successful",
            f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 📷 Screenshot saved: snap.png",
            f"[{datetime.datetime.now().strftime('%H:%M:%S')}] ✅ Task completed successfully!",
            f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 📊 Run #{task.run_count + 1}  Duration: {random.randint(3,15)}s",
        ]

        v = [0]
        def tick():
            if not self._running:
                return
            step = v[0]
            if step < len(log_steps):
                self.log_view.appendPlainText(log_steps[step])
                self.log_view.moveCursor(QTextCursor.MoveOperation.End)
            pct = int((step + 1) / len(log_steps) * 100)
            self.progress.setValue(pct)
            v[0] += 1
            if step >= len(log_steps) - 1:
                self._timer.stop()
                self._on_task_done(row)

        self._timer = QTimer(self)
        self._timer.timeout.connect(tick)
        self._timer.start(280)

    def _on_task_done(self, row):
        self._running = False
        task = self.tasks[row]
        task.status = "completed"
        task.run_count += 1
        task.last_run = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        self.run_btn.setVisible(True)
        self.stop_btn.setVisible(False)
        self.pause_btn.setVisible(False)
        self.progress.setVisible(False)
        self._refresh_item(row)
        self._show_task(row)
        self.status_lbl.setText(f"  ✅ Task completed: {task.name}")

        QMessageBox.information(
            self, "Task Complete",
            f"<b style='color:#6ee7b7'>✅ Task completed successfully!</b>"
            f"<br><br>Task: <b>{task.name}</b>"
            f"<br>Run #{task.run_count}  •  {task.last_run}"
        )

    def _stop_task(self):
        if self._timer:
            self._timer.stop()
        self._running = False
        row = self._current_row
        if 0 <= row < len(self.tasks):
            self.tasks[row].status = "idle"
            self._refresh_item(row)
        self.run_btn.setVisible(True)
        self.stop_btn.setVisible(False)
        self.pause_btn.setVisible(False)
        self.progress.setVisible(False)
        self.log_view.appendPlainText(
            f"\n[{datetime.datetime.now().strftime('%H:%M:%S')}] ⏹ Task stopped by user."
        )
        self.status_lbl.setText("  Task stopped")

    def _new_task(self):
        dlg = TaskEditorDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            task = RPATask(
                name=dlg.name_edit.text() or "New Task",
                description=dlg.desc_edit.text(),
                script=dlg.script_edit.toPlainText(),
            )
            self.tasks.append(task)
            self._add_task_item(task)
            self._update_stats()
            self.task_list.setCurrentRow(len(self.tasks) - 1)

    def _edit_task(self):
        row = self._current_row
        if 0 <= row < len(self.tasks):
            dlg = TaskEditorDialog(self, self.tasks[row])
            if dlg.exec() == QDialog.DialogCode.Accepted:
                t = self.tasks[row]
                t.name = dlg.name_edit.text() or t.name
                t.description = dlg.desc_edit.text()
                t.script = dlg.script_edit.toPlainText()
                self._refresh_item(row)
                self._show_task(row)

    def _clone_task(self):
        row = self._current_row
        if 0 <= row < len(self.tasks):
            import copy
            t = copy.deepcopy(self.tasks[row])
            t.name = f"{t.name} (Copy)"
            t.status = "idle"
            t.run_count = 0
            self.tasks.append(t)
            self._add_task_item(t)
            self.task_list.setCurrentRow(len(self.tasks) - 1)

    def _delete_task(self):
        row = self._current_row
        if 0 <= row < len(self.tasks):
            task = self.tasks[row]
            reply = QMessageBox.question(
                self, "Delete Task",
                f"Delete task <b>{task.name}</b>?<br>This cannot be undone.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.tasks.pop(row)
                self.task_list.takeItem(row)
                self._current_row = -1
                self._update_stats()
                if self.tasks:
                    self.task_list.setCurrentRow(0)

    def _refresh_item(self, row):
        if 0 <= row < len(self.tasks):
            item = self.task_list.item(row)
            task = self.tasks[row]
            if not item:
                return
            w = self.task_list.itemWidget(item)
            if w:
                w.deleteLater()
            # Rebuild the widget inline
            dot, dot_color, bg = STATUS_STYLE.get(task.status, ("●", "#64748b", "#1e2433"))
            new_w = QWidget()
            new_w.setObjectName("taskCard")
            new_w.setStyleSheet("#taskCard{background:#111827;} #taskCard:hover{background:#141b2b;}")
            wl = QVBoxLayout(new_w)
            wl.setContentsMargins(14, 12, 14, 12)
            wl.setSpacing(6)
            top = QHBoxLayout()
            name = QLabel(f"🤖  {task.name}")
            name.setStyleSheet("font-weight:700;color:#e2e8f0;font-size:13px;")
            badge = QLabel(f"  {dot} {task.status.upper()}  ")
            badge.setStyleSheet(
                f"background:{bg};color:{dot_color};border-radius:8px;"
                "padding:1px 8px;font-size:10px;font-weight:700;"
            )
            top.addWidget(name, 1)
            top.addWidget(badge)
            bot = QHBoxLayout()
            desc = QLabel(task.description[:46] + "…" if len(task.description) > 46 else task.description)
            desc.setStyleSheet("color:#475569;font-size:11px;")
            runs = QLabel(f"🔄 {task.run_count} runs")
            runs.setStyleSheet("color:#374151;font-size:10px;")
            bot.addWidget(desc, 1)
            bot.addWidget(runs)
            wl.addLayout(top)
            wl.addLayout(bot)
            self.task_list.setItemWidget(item, new_w)

    def _update_stats(self):
        pass  # Could update header stat pills here
