import sys
from ppg_runtime.application_context.PySide6 import ApplicationContext, PPGLifeCycle
from PySide6.QtWidgets import QMainWindow, QLabel

import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from pages.login import LoginPage
from pages.startup import StartupPage
from pages.app import AppPage
from pages.recovery import RecoveryPage

from bridge import Bridge

# TODO: set text selection (when text is selected): "selection-background-color: #2fa572;".
# TODO: time out of the app, in case of no user activity.
# TODO: free widgets unused in whole app.
# TODO: log system

if __name__ == "__main__":
    app = QApplication(sys.argv)

    bridge = Bridge()


    main_window = AppPage(bridge)

    if bridge.getNumberOfUser() == 0:
        startup_page = StartupPage(bridge)

        bridge.successful_startup.connect(main_window.show)
        bridge.failed_startup.connect(sys.exit)

        startup_page.show()

    else:
        login_page = LoginPage(bridge)
        recovery_page = RecoveryPage(bridge)

        # Login Signals
        bridge.successful_login.connect(main_window.show)
        bridge.recovery_login.connect(recovery_page.show)

        # Recovery Signals
        bridge.successful_recovery.connect(main_window.show)
        bridge.cancel_recovery.connect(login_page.show)
        bridge.failed_recovery.connect(sys.exit)

        login_page.show()

    sys.exit(app.exec())
