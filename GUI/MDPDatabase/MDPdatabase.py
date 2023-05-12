import sqlite3

class MDPData:
    def __init__(self):
        self.con = sqlite3.connect("MDPdatabase.sqlite")
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
    
    def get_username(self):
        self.cur.execute(f"SELECT username FROM User WHERE id = 1")

        result = self.cur.fetchone()

        if result:
            username = result[0]
            return username
        else:
            return None
    
    def get_times_conntected(self):
        self.cur.execute(f"SELECT times_connected FROM User WHERE id = 1")

        result = self.cur.fetchone()

        if result:
            times_connected = result[0]
            return times_connected
        else:
            return None
        
    def incr_connections(self) -> None:
        self.cur.execute("UPDATE User SET times_connected = times_connected + 1 WHERE id = 1")
        self.con.commit()

    def set_username(self, new_username: str) -> None:
        self.cur.execute("UPDATE User SET username = ? WHERE id = 1", (new_username,))
        self.con.commit()


    def is_app_initialized(self):
        if self.get_times_conntected() == 0:
            return False
        return True


    def close_cursor(self):
        self.cur.close()
