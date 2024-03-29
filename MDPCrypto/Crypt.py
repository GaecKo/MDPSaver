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

import	base64
import	os
import	sys

from		colorama							import	Back, Fore, Style, init
from		Crypto.Hash							import	SHA256
from		cryptography.fernet					import	Fernet
from		cryptography.hazmat.primitives			import	hashes
from		cryptography.hazmat.primitives.kdf.pbkdf2		import	PBKDF2HMAC

from		MDPLogs.logs						import	Log

init(autoreset=True)
LOGS = Log()


def generate_salt():
	with open("MDPCrypto/key/key.key", "wb") as file:
		file.write(os.urandom(16))


def get_salt():
	with open("MDPCrypto/key/key.key", "rb") as file:
		salt = file.read()

	return salt


def load_key(password):
	password	= password.encode()
	salt		= get_salt()
	kdf		= PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=380000)
	key		= base64.urlsafe_b64encode(kdf.derive(password))
	return key


def encrypt(key, to_encrypt: str) -> str:
	try:
		f	= Fernet(key)
		token	= f.encrypt(to_encrypt.encode())

		return token.decode()
	
	except:
		LOGS.create_log(
			"There was an internal error [FATAL]. (Cryptography) Key.Key changes?"
		)

		print(
			Back.RED
			+ "There was an internal error [FATAL]. (Cryptography).If you wish to repair this fatal error, you must contact dev team:"
			+ Style.RESET_ALL
		)

		print("\n'gaecko' on Discord\n")
		print(
			Fore.RED
			+ "PLEASE FIRST TRY TO RELAUNCH THE SITE AND CHECK IF IT IS WORKING. IF NOT:"
		)

		print(
			f"""Please provide {Back.BLUE + "key.key" + Style.RESET_ALL} file located in {Back.CYAN + "./MDPCrypto/key/key.key" + Style.RESET_ALL} and {Back.BLUE + "LOGS.txt" + Style.RESET_ALL} located in {Back.CYAN + "./MDPLOGS/log_file/LOGS.txt" + Style.RESET_ALL}"""
		)

		print("The program won't work until devs find a solution...")


def decrypt(key, to_decrypt: str) -> str:
	try:
		f		= Fernet(key)
		decrypted	= f.decrypt(to_decrypt.encode())

		return decrypted.decode()
	
	except:
		LOGS.create_log(
			"There was an internal error [FATAL]. (Cryptography) Key.Key changes?"
		)

		print(
			Back.RED
			+ "There was an internal error [FATAL]. (Cryptography).If you wish to repair this fatal error, you must contact dev team:"
			+ Style.RESET_ALL
		)

		print("\n'gaecko' on Discord\n")

		print(
			Fore.RED
			+ "PLEASE FIRST TRY TO RELAUNCH THE SITE AND CHECK IF IT IS WORKING. IF NOT:"
		)

		print(
			f"""Please provide {Back.BLUE + "key.key" + Style.RESET_ALL} file located in {Back.CYAN + "./MDPCrypto/key/key.key" + Style.RESET_ALL} and {Back.BLUE + "LOGS.txt" + Style.RESET_ALL} located in {Back.CYAN + "./MDPLOGS/log_file/LOGS.txt" + Style.RESET_ALL}"""
		)

		print("The program won't work until devs find a solution...")


def try_decrypt(key, to_decrypt):
	"""
	if okay: return true, if not: return False
	"""
	try:
		f = Fernet(key)
		_ = f.decrypt(to_decrypt.encode())

		return True
	
	except:
		return False


def encrypt_extern_password(password: str, to_encrypt: str) -> str:
	try:
		password	= password.encode()
		salt		= get_salt()
		kdf		= PBKDF2HMAC(
			algorithm=hashes.SHA256(), length=32, salt=salt, iterations=380000
		)
		key		= base64.urlsafe_b64encode(kdf.derive(password))
		f		= Fernet(key)
		token		= f.encrypt(to_encrypt.encode())

		return token.decode()
	
	except:
		LOGS.create_log(
			"There was an internal error [FATAL]. (Cryptography) Key.Key changes?"
		)

		print(
			Back.RED
			+ "There was an internal error [FATAL]. (Cryptography).If you wish to repair this fatal error, you must contact dev team:"
			+ Style.RESET_ALL
		)

		print("\n'gaecko' on Discord\n")

		print(
			Fore.RED
			+ "PLEASE FIRST TRY TO RELAUNCH THE SITE AND CHECK IF IT IS WORKING. IF NOT:"
		)

		print(
			f"""Please provide {Back.BLUE + "key.key" + Style.RESET_ALL} file located in {Back.CYAN + "./MDPCrypto/key/key.key" + Style.RESET_ALL} and {Back.BLUE + "LOGS.txt" + Style.RESET_ALL} located in {Back.CYAN + "./MDPLOGS/log_file/LOGS.txt" + Style.RESET_ALL}"""
		)

		print("The program won't work until devs find a solution...")


def decrypt_extern_password(password: str, to_decrypt: str) -> str:
	try:
		password 	= password.encode()
		salt 		= get_salt()
		kdf 		= PBKDF2HMAC(
			algorithm=hashes.SHA256(), length=32, salt=salt, iterations=380000
		)
		key 		= base64.urlsafe_b64encode(kdf.derive(password))
		f 		= Fernet(key)
		decrypted 	= f.decrypt(to_decrypt.encode())

		return decrypted.decode()
	
	except:
		LOGS.create_log(
			"There was an internal error [FATAL]. (Cryptography) Key.Key changes?"
		)

		print(
			Back.RED
			+ "There was an internal error [FATAL]. (Cryptography).If you wish to repair this fatal error, you must contact dev team:"
			+ Style.RESET_ALL
		)

		print("\n'gaecko' on Discord\n")

		print(
			Fore.RED
			+ "PLEASE FIRST TRY TO RELAUNCH THE SITE AND CHECK IF IT IS WORKING. IF NOT:"
		)

		print(
			f"""Please provide {Back.BLUE + "key.key" + Style.RESET_ALL} file located in {Back.CYAN + "./MDPCrypto/key/key.key" + Style.RESET_ALL} and {Back.BLUE + "LOGS.txt" + Style.RESET_ALL} located in {Back.CYAN + "./MDPLOGS/log_file/LOGS.txt" + Style.RESET_ALL}"""
		)

		print("The program won't work until devs find a solution...")


def hashing(to_hash):
	return SHA256.new(data=to_hash.encode()).hexdigest()


def low_hash(string):
	"""
	Low hash, only to save low importance info !!
	"""

	def to_32(value):
		"""
		Fonction interne utilisée par hashing.
		Convertit une valeur en un entier signé de 32 bits.
		Si 'value' est un entier plus grand que 2 ** 31, il sera tronqué.

		:param (int) value: valeur du caractère transformé par la valeur de hachage de cette itération
		:return (int): entier signé de 32 bits représentant 'value'
		"""
		value = value % (2**32)
		if value >= 2**31:
			value = value - 2**32

		value = int(value)
		return value

	if string:
		x = ord(string[0]) << 7
		m = 1000003

		for c in string:
			x = to_32((x * m) ^ ord(c))

		x ^= len(string)

		if x == -1:
			x = -2

		return str(x)
	
	return ""
