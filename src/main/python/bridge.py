from PySide6.QtCore import QObject, Slot, QUrl, Signal

from controller import Controller


class Bridge(QObject, Controller):
    # Login Signals
    successful_login = Signal()
    failed_login = Signal()
    create_account_login = Signal()
    recovery_login = Signal()

    # Startup Signals
    successful_startup = Signal()
    failed_startup = Signal()

    # Recovery Signals
    successful_recovery = Signal()
    failed_recovery = Signal()
    cancel_recovery = Signal()

    def __init__(self):
        Controller.__init__(self)  # initialize controller class, all its methods are now accessible
        QObject.__init__(self)

    # @Slot(str)
    # def buttonClicked(self, button_id):
    #     print(f"Button {button_id} clicked!")

    # Login Methods
    @Slot(str, str)
    def submitLogin(self, username, password):
        if self.check_login(username, password):
            print(f"Login Success")
            self.load_app(username, password)
            self.successful_login.emit()
        else:
            print(f"Login Failed")
            self.failed_login.emit()

    @Slot()
    def callStartup(self):
        print("Startup Called")
        self.create_account_login.emit()

    @Slot(str)
    def callRecovery(self, username):
        # TODO: auto select username for recovery
        print("Recovery Called")
        self.username = username  # articifically set username for recovery
        self.recovery_login.emit()

    # Startup Methods
    @Slot(str, str, str, str)
    def submitAccount(self, username, password, question, answer):

        if self.initiate_db_settings(username, password, question, answer):
            print(f"Startup Success")
            self.successful_startup.emit()
        else:
            self.failed_startup.emit()
