from PySide6.QtWidgets import QMainWindow, QStackedWidget, QMessageBox, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget, QLineEdit, QFrame
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from utils.PasswordPromp import PasswordPrompt
from utils.SceneGenerator import SceneImage
from controller import Controller

# TODO: work on QMessageBox design as well as the horizontal alignement of the forms for general coherence

class Welcome(QWidget):
    def __init__(self, parent=None):
        # TODO: clean code and add comments
        super().__init__(parent)

        self.setStyleSheet(open("startup.css").read())
        self.setFixedSize(400, 400)

        self.setObjectName("welcome")

        self.GenHBox = QVBoxLayout()
        self.GenHBox.setSpacing(5)

        line = QFrame(self)
        line.setObjectName("line")
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setLineWidth(8)


        self.logo_scene = SceneImage("MDPStyle/MDPSaver.png", 0.4, 0.4)
        self.logo_scene.setFixedSize(350, 130)


        self.presentation_text = QLabel()
        self.presentation_text.setAlignment(Qt.AlignCenter)
        self.presentation_text.setWordWrap(True)
        self.presentation_text.setText("""<span style="font-weight: bold;">MDPSaver</span> makes it easy to <span style="font-weight: bold;">store</span>, <span style="font-weight: bold;">access</span> & <span style="font-weight: bold;">generate passwords</span>. A single password gives you access to <span style="font-weight: bold;">all</span> your passwords, at <span style="font-weight: bold;">any</span> time.""")
        self.presentation_text.setFixedWidth(320)
        self.presentation_text.setObjectName("presentation-text")
        
        empty = " " * 16
    
        self.nextButton = QPushButton(text="Let's get started!" + empty, icon=QIcon("MDPStyle/right-arrow.png"))
        self.nextButton.setLayoutDirection(Qt.RightToLeft)
        self.nextButton.setCursor(Qt.PointingHandCursor)
        self.nextButton.setFixedWidth(320)
        self.nextButton.setFixedHeight(50)
        self.nextButton.clicked.connect(parent.show_next_page)

        self.GenHBox.addWidget(self.logo_scene, alignment=Qt.AlignCenter)
        self.GenHBox.addWidget(line)
        self.GenHBox.addWidget(self.presentation_text, alignment=Qt.AlignCenter)
        self.GenHBox.addWidget(self.nextButton, alignment=Qt.AlignCenter)
        self.setLayout(self.GenHBox)

