from random import randint
from crypto import decode, encode, hashing
from logs import Log
from time import sleep
import os
import sys
logs = Log()

def reset_default():
    default = "times_connected:1\nusername:?\nquestion:?\nserial_nbr:?"
    with open("default.txt", 'w', encoding="utf-8") as file:
        file.write(default)
    logs.create_log("DEFAULT WAS RESET")

def reset_hashed():
    default = ""
    with open("hashed.txt", 'w', encoding="utf-8") as file:
        file.write(default)
    logs.create_log("HASHED WAS RESET")
    
def reset_data():
    with open("data.txt", 'w', encoding="utf-8") as file:
        file.write("")
    logs.create_log("DATA WAS RESET")

def create_hashed():
    f = open(os.path.join(os.getcwd(), 'hashed.txt'), 'w')
    f.close()

def create_default():
    f = open(os.path.join(os.getcwd(), 'default.txt'), 'w')
    f.close()

def create_data():
    f = open(os.path.join(os.getcwd(), 'default.txt'), 'w')
    f.close()

def print_logo():
    with open("logo.txt", 'r', encoding="utf-8") as file:
        print(file.read())

def tutorial():
    print()
    print("- - - - - - - - - - - - - - - ")
    print("""
    When you will start the program next time, you will be asked your AP (access password that you will create in a few moments) which defines the password
    that controls all of your password, this password if very powerfull so chose it carefully! If you forgot it, you will be able to recover your other passwords
    by answering a question you are going to create just after this tutorial.

    The app lets you choose between 7 options, 
    you can chose one simply by writting the number corresponding to it. 
    
    1) Access my passwords 
    -> Let you access all your passwords.
    -> Once done, you can look after the site you wish to find the password of
    -> Then, you can chose wether you wand to delete it, reveal the password, change the password or change the username / email
    
    2) Add a password -> a) Add the name of the site (Facebook, Insta,..)
                         b) Add your username / email (username@coolguy.me)
                         c) Add the password of your account 

    3) Change Username -> to rename yourself
    
    4) Change Password -> With some verification, you will be able to change your password
    
    5) Tutorial -> You're in ;)
    
    6) Exit the program -> Simply stops the program and make sure everything is fine and ready for next time

    7) System settings -> To try to debug the programs if troubles went to happen
    
    If you have any recommendations/tips/bugs, please contact me on discord: GaecKo#7545""")
    
def wanna_do():
    print(
        """
    What do you want to do?
    -----------------------
    | 1) Access my passwords           ????????????????????????????????????????????????????????????????????????????????????????????????????????????
    | 2) Add a password                ????????????????????????????????????????????????????????????????????????????????????????????????????????????
    | 3) Change UserName               ????????????????????????????????????????????????????????????????????????????????????????????????????????????
    | 4) Change Access Password        ????????????????????????????????????????????????????????????????????????????????????????????????????????????
    | 5) Tutorial                      ????????????????????????????????????????????????????????????????????????????????????????????????????????????
    | 6) Exit                          ????????????????????????????????????????????????????????????????????????????????????????????????????????????  ????????? ????????? ????????? ????????? ????????? ?????????
    | 7) System Settings                                                     ????????? ????????? ????????? ????????? ????????? ????????? ??
        """
    )
    choice = input(">>")
    try:
        choice = int(choice)
        if choice <= 7:
            return choice
    except:
        print("Invalid choice, please try again.")
        return wanna_do()

def reboot_do():
    print(
        """
    What do you want to do?
    -----------------------
    | 1) Hard Reboot everything
    | 2) Delete all password (= reset data.txt)
    | 3) Reset default.txt (and so hashed.txt)
    | 4) Get help
    | 5) Go back
        """
    )
    choice = input(">>")
    try:
        choice = int(choice)
        if choice <= 6:
            return choice
    except:
        print("Invalid choice, please try again.")
        wanna_do()

def option_password():
    print(
    """
    - - - - - - - - - - - - - - - - - - - - - - - -
    You have the possibility to do multiple things;
    | 1) Reveal the password
    | 2) Delete the password
    | 3) Change the password
    | 4) Change the username / email
    | 5) Leave
    
    -----------------------
    What do you wish to do?
    """)
    choice = input(">>")
    try:
        choice = int(choice)
        if choice <= 5:
            return choice
    except:
        print("Invalid choice, please try again.")
        option_password()
    
