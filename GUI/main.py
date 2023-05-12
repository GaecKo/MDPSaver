import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from login import LoginPage
from pages import MainWindow
from startup import AccountCreationWindow
from MDPDatabase.controller import Controller 


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(open("styles.css").read())

    controller = Controller()

    if controller.is_first_startup():
        startup_page = AccountCreationWindow()

    login_page = LoginPage(controller)
    main_window = MainWindow(controller)

    login_page.successful_login.connect(main_window.show)
    login_page.show()

    sys.exit(app.exec())