class LoginForm(QWidget):
    def __init__(self, parent=None):
        # TODO: clean code and add comments
        super().__init__(parent)
        self.inputs_validity = [False, False]
        # [username, password]

        self.parent = parent

        self.setStyleSheet(open("startup.css").read())
        self.setFixedSize(400, 400)

        self.setObjectName("login-form")

        self.GenHBox = QVBoxLayout()
        

        self.title = QLabel(text="Login Information")
        self.title.setObjectName("title")

        # //// USERNAME PART ////
        self.username_layout = QVBoxLayout()
        self.username_layout.setSpacing(5)
        
        self.username_label_layout = QHBoxLayout()

        self.username_layout.setContentsMargins(10, 20, 10, 20)

        self.username_text = "<span style='font-weight: bold; color:white; font-size: 20px;'>Username*</span>"

        self.usermame_requirement = "<span style='color: red; font-size:13px; font-style:italic;'>* 2+ chars</span>"

        self.username_label = QLabel(text=self.username_text)   
        self.username_requirement_label = QLabel(text=self.usermame_requirement)

        self.username_label_layout.addWidget(self.username_label, alignment=Qt.AlignLeft)
        self.username_label_layout.addWidget(self.username_requirement_label, alignment=Qt.AlignRight)

        self.username_input = QLineEdit()
        self.username_input.setFixedWidth(360)
        self.username_input.setFixedHeight(29)
        self.username_input.textChanged.connect(self.validate_username)

        self.username_layout.addLayout(self.username_label_layout)
        self.username_layout.addWidget(self.username_input, alignment=Qt.AlignCenter)

        # //// PASSWORD PART ////
        self.password_layout = QVBoxLayout()
        self.password_layout.setSpacing(0)
        self.password_layout.setContentsMargins(10, 20, 10, 40)

        self.password_label_layout = QHBoxLayout()

        self.password_text =  "<span style='font-weight: bold; color:white; font-size: 20px;'>Access Password*</span>"

        self.password_requirement = "<span style='color: red; font-size:13px; font-style:italic;'>* 8+ chars, 1 symbol, 1 digit</span>"

        self.password_label = QLabel(text=self.password_text)
        self.password_requirement_label = QLabel(text=self.password_requirement)

        self.password_label_layout.addWidget(self.password_label, alignment=Qt.AlignLeft)
        self.password_label_layout.addWidget(self.password_requirement_label, alignment=Qt.AlignRight)

        self.password_input = PasswordPrompt()
        self.password_input.setFixedWidth(360)
        self.password_input.textChanged.connect(self.validate_password)

        self.password_layout.addLayout(self.password_label_layout)
        self.password_layout.addWidget(self.password_input, alignment=Qt.AlignCenter)

        line = QFrame(self)
        line.setObjectName("line2")
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setLineWidth(8)

        self.button_layout = QHBoxLayout()
        
        empty = " " * 3

        self.nextButton = QPushButton(text="Next" + empty, icon=QIcon("right-arrow.png"))
        self.setStyleSheet("""QPushButton:hover {    background-color: #2fa572; border: none;}""")
        self.update()
        self.nextButton.setLayoutDirection(Qt.RightToLeft)
        self.nextButton.setCursor(Qt.ForbiddenCursor)
        self.nextButton.setFixedHeight(50)
        self.nextButtonConnected = False
        

        self.prevButton = QPushButton(text="Back")
        self.prevButton.setCursor(Qt.PointingHandCursor)
        self.prevButton.setObjectName("backButton")
        self.prevButton.setFixedHeight(50)
        self.prevButton.clicked.connect(parent.show_prev_page)

        self.button_layout.addWidget(self.prevButton, 2)
        self.button_layout.addWidget(self.nextButton, 4)

        self.GenHBox.addWidget(self.title, alignment=Qt.AlignCenter)
        self.GenHBox.addWidget(line)
        self.GenHBox.addLayout(self.username_layout)
        self.GenHBox.addLayout(self.password_layout)
        self.GenHBox.addLayout(self.button_layout)
        
        self.setLayout(self.GenHBox)

    def validate_username(self, username):
        if len(username) < 2:
            self.username_input.setStyleSheet("border: 2px solid red;")
            self.username_requirement_label.setText("<span style='color: red; font-size:13px; font-style:italic;'>* 2+ chars</span>")
            self.inputs_validity[0] = False
            
        else:
            self.username_input.setStyleSheet("border: 2px solid green;")
            self.username_requirement_label.setText("<span style='color: green; font-size:13px; font-style:italic;'>* 2+ chars</span>")
            self.inputs_validity[0] = True

        self.verify_inputs()
    
    def validate_password(self, password):
        has_min_length = len(password) >= 8
        has_uppercase = any(char.isupper() for char in password)
        has_symbol = any(char in "}!@#$%^&*()-+?_=,<>/;:[]{" for char in password)

        if has_min_length and has_uppercase and has_symbol:
            self.password_input.setInputStyleSheet("border: 2px solid green;")
            self.password_requirement_label.setText("<span style='color: green; font-size:13px; font-style:italic;'>* 8+ chars, 1 symbol, 1 digit</span>")
            self.inputs_validity[1] = True

        else:
            self.password_input.setInputStyleSheet("border: 2px solid red;")
            self.password_requirement_label.setText("<span style='color: red; font-size:13px; font-style:italic;'>* 8+ chars, 1 symbol, 1 digit</span>")
            self.inputs_validity[1] = False
        self.verify_inputs()

    def verify_inputs(self):
        for bool_v in self.inputs_validity:
            if not bool_v :
                self.nextButton.setCursor(Qt.ForbiddenCursor)
                if self.nextButtonConnected:
                    self.nextButton.clicked.disconnect()
                    self.nextButtonConnected = False
                
                self.setStyleSheet("""QPushButton:hover {    background-color: #2fa572; border: none;}""")
                self.update()
                return

        self.nextButton.setCursor(Qt.PointingHandCursor)
        if self.nextButtonConnected:
            self.nextButton.clicked.disconnect()
        self.setStyleSheet("""QPushButton:hover {background-color: #2f8c66; border: 4px solid white;}""")
        self.nextButtonConnected = True
        self.nextButton.clicked.connect(self.parent.show_next_page)

    def get_username_password(self):
        return self.username_input.text(), self.password_input.text()  

