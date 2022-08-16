import sys, os, base64
from Crypto.Hash import SHA256
from MDPLogs.logs import Log
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from colorama import Back, Style, init

init(autoreset=True)

logs = Log()

def generate_salt():
    with open("MDPCrypto/key/key.key", 'wb') as file:
        file.write(os.urandom(16))

def get_salt():
    with open("MDPCrypto/key/key.key", 'rb') as file:
        salt = file.read()
    return salt

def encrypt(password: str, to_encrypt: str) -> str:
	try:
		password = password.encode()
		salt = get_salt()
		kdf = PBKDF2HMAC(
		algorithm=hashes.SHA256(),
		length=32,
		salt=salt,
		iterations=150000)
		key = base64.urlsafe_b64encode(kdf.derive(password))
		f = Fernet(key)
		token = f.encrypt(to_encrypt.encode())
		return token.decode()
	except:
		logs.create_log("There was an internal error [FATAL]. (Cryptography) Key.Key changes?")
		print(Back.RED + "There was an internal error [FATAL]. (Cryptography).If you wish to repair this fatal error, you must contact dev team:" + Style.RESET_ALL)
		print("\ngaecko8@gmail.com\n")
		print(f"""Please provide {Back.BLUE + "key.key" + Style.RESET_ALL} file located in {Back.CYAN + "./MDPCrypto/key/key.key" + Style.RESET_ALL} and {Back.BLUE + "logs.txt" + Style.RESET_ALL} located in {Back.CYAN + "./MDPLogs/log_file/logs.txt" + Style.RESET_ALL}""")
		print("The program won't work until devs find a solution...")
		sys.exit()

def decrypt(password: str, to_decrypt: str) -> str:
	try:
		password = password.encode()
		to_decrypt = to_decrypt.encode()
		salt = get_salt()
		kdf = PBKDF2HMAC(
		algorithm=hashes.SHA256(),
		length=32,
		salt=salt,
		iterations=150000)
		key = base64.urlsafe_b64encode(kdf.derive(password))
		f = Fernet(key)
		decrypted = f.decrypt(to_decrypt)
		return decrypted.decode()
	except:
		logs.create_log("There was an internal error [FATAL]. (Cryptography) Key.Key changes?")
		print(Back.RED + "There was an internal error [FATAL]. (Cryptography).If you wish to repair this fatal error, you must contact dev team:" + Style.RESET_ALL)
		print("\ngaecko8@gmail.com\n")
		print(f"""Please provide {Back.BLUE + "key.key" + Style.RESET_ALL} file located in {Back.CYAN + "./MDPCrypto/key/key.key" + Style.RESET_ALL} and {Back.BLUE + "logs.txt" + Style.RESET_ALL} located in {Back.CYAN + "./MDPLogs/log_file/logs.txt" + Style.RESET_ALL}""")
		print("The program won't work until devs find a solution...")
		sys.exit()

def hashing(to_hash):
    return SHA256.new(data=to_hash.encode()).hexdigest()

def low_hash(string):
	"""
	Not good hash !!
	"""
	def to_32(value):
		"""
		Fonction interne utilisée par hashing.
		Convertit une valeur en un entier signé de 32 bits.
		Si 'value' est un entier plus grand que 2 ** 31, il sera tronqué.

		:param (int) value: valeur du caractère transformé par la valeur de hachage de cette itération
		:return (int): entier signé de 32 bits représentant 'value'
		"""
		value = value % (2 ** 32)
		if value >= 2**31:
			value = value - 2 ** 32
		value = int(value)
		return value

	if string:
		x = ord(string[0]) << 7
		m = 1000003
		for c in string:
			x = to_32((x*m) ^ ord(c))
		x ^= len(string)
		if x == -1:
			x = -2
		return str(x)
	return ""
