# Name: [Your Name]
# Student ID: [Your ID]

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QStackedWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QLabel, QLineEdit, QDateEdit, QSpinBox,
    QPushButton, QDialog, QMessageBox, QScrollArea,
    QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QDate
from PySide6.QtGui import QFont

class RoomCard(QWidget):
    room_selected = Signal(str, int)

    def __init__(self, room_name: str, price: int, description: str, emoji: str = "🏨"):
        super().__init__()
        self._is_selected = False
        self.room_name = room_name
        self.price = price

        self._build_ui(emoji, description)
        self.deselect() 

    def _build_ui(self, emoji: str, description: str):
        self.setFixedSize(200, 200)
        self.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(6)

        self.emoji_lbl = QLabel(emoji)
        self.emoji_lbl.setAlignment(Qt.AlignCenter)
        self.emoji_lbl.setFont(QFont("Segoe UI", 24))

        self.name_lbl = QLabel(self.room_name)
        self.name_lbl.setAlignment(Qt.AlignCenter)
        self.name_lbl.setFont(QFont("Segoe UI", 11, QFont.Bold))

        self.price_lbl = QLabel(f"${self.price} / night")
        self.price_lbl.setAlignment(Qt.AlignCenter)
        self.price_lbl.setStyleSheet("color: #6366f1; font-weight: bold;")

        self.desc_lbl = QLabel(description)
        self.desc_lbl.setAlignment(Qt.AlignCenter)
        self.desc_lbl.setWordWrap(True)
        self.desc_lbl.setFont(QFont("Segoe UI", 9))
        self.desc_lbl.setStyleSheet("color: #6b7280;")

        self.select_btn = QPushButton("Select Room")
        self.select_btn.clicked.connect(self._on_select_clicked)

        layout.addWidget(self.emoji_lbl)
        layout.addWidget(self.name_lbl)
        layout.addWidget(self.price_lbl)
        layout.addWidget(self.desc_lbl)
        layout.addStretch()
        layout.addWidget(self.select_btn)

    def _on_select_clicked(self):
        self.room_selected.emit(self.room_name, self.price)

    def select(self):
        self._is_selected = True
        self.setStyleSheet("""
            RoomCard {
                background-color: #f0fdf4;
                border: 2px solid #22c55e;
                border-radius: 12px;
            }
        """)
        self.select_btn.setStyleSheet("""
            QPushButton {
                background-color: #22c55e;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 5px;
                font-weight: bold;
            }
        """)
        self.select_btn.setText("✓ Selected")

    def deselect(self):
        self._is_selected = False
        self.setStyleSheet("""
            RoomCard {
                background-color: #ffffff;
                border: 2px solid #e5e7eb;
                border-radius: 12px;
            }
            RoomCard:hover {
                border: 2px solid #6366f1;
                background-color: #f5f3ff;
            }
        """)
        self.select_btn.setStyleSheet("""
            QPushButton {
                background-color: #6366f1;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 5px;
            }
            QPushButton:hover { background-color: #4f46e5; }
        """)
        self.select_btn.setText("Select Room")

