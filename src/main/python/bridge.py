from PySide6.QtCore import QObject, Slot, QUrl, Signal

from controller import Controller


class Bridge(Controller, QObject):
    # Login Signals
    successful_login = Signal()
    recovery_login = Signal()

    # Startup Signals
    information_retrieve = Signal()
    successful_startup = Signal()
    failed_startup = Signal()

    # Recovery Signals
    successful_recovery = Signal()
    failed_recovery = Signal()
    cancel_recovery = Signal()

    def __init__(self):
        super().__init__()




        # initialize controller class, all its methods are now accessible

    @Slot(result=str)
    def hello(self):
        return "Hello from Python!"

    @Slot(str)
    def buttonClicked(self, button_id):
        print(f"Button {button_id} clicked!")
