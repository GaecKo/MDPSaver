from PySide6.QtWidgets import QWidget, QApplication, QLabel, QToolTip
from PySide6.QtGui import QMouseEvent
import sys

class HelpWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setToolTip("Help Text")

    def enterEvent(self, event: QMouseEvent) -> None:
        QToolTip.showText(event.globalPos(), self.toolTip())

    def leaveEvent(self, event: QMouseEvent) -> None:
        QToolTip.hideText()

class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.help_widget = HelpWidget(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWidget()
    widget.show()
    sys.exit(app.exec())
    