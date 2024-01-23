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

import 	os
import	sys

from		pwinput			import 	pwinput						# hide prompt package
from		time			import	sleep						# sleep
from		colorama		import	Fore, Back, Style, init		# color in stdout

from		MDPStyle.logo	import	logo						# app logo 
from		program			import	*							# controller


init(autoreset=True)											# Initialize Colorama


LOGS 		= Log()
program 	= Program()											# Initialize Log and Program instances
recovery 	= SystemRecovery()

if __name__ == "__main__":
	
	program.clear_stdout()
	print(logo())												# Logo printing
	print(Fore.MAGENTA + "\n(Press Enter to start)")
	input()
	print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")

	
	try:
		first = program.first()									# check & try for program first launch

	except:
		recovery.error_resolution(recovery.error())				# system recovery
		sys.exit()

	if first:
		print(
			f"""Hello stranger, it seems like it's the first time we see you out here. \nWhat's your {Fore.BLUE + "username" + rs}? """
		)
		
		program.set_username(input("\n\n>> "))							# set username
		print()
		
		program.program_first()											# launch user initialization

		LOGS.create_log("[DAY/MONTH/YEAR | HOUR:MIN (SEC)] ACTION")		# LOGS initialization
		LOGS.create_log("FIRST TIME CONNECTED, CREATIONS DONE")

	else:
		LOGS.create_log(												# add log of last session: 
			f"END OF SESSION {program.get_times_connected() - 1}\n\n"
			f"############################################################\n"
		)

		error = recovery.error()
		if error != True: 												# error = ["..."] if has errors, true otherwise
			recovery.error_resolution(error)
			sys.exit("Please restart program.")

		if get_salt() == b"": 											# no current salt
			generate_salt()

		print(
			f"Hello {program.get_username()}, you have been connected {program.get_times_connected()} times."
		)
		
		LOGS.create_log(
			f"START OF SESSION {program.get_times_connected()} ({program.get_username()})"
		)

	LOGS.create_log(													# end of initialization (both for first time and login)
		f"CHECKUP COMPLETED WITH SUCCESS (nbre connections: {program.get_times_connected()})"
	)
	program.add_one_connection()
															
	while True:															# Retrieve Access Password
		print(
			f"""\n---------------\nPlease give the {Fore.BLUE + "Access Password" + Style.RESET_ALL} to access all of your passwords"""
		)
		given_password = pwinput(prompt="Password: ")

		if hashing(given_password) == program.get_hashed_password():					# check if password is correct
			print("Good password")
			program.clear_stdout()
			break

		else:
			while (																		# allow password recovery by entering 1 as input
				given_password != "1"
				and hashing(given_password) != program.get_hashed_password()
			):
				print(
					Back.RED
					+ "Bad password, have you forgotten your password? (type 1 if so)"	# wrong password
					+ Style.RESET_ALL
					+ ""
				)

				given_password = pwinput(prompt="Password: ")

			if given_password == "1": 													# password recovery
				given_password = program.recover_password()

			else:																		# password is the good one!
				program.clear_stdout()				
				break			
	
	program.add_key(given_password)														# load key using the correct given password
	program.check_data()

	while recovery.error():																# infinite loop for menu. Each iteration checks for any 
		program.clear_stdout()															# system error in order to prevent system failure
		choice = program.wanna_do()

		if choice == 1:																	# access password function
			if not program.get_props():													# no password! 
				print("You currently have no saved password. Please add one first.")
				sleep(1.5)
			else:
				go 		= False															# loop while not go
				asked 	= False															# used in case of search in the password list
				leave 	= False															# to leave this menu

				while not go:
					print(
						Back.BLUE
						+ " Loading... "
						+ Style.RESET_ALL
					)

					liste, number = program.sites_list(given_password)					# retrieve list of sites
					print("\nHere are all the site registered:")
					print(liste)

					while True:															# select site / search
						if asked == False:
							index = program.choice_sit(number)

						if index == False:
							leave = True
							break

						elif isinstance(index, int) and not isinstance(index, bool):		# selected site, will show its menu later
							index -= 1
							site, username, code = program.search(							# retrieve site info
								given_password, index
							)	

							go 		= True
							leave	= False
							break

						elif index == True:													# Add a password
							choice 	= 2
							leave	= True
							go 		= True
							break

						elif isinstance(index, str):										# search for site
							sites, indexes = program.search_in_sites(				
								given_password, index
							)

							if sites == []:													# no sites
								print(
									f"""No Result found with keyword {Back.WHITE + Fore.BLACK + index + Style.RESET_ALL}, please retry."""
								)
								sleep(2.5)
								leave = True
								break

							elif sites == False:											# empty search field
								leave = True
								break

							else:															# show corresponding sites
								print(
									f"\n-> Keyword: '{Fore.BLUE + str(index) + Style.RESET_ALL}'"
								)

								for i in sites:
									print(i)

								index = program.choice_sit(indexes)
								asked = True

						else:
							leave 	= True
							go 		= True
							break

					if leave == True:
						break
					
						
					action = program.option_password(site)					# site has been selected, now we open site option menu

					if action == 1:											# show password
						print(program.print_site_password(site, username, code))

						print("\t Press Enter to hide password.")
						enter = input()
						
					elif action == 2:										# delete site
						program.delete_site(index)

					elif action == 3:										# change site password
						print("You are going to change your password")
						new_password = input("What's the new password?\n>> ")

						if len(new_password) >= 1:
							program.change_password_site(
								index, given_password, new_password
							)
						else:
							print(
								Back.RED
								+ "Invalid password, retry:"
								+ Style.RESET_ALL
								+ ""
							)
							new_password = input("What's the new password?\n>> ")
							program.change_password_site(
								index, given_password, new_password
							)

					elif action == 4:										# change site username
						print("You are going to change your username / email")
						new_username = input("What's the new username / email?\n>> ")

						if len(new_username) >= 1:
							program.change_username_site(
								index, given_password, new_username
							)
						else:
							print(
								Back.RED
								+ "Invalid password, retry:"
								+ Style.RESET_ALL
								+ ""
							)
							new_username = input(
								"What's the new username / email?\n>> "
							)

							program.change_username_site(
								index, given_password, new_username
							)

					elif action == 5:										# go back
						program.clear_stdout()
						go 		= True
						leave	= True
						break

				program.clear_stdout()


		if choice == 2:														# Add a password feature
			print(
				f"""\n------------------------\nYou are here to {Fore.GREEN + "add" + Style.RESET_ALL} the password of a specific site. (Type {Fore.RED + "back" + Style.RESET_ALL} to leave.)"""
			)

			i = 0
																	
			site = input(
				f"""Please tell the {Fore.CYAN + "site" + Style.RESET_ALL} you want to add a password for\n>> """ 	# retrieving site info
			)

			if site == "back" or site == "stop" or site == "retour":												# exit
				continue

			username = input( 																						# retrieving username info
				f"""Please tell your {Fore.CYAN + "username" + Fore.WHITE + " / " + Fore.CYAN + "email" + Style.RESET_ALL} on the site\n>> """
			)

			if username == "back" or username == "stop" or username == "retour":									# exit
				continue

			password = input( 																						# retrieving password info
				f"""Please tell your {Fore.CYAN + "password" + Style.RESET_ALL} related to the site\n>> """
			)

			if password == "back" or password == "stop" or password == "retour":									# exit
				continue

			
			program.add_site_password(given_password, site, password, username)
			program.check_data()																					# check data coherence (in some case, \n can be introduced unintentionally)


		if choice == 3:															# Filter search
			if program.get_props() == False:									# no current password...
				print(Back.RED + "Please first add passwords to filter them.")
				sleep(1.5)
				continue

			(lines, indexes) = program.passwords_content()

			if (lines, indexes) == (False, False):													
				continue

			if len(lines) == 0:													# no corresponding site
				print(
					f"""{Back.RED + "No result found with this filter.. Please retry"}"""
				)
				sleep(2)
				continue

			print(																# show result stat
				f"Site Filter: {Fore.MAGENTA + str(len(lines)) + rs} corresponding site(s)."
			)

			for i in range(len(lines)):											# print filtered sites
				print(lines[i])

			print(Fore.CYAN + " \tPress any key to leave")
			input()
			continue


		if choice == 4:															# Generate Password feature					
			password = program.generate_password(
				program.choose_security_level_password()
			)

			if password == None:												# go back
				continue

			print(																# show result
				f"""Here is the randomly generated password: (Press {Fore.MAGENTA + "CTRL + SHIFT + C" + Style.RESET_ALL} to copy)\n\n{password}\n\n"""
			)

			while True:															# do we save generated password ?
				to_save = input(
					"Would you like to add this password to your saved password? "
					+ Fore.CYAN
					+ "[Y/n] "
					+ Style.RESET_ALL
				)

				if to_save in ["Y", "y", "N", "n"]:
					if to_save in ["Y", "y"]:
						to_save = True

					if to_save in ["N", "n"]:
						to_save = False

					break

				print(Back.RED + "Invalid choice, please retry" + Style.RESET_ALL + "")

			if to_save:															# add password to saved password
				while True:														# retrieve info
					site = input(	
						f"""Please tell the {Fore.CYAN + "site" + Style.RESET_ALL} you want to add a password for\n>> """
					)

					if site == "back" or site == "stop" or site == "retour":
						program.clear_stdout()
						break

					username = input(
						f"""Please tell your {Fore.CYAN + "username" + Fore.WHITE + " / " + Fore.CYAN + "email" + Style.RESET_ALL} on the site\n>> """
					)

					if username == "back" or username == "stop" or username == "retour":
						program.clear_stdout()
						break

					program.add_site_password(
						given_password, site, password, username
					)

					program.check_data()
					program.clear_stdout()
					break


		if choice == 5:															# Change Username Feature
			print("\n------------------------\nPlease write down your new Username")

			new_username 	= input("\n>> ")									# retrieve new username
			good_one 		= program.confirm_username(new_username)			# confirm username

			program.set_username(good_one)										# set username

			print("\n")
			print(
				f"Here you go {program.get_username()}, your username has been changed."
			)

			sleep(2)


		if choice == 6:															# Modify Access Password
			print("\n------------------------\nAccessing Password modification...")
			program.change_access_password()									

			while True:													
				given_password = pwinput(										# prompt newly created Access Password
					prompt="- - - - - - - - - - - - - -\nPlease enter new password: "
				)

				if hashing(given_password) == program.get_hashed_password():	# newly created AP has been entered again, can continue
					program.clear_stdout()
					break

				else:															# wrong password, relaunch app
					print(
						Back.RED
						+ "Wrong password, please restart app."
						+ Style.RESET_ALL
						+ ""
					)

					sys.exit()


		if choice == 7:															# Access Tutorial feature
			program.tutorial()  


		if choice == 8:															# leave program feature
			print(Back.BLUE + f"See you soon {program.get_username()}!")
			sleep(1.5)
			break


		if choice == 9:															# Access System Settings feature
			recovery.system_settings()

	errors = recovery.error()
	if errors != True:															# new error: manage them before leaving
		recovery.error_resolution(errors)
