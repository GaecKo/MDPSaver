import PySide6
from PySide6.QtCore import QUrl, QFileSystemWatcher, QFile, QFileInfo
from PySide6.QtGui import QAbstractFileIconProvider
from PySide6.QtCore import QUrl, QFileSystemWatcher, QFile, QFileInfo
from PySide6.QtGui import QAbstractFileIconProvider
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QFileDialog
from PySide6.QtWebChannel import QWebChannel
import os
import random, uuid
import requests
from bs4 import BeautifulSoup
from bridge import Bridge
from jinja2 import Template


class MDPSaver(QMainWindow):
    def __init__(self, debug=False):
        super().__init__()

        self.bridge = Bridge(self)  # Custom bridge class (controller)
        self.debug = debug

        # Prepare UI
        self.__load_pages_path__()
        self.__init_ui__()
        self.__setup_connections__()

        if debug:
            self.__init_debug__()

        # Launch UI
        self.__launch_ui__()

    def __load_pages_path__(self):
        # Get the path to the current script and construct the HTML file path
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # raw HTML files, used to store jinja templated HTML for debug
        if self.debug:
            self.startup_path = os.path.join(current_dir, "../views/startup.html")
            self.login_path = os.path.join(current_dir, "../views/login.html")
            self.recovery_path = os.path.join(current_dir, "../views/recovery.html")
            self.app_path = os.path.join(current_dir, "../views/app.html")

            self.startup_css = os.path.join(current_dir, "../static/startup.css")
            self.login_css = os.path.join(current_dir, "../static/login.css")
            self.app_css = os.path.join(current_dir, "../static/app.css")
            self.recovery_css = os.path.join(current_dir, "../static/recovery.css")

            self.circle_js = os.path.join(current_dir, "../static/circle_simple.js")
            self.cirle1_js = os.path.join(current_dir, "../static/circle_1.js")
            self.cirle2_js = os.path.join(current_dir, "../static/circle_2.js")
            self.cirle3_js = os.path.join(current_dir, "../static/circle_3.js")

        # jinja templates
        self.startup_jinja = os.path.join(current_dir, "../views/startup.jinja2")
        self.login_jinja = os.path.join(current_dir, "../views/login.jinja2")
        self.recovery_jinja = os.path.join(current_dir, "../views/recovery.jinja2")
        self.app_jinja = os.path.join(current_dir, "../views/app.jinja2")

    def __init_ui__(self):
        # Initialize UI with the WebView, Channel, ...
        self.setWindowTitle("MDPSaver")
        self.setContentsMargins(0, 0, 0, 0)

        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)

        # Create a web channel and bridge between Python and JavaScript
        channel = QWebChannel(self.web_view.page())
        self.web_view.page().setWebChannel(channel)

        channel.registerObject("bridge", self.bridge)

    def resizeEvent(self, event:PySide6.QtGui.QResizeEvent) -> None:
        print(self.size())
        super().resizeEvent(event)

    def __launch_ui__(self):
        # Choose initial page to load
        if self.bridge.getNumberOfUser() == 0:
            self.__load_startup__()
        else:
            self.__load_login__()

    def __setup_connections__(self):
        # Startup Signals
        self.bridge.successful_startup.connect(self.__load_app__)
        self.bridge.back_login_startup.connect(self.__load_login__)

        # Login Signals
        self.bridge.successful_login.connect(self.__load_app__)
        self.bridge.failed_login.connect(self.__load_login__)
        self.bridge.recovery_login.connect(self.__load_recovery__)
        self.bridge.create_account_login.connect(self.__load_startup__)

        # Recovery Signals
        self.bridge.successful_recovery.connect(self.__load_app__)
        self.bridge.failed_recovery.connect(self.__load_login__)
        self.bridge.cancel_recovery.connect(self.__load_login__)

        # App Signals
        self.bridge.refresh_menu.connect(self.__load_app__)

    def __init_debug__(self):
        # Watch for changes in the jinja files and update the html files

        self.startup_watcher = QFileSystemWatcher([self.startup_jinja, self.startup_css], self)
        self.login_watcher = QFileSystemWatcher([self.login_jinja, self.login_css], self)
        self.recovery_watcher = QFileSystemWatcher([self.recovery_jinja, self.recovery_css], self)
        self.app_watcher = QFileSystemWatcher([self.app_jinja, self.app_css, self.circle_js, self.cirle1_js, self.cirle2_js, self.cirle3_js], self)

        self.startup_watcher.fileChanged.connect(self.__load_startup__)
        self.login_watcher.fileChanged.connect(self.__load_login__)
        self.recovery_watcher.fileChanged.connect(self.__load_recovery__)
        self.app_watcher.fileChanged.connect(self.__load_app__)

        # Create debug html files:
        open(self.startup_path, "w").write("")
        open(self.login_path, "w").write("")
        open(self.recovery_path, "w").write("")
        open(self.app_path, "w").write("")

    def __write_jinja__(self, html_path, html):
        with open(html_path, "w") as f:
            f.write(html)

    def __remove_debug_file__(self):
        print("Removing debug files")
        # delete html files
        os.remove(self.app_path)
        os.remove(self.login_path)
        os.remove(self.recovery_path)
        os.remove(self.startup_path)

    def __load_startup__(self):
        template = Template(open(self.startup_jinja).read())
        html = template.render(nbr_user=self.bridge.getNumberOfUser())

        if self.debug:
            self.__write_jinja__(self.startup_path, html)
            self.setFixedSize(350, 450)
            self.web_view.load(QUrl.fromLocalFile(self.startup_path))
        else:
            self.setFixedSize(350, 450)
            self.web_view.setHtml(html)



    def __load_login__(self):

        template = Template(open(self.login_jinja).read())
        html = template.render(usernames=self.bridge.get_usernames())

        if self.debug:
            self.__write_jinja__(self.login_path, html)
            self.setFixedSize(350, 450)
            self.web_view.load(QUrl.fromLocalFile(self.login_path))
        else:
            self.setFixedSize(350, 450)
            self.web_view.setHtml(html)



    def __load_recovery__(self):

        template = Template(open(self.recovery_jinja).read())
        html = template.render(usernames=self.bridge.get_usernames(), selected_username=self.bridge.username)
        if self.debug:
            self.__write_jinja__(self.recovery_path, html)
            self.setFixedSize(350, 450)
            self.web_view.load(QUrl.fromLocalFile(self.recovery_path))
        else:
            self.setFixedSize(350, 450)
            self.web_view.setHtml(html)


    def __load_app__(self):

        template = Template(open(self.app_jinja).read())
        # get all user passwords in the database
        passwords = self.bridge.get_all_passwords()
        # append the full path to passwords
        for p in passwords:
            p["icon"] = self.bridge.icon_path / p["icon"] if p["icon"] != "None" else self.bridge.icon_path.parent / "blank-profile-picture"

        html = template.render(username=self.bridge.username, passwords=passwords)  # to complete further on
        if self.debug:
            self.__write_jinja__(self.app_path, html)
            self.web_view.load(QUrl.fromLocalFile(self.app_path))
            self.setMinimumSize(930, 570)
        else:
            self.web_view.setHtml(html)
            self.setMinimumSize(930, 570)

    def closeEvent(self, event):
        # Stop monitoring the file for changes when the window is closed
        if self.debug:
            self.startup_watcher.removePaths(self.startup_watcher.files())
            self.login_watcher.removePaths(self.login_watcher.files())
            self.recovery_watcher.removePaths(self.recovery_watcher.files())
            self.app_watcher.removePaths(self.app_watcher.files())

            self.__remove_debug_file__()

        self.bridge.close_app()

        event.accept()