def confirm_username(username):
    print("""
    Do you confirm this username: {0}?
    | 1) Yes
    | 2) No
    
    """.format(username))
    one_two = input(">>")
    while one_two != "1" and one_two != "2":
        return confirm_username(username)
    if one_two == "1":
        print("Choice confirmed")
        return username
    elif one_two == "2":
        print("Please write down the wanted Username")
        new_username = input("\n>>")
        return confirm_username(new_username)

class DataFileCorrupted(Exception):
    def __init__(self, message="data.txt is corrupted, ask for a hard reboot, contact GaecKo#7545"):
        self.message = message
        self.attribute = "DataFileCorrupted"
        super().__init__(self.message)
        logs.create_log("DataFileCorrupted Error occured")
    def __str__(self):
        return self.attribute

class DefaultFileCorrupted(Exception):
    def __init__(self, message="default.txt is corrupted, ask for a hard reboot, contact GaecKo#7545"):
        self.message = message
        self.attribute = "DefaultFileCorrupted"
        super().__init__(self.message)
        logs.create_log("DefaultFileCorrupted Error occured")
    def __str__(self):
        return self.attribute

class HashedFileCorrupted(Exception):
    def __init__(self, message="hashed.txt is corrupted, ask for a hard reboot, contact GaecKo#7545"):
        self.message = message
        self.attribute = "HashedFileCorrupted"
        super().__init__(self.message)
        logs.create_log("HashedFileCorrupted Error occured")
    def __str__(self):
        return self.attribute
    
class MissingFiles(Exception):
    def __init__(self, message= "Missing Files, ask for help, contact GaecKo#7545"):
        self.message = message
        self.attribute = "MissingFiles"
        super().__init__(self.message)
        logs.create_log("MissingFiles Error occured")
    def __str__(self):
        return self.attribute

class MissingContentDefault(Exception):
    def __init__(self, message= "Missing Content in default.txt, ask for help, contact GaecKo#7545"):
        self.message = message
        self.attribute = "MissingContentDefault"
        super().__init__(self.message)
        logs.create_log("MissingContentDefault Error occured")
    def __str__(self):
        return self.attribute
    
class MissingContentHashed(Exception):
    def __init__(self, message= "Missing Content in hashed.txt, ask for help, contact GaecKo#7545"):
        self.message = message
        self.attribute = "MissingContentHashed"
        super().__init__(self.message)
        logs.create_log("MissingContentHashed Error occured")
    def __str__(self):
        return self.attribute

