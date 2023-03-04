import sys, os, base64
from Crypto.Hash import SHA256
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
KEY_PATH = "key.key"

class MDPSecurity:
    def __init__(self, password):
        self.key = self.load_key(password)
        self.f = Fernet(self.key)
        del password
    
    def hashing(self, to_hash: str) -> str:
        return SHA256.new(data=to_hash.encode()).hexdigest()
    
    def generate_salt(self) -> None:
        with open(KEY_PATH, 'wb') as file:
            file.write(os.urandom(16))

    def get_salt(self) -> bytes:
        with open(KEY_PATH, 'rb') as file:
            salt = file.read()
        return salt
    
    def decrypt(self, key: bytes, to_decrypt: str) -> str:
        try: 
            decrypted = self.f.decrypt(to_decrypt.encode())
            return decrypted.decode()
        except:
            return False
        
    def encrypt(self, key: bytes, to_encrypt: str) -> str:
        try:
            token = self.f.encrypt(to_encrypt.encode())
            return token.decode()
        except:
            return False

    def load_key(self, password: str) -> bytes:
        password = password.encode()
        salt = self.get_salt()
        kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=380000)
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key