#Vorraluck Taladon
#683040740-0

import sys
import json
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QScrollArea, QLabel, QDialog,
    QLineEdit, QComboBox, QDateEdit, QFormLayout,
    QMessageBox, QFileDialog, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, QDate, Signal
from PySide6.QtGui import QFont


# ─────────────────────────────────────────────
#  Priority config
# ─────────────────────────────────────────────
PRIORITY_LEVELS = ["Low", "Medium", "High", "Critical"]

PRIORITY_COLORS = {
    "Low":      "#d4edda",   # soft green
    "Medium":   "#cce5ff",   # soft blue
    "High":     "#fff3cd",   # soft yellow
    "Critical": "#f8d7da",   # soft red
}

PRIORITY_BORDER = {
    "Low":      "#28a745",
    "Medium":   "#4a90d9",
    "High":     "#ffc107",
    "Critical": "#dc3545",
}

PRIORITY_BADGE = {
    "Low":      ("#28a745", "#ffffff"),
    "Medium":   ("#4a90d9", "#ffffff"),
    "High":     ("#ffc107", "#000000"),
    "Critical": ("#dc3545", "#ffffff"),
}


# ─────────────────────────────────────────────
#  TaskCard – individual card widget
# ─────────────────────────────────────────────
class TaskCard(QFrame):
    """A card that represents a single to-do item."""

    delete_requested = Signal(object)   # emits itself

    def __init__(self, task: dict, parent=None):
        super().__init__(parent)
        self.task = task
        self._build_ui()
        self._apply_style()

    def _build_ui(self):
        self.setFixedHeight(100)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        priority = self.task.get("priority", "Low")
        border_color = PRIORITY_BORDER[priority]

        # Top row: title + Done button
        top_row = QHBoxLayout()
        top_row.setSpacing(8)

        self.lbl_title = QLabel(self.task["title"])
        self.lbl_title.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.lbl_title.setWordWrap(True)
        self.lbl_title.setStyleSheet("color:#1a1a2e;")
        top_row.addWidget(self.lbl_title, stretch=1)

        btn_done = QPushButton("✓ Done")
        btn_done.setFixedSize(72, 28)
        btn_done.setCursor(Qt.PointingHandCursor)
        btn_done.setToolTip("Mark as done and remove")
        btn_done.setStyleSheet(
            f"QPushButton{{background:transparent; border:1.5px solid {border_color};"
            f"border-radius:6px; font-size:9pt; color:{border_color}; font-weight:bold;}}"
            f"QPushButton:hover{{background:{border_color}; color:#fff;}}"
        )
        btn_done.clicked.connect(lambda: self.delete_requested.emit(self))
        top_row.addWidget(btn_done, alignment=Qt.AlignTop)

        # Bottom row: deadline + badge
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(8)

        deadline_str = self.task.get("deadline", "No deadline")
        lbl_dead = QLabel(f"📅  {deadline_str}")
        lbl_dead.setFont(QFont("Segoe UI", 9))
        lbl_dead.setStyleSheet("color:#555;")
        bottom_row.addWidget(lbl_dead)
        bottom_row.addStretch()

        bg, fg = PRIORITY_BADGE[priority]
        badge = QLabel(priority.upper())
        badge.setFixedSize(70, 20)
        badge.setAlignment(Qt.AlignCenter)
        badge.setStyleSheet(
            f"background:{bg}; color:{fg}; border-radius:9px;"
            f"font-size:8px; font-weight:bold; letter-spacing:1px;"
        )
        bottom_row.addWidget(badge)

        # Assemble
        outer = QVBoxLayout(self)
        outer.setContentsMargins(14, 10, 14, 10)
        outer.setSpacing(6)
        outer.addLayout(top_row)
        outer.addLayout(bottom_row)

    def _apply_style(self):
        priority = self.task.get("priority", "Low")
        bg     = PRIORITY_COLORS[priority]
        border = PRIORITY_BORDER[priority]
        self.setStyleSheet(
            f"TaskCard{{background:{bg}; border:1.5px solid {border};"
            f"border-radius:12px;}}"
            f"TaskCard:hover{{border:2px solid {border};}}"
        )

# ─────────────────────────────────────────────
#  AddTaskDialog – pop-up form
# ─────────────────────────────────────────────
class AddTaskDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Task")
        self.setFixedSize(320, 250)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title_label = QLabel("New Task")
        title_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        layout.addWidget(title_label)

        form = QFormLayout()
        self.inp_title = QLineEdit()
        self.inp_title.setPlaceholderText("Enter task name...")
        
        self.cmb_priority = QComboBox()
        self.cmb_priority.addItems(PRIORITY_LEVELS)
        
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("yyyy-MM-dd")

        form.addRow("Task:", self.inp_title)
        form.addRow("Priority:", self.cmb_priority)
        form.addRow("Deadline:", self.date_edit)
        layout.addLayout(form)

        btn_row = QHBoxLayout()
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.reject)
        
        btn_add = QPushButton("Add Task")
        btn_add.setStyleSheet("background: #3498db; color: white; font-weight: bold; padding: 8px; border-radius: 5px;")
        btn_add.clicked.connect(self._on_validate)
        
        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_add)
        layout.addLayout(btn_row)

    def _on_validate(self):
        if self.inp_title.text().strip(): self.accept()
        else: QMessageBox.warning(self, "Error", "Please enter a task title.")

    def get_task(self) -> dict:
        return {
            "title": self.inp_title.text(),
            "deadline": self.date_edit.date().toString("yyyy-MM-dd"),
            "priority": self.cmb_priority.currentText(),
            "done": False
        }


