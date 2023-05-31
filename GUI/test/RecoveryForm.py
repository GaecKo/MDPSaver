from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QSizePolicy, QHBoxLayout, QLineEdit, QLayout
from utils.SceneGenerator import SceneImage
from utils.PasswordPromp import PasswordPrompt



class LoginForm(QWidget):
    def __init__(self, parent=None):
        # TODO: clean code and add comments
        super().__init__(parent)
        self.inputs_validity = [False, False]
        # [question, answer]

        self.setStyleSheet(open("startup.css").read())
        self.setFixedSize(400, 400)

        self.setObjectName("recovery-form")

        self.GenHBox = QVBoxLayout()
        

        self.title = QLabel(text="Recovery Information")
        self.title.setObjectName("title")

        self.explain_text = "<span style='font-weight: italic; color:white; font-size: 15px;'>To enable <span style='font-weight:bold;'>account recovery</span> in case of a forgotten Access Password, please <span style='font-weight:bold;'>create</span> a <span style='font-weight:bold;'>question and answer</span>. You will be asked this question to recover your account.</span>"
        
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
        self.question_input.textChanged.connect(lambda: self.validate_question(self.question_input.text()) and self.validate_answer()) 

        self.question_layout.addLayout(self.question_label_layout)
        self.question_layout.addWidget(self.question_input, alignment=Qt.AlignCenter)

        # //// ANSWER PART ////
        self.answer_layout = QVBoxLayout()
        self.answer_layout.setSpacing(0)
        self.answer_layout.setContentsMargins(10, 10, 10, 10)

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

        self.answer_in_question = QLabel(text="<span style='color: red; font-size:13px; font-style:italic;'>* Question cannot contain answer</span>")
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
        self.nextButton.setLayoutDirection(Qt.RightToLeft)
        self.nextButton.setCursor(Qt.ForbiddenCursor)
        self.nextButton.setFixedHeight(50)
        self.nextButton.clicked.connect(lambda: None)

        self.prevButton = QPushButton(text="Back")
        self.prevButton.setCursor(Qt.PointingHandCursor)
        self.prevButton.setObjectName("backButton")
        self.prevButton.setFixedHeight(50)
        # self.prevButton.clicked.connect(parent.showPrevForm)

        self.button_layout.addWidget(self.prevButton, 2)
        self.button_layout.addWidget(self.nextButton, 4)

        self.GenHBox.addWidget(self.title, alignment=Qt.AlignCenter)
        self.GenHBox.addWidget(line)
        self.GenHBox.addWidget(self.explanation, alignment=Qt.AlignCenter)
        self.GenHBox.addLayout(self.question_layout)
        self.GenHBox.addLayout(self.answer_layout)
        self.GenHBox.addLayout(self.button_layout)
        
        self.setLayout(self.GenHBox)

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
    
    def validate_answer(self, answer):
        has_min_length = len(answer) >= 3
        is_not_in_question = answer.lower() not in self.question_input.text().lower() if len(answer) > 0 else True

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
                self.nextButton.clicked.disconnect()
                self.nextButton.clicked.connect(lambda: print("Not Okayyy"))
                return

        self.nextButton.setCursor(Qt.PointingHandCursor)
        self.nextButton.clicked.disconnect()
        self.nextButton.clicked.connect(lambda: print("Okayyy"))

    
if __name__ == '__main__':
    app = QApplication([])

    window = LoginForm()
    window.show()

    app.exec()