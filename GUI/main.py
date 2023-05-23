import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from login import LoginWindow
from pages import MainWindow
from recovery import RecoveryPage
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
        login_page = LoginWindow(controller)
        recovery_page = RecoveryPage(controller)

        login_page.successful_login.connect(main_window.show)
        login_page.recovery_login.connect(recovery_page.show)

        recovery_page.successful_recovery.connect(main_window.show)
        recovery_page.failed_recovery.connect(sys.exit)

        login_page.show()
    
    


    sys.exit(app.exec())
