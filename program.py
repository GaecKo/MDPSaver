#################################################################################################
#   | Author:       Arthur De Neyer - GaecKo                                                    #
#   | Last update:  Check github (https://github.com/GaecKo/MDPSaver)                           #
#                                                                                               #
#                               ======= ⚠ DISCLAIMER ⚠ ======                                  #
#   | This code is not suitable for professional use. As of the current state of the code, this #
#       whole program is not sustainable and thus deprecated.                                   #
#                                                                                               #
#   | If you wish to rebuild the program, feel free to do it and I'll check the PR!             #
#                                                                                               #
#################################################################################################

import	re

from		random		import	randint
from		time 			import	sleep
from		pwinput		import	pwinput

from		MDPCrypto.Crypt	import 	*
from		MDPLogs.logs	import 	Log

init(autoreset=True)
os.system("cls")

rs	= Style.RESET_ALL
LOGS	= Log()

class Program:
	def __init__(self):
		self.__data		= "MDPData/data.txt"
		self.__default 	= "MDPData/default.txt"
		self.__hashed 	= "MDPData/hashed.txt"

	def add_key(self, access_password):
		self.__key = load_key(access_password)
		LOGS.create_log("Key was loaded successfully")

	def tutorial(self):
		print(
			f"""\n
	The app lets you choose between 8 options, 
	you can chose one simply by writting the number corresponding to it. 
	
	1) {Back.LIGHTBLUE_EX + "Access my passwords" + rs}
	-> Let you access all your passwords.
	-> Once done, you can look after the site you wish to find the password of
	-> Then, you can chose wether you wand to delete it, reveal the password, change the password or change the username / email
	
	2) {Back.LIGHTBLUE_EX + "Add a password" + rs} -> a) Add the name of the site (Facebook, Insta,..)
						b) Add your username / email (username@coolguy.me)
						c) Add the password of your account 
	
	3) {Back.LIGHTBLUE_EX + "Filter Search" + rs} -> Search for all site with a given username-email / password corresponding. 

	4) {Back.LIGHTBLUE_EX + "Generate a random password" + rs} -> a) {Fore.GREEN + "Weak password" + rs} (only letters + numbers | size 8~12)
									b) {Fore.YELLOW + "Medium password" + rs} (letters + numbers + symbols | size 10~20)
									c) {Fore.MAGENTA + "Strong password" + rs} (long + letters + numbers + symbols | size 15~25)
									d) {Fore.CYAN + "Custom password" + rs} (choose caracteristics)
								-> You will then be able to save it if you wish so!

	5) {Back.LIGHTBLUE_EX + "Change Username" + rs} -> to rename yourself
	
	6) {Back.LIGHTBLUE_EX + "Change Password" + rs} -> With some verification, you will be able to change your password
	
	7) {Back.LIGHTBLUE_EX + "Tutorial" + rs} -> You're in ;)
	
	8) {Back.LIGHTBLUE_EX + "Exit the program" + rs} -> Simply stops the program and make sure everything is fine and ready for next time

	9) {Back.LIGHTBLUE_EX + "System settings" + rs} -> To try to debug the programs if troubles went to happen
	
	If you have any {Fore.CYAN + "recommendations" + rs}/{Fore.GREEN + "tips" + rs}/{Fore.RED + "bugs" + rs}, please contact me on discord: GaecKo#7545
		"""
		)
		input("\tPress Enter to continue.")

	def wanna_do(self):
		saved = self.get_number_of_saved_passwords()

		if saved > 1:
			stri = f"""~> {Fore.RED + str(saved)} saved passwords""" + rs + "!"

		elif saved == 1:
			stri = f"""~> {Fore.RED + str(saved)} saved password""" + rs + "!"

		else:
			stri = ""

		L = Fore.MAGENTA + "|" + rs
		B = " - - - - - - - - - - - - - -"

		print(
			f"""
	{B}
	{L} 1) {Fore.BLUE + "Access" + rs} my Passwords                                        
	{L} 2) {Fore.GREEN + "Add" + rs} a Password {Fore.LIGHTGREEN_EX + "+" + rs}               {Fore.LIGHTRED_EX + "╭━╮╭━┳━━━┳━━━╮╭━━━┳━━━┳╮╱╱╭┳━━━┳━━━╮" + rs}
	{L} 3) {Fore.MAGENTA + "Filter" + rs} Search                  {Fore.LIGHTRED_EX + "┃┃╰╯┃┣╮╭╮┃╭━╮┃┃╭━╮┃╭━╮┃╰╮╭╯┃╭━━┫╭━╮┃" + rs}
	{L} 4) {Fore.CYAN + "Generate" + rs} Random Password       {Fore.LIGHTRED_EX + "┃╭╮╭╮┃┃┃┃┃╰━╯┃┃╰━━┫┃╱┃┣╮┃┃╭┫╰━━┫╰━╯┃" + rs}
	{L} 5) Change UserName {Fore.YELLOW + "/..." + rs}           {Fore.LIGHTRED_EX + "┃┃┃┃┃┃┃┃┃┃╭━━╯╰━━╮┃╰━╯┃┃╰╯┃┃╭━━┫╭╮╭╯" + rs}
	{L} 6) Change Access Password {Fore.LIGHTRED_EX + "***" + rs}     {Fore.LIGHTRED_EX + "┃┃┃┃┃┣╯╰╯┃┃╱╱╱┃╰━╯┃╭━╮┃╰╮╭╯┃╰━━┫┃┃╰╮" + rs}
	{L} 7) Tutorial / Help {Fore.LIGHTCYAN_EX + "?" + rs}              {Fore.LIGHTRED_EX + "╰╯╰╯╰┻━━━┻╯╱╱╱╰━━━┻╯╱╰╯╱╰╯╱╰━━━┻╯╰━╯" + rs}
	{L} 8) Exit {Fore.RED + "->/" + rs}                         {stri}
	{L} 9) System Settings
	{B}
	"""
		)
		choice = input(">> ")
		try:
			choice = int(choice)

			if choice <= 9:
				return choice
			
		except:
			print(Back.RED + "Invalid choice, please try again.")
			self.clear_stdout()
			return self.wanna_do()

	def choose_security_level_password(self) -> int:
		print(
			f"""
	- - - - - - - - - - - - - - - - - - - - - - - -
	Please choose a security level: 
	| 1) {Fore.GREEN + "Weak password" + rs} (only letters + numbers | size 8~12)
	| 2) {Fore.YELLOW + "Medium password" + rs} (letters + numbers + symbols | size 10~20)
	| 3) {Fore.MAGENTA + "Strong password" + rs} (long + letters + numbers + symbols | size 15~25)
	| 4) {Fore.CYAN + "Custom password" + rs} (choose caracteristics)
	"""
		)
		security_level = input("\n>> ")
		if security_level in "backretourexitquitter":
			return None
		
		try:
			security_level = int(security_level)
			if security_level < 5 and security_level > 0:
				return security_level
			
			print(Back.RED + "Invalid choice, please retry")
			sleep(1.5)
			return self.choose_security_level_password()
		
		except:
			print(Back.RED + "Invalid choice, please retry")
			sleep(1.5)
			return self.choose_security_level_password()

	def generate_password(self, security_level: int) -> str:
		if security_level == None:
			return None

		def generator(
			min_size: int, max_size: int, symbols: bool = True, numbers: bool = True
		) -> str:
			char = [	
					['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], 
		   			['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], 
					["0", "1", "2", "3", "4", "5",  "6", "7", "8", "9"],
            			["&", "#", "_", "@", "!", "?", ".", ";", "/", "§", "=", "<", ">"]
				]
			generated_password 	= ""
			password_size 		= randint(min_size, max_size)

			if not numbers:
				del char[2]

			if not symbols:
				del char[-1]

			for _ in range(password_size):
				char_category = randint(0, len(char) - 1)
				if randint(1, 2) == 1:
					generated_password += char[char_category][
						randint(0, len(char[char_category]) - 1)
					].upper()

				else:
					generated_password += char[char_category][
						randint(0, len(char[char_category]) - 1)
					].lower()

			return generated_password

		if security_level == 1:
			return generator(8, 12, False)

		elif security_level == 2:
			return generator(10, 20)

		elif security_level == 3:
			return generator(18, 30)

		elif security_level == 4:
			while True:
				try:
					size = int(
						input("\nPlease tell the size you want for the password:\n>> ")
					)
					break
				except:
					print(Back.RED + "Invalid choice, please retry" + rs)

			while True:
				symbols = input(
					f"""\nDo you wish to have symbols included? {Fore.CYAN +"[Y/n]" + rs} """
				)

				if symbols in ["Y", "y", "N", "n"]:
					if symbols in ["Y", "y"]:
						symbols = True

					else:
						symbols = False

					break
				print(Back.RED + "Invalid choice, please retry")

			while True:
				numbers = input(
					f"""\nDo you wish to have numbers included? {Fore.CYAN +"[Y/n]" + rs} """
				)

				if numbers in ["Y", "y", "N", "n"]:
					if numbers in ["Y", "y"]:
						numbers = True

					else:
						numbers = False

					break
				print(Back.RED + "Invalid choice, please retry")

			return generator(size, size, symbols, numbers)

	def option_password(self, site):
		self.clear_stdout()
		print(
			f"""
	- - - - - - - - - - - - - - - - - - - - - - - -
	What do you wish to do with site '{Fore.GREEN + site + rs}'?
	| 1) {Fore.CYAN + "Reveal" + rs} the password
	| 2) {Fore.RED + "Delete" + rs} the password
	| 3) Change the {Fore.MAGENTA + "password" + rs} 
	| 4) Change the {Fore.CYAN + "username / email" + rs} 
	| 5) Leave
	-----------------------
			"""
		)
		choice = input(">> ")
		try:
			choice = int(choice)

			if choice <= 5 and choice > 0:
				return choice
			
			print(Back.RED + "Invalid choice, please try again." + rs)

			sleep(1)
			
			return self.option_password(site)
		
		except:
			print(Back.RED + "Invalid choice, please try again." + rs)

			sleep(1)

			return self.option_password(site)

	def confirm_username(self, username):
		print(
			f"""
	Do you confirm this username: {username}?
	| 1) {Fore.GREEN + "Yes" + rs}
	| 2) {Fore.RED + "No" + rs}
		
			"""
		)
		one_two = input(">> ")

		while one_two != "1" and one_two != "2":
			return self.confirm_username(username)
		
		if one_two == "1":
			print("Choice confirmed")
			return username
		
		elif one_two == "2":
			print("Please write down the wanted Username")
			new_username = input("\n>> ")
			return self.confirm_username(new_username)

	def program_first(self):
		if get_salt() == b"":
			generate_salt()

		print("It seems that it's the first time you connect to the system")
		print("Would you like to see a walkthrough of the program?")
		print()
		print(f""" | (1): {Fore.GREEN + "Yes"}""")
		print(f""" | (2): {Fore.RED + "No"}""")
		print()
		print("(type the number of your corresponding choice just after the '>> ')")

		choice = input(">> ")

		try:
			choice = int(choice)

		except:
			self.program_first()
			return
		
		while choice != 1 or choice != 2:
			if choice == 1:
				print("Getting to the tutorial...")
				sleep(1)
				print("\n" * 50)

				self.tutorial()

				print(
					f"When you will start the program next time, you will be asked your AP (access password that you will create in a few moments)\nwhich defines the password that controls all of your password, this password if very powerfull so choose it carefully!\n>> If you forget it, you will be able to recover your other passwords by answering a question you are going to create just after this tutorial."
				)

				break

			elif choice == 2:
				print("Going back to the initial place...")
				break

			print("Would you like to see a walkthrough of the program?")
			print()
			print(f""" | (1): {Fore.GREEN + "Yes"}""")
			print(f""" | (2): {Fore.RED + "No"}""")
			print()
			choice = int(input(">> "))

		print(
			f"""\n - - - - - - - - - - - - - - - - - - - - - -\nAs it's the first time you log in, you have to create an {Fore.GREEN + "access password" + rs}. """
		)

		# create password
		self.create_password()

		LOGS.create_log("CREATION OF SALT FOR CRYPTO")
		LOGS.create_log("CREATION OF PASSWORD STARTED")

		print(
			"\n- - - - Important Note:\n-> Don't leave the program with the right upper red cross in cmd! In case of "
			"problems, it won't be possible to fully help you."
		)

	def create_serial_number(self, access_password):
		initial 	= randint(1000, 1000000)
		added 	= abs(int(low_hash(access_password)))

		LOGS.create_log("CREATION OF SERIAL NUMBER")
		return str(initial + added)

	def get_props(self):
		with open(self.__data, "r", encoding="utf-8") as file:
			if file.readlines() == []:
				return False
			
			else:
				return True

	def get_key(self):
		return self.__key

	def get_number_of_saved_passwords(self):
		content = self.get_content(self.__data)
		return len(content)

	def get_personnal_question(self):
		with open(self.__default, "r", encoding="utf-8") as file:
			return decrypt_extern_password(
				self.get_serial_number(), 
				file.readlines()[2].split(":")[1].rstrip("\n")
			)

	def get_first_personnal_question(self):
		with open(self.__default, "r", encoding="utf-8") as file:
			return file.readlines()[2].split(":")[1].rstrip("\n")

	def get_serial_number(self):
		with open(self.__default, "r", encoding="utf-8") as file:
			return file.readlines()[3].split(":")[1]

	def get_hashed_password(self):
		with open(self.__hashed, "r", encoding="utf-8") as file:
			return file.readlines()[0].rstrip("\n")

	def get_hashed_answer(self):
		with open(self.__hashed, "r", encoding="utf-8") as file:
			return file.readlines()[1].rstrip("\n")

	def get_times_connected(self):
		with open(self.__default, "r", encoding="utf-8") as file:
			return int(file.readlines()[0].split(":")[1])

	def get_content(self, filetoopen):
		with open(filetoopen, "r", encoding="utf-8") as file:
			return file.readlines()

	def get_coded_password(self):
		with open(self.__hashed, "r", encoding="utf-8") as file:
			return file.readlines()[2].rstrip("\n")

	def get_username(self):
		with open(self.__default, "r", encoding="utf-8") as file:
			return file.readlines()[1].split(":")[1].rstrip("\n")

	def write_content(self, content: list, filetoopen: str):
		"""
		pre: content is iterable / filetoopen is existing
		"""
		with open(filetoopen, "w", encoding="utf-8") as file:
			file.writelines(content)

	def encrypt_question(self, question):
		serial 		= self.get_serial_number()
		encryptd_question = encrypt_extern_password(serial, question)
		content 		= self.get_content(self.__default)
		content[2] 		= "question:" + encryptd_question + "\n"

		self.write_content(content, self.__default)
		LOGS.create_log("QUESTION WAS ENCRYPTED")

	def add_site_password(self, access_password, site, site_password, username):
		with open(self.__data, "r", encoding="utf-8") as file:
			content = file.read()

		if self.get_props():
			content += "\n" + encrypt(
				self.__key, site + " | " + username + " | " + site_password
			)

		else:
			content += encrypt(
				self.__key, site + " | " + username + " | " + site_password
			)

		self.write_content(content, self.__data)
		LOGS.create_log("SITE AND PASSWORD ADDED")

	def add_one_connection(self):
		times 	= self.get_times_connected() + 1
		lines 	= self.get_content(self.__default)
		lines[0] 	= "times_connected:" + str(times) + "\n"

		self.write_content(lines, self.__default)

	def first(self):
		if self.get_times_connected() == 1:
			LOGS.create_log("FIRST TIME CONNECTED")
			return True
		
		return False

	def set_username(self, user_name) -> str:
		lines 	= self.get_content(self.__default)
		lines[1] 	= "username:" + user_name + "\n"

		self.write_content(lines, self.__default)
		LOGS.create_log("USERNAME WAS SET")

	def search(self, access_password, index):
		content 	= self.get_content(self.__data)
		line 		= decrypt(self.__key, content[index]).rstrip("\n").split(" | ")

		LOGS.create_log("A PASSWORD WAS SHOWN")
		return line[0], line[1], line[2]

	def check_data(self):
		content 	= self.get_content(self.__data)
		passing 	= False
		nbr 		= 0

		while passing == False:
			if len(content) == 0:
				break

			for i in range(len(content)):
				if content[i] == "\n":
					content.pop(i)
					nbr += 1
					break
				if i == len(content) - 1:
					passing = True

		self.write_content(content, self.__data)
		LOGS.create_log(f"DATA FILE WAS CHECKED. FILE HAD {nbr} EMPTY LINES")

	def print_site_password(self, site, username, password):
		stri = "    " + f"""{Fore.WHITE + "_" + rs}""" * (
			len(site) + len(username) + len(password) + 8
		)
		stri += f"""\n   {Fore.WHITE + "|" + rs} {site} {Fore.WHITE + "|" + rs} {username} {Fore.WHITE + "|" + rs} {password} {Fore.WHITE + "|" + rs}\n"""
		stri += "    " + f"""{Fore.WHITE + "‾" + rs}""" * (
			len(site) + len(username) + len(password) + 8
		)

		return stri
		"""
		 __________________________________
		| HelloWorld | UserName | Password |
		 ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
		"""

	def choice_sit(self, number):
		if isinstance(number, int):
			choice_site = input(
				f"""\t\t   Press {Fore.RED + "enter" + rs} to leave\nPlease enter a number to access and '{Fore.GREEN + "+" +rs}' or '{Fore.GREEN + str(number) +rs}' to {Fore.GREEN + "add" + rs} a password. \n\tYou can type the {Fore.BLUE + "keyword" + rs} of a site as well.\n>> """
			)

			try:
				choice_site = int(choice_site)
				if choice_site > 0 and choice_site < number:
					return choice_site
				
				elif choice_site == number:
					return True
				
			except:
				if choice_site in ["+"]:
					return True
				
				if isinstance(choice_site, str):
					return choice_site
				
				print(Back.RED + "Invalid choice, retry" + rs)
				return False
			
		if isinstance(number, list):
			choice_site = input(
				f"\nPlease enter a number to access the searched site.\n>> "
			)

			try:
				choice_site = int(choice_site)
				if choice_site > 0 and choice_site - 1 in number:
					return choice_site
				else:
					print(Back.RED + "Selected number not in the given site." + rs)
					sleep(1.5)
					return False
				
			except:
				print(Back.RED + "Please enter a valid number, retry." + rs)
				sleep(1.5)
				return False

	def sites_list(self, access_password):
		content 	= self.get_content(self.__data)
		text 		= f"""Site: {Fore.MAGENTA + str(len(content)) + rs} registered. {Fore.BLUE + "Search" + rs} by typing the keyword.\n"""

		for i in range(len(content)):
			line = decrypt(self.__key, content[i].rstrip("\n")).split(" | ")
			text += Fore.MAGENTA + "| " + rs + str(i + 1) + ") " + line[0] + "\n"

		return (text, len(content) + 1)

	def hide_password(self, password: str) -> str:
		if len(password) < 4 and len(password) > 1:
			return "*" + password[1:]
		
		elif len(password) == 1:
			return password
		
		password 		= list(password)
		n_chars 		= (len(password) // 2) + 1
		replaced_index 	= set()

		for i in range(n_chars):
			random_index = randint(0, len(password) - 1)
			while random_index in replaced_index:
				random_index = randint(0, len(password) - 1)

			replaced_index.add(random_index)
			password[random_index] = "*"

		return "".join(password)

	def highlight_keyword(self, keyword: str, text: str) -> str:
		return re.sub(
			keyword,
			lambda m: Fore.BLUE + m.group(0) + Style.RESET_ALL,
			text,
			flags=re.IGNORECASE,
		)

	def passwords_content(self):
		content	= self.get_content(self.__data)
		indexes 	= []
		good_ones 	= []
		types 	= ["Email-Username", "password"]

		print(
			f"""Search with?\n\t(1) {Fore.MAGENTA + " Email" + rs} - {Fore.MAGENTA + "Username" + rs } \n\t(2) {Fore.MAGENTA + " Password" + rs}\n"""
		)

		search_choice = None

		while search_choice not in ["1", "2"]:
			print("Please choose between (1, 2).")
			search_choice = input(">>")
			if search_choice == "":
				return (False, False)

		type_search 	= types[int(search_choice) - 1]
		type_search_index = int(search_choice)

		print(
			f"""Please enter the keyword to find corresponding {Fore.MAGENTA + type_search + rs}"""
		)

		keyword = ""
		while keyword in ["", " ", ".", ","]:
			print("Keyword (has to be valid):")
			if type_search == "password":
				keyword = pwinput(prompt=">>")

			else:
				keyword = input(">>")

		self.clear_stdout()

		for i in range(len(content)):
			line = decrypt(self.__key, content[i].rstrip("\n"))
			if keyword.upper() in line.split(" | ")[type_search_index].upper():
				good_ones.append(line)
				indexes.append(i + 1)

		if type_search_index == 2:
			hidden_password = self.hide_password(keyword)
			for i in range(len(good_ones)):
				pass_content = good_ones[i].split(" | ")
				good_ones[i] = f"""{Fore.MAGENTA + "|" + rs } {indexes[i]}) {pass_content[0]} | {Fore.MAGENTA + ".. " +  hidden_password + " .." + rs}"""

			print(
				f"""-> Password Filter : '{Fore.BLUE + hidden_password + rs}' ~ {len(good_ones)} result(s)"""
			)

		else:
			for i in range(len(good_ones)):
				pass_content = good_ones[i].split(" | ")
				good_ones[i] = f"""{Fore.MAGENTA + "|" + rs } {indexes[i]}) {pass_content[0]} | {self.highlight_keyword(keyword, pass_content[type_search_index])} """

			print(
				f"""-> {type_search} Filter : '{Fore.BLUE + keyword + rs}' ~ {len(good_ones)} result(s)"""
			)

		LOGS.create_log(f"{type_search.upper()} USED TO SEARCH AND FILTER SITES")
		return (good_ones, indexes)

	def search_in_sites(self, access_password, keyword):
		if keyword in ["", " ", ".", ","]:
			return (False, False)
		
		keyword 		= keyword.rstrip()
		good_one 		= []
		indexes 		= []
		lists, number 	= self.sites_list(access_password)
		lists 		= lists.split("\n")[1:]
		bef 			= [i.upper() for i in (lists[:])]

		for index, line in enumerate(bef):
			if keyword.upper() in line:
				good_one.append(lists[index])
				indexes.append(index)

		return (good_one, indexes)

	def delete_site(self, index):
		content = self.get_content(self.__data)
		content.pop(index)

		self.write_content(content, self.__data)
		self.check_data()
		LOGS.create_log("A SITE WAS DELETED")

	def change_username_site(self, index, access_password, new_username):
		content 		= self.get_content(self.__data)
		line 			= decrypt(self.__key, content[index]).split(" | ")
		line[1] 		= new_username
		line 			= encrypt(self.__key, " | ".join(line))
		content[index] 	= line + "\n"

		self.write_content(content, self.__data)
		self.check_data()
		LOGS.create_log("A SITE USERNAME WAS CHANGED")

	def change_password_site(self, index, access_password, new_password):
		content 		= self.get_content(self.__data)
		line 			= decrypt(self.__key, content[index]).split(" | ")
		line[2] 		= new_password
		line 			= encrypt(self.__key, " | ".join(line))
		content[index] 	= line + "\n"

		self.write_content(content, self.__data)
		self.check_data()
		LOGS.create_log("A SITE PASSWORD WAS CHANGED")

	def change_hashed_password(self, new_access):
		content 	= self.get_content(self.__hashed)
		content[0]	= hashing(new_access) + "\n"

		self.write_content(content, self.__hashed)
		LOGS.create_log("PASSWORD HASH WAS CHANGED (DUE TO PASSWORD CHANGE)")

	def recover_password(self):
		LOGS.create_log("RECOVERING PASSWORD BEGINNED")
		print("\n -------+-------+-------+-------")

		while True:
			print(
				"Please give the answer of your personnal question: (if you don't know it, contact ´gaecko´ on Discord)"
			)
			print("- - - - - - -")
			print(self.get_personnal_question())
			print("---")
			answer = input("answer: \n>> ")
			if hashing(answer) == self.get_hashed_answer():
				break
			else:
				print(Back.RED + "You didn't give the good answer, please retry" + rs)
				return self.recover_password()
			
		print(Fore.GREEN + "Good answer!\n" + rs)

		old_password = decrypt_extern_password(answer, self.get_coded_password())

		print("Please create a new password and a new question.")

		LOGS.create_log("CREATION OF PASSWORD STARTED")

		new = self.create_password(True)
		self.change_hashed_password(new)
		self.change_encryptd_data(old_password, new)

		LOGS.create_log("RECOVERING PASSWORD SUCCESS")
		print(Back.GREEN + "PLEASE RESTART THE PROGRAM. " + rs)

		sleep(3)
		sys.exit()

	def change_encryptd_data(self, old, new):
		content = self.get_content(self.__data)
		for i in range(len(content)):
			content[i] = (
				encrypt_extern_password(new, decrypt_extern_password(old, content[i]))
				+ "\n"
			)

		if len(content) > 0:
			content[-1] = content[-1].rstrip("\n")

		self.write_content(content, self.__data)

	def change_access_password(self, from_updator=False):
		def wrong_password():
			print(
				Back.RED
				+ "Wrong Password, if you have forgotten your password, type 1, type anything else to retry."
				+ rs
			)

			forgot = input(">> ")
			if forgot == "1":
				self.recover_password()

			else:
				self.change_access_password()

		LOGS.create_log("CHANGING ACCESS PASSWORD")

		if from_updator:
			old = pwinput(prompt="\nOld Password: ")

			if low_hash(old) != self.get_hashed_password():
				wrong_password()
				return
			
			old_verif = pwinput(prompt="Confirm Old Password: ")
			if low_hash(old_verif) == self.get_hashed_password():
				print(
					f"""\n{Fore.MAGENTA + "You can use the same password and question as before!"}"""
				)

				new_password = self.create_password(True)
				self.change_encryptd_data(old_verif, new_password)

		else:
			old = pwinput(prompt="\nOld Password: ")

			if hashing(old) != self.get_hashed_password():
				wrong_password()
				return
			
			old_verif = pwinput(prompt="Confirm Old Password: ")

			if hashing(old_verif) == self.get_hashed_password():
				print("\n")
				new_password = self.create_password(True)
				self.change_encryptd_data(old_verif, new_password)

			else:
				wrong_password()
		LOGS.create_log("CHANGING PASSWORD SUCCESS")

	def create_password(self, returning=False):
		letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
		Numbers = ["0", "1", "2", "3", "4", "5",  "6", "7", "8", "9"]

		print(
			f"""Your password needs at least {Fore.RED + "1 number" + rs}, {Fore.RED + "1 upper letter" + rs}, and a minimum length of {Fore.RED + "8 characters" + rs}."""
		)

		while True:
			password = pwinput(prompt="Password: ")
			confirm_password = pwinput(prompt="Confirm Password: ")
			if password == confirm_password:
				break
			else:
				print(
					f"""\n{Back.RED + "Passwords are differents! Please retry." + rs} \n"""
				)

		upper = False
		numb 	= False

		for i in password:
			if i in letters:
				upper = True
			if i in Numbers:
				numb = True
			if numb and upper: break 

		if len(password) < 8:
			print(
				f"""\n{Fore.RED + "Password is only " + str(len(password)) + " of lenght, it has to be of 8 characters minimum." + rs}"""
			)

			return self.create_password(returning)
		
		elif upper != True or numb != True:
			if upper != True:
				print(
					f"""\n{Fore.RED + "Your password doesn't include any upper letter, you need at least one" + rs}"""
				)

				return self.create_password(returning)

			elif numb != True:
				print(
					f"""\n{Fore.RED + "Your password doesn't include any number, you need at least one" + rs}"""
				)

				return self.create_password(returning)
		else:
			# -------------------------------------- Hash of the AP
			hashed 	= hashing(password)
			content 	= self.get_content(self.__hashed)

			try:
				content[0] = hashed + "\n"

			except IndexError:
				content.append(hashed)

			self.write_content(content, self.__hashed)

			# -------------------------------------- Creation of the Q? + Answer
			print("\n- - - - - - - - - - - - - - - - - - - - - - ")
			print(
				"Access password validated, it will now be your access key to all of your passwords"
			)
			print(
				f"If you {Fore.RED + 'forget' + Fore.RESET} your password, you will have the opportunity to {Fore.GREEN + 'answer' + Fore.RESET} a personnal question that you have to create now.\n"
			)

			print("Please create a question:")
			question = input(">> ")

			print("----")
			print("Now the answer:")
			answer = input(">> ")

			self.clear_stdout()
			# -------------------------------------- Hash of the rep
			hashed_answer 	= hashing(answer)
			content 		= self.get_content(self.__hashed)
			content[0] 		= content[0].rstrip("\n") + "\n"

			try:
				content[1] = hashed_answer + "\n"

			except IndexError:
				content.append(hashed_answer + "\n")

			self.write_content(content, self.__hashed)

			# -------------------------------------- encrypt of the AP with the rep
			encryptd 	= encrypt_extern_password(answer, password)
			content 	= self.get_content(self.__hashed)

			try:
				content[2] = encryptd

			except IndexError:
				content.append(encryptd)

			self.write_content(content, self.__hashed)

			# -------------------------------------- Create the serial number
			content 	= self.get_content(self.__default)
			content[3] 	= "serial_nbr:" + self.create_serial_number(password)

			self.write_content(content, self.__default)

			# -------------------------------------- Add the question in default.txt
			content 	= self.get_content(self.__default)
			content[2] 	= "question:" + question + "\n"

			self.write_content(content, self.__default)
			self.encrypt_question(self.get_first_personnal_question())
			
			LOGS.create_log("CREATION OF PASSWORD ENDED")

			if returning == True:
				return password

	def clear_stdout(self):
		if "win32" in sys.platform:
			os.system("cls")

		else:
			os.system("clear")


class SystemRecovery:
	class DataFileCorrupted(Exception):
		def __init__(
			self,
			message="data.txt is corrupted, ask for a hard reboot, contact GaecKo#7545",
		):
			self.message 	= message
			self.attribute 	= "DataFileCorrupted"

			super().__init__(self.message)
			LOGS.create_log("DataFileCorrupted Error occured")

		def __str__(self):
			return self.attribute

	class DefaultFileCorrupted(Exception):
		def __init__(
			self,
			message="default.txt is corrupted, ask for a hard reboot, contact GaecKo#7545",
		):
			self.message 	= message
			self.attribute 	= "DefaultFileCorrupted"

			super().__init__(self.message)
			LOGS.create_log("DefaultFileCorrupted Error occured")

		def __str__(self):
			return self.attribute

	class HashedFileCorrupted(Exception):
		def __init__(
			self,
			message="hashed.txt is corrupted, ask for a hard reboot, contact GaecKo#7545",
		):
			self.message 	= message
			self.attribute 	= "HashedFileCorrupted"

			super().__init__(self.message)
			LOGS.create_log("HashedFileCorrupted Error occured")

		def __str__(self):
			return self.attribute

	class MissingFiles(Exception):
		def __init__(self, message="Missing Files, ask for help, contact GaecKo#7545"):
			self.message 	= message
			self.attribute 	= "MissingFiles"

			super().__init__(self.message)
			LOGS.create_log("MissingFiles Error occured")

		def __str__(self):
			return self.attribute

	class MissingContentDefault(Exception):
		def __init__(
			self,
			message="Missing Content in default.txt, ask for help, contact GaecKo#7545",
		):
			self.message 	= message
			self.attribute 	= "MissingContentDefault"

			super().__init__(self.message)
			LOGS.create_log("MissingContentDefault Error occured")

		def __str__(self):
			return self.attribute

	class MissingContentHashed(Exception):
		def __init__(
			self,
			message="Missing Content in hashed.txt, ask for help, contact GaecKo#7545",
		):
			self.message 	= message
			self.attribute 	= "MissingContentHashed"

			super().__init__(self.message)
			LOGS.create_log("MissingContentHashed Error occured")

		def __str__(self):
			return self.attribute

	class KeyFileCorrupted(Exception):
		def __init__(self, message="Missing key.key file"):
			self.message 	= message
			self.attribute 	= "KeyFileCorrupted"

			super().__init__(self.message)
			LOGS.create_log("KeyFileCorrupted Error occured")

		def __str__(self):
			return self.attribute

	def __init__(self):
		self.__default 	= "MDPData/default.txt"
		self.__hashed 	= "MDPData/hashed.txt"
		self.__key 		= "MDPCrypto/key/key.key"
		self.__data 	= "MDPData/data.txt"

	def reset_default(self):
		default = "times_connected:1\nusername:?\nquestion:?\nserial_nbr:?"

		with open(self.__default, "w", encoding="utf-8") as file:
			file.write(default)

		LOGS.create_log("DEFAULT WAS RESET")

	def reset_hashed(self):
		default = ""

		with open(self.__hashed, "w", encoding="utf-8") as file:
			file.write(default)

		LOGS.create_log("HASHED WAS RESET")

	def reset_key(self):
		default = ""

		with open(self.__key, "w", encoding="utf-8") as file:
			file.write(default)

		LOGS.create_log("KEY.KEY WAS RESET")

	def reset_data(self):
		with open(self.__data, "w", encoding="utf-8") as file:
			file.write("")

		LOGS.create_log("DATA WAS RESET")

	def create_hashed(self):
		f = open(self.__hashed, "w+")
		f.close()

		LOGS.create_log("HASHED WAS CREATED")

	def create_default(self):
		f = open(self.__default, "w+")
		f.close()

		LOGS.create_log("DEFAULT WAS CREATED")

	def create_data(self):
		f = open(self.__data, "w+")
		f.close()

		LOGS.create_log("DATA WAS CREATED")

	def create_key(self):
		f = open(self.__key, "w+")
		f.close()

		LOGS.create_log("KEY.KEY WAS CREATED")

	def get_hashed_password(self):
		with open(self.__hashed, "r", encoding="utf-8") as file:
			return file.readlines()[0].rstrip("\n")

	def reboot_do(self):
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
		choice = input(">> ")
		try:
			choice = int(choice)
			if choice <= 6:
				return choice
			
		except:
			print(Back.RED + "Invalid choice, please try again.")
			return self.reboot_do()

	def error(self):
		error = []

		try:
			with open(self.__default, "r", encoding="utf-8") as file:
				content = file.readlines()
			if (
				content[1].rstrip("\n").split(":")[1] == "?"
				or content[2].rstrip("\n").split(":")[1] == "?"
				or content[3].rstrip("\n").split(":")[1] == "?"
			):
				error.append(str(self.MissingContentDefault()))

		except:
			error.append([str(self.DefaultFileCorrupted()), str(self.MissingFiles())])

		try:
			with open(self.__hashed, "r", encoding="utf-8") as file:
				if len(file.readlines()) != 3:
					error.append(str(self.MissingContentHashed()))

		except:
			error.append([str(self.HashedFileCorrupted()), str(self.MissingFiles())])

		try:
			with open(self.__key, "rb") as file:
				content = file.read()

		except:
			error.append([str(self.KeyFileCorrupted()), str(self.MissingFiles())])

		try:
			file = open(self.__data, "r", encoding="utf-8")

		except:
			error.append([str(self.DataFileCorrupted()), str(self.MissingFiles())])

		if error != []:
			return error
		
		return True

	def error_resolution(self, error):
		if error == True:
			return "No problems were seen, if there is something, contact 'gaecko' on Discord"
		
		troubles = "Here are the problems seen: \n"
		solution = []

		for index, err in enumerate(error):
			if err == "MissingContentDefault":
				troubles += "- MissingContent Error: default.txt may lack of content, program can't run properly.\n"
				solution.append("REPAIR DEFAULT.TXT")

			if err == "MissingContentHashed":
				troubles += "- MissingContent Error: hashed.txt lacks of information, program can't run properly.\n"
				solution.append("REPAIR HASHED.TXT")

			if err == ["HashedFileCorrupted", "MissingFiles"]:
				troubles += "- HashedFileCorrupted and MissingFiles Error: hashed.txt is missing, program can't run properly. \n"
				solution.append("CREATE HASHED.TXT")

			if err == ["DefaultFileCorrupted", "MissingFiles"]:
				troubles += "- DefaultFileCorrupted and MissingFiles Error: default.txt is missing, program can't run properly. \n"
				solution.append("CREATE DEFAULT.TXT")

			if err == ["DataFileCorrupted", "MissingFiles"]:
				troubles += "- DatatFileCorrupted and MissingFiles Error: data.txt is missing, program can't run properly. \n"
				solution.append("CREATE DATA.TXT")

			if err == ["KeyFileCorrupted", "MissingFiles"]:
				troubles += "- KeyFileCorrupted and MissingFiles Error: key.key is missing, program can't run properly.\n"
				solution.append("CREATE KEY.KEY")

		print(
			Back.RED
			+ "################################# ERRORS #################################"
			+ rs
			+ "\n\n",
			troubles,
		)

		for lines in troubles.split("\n")[:-1]:
			LOGS.create_log(lines.lstrip("- "))

		for sol in solution:
			if sol == "REPAIR DEFAULT.TXT":
				while True:
					print(
						"------------\nDefault has to be repaired otherwise your passwords will be corrupted and the system not useable."
					)

					print(
						f"""{Fore.MAGENTA + "None of your passwords will be lost if you use the same Access Password as before."}"""
					)

					choice = input(
						f"""Do you wish to repair default.txt? {Fore.CYAN + "[Y/n]" + rs} """
					)

					if choice == "Y":
						self.reset_default()
						print(
							"---------\n default.txt has been repaired, you will have to complete informations next time you start the program."
						)

						LOGS.create_log("default.txt has been repaired")
						break

					elif choice == "n":
						print(
							Back.RED
							+ "Error will occure again. Program won't be useable, contact GaecKo#7545 for help."
							+ rs
						)

						LOGS.create_log("default.txt has not been repaired")
						break

			if sol == "REPAIR HASHED.TXT":
				while True:
					print(
						"------------\nHashed has to be repaired otherwise your passwords will be corrupted and the system not useable."
					)

					print(
						Fore.MAGENTA
						+ "None of your passwords will be lost if you use the same Access Password as before."
					)

					choice = input(
						"Do you wish to repair hashed.txt? " + Fore.CYAN + "[Y/n] " + rs
					)

					if choice == "Y":
						self.reset_hashed()
						print(
							"hashed.txt has been repaired, you will have to complete informations next time you start the program."
						)

						LOGS.create_log("hashed.txt has been repaired")
						break

					elif choice == "n":
						print(
							Back.RED
							+ "Error will occure again. Program won't be useable, contact GaecKo#7545 for help."
							+ rs
						)

						LOGS.create_log("hashed.txt has not been repaired")
						break

			if sol == "CREATE HASHED.TXT":
				while True:
					print(
						"------------\nhashed.txt has to be created, or the program won't run."
					)

					print(
						Fore.MAGENTA
						+ "None of your passwords will be lost if you use the same Access Password as before."
					)

					choice = input(
						"Do you wish to create hashed.txt? " + Fore.CYAN + "[Y/n] " + rs
					)

					if choice == "Y":
						self.create_hashed()
						print(
							"---------\nhashed.txt has been created, you will have to complete informations next time you start the program."
						)

						LOGS.create_log("hashed.txt has been created")
						break

					elif choice == "n":
						print(
							Back.RED
							+ "Error will occure again. Program won't be useable."
							+ rs
						)

						LOGS.create_log("hashed.txt has not been created")
						break

			if sol == "CREATE DEFAULT.TXT":
				while True:
					print(
						"------------\ndefault.txt has to be created, or the program won't run."
					)

					print(
						Fore.MAGENTA
						+ "None of your passwords will be lost if you use the same Access Password as before."
					)

					choice = input(
						f"""Do you wish to create default.txt? {Fore.CYAN + "[Y/n]" + rs} """
					)

					if choice == "Y":
						self.create_default()
						self.reset_default()
						print(
							"---------\ndefault.txt has been created, you will have to complete informations next time you start the program."
						)

						LOGS.create_log("default.txt has been created")
						break

					elif choice == "n":
						print(
							Back.RED
							+ "Error will occure again. Program won't be useable."
							+ rs
						)

						LOGS.create_log("default.txt has not been created")
						break

			if sol == "CREATE DATA.TXT":
				while True:
					print(
						"------------\ndata.txt has to be created, or the program won't run."
					)

					choice = input(
						"Do you wish to create data.txt? " + Fore.CYAN + "[Y/n] " + rs
					)

					if choice == "Y":
						self.create_data()
						print(
							"---------\ndata.txt has been created, you will have to complete informations next time you start the program."
						)

						LOGS.create_log("data.txt has been created")
						break

					elif choice == "n":
						print(
							Back.RED
							+ "Error will occure again. Program won't be useable."
							+ rs
						)

						LOGS.create_log("data.txt has not been created")
						break

			if sol == "CREATE KEY.KEY":
				while True:
					print(
						"------------\nkey.key has to be created, or the program won't run."
					)

					choice = input(
						"Do you wish to create key.key? " + Fore.CYAN + "[Y/n] " + rs
					)

					if choice == "Y":
						self.create_key()
						print("---------\nkey.key has been created.")
						LOGS.create_log("key.key has been created")
						break

					elif choice == "n":
						print(
							Back.RED
							+ "Error will occure again. Program won't be useable."
							+ rs
						)

						LOGS.create_log("key.key has not been created")
						break

	def system_settings(self):
		password = pwinput(prompt="Password: ")

		if hashing(password) != self.get_hashed_password():
			print(Back.RED + "Wrong Password, please restart system to retry." + rs)
			sys.exit()

		verif_password = pwinput(prompt="Confirm password: ")

		if hashing(verif_password) != self.get_hashed_password():
			print(Back.RED + "Wrong Password, please restart system to retry." + rs)
			sys.exit()

		print("\n" * 50)
		print("\n\nHere are the specific actions you can do:")
		action = self.reboot_do()

		if action == 1:
			while True:
				choice = input(
					f"""{Back.RED + "Are you sure you want to delete everything? You will loose all your passwords "+ rs  + Fore.CYAN + "[Y/n]" + rs} """
				)

				if choice == "Y":
					print("deleting...")
					self.reset_data()
					self.reset_default()
					self.reset_hashed()
					self.reset_key()
					sys.exit()

				elif choice == "n":
					break

		if action == 2:
			while True:
				choice = input(
					f"""{Back.RED + "Are you sure you want to delete all your passwords? "  + rs +Fore.CYAN + "[Y/n]" + rs} """
				)

				if choice in ["Y", "y"]:
					print("deleting...")
					self.reset_data()
					sys.exit()

				elif choice in ["N", "n"]:
					break

		if action == 3:
			while True:
				choice = input(
					f"""Are you sure you want to reset all informations? {Back.RED + "You will loose all your passwords " +rs + Fore.CYAN + "[Y/n]" + rs} """
				)

				if choice in ["Y", "y"]:
					print("Reseting...")
					self.reset_default()
					self.reset_hashed()
					sys.exit()

				elif choice == ["n", "N"]:
					break

		if action == 4:
			print(
				"You can always contact on discord: GaecKo#9333 and you have the tutorial in the main menu."
			)

			print("------")
			print(
				"Here are the common issues that could sadly happen due to a program error:"
			)

			print("- My passwords are not readable")
			print("- My question is not readable")
			print("- My password doesn't seem to work")
			print("- Error in my cmd, I don't know what to do")

			print(
				"--> In all these cases, contact me on discord, describe the problem and send me the 'logs.txt' file, which could help me."
			)

			print(
				"--> After each use, the system gets completely checked and if it contains errors, solutions are given to fix them."
			)
		if action == 5:
			return
