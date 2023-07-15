import sys
from ppg_runtime.application_context.PySide6 import ApplicationContext, PPGLifeCycle
from PySide6.QtWidgets import QMainWindow, QLabel

import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from MDPSaver import MDPSaver


# TODO: set text selection (when text is selected): "selection-background-color: #2fa572;".
# TODO: time out of the app, in case of no user activity.
# TODO: free widgets unused in whole app.
# TODO: log system

if __name__ == "__main__":
    app = QApplication(sys.argv)

    MDPSaver = MDPSaver(debug=True)
    MDPSaver.show()

    sys.exit(app.exec())
