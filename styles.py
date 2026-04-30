# ── Modern Blue Design System ──────────────────────────────────────────────────
"""
Modern Dark Theme with Bright Blue Accent
Primary: Dark Slate (#1E293B) | Accent: Bright Blue (#2563EB)
Background: Very Dark (#0F172A) | Card: Dark Blue (#192134)
"""

DARK_THEME = """
/* ── CSS Variables (Design System) ──────────────────────────────────────── */
:root {
    --primary: #1E293B;
    --primary-foreground: #FFFFFF;
    --secondary: #334155;
    --secondary-foreground: #FFFFFF;
    --accent: #2563EB;
    --accent-foreground: #FFFFFF;
    --background: #0F172A;
    --foreground: #FFFFFF;
    --card: #192134;
    --card-foreground: #FFFFFF;
    --muted: #10182B;
    --muted-foreground: #94A3B8;
    --border: rgba(255,255,255,0.08);
    --destructive: #DC2626;
    --destructive-foreground: #FFFFFF;
    --ring: #1E293B;
}

/* ── Reset & Base ──────────────────────────────────────────────────────────── */
* {
    font-family: ".AppleSystemUIFont", "Helvetica Neue", Arial;
    font-size: 13px;
    color: #FFFFFF;
    outline: none;
}
QMainWindow, QDialog {
    background: #0F172A;
}
QWidget {
    background: transparent;
}
QWidget#centralWidget, QWidget#mainContent {
    background: #0F172A;
}
QStackedWidget {
    background: #0F172A;
}

/* ── Sidebar ────────────────────────────────────────────────────────────────── */
QWidget#sidebar {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #192134, stop:1 #1E293B);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* ── Scrollbars ──────────────────────────────────────────────────────────── */
QScrollBar:vertical {
    background: #10182B; width: 5px; border-radius: 3px; margin: 0;
}
QScrollBar::handle:vertical {
    background: #2563EB; border-radius: 3px; min-height: 24px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal {
    background: #10182B; height: 5px; border-radius: 3px; margin: 0;
}
QScrollBar::handle:horizontal {
    background: #2563EB; border-radius: 3px;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }

/* ── Tooltip ─────────────────────────────────────────────────────────────── */
QToolTip {
    background: #1E293B;
    color: #FFFFFF;
    border: 1px solid rgba(37,99,235,0.3);
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 12px;
}

/* ── Menu ────────────────────────────────────────────────────────────────── */
QMenu {
    background: #192134;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 4px;
}
QMenu::item {
    padding: 8px 16px;
    border-radius: 6px;
    color: #CBD5E1;
    font-size: 13px;
}
QMenu::item:selected {
    background: #2563EB;
    color: #FFFFFF;
}
QMenu::separator {
    height: 1px;
    background: rgba(255,255,255,0.08);
    margin: 4px 0;
}

/* ── Dialog ────────────────────────────────────────────────────────────────── */
QDialog {
    background: #192134;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
}

/* ── Message Box ─────────────────────────────────────────────────────────── */
QMessageBox {
    background: #192134;
}
QMessageBox QLabel {
    color: #FFFFFF;
}
QMessageBox QPushButton {
    background: #1E293B;
    color: #FFFFFF;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 6px;
    padding: 6px 20px;
    min-width: 80px;
}
QMessageBox QPushButton:hover {
    background: #2563EB;
    color: white;
    border-color: #2563EB;
}

/* ── Tab Widget ────────────────────────────────────────────────────────────── */
QTabWidget::pane {
    background: #192134;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
}
QTabBar::tab {
    background: #1E293B;
    color: #94A3B8;
    padding: 8px 16px;
    border: none;
    border-bottom: 2px solid transparent;
    border-radius: 6px 6px 0 0;
    font-size: 12px;
    font-weight: 500;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background: #2563EB;
    color: #FFFFFF;
    border-bottom: 2px solid #2563EB;
    font-weight: 600;
}
QTabBar::tab:hover:!selected {
    background: #334155;
    color: #E2E8F0;
}

/* ── Form fields ───────────────────────────────────────────────────────────── */
QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox {
    background: #1E293B;
    color: #FFFFFF;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 6px;
    padding: 8px 12px;
    selection-background-color: #2563EB;
    selection-color: #FFFFFF;
}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus,
QSpinBox:focus, QDoubleSpinBox:focus {
    border: 2px solid #2563EB;
    background: #192134;
}
QLineEdit:hover, QTextEdit:hover {
    border: 1px solid rgba(37,99,235,0.3);
}
QLineEdit::placeholder { color: #64748B; }

QSpinBox::up-button, QSpinBox::down-button,
QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
    background: #334155;
    border: none;
    border-radius: 3px;
    width: 16px;
}
QSpinBox::up-button:hover, QSpinBox::down-button:hover,
QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {
    background: #2563EB;
}

/* ── ComboBox ──────────────────────────────────────────────────────────────── */
QComboBox {
    background: #1E293B;
    color: #CBD5E1;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 6px;
    padding: 6px 12px;
    min-height: 36px;
}
QComboBox:hover { 
    border: 1px solid rgba(37,99,235,0.3);
}
QComboBox:focus { 
    border: 2px solid #2563EB;
}
QComboBox::drop-down {
    border: none;
    width: 24px;
    subcontrol-position: right center;
}
QComboBox::down-arrow {
    width: 10px;
    height: 10px;
}
QComboBox QAbstractItemView {
    background: #1E293B;
    color: #FFFFFF;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 6px;
    selection-background-color: #2563EB;
    padding: 2px;
    outline: none;
}
QComboBox QAbstractItemView::item {
    padding: 8px 12px;
    border-radius: 4px;
}
QComboBox QAbstractItemView::item:hover {
    background: #2563EB;
}

/* ── Checkbox ──────────────────────────────────────────────────────────────── */
QCheckBox {
    spacing: 8px;
    color: #CBD5E1;
}
QCheckBox::indicator {
    width: 16px; height: 16px;
    border-radius: 4px;
    border: 1px solid rgba(255,255,255,0.08);
    background: #1E293B;
}
QCheckBox::indicator:checked {
    background: #2563EB;
    border-color: #2563EB;
}
QCheckBox::indicator:hover {
    border-color: #2563EB;
}

/* ── Radio ─────────────────────────────────────────────────────────────────── */
QRadioButton {
    color: #CBD5E1;
    spacing: 8px;
}
QRadioButton::indicator {
    width: 16px; height: 16px;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.08);
    background: #1E293B;
}
QRadioButton::indicator:checked {
    background: #2563EB;
    border-color: #2563EB;
}

/* ── GroupBox ──────────────────────────────────────────────────────────────── */
QGroupBox {
    background: #1E293B;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    margin-top: 16px;
    padding: 12px 12px 8px 12px;
    font-weight: 600;
    color: #94A3B8;
    font-size: 11px;
    letter-spacing: 0.5px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    top: -10px;
    padding: 0px 4px;
    background: #192134;
    color: #2563EB;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* ── Progress Bar ──────────────────────────────────────────────────────────── */
QProgressBar {
    background: #1E293B;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 4px;
    height: 8px;
    text-align: center;
    color: transparent;
}
QProgressBar::chunk {
    background: #2563EB;
    border-radius: 3px;
}

/* ── Status Bar ────────────────────────────────────────────────────────────── */
QStatusBar {
    background: #0F172A;
    color: #94A3B8;
    border-top: 1px solid rgba(255,255,255,0.08);
    font-size: 11px;
    padding: 0 12px;
}

/* ── Splitter ──────────────────────────────────────────────────────────────── */
QSplitter::handle {
    background: rgba(255,255,255,0.08);
    width: 1px;
    height: 1px;
}

/* ── List Widget ───────────────────────────────────────────────────────────── */
QListWidget {
    background: transparent;
    border: none;
    outline: none;
}
QListWidget::item {
    padding: 6px 10px;
    border-radius: 6px;
    color: #CBD5E1;
}
QListWidget::item:selected {
    background: #2563EB;
    color: #FFFFFF;
}
QListWidget::item:hover {
    background: #1E293B;
}

/* ── Table Widget ──────────────────────────────────────────────────────────── */
QTableWidget {
    background: #0F172A;
    alternate-background-color: #192134;
    border: none;
    gridline-color: transparent;
    outline: none;
    selection-background-color: #2563EB;
}
QTableWidget::item { padding: 0; border: none; }
QTableWidget::item:selected {
    background: #2563EB;
    color: #FFFFFF;
}
QHeaderView { background: transparent; border: none; }
QHeaderView::section {
    background: #1E293B;
    color: #94A3B8;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    padding: 8px 10px;
    border: none;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    border-right: 1px solid rgba(255,255,255,0.08);
}
QHeaderView::section:hover { color: #2563EB; }
QHeaderView::section:last { border-right: none; }
"""
