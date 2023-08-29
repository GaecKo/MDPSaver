from MDPDatabase.MDPDatabase import MDPDatabase
from MDPDatabase.security import *
from IconGrabber import IconGrabber
import os, time, random, string
from pathlib import Path

from PIL import Image

import random, uuid


from PySide6.QtCore import QFileInfo
from PySide6.QtGui import QAbstractFileIconProvider
from PySide6.QtWidgets import QFileDialog

import io
if os.name == "nt":
    import win32con
    import win32api
    import win32ui
    import win32gui


BI_RGB = 0
DIB_RGB_COLORS = 0


class Controller:
    """
    Controller is an interface for the database usage.
    """

    def __init__(self, parent=None):
        self.parent = parent
        self.db = MDPDatabase()

        self.key = None  # Will contain the key to decrypt data
        self.username = None  # has to be set when logged in!
        self.icon_path = Path(__file__).parent.parent
        self.icon_path = self.icon_path / "resources" / "icons"
        self.grabber = IconGrabber(self, "#5e5e51")

        # Create icon folder if not exists
        if not os.path.exists(self.icon_path):
            os.makedirs(self.icon_path, exist_ok=True)

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

            site, username, password = decrypt(self.key, c_site), decrypt(self.key, c_username), decrypt(self.key,
                                                                                                         c_password)
            # passwords[index] = [site, username, password]
            passwords[index] = {"target": site, "username": username, "password": password, "icon": data[3], "id": data[4]}

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

        self.db.add_password(crypted_site, crypted_username, crypted_password, self.username,
                             "None" if icon is None else icon)

    def remove_password(self, id):
        self.db.remove_password(id)

    # TODO: icon modification?
    def update_password(self, site, identifier, password, id):
        crypted_password = encrypt(self.key, password)
        crypted_username = encrypt(self.key, identifier)
        crypted_site = encrypt(self.key, site)

        self.db.set_password(crypted_site, crypted_username, crypted_password, id)

    def generate_random_password(self, nb_letters: int, nb_numbers: int, nb_symbols: int, uppercase: bool) -> str:
        if uppercase:
            letters = string.ascii_letters
        else:
            letters = string.ascii_lowercase

        symbols = '!@#$%^&*()_+[]{}|;:,.<>?'
        numbers = string.digits

        result = []

        for _ in range(nb_letters):
            result.append(random.choice(letters))

        for _ in range(nb_symbols):
            result.append(random.choice(symbols))

        for _ in range(nb_numbers):
            result.append(random.choice(numbers))

        random.shuffle(result)
        return ''.join(result)

    def generate_simple_password(self, upper: bool, numbers: bool, symbols: bool, length: int) -> str:
        # Find number of each elements (symbol, letter, number)
        nb_elements = 1
        if numbers: nb_elements += 1
        if symbols: nb_elements += 1

        if not numbers and not symbols: nb_letters = length
        else: nb_letters = random.randint(1, 2 * (length//nb_elements))

        nb_numbers = 0
        nb_symbols = 0

        remaining_length = length - nb_letters

        if numbers and not symbols: nb_numbers = remaining_length

        elif symbols and not numbers: nb_symbols = remaining_length

        elif numbers and symbols:
            nb_numbers = random.randint(1, remaining_length-1)
            remaining_length = remaining_length - nb_numbers
            nb_symbols = remaining_length

        return self.generate_random_password(nb_letters, nb_numbers, nb_symbols, upper)

    def generate_advanced_password(self, nb_letters: int, nb_numbers: int, nb_symbols: int, upper: bool):
        return self.generate_random_password(nb_letters, nb_numbers, nb_symbols, upper)

    def generate_unique_filename(self):
        # get all filenames from icon fiels dir
        filenames = [f for f in os.listdir(self.icon_path) if os.path.isfile(os.path.join(self.icon_path, f))] + [""]
        filename = ""
        while filename in filenames:
            filename = str(uuid.uuid4()) + str(uuid.uuid4())
            filename = filename[:random.randint(6, len(filename))]
        print(f"File: %s" % filename)
        return filename[:random.randint(6, len(filename))]


    def get_image_or_icon_file_path(self):
        file_types = "All Files (*)"
        file_types += ";;Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        file_types += ";;Icon Files (*.ico)"

        file_name, _ = QFileDialog.getOpenFileName(None, "Select Image or Icon", "", file_types)
        return file_name

    def extract_icon_from_executable(self, executable_path):
        executable_file = win32api.LoadLibraryEx(executable_path, 0, win32con.LOAD_LIBRARY_AS_DATAFILE)

        # Extraire l'icône du groupe spécifié
        icon_handle = win32gui.ExtractIconEx(executable_path, 0)[0]

        # Obtenir les données brutes de l'icône
        icon_info = win32gui.GetIconInfo(icon_handle)
        bmp_handle = icon_info[4]

        # Obtenir les informations du bitmap
        bmp_info = win32gui.GetObject(bmp_handle)

        # Créer un contexte de périphérique compatible et un bitmap
        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, bmp_info.bmWidth, bmp_info.bmHeight)
        hdc = hdc.CreateCompatibleDC()

        # Sélectionner le bitmap dans le contexte de périphérique
        hdc.SelectObject(hbmp)

        # Dessiner l'icône sur le bitmap
        hdc.DrawIcon((0, 0), icon_handle)

        bmpstr = hbmp.GetBitmapBits(True)
        img = Image.frombuffer(
            'RGB',
            (32, 32),
            bmpstr,
            'raw',
            'BGRX',
            0,
            1
        )

        unique_filename = self.generate_unique_filename()
        ico_path = self.icon_path / f"{unique_filename}.ico"

        img.save(ico_path, format="ICO", quality=95)  # Adjust quality if needed

        print("Icon saved to:", ico_path, " with name:", unique_filename)

        win32gui.DestroyIcon(icon_handle)

        return unique_filename

    def save_favicon_locally(self, favicon):
        unique_filename = self.generate_unique_filename()
        ico_path = self.icon_path / f"{unique_filename}.png"
        with open(ico_path, "wb") as f:
            f.write(favicon)
        return unique_filename
    
    def __push_password__(self, target, username, password, icon):
        filename = self.grabber.get_icon(target)
        print(f"filename : {filename}")
        if filename is None:
            if icon is True:
                # show filebrowser dialog
                file_name = self.get_image_or_icon_file_path()
                print(file_name)
                if file_name:
                    if file_name.endswith(".exe") or file_name.endswith(".dll") and os.name == "nt":
                        # extract icon from executable
                        try:
                            filename = self.extract_icon_from_executable(file_name)
                        except Exception as e:
                            filename =  None
                    else:
                        # copy file to appdata
                        favicon = open(file_name, "rb").read()
                        filename = self.save_favicon_locally(favicon)
        
        if filename is None:
            filename = self.icon_path.parent / "blank-profile-picture.ico"

        self.add_password(target, username, password, filename)

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
            # old_data = (crypted_username, crypted_site, crypted_pass, icon, id)
            old_c_username, old_c_site, old_c_pass, id = old_data[0], old_data[1], old_data[2], old_data[4]

            # Translate it to real values;
            username, site, passw = decrypt(old_key, old_c_username), decrypt(old_key, old_c_site), decrypt(old_key,
                                                                                                            old_c_pass)

            # Encrypt to new key
            crypted_username, crypted_site, crypted_pass = encrypt(new_key, username), encrypt(new_key, site), encrypt(
                new_key, passw)

            # Update DB
            self.db.set_password(crypted_site, crypted_username, crypted_pass, id)

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