class RecoveryForm(QWidget):

    def __init__(self, parent=None):
        # TODO: clean code and add comments
        super().__init__(parent)
        self.inputs_validity = [False, False]
        # [question, answer]
        self.parent = parent

        self.setStyleSheet(open("startup.css").read())
        self.setFixedSize(400, 400)

        self.setObjectName("recovery-form")

        self.GenHBox = QVBoxLayout()
        

        self.title = QLabel(text="Recovery Information")
        self.title.setObjectName("title")

        self.explain_text = "<span style='font-weight: italic; color:white; font-size: 15px;'>To enable <span style='font-weight:bold;'>account recovery</span> in case of a forgotten Access Password, please <span style='font-weight:bold;'>create</span> a <span style='font-weight:bold;'>question and its answer</span>. Don't forget it!</span>"
        
        self.explanation = QLabel(text=self.explain_text)
        self.explanation.setWordWrap(True)
        self.explanation.setAlignment(Qt.AlignCenter)
        self.explanation.setFixedWidth(360)
        self.explanation.setContentsMargins(0, 20, 0, 10)

        # //// Question PART ////
        self.question_layout = QVBoxLayout()
        self.question_layout.setSpacing(5)
        
        self.question_label_layout = QHBoxLayout()

        self.question_layout.setContentsMargins(10, 10, 10, 10)

        self.question_text = "<span style='font-weight: bold; color:white; font-size: 20px;'>Recovery Question*</span>"

        self.question_requirement = "<span style='color: red; font-size:13px; font-style:italic;'>* 10+ chars, contains '?'</span>"

        self.question_label = QLabel(text=self.question_text)   
        self.question_requirement_label = QLabel(text=self.question_requirement)

        self.question_label_layout.addWidget(self.question_label, alignment=Qt.AlignLeft)
        self.question_label_layout.addWidget(self.question_requirement_label, alignment=Qt.AlignRight)

        self.question_input = QLineEdit()
        self.question_input.setFixedWidth(360)
        self.question_input.setFixedHeight(29)
        self.question_input.textChanged.connect(self.connect_question) 

        self.question_layout.addLayout(self.question_label_layout)
        self.question_layout.addWidget(self.question_input, alignment=Qt.AlignCenter)

        # //// ANSWER PART ////
        self.answer_layout = QVBoxLayout()
        self.answer_layout.setSpacing(0)
        self.answer_layout.setContentsMargins(10, 0, 10, 20)

        self.answer_label_layout = QHBoxLayout()

        self.answer_text =  "<span style='font-weight: bold; color:white; font-size: 20px;'>Answer*</span>"

        self.answer_requirement = "<span style='color: red; font-size:13px; font-style:italic;'>* 3+ chars</span>"

        self.answer_label = QLabel(text=self.answer_text)
        self.answer_requirement_label = QLabel(text=self.answer_requirement)

        self.answer_label_layout.addWidget(self.answer_label, alignment=Qt.AlignLeft)
        self.answer_label_layout.addWidget(self.answer_requirement_label, alignment=Qt.AlignRight)

        self.answer_input = QLineEdit()
        self.answer_input.setFixedWidth(360)
        self.answer_input.setFixedHeight(29)
        self.answer_input.textChanged.connect(self.validate_answer)

        self.answer_in_question = QLabel(text="<span style='color: red; font-size:13px; font-style:italic;'>* Question must not contain answer</span>")
        self.answer_in_question.hide()

        self.answer_layout.addLayout(self.answer_label_layout)
        self.answer_layout.addWidget(self.answer_input, alignment=Qt.AlignCenter)
        self.answer_layout.addWidget(self.answer_in_question, alignment=Qt.AlignCenter)

        line = QFrame(self)
        line.setObjectName("line2")
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setLineWidth(8)

        self.button_layout = QHBoxLayout()
        

        self.nextButton = QPushButton(text="Create Account  ", icon=QIcon("right-arrow.png"))
        self.setStyleSheet("""QPushButton:hover {    background-color: #2fa572; border: none;}""")
        self.update()
        self.nextButton.setLayoutDirection(Qt.RightToLeft)
        self.nextButton.setCursor(Qt.ForbiddenCursor)
        self.nextButton.setFixedHeight(50)
        self.nextButtonConnected = False

        self.prevButton = QPushButton(text="Back")
        self.prevButton.setCursor(Qt.PointingHandCursor)
        self.prevButton.setObjectName("backButton")
        self.prevButton.setFixedHeight(50)
        self.prevButton.clicked.connect(parent.show_prev_page)

        self.button_layout.addWidget(self.prevButton, 2)
        self.button_layout.addWidget(self.nextButton, 4)

        self.GenHBox.addWidget(self.title, alignment=Qt.AlignCenter)
        self.GenHBox.addWidget(line)
        self.GenHBox.addWidget(self.explanation, alignment=Qt.AlignCenter)
        self.GenHBox.addLayout(self.question_layout)
        self.GenHBox.addLayout(self.answer_layout)
        self.GenHBox.addLayout(self.button_layout)
        
        self.setLayout(self.GenHBox)

    def connect_question(self):
        self.validate_question(self.question_input.text())
        self.validate_answer(self.answer_input.text())

    def validate_question(self, question):

        has_min_length = len(question) >= 10
        has_question_mark = "?" in question
        

        if has_min_length and has_question_mark:
            self.question_input.setStyleSheet("border: 2px solid green;")
            self.question_requirement_label.setText("<span style='color: green; font-size:13px; font-style:italic;'>* 10+ chars, coutains '?'</span>")
            self.inputs_validity[0] = True
            
        else:
            self.question_input.setStyleSheet("border: 2px solid red;")
            self.question_requirement_label.setText("<span style='color: red; font-size:13px; font-style:italic;'>* 10+ chars, coutains '?'</span>")
            self.inputs_validity[0] = False

        self.verify_inputs()
    
    def is_not_in_question(self, answer, question):
        if len(answer) == 0: return True\
        
        question.replace("?", "")
        questions_words = question.split(" ")
        for word in questions_words:
            if word.lower() == answer.lower():
                return False
        return True

    def validate_answer(self, answer):
        has_min_length = len(answer) >= 3
        is_not_in_question = self.is_not_in_question(answer, self.question_input.text())

        if has_min_length :
            self.answer_requirement_label.setText("<span style='color: green; font-size:13px; font-style:italic;'>* 3+ chars</span>")

        else:
            self.answer_requirement_label.setText("<span style='color: red; font-size:13px; font-style:italic;'>* 3+ chars</span></span>")

        if is_not_in_question:
            self.answer_in_question.hide()
        else:
            self.answer_in_question.show()

        if is_not_in_question and has_min_length:
            self.answer_input.setStyleSheet("border: 2px solid green;")
            self.inputs_validity[1] = True
        else:
            self.answer_input.setStyleSheet("border: 2px solid red;")
            self.inputs_validity[1] = False
        
        self.verify_inputs()

    def verify_inputs(self):
        for bool_v in self.inputs_validity:
            if not bool_v:
                self.nextButton.setCursor(Qt.ForbiddenCursor)
                if self.nextButtonConnected:
                    self.nextButton.clicked.disconnect()
                    self.nextButtonConnected = False
                self.setStyleSheet("""QPushButton:hover {    background-color: #2fa572; border: none;}""")
                self.update()

                return

        self.nextButton.setCursor(Qt.PointingHandCursor)
        if self.nextButtonConnected: 
            self.nextButton.clicked.disconnect()
        self.setStyleSheet("""QPushButton:hover {background-color: #2f8c66; border: 4px solid white;}""")
        self.nextButtonConnected = True

        self.nextButton.clicked.connect(self.finish_form)
        
    def finish_form(self):
        self.parent.information_retrieved.emit()

    def get_question_answer(self):
        return self.question_input.text(), self.answer_input.text()

