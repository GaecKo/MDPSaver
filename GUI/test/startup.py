from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from welcome import Welcome
from LoginForm import LoginForm
from RecoveryForm import RecoveryForm



class Startup(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setStyleSheet(open("startup.css").read())
        self.setObjectName("startup")
        self.setWindowTitle("MDPSaver Startup")

        self.welcome_page = Welcome(self)
        self.login_page = LoginForm(self)
        self.recovery_page = RecoveryForm(self)

        self.widgets = [self.welcome_page, self.login_page, self.recovery_page]

        self.QStackedWidget = QStackedWidget()
        self.cur_page = 0
        self.QStackedWidget.addWidget(self.welcome_page)
        self.QStackedWidget.addWidget(self.login_page)
        self.QStackedWidget.addWidget(self.recovery_page)

        self.QStackedWidget.setCurrentIndex(self.cur_page)

        self.setCentralWidget(self.QStackedWidget)
    

    def show_next_page(self):
        if self.cur_page == 2: return

        self.cur_page += 1
        self.QStackedWidget.setCurrentIndex(self.cur_page)

    def show_prev_page(self):
        if self.cur_page == 0: return

        self.cur_page -= 1
        self.QStackedWidget.setCurrentIndex(self.cur_page)
    
if __name__ == "__main__":
    app = QApplication()
    window = Startup()
    window.show()
    app.exec()
