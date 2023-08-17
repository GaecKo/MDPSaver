import sqlite3
import os
from .ApplySQL import apply_sql


# TODO: Add type for all arguments and return values
# TODO: Clean SQL requests

class MDPDatabase:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        database_path = os.path.join(current_dir, "MDPDatabase.sqlite")
        print("DB FILE EXIST: ", os.path.exists(database_path))

        if not os.path.exists(database_path):
            apply_sql()

        self.con = sqlite3.connect(database_path)
        self.cur = self.con.cursor()

    def add_password(self, c_site: str, c_identifier: str, c_password: str, user: str, icon: str) -> None:
        self.cur.execute(f"INSERT INTO Password (user, site, identifier, password, icon) VALUES (?,?,?,?,?)",
                         (user, c_site, c_identifier, c_password, icon))
        self.con.commit()

    def count(self, table):
        self.cur.execute(f"SELECT COUNT(*) FROM {table}")
        return self.cur.fetchone()[0]

    def get_password_data(self, id: int) -> tuple:
        """
        @pre: id -> id of the password 
        @return: a tuple: (site, username, crypted_password) if id in db
                 None otherwise
        """
        self.cur.execute(f"SELECT site, identifier, password, icon FROM Password WHERE id = '{id}'")
        self.cur.execute(f"SELECT site, identifier, password, icon FROM Password WHERE id = '{id}'")

        result = self.cur.fetchone()

        if result:
            site, username, password, icon = result
            return (site, username, password, icon)
            site, username, password, icon = result
            return (site, username, password, icon)
        else:
            return None

    def get_all_passwords(self, username: str) -> list:

        self.cur.execute(f"SELECT site, identifier, password, icon FROM Password WHERE user = '{username}'")
        result = self.cur.fetchall()

        if result:
            return result
        else:
            return []

    def get_usernames(self):
        self.cur.execute(f"SELECT username FROM User")

        result = self.cur.fetchall()
        return result

    def get_user_attribute(self, attribute: str, username):

        if attribute not in ["username", "times_connected", "serial_number"]:
            return None

        self.cur.execute(f"SELECT {attribute} FROM User WHERE username = '{username}'")

        result = self.cur.fetchone()

        if result:
            return result[0]
        else:
            return None

    def get_user_security(self, attribute: str, username) -> str:

        if attribute not in ["username", "hashed_password", "hashed_answer", "encrypted_password", "encrypted_question",
                             "salt"]:
            return None

        self.cur.execute(f"SELECT {attribute} FROM UserSecurity WHERE user = '{username}'")

        result = self.cur.fetchone()

        if result:
            return result[0]
        else:
            return None

    def incr_connections(self, username) -> None:
        self.cur.execute("UPDATE User SET times_connected = times_connected + 1 WHERE username = ?", (username,))
        self.con.commit()

    def set_username(self, new_username: str, username) -> None:
        self.cur.execute(f"UPDATE User SET username = ? WHERE username = {username}", (new_username,))
        self.con.commit()

    def set_password(self, new_identifier, new_site, new_pass, username) -> None:
        query = "UPDATE Password SET site = ?, identifier = ?, password = ? WHERE user = ?"
        values = (new_site, new_identifier, new_pass, username)
        self.cur.execute(query, values)

        self.con.commit()

    def initiate_user(self, username, serial_number, number_of_connections=0) -> bool:

        self.cur.execute(f"INSERT INTO User (username, times_connected, serial_number) VALUES (?, ?, ?)",
                         (username, number_of_connections, serial_number))
        try:
            self.con.commit()
            return True
        except:
            return False

    def delete_user_security(self, username):

        self.cur.execute(f"DELETE FROM UserSecurity WHERE user = '{username}'")
        self.con.commit()

    def delete_user(self, username):

        self.cur.execute(f"DELETE FROM User WHERE username = '{username}'")
        self.con.commit()

    def delete_password(self, id):
        self.cur.execute(f"DELETE FROM Password WHERE id = '{id}'")
        self.con.commit()

    def set_serial_number(self, serial_number, username):
        username = self.get_user("username")
        self.cur.execute(f"UPDATE User SET serial_number = ? WHERE username = '{username}'", (serial_number,))

    def initiate_user_security(self, username, hashed_password, hashed_answer, encrypted_password, encrypted_question,
                               salt) -> bool:
        self.cur.execute(
            f"INSERT INTO UserSecurity (user, hashed_password, hashed_answer, encrypted_password, encrypted_question, salt) VALUES (?, ?, ?, ?, ?, ?)",
            (username, hashed_password, hashed_answer, encrypted_password, encrypted_question, salt))
        try:
            self.con.commit()
            return True
        except:
            return False

    def close_cursor(self):
        self.cur.close()
        self.con.close()

    def reset_db(self):
        apply_sql()
