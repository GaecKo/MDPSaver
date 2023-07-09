# author: Arthur De Neyer - GaecKo
# last update: check github (https://github.com/GaecKo/MDPSaver)
#           ==== ⚠ DISCLAIMER ⚠ ====
# This code is not suitable for professional use. As of the current state of the code, this 
# whole program is not sustainable and thus depreciated. 
# 
# If you wish to rebuilt the program, feel free to do it and I'll check the PR! 

# A video is coverring this part (with use of a .exe file): https://youtu.be/y8biYrRKB9s

from program import *
from MDPCrypto.Crypt import *
from MDPLogs.logs import Log
from colorama import Fore, init, Style, Back
import time, pwinput, sys

init(autoreset=True)
program = Program()
logs = Log()

def check_data_encrypt(password) -> bool:
    """
    return True if it is already updated to new version
    return False if not
    """
    with open("MDPData/data.txt", "r", encoding="utf-8") as f:
        test = f.readlines()[0].rstrip("\n")
    return try_decrypt(program.get_key(), test)

def convert_data(password):
    with open("MDPData/data.txt", 'r', encoding="utf-8") as f:
        content = f.readlines()
    for index, line in enumerate(content):
        # "dhadhzaç | fbnezpfhz^p | fnepafa," -> "nfd^zjZ¨HFGZ RGJ¨ZEJ  	EJF¨Z   E"
        line = line.split(" | ")
        site, username, paswd = decode(password, line[0]), decode(password, line[1]), decode(password, line[2].rstrip("\n"))
        content[index] = encrypt(program.get_key(), site + " | " + username + " | " + paswd) + "\n"
    content[-1].rstrip("\n")
    with open("MDPData/data.txt", "w", encoding="utf-8") as f:
        f.writelines(content)

def encode(key, plain_text):
	enc = []
	for i, e in enumerate(plain_text):
		key_c = key[i % len(key)]
		enc_c = chr((ord(e) + ord(key_c)) % 256)
		enc.append(enc_c)
	return "".join(enc)

def decode(key, cipher_text):
	dec = []
	for i, e in enumerate(cipher_text):
		key_c = key[i % len(key)]
		dec_c = chr((256 + ord(e) - ord(key_c)) % 256)
		dec.append(dec_c)
	return str("".join(dec))

if __name__ == "__main__":
    print(Fore.CYAN + "Welcome to Updator." + Style.RESET_ALL + " Only use this if you want to convert your data from old MDPSaver version to the new one.")
    logs.create_log("Update tool started!")
    if get_salt() == b'':
        generate_salt()
    while True:
        password = pwinput.pwinput(prompt="Password: ")
        try:
            saved_password = program.get_hashed_password()
        except:
            print(Fore.MAGENTA + "Program has no information about you.")
            print(Fore.CYAN + "Are you sure you have moved your old files into the new folders correctly?")
            print(Fore.RED + "Update couldn't be completed. Try moving your old files again.")
            time.sleep(8)
            sys.exit()
        if low_hash(password) == saved_password:
            print(Fore.GREEN + "Good Password!")
            program.add_key(password)
            break
        if hashing(password) == saved_password:
            print(Fore.MAGENTA + "It seems like it is already working. Update already done.")
            print("You can use the program! Your password should be working!")
            sys.exit()
        else:
            print(Back.RED +  "Wrong Password, please retry." + Style.RESET_ALL)
    
    updated = check_data_encrypt(password)
    if updated == True and low_hash(password) == program.get_hashed_password():
        print(Fore.CYAN + "it seems like you need to update your personnal info...")
        program.change_access_password(True)
        print(Back.GREEN + "Program has successfully been updated!")
        logs.create_log("Data was already updated but not personnal info.")
        sys.exit()
    elif updated == True:
        print(Fore.MAGENTA + "It seems like it is already working. Update already done.")
        print("You can use the program! Your password should be working!")
        sys.exit()
    elif updated == False:
        logs.create_log("Updating Data...                                   [0/2]")
        print(Fore.BLUE + "Update can be done.")
        print(Fore.BLUE + "Converting data", end='')
        time.sleep(0.5)
        print(Fore.BLUE + ".", end='')
        time.sleep(0.5)
        print(Fore.BLUE + ".", end='')
        time.sleep(0.5)
        print(Fore.BLUE + ".", end='')
        convert_data(password)
        print(Fore.GREEN + "Data has been updated to new encrypting method!")
        logs.create_log("Data converted to new encrypting method!           [1/2]")
        print(Fore.RED + "You need to reset your password for program to work (You can use the exact same info as before)")
        program.change_access_password(True)
        print(Back.GREEN + "Program has successfully been updated!")
        logs.create_log("Personnal info (hashed.txt) has been updated!      [2/2]")
        time.sleep(4)
        sys.exit()