from crypto import decode, encode, hashing
from function import *

class Data:
    def __init__(self):
        self.__files = "data.txt"
        self.__default = "default.txt"
        self.__hashed = "hashed.txt"
    
    def get_props(self):
        with open(self.__files, 'r', encoding="utf-8") as file:
            if file.readlines() == []:
                return False
            else:
                return True
    
    def get_personnal_question(self):
        with open(self.__default, 'r', encoding="utf-8") as file:
            return file.readlines()[2].split(":")[1].rstrip('\n')
    
    def get_hashed_password(self):
        with open(self.__hashed, 'r', encoding="utf-8") as file:
            return file.readlines()[0].rstrip("\n")
    
    def get_hashed_answer(self):
        with open(self.__hashed, 'r', encoding="utf-8") as file:
            return file.readlines()[1].rstrip("\n") 

    def get_times_connected(self):
        with open(self.__default, 'r') as file:
            return int(file.readlines()[0].split(":")[1])
        
    def add_site_password(self, access_password, site, site_password):
        with open(self.__files, 'r', encoding="utf-8") as file:
            content = file.read()
        if self.get_props():
            content += "\n" + encode(access_password, site) + " | " +encode(access_password, site_password)
        else:
            content += encode(access_password, site) + " | " +encode(access_password, site_password)
        with open(self.__files, 'w', encoding="utf-8") as file:
            file.write(content)

    def add_one_connection(self):
        times = self.get_times_connected() + 1
        with open(self.__default, 'r') as file:
            lines = file.readlines()
        lines[0] = "times_connected:" + str(times) + "\n"
        with open(self.__default, 'w') as file:
            file.writelines(lines)

    def back_to_first_start(self): # to complete
        with open(self.__default, 'w') as file:
            file.write("times_connected:" + str(0))

    def first(self):
        return self.get_times_connected() == 1

    def set_username(self, user_name) -> str:
        with open(self.__default, 'r') as file:
            lines = file.readlines()
        lines[1] = "username:" + user_name + "\n"
        with open(self.__default, 'w') as file:
            file.writelines(lines)
        
    def get_username(self):
        with open(self.__default, 'r') as file:
            return file.readlines()[1].split(":")[1].rstrip("\n")

    def search(self, access_password, index):
        d = {}
        with open(self.__files, 'r', encoding="utf-8") as file:
            content = file.readlines()
        return (decode(access_password, content[index].split(" | ")[0]), decode(access_password, content[index].split(" | ")[1].rstrip("\n")))
    
    def checkup(self):
        try:
            with open(self.__default, 'r', encoding="utf-8") as file:
                content = file.readlines()
            if content[1].rstrip("\n").split(":")[1] == "?":
                raise MissingContent
            if content[2].rstrip("\n").split(":")[1] == "?":
                raise MissingContent
        except:
            raise DefaultFileCorrupted
        try:
            with open(self.__hashed, 'r', encoding="utf-8") as file:
                if len(file.readlines()) != 3:
                    raise MissingContent
        except:
            raise HashedFileCorrupted
        return True
    
    def sites_list(self, access_password):
        with open(self.__files, 'r', encoding="utf-8") as file:
            content = file.readlines()
        text = ""
        for i in range(len(content)):
            text += "| " + str(i+1) +") " + decode(access_password, content[i].split(" | ")[0]) + "\n"
        return (text, len(content) + 1)
        
    def delete_site(self, index):
        with open(self.__files, 'r', encoding="utf-8") as file:
            content = file.readlines()
        content.pop(index)
        with open(self.__files, "w", encoding="utf-8") as file:
            file.writelines(content)
        
    def change_password_site(self, index, access_password, new_password):
        with open(self.__files, 'r', encoding="utf-8") as file:
            content = file.readlines()
        site = content[index].split(" | ")[0] + " | " + encode(access_password, new_password)
        content[index] = site
        with open(self.__files, "w", encoding="utf-8") as file:
            file.writelines(content)
        
    def change_hashed_password(self, new_access):
        with open(self.__hashed, 'r', encoding="utf-8") as file:
            content = file.readlines()
        content[0] = hashing(new_access) + "\n"
        with open(self.__hashed, 'w', encoding='utf-8') as file:
            file.writelines(content)
    
    def get_coded_password(self):
        with open(self.__hashed, 'r', encoding='utf-8') as file:
            content = file.readlines()
        return content[2].rstrip("\n")

    def recover_password(self):
        print("\n -------+-------+-------+-------")
        while True:
            print("Please give the answer of your personnal question: (if you don't know it, contact GaecKo#7545)")
            print("- - - - - - -")
            print(self.get_personnal_question())
            print("---")
            answer = input("answer: \n>>")
            if hashing(answer) == self.get_hashed_answer():
                break
            else:
                print("You didn't give the good answer, please retry")
                self.recover_password()
                return
        print("Good answer!")
        old_password = decode(answer, self.get_coded_password())
        print(old_password)
        print("Please create a new password and a new question.")
        new = create_password(True)
        print(new)
        self.change_hashed_password(new)
        print(hashing(new))
        print(self.get_hashed_password)
        
        with open(self.__files, 'r', encoding="utf-8") as file:
            content = file.readlines()
        for i in range(len(content)):
            content[i] = content[i].split(" | ")
            content[i][0] = encode(new, decode(old_password, content[i][0]))
            content[i][1] = encode(new, decode(old_password, content[i][1].rstrip("\n"))) + "\n"
            content[i] = content[i][0] + " | " + content[i][1]
        if len(content) > 0:
            content[-1] = content[-1].rstrip("\n")
        with open(self.__files, 'w', encoding="utf-8") as file:
            file.writelines(content)
        return new
            
    def change_access_password(self):
        old = input("Old password:\n>>")
        old_verif = input("Confirm Old password\n>>")
        if hashing(old_verif) == self.get_hashed_password() and hashing(old) == self.get_hashed_password():
            new_password = input("New password:\n>>")
            self.change_hashed_password(new_password)
            with open(self.__files, 'r', encoding="utf-8") as file:
                content = file.readlines()
            for i in range(len(content)):
                content[i] = content[i].split(" | ")
                content[i][0] = encode(new_password, decode(old, content[i][0]))
                content[i][1] = encode(new_password, decode(old, content[i][1].rstrip("\n"))) + "\n"
                content[i] = content[i][0] + " | " + content[i][1]
            if len(content) > 0:
                content[-1] = content[-1].rstrip("\n")
            with open(self.__files, 'w', encoding="utf-8") as file:
                file.writelines(content)
        else:
            print("If you have forgotten your password, type 1, type anything else to retry.")
            forgot = input(">>")
            if forgot == "1":
                self.recover_password()
            else:
                self.change_access_password()
            
        
    
# propro = Data()
# propro.change_hashed_password("HELLO")