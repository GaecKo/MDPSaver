# author: Arthur De Neyer - GaecKo
# last update: check github (https://github.com/GaecKo/MDPSaver)
#           ==== ⚠ DISCLAIMER ⚠ ====
# This part of the code concerns the security of the program. It uses verified and secured methods of
# famous modules (listed in the imports just below).
# In case of any suspicion on the system reliability and security, please open a new Issue on github.

import sys, os, base64
from Crypto.Hash import SHA256
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def load_key(password, salt) -> bytes:
    password = password.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=380000)
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key


def encrypt(key: bytes, to_encrypt: str) -> str:
    f = Fernet(key)
    token = f.encrypt(to_encrypt.encode())
    return token.decode()


def decrypt(key: bytes, to_decrypt: str) -> str:
    f = Fernet(key)
    decrypted = f.decrypt(to_decrypt.encode())
    return decrypted.decode()


def try_decrypt(key, to_decrypt):
    """
    if okay: return true, if not: return False
    """
    try:
        f = Fernet(key)
        decrypted = f.decrypt(to_decrypt.encode())
        return True
    except:
        return False


def encrypt_extern_password(password: str, to_encrypt: str, salt) -> str:
    password = password.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=380000)
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)
    token = f.encrypt(to_encrypt.encode())
    return token.decode()


def decrypt_extern_password(password: str, to_decrypt: str, salt) -> str:
    password = password.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=380000)
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)
    decrypted = f.decrypt(to_decrypt.encode())
    return decrypted.decode()


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
        if value >= 2 ** 31:
            value = value - 2 ** 32
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
