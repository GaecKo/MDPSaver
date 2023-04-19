import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from login import LoginPage
from pages import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(open("styles.css").read())

    # login_page = LoginPage()
    main_window = MainWindow()

    # login_page.successful_login.connect(main_window.show)
    # login_page.show()
    main_window.show()

    sys.exit(app.exec())
