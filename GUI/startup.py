import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Signal, QSize
from controller import Controller

class AccountCreationWindow(QMainWindow):

    successfull_startup = Signal()
    failed_startup = Signal()

    def __init__(self, controller: Controller):
        super().__init__()

        self.setStyleSheet(open("MDPStyle/startup.css").read())

        self.setWindowTitle("Account Creation")
        self.setFixedSize(QSize(800, 300))

        self.controller = controller

        self.mandatory_input = [False, False, False, False]
        # [Username, Password, Rec Question, Answer]

        # Username label and input
        self.username_label = QLabel("Username:", self)
        self.username_label.move(50, 30)
        self.username_input = QLineEdit(self)
        self.username_input.setGeometry(150, 30, 200, 20)
        self.username_input.textChanged.connect(self.validate_username)

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
        self.question_input.textChanged.connect(self.validate_question)

        # Answer label and input
        self.answer_label = QLabel("Answer:", self)
        self.answer_label.move(50, 130)
        self.answer_input = QLineEdit(self)
        self.answer_input.setGeometry(150, 130, 200, 20)
        self.answer_input.textChanged.connect(self.validate_answer)

        # Confirm button
        self.confirm_button = QPushButton("Confirm", self)
        self.confirm_button.setGeometry(300, 180, 200, 30)
        self.confirm_button.clicked.connect(self.confirm_account_creation)
        self.confirm_button.setEnabled(False)  # Initially disabled

    def validate_username(self, username):
        # Username validation criteria (0)
        has_min_length = len(username) >= 2

        # Enable confirm button if all criteria are met, disable otherwise
        if has_min_length:
            self.mandatory_input[0] = True
        else:
            self.mandatory_input[0] = False

        self.confirm_button.setEnabled(self.check_mandotary_inputs())

    def validate_password(self, password):
        # Password validation criteria (1)
        has_min_length = len(password) >= 8
        has_number = any(char.isdigit() for char in password)
        has_uppercase = any(char.isupper() for char in password)

        # Enable confirm button if all criteria are met, disable otherwise
        if has_min_length and has_number and has_uppercase:
            self.mandatory_input[1] = True
        else:
            self.mandatory_input[1] = False

        self.confirm_button.setEnabled(self.check_mandotary_inputs())

    # TODO: Check answer & question simultaneously (answer shouldnt be in question)
    def validate_question(self, question):
        answer = self.answer_input.text()
        # Question validation criteria (2)
        has_min_length = len(question) > 10
        has_question = "?" in question 
        not_answer_in = answer.strip() not in question if len(answer) > 0 else True



        # Switch to True this mandotary input if okay
        if has_min_length and has_question and not_answer_in:
            self.mandatory_input[2] = True
        else:
            self.mandatory_input[2] = False
        
        self.confirm_button.setEnabled(self.check_mandotary_inputs())

    def validate_answer(self, answer):
        # Answer validation criteria (3)
        question = self.question_input.text()
        
        has_min_length = len(answer) >= 2
        not_answer_in = answer.strip() not in question if len(answer) > 0 else True



        # Enable confirm button if all criteria are met, disable otherwise
        if has_min_length and not_answer_in:
            self.mandatory_input[3] = True
        else:
            self.mandatory_input[3] = False

        self.confirm_button.setEnabled(self.check_mandotary_inputs())

    def check_mandotary_inputs(self):
        print(self.mandatory_input)
        for state in self.mandatory_input:
            if state == False:
                return False
        return True

    def confirm_account_creation(self):
        
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Account Creation")
        msg_box.setText("Do you confirm account creation? These informations can still be changed later on.")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        # Show the message box and wait for the user's response
        result = msg_box.exec()

        # If the user clicked 'Yes', create the account
        if result != QMessageBox.Yes:
            return

        # Retrieve entered values for further processing
        username = self.username_input.text()
        password = self.password_input.text()
        question = self.question_input.text()
        answer = self.answer_input.text()

        # XXX call 2 functions instead of just one. 
        if self.controller.initiate_db_settings(username, password, question, answer):
            self.successfull_startup.emit()
            self.close()
            
        else:
            self.controller.kill_db()

            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle("Error")
            msg_box.setText("An error occurred:")
            msg_box.setInformativeText("An error occured while initializing the app. Please retry. If the error persists, contact dev team.")
            msg_box.setStandardButtons(QMessageBox.Ok)

            msg_box.exec()
            self.close()
            self.failed_startup.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AccountCreationWindow()
    window.setGeometry(300, 300, 800, 250)  # Set window size
    window.show()
    sys.exit(app.exec())
