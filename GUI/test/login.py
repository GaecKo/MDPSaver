import sys
import PySide6
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPalette, QColor, QFont, QPixmap, QCursor
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFrame

class LoginPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Page")
        self.setStyleSheet(open("styles.css").read())
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Set fixed size for the login page
        central_widget.setFixedWidth(650)
        central_widget.setFixedHeight(250)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 0, 10, 0)
        main_layout.setAlignment(Qt.AlignCenter)

        # Left Part: Image
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)

        image_label = QLabel(self)
        image_label.setPixmap(QPixmap("MDPSaver.png").scaled(QSize(325, 325), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setObjectName("imageLabel")

        left_layout.addWidget(image_label)

        # Right Part: Login Form
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(3, 0, 5, 0)
        

        title_label = QLabel("Login", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("title")
        right_layout.addWidget(title_label)

        user_layout = QHBoxLayout()

        user_layout.setAlignment(Qt.AlignCenter)

        user_icon_label = QLabel(self)
        user_icon_label.setPixmap(QPixmap("user.png").scaled(QSize(40, 40), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        user_layout.addWidget(user_icon_label)
        user_layout.setSpacing(10)

        username_label = QLabel("GaecKo", self)
        username_label.setObjectName("usernameLabel")
        user_layout.addWidget(username_label)

        right_layout.addLayout(user_layout)
        right_layout.setAlignment(Qt.AlignRight)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Password")
        right_layout.addWidget(self.password_input)

        login_button = QPushButton("Login", self)
        login_button.setObjectName("loginButton")
        login_button.setCursor(QCursor(Qt.PointingHandCursor))
        right_layout.addWidget(login_button)

        forgot_password_label = QLabel("Forgot password?", self)
        forgot_password_label.setObjectName("forgotPasswordLabel")
        forgot_password_label.setCursor(QCursor(Qt.PointingHandCursor))
        right_layout.addWidget(forgot_password_label)

        # Vertical Line
        line = QFrame(self)
        line.setObjectName("line")
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setLineWidth(2)

        # Combine Left and Right Parts
        main_layout.addLayout(left_layout)
        main_layout.addWidget(line)
        main_layout.addLayout(right_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set a custom palette for the application
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#F5F5F5"))  # Background color
    palette.setColor(QPalette.Button, QColor("#428BCA"))  # Button color
    palette.setColor(QPalette.ButtonText, QColor("#FFFFFF"))  # Button text color
    app.setPalette(palette)

    # Set a custom font for the application
    font = QFont("Arial", 12)
    app.setFont(font)

    window = LoginPage()
    window.show()

    sys.exit(app.exec())