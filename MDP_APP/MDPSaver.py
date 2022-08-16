from program import *
from MDPCrypto.Crypt import hashing, get_salt, generate_salt
from time import sleep
from MDPLogs.logs import Log
from colorama import Fore, Back, Style, init
import sys, os
import pwinput
from MDPStyle.logo import logo
init(autoreset=True)
os.system('cls')
print("\n" * 200)
logs = Log()
program = Program() 
recovery = SystemRecovery()

if __name__ == "__main__":
    print(logo())
    print(Fore.MAGENTA +"\n(Press Enter to start)")
    input() 
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    try: first = program.first()
    except: recovery.error_resolution(recovery.error()); sys.exit()
    if program.first():
        print("Hello stranger, it seems like it's the first time we see you out here. \nWhat's your username? ")
        program.set_username(input("\n\n>>"))
        print()
        program.program_first()
        logs.create_log("[DAY/MONTH/YEAR | HOUR:MIN (SEC)] ACTION")
        logs.create_log("FIRST TIME CONNECTED, CREATIONS DONE")
        print("\n- - - - Important Note:\n-> Don't leave the program with the right upper red cross in cmd! In case of problems, it won't be possible to fully help you.")
    else:
        error = recovery.error()
        if error != True:
            recovery.error_resolution(error)
            sys.exit("Please restart program.")
        if get_salt() == b'':
            generate_salt()
        print(f"Hello {program.get_username()}, you have been connected {program.get_times_connected()} times.")
        logs.create_log(F"END OF SESSION {program.get_times_connected() - 1}\n\n############################################################\n")
        logs.create_log(F"START OF SESSION {program.get_times_connected()} ({program.get_username()})")
    logs.create_log(F"CHECKUP COMPLETED WITH SUCCESS (nbre connections: {program.get_times_connected()})")
    program.add_one_connection()
    while True:
        print("\n---------------\nPlease give the Access Password to access all of your passwords")
        given_password = pwinput.pwinput(prompt='Password: ')
        if hashing(given_password) == program.get_hashed_password():
            print("Good password")
            print("\n" * 200)
            break
        else:
            print(Back.RED + "Bad password, have you forgotten your password? (type 1 if so)" + Style.RESET_ALL + "")
            given_password = pwinput.pwinput(prompt='Password: ')
            while given_password != "1" and hashing(given_password) != program.get_hashed_password():
                print(Back.RED + "Bad password, have you forgotten your password? (type 1 if so)" + Style.RESET_ALL + "")
                given_password = input(">>")
            if given_password == "1":
                given_password = program.recover_password()
            else:
                print("\n" * 200)
                break
        program.check_data()

    while recovery.error():
        choice = program.wanna_do()
        if choice == 1:
            if not program.get_props():
                print("You currently have no saved password. Please add one first.")
                sleep(1.5)
            else:
                go = False # boucle while not go
                asked = False # used in case of search in the password list
                leave = False # to leave this menu 
                while not go:
                    print(Back.WHITE + " * " + Back.BLUE + " Loading... " + Style.RESET_ALL)
                    liste, number = program.sites_list(given_password)
                    print("\n" * 200)
                    print("Here are all the site registered:")
                    print(liste)
                    while True:
                        if asked == False:
                            index = program.choice_sit(number) 
                        if index == False:
                            leave = True
                            break
                        elif isinstance(index, int) and not isinstance(index, bool):
                            index -= 1
                            print("INDEX HAS BEEN CHANGED!!! Now: ", index)
                            sleep(1.5)
                            site, username, code = program.search(given_password, index)
                            go = True
                            leave = False
                            break
                        elif index == True:
                            choice = 2
                            leave = True
                            go = True
                            break
                        elif isinstance(index, str):
                            sites, indexes = program.search_in_sites(given_password, index)
                            if sites == []:
                                print(f"""No Result found with keyword {Back.WHITE + Fore.BLACK + index + Style.RESET_ALL}, please retry.""")
                                sleep(2.5)
                                leave = True
                                break
                            elif sites == False:
                                leave = True
                                break
                            else:
                                print(F"\n-> Keyword: '{index}'")
                                for i in sites:
                                    print(i)
                                index = program.choice_sit(indexes)
                                asked = True
                        else:
                            leave = True
                            go = True
                            break
                    if leave == True:
                        break
                    action = program.option_password()
                    if action == 1:
                        print(program.print_site_password(site, username, code))
                        print("\t press enter to hide password.")
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
                            print(Back.RED + "Invalid password, retry:" + Style.RESET_ALL + "")
                            new_password = input("What's the new password?\n>>")
                            program.change_password_site(index, given_password, new_password)
                        print("\n" * 200)
                    
                    elif action == 4:
                        print("You are going to change your username / email")
                        new_username = input("What's the new username / email?\n>>")
                        if len(new_username) >= 1:
                            program.change_username_site(index, given_password, new_username)
                        else:
                            print(Back.RED + "Invalid password, retry:" + Style.RESET_ALL + "")
                            new_username = input("What's the new username / email?\n>>")
                            program.change_username_site(index, given_password, new_username)
                    elif action == 5:
                        print("\n" * 200)
                        go = True
                        leave = True
                        break
        
        if choice == 2:
            print("\n------------------------\nYou are here to add the password of a specific site.")
            i = 0
            while True:
                site = input("Please tell the site you want to add a password for\n>>")
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
        
        if choice == 3:
            password = program.generate_password(program.choose_security_level_password())
            print(f"Here is the randomly generated password:\n\n{password}\n\n")
            while True:
                to_save = input("Would you like to add this password to your saved password? " + Fore.CYAN + "[Y/n] " + Style.RESET_ALL )
                if to_save in ["Y", "y", "N", "n"]:
                    if to_save in ["Y", "y"]: to_save = True
                    if to_save in ["N", "n"]: to_save = False
                    break
                print(Back.RED + "Invalid choice, please retry" + Style.RESET_ALL + "")
            if to_save:
                while True:
                    site = input("Please tell the name of the site, enter 'back' or 'stop' or 'retour' to leave.\n>>")
                    if site == "back" or site == "stop" or site == "retour":
                        print("\n" * 200)
                        break
                    username = input("Please tell your username / email on the site\n>>")
                    if username == "back" or username == "stop" or username == "retour":
                        print("\n" * 200)
                        break
                    
                    print("\n" * 200)
                    program.add_site_password(given_password, site, password, username)
                    program.check_data()
                    break
                print("\n"*200)
        
        if choice == 4:
            print("\n------------------------\nPlease write down your new Username")
            new_username = input("\n>>")
            good_one = program.confirm_username(new_username)
            program.set_username(good_one)
            print("\n")
            print(f"Here you go {program.get_username()}, your username has been changed.")

        if choice == 5:
            print("\n------------------------\nAccessing Password modification...")
            program.change_access_password()
            while True:
                given_password = pwinput.pwinput(prompt="- - - - - - - - - - - - - -\nPlease enter new password: ")
                if hashing(given_password) == program.get_hashed_password():
                    print("\n" * 200)
                    break
                else:
                    print(Back.RED + "Wrong password, please try again." + Style.RESET_ALL + "")
       
        if choice == 6:
            program.tutorial() # TODO: Adapt to new param
        
        if choice == 7:
            print(Back.BLUE + f"See you soon {program.get_username()}!")
            sleep(1.5)
            break

        if choice == 8:
            recovery.hard_reboot() 
    
    errors = recovery.error()
    if errors != True:
        recovery.error_resolution(errors)