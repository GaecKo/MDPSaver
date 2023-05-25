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
    
    def get_all_passwords(self):
        self.cur.execute(f"SELECT site, username, password FROM Password")

        result = self.cur.fetchall()
        return result
    
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

    def set_password(self, new_username, new_site, new_pass, id) -> None:
        query = "UPDATE Password SET site = ?, username = ?, password = ? WHERE id = ?"
        values = (new_site, new_username, new_pass, id)
        self.cur.execute(query, values)
        
        self.con.commit() 

    def is_app_initialized(self):

        self.cur.execute("SELECT username FROM User")

        result = self.cur.fetchone()

        if result:
            return True
        else:
            return False

    def initiate_user(self, username, serial_number, number_of_connections=0) -> bool:

        self.cur.execute(f"INSERT INTO User (username, times_connected, serial_number) VALUES (?, ?, ?)", (username, number_of_connections, serial_number))
        try:
            self.con.commit()
            return True
        except:
            return False

    def delete_user_security(self):

        self.cur.execute(f"DELETE FROM UserSecurity")
        self.con.commit()
    
    def delete_user(self):

        self.cur.execute(f"DELETE FROM User")
        self.con.commit()
    
    
    def set_serial_number(self, serial_number):
        username = self.get_user("username")
        self.cur.execute(f"UPDATE User SET serial_number WHERE username = {username}")

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

