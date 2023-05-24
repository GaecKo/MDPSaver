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
        crypted_username = encrypt(self.key, username)
        crypted_site = encrypt(self.key, username)

        self.db.add_password(crypted_site, crypted_username, crypted_password)

    def is_first_startup(self):
        return not self.db.is_app_initialized()
    
    # load key when starting

    def load_app(self, password):
        self.key = load_key(password, self.get_salt())
        self.add_connection()

    # XXX URGENT: Move serial & initiate user in another function 
    def initiate_user_security(self, username, password, rec_question, rec_answer) -> bool:
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


class Recover:
    def __init__(self, controller: Controller):
        self.controller = controller

        self.serial_number = self.controller.get_serial_number()
        self.salt = self.controller.get_salt()
        self.db = self.controller.get_db()
        self.old_salt = None # Will be set when initiating app
    
    def get_personnal_question(self):
        e_question = self.controller.get_encrypted_question()
        question = decrypt_extern_password(str(self.serial_number), e_question, self.salt) # question is encrypted using str(serial_number)

        return question
    
    def verify_answer(self, answer):
        print(hashing(answer))
        print(self.controller.get_hashed_answer())
        return hashing(answer) == self.controller.get_hashed_answer()
    
    def delete_user_security(self):
        self.db.delete_user_security()
    
    def update_passwords(self, old_password, old_salt, new_password, new_salt) -> None:
        data = self.db.get_all_passwords()

        # Loal old and new key
        old_key = load_key(old_password, old_salt) 
        new_key = load_key(new_password, new_salt)

        for index, old_data in enumerate(data):
            # Retrieve old crypted data;
            old_c_username, old_c_site, old_c_pass = old_data[0], old_data[1], old_data[2]  

            # Translate it to real values;
            username, site, passw = decrypt(old_key, old_c_username), decrypt(old_key, old_c_site), decrypt(old_key, old_c_pass)

            # Encrypt to new key
            crypted_username, crypted_site, crypted_pass = encrypt(new_key, username), encrypt(new_key, site), encrypt(new_key, passw)

            # Update DB
            self.db.set_password(crypted_username, crypted_site, crypted_pass, index + 1)

    
    def write_user_security(self, password, rec_question, rec_answer):
        self.old_salt = self.salt
        # XXX call 2 functions so user isnt replaced
        self.controller.initiate_user_security(self.controller.get_username(), password, rec_question, rec_answer)

    def get_old_password(self, answer, old_salt) -> str:
        return decrypt_extern_password(answer, self.controller.get_encrypted_password(), old_salt)

    def applicate_recovery(self, new_password, rec_question, new_answer, old_answer) -> bool:
        # XXX check for each step completion

        # 1) Delete current User Security
        self.delete_user_security()

        # 2) Write new informations in User Security
        self.write_user_security(new_password, rec_question, new_answer)

        # 3) Make transition of password encrypting
        old_password = self.get_old_password(old_answer, self.old_salt)
        old_salt = self.old_salt
        new_salt = self.controller.get_salt()

        self.update_passwords(old_password, old_salt, new_password, new_salt)
        

        # 4) Load app with new password
        self.controller.load_app(new_password)

        return True