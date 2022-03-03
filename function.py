from crypto import encode, decode, hashing
def print_logo():
    with open("logo.txt", 'r') as file:
        print(file.read())

def program_first():
    print("It seems that it's the first time you connect to the system")
    print("Would you like to see a walkthrough of the program?")
    print()
    print(" | (1): Yes")
    print(" | (2): No")
    print()
    print("(type the number of your corresponding choice just after the '>>')")
    choice = int(input(">>"))
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
    create_password()

def tutorial():
    print()
    print("- - - - - - - - - - - - - - - ")
    print("""
    The app lets you choose between 7 options, 
    you can chose one simply by writting the number corresponding to it. 
    
    1) Access my passwords -> Let you access all your password by asking you your main access password.
    -> Once done, you can look after the site you wish to find the password of
    -> Then, you can chose wether you wand to delete it, reveal the password or change the password
    
    2) Change Username -> lets you rename yourself
    
    3) Change Password -> With some verification, you will be able to change your password
    
    4) Tutorial -> You're in ;)
    
    5) Exit the program -> Simply stops the program and make sure everything is fine and ready for next time
    
    If you have any recommendations/tips/bugs, please contact me on discord: GaecKo#7545""")
    
def wanna_do():
    print(
        """
    What do you want to do?
    -----------------------
    | 1) Access my passwords
    | 2) Add a password
    | 3) Change UserName
    | 4) Change Access Password 
    | 5) Tutorial
    | 6) Exit
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

def create_password(returning=False):
    UpLetters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    Numbers = ["0", "1", "2", "3", "4", "5",  "6", "7", "8", "9"]
    print("Your password needs at least 1 number, one upper letter, and a minimum length of 8 characters.")
    print("- - - - - - - - - - - - - - - - - - - - - - \n")
    password = input("password: \n>>")
    upper = False
    numb = False
    for i in password:
        if i in UpLetters:
            upper = True
        if i in Numbers:
            numb = True
    
    if len(password) < 8:
        print("\n Password is only ", len(password), " of lenght, it has to be of 8 characters minimum.")
        create_password()
        return 
    elif upper!= True or numb != True:   
        if upper != True:
            print("\nYour password doesn't include any upper letter, you need at least one")
            create_password()
            return
        elif numb != True:
            print("\nYour password doesn't include any number, you need at least one")
            create_password()
            return
    else:
    # -------------------------------------- Hash of the AP   
        hashed = hashing(password)
        with open("hashed.txt", 'r', encoding="utf-8")as file:
            content = file.readlines()
        try:
            content[0] = hashed + "\n"
        except IndexError:
            content.append(hashed)
        with open('hashed.txt', 'w', encoding="utf-8") as file:
            file.writelines(content)

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
        with open("hashed.txt", 'r', encoding="utf-8") as file:
            content = file.readlines()
        content[0] = content[0].rstrip("\n") + "\n"
        try:
            content[1] = hashed_answer + "\n"
        except IndexError:
            content.append(hashed_answer + "\n")
        with open('hashed.txt', 'w', encoding="utf-8") as file:
            file.writelines(content)
    # -------------------------------------- Encode of the AP with the rep    
        encoded = encode(answer, password)
        with open("hashed.txt", 'r', encoding="utf-8") as file:
            content = file.readlines()
        try:
            content[2] = encoded
        except IndexError:
            content.append(encoded)
        with open("hashed.txt", 'w', encoding="utf-8") as file:
            file.writelines(content)
    # -------------------------------------- Add of the question in default.txt
        with open("default.txt", 'r') as file:
            content = file.readlines()
        content[2] = ("question:"+ question)
        with open("default.txt", 'w') as file:
            file.writelines(content)
        if returning == True:
            return password
        
def option_password():
    print(
    """
    - - - - - - - - - - - - - - - - - - - - - - - -
    You have the possibility to do multiple things;
    | 1) Reveal the password
    | 2) Delete the password
    | 3) Change the password
    | 4) Leave
    
    -----------------------
    What do you wish to do?
    """)
    choice = input(">>")
    try:
        choice = int(choice)
        if choice <= 4:
            return choice
    except:
        print("Invalid choice, please try again.")
        option_password()
    
def choice_sit(number):
    try:
        choice_site = int(input("\nPlease tell the number corresponding to the site you wish to access\n>>"))
        if choice_site > 0 and choice_site <= number:
            return choice_site
    except:
        print("Invalid number, retry")
        choice_sit(number)

def confirm_username(username):
    print("""
    Do you confirm this username: {0}?
    | 1) Yes
    | 2) No
    
    """.format(username))
    one_two = input(">>")
    while one_two != "1" and one_two != "2":
        confirm_username(username)
    if one_two == "1":
        print("Choice confirmed")
        return username
    elif one_two == "2":
        print("Please write down the wanted Username")
        new_username = input("\n>>")
        confirm_username(new_username)

class DataFileCorrupted(Exception):
    def __init__(self, message="data.txt is corrupted, ask for a hard reboot, contact GaecKo#7545"):
        self.message = message
        super().__init__(self.message)

class DefaultFileCorrupted(Exception):
    def __init__(self, message="default.txt is corrupted, ask for a hard reboot, contact GaecKo#7545"):
        self.message = message
        super().__init__(self.message)

class HashedFileCorrupted(Exception):
    def __init__(self, message="hashed.txt is corrupted, ask for a hard reboot, contact GaecKo#7545"):
        self.message = message
        super().__init__(self.message)
    
class MissingFiles(Exception):
    def __init__(self, message= "Missing Files, ask for help, contact GaecKo#7545"):
        self.message = message
        super().__init__(self.message)

class MissingContent(Exception):
    def __init__(self, message= "Missing Content, ask for help, contact GaecKo#7545"):
        self.message = message
        super().__init__(self.message)