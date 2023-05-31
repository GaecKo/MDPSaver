from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QSizePolicy
from utils.SceneGenerator import SceneImage


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


        self.logo_scene = SceneImage("MDPSaver.png", 0.4, 0.4)
        self.logo_scene.setFixedSize(350, 130)


        self.presentation_text = QLabel()
        self.presentation_text.setAlignment(Qt.AlignCenter)
        self.presentation_text.setWordWrap(True)
        self.presentation_text.setText("""<span style="font-weight: bold;">MDPSaver</span> makes it easy to <span style="font-weight: bold;">store</span>, <span style="font-weight: bold;">access</span> & <span style="font-weight: bold;">generate passwords</span>. A single password gives you access to <span style="font-weight: bold;">all</span> your passwords, at <span style="font-weight: bold;">any</span> time.""")
        self.presentation_text.setFixedWidth(300)
        self.presentation_text.setObjectName("presentation-text")

        #self.GenHBox.addWidget(self.title, alignment=Qt.AlignCenter)
        #self.GenHBox.addWidget(line1)
        
        

        empty = " " * 16
    
        self.nextButton = QPushButton(text="Let's get started!" + empty, icon=QIcon("right-arrow.png"))
        self.nextButton.setLayoutDirection(Qt.RightToLeft)
        self.nextButton.setCursor(Qt.PointingHandCursor)
        self.nextButton.setFixedWidth(300)
        self.nextButton.setFixedHeight(50)
        # nextButton.clicked.connect(parent.showNextForm)

        self.GenHBox.addWidget(self.logo_scene, alignment=Qt.AlignCenter)
        self.GenHBox.addWidget(line)
        self.GenHBox.addWidget(self.presentation_text, alignment=Qt.AlignCenter)
        self.GenHBox.addWidget(self.nextButton, alignment=Qt.AlignCenter)
        self.setLayout(self.GenHBox)


if __name__ == '__main__':
    app = QApplication([])

    window = Welcome()
    window.show()

    app.exec()