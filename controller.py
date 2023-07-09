from MDPDatabase.MDPdatabase import MDPData 
from MDPDatabase.security import *
import os

class Controller:
    def __init__(self): 
        self.db = MDPData()
        self.key = None # Will contain the key to decrypt data

    def get_all_passwords(self):
        if self.key == None:
            return None
        
        passwords = list(self.db.get_all_passwords())
        

        for index, data in enumerate(passwords):
            data = list(data)
            c_site, c_username, c_password = data[0], data[1], data[2]

            site, username, password = decrypt(self.key, c_site), decrypt(self.key, c_username), decrypt(self.key, c_password)
            print(site, username, password)
            passwords[index] = [site, username, password]
        
        return passwords


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
        return self.db.get_user_security("encrypted_password")
    
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
        crypted_site = encrypt(self.key, site)

        self.db.add_password(crypted_site, crypted_username, crypted_password)

    def is_first_startup(self):
        return not self.db.is_app_initialized()
    
    # load key when starting

    def load_app(self, password):
        self.key = load_key(password, self.get_salt())
        self.add_connection()

    def initiate_db_settings(self, username, password, rec_question, rec_answer, nbr_connections=0) -> bool:
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
        if not self.db.initiate_user(username, serial_number, nbr_connections):
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
        self.db = self.controller.get_db()
    
    def get_personnal_question(self):
        e_question = self.controller.get_encrypted_question()
        serial_number = self.controller.get_serial_number()
        salt = self.controller.get_salt()
        question = decrypt_extern_password(str(serial_number), e_question, salt) # question is encrypted using str(serial_number)

        return question
    
    def verify_answer(self, answer):
        return hashing(answer) == self.controller.get_hashed_answer()
    
    def delete_user_security(self):
        self.db.delete_user_security()
    
    def delete_user(self):
        self.db.delete_user()

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
        username = self.controller.get_username()

        # 1) Delete current User Security
        self.delete_user_security()

        # 2) Delete current User
        self.delete_user()

        # 2) Write new informations in User Security
        self.write_user_security(username, new_password, rec_question, new_answer, nbr_connections)

        # 3) Make transition of password encrypting
        
        new_salt = self.controller.get_salt() # It'different than initial salt, as user security has been updated just above

        self.update_passwords(old_password, old_salt, new_password, new_salt)
        
        # 4) Load app with new password
        self.controller.load_app(new_password)

        return True