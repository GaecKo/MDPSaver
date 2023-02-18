# author: Arthur De Neyer - GaecKo
# last update: check github (https://github.com/GaecKo/MDPSaver)
#           ==== ⚠ DISCLAIMER ⚠ ====
# This code is not suitable for professional use. As of the current state of the code, this 
# whole program is not sustainable and thus depreciated. 
# 
# If you wish to rebuilt the program, feel free to do it and I'll check the PR! 

# This file is used to test the Speed of the program. You can just launch it and it will work. 

from MDPCrypto.Crypt import *
from program import Program, SystemRecovery
import time, threading, os
from colorama import init, Fore, Back, Style

init(autoreset=True)
pr = Program()
sr = SystemRecovery()
global password
password = "Coco1212"

def generate_password(nbr:int):
    content = []
    for _ in range(nbr):
        content.append(encrypt(pr.get_key(), pr.generate_password(3) + " | " + pr.generate_password(3) + " | " + pr.generate_password(3)) + "\n")
    content[-1].rstrip("\n")
    with open("SpeedTest.txt", 'w+', encoding="utf-8") as f:
        f.writelines(content)

def del_file():
    os.remove("SpeedTest.txt")

def load_data():
    with open("SpeedTest.txt", 'r', encoding="utf-8") as f:
        content = f.readlines()
    for i in range(len(content)-1):
        decrypt(pr.get_key(), content[i].rstrip("\n"))

def calcul_time(nbr_password:int) -> tuple:
    a = time.time()
    generate_password(nbr_password)
    b = time.time()
    print(Fore.GREEN + f" ~> Done [1/2] (Encryption: {str(round(b-a, 5))} sec)")
    load_data()
    c = time.time()
    print(Fore.GREEN + f" ~> Done [2/2] (Decryption: {str(round(c-b, 5))} sec)")
    del_file()
    return b-a, c-b

def check_key():
    with open("MDPCrypto/key/key.key", 'rb') as f:
        if f.read() == b'':
            generate_salt()

def write_result(create, load, nbr_password):
    print(
f"""
= = = = = = = = = = = = = = = = = = = = = = = = = = = =
{Fore.GREEN + "Creation" + Style.RESET_ALL} of the {Fore.YELLOW + str(nbr_password) + Style.RESET_ALL} encrypted passwords: {Back.RED + Fore.WHITE + str(round(create, 4)) + Style.RESET_ALL} sec. ~> ± {Fore.CYAN + str(round((create/nbr_password) * 1000, 5)) + Style.RESET_ALL} ms per password.
{Fore.BLUE + "Loading" + Style.RESET_ALL} of the {Fore.YELLOW + str(nbr_password) + Style.RESET_ALL} encrypted passwords: {Back.RED + Fore.WHITE + str(round(load, 4)) + Style.RESET_ALL} sec. ~> ± {Fore.CYAN + str(round((load/nbr_password) * 1000, 5)) + Style.RESET_ALL} ms per password.
Total time: {Fore.RED + str(round(load + create, 2)) + Style.RESET_ALL} sec 
= = = = = = = = = = = = = = = = = = = = = = = = = = = =
""")
    pass

if __name__ == "__main__":
    print(Fore.MAGENTA + "Testing Utility has started.")
    check_key()
    pr.add_key(password)
    while True:
        try:
            nbr = int(input(Fore.YELLOW + "Please tell the number of password you want to test with: \n>>"))
            break
        except:
            print(Back.RED + 'Enter a valid number.')

    create_time, load_time = calcul_time(nbr)
    time.sleep(1)
    write_result(create_time, load_time, nbr)
    
