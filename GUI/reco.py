from PySide6.QtWidgets import QDialog, QSizePolicy, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QWidget, QMainWindow, QStackedWidget, QFrame, QGroupBox, QHBoxLayout
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal, Qt 
from controller import Controller, Recover

# TODO: works on comments
# TODO: if back asked from new info inputs, ask for confirmation and go back to initial login
# XXX: self.parent seems to interfere with the parent() method of QWidget

class CheckAnswer(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.setObjectName("answering")
        self.setStyleSheet(open("MDPStyle/recovery.css", 'r').read())

        self.parent = parent
        self.setFixedSize(400, 400)
        self.setWindowTitle("Confirm Indentity")


        self.GenVBox = QVBoxLayout()
        self.GenVBox.setSpacing(5)

        self.title = QLabel("Recover Account")
        self.title.setObjectName("title")

        line = QFrame(self)
        line.setObjectName("line")
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setLineWidth(8)

        self.explaination_text = "<span style='font-size:15; font-style: italic;'>You are about to <span style='font-weight:bold;'> recover your account</span>. This operation implies an <span style='font-weight:bold;'>update</span> of your current <span style='font-weight:bold;'>Access Password</span> & <span style='font-weight:bold;'>Security Question</span>. To process, please <span style='font-weight:bold;'>answer</span> the question you created:</span>"
        self.explaination = QLabel(text=self.explaination_text)
        self.explaination.setAlignment(Qt.AlignCenter)
        self.explaination.setWordWrap(True)
        self.explaination.setFixedWidth(320)

        # QUESTION - ANSWER GROUP
        self.question_group = QGroupBox()
        self.question_group.setContentsMargins(0, 0, 0, 0) 
        self.question_group.setObjectName("question-group") 
        self.question_layout = QVBoxLayout()
        self.question_group.setContentsMargins(0, 0, 0, 0)
        self.question_group.setFixedWidth(360)

        # Question
        self.question_text = parent.get_question()

        self.question = QLabel(self.question_text)
        self.question.setWordWrap(True)
        self.question.setAlignment(Qt.AlignCenter)
        self.question.setObjectName("question")

        # Answer
        self.answer = QLineEdit()
        self.answer.setFixedWidth(340)
        self.answer.setFixedHeight(29)
        self.answer.setPlaceholderText("Answer")

        # Question Group Box composition
        self.question_layout.addWidget(self.question, alignment=Qt.AlignCenter)
        self.question_layout.addWidget(self.answer, alignment=Qt.AlignCenter)
        self.question_group.setLayout(self.question_layout)

        # Next button part
        self.button_layout = QHBoxLayout()

        self.nextButton = QPushButton(text="Next  ", icon=QIcon("MDPStyle/right-arrow.png"))
        # self.setStyleSheet("""QPushButton:hover {    background-color: #2fa572; border: none;}""")
        self.update()
        self.nextButton.setLayoutDirection(Qt.RightToLeft)
        self.nextButton.setCursor(Qt.PointingHandCursor)
        self.nextButton.setFixedHeight(50)
        self.nextButton.clicked.connect(self.verify_answer)

        self.prevButton = QPushButton(text="Back")
        self.prevButton.setCursor(Qt.PointingHandCursor)
        self.prevButton.setObjectName("backButton")
        self.prevButton.setFixedHeight(50)
        self.prevButton.clicked.connect(parent.show_prev_page)

        self.button_layout.addWidget(self.prevButton, 2)
        self.button_layout.addWidget(self.nextButton, 4)
        

        # Adding Widgets to main layout

        self.GenVBox.addWidget(self.title, alignment=Qt.AlignCenter)
        self.GenVBox.addWidget(line)
        self.GenVBox.addSpacing(30)
        self.GenVBox.addWidget(self.explaination, alignment=Qt.AlignCenter)
        self.GenVBox.addSpacing(30)
        self.GenVBox.addWidget(self.question_group, alignment=Qt.AlignCenter)
        self.GenVBox.addSpacing(20)
        self.GenVBox.addLayout(self.button_layout)

        self.setLayout(self.GenVBox)

    def verify_answer(self):
        if not self.parent.verify_answer(self.answer.text()):
            QMessageBox.warning(self, "Error", "Invalid credentials.")
        else:
            self.parent.show_next_page()



class SetNewInformations(QWidget):
    def __init__(self, parent, recover: Recover) -> None:
        super().__init__(parent)

        self.parent = parent
        self.setFixedSize(400, 400)
        self.setObjectName("newinfo")
        self.setStyleSheet(open("MDPStyle/recovery.css", "r").read())


class Recovery(QMainWindow):
    
    cancel_recovery = Signal()
    successful_recovery = Signal()
    information_retrieve = Signal()

    def __init__(self, controller: Controller):
        super().__init__()


        self.controller = controller
        self.recover = Recover(self.controller)

        self.setWindowTitle("MDPSaver Recovery")
        self.setFixedSize(400, 400)
        self.setObjectName("recovery")
        self.setStyleSheet(open("MDPStyle/recovery.css", "r").read())

        

        # Sub pages that will be shown
        self.checkAnswer = CheckAnswer(self)
        self.setNewInformations = SetNewInformations(self, self.recover)

        # Set the stacked widget and its content
        self.cur_page = 0;
        self.QStackedWidget = QStackedWidget()
        self.QStackedWidget.addWidget(self.checkAnswer)
        self.QStackedWidget.addWidget(self.setNewInformations)
        self.QStackedWidget.setCurrentIndex(self.cur_page)

        self.setCentralWidget(self.QStackedWidget)

    def verify_answer(self, given_answer: str):
        return self.recover.verify_answer(given_answer)

    def show_next_page(self):
        if self.cur_page == 1: return

        self.cur_page += 1
        self.QStackedWidget.setCurrentIndex(self.cur_page)

    def show_prev_page(self):
        if self.cur_page == 0: 
            self.cancel_recovery.emit()
            self.close()
            return

        self.cur_page -= 1
        self.QStackedWidget.setCurrentIndex(self.cur_page)
    
    def get_question(self):
        return self.recover.get_personnal_question()

    def get_hashed_answer(self):
        return self.controller.get_hashed_answer()

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    from controller import Controller
    import sys

    app = QApplication(sys.argv)

    controller = Controller()

    recovery = Recovery(controller)

    recovery.show()

    sys.exit(app.exec())
        