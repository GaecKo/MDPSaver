from program import *
from MDPCrypto.Crypt import hashing
from time import sleep
from Logs.logs import Log
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
        logs.create_log(F"END OF SESSION {program.get_times_connected() - 1}\n\n############################################################\n")
        logs.create_log(F"START OF SESSION {program.get_times_connected()} ({program.get_username()})")
    logs.create_log(F"CHECKUP COMPLETED WITH SUCCESS (nbre connections: {program.get_times_connected()})")
    program.add_one_connection()
    while True:
        print("\n---------------\nPlease give the Access Password to access all of your passwords")
        given_password = input(">>")
        if hashing(given_password) == program.get_hashed_password():
            print("Good password")
            print("\n" * 200)
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
                print("\n" * 200)
                break
        program.check_data()

    while program.error():
        try:
            if index != True:
                choice = wanna_do()
        except:
            choice = wanna_do()
        if choice == 1:
            if not program.get_props():
                print("You currently have no saved password. Please add one first.")
                sleep(2)
            else:
                go = False
                leave = False
                asked = False
                hardleave = False
                while not go:
                    print("Here are all the site registered")
                    liste, number = program.sites_list(given_password)
                    print(liste)
                    while True:
                        if asked == False:
                            index = program.choice_sit(number) 
                        if index == False:
                            leave = True
                            break
                        elif isinstance(index, int):
                            index -= 1
                            site, username, code = program.search(given_password, index)
                            go = True
                            leave = False
                            break
                        elif index == True:
                            choice = 2
                            leave = True
                            break
                        elif isinstance(index, str):
                            sites, indexes = program.search_in_sites(given_password, index)
                            if sites == []:
                                print(F"No Result found with keyword '{index}', please retry.")
                                sleep(2.5)
                                hardleave = True
                                break
                            elif sites == False:
                                hardleave = True
                                break
                            else:
                                print(F"\n-> Keyword: '{index}'")
                                for i in sites:
                                    print(i)
                                index = program.choice_sit(indexes)
                                asked = True
                        else:
                            leave = True
                            break
                    if leave == True:
                        break
                    if hardleave == True:
                        print("\n" * 200)
                        break
                    action = option_password()
                    if action == 1:
                        print(("-"*(len(site) + len(username) + len(code) +6)) + "\n" + site + " | " + username + " | " + code + "\n" + ("-"*(len(site) + len(username) + len(code) +6)))
                        print("\n\t press enter to hide password.")
                        enter = input()
                        print("\n" * 200)
                    elif action == 2:
                        program.delete_site(index)
                        print("\n" * 200)
                    elif action == 3:
                        print("You are going to change your password")
                        new_password = input("What's the new password?\n>>")
                        if len(new_password) >= 1:
                            program.change_password_site(index, given_password, new_password)
                        else:
                            print("Invalid password, retry:")
                            new_password = input("What's the new password?\n>>")
                            program.change_password_site(index, given_password, new_password)
                        print("\n" * 200)
                    
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
            
        elif choice == 2:
            print("\n------------------------\nYou are here to add the password of a specific site.")
            i = 0
            while True:
                try:
                    if index == True:
                        choice = 1
                except: pass
                site = input("Please tell the name of the site, enter 'back' or 'stop' or 'retour' to leave.\n>>")
                if site == "back" or site == "stop" or site == "retour":
                    print("\n" * 200)
                    break
                username = input("Please tell your username / email on the site\n>>")
                if username == "back" or username == "stop" or username == "retour":
                    print("\n" * 200)
                    break
                password = input("Please tell your password of the site\n>>")
                if password == "back" or password == "stop" or password == "retour":
                    print("\n" * 200)
                    break
                print("\n" * 200)
                program.add_site_password(given_password, site, password, username)
                program.check_data()
                break
        
        elif choice == 3:
            print("\n------------------------\n")

            pass
        
        elif choice == 4:
            print("\n------------------------\nPlease write down your new Username")
            new_username = input("\n>>")
            good_one = confirm_username(new_username)
            program.set_username(good_one)
            print("Here you go {}, your username has been changed.".format(program.get_username()))

        elif choice == 5:
            print("\n------------------------\nAccessing Password modification...")
            program.change_access_password()
            while True:
                given_password = input("- - - - - - - - - - - - - -\nPlease enter new password:\n>>")
                if hashing(given_password) == program.get_hashed_password():
                    print("\n" * 200)
                    break
                else:
                    print("Wrong password, please try again.")
       
        elif choice == 6:
            tutorial() # TODO: Adapt to new param
        
        elif choice == 7:
            print("See you soon {} !".format(program.get_username()))
            sleep(2.5)
            break

        elif choice == 8:
            program.hard_reboot() 
    
    if program.error() != True:
        program.error_resolution(program.error())
