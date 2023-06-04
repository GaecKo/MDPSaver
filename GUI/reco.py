from typing import Optional
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QWidget, QMainWindow, QStackedWidget
from PySide6.QtCore import Signal
from controller import Controller, Recover

class CheckAnswer(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.parent = parent
        self.setFixedSize(400, 400)

class SetNewInformations(QWidget):
    def __init__(self, parent, recover: Recover) -> None:
        super().__init__(parent)

        self.parent = parent
        self.setFixedSize(400, 400)

class Recovery(QMainWindow):
    def __init__(self, controller: Controller):
        super().__init__()


        self.controller = controller
        self.setFixedSize(400, 400)
        self.recover = Recover(self.controller)

        # Sub pages that will be shown
        self.checkAnswer = CheckAnswer(self)
        self.setNewInformations = SetNewInformations(self)

        # Set the stacked widget and its content
        self.QStackedWidget = QStackedWidget()
        self.QStackedWidget.addWidget(self.checkAnswer)
        self.QStackedWidget.addWidget(self.setNewInformations)
        self.QStackedWidget.setCurrentIndex(0)



        