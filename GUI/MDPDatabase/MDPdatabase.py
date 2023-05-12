import sqlite3

class MDPData:
    def __init__(self):
        con = sqlite3.connect("MDPdatabase.sqlite")
        self.cur = con.cursor()
    
    def add_password(self, site: str, username: str, password: str):
