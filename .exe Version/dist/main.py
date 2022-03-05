from program import *
from crypto import hashing
from time import sleep
from logs import Log
import sys
logs = Log()
program = Program() 

if __name__ == "__main__":
    print_logo()
    print("\n(Press Enter to start)")
    input() 
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    if program.first():
        print("Hello stranger, it seems like it's the first time we see you out here. \nWhat's your username? ")
        program.set_username(input("\n\n>>"))
        print()
        program.program_first()
        logs.create_log("[DAY/MONTH/YEAR | HOUR:MIN (SEC)] ACTION")
        logs.create_log("FIRST TIME CONNECTED, CREATIONS DONE")
        print("\n- - - - Important Note:\n-> Don't leave the program with the right upper red cross in cmd! In case of problems, it won't be possible to fully help you.")
    else:
        error = program.error()
        if error != True:
            program.error_resolution(error)
            sys.exit("Please restart program.")
        print("Hello ", program.get_username(), ", you have been connected ", program.get_times_connected(), ' times.')
        logs.create_log(F"START OF SESSION {program.get_times_connected()}({program.get_username()})")
    logs.create_log(F"CHECKUP COMPLETED WITH SUCCESS (nbre connections: {program.get_times_connected()})")
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
            given_password = input(">>")
            while given_password != "1" and hashing(given_password) != program.get_hashed_password():
                print("bad password, have you forgotten your password? (type 1 if so)")
                given_password = input(">>")
            if given_password == "1":
                given_password = program.recover_password()
            else:
                break

    while program.error():
        choice = wanna_do()
        if choice == 1:
            if not program.get_props():
                print("You currently have no saved password. Please add one first.")
            else:
                go = False
                leave = False
                while not go:
                    print("Here are all the site registered")
                    liste, number = program.sites_list(given_password)
                    print(liste)
                    while True:
                        try:
                            index = choice_sit(number) - 1
                            site, username, code = program.search(given_password, index)
                            go = True
                            break
                        except:
                            leave = True
                            break
                    if leave == True:
                        break
                    action = option_password()
                    if action == 1:
                        print(("-"*(len(site) + len(username) + len(code) +6)) + "\n" + site + " | " + username + " | " + code + "\n" + ("-"*(len(site) + len(username) + len(code) +6)))
                        sleep(2)
                    elif action == 2:
                        program.delete_site(index)
                    elif action == 3:
                        print("You are going to change your password")
                        new_password = input("What's the new password?\n>>")
                        if len(new_password) >= 1:
                            program.change_password_site(index, given_password, new_password)
                        else:
                            print("Invalid password, retry:")
                            new_password = input("What's the new password?\n>>")
                            program.change_password_site(index, given_password, new_password)
                    
                    elif action == 4:
                        print("You are going to change your username / email")
                        new_username = input("What's the new username / email?\n>>")
                        if len(new_username) >= 1:
                            program.change_username_site(index, given_password, new_username)
                        else:
                            print("Invalid password, retry:")
                            new_username = input("What's the new username / email?\n>>")
                            program.change_username_site(index, given_password, new_username)
                    elif action == 5:
                        go = True
            
        if choice == 2:
            print("\n------------------------\nYou are here to add the password of a specific site.")
            site = input("Please tell the name of the site\n>>")
            username = input("Please tell your username / email on the site\n>>")
            password = input("Please tell your password of the site\n>>")
            program.add_site_password(given_password, site, password, username)
        
        if choice == 3:
            print("\n------------------------\nPlease write down your new Username")
            new_username = input("\n>>")
            good_one = confirm_username(new_username)
            program.set_username(good_one)
            print("Here you go {}, your username has been changed.".format(program.get_username()))

        if choice == 4:
            print("\n------------------------\nAccessing Password modification...")
            program.change_access_password()
            while True:
                given_password = input("- - - - - - - - - - - - - -\nPlease enter new password:\n>>")
                if hashing(given_password) == program.get_hashed_password():
                    break
                else:
                    print("Wrong password, please try again.")
       
        if choice == 5:
            tutorial()
        
        if choice == 6:
            print("See you soon {} !".format(program.get_username()))
            break

        if choice == 7:
            program.hard_reboot()
    
    if program.error() != True:
        program.error_resolution(program.error())
    logs.create_log(F"END OF SESSION {program.get_times_connected() - 1}\n\n############################################################\n")

