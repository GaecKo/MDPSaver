import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from login import LoginPage
from pages import MainWindow
from startup import AccountCreationWindow
from controller import Controller 


if __name__ == "__main__":
    app = QApplication(sys.argv)

    controller = Controller()
    main_window = MainWindow(controller)

    if controller.is_first_startup():
        startup_page = AccountCreationWindow(controller)
        startup_page.successfull_startup.connect(main_window.show)

        startup_page.failed_startup.connect(sys.exit)
        startup_page.show()

    else:
        login_page = LoginPage(controller)
        login_page.successful_login.connect(main_window.show)
        login_page.show()
    
    controller.add_connection()


    sys.exit(app.exec())
