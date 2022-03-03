from files import Data
from function import *
from time import sleep
program = Data() # deux créations de classe
        
if __name__ == "__main__":
    
    print_logo()
    print("                 (Press Z + Enter to start)")
    while True:
        if input() in ["Z", "z"]:
            break
    
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    if program.first():
        print("Hello stranger, it seems like it's the first time we see you out here. \nWhat's your username? ")
        program.set_username(input("\n\n>>"))
        print()
        program_first()
    else:
        print("Hello ", program.get_username(), ", you have been connected ", program.get_times_connected(), ' times.')
    program.checkup()
    program.add_one_connection()
    while True:
        print("\n---------------\nPlease give the Access Password to access all of your passwords")
        given_password = input(">>")
        if hashing(given_password) == program.get_hashed_password():
            print("Good password")
            print("\n" * 50)
            break
        else:
            print("bad password, have you forgotten your password? (type 1 if so)")
            print(hashing(given_password) , "|", program.get_hashed_password())
            given_password = input(">>")
            while hashing(given_password) == program.get_hashed_password() or given_password != "1":
                print("bad password, have you forgotten your password? (type 1 if so)")
                given_password = input(">>")
            if given_password == "1":
                given_password = program.recover_password()
                print(given_password)
            else:
                break

    while program.checkup():
        choice = wanna_do()
        if choice == 1:
            if not program.get_props():
                print("You currently have no saved password. Please add one first.")
            else:
                go = False
                while not go:
                    print("Here are all the site registered")
                    liste, number = program.sites_list(given_password)
                    print(liste)
                    while True:
                        try:
                            index = choice_sit(number) - 1
                            site, code = program.search(given_password, index)
                            break
                        except:
                            pass
                    action = option_password()
                    if action == 1:
                        print(("-"*(len(site) + len(code) +3)) + "\n" + site + " | " + code + "\n" + ("-"*(len(site) + len(code) +3)))
                        sleep(2)
                    elif action == 2:
                        program.delete_site(index)
                    elif action == 3:
                        print("You are going to change your password")
                        new_password = input("What's the new password?\n>>")
                        if len(new_password) >= 1:
                            program.change_password_site(choice_sit(number) - 1, given_password, new_password)
                        else:
                            print("Invalid password, retry:")
                            new_password = input("What's the new password?\n>>")
                            program.change_password_site(choice_sit(number) - 1, given_password, new_password)
                    elif action == 4:
                        go = True
            
        if choice == 2:
            print("\n------------------------\nYou are here to add the password of a specific site.")
            site = input("Please tell the name of the site\n>>")
            password = input("Please tell your password of the site\n>>")
            program.add_site_password(given_password, site, password)
        
        if choice == 3:
            print("\n------------------------\nPlease write down your new Username")
            new_username = input("\n>>")
            good_one = confirm_username(new_username)
            program.set_username(good_one)
            print("Here you go {}, your username has been changed.".format(program.get_username()))

        if choice == 4:
            print("\n------------------------\nAccessing Password modification...")
            program.change_access_password()
            given_password = input("- - - - - - - - - - - - - -\nPlease enter new password:\n>>")
       
        if choice == 5:
            tutorial()
        
        if choice == 6:
            print("See you soon {} !".format(program.get_username()))
            break

