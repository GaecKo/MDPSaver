from MDPDatabase.MDPdatabase import MDPData 
from MDPDatabase.security import *
import os

class Controller:
    def __init__(self): 
        self.db = MDPData()
        self.key = None # Will contain the key to decrypt data

    def get_username(self):
        return self.db.get_username()
    

    def add_connection(self):
        print("Added Connections")
        self.db.incr_connections()

    def is_first_startup(self):
        return not self.db.is_app_initialized()
    
    # load key when starting

    def load_app(self, password):
        self.key = load_key(password, self.db.get_salt(hashing(password)))

    def initiate_app(self, username, password, rec_question, rec_answer) -> bool:
        # This function initializes UserSecurity / recovery / ... It follows MDPSaverLogic.png
        # 1) Create the salt (used to load the key)
        salt = os.urandom(16)

        # 2) Create the serial number (used to encrypt the question)
        serial_number = abs(int(low_hash(password)))

        # 3) Hash of the AP
        hashed_password = hashing(password)

        # 4) Hash of the Answer
        hashed_answer = hashing(rec_answer)

        # 5) Encryption of the AP with the Answer
        encrypted_password = encrypt_extern_password(rec_answer, password, salt)

        # 6) Encryption of the Question with the Serial Number
        encrypted_question = encrypt_extern_password(str(serial_number), rec_question, salt)

        if not self.db.initiate_user(username, serial_number):
            return False
        
        if not self.db.initiate_user_security(hashed_password, hashed_answer, encrypted_password, encrypted_question, salt):
            return False
        
        # Key is used to decrypt / encrypt passwords / ...
        self.key = load_key(password, salt)

        return True
    
    def check_login(self, password):
        return hashing(password) == self.db.get_hashed_password()

    def kill_db(self):
        print("KILLED DB")
        self.db.apply_sql()
