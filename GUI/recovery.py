from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PySide6.QtCore import Signal
from controller import Controller, Recover

class RecoveryPage(QDialog):
    successful_recovery = Signal()
    failed_recovery = Signal()

    def __init__(self, controller: Controller, parent=None):

        self.controller = controller
        self.recover = Recover()
        self.good_answer = None # will be set to the good answer

        super(RecoveryPage, self).__init__(parent)

        self.setWindowTitle("Recovery")

        self.current_layout = self.answering_layout()

        self.setLayout(self.current_layout)


    def answering_layout(self) -> QVBoxLayout:
        layout = QVBoxLayout()

        self.username_label = QLabel(f"Recovery for: {self.controller.get_username()}")
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

        self.recover_button = QPushButton("Recover")
        layout.addWidget(self.recover_button)

        self.recover_button.clicked.connect(self.check_given_answer)

        return layout

    def new_informations_layout(self):

        self.mandatory_input = [False, False, False]
        # Passwords, Question, Answer

        # New Password
        self.new_password_label = QLabel(text="New password:")
        self.new_password = QLineEdit()
        self.new_password.textChanged.connect(self.check_passwords)

        self.current_layout.addWidget(self.new_password_label)
        self.current_layout.addWidget(self.new_password)

        # New Password Verif
        self.new_password_verif_label = QLabel(text="Confirm password:")
        self.new_password_verif = QLineEdit()
        self.new_password_verif.textChanged.connect(self.check_passwords)

        self.current_layout.addWidget(self.new_password_verif_label)
        self.current_layout.addWidget(self.new_password_verif)

        # New Question
        self.new_question_label = QLabel(text="Create new Question:")
        self.new_question = QLineEdit()
        self.new_question.textChanged.connect(self.check_question)

        self.current_layout.addWidget(self.new_question_label)
        self.current_layout.addWidget(self.new_question)

        # New Answer 
        self.new_answer_label = QLabel(text="Answer:")
        self.new_answer = QLineEdit()
        self.new_answer.textChanged.connect(self.check_answer)

        self.current_layout.addWidget(self.new_answer_label)
        self.current_layout.addWidget(self.new_answer)

        # confirm button
        self.confirm_button = QPushButton(text="Confirm")

        self.current_layout.addWidget(self.confirm_button)


    def check_mandotary_inputs(self):
        print(self.mandatory_input)
        for attr in self.mandatory_input:
            if attr == False:
                return False
        return True 

    def check_passwords(self):
        password = self.new_password.text()
        password_verif = self.new_password_verif.text()
        # Password validation criteria (1)
        has_min_length = len(password) >= 8 
        has_number = any(char.isdigit() for char in password)
        has_uppercase = any(char.isupper() for char in password)
        
        are_equel = password == password_verif

        # Enable confirm button if all criteria are met, disable otherwise
        if has_min_length and has_number and has_uppercase and are_equel:
            self.mandatory_input[0] = True
        else:
            self.mandatory_input[0] = False

        self.confirm_button.setEnabled(self.check_mandotary_inputs())

    def check_question(self, question):
        # Question validation criteria (1)
        has_min_length = len(question) > 10
        has_question = "?" in question 
        not_same_has_initial = question != self.rec_question

        # Switch to True this mandotary input if okay
        if has_min_length and has_question and not_same_has_initial:
            self.mandatory_input[1] = True
        else:
            self.mandatory_input[1] = False
        
        self.confirm_button.setEnabled(self.check_mandotary_inputs())

    def check_answer(self, answer):
        # Answer validation criteria (2)
        has_min_length = len(answer) >= 2

        # Enable confirm button if all criteria are met, disable otherwise
        if has_min_length:
            self.mandatory_input[2] = True
        else:
            self.mandatory_input[2] = False

        self.confirm_button.setEnabled(self.check_mandotary_inputs())

    def delete_layout(self):
        widgets = [self.current_layout.itemAt(i).widget() for i in range(self.current_layout.count())]

        for widgets in widgets:
            widgets.deleteLater()
        
        

    def check_given_answer(self):
        answer = self.answer_input.text() 
        if self.recover.verify_answer(answer):
            
            self.good_answer = answer

            self.delete_layout()

            self.setLayout(self.new_informations_layout())
           
            
        else:
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Wrong Answer")
            msg_box.setText("You gave the wrong answer. Please retry.")
            msg_box.setStandardButtons(QMessageBox.Ok)

            # Show the message box and wait for the user's response
            result = msg_box.exec()
            self.answer_input.setText("")