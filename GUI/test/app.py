from PySide6.QtCore import QObject, Slot, QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtWebChannel import QWebChannel
import os

class Bridge(QObject):
    @Slot(result=str)
    def hello(self):
        return "Hello from Python!"

    @Slot(str)
    def buttonClicked(self, button_id):
        print(f"Button {button_id} clicked!")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HTML/CSS App")
        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)

        
        # Create a web channel and bridge between Python and JavaScript
        channel = QWebChannel(self.web_view.page())
        self.web_view.page().setWebChannel(channel)
        self.bridge = Bridge()  # Custom bridge class (see step 3)
        channel.registerObject("bridge", self.bridge)

        # Get the path to the current script and construct the HTML file path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_file_path = os.path.join(current_dir, "app.html")

        self.web_view.load(QUrl.fromLocalFile(html_file_path))

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()