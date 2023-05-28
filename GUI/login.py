import sys
from utils.PasswordPromp import PasswordPrompt
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QCursor, QTransform
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QGraphicsView, QGraphicsScene, QSizePolicy, QMessageBox
from controller import Controller

class LoginWindow(QMainWindow):
    successful_login = Signal()
    recovery_login = Signal()
    
    def __init__(self, controller: Controller, parent=None):

        self.controller = controller

        super().__init__()
        self.setWindowTitle("Login Page")
        
        self.setStyleSheet(open("MDPStyle/login.css").read())

        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Set fixed size for the login page
        central_widget.setFixedSize(700, 250)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 0, 10, 0)
        main_layout.setAlignment(Qt.AlignCenter)



        ## /////////// Left Part: Image ///////////

        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)

        # Create a QGraphicsView instance for the logo
        graphics_logo = QGraphicsView()

        # Create a QGraphicsScene instance for the logo
        logo_scene = QGraphicsScene()
        graphics_logo.setScene(logo_scene)

        # Load an image
        logo_path = "MDPStyle/MDPSaver.png"
        pixmap = QPixmap(logo_path)

        # Create a QGraphicsPixmapItem and add it to the scene
        logo_scene.addPixmap(pixmap)

        # Use a transform to scale down the view
        transform_logo = QTransform()
        transform_logo.scale(0.45, 0.45)  # This will make the view half the original size
        graphics_logo.setTransform(transform_logo)
        graphics_logo.show()

        # Create a layout to hold the QGraphicsView (Left Part)
        left_layout.addWidget(graphics_logo)



        ## /////////// Right Part: Login Form ///////////

        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(3, 0, 5, 0)

        # Title Label
        title_label = QLabel("Login", self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setObjectName("title")
        right_layout.addWidget(title_label)

        # User Layout: Scene (image) and Username
        user_layout = QHBoxLayout()
        user_layout.setAlignment(Qt.AlignCenter)

        # QGraphicsView contains the scene
        graphics_user = QGraphicsView()
        graphics_user.scale(0.1, 0.1)
        graphics_user.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # QGraphicsScene contains the image
        user_scene = QGraphicsScene()
        graphics_user.setScene(user_scene)

        # Load the user image
        user_path = "MDPStyle/user.png"
        pixmap = QPixmap(user_path)
        user_scene.addPixmap(pixmap)

        # Use a transform to scale down the view
        transform_user = QTransform()
        transform_user.scale(0.1, 0.1)
        graphics_user.setTransform(transform_user)
        graphics_user.show()

        user_layout.addWidget(graphics_user)

        # Username Label
        
        username_label = QLabel(self.controller.get_username(), self)
        username_label.setObjectName("usernameLabel")

        user_layout.addWidget(username_label)
        right_layout.addLayout(user_layout)


        # Password Input
        self.password_input = PasswordPrompt()
        self.password_input.setObjectName("passwordInput")
        self.password_input.setPlaceholderText("Password")
        self.password_input.returnPressed.connect(self.check_login)

        right_layout.addWidget(self.password_input)

        # Login Button
        login_button = QPushButton("Login", self)
        login_button.setObjectName("loginButton")
        login_button.setCursor(QCursor(Qt.PointingHandCursor))
        login_button.clicked.connect(self.check_login)

        right_layout.addWidget(login_button)

        # Forgot Password Label and Layout
        forgot_layout = QHBoxLayout()

        forgot_layout.setAlignment(Qt.AlignRight)

        forgot_password = QPushButton(text="Forgot password?")
        forgot_password.setObjectName("forgotPassword")
        forgot_password.clicked.connect(self.recovery)
        forgot_password.setCursor(QCursor(Qt.PointingHandCursor))

        forgot_layout.addWidget(forgot_password)

        right_layout.addLayout(forgot_layout)
        right_layout.addSpacing(20)
        
        ## === Vertical Line ===
        line = QFrame(self)
        line.setObjectName("line")
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setLineWidth(2)

        ## === Combine Parts ===
        main_layout.addLayout(left_layout, 3)
        main_layout.addWidget(line)
        main_layout.addLayout(right_layout, 2)

    def check_login(self):
        if self.controller.check_login(self.password_input.text()): 
            self.controller.load_app(self.password_input.text())
            self.successful_login.emit()
            self.close()
            
        else:
            QMessageBox.warning(self, "Error", "Invalid credentials.")
            self.password_input.setText("")

    def recovery(self):
        self.recovery_login.emit()
        self.close()

