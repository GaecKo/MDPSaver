from MDPDatabase.MDPdatabase import MDPData 
from MDPDatabase.security import *
import os

class Controller:
    def __init__(self): 
        self.db = MDPData()
        self.key = None # Will contain the key to decrypt data

    def get_username(self):
        return self.db.get_user("username")
    
    def get_serial_number(self):
        return self.db.get_user("serial_number")

    def get_times_connected(self):
        return self.db.get_user("times_connected")

    def get_hashed_password(self):
        return self.db.get_user_security("hashed_password")
    
    def get_hashed_answer(self):
        return self.db.get_user_security("hashed_answer")
    
    def get_encrypted_password(self):
        return self.db.get_user("encrypted_password")
    
    def get_encrypted_question(self):
        return self.db.get_user_security("encrypted_question")
    
    def get_salt(self):
        return self.db.get_user_security("salt")

    def get_db(self):
        return self.db

    def add_connection(self):
        print("Added Connections")
        self.db.incr_connections()
    
    def add_password(self, site, username, password):
        crypted_password = encrypt(self.key, password)
        self.db.add_password(site, username, crypted_password)

    def is_first_startup(self):
        return not self.db.is_app_initialized()
    
    # load key when starting

    def load_app(self, password):
        print(self.get_salt())
        self.key = load_key(password, self.get_salt())
        self.add_connection()

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
        
        if not self.db.initiate_user_security(username, hashed_password, hashed_answer, encrypted_password, encrypted_question, salt):
            return False
        
        # Key is used to decrypt / encrypt passwords / ...
        self.key = load_key(password, salt)

        return True
    
    def check_login(self, password):
        return hashing(password) == self.db.get_user_security("hashed_password")

    def kill_db(self):
        print("KILLED DB")
        self.db.apply_sql()


class Recover(Controller):
    def __init__(self):
        super().__init__()
        self.serial_number = super().get_serial_number()
        self.salt = super().get_salt()
        self.db = super().get_db()
    
    def get_personnal_question(self):
        e_question = super().get_encrypted_question()
        question = decrypt_extern_password(str(self.serial_number), e_question, self.salt) # question is encrypted using str(serial_number)

        return question
    
    def verify_answer(self, answer):
        print(hashing(answer))
        print(super().get_hashed_answer())
        return hashing(answer) == super().get_hashed_answer()
    
    def delete_user_security(self):
        self.db.delete_user_security()
    
    def update_passwords(self, old_password, new_password):
        passwords = self.db.get_all_passwords()
