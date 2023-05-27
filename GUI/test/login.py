import sys
import PySide6
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPalette, QColor, QFont, QPixmap, QCursor, QTransform
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QGraphicsView, QGraphicsScene, QSizePolicy

class LoginPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Page")
        self.setStyleSheet(open("styles.css").read())
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Set fixed size for the login page
        central_widget.setFixedWidth(700)
        central_widget.setFixedHeight(275)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 0, 10, 0)
        main_layout.setAlignment(Qt.AlignCenter)

        # Left Part: Image
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)


        # Create a QGraphicsView instance
        graphics_logo = QGraphicsView()

        
        # Create a QGraphicsScene instance
        logo_scene = QGraphicsScene()
        graphics_logo.setScene(logo_scene)

        # Load an image
        logo_path = "MDPSaver.png"
        pixmap = QPixmap(logo_path)

        # Create a QGraphicsPixmapItem and add it to the scene
        logo_scene.addPixmap(pixmap)

        # Use a transform to scale down the view
        transform_logo = QTransform()
        transform_logo.scale(0.45, 0.45)  # This will make the view half the original size
        graphics_logo.setTransform(transform_logo)
        graphics_logo.show()

        # Create a layout to hold the QGraphicsView
        left_layout.addWidget(graphics_logo)

        # Right Part: Login Form
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(3, 0, 5, 0)
        
        

        title_label = QLabel("Login", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("title")
        right_layout.addWidget(title_label)

        user_layout = QHBoxLayout()

        user_layout.setAlignment(Qt.AlignCenter)

        graphics_user = QGraphicsView()
        graphics_user.scale(0.1, 0.1)
        graphics_user.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        user_scene = QGraphicsScene()
        graphics_user.setScene(user_scene)

        user_path = "user.png"
        pixmap = QPixmap(user_path)


        user_scene.addPixmap(pixmap)

        transform_user = QTransform()
        transform_user.scale(0.1, 0.1)
        graphics_user.setTransform(transform_user)
        graphics_user.show()

        user_layout.addWidget(graphics_user)

        # user_layout.addWidget()
        

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

        # XXX make it so there is no space between button and this label
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
        main_layout.addLayout(left_layout, 3)
        main_layout.addWidget(line)
        main_layout.addLayout(right_layout, 2)


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