# Name: Your Name
# Student ID: 12345678

import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout,
    QCheckBox, QFrame
)
from PySide6.QtCore import Qt


class LoginUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.resize(380, 600)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(15)

        # ===== Title =====
        title = QLabel("LOGIN")
        title.setAlignment(Qt.AlignLeft)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(title)

        main_layout.addSpacing(20)

        # ===== Email =====
        email_label = QLabel("Email")
        email_input = QLineEdit()
        email_input.setFixedHeight(35)

        main_layout.addWidget(email_label)
        main_layout.addWidget(email_input)

        main_layout.addSpacing(15)

        # ===== Password =====
        password_label = QLabel("Password")
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)
        password_input.setFixedHeight(35)

        main_layout.addWidget(password_label)
        main_layout.addWidget(password_input)

        main_layout.addSpacing(10)

        # ===== Remember Me =====
        remember = QCheckBox("Remember me?")
        main_layout.addWidget(remember)

        main_layout.addSpacing(20)

        # ===== Login Button =====
        login_btn = QPushButton("LOGIN")
        login_btn.setFixedHeight(40)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #e6527a;
                color: white;
                border-radius: 8px;
                font-weight: bold;
            }
        """)
        main_layout.addWidget(login_btn)

        main_layout.addSpacing(10)

        # ===== Forgot Password =====
        forgot = QLabel("Forgot Password?")
        forgot.setAlignment(Qt.AlignRight)
        main_layout.addWidget(forgot)

        main_layout.addSpacing(20)

        # ===== OR Divider =====
        or_layout = QHBoxLayout()

        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)

        or_label = QLabel("OR")
        or_label.setAlignment(Qt.AlignCenter)
        or_label.setStyleSheet("padding: 3px; border: 1px solid gray;")

        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)

        or_layout.addWidget(line1)
        or_layout.addWidget(or_label)
        or_layout.addWidget(line2)

        main_layout.addLayout(or_layout)

        main_layout.addSpacing(20)

        # ===== Social Buttons =====
        social_layout = QHBoxLayout()
        social_layout.setAlignment(Qt.AlignCenter)

        google = QPushButton("G")
        facebook = QPushButton("f")
        linkedin = QPushButton("in")

        for btn in [google, facebook, linkedin]:
            btn.setFixedSize(40, 40)
            btn.setStyleSheet("border-radius: 20px;")

        social_layout.addWidget(google)
        social_layout.addWidget(facebook)
        social_layout.addWidget(linkedin)

        main_layout.addLayout(social_layout)

        main_layout.addSpacing(20)

        # ===== Sign Up =====
        signup = QLabel("Need an account? SIGN UP")
        signup.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(signup)

        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginUI()
    window.show()
    sys.exit(app.exec())
