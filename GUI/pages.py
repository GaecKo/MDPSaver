from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QGroupBox, QLabel, QWidget


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("MDPSaver")
        self.setFixedSize(800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout()
        central_widget.setLayout(layout)

        left_panel = QVBoxLayout()
        left_panel.setObjectName("leftPanel")
        right_panel = QVBoxLayout()
        right_panel.setObjectName("rightPanel")

        layout.addLayout(left_panel)
        layout.addLayout(right_panel)

        self.passwords_button = QPushButton("Passwords")
        self.create_button = QPushButton("Add")
        self.account_button = QPushButton("Account")
        self.settings_button = QPushButton("Settings")

        left_panel.addWidget(self.passwords_button)
        left_panel.addWidget(self.create_button)
        left_panel.addWidget(self.account_button)
        left_panel.addWidget(self.settings_button)

        self.stacked_widget = QStackedWidget()

        

        self.passwords_page = self.show_passwords_page()
        self.create_page = self.create_passwords_page()
        self.account_page = self.create_account_page()
        self.settings_page = self.create_settings_page()

        self.stacked_widget.addWidget(self.passwords_page)
        self.stacked_widget.addWidget(self.create_page)
        self.stacked_widget.addWidget(self.account_page)
        self.stacked_widget.addWidget(self.settings_page)

        right_panel.addWidget(self.stacked_widget)

        self.passwords_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.create_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        self.account_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.settings_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))




    def show_passwords_page(self):
        passwords_page = QGroupBox("Passwords Page")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("This is the Passwords page."))
        passwords_page.setLayout(layout)
        return passwords_page

    def create_passwords_page(self):
        create_page = QGroupBox("Create Page")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("This is the Creation page."))
        create_page.setLayout(layout)
        return create_page

    def create_account_page(self):
        account_page = QGroupBox("Account Page")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("This is the Account page."))
        account_page.setLayout(layout)
        return account_page

    def create_settings_page(self):
        settings_page = QGroupBox("Settings Page")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("This is the Settings page."))
        settings_page.setLayout(layout)
        return settings_page
