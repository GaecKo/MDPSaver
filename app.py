from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QGroupBox, QLabel, QWidget, QLineEdit
from controller import Controller, Recover


class MainWindow(QMainWindow):
    def __init__(self, controller: Controller, parent=None):
        self.controller = controller 
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("MDPSaver")
        self.setFixedSize(800, 600)

    def activate(self):
        self.create()
        self.show()
        
    def create(self):
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

        passwords = self.controller.get_all_passwords()
        if passwords != None:
            for index, data in enumerate(passwords):
                group = QGroupBox()
                genHBox = QHBoxLayout()

                site = QLineEdit(data[0])
                username = QLineEdit(data[1])
                password = QLineEdit(data[2])

                genHBox.addWidget(site)
                genHBox.addWidget(username)
                genHBox.addWidget(password)

                group.setLayout(genHBox)
                layout.addWidget(group)


        passwords_page.setLayout(layout)
        return passwords_page

    def create_passwords_page(self):
        create_page = QGroupBox("Create Page")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("This is the Creation page."))

        self.site_input = QLineEdit()
        self.site_input.setPlaceholderText("Site")

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")

        button = QPushButton(text="Add")
        button.clicked.connect(self.add_password)

        layout.addWidget(self.site_input)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(button)

        create_page.setLayout(layout)
        return create_page

    def add_password(self):
        self.controller.add_password(self.site_input.text(), self.username_input.text(), self.password_input.text())

        self.site_input.setText("")
        self.username_input.setText("")
        self.password_input.setText("")
        
        # TODO: actualisation system
        

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
