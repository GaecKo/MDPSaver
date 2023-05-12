import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton

class AccountCreationWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Account Creation")

        # Username label and input
        self.username_label = QLabel("Username:", self)
        self.username_label.move(50, 30)
        self.username_input = QLineEdit(self)
        self.username_input.setGeometry(150, 30, 200, 20)

        # Password label and input
        self.password_label = QLabel("Password:", self)
        self.password_label.move(400, 30)
        self.password_input = QLineEdit(self)
        self.password_input.setGeometry(500, 30, 200, 20)
        self.password_input.setEchoMode(QLineEdit.Password)  # Hide entered text
        self.password_input.textChanged.connect(self.validate_password)

        # Recovery question label and input
        self.question_label = QLabel("Recovery Question:", self)
        self.question_label.move(50, 80)
        self.question_input = QLineEdit(self)
        self.question_input.setGeometry(150, 80, 550, 20)

        # Answer label and input
        self.answer_label = QLabel("Answer:", self)
        self.answer_label.move(50, 130)
        self.answer_input = QLineEdit(self)
        self.answer_input.setGeometry(150, 130, 200, 20)

        # Confirm button
        self.confirm_button = QPushButton("Confirm", self)
        self.confirm_button.setGeometry(300, 180, 200, 30)
        self.confirm_button.clicked.connect(self.confirm_account_creation)
        self.confirm_button.setEnabled(False)  # Initially disabled

    def validate_password(self, password):
        # Password validation criteria
        has_min_length = len(password) >= 8
        has_number = any(char.isdigit() for char in password)
        has_uppercase = any(char.isupper() for char in password)

        # Enable confirm button if all criteria are met, disable otherwise
        self.confirm_button.setEnabled(has_min_length and has_number and has_uppercase)

    def confirm_account_creation(self):
        # Retrieve entered values for further processing
        username = self.username_input.text()
        password = self.password_input.text()
        question = self.question_input.text()
        answer = self.answer_input.text()

        # Add your account creation logic here
        print("Account created successfully!")
        print(f"Username: {username}")
        print(f"Password: {password}")
        print(f"Recovery Question: {question}")
        print(f"Answer: {answer}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AccountCreationWindow()
    window.setGeometry(300, 300, 800, 250)  # Set window size
    window.show()
    sys.exit(app.exec())
