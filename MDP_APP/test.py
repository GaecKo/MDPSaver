from colorama import Fore, Back, Style, init

init(autoreset=True)
# print(Fore.RED + 'some red text')
# print(Back.GREEN + 'and with a green background')
# print(Style.DIM + 'and in dim text')
# print(Style.RESET_ALL)
# print('back to normal now')

print(
f"""

Hello, this is {Fore.RED + "red text" + Style.RESET_ALL}, and you?
what is your {Fore.BLUE + "fav color"} ?

""")

