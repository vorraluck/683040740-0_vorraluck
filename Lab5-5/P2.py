#Vorraluck Taladon
#683040740-0

"""
Student Registration System — PySide6
======================================
3 pages via QStackedWidget + Signal/Slot.

Page 1 : Card list (drag-drop reorder, delete)
Page 2 : Add student form
Page 3 : Review & confirm
"""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QComboBox, QPushButton, QFrame,
    QScrollArea, QSizePolicy, QMessageBox, QSpacerItem,
)
from PySide6.QtCore import Qt, QMimeData, QPoint, Signal
from PySide6.QtGui import QFont, QDrag, QPixmap, QPainter, QColor

COURSES = [
    "— Select Course —",
    "CS101 · Intro to Programming",
    "CS102 · Data Structures",
    "CS201 · Algorithms",
    "CS202 · Database Systems",
    "CS301 · Operating Systems",
    "CS302 · Computer Networks",
    "MATH101 · Calculus I",
    "MATH102 · Calculus II",
    "MATH201 · Linear Algebra",
    "ENG101 · Technical Writing",
    "PHYS101 · Physics I",
]

STYLE = """
QMainWindow, QWidget { background: #ffffff; font-family: 'Segoe UI'; font-size: 13px; }

/* ── Page 1 header ── */
#headerBar {
    border-bottom: 1px solid #e5e7eb;
    background: #ffffff;
}
#titleLabel { font-size: 20px; font-weight: bold; }
#countLabel { font-size: 13px; color: #6b7280; margin-left: 8px; }
#addBtn {
    background: #2563eb; color: white; border: none;
    border-radius: 6px; padding: 8px 18px; font-weight: bold;
}
#addBtn:hover { background: #1d4ed8; }

/* ── Student card ── */
#studentCard {
    background: #fce8e6;
    border-radius: 8px;
    border: 1px solid #f5c6c2;
}
#studentCard:hover { background: #f9d5d1; }
#dragHandle { color: #9ca3af; font-size: 16px; }
#studentName { font-weight: bold; font-size: 13px; }
#studentId   { color: #6b7280; font-size: 12px; }
#facultyLine { color: #6b7280; font-size: 12px; }
#courseLine  { color: #374151; font-size: 12px; }
#deleteBtn   { color: #9ca3af; border: none; background: transparent; font-size: 14px; }
#deleteBtn:hover { color: white; background: #ef4444; border-radius: 10px; }

/* ── Empty state ── */
#emptyLabel { color: #9ca3af; font-size: 13px; }

/* ── Page 2 — form ── */
#formTitle   { font-size: 20px; font-weight: bold; }
#sectionLabel { font-size: 10px; font-weight: bold; color: #6b7280; letter-spacing: 1px; }
#fieldLabel  { font-size: 13px; color: #374151; }

QLineEdit {
    border: 1px solid #d1d5db; border-radius: 6px;
    padding: 7px 10px; font-size: 13px; background: #ffffff;
}
QLineEdit:focus { border-color: #2563eb; }
QLineEdit[required="true"] { border-color: #d1d5db; }

QComboBox {
    border: 1px solid #d1d5db; border-radius: 6px;
    padding: 7px 10px; font-size: 13px; background: #ffffff;
}
QComboBox:focus { border-color: #2563eb; }
QComboBox::drop-down { border: none; width: 24px; }

/* ── Buttons ── */
#cancelBtn {
    border: 1px solid #d1d5db; border-radius: 6px;
    padding: 8px 20px; background: white; color: #374151;
}
#cancelBtn:hover { background: #f3f4f6; }
#reviewBtn {
    background: #2563eb; color: white; border: none;
    border-radius: 6px; padding: 8px 24px; font-weight: bold;
}
#reviewBtn:hover { background: #1d4ed8; }
#confirmBtn {
    background: #16a34a; color: white; border: none;
    border-radius: 6px; padding: 8px 24px; font-weight: bold;
}
#confirmBtn:hover { background: #15803d; }
#backBtn {
    border: 1px solid #d1d5db; border-radius: 6px;
    padding: 8px 20px; background: white; color: #374151;
}
#backBtn:hover { background: #f3f4f6; }

/* ── Page 3 review card ── */
#reviewCard {
    background: #f9fafb; border: 1px solid #e5e7eb;
    border-radius: 10px;
}
#reviewKey   { color: #6b7280; font-size: 12px; }
#reviewValue { font-size: 13px; color: #111827; }
"""

