import sqlite3

class MDPData:
    def __init__(self):
        con = sqlite3.connect("MDPdatabase.sqlite")
        cur = con.cursor()