class Program:
    def __init__(self):
        self.__files = "data.txt"
        self.__default = "default.txt"
        self.__hashed = "hashed.txt"

    def error(self):
        error = []
        try:
            with open(self.__default, 'r', encoding="utf-8") as file:
                content = file.readlines()
            if content[1].rstrip("\n").split(":")[1] == "?" or content[2].rstrip("\n").split(":")[1] == "?" or content[3].rstrip("\n").split(":")[1] == "?":
                error.append(str(MissingContentDefault()))
        except:
            error.append([str(DefaultFileCorrupted()), str(MissingFiles())])
        try:
            with open(self.__hashed, 'r', encoding="utf-8") as file:
                if len(file.readlines()) != 3:
                    error.append(str(MissingContentHashed()))
        except:
            error.append([str(HashedFileCorrupted()), str(MissingFiles())])
        
        try:
            file = open("data.txt", 'r', encoding="utf-8")
        except:
            error.append([str(DataFileCorrupted()), str(MissingFiles())])
                

        if error != []:
            return error
        return True

    def error_resolution(self, error):
        if error == True:
            return "No problems were seen, if there is something, contact GaecKo#7545"
        troubles = "Here are the problems seen: \n"
        solution = []
        for index, err in enumerate(error):
            if err == "MissingContentDefault":
               troubles += "- MissingContent Error: default.txt may lack of content, program can't run properly.\n"
               solution.append("REPAIR DEFAULT")
            if err == "MissingContentHashed":
               troubles += "- MissingContent Error: hashed.txt lacks of information, program can't run properly.\n"
               solution.append("REPAIR HASHED")
            if err == "HashedFileCorrupted" and error[index + 1] == "MissingFiles":
                troubles += "- HashedFileCorrupted and MissingFiles Error: hashed.txt is missing, program can't run properly."
                solution.append("CREATE HASHED.TXT")
            if err == "DefaultFileCorrupted" and error[index + 1] == "MissingFiles":
                troubles += "- DefaultFileCorrupted and MissingFiles Error: default.txt is missing, program can't run properly."
                solution.append("CREATE DEFAULT.TXT")
            if err == "DataFileCorrupted" and error[index + 1] == "MissingFiles":
                troubles += "- DatatFileCorrupted and MissingFiles Error: data.txt is missing, program can't run properly."
                solution.append("CREATE DATA.TXT")
        print("################################# ERRORS #################################\n\n", troubles)
        for sol in solution:
            if sol == "REPAIR DEFAULT":
                while True:
                    print("------------\nDefault has to be repaired otherwise your passwords will be corrupted and the system not useable.")
                    print("None of your passwords will be lost if you use the same Access Password as before.")
                    choice = input("Do you wish to repair default.txt? (Y/n)")
                    if choice == "Y":
                        reset_default()
                        print("---------\n default.txt has been repaired, you will have to complete informations next time you start the program.")
                        break
                    elif choice == "n":
                        print("Error will occure again. Program won't be useable, contact GaecKo#7545 for help.")
                        break
            if sol == "REPAIR HASHED":
                while True:
                    print("------------\nHashed has to be repaired otherwise your passwords will be corrupted and the system not useable.")
                    print("None of your passwords will be lost if you use the same Access Password as before.")
                    choice = input("Do you wish to repair hashed.txt? (Y/n)")
                    if choice == "Y":
                        reset_hashed()
                        print("hashed.txt has been repaired, you will have to complete informations next time you start the program.")
                        break
                    elif choice == "n":
                        print("Error will occure again. Program won't be useable, contact GaecKo#7545 for help.")
                        break
            if sol == "CREATE HASHED.TXT":
                while True:
                    print("------------\nhashed.txt has to be created, or the program won't run.")
                    print("None of your passwords will be lost if you use the same Access Password as before.")
                    choice = input("Do you wish to create hashed.txt? (Y/n)")
                    if choice == "Y":
                        create_hashed()
                        print("---------\nhashed.txt has been created, you will have to complete informations next time you start the program.")
                        break
                    elif choice == "n":
                        print("Error will occure again. Program won't be useable.")
                        break
            if sol == "CREATE DEFAULT.TXT":
                while True:
                    print("------------\ndefault.txt has to be created, or the program won't run.")
                    print("None of your passwords will be lost if you use the same Access Password as before.")
                    choice = input("Do you wish to create default.txt? (Y/n)")
                    if choice == "Y":
                        create_default()
                        print("---------\ndefault.txt has been created, you will have to complete informations next time you start the program.")
                        break
                    elif choice == "n":
                        print("Error will occure again. Program won't be useable.")
                        break
            if sol == "CREATE DATA.TXT":
                while True:
                    print("------------\ndata.txt has to be created, or the program won't run.")
                    choice = input("Do you wish to create data.txt? (Y/n)")
                    if choice == "Y":
                        create_data()
                        print("---------\ndata.txt has been created, you will have to complete informations next time you start the program.")
                        break
                    elif choice == "n":
                        print("Error will occure again. Program won't be useable.")
                        break

    def hard_reboot(self):
        password = input("Password: \n>>")
        if hashing(password) != self.get_hashed_password():
            print("Wrong Password, please restart system to retry.")
            sys.exit()
        verif_password = input("Confirm password: \n>>")
        if hashing(verif_password) != self.get_hashed_password():
            print("Wrong Password, please restart system to retry.")
            sys.exit()
        print("\n" * 50)
        print("\n\nHere are the specific actions you can do:")
        action = reboot_do()
        if action == 1:
            while True:
                choice = input("Are you sure you want to delete everything?(You will lost all your passwords, ...) (Y/n)")
                if choice == "Y":
                    print("deleting...")
                    reset_data()
                    reset_default()
                    reset_hashed()
                    sys.exit()
                elif choice == "n":
                    break
        if action == 2:
            while True:
                choice = input("Are you sure you want to delete all of your passwords? (Y/n)")
                if choice == "Y":
                    print("deleting...")
                    reset_data()
                elif choice == "n":
                    break
        if action == 3:
            while True:
                choice = input("""Are you sure you want to reset all informations? 
                None of the passwords will be lost if you use the same Access Password as the current one. (Y/n)""")
                if choice == "Y":
                    print("Reseting...")
                    reset_default()
                    reset_hashed()
                    sys.exit()
                elif choice == "n":
                    break
        if action == 4:
            print("You can always contact on discord: GaecKo#9333 and you have the tutorial in the main menu.")
            print("------")
            print("Here are the common issues that could sadly happen due to a program error:")
            print("- My passwords are not readable")
            print("- My question is not readable")
            print("- My password doesn't seem to work")
            print("- Error in my cmd, I don't know what to do")
            print("--> In all these cases, contact me on discord, describe the problem and send me the 'logs.txt' file, which could help me.")
            print("--> After each use, the system gets completely checked and if it contains errors, solutions are given to fix them.")

    def program_first(self):
        print("It seems that it's the first time you connect to the system")
        print("Would you like to see a walkthrough of the program?")
        print()
        print(" | (1): Yes")
        print(" | (2): No")
        print()
        print("(type the number of your corresponding choice just after the '>>')")
        choice = input(">>")
        try:
            choice = int(choice)
        except:
            self.program_first()
            return
        while choice != 1 or choice != 2:
            if choice == 1:
                print("Getting to the tutorial...")
                tutorial()
                break
            elif choice == 2:
                print("Going back to the initial place...")
                break
            print("Would you like to see a walkthrough of the program?")
            print()
            print(" | (1): Oui")
            print(" | (2): Non")
            print()
            choice = int(input(">>"))
        print("\n - - - - - - - - - - - - - - - - - - - - - -\nAs it's the first time you log in, you have to create an access password. ")
        self.create_password()
        logs.create_log("CREATION OF PASSWORD STARTED")
    
    def create_serial_number(self, access_password):
        initial = randint(1000, 1000000)
        added = abs(int(hashing(access_password)))
        logs.create_log("CREATION OF SERIAL NUMBER")
        return str(initial + added)

    def get_props(self):
        with open(self.__files, 'r', encoding="utf-8") as file:
            if file.readlines() == []:
                return False
            else:
                return True
    
    def get_personnal_question(self):
        with open(self.__default, 'r', encoding="utf-8") as file:
            return decode(self.get_serial_number(), file.readlines()[2].split(":")[1].rstrip('\n'))

    def get_first_personnal_question(self):
        with open(self.__default, 'r', encoding="utf-8") as file:
            return file.readlines()[2].split(":")[1].rstrip('\n')

    def get_serial_number(self):
        with open(self.__default, 'r', encoding="utf-8") as file:
            return file.readlines()[3].split(":")[1]

    def get_hashed_password(self):
        with open(self.__hashed, 'r', encoding="utf-8") as file:
            return file.readlines()[0].rstrip("\n")

    def get_hashed_answer(self):
        with open(self.__hashed, 'r', encoding="utf-8") as file:
            return file.readlines()[1].rstrip("\n") 

    def get_times_connected(self):
        with open(self.__default, 'r', encoding="utf-8") as file:
            return int(file.readlines()[0].split(":")[1])
        
    def get_content(self, filetoopen):
        with open(filetoopen, 'r', encoding="utf-8") as file:
            return file.readlines()

    def write_content(self, content, filetoopen):
        """
        pre: content is iterable / filetoopen is existing
        """
        with open(filetoopen, 'w', encoding="utf-8") as file:
            file.writelines(content)

    def encode_question(self, question):
        serial = self.get_serial_number()
        encoded_question = encode(serial, question)
        content = self.get_content(self.__default)
        content[2] = "question:"+ encoded_question + "\n"
        self.write_content(content, self.__default)
        logs.create_log("QUESTION WAS ENCODED")

    def add_site_password(self, access_password, site, site_password, username):
        with open(self.__files, 'r', encoding="utf-8") as file:
            content = file.read()
        if self.get_props():
            content += "\n" + encode(access_password, site) + " | " + encode(access_password, username) + " | " + encode(access_password, site_password)
        else:
            content += encode(access_password, site) + " | " + encode(access_password, username) + " | " +encode(access_password, site_password)
        self.write_content(content, self.__files)
        logs.create_log("SITE AND PASSWORD ADDED")

    def add_one_connection(self):
        times = self.get_times_connected() + 1
        lines = self.get_content(self.__default)
        lines[0] = "times_connected:" + str(times) + "\n"
        self.write_content(lines, self.__default)

    def first(self):
        if self.get_times_connected() == 1:
            logs.create_log("FIRST TIME CONNECTED")
            return True
        return False

    def set_username(self, user_name) -> str:
        lines = self.get_content(self.__default)
        lines[1] = "username:" + user_name + "\n"
        self.write_content(lines, self.__default)
        logs.create_log("USERNAME WAS SET")
        
    def get_username(self):
        with open(self.__default, 'r', encoding="utf-8") as file:
            return file.readlines()[1].split(":")[1].rstrip("\n")

    def search(self, access_password, index):
        content = self.get_content(self.__files)
        logs.create_log("A PASSWORD WAS SHOWN")
        return (decode(access_password, content[index].split(" | ")[0]), decode(access_password, content[index].split(" | ")[1]), decode(access_password, content[index].split(" | ")[2].rstrip("\n")))
    
    def check_data(self):
        content = self.get_content(self.__files)
        passing = False
        nbr = 0
        while passing == False:
            for i in range(len(content)):
                if content[i] == "\n":
                    content.pop(i)
                    nbr += 1
                    break
                if i == len(content) - 1:
                    passing = True      
        self.write_content(content, self.__files)
        logs.create_log(F"DATA FILE WAS CHECKED. FILE HAD {nbr} EMPTY LINES")

    def choice_sit(self, number):
        if isinstance(number, int):
            choice_site = input(F"\nPlease enter a number to access and '+' or {number} to add a password. \n\tYou can type the keyword of a site as well.\n>>")
            try:
                choice_site = int(choice_site)
                if choice_site > 0 and choice_site < number:
                    return choice_site
                elif choice_site == number:
                    return True
            except:
                if choice_site in ["+", "plus", "add", "ajouter", "ajout"]:
                    return True
                if isinstance(choice_site, str):
                    return choice_site
                print("Invalid choice, retry")
                return False
        if isinstance(number, list):
            choice_site = input(F"\nPlease enter a number to access the searched site.\n>>")
            try:
                choice_site = int(choice_site)
                if choice_site > 0 and choice_site - 1 in number:
                    return choice_site
                else:
                    return False
            except:
                return False

    def sites_list(self, access_password):
        content = self.get_content(self.__files)
        text = F"Site: {len(content)} registered. Search by typing the keyword.\n"
        for i in range(len(content)):
            text += "| " + str(i+1) +") " + decode(access_password, content[i].split(" | ")[0]) + "\n"
        return (text, len(content) + 1)
    
    def search_in_sites(self, access_password, keyword):
        if keyword in ["", " ", ".", ","]:
            print("\nInvalid Keyword, retry")
            sleep(2.5)
            return (False, False)
        keyword = keyword.rstrip()
        good_one = []
        indexes = []
        lists, number = self.sites_list(access_password)
        lists = lists.split("\n")[1:]
        bef = [i.upper() for i in(lists[:])]
        for index, line in enumerate(bef):
            if keyword.upper() in line:
                good_one.append(lists[index])
                indexes.append(index)
        return (good_one, indexes)
        
    def delete_site(self, index):
        content = self.get_content(self.__files)
        content.pop(index)
        self.write_content(content, self.__files)
        logs.create_log("A SITE WAS DELETED")
        
    def change_username_site(self, index, access_password, new_username):
        content = self.get_content(self.__files)
        site = content[index].split(" | ")[0] + " | " + encode(access_password, new_username) + " | " + content[index].split(" | ")[2] 
        content[index] = site
        self.write_content(content, self.__files)
        logs.create_log("A SITE USERNAME WAS CHANGED")

    def change_password_site(self, index, access_password, new_password):
        content = self.get_content(self.__files)
        site = content[index].split(" | ")[0] + " | " + content[index].split(" | ")[1] + " | " + encode(access_password, new_password) + "\n"
        content[index] = site
        self.write_content(content, self.__files)
        logs.create_log("A SITE PASSWORD WAS CHANGED")
        
    def change_hashed_password(self, new_access):
        content = self.get_content(self.__hashed)
        content[0] = hashing(new_access) + "\n"
        self.write_content(content, self.__hashed)
        logs.create_log("PASSWORD HASH WAS CHANGED (DUE TO PASSWORD CHANGE)")

    def get_coded_password(self):
        with open(self.__hashed, 'r', encoding='utf-8') as file:
            return file.readlines[2].rstrip("\n")

    def recover_password(self):
        logs.create_log("RECOVERING PASSWORD BEGINNED")
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
                return self.recover_password()
        print("Good answer! \n")
        old_password = decode(answer, self.get_coded_password())
        print("Please create a new password and a new question.")
        logs.create_log("CREATION OF PASSWORD STARTED")
        new = self.create_password(True)
        self.change_hashed_password(new)
        self.change_encoded_data(old_password, new)
        logs.create_log("RECOVERING PASSWORD SUCCESS")
        return new
    
    def change_encoded_data(self, old, new):
        content = self.get_content(self.__files)
        for i in range(len(content)):
            content[i] = content[i].split(" | ")
            content[i][0] = encode(new, decode(old, content[i][0]))
            content[i][1] = encode(new, decode(old, content[i][1]))
            content[i][2] = encode(new, decode(old, content[i][2].rstrip("\n"))) + "\n"
            content[i] = content[i][0] + " | " + content[i][1] + " | " + content[i][2]
        if len(content) > 0:
            content[-1] = content[-1].rstrip("\n")
        self.write_content(content, self.__files)

    def change_access_password(self):
        def wrong_password():
            print("Wrong Password, if you have forgotten your password, type 1, type anything else to retry.")
            forgot = input(">>")
            if forgot == "1":
                self.recover_password()
            else:
                self.change_access_password()
        logs.create_log("CHANGING ACCESS PASSWORD")
        old = input("Old password:\n>>")
        if hashing(old) != self.get_hashed_password():
            wrong_password()
            return
        old_verif = input("Confirm Old password\n>>")
        if hashing(old_verif) == self.get_hashed_password():
            print("\n")
            new_password = self.create_password(True)
            self.change_encoded_data(old_verif, new_password)
        else:
            print("Wrong Password, if you have forgotten your password, type 1, type anything else to retry.")
            forgot = input(">>")
            if forgot == "1":
                self.recover_password()
            else:
                self.change_access_password()
        logs.create_log("CHANGING PASSWORD SUCCESS")

    def create_password(self, returning=False):
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        Numbers = ["0", "1", "2", "3", "4", "5",  "6", "7", "8", "9"]
        print("Your password needs at least 1 number, one upper letter, and a minimum length of 8 characters.")
        print("- - - - - - - - - - - - - - - - - - - - - - \n")
        password = input("password: \n>>")
        upper = False
        numb = False
        for i in password:
            if i in letters:
                upper = True
            if i in Numbers:
                numb = True
        if len(password) < 8:
            print("\n Password is only ", len(password), " of lenght, it has to be of 8 characters minimum.")
            return self.create_password()
        elif upper!= True or numb != True:   
            if upper != True:
                print("\nYour password doesn't include any upper letter, you need at least one")
                return self.create_password()
                
            elif numb != True:
                print("\nYour password doesn't include any number, you need at least one")
                return self.create_password()
        else:
        # -------------------------------------- Hash of the AP   
            hashed = hashing(password)
            content = self.get_content(self.__hashed)
            try:
                content[0] = hashed + "\n"
            except IndexError:
                content.append(hashed)
            self.write_content(content, self.__hashed)

        # -------------------------------------- Creation of the Q? + Answer
            print("\n- - - - - - - - - - - - - - - - - - - - - - ")
            print("Access password validated, it will now be your access key to all of your passwords")
            print("If you forgot your password, you will have the opportunity to answer a personnal question that you have to create now.\n")
            print("Please create a question:")
            question = input(">>")
            print("----")
            print("Now the answer:")
            answer = input(">>")
        # -------------------------------------- Hash of the rep
            hashed_answer = hashing(answer)
            content = self.get_content(self.__hashed)
            content[0] = content[0].rstrip("\n") + "\n"
            try:
                content[1] = hashed_answer + "\n"
            except IndexError:
                content.append(hashed_answer + "\n")
            self.write_content(content, self.__hashed)
        # -------------------------------------- Encode of the AP with the rep    
            encoded = encode(answer, password)
            content = self.get_content(self.__hashed)
            try:
                content[2] = encoded
            except IndexError:
                content.append(encoded)
            self.write_content(content, self.__hashed)
        # -------------------------------------- Create the serial number
            content = self.get_content(self.__default) 
            content[3] = "serial_nbr:" + self.create_serial_number(password)
            self.write_content(content, self.__default)
        # -------------------------------------- Add of the question in default.txt
            content = self.get_content(self.__default)
            content[2] = "question:"+ question + "\n"
            self.write_content(content, self.__default)
            self.encode_question(self.get_first_personnal_question())
            logs.create_log("CREATION OF PASSWORD ENDED")
            if returning == True:
                return password