#Page 1
class StudentCard(QFrame):
    deleteRequested = Signal(int)   # emits index in the list

    def __init__(self, student: dict, index: int):
        super().__init__()
        self.student = student
        self.index   = index
        self.setObjectName("studentCard")
        self.setFixedHeight(90 + len(student["courses"]) * 18)
        self._build()
        self._dragging = False
        self.setAcceptDrops(False)

    def _build(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 10, 10)
        layout.setSpacing(8)

        handle = QLabel("⠿")
        handle.setObjectName("dragHandle")
        handle.setFixedWidth(18)
        handle.setCursor(Qt.OpenHandCursor)
        layout.addWidget(handle)

        info = QVBoxLayout()
        info.setSpacing(2)

        name_row = QHBoxLayout()
        name_lbl = QLabel(f"{self.student['first']} {self.student['last']}")
        name_lbl.setObjectName("studentName")
        sid_lbl  = QLabel(self.student["sid"])
        sid_lbl.setObjectName("studentId")
        name_row.addWidget(name_lbl)
        name_row.addWidget(sid_lbl)
        name_row.addStretch()
        info.addLayout(name_row)

        fac_lbl = QLabel(f"{self.student['faculty']}  ·  {self.student['major']}")
        fac_lbl.setObjectName("facultyLine")
        info.addWidget(fac_lbl)

        for c in self.student["courses"]:
            c_lbl = QLabel(c)
            c_lbl.setObjectName("courseLine")
            info.addWidget(c_lbl)

        layout.addLayout(info, 1)

        del_btn = QPushButton("✕")
        del_btn.setObjectName("deleteBtn")
        del_btn.setFixedSize(22, 22)
        del_btn.setCursor(Qt.PointingHandCursor)
        del_btn.clicked.connect(lambda: self.deleteRequested.emit(self.index))
        layout.addWidget(del_btn, 0, Qt.AlignTop)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_start = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            dist = (event.position().toPoint() - self._drag_start).manhattanLength()
            if dist > 10:
                self._start_drag()

    def _start_drag(self):
        drag = QDrag(self)
        mime = QMimeData()
        mime.setText(str(self.index))
        drag.setMimeData(mime)

        px = QPixmap(self.size())
        px.fill(Qt.transparent)
        p  = QPainter(px)
        p.setOpacity(0.7)
        self.render(p)
        p.end()
        drag.setPixmap(px)
        drag.setHotSpot(QPoint(self.width() // 2, self.height() // 2))
        drag.exec(Qt.MoveAction)

class Page1(QWidget):
    goToAdd = Signal()

    def __init__(self, students: list):
        super().__init__()
        self.students = students
        self._build()
        self.setAcceptDrops(True)

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Header bar
        header = QWidget()
        header.setObjectName("headerBar")
        header.setFixedHeight(60)
        hl = QHBoxLayout(header)
        hl.setContentsMargins(24, 0, 24, 0)

        title_lbl = QLabel("Students")
        title_lbl.setObjectName("titleLabel")
        self.count_lbl = QLabel("0 enrolled")
        self.count_lbl.setObjectName("countLabel")

        add_btn = QPushButton("+ Add Student")
        add_btn.setObjectName("addBtn")
        add_btn.clicked.connect(self.goToAdd)

        hl.addWidget(title_lbl)
        hl.addWidget(self.count_lbl)
        hl.addStretch()
        hl.addWidget(add_btn)
        root.addWidget(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.cards_container = QWidget()
        self.cards_layout    = QVBoxLayout(self.cards_container)
        self.cards_layout.setContentsMargins(24, 20, 24, 20)
        self.cards_layout.setSpacing(10)
        self.cards_layout.addStretch()

        scroll.setWidget(self.cards_container)
        root.addWidget(scroll, 1)

        self.empty_lbl = QLabel("No students registered yet.\nClick \"+ Add Student\" to get started.")
        self.empty_lbl.setObjectName("emptyLabel")
        self.empty_lbl.setAlignment(Qt.AlignCenter)
        self.cards_layout.insertWidget(0, self.empty_lbl)

        self.refresh()

    def refresh(self):
        while self.cards_layout.count() > 2:
            item = self.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        n = len(self.students)
        self.count_lbl.setText(f"{n} enrolled")
        self.empty_lbl.setVisible(n == 0)

        for i, s in enumerate(self.students):
            card = StudentCard(s, i)
            card.deleteRequested.connect(self._delete_student)
            self.cards_layout.insertWidget(i, card)

    def _delete_student(self, index):
        self.students.pop(index)
        self.refresh()

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        src = int(event.mimeData().text())
        y = event.position().toPoint().y()
        dst = len(self.students)
        for i in range(self.cards_layout.count()):
            item = self.cards_layout.itemAt(i)
            if item and item.widget() and isinstance(item.widget(), StudentCard):
                if y < item.widget().mapTo(self, QPoint(0, 0)).y() + item.widget().height() // 2:
                    dst = item.widget().index
                    break
        if src != dst:
            student = self.students.pop(src)
            dst = min(dst, len(self.students))
            self.students.insert(dst, student)
            self.refresh()
        event.acceptProposedAction()

#Page2
class Page2(QWidget):
    goBack    = Signal()
    goReview  = Signal(dict)

    def __init__(self):
        super().__init__()
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(40, 32, 40, 32)
        root.setSpacing(0)

        # Title
        title = QLabel("Add Student")
        title.setObjectName("formTitle")
        root.addWidget(title)

        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setStyleSheet("color: #e5e7eb;")
        root.addWidget(div)
        root.addSpacing(24)

        sec1 = QLabel("PERSONAL INFORMATION")
        sec1.setObjectName("sectionLabel")
        root.addWidget(sec1)
        root.addSpacing(12)

        grid = QGridLayout()
        grid.setSpacing(14)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(3, 1)

        def lbl(text):
            l = QLabel(text)
            l.setObjectName("fieldLabel")
            return l

        self.sid_input   = QLineEdit(); self.sid_input.setPlaceholderText("e.g. 65010001")
        self.first_input = QLineEdit(); self.first_input.setPlaceholderText("First name")
        self.last_input  = QLineEdit(); self.last_input.setPlaceholderText("Last name")
        self.fac_input   = QLineEdit(); self.fac_input.setPlaceholderText("e.g. Science & Technology")
        self.maj_input   = QLineEdit(); self.maj_input.setPlaceholderText("e.g. Computer Science")

        grid.addWidget(lbl("Student ID *"),  0, 0)
        grid.addWidget(self.sid_input,        0, 1, 1, 3)
        grid.addWidget(lbl("First Name *"),   1, 0)
        grid.addWidget(self.first_input,      1, 1)
        grid.addWidget(lbl("Last Name *"),    1, 2)
        grid.addWidget(self.last_input,       1, 3)
        grid.addWidget(lbl("Faculty *"),      2, 0)
        grid.addWidget(self.fac_input,        2, 1)
        grid.addWidget(lbl("Major *"),        2, 2)
        grid.addWidget(self.maj_input,        2, 3)

        root.addLayout(grid)
        root.addSpacing(28)

        sec2 = QLabel("COURSE SELECTION  (CHOOSE 1–3)")
        sec2.setObjectName("sectionLabel")
        root.addWidget(sec2)
        root.addSpacing(12)

        course_grid = QGridLayout()
        course_grid.setSpacing(14)
        course_grid.setColumnStretch(1, 1)

        self.course_cbs = []
        for i in range(3):
            cb = QComboBox()
            cb.addItems(COURSES)
            self.course_cbs.append(cb)
            course_grid.addWidget(lbl(f"Course {i+1}"), i, 0)
            course_grid.addWidget(cb, i, 1)

        root.addLayout(course_grid)
        root.addStretch()

        btn_row = QHBoxLayout()
        cancel_btn = QPushButton("← Cancel")
        cancel_btn.setObjectName("cancelBtn")
        cancel_btn.clicked.connect(self._cancel)

        review_btn = QPushButton("Review →")
        review_btn.setObjectName("reviewBtn")
        review_btn.clicked.connect(self._review)

        btn_row.addWidget(cancel_btn)
        btn_row.addStretch()
        btn_row.addWidget(review_btn)
        root.addLayout(btn_row)

    def clear(self):
        for w in (self.sid_input, self.first_input, self.last_input,
                  self.fac_input, self.maj_input):
            w.clear()
        for cb in self.course_cbs:
            cb.setCurrentIndex(0)

    def _cancel(self):
        self.clear()
        self.goBack.emit()

    def _review(self):
        fields = {
            "Student ID":  self.sid_input.text().strip(),
            "First Name":  self.first_input.text().strip(),
            "Last Name":   self.last_input.text().strip(),
            "Faculty":     self.fac_input.text().strip(),
            "Major":       self.maj_input.text().strip(),
        }
        missing = [k for k, v in fields.items() if not v]
        if missing:
            QMessageBox.warning(self, "Missing Fields",
                                "Please fill in: " + ", ".join(missing))
            return

        selected = [cb.currentText() for cb in self.course_cbs
                    if cb.currentIndex() > 0]
        if not selected:
            QMessageBox.warning(self, "No Course Selected",
                                "Please select at least one course.")
            return

        if len(selected) != len(set(selected)):
            QMessageBox.warning(self, "Duplicate Course",
                                "Please select different courses.")
            return

        self.goReview.emit({
            "sid":     fields["Student ID"],
            "first":   fields["First Name"],
            "last":    fields["Last Name"],
            "faculty": fields["Faculty"],
            "major":   fields["Major"],
            "courses": selected,
        })

#Page3
class Page3(QWidget):
    goBack    = Signal()
    confirmed = Signal(dict)

    def __init__(self):
        super().__init__()
        self._data = {}
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(40, 32, 40, 32)
        root.setSpacing(0)

        title = QLabel("Review Student Info")
        title.setObjectName("formTitle")
        root.addWidget(title)

        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setStyleSheet("color: #e5e7eb;")
        root.addWidget(div)
        root.addSpacing(24)

        card = QFrame()
        card.setObjectName("reviewCard")
        card_layout = QGridLayout(card)
        card_layout.setContentsMargins(24, 20, 24, 20)
        card_layout.setSpacing(12)
        card_layout.setColumnStretch(1, 1)

        def row_label(text):
            l = QLabel(text)
            l.setObjectName("reviewKey")
            return l

        self.rv = {}
        fields = [
            ("sid",     "Student ID"),
            ("first",   "First Name"),
            ("last",    "Last Name"),
            ("faculty", "Faculty"),
            ("major",   "Major"),
        ]
        for i, (key, label) in enumerate(fields):
            card_layout.addWidget(row_label(label), i, 0)
            lbl = QLabel("—")
            lbl.setObjectName("reviewValue")
            card_layout.addWidget(lbl, i, 1)
            self.rv[key] = lbl

        self.course_row_labels = []
        for j in range(3):
            r = len(fields) + j
            card_layout.addWidget(row_label(f"Course {j+1}"), r, 0)
            lbl = QLabel("—")
            lbl.setObjectName("reviewValue")
            card_layout.addWidget(lbl, r, 1)
            self.course_row_labels.append(lbl)

        root.addWidget(card)
        root.addStretch()

        btn_row = QHBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.setObjectName("backBtn")
        back_btn.clicked.connect(self.goBack)

        confirm_btn = QPushButton("✓ Confirm & Register")
        confirm_btn.setObjectName("confirmBtn")
        confirm_btn.clicked.connect(self._confirm)

        btn_row.addWidget(back_btn)
        btn_row.addStretch()
        btn_row.addWidget(confirm_btn)
        root.addLayout(btn_row)

    def load(self, data: dict):
        self._data = data
        self.rv["sid"].setText(data["sid"])
        self.rv["first"].setText(data["first"])
        self.rv["last"].setText(data["last"])
        self.rv["faculty"].setText(data["faculty"])
        self.rv["major"].setText(data["major"])
        for i, lbl in enumerate(self.course_row_labels):
            lbl.setText(data["courses"][i] if i < len(data["courses"]) else "—")

    def _confirm(self):
        self.confirmed.emit(self._data)

#MainWindow
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Registration")
        self.resize(900, 600)

        self.students: list[dict] = []

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.page1 = Page1(self.students)
        self.page2 = Page2()
        self.page3 = Page3()

        self.stack.addWidget(self.page1)  
        self.stack.addWidget(self.page2) 
        self.stack.addWidget(self.page3)  

        self.page1.goToAdd.connect(self._go_add)
        self.page2.goBack.connect(self._go_list)
        self.page2.goReview.connect(self._go_review)
        self.page3.goBack.connect(lambda: self.stack.setCurrentIndex(1))
        self.page3.confirmed.connect(self._confirm)

        self.stack.setCurrentIndex(0)

    def _go_add(self):
        self.page2.clear()
        self.stack.setCurrentIndex(1)

    def _go_list(self):
        self.stack.setCurrentIndex(0)

    def _go_review(self, data: dict):
        self.page3.load(data)
        self.stack.setCurrentIndex(2)

    def _confirm(self, data: dict):
        self.students.append(data)
        self.page1.refresh()
        self.page2.clear()
        self.stack.setCurrentIndex(0)

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
