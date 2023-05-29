from PySide6.QtCore import QPropertyAnimation, QRect, QSize, Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QStackedWidget

class Form1(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout()
        nextButton = QPushButton("Next")
        nextButton.clicked.connect(parent.showNextForm)
        layout.addWidget(nextButton)
        self.setLayout(layout)



class Form2(QWidget):
    def __init__(self, parent):
        super().__init__()
        layout = QVBoxLayout()
        next = QPushButton("next")
        next.clicked.connect(parent.showNextForm)

        prev = QPushButton("prev")
        prev.clicked.connect(parent.showPreviousForm)

        
        layout.addWidget(next)
        layout.addWidget(prev)
        # Add form widgets and layout here
        self.setLayout(layout)


class Form3(QWidget):
    def __init__(self, parent):
        super().__init__()
        layout = QVBoxLayout()
        # Add form widgets and layout here
        self.setLayout(layout)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.stackedWidget = QStackedWidget(self)
        self.stackedWidget.addWidget(Form1(self))
        self.stackedWidget.addWidget(Form2(self))
        self.stackedWidget.addWidget(Form3(self))

        layout = QVBoxLayout()
        layout.addWidget(self.stackedWidget)
        self.setLayout(layout)

        self.currentFormIndex = 0

    def showNextForm(self):
        nextIndex = (self.currentFormIndex + 1) % self.stackedWidget.count()
        self.animateTransition(nextIndex, reverse=False)

    def showPreviousForm(self):
        previousIndex = (self.currentFormIndex - 1) % self.stackedWidget.count()
        self.animateTransition(previousIndex, reverse=True)

    def animateTransition(self, nextIndex, reverse=False):
        currentForm = self.stackedWidget.currentWidget()
        nextForm = self.stackedWidget.widget(nextIndex)

        startRect = self.stackedWidget.geometry()
        endRect = QRect(-self.width(), 0, self.width(), self.height())

        if reverse:
            startRect = QRect(self.width(), 0, self.width(), self.height())
            endRect = self.stackedWidget.geometry()

        self.animation = QPropertyAnimation(self.stackedWidget, b"geometry")
        self.animation.setDuration(500)
        self.animation.setStartValue(startRect)
        self.animation.setEndValue(endRect)
        self.animation.start()

        self.stackedWidget.setCurrentIndex(nextIndex)
        self.currentFormIndex = nextIndex

        startRect = QRect(self.width(), 0, self.width(), self.height())
        endRect = self.stackedWidget.geometry()

        if reverse:
            startRect = self.stackedWidget.geometry()
            endRect = QRect(-self.width(), 0, self.width(), self.height())

        self.animation = QPropertyAnimation(self.stackedWidget, b"geometry")
        self.animation.setDuration(500)
        self.animation.setStartValue(startRect)
        self.animation.setEndValue(endRect)
        self.animation.start()


if __name__ == "__main__":
    app = QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec()

