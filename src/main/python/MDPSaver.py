from PySide6.QtCore import QUrl, QFileSystemWatcher, QFile
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget
from PySide6.QtWebChannel import QWebChannel
import os
from bridge import Bridge
from jinja2 import Template
from controller import Recover


class MDPSaver(QMainWindow):
    def __init__(self, debug=False):
        super().__init__()

        self.bridge = Bridge() # Custom bridge class (controller)
        self.debug = debug

        # Launch UI
        self.__load_pages_path__()
        self.__init_ui__()
        self.__load_ui__()
        self.__setup_connections__()
        if debug:
            self.__init_debug__()

    def __load_pages_path__(self):
        # Get the path to the current script and construct the HTML file path
        current_dir = os.path.dirname(os.path.abspath(__file__))

        self.startup_path = os.path.join(current_dir, "../views/startup.html")
        self.login_path = os.path.join(current_dir, "../views/login.html")
        self.recovery_path = os.path.join(current_dir, "../views/recovery.html")
        self.app_path = os.path.join(current_dir, "../views/app.html")


    def __init_ui__(self):
        # Initialize UI with the WebView, Channel, ...
        self.setWindowTitle("MDPSaver")

        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)

        # Create a web channel and bridge between Python and JavaScript
        channel = QWebChannel(self.web_view.page())
        self.web_view.page().setWebChannel(channel)

        channel.registerObject("bridge", self.bridge)

    def __load_ui__(self):
        # Choose initial page to load
        if self.bridge.getNumberOfUser() == 0:
            self.__load_startup__()
        else:
            self.__load_login__()

    def __setup_connections__(self):
        # Startup Signals
        self.bridge.successful_startup.connect(self.__load_app__)

        # Login Signals
        self.bridge.successful_login.connect(self.__load_app__)
        self.bridge.failed_login.connect(lambda: self.__load_login__(from_failed=True))
        self.bridge.recovery_login.connect(self.__load_recovery__)
        self.bridge.create_account_login.connect(self.__load_startup__)

        # Recovery Signals
        self.bridge.successful_recovery.connect(self.__load_app__)
        self.bridge.failed_recovery.connect(self.__load_login__)
        self.bridge.cancel_recovery.connect(self.__load_login__)

    def __init_debug__(self):
        def reloadPage():
            # Reload the web view when the HTML file changes
            self.web_view.reload()

        self.file_watcher = QFileSystemWatcher([self.startup_path, self.login_path, self.recovery_path, self.app_path], self)
        self.file_watcher.fileChanged.connect(reloadPage)

    def __load_startup__(self):
        # TODO: load page using Jinja2
        # TODO: if app has usernames, button for login
        self.web_view.load(QUrl.fromLocalFile(self.startup_path))

    def __load_login__(self, from_failed= False):
        # TODO: load page using Jinja2

        template = Template(open(self.login_path).read())

        self.web_view.setHtml(template.render(usernames=self.bridge.get_usernames(), from_failed=from_failed))


    def __load_recovery__(self, from_failed= False):
        # TODO: load page using Jinja2

        question = self.bridge.get_personnal_question() # XXX: Using templating or asking from JS?

        template = Template(open(self.recovery_path).read())

        self.web_view.setHtml(template.render(usernames=self.bridge.get_usernames(), selected_username=self.bridge.username))

    def __load_app__(self):
        # TODO: load page using Jinja2
        self.web_view.load(QUrl.fromLocalFile(self.app_path))

    def closeEvent(self, event):
        # Stop monitoring the file for changes when the window is closed
        if self.debug:
            self.file_watcher.removePaths(self.file_watcher.files())
        event.accept()

