import sys
from PySide6.QtWidgets import QMainWindow, QLabel

import sys, os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from MDPSaver import MDPSaver

os.environ["QT_DEBUG_PLUGINS"] = "1"

# TODO: investigate on which Python Qt framework to use (PySide6, PyQt6, PyQt5, PySide2, PyQt4).

# TODO: investigate on ppg_runtime

# TODO: set text selection (when text is selected): "selection-background-color: #2fa572;".
# TODO: time out of the app, in case of no user activity.
# TODO: free widgets unused in whole app.
# TODO: log system

if __name__ == "__main__":
    app = QApplication(sys.argv)

    MDPSaver = MDPSaver(debug=True)
    MDPSaver.show()

    sys.exit(app.exec())