class ConfirmDialog(QDialog):
    def __init__(self, guest_name: str, room_name: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Booking Confirmed")
        self.setFixedSize(360, 220)
        self.setModal(True)
        self._build_ui(guest_name, room_name)

    def _build_ui(self, guest_name: str, room_name: str):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        icon_lbl = QLabel("🎉")
        icon_lbl.setFont(QFont("Segoe UI", 30))
        icon_lbl.setAlignment(Qt.AlignCenter)

        msg_lbl = QLabel(f"Thank you, <b>{guest_name}</b>!<br>Your booking for the <b>{room_name}</b> is confirmed.")
        msg_lbl.setAlignment(Qt.AlignCenter)
        msg_lbl.setWordWrap(True)

        self.ok_btn = QPushButton("Great!")
        self.ok_btn.clicked.connect(self.accept)
        self.ok_btn.setMinimumHeight(40)
        self.ok_btn.setStyleSheet("background-color: #6366f1; color: white; border-radius: 8px; font-weight: bold;")

        layout.addWidget(icon_lbl)
        layout.addWidget(msg_lbl)
        layout.addWidget(self.ok_btn)

# ─────────────────────────────────────────────
#  Page 1: Booking Page
# ─────────────────────────────────────────────
class BookingPage(QWidget):
    def __init__(self):
        super().__init__()
        self.selected_room = None
        self.selected_price = 0
        self.cards = []
        self._build_ui()

    def _build_ui(self):
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        container = QWidget()
        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(30, 24, 30, 24)
        main_layout.setSpacing(20)

        title = QLabel("🏨 Book Your Stay at CozyStay")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        main_layout.addWidget(title)

        # Form Section
        form_frame = QFrame()
        form_layout = QFormLayout(form_frame)
        
        self.name_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.checkin_input = QDateEdit(QDate.currentDate())
        self.checkin_input.setCalendarPopup(True)
        self.checkin_input.setDisplayFormat("dd/MM/yyyy")
        
        self.checkout_input = QDateEdit(QDate.currentDate().addDays(1))
        self.checkout_input.setCalendarPopup(True)
        self.checkout_input.setDisplayFormat("dd/MM/yyyy")
        
        self.guests_input = QSpinBox()
        self.guests_input.setRange(1, 10)
        self.guests_input.setSuffix(" guest(s)")

        # Style and Add to Layout
        input_style = "border: 1px solid #d1d5db; border-radius: 6px; padding: 6px; background: white;"
        for lbl_txt, widget in [("Full Name:", self.name_input), ("Phone Number:", self.phone_input), 
                                 ("Check-in:", self.checkin_input), ("Check-out:", self.checkout_input), 
                                 ("Guests:", self.guests_input)]:
            widget.setStyleSheet(input_style)
            form_layout.addRow(QLabel(lbl_txt), widget)
        
        main_layout.addWidget(form_frame)

        # Room Selection
        main_layout.addWidget(QLabel("<b>🛏 Select a Room</b>"))
        cards_layout = QHBoxLayout()
        rooms_data = [
            ("Standard Room", 50,  "Single bed, Free Wi-Fi", "🛏"),
            ("Deluxe Room",   120, "Double bed, Ocean view", "🌊"),
            ("Suite Room",    250, "Living room, Jacuzzi",   "👑")
        ]

        for name, price, desc, emoji in rooms_data:
            card = RoomCard(name, price, desc, emoji)
            card.room_selected.connect(self._on_room_selected)
            cards_layout.addWidget(card)
            self.cards.append(card)

        main_layout.addLayout(cards_layout)

        # Navigation
        btn_layout = QHBoxLayout()
        self.clear_btn = QPushButton("🗑 Clear Info")
        self.clear_btn.clicked.connect(self.clear_form)
        self.next_btn = QPushButton("Next →")
        
        btn_layout.addWidget(self.clear_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.next_btn)
        main_layout.addLayout(btn_layout)

        scroll.setWidget(container)
        QVBoxLayout(self).addWidget(scroll)

    def _on_room_selected(self, room_name: str, price: int):
        self.selected_room = room_name
        self.selected_price = price
        for card in self.cards:
            if card.room_name == room_name:
                card.select()
            else:
                card.deselect()

    def clear_form(self):
        self.name_input.clear()
        self.phone_input.clear()
        self.checkin_input.setDate(QDate.currentDate())
        self.checkout_input.setDate(QDate.currentDate().addDays(1))
        self.guests_input.setValue(1)
        self.selected_room = None
        for card in self.cards: card.deselect()

    def get_booking_data(self):
        name = self.name_input.text()
        phone = self.phone_input.text()
        checkin = self.checkin_input.date()
        checkout = self.checkout_input.date()

        if not name or not phone:
            QMessageBox.warning(self, "Error", "Fill in name and phone.")
            return None
        if checkin >= checkout:
            QMessageBox.warning(self, "Error", "Check-out must be after check-in.")
            return None
        if not self.selected_room:
            QMessageBox.warning(self, "Error", "Select a room.")
            return None

        nights = checkin.daysTo(checkout)
        return {
            "name": name, "phone": phone, "checkin": self.checkin_input.text(),
            "checkout": self.checkout_input.text(), "room": self.selected_room,
            "price": self.selected_price, "nights": nights, "guests": self.guests_input.value(),
            "total": nights * self.selected_price
        }

# ─────────────────────────────────────────────
#  PAGE 2: ReviewPage
# ─────────────────────────────────────────────
class ReviewPage(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        self.labels = {}
        
        title = QLabel("📋 Booking Summary")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        layout.addWidget(title)

        self.info_frame = QFrame()
        self.info_layout = QFormLayout(self.info_frame)
        
        fields = ["Room", "Guest Name", "Phone", "Check-in", "Check-out", "Nights", "Total Price"]
        for field in fields:
            lbl = QLabel("-")
            self.labels[field] = lbl
            self.info_layout.addRow(QLabel(f"<b>{field}:</b>"), lbl)
            
        layout.addWidget(self.info_frame)

        btn_layout = QHBoxLayout()
        self.back_btn = QPushButton("← Back")
        self.submit_btn = QPushButton("✅ Confirm Booking")
        btn_layout.addWidget(self.back_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.submit_btn)
        layout.addLayout(btn_layout)

    def load_data(self, data: dict):
        self.labels["Room"].setText(data["room"])
        self.labels["Guest Name"].setText(data["name"])
        self.labels["Phone"].setText(data["phone"])
        self.labels["Check-in"].setText(data["checkin"])
        self.labels["Check-out"].setText(data["checkout"])
        self.labels["Nights"].setText(str(data["nights"]))
        self.labels["Total Price"].setText(f"${data['total']}")
        self.labels["Total Price"].setStyleSheet("font-size: 16px; color: green; font-weight: bold;")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CozyStay — Hotel Booking System")
        self.setMinimumSize(850, 700)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.page1 = BookingPage()
        self.page2 = ReviewPage()

        self.stack.addWidget(self.page1)
        self.stack.addWidget(self.page2)

        self.page1.next_btn.clicked.connect(self._go_to_review)
        self.page2.back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.page2.submit_btn.clicked.connect(self._on_submit)

    def _go_to_review(self):
        data = self.page1.get_booking_data()
        if data:
            self.page2.load_data(data)
            self.stack.setCurrentIndex(1)

    def _on_submit(self):
        data = self.page1.get_booking_data()
        dlg = ConfirmDialog(data["name"], data["room"], self)
        if dlg.exec():
            self.page1.clear_form()
            self.stack.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())