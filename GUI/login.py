from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Signal
from controller import Controller

class LoginWindow(QDialog):
    successful_login = Signal()
    recovery_login = Signal()

    def __init__(self, controller: Controller, parent=None):

        self.controller = controller
        
        super(LoginWindow, self).__init__(parent)

        self.setWindowTitle("Login")

        layout = QVBoxLayout()

        self.username_label = QLabel(f"{controller.get_username()}")
        layout.addWidget(self.username_label)

        self.password_label = QLabel("Password")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        layout.addWidget(self.login_button)

        self.login_button.clicked.connect(self.check_login)

        self.help_button = QPushButton("Forgot Password?")
        self.help_button.clicked.connect(self.recovery)

        layout.addWidget(self.help_button)

        self.setLayout(layout)

    def check_login(self):
        
        if self.controller.check_login(self.password_input.text()): 
            self.controller.load_app(self.password_input.text())
            self.successful_login.emit()
            self.close()
            
        else:
            QMessageBox.warning(self, "Error", "Invalid credentials.")

    def recovery(self):
        self.recovery_login.emit()
        self.close()
