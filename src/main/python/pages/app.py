from PySide6.QtCore import QObject, Slot, QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget
from PySide6.QtWebChannel import QWebChannel
import os


class AppPage(QMainWindow):
    def __init__(self, bridge):
        super().__init__()

        self.bridge = bridge # Custom bridge class (controller)
        self.web_view = None
        self.bridge = None

        self.buildPage()

    def buildPage(self):
        self.setWindowTitle("MDPSaver")
        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)

        # Create a web channel and bridge between Python and JavaScript
        channel = QWebChannel(self.web_view.page())
        self.web_view.page().setWebChannel(channel)

        channel.registerObject("bridge", self.bridge)

        # Get the path to the current script and construct the HTML file path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_file_path = os.path.join(current_dir, "../../views/app.html")

        self.web_view.load(QUrl.fromLocalFile(html_file_path))

