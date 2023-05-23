import sqlite3
from .ApplySQL import apply_sql

class MDPData:
    def __init__(self):
        self.con = sqlite3.connect("MDPDatabase/MDPdatabase.sqlite")
        self.cur = self.con.cursor()
    
    def add_password(self, site: str, username: str, crypted_password: str) -> None:
        self.cur.execute(f"INSERT INTO Password (site, username, password) VALUES (?,?,?)", (site, username, crypted_password))
        self.con.commit()
    
    def get_password_data(self, id: int) -> tuple:
        """
        @pre: id -> id of the password 
        @return: a tuple: (site, username, crypted_password) if id in db
                 None otherwise
        """
        self.cur.execute(f"SELECT site, username, password FROM Password WHERE id = {id}")

        result = self.cur.fetchone()

        if result:
            site, username, password = result
            return (site, username, password)
        else:
            return None 
    
    def get_salt(self, hashed_password):
        self.cur.execute(f"SELECT salt FROM UserSecurity WHERE hashed_password = {hashed_password}")

        result = self.cur.fetchone()

        if result:
            salt = result[0]
            return salt
        else:
            return None
    
    def get_user(self, attribute: str):

        if attribute not in ["username", "times_connected", "serial_number"]:
            return None

        self.cur.execute(f"SELECT {attribute} FROM User")

        result = self.cur.fetchone()

        if result:
            return result[0]
        else:
            return None
    
    def get_user_security(self, attribute: str) -> str:
        if attribute not in ["username", "hashed_password", "hashed_answer", "encrypted_password", "encrypted_question", "salt"]:
            return None
        
        self.cur.execute(f"SELECT {attribute} FROM UserSecurity")

        result = self.cur.fetchone()

        if result:
            return result[0]
        else:
            return None
        
    def incr_connections(self) -> None:
        self.cur.execute("UPDATE User SET times_connected = times_connected + 1")
        self.con.commit()

    def set_username(self, new_username: str) -> None:
        self.cur.execute("UPDATE User SET username = ? WHERE id = 1", (new_username,))
        self.con.commit()

    def is_app_initialized(self):

        self.cur.execute(f"SELECT username FROM User")

        result = self.cur.fetchone()

        if result:
            return True
        else:
            return False

    def initiate_user(self, username, serial_number) -> bool:
        self.cur.execute(f"INSERT INTO User (username, times_connected, serial_number) VALUES (?, ?, ?)", (username, 0, serial_number))
        try:
            self.con.commit()
            return True
        except:
            return False

    def initiate_user_security(self, username, hashed_password, hashed_answer, encrypted_password, encrypted_question, salt) -> bool:
        self.cur.execute(f"INSERT INTO UserSecurity (username, hashed_password, hashed_answer, encrypted_password, encrypted_question, salt) VALUES (?, ?, ?, ?, ?, ?)", (username, hashed_password, hashed_answer, encrypted_password, encrypted_question, salt))
        try:
            self.con.commit()
            return True
        except:
            return False

    def close_cursor(self):
        self.cur.close()

    def reset_db(self):
        apply_sql()

if __name__ == "__main__":
    data = MDPData()
    data.get_times_conntected()