from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Signal


class LoginPage(QDialog):
    successful_login = Signal()

    def __init__(self, parent=None):
        super(LoginPage, self).__init__(parent)

        self.setWindowTitle("Login")

        layout = QVBoxLayout()

        self.username_label = QLabel("Username")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Password")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        layout.addWidget(self.login_button)

        self.login_button.clicked.connect(self.check_login)

        self.setLayout(layout)

    def check_login(self):
        # In a real application, you would authenticate against a database or an API
        if self.username_input.text() == "admin" and self.password_input.text() == "password":
            self.successful_login.emit()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Invalid credentials.")
