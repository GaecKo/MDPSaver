from MDPDatabase.MDPDatabase import MDPDatabase
from MDPDatabase.security import *
import os, time, random

from bs4 import BeautifulSoup
import random, uuid
import requests
from bs4 import BeautifulSoup

from PySide6.QtCore import QFileInfo
from PySide6.QtGui import QAbstractFileIconProvider
from PySide6.QtWidgets import QFileDialog

class Controller:
    """
    Controller is an interface for the database usage.
    """
    def __init__(self, parent=None):
        self.parent = parent
        self.db = MDPDatabase()
        self.key = None  # Will contain the key to decrypt data
        self.username = None # has to be set when logged in!

    def getNumberOfUser(self):
        return self.db.count("User")

    def setUserId(self, userId):
        self.userId = userId

    def get_all_passwords(self) -> list[dict]:
        if self.key == None:
            return None

        passwords = list(self.db.get_all_passwords(self.username))

        for index, data in enumerate(passwords):
            data = list(data)
            c_site, c_username, c_password = data[0], data[1], data[2]

            site, username, password = decrypt(self.key, c_site), decrypt(self.key, c_username), decrypt(self.key, c_password)
            # passwords[index] = [site, username, password]
            passwords[index] = {"target": site, "username": username, "password": password}

        return passwords

    def get_usernames(self):
        return list(self.db.get_usernames())

    def get_serial_number(self):
        return self.db.get_user_attribute("serial_number", self.username)

    def get_times_connected(self):
        return self.db.get_user_attribute("times_connected", self.username)

    def get_hashed_password(self):
        return self.db.get_user_security("hashed_password", self.username)

    def get_hashed_answer(self):
        return self.db.get_user_security("hashed_answer", self.username)

    def get_encrypted_password(self):
        return self.db.get_user_security("encrypted_password", self.username)

    def get_encrypted_question(self):
        return self.db.get_user_security("encrypted_question", self.username)

    def get_salt(self):
        return self.db.get_user_security("salt", self.username)

    def get_db(self):
        return self.db

    def add_connection(self):
        print("Added Connections")
        self.db.incr_connections(self.username)

    def add_password(self, site, identifier, password, icon):
        print(f"Adding: {site}, {identifier}, {password}, {icon}")
        crypted_password = encrypt(self.key, password)
        crypted_username = encrypt(self.key, identifier)
        crypted_site = encrypt(self.key, site)

        self.db.add_password(crypted_site, crypted_username, crypted_password, self.username, "None" if icon is None else icon)

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

    def save_favicon_locally(self, favicon_url): # XXX: unused function ?
        if favicon_url:
            try:
                favicon = requests.get(favicon_url).content
                filename = self.generate_unique_filename()


                print("Path: ", os.path.join(os.environ['APPDATA'], "MDPSaver", f"{filename}.ico"))
                with open(os.path.join(os.environ['APPDATA'], "MDPSaver", f"{filename}.ico"), "wb") as f:
                    f.write(favicon)

                return filename
            except:
                pass
        return None

    def get_image_or_icon_file_path(self):
        file_name, _ = QFileDialog.getOpenFileName(None, "Select Image or Icon", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif);;Icon Files (*.ico);;Executable Files (*.exe)")
        return file_name

    def extract_icon_from_executable(self, executable_path):
        icon = QAbstractFileIconProvider().icon(QFileInfo(executable_path))
        return icon.pixmap(32, 32).toImage()

    def __push_password__(self, target, username, password, icon):
        if not os.path.exists(os.path.join(os.environ['APPDATA'], "MDPSaver")):
                    os.makedirs(os.path.join(os.environ['APPDATA'], "MDPSaver"), exist_ok=True)
        favicon = self.get_favicon_url(target)
        if icon == "on":
            if favicon is None:
                # show filebrowser dialog
                file_name, _ = QFileDialog.getOpenFileName(self.parent, "Select Icon - Just quit to not use one.", "", "Icon Files (*.ico);;Image Files (*.png *.svg);;Executable Files (*.exe *.dll);;All Files (*)")
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


        self.add_password(target, username, password, favicon)


    # load key when starting the app, as well as the username of the current user
    def load_app(self, username, password):
        self.username = username
        self.key = load_key(password, self.get_salt())
        self.add_connection()

    def initiate_db_settings(self, username, password, rec_question, rec_answer, nbr_connections=0) -> bool:
        # This function initializes UserSecurity / recovery / ... It follows MDPSaverLogic.png
        # 1) Create the salt (used to load the key)
        salt = os.urandom(16)

        # 2) Create the serial number (used to encrypt the question)
        serial_number = abs(int(time.time()))

        # 3) Hash of the AP
        hashed_password = hashing(password)

        # 4) Hash of the Answer
        hashed_answer = hashing(rec_answer)

        # 5) Encryption of the AP with the Answer
        encrypted_password = encrypt_extern_password(rec_answer, password, salt)

        # 6) Encryption of the Question with the Serial Number
        encrypted_question = encrypt_extern_password(str(serial_number), rec_question, salt)
        if not self.db.initiate_user(username, serial_number, nbr_connections):
            return False

        if not self.db.initiate_user_security(username, hashed_password, hashed_answer, encrypted_password,
                                              encrypted_question, salt):
            return False

        # Key is used to decrypt / encrypt passwords / ...
        self.key = load_key(password, salt)

        return True

    def check_login(self, username, password):
        return hashing(password) == self.db.get_user_security("hashed_password", username)

    def close_app(self):
        self.db.close_cursor()

    def kill_db(self):
        print("KILLED DB")
        self.db.reset_db()


