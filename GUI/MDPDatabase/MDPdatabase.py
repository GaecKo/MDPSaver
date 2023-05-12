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
    
    def get_user

    def close_cursor(self):
        self.cur.close()
