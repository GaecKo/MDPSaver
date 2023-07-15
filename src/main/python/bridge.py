from PySide6.QtCore import QObject, Slot, QUrl, Signal

from controller import Controller


class Bridge(QObject, Controller):
    # Login Signals
    successful_login = Signal()
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

    # Startup Methods
    @Slot()
    def submitAccount(self, username, password, question, answer):
        self.createAccount(username, password, question, answer)

    @Slot(str)
    def successful_startup_emit(self):
        self.successful_startup.emit()
        print(f"Startup Success")