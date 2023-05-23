from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Signal
from controller import Controller, Recover

class RecoveryPage(QDialog):
    successful_recovery = Signal()
    failed_recovery = Signal()

    def __init__(self, controller: Controller, parent=None):

        self.controller = controller
        self.recover = Recover()

        super(RecoveryPage, self).__init__(parent)

        self.setWindowTitle("Recovery")

        layout = QVBoxLayout()

        self.username_label = QLabel(f"Recovery for: {controller.get_username()}")
        layout.addWidget(self.username_label)

        # Retrieve question using serial number
        self.rec_question = self.recover.get_personnal_question()



        self.question_label = QLabel("Question:")
        self.question = QLabel(self.rec_question)

        layout.addWidget(self.question_label)
        layout.addWidget(self.question)

        self.answer_label = QLabel("Answer:")
        self.answer_input = QLineEdit()

        layout.addWidget(self.answer_label)
        layout.addWidget(self.answer_input)

        self.login_button = QPushButton("Login")
        layout.addWidget(self.login_button)

        self.login_button.clicked.connect(self.check_login)

        self.help_button = QPushButton("Forgot Password?")

        self.setLayout(layout)

    def check_login(self):
        answer = self.answer_input.text()
        if self.recover.check_answer(answer):
            print("Answer is good")
        else:
            print("Answer is bad")