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
        print(decrypt(pr.get_key(), content[i].rstrip("\n")))

def calcul_time(nbr_password:int) -> tuple:
    a = time.time()
    generate_password(nbr_password)
    b = time.time()
    print(Fore.GREEN + f" ~> Done [1/2] ({str(round(b-a))} sec)")
    load_data()
    c = time.time()
    print(Fore.GREEN + f" ~> Done [2/2] ({str(round(c-b))} sec)")
    del_file()
    return b-a, c-b

def animation(loadingtext):
    word = list(loadingtext)
    for i in range(0,len(word)):
        lower=word[i-1].lower()
        word[i-1]=lower
        caps=word[i].upper()
        word[i]=caps
        wordstr=''.join(word)
        sys.stdout.write('\r' + wordstr)
        time.sleep(0.3)

def check_key():
    with open("MDPCrypto/key/key.key", 'rb') as f:
        if f.read() == b'':
            generate_salt()

def start_anim(txt):
    ev = threading.Event()
    def _loop(ev, txt):
        while not ev.is_set():
            animation(txt)
    threading.Thread(target=_loop, args=(ev, txt)).start()
    return ev

def write_result(create, load, nbr_password):
    print(
f"""
= = = = = = = = = = = = = = = = = = = = = = = = = = = =
{Fore.GREEN + "Creation" + Style.RESET_ALL} of the {Fore.YELLOW + str(nbr_password) + Style.RESET_ALL} encrypted passwords: {Back.RED + Fore.WHITE + str(round(create, 2)) + Style.RESET_ALL} sec. ~~> ± {Fore.CYAN + str(round((create/nbr_password) * 1000, 3)) + Style.RESET_ALL} ms per password.
{Fore.BLUE + "Loading" + Style.RESET_ALL} of the {Fore.YELLOW + str(nbr_password) + Style.RESET_ALL} encrypted passwords: {Back.RED + Fore.WHITE + str(round(load, 2)) + Style.RESET_ALL} sec. ~~> ± {Fore.CYAN + str(round((load/nbr_password) * 1000, 3)) + Style.RESET_ALL} ms per password.
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

    ev = start_anim(Fore.CYAN + "Loading result" )
    create_time, load_time = calcul_time(nbr)
    ev.set()
    time.sleep(1)
    write_result(create_time, load_time, nbr)
    