import os
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QLineEdit, QPushButton, QHBoxLayout, QSizePolicy, QGroupBox, QLayout

# Get the current directory of the script
from_dir = os.path.dirname(os.path.abspath(__file__))

# Define file paths
style_path = os.path.join(from_dir, "PasswordPrompt.css")
eye_path = os.path.join(from_dir, "eye-regular.svg")
eye_slash_path = os.path.join(from_dir, "eye-slash-regular.svg")


class PasswordPrompt(QWidget):
    def __init__(self):
        super(PasswordPrompt, self).__init__()
        self.GenHBox = QHBoxLayout()

        self.GenHBox.setContentsMargins(0, 0, 0, 0)
        self.GenHBox.setSpacing(0)

        self.GenWidget = QGroupBox()
        self.GenWidget.setFixedHeight(34)
        self.GenWidget.setContentsMargins(0, 0, 0, 0)


        # Set the stylesheet for the widget
        self.setStyleSheet(open(style_path, "r").read())

        # Set up the layout
        self.hbox = QHBoxLayout()
        self.hbox.setContentsMargins(4, 4, 4, 4)
        self.hbox.setSpacing(0)
        
        # Create the password input field
        self.password_input = QLineEdit()

        self.password_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.returnPressed = self.password_input.returnPressed
        self.textChanged = self.password_input.textChanged

        # Create the eye icon button
        self.eye_icon = QIcon(eye_path)
        self.eye_button = QPushButton()
        self.eye_button.setIcon(self.eye_icon)
        self.eye_button.setIconSize(QSize(20, 20))
        self.eye_button.setFixedSize(QSize(24, 24))
        self.eye_button.setCheckable(True)
        self.eye_button.clicked.connect(self.toggle_eye)

        # Add the widgets to the layout
        self.hbox.addWidget(self.password_input)
        self.hbox.addWidget(self.eye_button)

        self.GenWidget.setLayout(self.hbox)
        self.GenHBox.addWidget(self.GenWidget)

        # Set the layout for the widget
        self.setLayout(self.GenHBox)
    
    def setText(self, text):
        self.password_input.setText(text)

    def toggle_eye(self):
        # Handle the eye button click event
        if self.eye_button.isChecked():
            self.eye_button.setIcon(QIcon(eye_slash_path))
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.eye_button.setIcon(QIcon(eye_path))
            self.password_input.setEchoMode(QLineEdit.Password)

        self.password_input.setFocus()

    def text(self):
        # Return the entered password
        return self.password_input.text()

    def setPlaceholderText(self, text):
        # Set the placeholder text for the password input field
        self.password_input.setPlaceholderText(text)
    
    def setInputStyleSheet(self, style):
        # Set the stylesheet for the password input field
        self.GenWidget.setStyleSheet("QGroupBox {" + style + "}")
    
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    widget = PasswordPrompt()
    widget.show()
    sys.exit(app.exec())
