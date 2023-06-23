from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QWidget, QMainWindow, QStackedWidget, QFrame, QGroupBox
from PySide6.QtCore import Signal, Qt 
from controller import Controller, Recover

# TODO: works on comments

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


        self.explaination_text = "<span style='font-size:15; font-style: italic;'>In order to recover your Access Password, please answer the question you created:</span>"
        self.explaination = QLabel(text=self.explaination_text)
        self.explaination.setAlignment(Qt.AlignCenter)
        self.explaination.setWordWrap(True)
        self.explaination.setFixedWidth(320)

        # QUESTION - ANSWER GROUP
        self.question_group = QGroupBox()
        self.question_group.setContentsMargins(0, 0, 0, 0) 
        self.question_group.setObjectName("question-group")

        # Question
        self.question_text = parent.get_question()

        self.question = QLabel(self.question_text)
        self.question.setObjectName("question")

        # Answer
        self.answer = QLineEdit()


        # Adding Widgets to layout

        self.GenVBox.addWidget(self.title, alignment=Qt.AlignCenter)
        self.GenVBox.addWidget(line)
        self.GenVBox.addWidget(self.explaination, alignment=Qt.AlignCenter)
        self.GenVBox.addWidget(self.question_group, alignment=Qt.AlignCenter)

        self.setLayout(self.GenVBox)


        
class SetNewInformations(QWidget):
    def __init__(self, parent, recover: Recover) -> None:
        super().__init__(parent)

        self.parent = parent
        self.setFixedSize(400, 400)
        self.setObjectName("newinfo")
        self.setStyleSheet(open("MDPStyle/recovery.css", "r").read())
       



class Recovery(QMainWindow):
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
        self.QStackedWidget = QStackedWidget()
        self.QStackedWidget.addWidget(self.checkAnswer)
        self.QStackedWidget.addWidget(self.setNewInformations)
        self.QStackedWidget.setCurrentIndex(0)

        self.setCentralWidget(self.QStackedWidget)


    
    def get_question(self):
        return self.recover.get_personnal_question()



if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    from controller import Controller
    import sys

    app = QApplication(sys.argv)

    controller = Controller()

    recovery = Recovery(controller)

    recovery.show()

    sys.exit(app.exec())
        