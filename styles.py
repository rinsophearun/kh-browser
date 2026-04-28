# ── AntiDetect Premium Design System ─────────────────────────────────────────
DARK_THEME = """
/* ── Reset & Base ────────────────────────────────────────────────────────── */
* {
    font-family: ".AppleSystemUIFont", "Helvetica Neue", Arial;
    font-size: 13px;
    color: #e2e8f0;
    outline: none;
}
QMainWindow, QDialog {
    background: #07090f;
}
QWidget {
    background: transparent;
}
QWidget#centralWidget, QWidget#mainContent {
    background: #07090f;
}
QStackedWidget {
    background: #07090f;
}

/* ── Sidebar ─────────────────────────────────────────────────────────────── */
QWidget#sidebar {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #080b12, stop:1 #0a0d16);
    border-right: 1px solid #141a28;
}

/* ── Scrollbars ──────────────────────────────────────────────────────────── */
QScrollBar:vertical {
    background: #0a0d16; width: 5px; border-radius: 3px; margin: 0;
}
QScrollBar::handle:vertical {
    background: #f97316; border-radius: 3px; min-height: 24px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal {
    background: #0a0d16; height: 5px; border-radius: 3px; margin: 0;
}
QScrollBar::handle:horizontal {
    background: #f97316; border-radius: 3px;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }

/* ── Tooltip ─────────────────────────────────────────────────────────────── */
QToolTip {
    background: #1a2236;
    color: #f1f5f9;
    border: 1px solid #f9731640;
    border-radius: 6px;
    padding: 5px 10px;
    font-size: 12px;
}

/* ── Menu ────────────────────────────────────────────────────────────────── */
QMenu {
    background: #0e1420;
    border: 1px solid #1e2d45;
    border-radius: 12px;
    padding: 6px;
}
QMenu::item {
    padding: 8px 20px 8px 12px;
    border-radius: 8px;
    color: #94a3b8;
    font-size: 13px;
}
QMenu::item:selected {
    background: #1e2d45;
    color: #f1f5f9;
}
QMenu::separator {
    height: 1px;
    background: #1e2d45;
    margin: 4px 0;
}

/* ── Dialog ──────────────────────────────────────────────────────────────── */
QDialog {
    background: #0a0d16;
    border: 1px solid #1e2d45;
    border-radius: 16px;
}

/* ── Message Box ─────────────────────────────────────────────────────────── */
QMessageBox {
    background: #0a0d16;
}
QMessageBox QLabel {
    color: #e2e8f0;
}
QMessageBox QPushButton {
    background: #1e2d45;
    color: #e2e8f0;
    border: 1px solid #253555;
    border-radius: 8px;
    padding: 6px 20px;
    min-width: 80px;
}
QMessageBox QPushButton:hover {
    background: #f97316;
    color: white;
    border-color: #f97316;
}

/* ── Tab Widget ──────────────────────────────────────────────────────────── */
QTabWidget::pane {
    background: #0a0d16;
    border: 1px solid #1e2d45;
    border-radius: 0 12px 12px 12px;
}
QTabBar::tab {
    background: #07090f;
    color: #475569;
    padding: 10px 20px;
    border: 1px solid transparent;
    border-bottom: none;
    border-radius: 10px 10px 0 0;
    font-size: 12px;
    font-weight: 500;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background: #0a0d16;
    color: #f97316;
    border-color: #1e2d45;
    font-weight: 700;
}
QTabBar::tab:hover:!selected {
    background: #0e1420;
    color: #94a3b8;
}

/* ── Form fields ─────────────────────────────────────────────────────────── */
QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox {
    background: #0e1420;
    color: #e2e8f0;
    border: 1px solid #1e2d45;
    border-radius: 10px;
    padding: 8px 12px;
    selection-background-color: #f9731640;
    selection-color: #f1f5f9;
}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus,
QSpinBox:focus, QDoubleSpinBox:focus {
    border-color: #f97316;
    background: #0f1520;
}
QLineEdit:hover, QTextEdit:hover {
    border-color: #f9731660;
}
QLineEdit::placeholder { color: #334155; }

QSpinBox::up-button, QSpinBox::down-button,
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
    background: #1e2d45;
    border: none;
    border-radius: 4px;
    width: 16px;
}
QSpinBox::up-button:hover, QSpinBox::down-button:hover,
QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {
    background: #f97316;
}

/* ── ComboBox ────────────────────────────────────────────────────────────── */
QComboBox {
    background: #0e1420;
    color: #94a3b8;
    border: 1px solid #1e2d45;
    border-radius: 10px;
    padding: 6px 12px;
    min-height: 36px;
}
QComboBox:hover { border-color: #f9731660; }
QComboBox:focus { border-color: #f97316; }
QComboBox::drop-down {
    border: none;
    width: 28px;
    subcontrol-position: right center;
}
QComboBox::down-arrow {
    width: 10px;
    height: 10px;
}
QComboBox QAbstractItemView {
    background: #0e1420;
    color: #e2e8f0;
    border: 1px solid #1e2d45;
    border-radius: 10px;
    selection-background-color: #1e2d45;
    padding: 4px;
    outline: none;
}
QComboBox QAbstractItemView::item {
    padding: 8px 12px;
    border-radius: 6px;
}
QComboBox QAbstractItemView::item:hover {
    background: #1e2d45;
}

/* ── Checkbox ────────────────────────────────────────────────────────────── */
QCheckBox {
    spacing: 8px;
    color: #94a3b8;
}
QCheckBox::indicator {
    width: 16px; height: 16px;
    border-radius: 5px;
    border: 2px solid #1e2d45;
    background: #0e1420;
}
QCheckBox::indicator:checked {
    background: #f97316;
    border-color: #f97316;
}
QCheckBox::indicator:hover {
    border-color: #f97316;
}

/* ── Radio ───────────────────────────────────────────────────────────────── */
QRadioButton {
    color: #94a3b8;
    spacing: 8px;
}
QRadioButton::indicator {
    width: 16px; height: 16px;
    border-radius: 8px;
    border: 2px solid #1e2d45;
    background: #0e1420;
}
QRadioButton::indicator:checked {
    background: #f97316;
    border-color: #f97316;
}

/* ── GroupBox ────────────────────────────────────────────────────────────── */
QGroupBox {
    background: #0e1420;
    border: 1px solid #1e2d45;
    border-radius: 12px;
    margin-top: 18px;
    padding: 14px 12px 10px 12px;
    font-weight: 600;
    color: #64748b;
    font-size: 11px;
    letter-spacing: 1px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 14px;
    top: -1px;
    padding: 2px 8px;
    background: #0a0d16;
    color: #f97316;
    border-radius: 4px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* ── Progress Bar ────────────────────────────────────────────────────────── */
QProgressBar {
    background: #1e2d45;
    border: none;
    border-radius: 4px;
    height: 8px;
    text-align: center;
    color: transparent;
}
QProgressBar::chunk {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #f97316, stop:1 #fb923c);
    border-radius: 4px;
}

/* ── Status Bar ──────────────────────────────────────────────────────────── */
QStatusBar {
    background: #040608;
    color: #334155;
    border-top: 1px solid #141a28;
    font-size: 11px;
    padding: 0 12px;
}

/* ── Splitter ────────────────────────────────────────────────────────────── */
QSplitter::handle {
    background: #1e2d45;
    width: 1px;
    height: 1px;
}

/* ── List Widget ─────────────────────────────────────────────────────────── */
QListWidget {
    background: transparent;
    border: none;
    outline: none;
}
QListWidget::item {
    padding: 8px 12px;
    border-radius: 8px;
    color: #94a3b8;
}
QListWidget::item:selected {
    background: #1e2d45;
    color: #f1f5f9;
}
QListWidget::item:hover {
    background: #131d30;
}

/* ── Table Widget ────────────────────────────────────────────────────────── */
QTableWidget {
    background: #07090f;
    alternate-background-color: #09111c;
    border: none;
    gridline-color: transparent;
    outline: none;
    selection-background-color: #1e2d45;
}
QTableWidget::item { padding: 0; border: none; }
QTableWidget::item:selected {
    background: #1a2840;
    color: #f1f5f9;
}
QHeaderView { background: transparent; border: none; }
QHeaderView::section {
    background: #0a0d16;
    color: #475569;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    padding: 10px 10px;
    border: none;
    border-bottom: 1px solid #141a28;
    border-right: 1px solid #141a28;
}
QHeaderView::section:hover { color: #f97316; }
QHeaderView::section:last { border-right: none; }
"""