class AccountCreationWindow(QMainWindow):

    information_retrieved = Signal()
    successfull_startup = Signal()
    failed_startup = Signal()


    def __init__(self, controller: Controller):
        super().__init__()

        self.controller = controller

        self.setStyleSheet(open("startup.css").read())
        self.setObjectName("startup")
        self.setWindowTitle("MDPSaver Startup")

        self.welcome_page = Welcome(self)
        self.login_page = LoginForm(self)
        self.recovery_page = RecoveryForm(self)

        self.widgets = [self.welcome_page, self.login_page, self.recovery_page]

        self.QStackedWidget = QStackedWidget()
        self.cur_page = 0
        self.QStackedWidget.addWidget(self.welcome_page)
        self.QStackedWidget.addWidget(self.login_page)
        self.QStackedWidget.addWidget(self.recovery_page)

        self.QStackedWidget.setCurrentIndex(self.cur_page)

        self.setCentralWidget(self.QStackedWidget)
    
        # Set up signal so it retrieves informations from child pages
        self.information_retrieved.connect(self.process_account_creation)

    def show_next_page(self):
        if self.cur_page == 2: return

        self.cur_page += 1
        self.QStackedWidget.setCurrentIndex(self.cur_page)

    def show_prev_page(self):
        if self.cur_page == 0: return

        self.cur_page -= 1
        self.QStackedWidget.setCurrentIndex(self.cur_page)

    def process_account_creation(self):
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

        # TODO: Check if values are valid (strip)
        username, password = self.login_page.get_username_password()
        question, answer = self.recovery_page.get_question_answer()

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
            self.parent.failed_startup.emit()
