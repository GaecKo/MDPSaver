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
from controller import Recover


class MDPSaver(QMainWindow):
    def __init__(self, debug=False):
        super().__init__()

        self.bridge = Bridge()  # Custom bridge class (controller)
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
            self.add_password_path = os.path.join(current_dir, "../views/add_password.html")

        # jinja templates
        self.startup_jinja = os.path.join(current_dir, "../views/startup.jinja2")
        self.login_jinja = os.path.join(current_dir, "../views/login.jinja2")
        self.recovery_jinja = os.path.join(current_dir, "../views/recovery.jinja2")
        self.app_jinja = os.path.join(current_dir, "../views/app.jinja2")
        self.add_password_path_jinja = os.path.join(current_dir, "../views/add_password.jinja2")

    def __init_ui__(self):
        # Initialize UI with the WebView, Channel, ...
        self.setWindowTitle("MDPSaver")

        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)

        # Create a web channel and bridge between Python and JavaScript
        channel = QWebChannel(self.web_view.page())
        self.web_view.page().setWebChannel(channel)

        channel.registerObject("bridge", self.bridge)

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
        self.bridge.add_password_view.connect(self.__add_password__)
        self.bridge.push_password.connect(self.__push_password__)

    def __init_debug__(self):
        # Watch for changes in the jinja files and update the html files

        self.startup_watcher = QFileSystemWatcher([self.startup_jinja], self)
        self.login_watcher = QFileSystemWatcher([self.login_jinja], self)
        self.recovery_watcher = QFileSystemWatcher([self.recovery_jinja], self)
        self.app_watcher = QFileSystemWatcher([self.app_jinja], self)
        self.add_password_watcher = QFileSystemWatcher([self.add_password_path_jinja], self)

        self.startup_watcher.fileChanged.connect(self.__load_startup__)
        self.login_watcher.fileChanged.connect(self.__load_login__)
        self.recovery_watcher.fileChanged.connect(self.__load_recovery__)
        self.app_watcher.fileChanged.connect(self.__load_app__)
        self.add_password_watcher.fileChanged.connect(self.__add_password__)

        
        # Create debug html files:
        open(self.startup_path, "w").write("")
        open(self.login_path, "w").write("")
        open(self.recovery_path, "w").write("")
        open(self.app_path, "w").write("")

    def __write_jinja__(self, html_path, html):
        with open(html_path, "w") as f:
            f.write(html)

    def __remove_debug__(self):
        # delete html files
        os.remove(self.app_path)
        os.remove(self.login_path)
        os.remove(self.recovery_path)
        os.remove(self.startup_path)

    def __load_startup__(self):
        # TODO: if app has usernames, button for login
        template = Template(open(self.startup_jinja).read())
        html = template.render(nbr_user=self.bridge.getNumberOfUser())

        if self.debug:
            self.__write_jinja__(self.startup_path, html)

            self.web_view.load(QUrl.fromLocalFile(self.startup_path))
        else:
            self.web_view.setHtml(html)

    def __load_login__(self):

        template = Template(open(self.login_jinja).read())
        html = template.render(usernames=self.bridge.get_usernames())

        if self.debug:
            self.__write_jinja__(self.login_path, html)
            self.web_view.load(QUrl.fromLocalFile(self.login_path))
        else:
            self.web_view.setHtml(html)

    def __load_recovery__(self):

        template = Template(open(self.recovery_jinja).read())
        html = template.render(usernames=self.bridge.get_usernames(), selected_username=self.bridge.username)
        if self.debug:
            self.__write_jinja__(self.recovery_path, html)
            self.web_view.load(QUrl.fromLocalFile(self.recovery_path))
        else:
            self.web_view.setHtml(html)

    def __load_app__(self):

        template = Template(open(self.app_jinja).read())
        # get all user passwords in the database
        username=self.bridge.username
        passwords = self.bridge.get_all_passwords(username=username)
        print(username, passwords)
        html =  template.render(username=self.bridge.username, passwords=passwords) # to complete further on
        if self.debug:
            self.__write_jinja__(self.app_path, html)
            self.web_view.load(QUrl.fromLocalFile(self.app_path))
        else:
            self.web_view.setHtml(html)

    def __add_password__(self):
        template = Template(open(self.add_password_path_jinja).read())
        html = template.render(username=self.bridge.username)
        if self.debug:
            self.__write_jinja__(self.add_password_path, html)
            self.web_view.load(QUrl.fromLocalFile(self.add_password_path))
        else:
            self.web_view.setHtml(html)

    def get_favicon_url(self, target):
        favicon = None
        if target.startswith("http://") or target.startswith("https://"):
            try:
                soup = BeautifulSoup(requests.get(target, timeout=3).text, 'html.parser')
                favicon_tag = soup.find('link', rel='icon')
                favicon = favicon_tag['href'] if favicon_tag and 'href' in favicon_tag.attrs else None
            except:
                return None
        return favicon

    def generate_unique_filename(self):
        filename = str(uuid.uuid4()) + str(uuid.uuid4()) + str(uuid.uuid4())
        return filename[:random.randint(6, len(filename))]

    def save_favicon_locally(self, favicon_url):
        if favicon_url:
            try:
                favicon = requests.get(favicon_url).content
                filename = self.generate_unique_filename()

                

                with open(os.path.join(os.environ['APPDATA'], "MDPSaver", f"{filename}.ico"), "wb") as f:
                    f.write(favicon)

                return filename
            except:
                pass
        return None

    def get_image_or_icon_file_path():
        file_name, _ = QFileDialog.getOpenFileName(None, "Select Image or Icon", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif);;Icon Files (*.ico);;Executable Files (*.exe)")
        return file_name
    
    def extract_icon_from_executable(executable_path):
        icon = QAbstractFileIconProvider().icon(QFileInfo(executable_path))
        return icon.pixmap(32, 32).toImage()

    def __push_password__(self, target, username, password, icon):
        if not os.path.exists(os.path.join(os.environ['APPDATA'], "MDPSaver")):
                    os.makedirs(os.path.join(os.environ['APPDATA'], "MDPSaver"), exist_ok=True)
        favicon = self.get_favicon_url(target)
        if icon == "on":
            if favicon is None:
                # show filebrowser dialog
                file_name, _ = QFileDialog.getOpenFileName(self, "Select Icon - Just quit to not use one.", "", "Icon Files (*.ico);;Image Files (*.png *.svg);;Executable Files (*.exe *.dll);;All Files (*)")
                if file_name:
                    if file_name.endswith(".exe") or file_name.endswith(".dll"):
                        # extract icon from executable
                        try :
                            favicon = self.generate_unique_filename()
                            icon = self.extract_icon_from_executable(file_name)
                            open(os.path.join(os.environ['APPDATA'], "MDPSaver", f"{favicon}.ico"), "wb").write(icon)
                        except:
                            favicon = None
                    
                    else:
                        # copy file to appdata
                        favicon = self.generate_unique_filename()
                        open(os.path.join(os.environ['APPDATA'], "MDPSaver", f"{favicon}.ico"), "wb").write(open(file_name, "rb").read())
                    

        self.bridge.add_password(target, username, password, favicon)



    def closeEvent(self, event):
        # Stop monitoring the file for changes when the window is closed
        if self.debug:
            self.startup_watcher.removePaths(self.startup_watcher.files())
            self.login_watcher.removePaths(self.login_watcher.files())
            self.recovery_watcher.removePaths(self.recovery_watcher.files())
            self.app_watcher.removePaths(self.app_watcher.files())

            self.__remove_debug__()

        event.accept()