# ─────────────────────────────────────────────
#  MainWindow
# ─────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("To-Do List")
        self.resize(500, 650)
        self.tasks = []
        self.cards = []
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(25, 20, 25, 20)

        # Header
        header = QHBoxLayout()
        title = QLabel("My To-Do List")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        self.lbl_count = QLabel("0/0 done")
        self.lbl_count.setStyleSheet("color: #95a5a6; font-size: 10pt;")
        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.lbl_count)
        root.addLayout(header)

        # Buttons
        btns = QHBoxLayout()
        self.btn_add = self._create_nav_btn("＋ Add Task", "#3498db")
        self.btn_load = self._create_nav_btn("📂 Load JSON", "#7f8c8d")
        self.btn_save = self._create_nav_btn("💾 Save JSON", "#27ae60")
        
        self.btn_add.clicked.connect(self._add_task)
        self.btn_load.clicked.connect(self._load_json)
        self.btn_save.clicked.connect(self._save_json)
        
        btns.addWidget(self.btn_add)
        btns.addWidget(self.btn_load)
        btns.addWidget(self.btn_save)
        btns.addStretch()
        root.addLayout(btns)

        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("background: #eee;")
        root.addWidget(line)

        # Scroll Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.setStyleSheet("background: transparent;")
        
        self.container = QWidget()
        self.container.setStyleSheet("background: transparent;")
        self.card_layout = QVBoxLayout(self.container)
        self.card_layout.setSpacing(12)
        self.card_layout.addStretch() 
        
        self.lbl_empty = QLabel("No tasks yet.\nClick + Add Task to start!")
        self.lbl_empty.setAlignment(Qt.AlignCenter)
        self.lbl_empty.setStyleSheet("color: #bdc3c7; font-size: 11pt; margin-top: 50px;")
        self.card_layout.insertWidget(0, self.lbl_empty)

        self.scroll.setWidget(self.container)
        root.addWidget(self.scroll)

    def _create_nav_btn(self, text, color):
        btn = QPushButton(text)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {color}; color: white; border-radius: 6px;
                padding: 7px 12px; font-weight: bold; font-size: 9pt;
            }}
            QPushButton:hover {{ background: {color}; opacity: 0.8; }}
        """)
        return btn
    
  # ── task management ─────────────────────────

    def _add_task(self):
        dlg = AddTaskDialog(self)
        if dlg.exec() == QDialog.Accepted:
            task = dlg.get_task()
            self.tasks.append(task)
            self._insert_card(task)
            self._refresh_ui()

    def _insert_card(self, task):
        if not task.get("done"):
            card = TaskCard(task)
            card.delete_requested.connect(self._remove_card)
            self.card_layout.insertWidget(self.card_layout.count() - 1, card)
            self.cards.append(card)

    def _remove_card(self, card):
        card.task["done"] = True
        self.cards.remove(card)
        self.card_layout.removeWidget(card)
        card.deleteLater()
        self._refresh_ui()


    # ── JSON IO ─────────────────────────────────
    def _save_json(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save JSON", "", "JSON (*.json)")
        if path:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self.tasks, f, indent=4)
            QMessageBox.information(self, "Saved", "Tasks saved successfully!")

    def _load_json(self):
        path, _ = QFileDialog.getOpenFileName(self, "Load JSON", "", "JSON (*.json)")
        if path:
            with open(path, 'r', encoding='utf-8') as f:
                self.tasks = json.load(f)
            
            for c in self.cards: c.deleteLater()
            self.cards.clear()
            
            for t in self.tasks: self._insert_card(t)
            self._refresh_ui()

    def _refresh_ui(self):
        n = len(self.tasks)
        done = sum(1 for t in self.tasks if t.get("done"))
        self.lbl_count.setText(f"{done}/{n} done")
        self.lbl_empty.setVisible(len(self.cards) == 0)


    # ── helpers ─────────────────────────────────
    def _refresh_count(self):
        n    = len(self.tasks)
        done = sum(1 for t in self.tasks if t.get("done"))
        self.lbl_count.setText(f"{done}/{n} done")

    def _refresh_empty(self):
        has = len(self.tasks) > 0
        self.lbl_empty.setVisible(not has)
        #self.scroll_area.setVisible(has)

# ─────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())