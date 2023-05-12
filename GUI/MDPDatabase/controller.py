from MDPDatabase import MDPData 
from security import *

class Controller:
    def __init__(self): 
        self.db = MDPData()

    def get_username(self):
        return self.db.get_username()
    
    def is_first_startup(self):
        return  not self.db.is_app_initialized()
            

    def check_login(self, password):
        pass
     