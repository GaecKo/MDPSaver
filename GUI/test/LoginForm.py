from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QHBoxLayout, QLineEdit
from utils.PasswordPromp import PasswordPrompt



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

    def fade_in(self):
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.Linear)

        self.animation.start()
        self.animation.deleteLater()
        

    def fade_out(self):
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.setEasingCurve(QEasingCurve.Linear)

        self.animation.start()
        self.animation.deleteLater()
    
    def graphicsEffect(self):
        super().graphicsEffect()

    
if __name__ == '__main__':
    app = QApplication([])

    window = LoginForm()
    window.show()

    app.exec()