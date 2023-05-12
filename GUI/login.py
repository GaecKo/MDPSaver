from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Signal
from MDPDatabase.controller import Controller

class LoginPage(QDialog):
    successful_login = Signal()

    def __init__(self, controller: Controller, parent=None):

        self.controller = controller
        
        super(LoginPage, self).__init__(parent)

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

        self.setLayout(layout)

    def check_login(self):
        # In a real application, you would authenticate against a database or an API
        if self.controller.check_login(self.password_input.text()): 
            self.successful_login.emit()
            self.close()
            
        else:
            QMessageBox.warning(self, "Error", "Invalid credentials.")