class Recover:
    def __init__(self, controller: Controller):
        self.controller = controller
        self.username = self.controller.username
        self.db = self.controller.get_db()

    def get_personnal_question(self):
        e_question = self.controller.get_encrypted_question()
        serial_number = self.controller.get_serial_number()
        salt = self.controller.get_salt()
        question = decrypt_extern_password(str(serial_number), e_question,
                                           salt)  # question is encrypted using str(serial_number)

        return question

    def verify_answer(self, answer):
        return hashing(answer) == self.controller.get_hashed_answer()

    def delete_user_security(self, username):
        self.db.delete_user_security(username)

    def delete_user(self, username):
        self.db.delete_user(username)

    def update_passwords(self, old_password, old_salt, new_password, new_salt, username) -> None:
        data = self.db.get_all_passwords(username)
        # Load old and new key
        old_key = load_key(old_password, old_salt)
        new_key = load_key(new_password, new_salt)

        for index, old_data in enumerate(data):
            # Retrieve old crypted data;
            old_c_username, old_c_site, old_c_pass = old_data[0], old_data[1], old_data[2]

            # Translate it to real values;
            username, site, passw = decrypt(old_key, old_c_username), decrypt(old_key, old_c_site), decrypt(old_key,
                                                                                                            old_c_pass)

            # Encrypt to new key
            crypted_username, crypted_site, crypted_pass = encrypt(new_key, username), encrypt(new_key, site), encrypt(
                new_key, passw)

            # Update DB
            self.db.set_password(crypted_username, crypted_site, crypted_pass, index + 1)

    def write_user_security(self, username, password, rec_question, rec_answer, nbr_connections):
        # XXX call 2 functions so user isnt replaced
        self.controller.initiate_db_settings(username, password, rec_question, rec_answer, nbr_connections)

    def get_old_password(self, answer, encrypted_password, old_salt) -> str:
        return decrypt_extern_password(answer, encrypted_password, old_salt)

    def applicate_recovery(self, new_password, rec_question, new_answer, old_answer) -> bool:
        # XXX check for each step completion

        # 0) Retrieve required User / UserSecurity informations before deletion
        old_salt = self.controller.get_salt()
        nbr_connections = self.controller.get_times_connected()
        encrypted_password = self.controller.get_encrypted_password()
        old_password = self.get_old_password(old_answer, encrypted_password, old_salt)
        username = self.username

        # 1) Delete current User Security
        self.delete_user_security(username)

        # 2) Delete current User
        self.delete_user(username)

        # 2) Write new informations in User Security
        self.write_user_security(username, new_password, rec_question, new_answer, nbr_connections)

        # 3) Make transition of password encrypting

        new_salt = self.controller.get_salt()  # It's different than initial salt, as user security has been updated just above


        self.update_passwords(old_password, old_salt, new_password, new_salt, username)

        # 4) Load app with new password
        self.controller.load_app(username, new_password)

        return True